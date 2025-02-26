import os
import re
import html
import traceback
import mammoth
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from openpyxl import Workbook

# =============================
# == Marker Keys and Config ==
# =============================

PLAIN_TEXT_KEYS = [
    "Title & OG Title",
    "Description & OG Description",
    "URL & Canonical & OG URL",
    "CTA_URL",
    "CTA_TEXT",
    "ALT_txt",
    "Views",
    "Time_to_Read",
    "Publish date",
    "Category_Url",
    "Category_Text",
    "Speciality_look_up",
    "Location_look_up",
]

SCHEMA_KEYS = [
    "Breadcrumb Schema",
    "FAQ Schema"
]

RICH_HTML_KEYS = [
    "Embed Link"
]

MOBILE_STRIP_KEY = "Mobile Strip"

# All known keys
KNOWN_KEYS = PLAIN_TEXT_KEYS + SCHEMA_KEYS + RICH_HTML_KEYS + [MOBILE_STRIP_KEY]


# =============================
# == DOCX to HTML Conversion ==
# =============================

def generate_breadcrumb_bar(page_url):
    """
    Given a URL like 'https://www.medicoverhospitals.in/diseases/scalp-folliculitis/',
    returns a breadcrumb-bar HTML snippet.
    """
    parsed = urlparse(page_url)
    domain = f"{parsed.scheme}://{parsed.netloc}"
    path = parsed.path.strip("/")
    if not path:
        return f"""
<div class="breadcrumb-bar">
  <div class="container">
    <nav class="page-breadcrumb">
      <ol class="breadcrumb">
        <li class="breadcrumb-item active">Home</li>
      </ol>
    </nav>
  </div>
</div>
""".strip()

    segments = path.split("/")
    li_items = []
    home_item = f'<li class="breadcrumb-item"><a href="{domain}/">Home</a></li>'
    li_items.append(home_item)

    for i, seg in enumerate(segments):
        pretty_seg = seg.replace("-", " ").title()
        sub_path = "/".join(segments[: i + 1])
        full_link = f"{domain}/{sub_path}/"
        if i < len(segments) - 1:
            li = f'<li class="breadcrumb-item"><a href="{full_link}">{pretty_seg}</a></li>'
        else:
            li = f'<li class="breadcrumb-item active">{pretty_seg}</li>'
        li_items.append(li)

    li_html = "\n".join(li_items)
    breadcrumb_bar_html = f"""
<div class="breadcrumb-bar">
  <div class="container">
    <nav class="page-breadcrumb">
      <ol class="breadcrumb">
        {li_html}
      </ol>
    </nav>
  </div>
</div>
""".strip()

    return breadcrumb_bar_html


def convert_docx_to_html(docx_path):
    """Convert a DOCX file to HTML using Mammoth."""
    with open(docx_path, "rb") as docx_file:
        result = mammoth.convert_to_html(docx_file)
        return result.value


# ============================================
# == Unwrap Headings Inside Tables (Bug Fix) ==
# ============================================

def unwrap_headings_in_tables(soup):
    """
    Find any heading tags (h1-h4) that are nested within <table> elements,
    remove them from the table, and insert them immediately after the table.
    This helps prevent headings from being captured as part of the table's content.
    """
    for table in soup.find_all("table"):
        headings = table.find_all(["h1", "h2", "h3", "h4"])
        for heading in headings:
            heading.extract()  # Remove heading from table
            table.insert_after(heading)  # Insert heading immediately after the table
    return soup


# =============================
# == Section Extraction Logic ==
# =============================

def extract_sections_from_html(html_content):
    """
    Parse the HTML and split it into sections based on marker keys.
    This version filters out nested tags so that, for example, paragraphs inside a table are not
    collected separately from the table.
    """
    soup = BeautifulSoup(html_content, "html.parser")
    sections = {}

    # Collect all matching tags
    candidate_tags = soup.find_all(["p", "h1", "h2", "h3", "div", "ul", "ol", "table"])
    
    # Filter out tags nested within one of the candidate tags.
    all_tags = []
    for tag in candidate_tags:
        if not tag.find_parent(["p", "h1", "h2", "h3", "div", "ul", "ol", "table"]):
            all_tags.append(tag)

    markers = []
    for i, tag in enumerate(all_tags):
        text = tag.get_text(strip=True)
        if text in KNOWN_KEYS:
            markers.append((i, text))

    for j, (i, key) in enumerate(markers):
        start = i + 1
        end = markers[j+1][0] if j + 1 < len(markers) else len(all_tags)
        block_html = "".join(str(t) for t in all_tags[start:end]).strip()

        if key == MOBILE_STRIP_KEY:
            delimiter = "[[[[DELIMITER]]]]"
            parts = block_html.split(delimiter)
            if parts:
                sections[key] = parts[0].strip()
                if len(parts) > 1:
                    remainder = delimiter.join(parts[1:]).strip()
                    sections["content"] = sections.get("content", "") + remainder
            else:
                sections[key] = block_html
        elif key in PLAIN_TEXT_KEYS:
            stripped_text = " ".join(t.get_text(strip=True) for t in all_tags[start:end])
            sections[key] = stripped_text
        else:
            sections[key] = "".join(str(t) for t in all_tags[start:end]).strip()

    if markers:
        last_idx, last_key = markers[-1]
        if last_key != MOBILE_STRIP_KEY and last_idx < len(all_tags) - 1:
            leftover = "".join(str(t) for t in all_tags[last_idx+1:]).strip()
            if leftover:
                sections["content"] = sections.get("content", "") + leftover
    else:
        sections["content"] = html_content

    return sections


