# DOCX to PHP Converter

This project is an automated tool designed to convert Word documents (DOCX) into PHP web pages, specifically tailored for medical content management. It's particularly useful for converting medical articles, disease information, and FAQs into web-ready PHP pages with proper formatting and navigation.

## Features

- Converts DOCX files to structured PHP web pages
- Automatically generates:
  - Mobile and desktop navigation
  - Breadcrumb navigation
  - FAQ sections with accordion functionality
  - SEO-friendly metadata
  - Schema markup
- Handles special content types:
  - Tables (with responsive scrolling)
  - Embedded iframes
  - CTAs (Call-to-Action buttons)
  - Lists and navigation elements
- Supports multiple template types based on URL structure
- Maintains consistent formatting and styling

## Project Structure

- `Templates/` - Contains PHP template files
- `doc_files/` - Directory for input DOCX files
- `dot_php_files/` - Directory for output PHP files
- `main_final_with_Accordian.py` - Main conversion script
- `generation_log.xlsx` - Logs the conversion process

## Requirements

- Python 3.x
- Required Python packages:
  - mammoth (for DOCX to HTML conversion)
  - beautifulsoup4 (for HTML parsing)
  - openpyxl (for Excel log handling)

## Usage

1. Place your DOCX files in the `doc_files` directory

2. Run the main script:
   ```bash
   python main_final_with_Accordian.py
   ```

3. The script will:
   - Convert DOCX files to HTML
   - Process the content according to predefined markers
   - Generate appropriate PHP files in the `dot_php_files` directory
   - Create a log entry in `generation_log.xlsx`

## Content Structure

Your DOCX files should include the following markers for proper conversion:

### Plain Text Fields:
- Title & OG Title
- Description & OG Description
- URL & Canonical & OG URL
- CTA_URL
- CTA_TEXT
- ALT_txt
- Views
- Time_to_Read
- Publish date
- Category_Url
- Category_Text
- Speciality_look_up
- Location_look_up

### Special Sections:
- Breadcrumb Schema
- FAQ Schema
- Embed Link
- Mobile Strip

## Output

The generated PHP files will include:
- Properly formatted HTML content
- SEO metadata
- Schema markup
- Mobile and desktop navigation
- Responsive design elements
- Integrated CTAs
- FAQ sections (if present)

## Logging

The conversion process is logged in `generation_log.xlsx`, which tracks:
- Input file names
- Output locations
- Conversion status
- Any errors encountered

## Notes

- Ensure your DOCX files follow the required structure with proper markers
- FAQs should be under a heading containing "Frequently Asked Questions"
- Tables are automatically made responsive
- Internal links are remapped to match the navigation structure