# =============================
# == Cleaning / Utility funcs ==
# =============================

def remove_all_p_tags(raw_html):
    """Remove <p> tags from raw_html."""
    unescaped = html.unescape(raw_html)
    no_ptags = re.sub(r"</?p[^>]*>", "", unescaped)
    return no_ptags.strip()

def clean_schema_field(raw_html):
    """For schema fields, remove <p> tags."""
    return remove_all_p_tags(raw_html)

def clean_rich_field(raw_html):
    """
    For rich HTML fields (such as Embed Link), unescape the HTML and,
    if an <iframe> element is present, return it as proper HTML.
    Otherwise, return the unescaped text directly.
    """
    unescaped = html.unescape(raw_html)
    soup = BeautifulSoup(unescaped, "html.parser")
    iframe = soup.find("iframe")
    if iframe:
        return str(iframe).strip()
    return unescaped.strip()

def clean_mobile_strip(raw_html):
    """
    Clean the Mobile Strip:
      - Extract the visible text as tokens (separated by '|').
      - Return the tokens text for navigation building.
    """
    # First, parse the HTML
    soup = BeautifulSoup(raw_html, "html.parser")
    
    # Find all text nodes that are not empty after stripping
    tokens = []
    for text in soup.stripped_strings:
        text = text.strip()
        if text and text not in {'|', '||'}:  # Skip delimiter characters
            tokens.append(text)
    
    # Join with the delimiter
    return " | ".join(tokens)

def clean_field(key, raw_html):
    """Clean content based on marker key."""
    if key in PLAIN_TEXT_KEYS:
        return BeautifulSoup(raw_html, "html.parser").get_text(strip=True)
    elif key in SCHEMA_KEYS:
        return clean_schema_field(raw_html)
    elif key in RICH_HTML_KEYS:
        return clean_rich_field(raw_html)
    elif key == MOBILE_STRIP_KEY:
        return clean_mobile_strip(raw_html)
    else:
        return raw_html

# NEW FUNCTION: Insert iframe before the first <h2>
def inject_iframe_before_first_h2(content_html, iframe_html):
    """
    Insert the iframe HTML right before the first <h2> element in the content.
    If no <h2> element is found, insert at the top.
    """
    if not iframe_html:
        return content_html
        
    soup = BeautifulSoup(content_html, "html.parser")
    h2_tag = soup.find("h2")
    iframe_soup = BeautifulSoup(iframe_html, "html.parser")
    
    if h2_tag:
        h2_tag.insert_before(iframe_soup)
        h2_tag.insert_before(soup.new_tag('br'))  # Add line break for spacing
    else:
        if soup.body:
            soup.body.insert(0, iframe_soup)
        else:
            soup.insert(0, iframe_soup)
    
    return str(soup)


# =============================
# == Mobile + Desktop Nav Build ==
# =============================

def should_separate_h1(page_url):
    """
    Returns True if the page URL is one where you want to extract and pass the H1 separately.
    """
    parsed = urlparse(page_url)
    parts = parsed.path.strip("/").split("/") if parsed.path.strip("/") else []
    if not parts:
        return False
    category = parts[0].lower()
    if category == "doctors":
        return True
    if category in ("diseases", "procedures") and len(parts) >= 3 and parts[2].lower() == "specialist":
        return True
    return False

def extract_h1(content_html):
    """
    Extracts the first <h1> from the content HTML and removes it.
    Returns a tuple: (h1_html, updated_content_html)
    """
    soup = BeautifulSoup(content_html, "html.parser")
    h1_tag = soup.find("h1")
    h1_html = ""
    if h1_tag:
        h1_html = str(h1_tag)
        h1_tag.decompose()
    return h1_html, str(soup)

def build_mobile_strip_nav(token_line):
    """
    Build mobile nav and desktop nav separately from the given tokens.
    Returns a tuple of (mobile_html, desktop_html)
    Book Appointment is only included in mobile navigation.
    """
    tokens = [t.strip() for t in token_line.split("|") if t.strip()]
    mobile_lines = []
    
    # Mobile navigation - includes Book Appointment
    for i, tok in enumerate(tokens):
        tok = tok.strip()
        if tok.lower() == "book appointment":
            mobile_lines.append(
                '<li><button data-target="#book-an-appointment" type="button" class="current">Book Appointment</button></li>'
            )
        else:
            link_id = make_id(tok)
            class_part = ' class="current"' if i == 0 else ""
            mobile_lines.append(
                f'<li><button{class_part} data-target="#{link_id}" type="button">{tok}</button></li>'
            )

    mobile_html = "\n      ".join(mobile_lines)
    
    # Desktop navigation - excludes Book Appointment
    desktop_lines = []
    for tok in tokens:
        tok = tok.strip()
        if tok.lower() != "book an appointment":  # Skip Book Appointment for desktop
            link_id = make_id(tok)
            desktop_lines.append(f'<a class="dropdown-item" href="#{link_id}">{tok}</a>')

    # Add FAQs link if not already present
    tokens_lower = [x.lower() for x in tokens]
    if "faqs" not in tokens_lower and "frequently asked questions" not in tokens_lower:
        desktop_lines.append('<a class="dropdown-item" href="#faqs">Frequently Asked Questions</a>')

    desktop_html = "\n    ".join(desktop_lines)

    return mobile_html, f"""
<div class="btn-group d-none d-lg-block">
  <div class="dropdown-menu section_optns d-block position-relative">
    {desktop_html}
  </div>
</div>
""".strip()

def build_desktop_nav(token_line):
    """
    Dedicated function that ONLY builds the desktop nav.
    """
    tokens = [t.strip() for t in token_line.split("|") if t.strip()]
    lines = []
    for t in tokens:
        if t.lower() not in {"book appointment"}:
            link_id = make_id(t)
            lines.append(f'<a class="dropdown-item" href="#{link_id}">{t}</a>')
    if "faqs" not in [x.lower() for x in tokens]:
        lines.append('<a class="dropdown-item" href="#faqS">Frequently Asked Questions</a>')
    combined = "\n".join(lines)
    return f"""
<div class="btn-group d-none d-lg-block">
  <div class="dropdown-menu section_optns d-block position-relative">
    {combined}
  </div>
</div>
""".strip()


# =============================
# == Headings + Link Remapping ==
# =============================

def make_id(token):
    """Convert a token into a valid HTML ID."""
    # Remove leading/trailing whitespace and convert to lowercase
    temp = token.strip().lower()
    # Remove any special characters except alphanumeric and spaces
    temp = re.sub(r"[^\w\s-]", "", temp)
    # Replace spaces with hyphens
    temp = re.sub(r"\s+", "-", temp)
    # Remove any leading or trailing hyphens
    temp = temp.strip("-")
    return temp

def flatten_heading(heading_tag):
    text_content = heading_tag.get_text(strip=True)
    heading_tag.clear()
    heading_tag.string = text_content

def assign_heading_ids(soup, tokens):
    """Assign IDs to headings that match the navigation tokens."""
    # First, clean up any existing IDs
    for heading in soup.find_all(["h1", "h2", "h3", "h4"]):
        for a in heading.find_all("a", attrs={"id": True}, recursive=False):
            a.decompose()
        flatten_heading(heading)

    # Create a mapping of normalized tokens to their original form
    token_map = {make_id(token): token for token in tokens}
    
    # First pass: try to match exact headings
    for heading in soup.find_all(["h2", "h3", "h4"]):
        heading_text = heading.get_text(strip=True)
        heading_id = make_id(heading_text)
        
        # If this heading matches a token exactly
        if heading_id in token_map:
            heading["id"] = heading_id
            print(f"[DEBUG] Assigned id='{heading_id}' to heading: '{heading_text}'")
            continue
        
        # Try partial matches
        for token_id, token in token_map.items():
            if token_id in heading_id or heading_id in token_id:
                heading["id"] = token_id
                print(f"[DEBUG] Assigned id='{token_id}' to heading: '{heading_text}' (partial match)")
                break

    # Second pass: try to find any unmatched tokens
    for token_id, token in token_map.items():
        # Skip "Book Appointment" as it's handled specially
        if token.lower() == "book appointment":
            continue
            
        # If we haven't found a match yet, look for partial matches in the content
        if not soup.find(id=token_id):
            pattern = re.compile(re.escape(token.lower()))
            for heading in soup.find_all(["h1", "h2", "h3", "h4"]):
                if pattern.search(heading.get_text(strip=True).lower()):
                    heading["id"] = token_id
                    print(f"[DEBUG] Assigned id='{token_id}' to heading: '{heading.get_text(strip=True)}' (fallback)")
                    break
            else:
                print(f"[WARN] No heading found for token '{token}'")

def remap_internal_links(soup, tokens):
    for token in tokens:
        norm = make_id(token)
        pattern = re.compile(r"\b" + re.escape(token.lower()) + r"\b")
        links = soup.find_all("a", string=lambda x: x and pattern.search(x.lower()))
        for link in links:
            old_href = link.get("href", "")
            if old_href.startswith("#"):
                link["href"] = f"#{norm}"
                print(f"[DEBUG] Link text='{link.get_text(strip=True)}' => href='#{norm}'")

def process_navigation_and_links(content_html, tokens):
    """Process the content HTML to add IDs to headings and remap internal links."""
    soup = BeautifulSoup(content_html, "html.parser")
    
    # Clean and normalize tokens
    cleaned_tokens = []
    for token in tokens:
        token = token.strip()
        if token and token.lower() != "book appointment":
            cleaned_tokens.append(token)
    
    # First pass: assign IDs to exact matches
    assign_heading_ids(soup, cleaned_tokens)
    
    # Second pass: ensure all headings have IDs
    for heading in soup.find_all(["h1", "h2", "h3", "h4"]):
        if not heading.get("id"):
            heading_text = heading.get_text(strip=True)
            heading["id"] = make_id(heading_text)
            print(f"[DEBUG] Assigned fallback id='{heading['id']}' to heading: '{heading_text}'")
    
    remap_internal_links(soup, cleaned_tokens)
    return str(soup)

# =============================
# == Duplicate <ul> Cleaner  ==
# =============================

def remove_duplicate_ul(raw_html):
    pattern = re.compile(r'((<ul>.*?</ul>)(\s*))+', re.DOTALL)
    def dedup(match):
        block = match.group(0)
        uls = re.findall(r'(<ul>.*?</ul>)', block, re.DOTALL)
        if uls:
            return uls[0]
        return block
    return pattern.sub(dedup, raw_html)

def wrap_ul_with_diseases_div(html_content, url):
    """Wrap <ul> elements based on the URL structure."""
    # Return early if the URL is empty or invalid
    if not url or not isinstance(url, str):
        print("[WARNING] Invalid or missing URL. Skipping <ul> wrapping.")
        return html_content

    soup = BeautifulSoup(html_content, 'html.parser')

    # Return early if there are no <ul> elements
    if not soup.find('ul'):
        print("[DEBUG] No <ul> elements found. Skipping wrapping.")
        return html_content

    # List of URL structures to match
    target_url_structures = [
        r"https://www\.medicoverhospitals\.in/procedures/.*/specialist/.*",
        r"https://www\.medicoverhospitals\.in/diseases/.*/specialist/.*",
        r"https://www\.medicoverhospitals\.in/doctors/.*/.*"
    ]

    # Check if the URL matches any of the target structures
    matches_structure = any(re.match(structure, url) for structure in target_url_structures)

    for ul in soup.find_all('ul'):
        # Skip if the <ul> is already wrapped in a 'dots' or 'diseases' div
        parent = ul.find_parent('div', class_=['dots', 'diseases'])
        if parent:
            print(f"[DEBUG] Skipping <ul> already wrapped in {parent.get('class')}")
            continue

        if matches_structure:
            # For URLs matching the structure: Wrap <ul> in a <div> with class 'dots'
            div = soup.new_tag('div', **{'class': 'dots'})
            ul.wrap(div)
        else:
            # For all other URLs: Add 'dots' class to <ul> and wrap in a <div> with class 'diseases'
            existing_classes = ul.get('class', [])
            ul['class'] = existing_classes + ['dots']  # Preserve existing classes
            div = soup.new_tag('div', **{'class': 'diseases'})
            ul.wrap(div)

    return str(soup)

def build_desktop_nav(token_line):
    """
    Dedicated function that ONLY builds the desktop nav.
    """
    tokens = [t.strip() for t in token_line.split("|") if t.strip()]
    lines = []
    for t in tokens:
        if t.lower() not in {"book appointment"}:
            link_id = make_id(t)
            lines.append(f'<a class="dropdown-item" href="#{link_id}">{t}</a>')
    if "faqs" not in [x.lower() for x in tokens]:
        lines.append('<a class="dropdown-item" href="#faqS">Frequently Asked Questions</a>')
    combined = "\n".join(lines)
    return f"""
<div class="btn-group d-none d-lg-block">
  <div class="dropdown-menu section_optns d-block position-relative">
    {combined}
  </div>
</div>
""".strip()

def wrap_tables_with_div(html_content):
    """
    Find every <table> element in the HTML, add a "table" class to it,
    and wrap it in a <div> with classes "scrollSlt table_div".
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    for table in soup.find_all('table'):
        classes = table.get('class', [])
        if "table" not in classes:
            classes.append("table")
        table['class'] = classes
        if not table.find_parent("div", class_="scrollSlt table_div"):
            wrapper = soup.new_tag('div', **{'class': 'scrollSlt table_div'})
            table.wrap(wrapper)
    return str(soup)


# =============================
# == Revised FAQ Extraction  ==
# =============================

def extract_faqs_from_content_accordion(content_html):
    """
    Extracts FAQs only if they appear after an <h2> whose text includes 
    "Frequently Asked Questions" (case-insensitive). Only <h3> tags with a question mark 
    in this section are treated as FAQ questions.
    
    Each FAQ is wrapped in a Bootstrap accordion item. The first FAQ is shown by default.
    
    Returns a tuple:
      (accordion_html, updated_content_html)
    where accordion_html is the complete accordion markup and updated_content_html is the content
    with the FAQ heading and FAQ items removed.
    """
    soup = BeautifulSoup(content_html, "html.parser")
    faq_heading = soup.find(lambda tag: tag.name == "h2" and 
                              "frequently asked questions" in tag.get_text(strip=True).lower())
    if not faq_heading:
        return "", content_html

    faq_items = []
    faq_counter = 1
    sibling = faq_heading.next_sibling
    # Iterate over siblings until we hit another <h2> or run out
    while sibling:
        if sibling.name == "h2":
            break
        if sibling.name == "h3":
            question_text = sibling.get_text(strip=True)
            if "?" in question_text:
                answer_el = sibling.find_next_sibling("p")
                answer_text = answer_el.get_text(strip=True) if answer_el else ""
                faq_id = f"faqs{faq_counter:02d}"
                # For the first FAQ, show it by default; others are collapsed.
                accordion_item = f'''
<div class="accordion-item">
  <h3 class="accordion-header">
    <button class="accordion-button{' collapsed' if faq_counter != 1 else ''}" type="button" data-bs-toggle="collapse" data-bs-target="#{faq_id}" aria-expanded="{'true' if faq_counter == 1 else 'false'}">
      {question_text}
    </button>
  </h3>
  <div id="{faq_id}" class="accordion-collapse collapse{' show' if faq_counter == 1 else ''}" data-bs-parent="#faqaccord">
    <div class="accordion-body py-2 px-0">
      <p>{answer_text}</p>
    </div>
  </div>
</div>
'''.strip()
                faq_items.append(accordion_item)
                faq_counter += 1
                sibling.decompose()
                if answer_el:
                    answer_el.decompose()
                sibling = faq_heading.next_sibling
                continue
        sibling = sibling.next_sibling

    # Remove the FAQ heading itself
    faq_heading.decompose()

    if faq_items:
        accordion_html = f'''
<div class="accordion cstm-accordion mb-4 pb-2" id="faqaccord">
{''.join(faq_items)}
</div>
'''.strip()
    else:
        accordion_html = ""

    return accordion_html, str(soup)


# =============================
# == PHP Template Generation ==
# =============================

def generate_php_file(template_path, output_path, sections):
    """Load the PHP template, replace placeholders, and write final .php."""
    with open(template_path, "r", encoding="utf-8") as f:
        template = f.read()

    # Get clean values for all fields
    title_plain = clean_field("Title & OG Title", sections.get("Title & OG Title", ""))
    description_plain = clean_field("Description & OG Description", sections.get("Description & OG Description", ""))
    url_plain = clean_field("URL & Canonical & OG URL", sections.get("URL & Canonical & OG URL", ""))
    cta_url = clean_field("CTA_URL", sections.get("CTA_URL", ""))
    cta_text = clean_field("CTA_TEXT", sections.get("CTA_TEXT", ""))
    alt_txt = clean_field("ALT_txt", sections.get("ALT_txt", ""))
    views = clean_field("Views", sections.get("Views", ""))
    time_to_read = clean_field("Time_to_Read", sections.get("Time_to_Read", ""))
    publish_date = clean_field("Publish date", sections.get("Publish date", ""))
    category_url = clean_field("Category_Url", sections.get("Category_Url", ""))
    category_text = clean_field("Category_Text", sections.get("Category_Text", ""))
    Speciality_look_up = clean_field("Speciality_look_up", sections.get("Speciality_look_up", ""))
    Location_look_up = clean_field("Location_look_up", sections.get("Location_look_up", ""))
    embed = clean_field("Embed Link", sections.get("Embed Link", ""))
    breadcrumb = clean_field("Breadcrumb Schema", sections.get("Breadcrumb Schema", ""))
    faq = clean_field("FAQ Schema", sections.get("FAQ Schema", ""))
    
    # Get the mobile strip content and clean it
    mobile_strip = clean_field("Mobile Strip", sections.get("Mobile Strip", ""))
    token_line = clean_mobile_strip(mobile_strip)
    
    # Print debug information
    print("[DEBUG] Extracted navigation tokens:", token_line)
    
    # Generate breadcrumb bar
    breadcrumbbar_html = generate_breadcrumb_bar(url_plain)
    
    # Generate mobile and desktop navigation
    mobile_nav, desktop_nav = build_mobile_strip_nav(token_line)

    main_content = sections.get("content", "").strip()

    # Extract FAQs and update content if FAQs are found
    faq_section = ""
    if "FAQ Schema" in sections:
        faq_section, main_content = extract_faqs_from_content_accordion(main_content)

    # Process content for navigation and links
    tokens = [t.strip() for t in token_line.split("|") if t.strip()]
    main_content = process_navigation_and_links(main_content, tokens)

    # Insert iframe before first H2
    main_content = inject_iframe_before_first_h2(main_content, embed)

    # Wrap tables with scrollable divs
    main_content = wrap_tables_with_div(main_content)

    # Clean up any duplicate ULs that might have been created
    main_content = remove_duplicate_ul(main_content)
    main_content = wrap_ul_with_diseases_div(main_content, url_plain)

    # Determine CTA includes based on URL
    cta_top, cta_bottom = determine_cta_includes(url_plain)
    
    # Insert CTAs into content at appropriate positions
    if cta_top and cta_bottom:
        main_content = insert_cta_in_content(main_content, cta_top, cta_bottom)

    # Optionally extract and separate H1 if needed
    h1_html = ""
    if should_separate_h1(url_plain):
        h1_html, main_content = extract_h1(main_content)

    # Generate image URL if needed
    image_url = generate_image_url(url_plain)

    # Template replacements
    replacements = {
        "%%TITLE%%":             title_plain,
        "%%META_DESCRIPTION%%":  description_plain,
        "%%OG_TITLE%%":         title_plain,
        "%%OG_DESCRIPTION%%":   description_plain,
        "%%CANONICAL_URL%%":    url_plain,
        "%%OG_URL%%":           url_plain,
        "%%BREADCRUMB_SCHEMA%%":  breadcrumb,
        "%%FAQ_SCHEMA%%":         faq,
        "%%MOBILE_STRIP%%":       mobile_nav,
        "%%DESKTOP_STRIP%%":      desktop_nav,
        "%%Main_content%%":       main_content,
        "%%Faq_html%%":           faq_section,
        "%%breadcrumbbar%%":      breadcrumbbar_html,
        "%%CTA_URL%%":            cta_url,
        "%%CTA_TEXT%%":           cta_text,
        "%%ALT_txt%%":           alt_txt,
        "%%alt_text%%":           alt_txt,        # Adding lowercase version
        "%%Views%%":             views,
        "%%views%%":             views,          # Adding lowercase version
        "%%Time_to_Read%%":      time_to_read,
        "%%time_to_read%%":      time_to_read,   # Adding lowercase version
        "%%Publish_date%%":      publish_date,
        "%%publish_date%%":      publish_date,   # Adding lowercase version
        "%%published_date%%":    publish_date,   # Adding alternative version
        "%%Category_Url%%":      category_url,
        "%%Category_Text%%":     category_text,
        "%%category_text%%":     category_text,  # Adding lowercase version
        "%%Speciality_look_up%%": Speciality_look_up,
        "%%Location_look_up%%":   Location_look_up,
        "%%Embed_Link%%":        embed,
        "%%image_url%%":         image_url,
        "%%H1%%":               h1_html,
        "%%speciality_look_up%%": Speciality_look_up
    }
    
    # Print debug information about replacements
    print("\n[DEBUG] Template Replacement Values:")
    for key, value in replacements.items():
        if value:  # Only print non-empty values
            print(f"  {key}: {value[:50]}{'...' if len(value) > 50 else ''}")
    
    for placeholder, value in replacements.items():
        template = template.replace(placeholder, value)
    
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(template)


# =============================
# == Filename Helper         ==
# =============================

def determine_output_filename(page_url, fallback_name):
    """
    Determine the output file path based on the URL.
    """
    base_folder = "dot_php_files"
    parsed = urlparse(page_url)
    parts = parsed.path.strip("/").split("/") if parsed.path.strip("/") else []
    trailing = page_url.endswith("/")

    if not parts:
        return os.path.join(base_folder, "index.php")

    category = parts[0].lower()

    if category == "articles":
        if len(parts) >= 2:
            return os.path.join(base_folder, "articles", parts[1] + ".php")
        else:
            return os.path.join(base_folder, "articles", "index.php")

    elif category == "diseases":
        if len(parts) == 2:
            return os.path.join(base_folder, "diseases", parts[1], "index.php") if trailing else os.path.join(base_folder, "diseases", parts[1] + ".php")
        elif len(parts) == 3:
            return os.path.join(base_folder, "diseases", parts[1], parts[2], "index.php") if trailing else os.path.join(base_folder, "diseases", parts[1], parts[2] + ".php")
        elif len(parts) == 4:
            return os.path.join(base_folder, "diseases", parts[1], parts[2], parts[3] + ".php")
        else:
            return os.path.join(base_folder, "diseases", *parts[1:]) + ("/index.php" if trailing else ".php")

    elif category == "hospitals":
        if len(parts) == 3:
            return os.path.join(base_folder, "hospitals", parts[1], parts[2], "index.php") if trailing else os.path.join(base_folder, "hospitals", parts[1], parts[2] + ".php")
        elif len(parts) >= 4:
            return os.path.join(base_folder, "hospitals", parts[1], parts[2], parts[3] + ".php")
        else:
            return os.path.join(base_folder, "hospitals", *parts[1:]) + ("/index.php" if trailing else ".php")

    elif category == "procedures":
        if len(parts) == 2:
            return os.path.join(base_folder, "procedures", parts[1], "index.php") if trailing else os.path.join(base_folder, "procedures", parts[1] + ".php")
        elif len(parts) == 3:
            return os.path.join(base_folder, "procedures", parts[1], parts[2], "index.php") if trailing else os.path.join(base_folder, "procedures", parts[1], parts[2] + ".php")
        elif len(parts) == 4:
            return os.path.join(base_folder, "procedures", parts[1], parts[2], parts[3] + ".php")
        else:
            return os.path.join(base_folder, "procedures", *parts[1:]) + ("/index.php" if trailing else ".php")

    elif category == "symptoms":
        if len(parts) == 2:
            return os.path.join(base_folder, "symptoms", parts[1] + ".php")
        else:
            return os.path.join(base_folder, "symptoms", *parts[1:]) + ("/index.php" if trailing else ".php")

    elif category == "doctors":
        if len(parts) == 2:
            return os.path.join(base_folder, "doctors", parts[1], "index.php") if trailing else os.path.join(base_folder, "doctors", parts[1] + ".php")
        elif len(parts) == 3:
            return os.path.join(base_folder, "doctors", parts[1], parts[2] + ".php")
        else:
            return os.path.join(base_folder, "doctors", *parts[1:]) + ("/index.php" if trailing else ".php")

    elif category == "specialties":
        if len(parts) == 2:
            return os.path.join(base_folder, "specialties", parts[1] + ".php")
        else:
            return os.path.join(base_folder, "specialties", *parts[1:]) + ("/index.php" if trailing else ".php")

    elif category == "medicine":
        if len(parts) == 2:
            return os.path.join(base_folder, "medicine", parts[1] + ".php")
        else:
            return os.path.join(base_folder, "medicine", *parts[1:]) + ("/index.php" if trailing else ".php")

    elif category == "diagnostics-pathology-tests":
        if len(parts) == 2:
            return os.path.join(base_folder, "diagnostics-pathology-tests", parts[1] + ".php")
        else:
            return os.path.join(base_folder, "diagnostics-pathology-tests", *parts[1:]) + ("/index.php" if trailing else ".php")

    elif category == "surgery-cost":
        if len(parts) == 2:
            return os.path.join(base_folder, "surgery-cost", parts[1] + ".php")
        else:
            return os.path.join(base_folder, "surgery-cost", *parts[1:]) + ("/index.php" if trailing else ".php")

    else:
        return os.path.join(base_folder, os.path.splitext(fallback_name)[0] + ".php")


def determine_template(page_url):
    """
    Choose the PHP template based on the URL's path.
    """
    parsed = urlparse(page_url)
    parts = parsed.path.strip("/").split("/") if parsed.path.strip("/") else []
    if not parts:
        return "default.php"

    category = parts[0].lower()

    if category == "articles":
        return "Templates/articles.php"

    elif category == "diseases":
        if len(parts) == 2:
            return "Templates/diseases.php"
        elif len(parts) == 3:
            return "Templates/diseaseindia.php"
        elif len(parts) == 4:
            return "Templates/diseaselocation.php"
        else:
            return "Templates/diseases.php"

    elif category == "hospitals":
        if len(parts) == 3:
            return "Templates/hospitallocation.php"
        elif len(parts) >= 4:
            return "Templates/hospitallocationspeciality.php"
        else:
            return "Templates/hospitallocation.php"

    elif category == "procedures":
        if len(parts) == 2:
            return "Templates/procedures.php"
        elif len(parts) == 3:
            return "Templates/proceduresindia.php"
        elif len(parts) == 4:
            return "Templates/procedureslocation.php"
        else:
            return "Templates/procedures.php"

    elif category == "symptoms":
        return "Templates/symptoms.php"

    elif category == "doctors":
        if len(parts) == 2:
            return "Templates/doctorspeciality.php"
        elif len(parts) == 3:
            return "Templates/doctorspecialitylocation.php"
        else:
            return "Templates/doctorspeciality.php"

    elif category == "specialties":
        return "Templates/speciality.php"

    elif category == "medicine":
        return "Templates/medicine.php"

    elif category == "diagnostics-pathology-tests":
        return "Templates/diagnostics.php"

    elif category == "surgery-cost":
        return "Templates/surgerycost.php"

    else:
        return "default.php"
    
def determine_cta_includes(page_url):
    """
    Based on the URL structure, return a tuple (cta_top, cta_bottom) with proper PHP include statements.
    """
    parsed = urlparse(page_url)
    parts = parsed.path.strip("/").split("/") if parsed.path.strip("/") else []
    if not parts:
        relative = "../"
    else:
        category = parts[0].lower()
        if category == "articles":
            relative = "../"
        elif category == "diseases":
            if len(parts) == 2:
                relative = "../../"
            elif len(parts) == 3:
                relative = "../../../"
            elif len(parts) >= 4:
                relative = "../../../"
            else:
                relative = "../"
        elif category == "hospitals":
            if len(parts) == 3:
                relative = "../../"
            elif len(parts) >= 4:
                relative = "../../../"
            else:
                relative = "../"
        elif category == "procedures":
            if len(parts) in [2, 3]:
                relative = "../../"
            elif len(parts) >= 4:
                relative = "../"
            else:
                relative = "../"
        elif category == "doctors":
            if len(parts) == 2:
                relative = "../"
            elif len(parts) >= 3:
                relative = "../../"
            else:
                relative = "../"
        else:
            relative = "../"
    cta_top   = f'<?php include "{relative}include/symptoms-ctaadvtop.php" ?>'
    cta_bottom = f'<?php include "{relative}include/symptoms-ctaadvbtm.php" ?>'
    return cta_top, cta_bottom

def insert_cta_in_content(content_html, cta_top, cta_bottom):
    """
    Inserts the CTA include snippets into the content HTML based on the conditions:
      - CTA 1: Top of the second H2 if there are 2 or more H2s.
      - CTA 2: Top of the last H2 if there are 3 or more H2s.
    """
    soup = BeautifulSoup(content_html, "html.parser")
    
    # Find all H2 tags
    h2_tags = soup.find_all("h2")
    h2_count = len(h2_tags)
    
    # Insert CTA 1: Top of the second H2 if there are 2 or more H2s
    if h2_count >= 2:
        second_h2 = h2_tags[1]  # Index 1 is the second H2
        second_h2.insert_before(BeautifulSoup(cta_top, "html.parser"))
    
    # Insert CTA 2: Top of the last H2 if there are 3 or more H2s
    if h2_count >= 3:
        last_h2 = h2_tags[-1]  # Last H2
        last_h2.insert_before(BeautifulSoup(cta_bottom, "html.parser"))
    
    return str(soup)


def generate_image_url(og_url):
    """
    Given an OG URL, returns an image URL by prepending '/images' to the path and
    appending '.webp' if necessary.
    """
    parsed = urlparse(og_url)
    new_path = "/images" + parsed.path
    if not new_path.endswith(".webp"):
        new_path += ".webp"
    return f"{parsed.scheme}://{parsed.netloc}{new_path}"


# =============================
# == Main Orchestrator       ==
# =============================

def main():
    doc_folder = "doc_files"
    output_folder = "dot_php_files"
    log_file = "generation_log.xlsx"

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    wb = Workbook()
    ws = wb.active
    ws.append(["URL", "Status"])

    for filename in os.listdir(doc_folder):
        if filename.lower().endswith(".docx"):
            doc_path = os.path.join(doc_folder, filename)
            try:
                html_content = convert_docx_to_html(doc_path)
                soup = BeautifulSoup(html_content, "html.parser")
                soup = unwrap_headings_in_tables(soup)
                html_content = str(soup)
                
                sections = extract_sections_from_html(html_content)
                page_url = sections.get("URL & Canonical & OG URL", "")
                template_file = determine_template(page_url)
                output_filename = determine_output_filename(page_url, filename)
                output_path = os.path.join(output_folder, output_filename)

                output_dir = os.path.dirname(output_path)
                if not os.path.exists(output_dir):
                    os.makedirs(output_dir, exist_ok=True)

                print(f"\n[INFO] Processing '{filename}' => '{output_filename}' using template '{template_file}'")
                generate_php_file(template_file, output_path, sections)
                ws.append([page_url, "Success"])
                print(f"[SUCCESS] Generated '{output_filename}'")
            except Exception as e:
                error_msg = f"Error: {str(e)}"
                ws.append([sections.get("URL & Canonical & OG URL", ""), error_msg])
                print(f"[FAIL] Processing '{filename}': {error_msg}")
                traceback.print_exc()

    wb.save(log_file)
    print(f"[INFO] Excel log saved to {log_file}")


if __name__ == "__main__":
    main()
