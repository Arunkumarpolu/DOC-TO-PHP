<!DOCTYPE html>
<html lang="en">
<head>
  <!-- Google Analytics -->
  <script async src="https://www.googletagmanager.com/gtag/js?id=G-79Z2DRYPBW"></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){dataLayer.push(arguments);}
    gtag("js", new Date());
    gtag("config", "G-79Z2DRYPBW");
  </script>

  <meta charset="UTF-8">
  <title>%%TITLE%%</title>
  <meta name="description" content="%%META_DESCRIPTION%%">
  <meta name="robots" content="index, follow">
  <meta property="og:title" content="%%OG_TITLE%%">
  <meta property="og:description" content="%%OG_DESCRIPTION%%">
  <meta property="og:type" content="website">
  <meta property="og:url" content="%%OG_URL%%">
  <meta property="og:image" content="%%image_url%%">
  <meta property="og:image:width" content="132">
  <meta property="og:image:height" content="80">
  <link rel="canonical" href="%%CANONICAL_URL%%">
  
  <!-- Breadcrumb Schema JSON-LD -->
  %%BREADCRUMB_SCHEMA%%
  
  <!-- FAQ Schema JSON-LD -->
  %%FAQ_SCHEMA%%
  
  <?php include "../../../include/header-specialist.php"; ?>
</head>
<body>

  <!-- Breadcrumb Bar -->
  %%breadcrumbbar%%

  <section class="goto-sec goto-mob d-lg-none fixednav">
	<div class="container">
        <ul class="mn_nav">
        %%MOBILE_STRIP%%
        </ul>
	</div>
</section>


  <section class="doc-list-card">
    <div class="container">
      <div class="row g-3 g-xl-4">
        <div class="col-xl-9 col-lg-8">
          <div class="row">
            <div class="col-md-8 col-lg-8 col-xl-8 col-sm-12">
              <!-- H1 Heading (if separated) -->
              %%H1%%
            </div>
            <div class="col-md-4 col-sm-12">
              <div class="form-group card-label">
                <?php $speciality = "orthopedics"; include("../../../include/locationdropdown.php"); ?>
              </div>
            </div>
          </div>
          <?php
            $location = "pune";
            $speciality = "orthopedics";
            include("../../../include/doctors-newdisplay.php");
          ?>
          
          <!-- Main Content from DOCX -->
          %%Main_content%%
          </div>
          <div class="col-xl-3 col-lg-4" id="book-an-appointment">
          <div class="d-none d-lg-block mb-4">
            <div class="section_optns d-block position-relative">
            %%DESKTOP_STRIP%%
            </div>
          </div>

          <script type="text/javascript" defer>
            $(document).ready(function() {
              // Desktop navigation click handler
              $(".section_optns a").on("click", function(e) {
                e.preventDefault();
                var target = $(this).attr("href");
                scrollToSection(target);
              });

              // Mobile navigation click handler
              $(".mn_nav button").on("click", function(e) {
                e.preventDefault();
                var target = $(this).attr("data-target");
                scrollToSection(target);
              });
            });

            function scrollToSection(target) {
              if (!target) return;
              
              // Remove the initial # if present
              var sectionId = target.replace(/^#+/, '');
              var section = document.getElementById(sectionId);
              
              if (section) {
                var offset = 120; // Adjust this value based on your header height
                var sectionTop = $(section).offset().top - offset;
                
                $("html, body").animate({
                  scrollTop: sectionTop
                }, 800, function() {
                  // Update URL hash after scrolling
                  if (history.pushState) {
                    history.pushState(null, null, '#' + sectionId);
                  } else {
                    location.hash = '#' + sectionId;
                  }
                });
              }
            }

            // Mobile menu toggle
            $(document).ready(function() {
              $("#mobile_btn").click(function() {
                $(".mn_nav").slideToggle();
              });
            });
          </script>
          <?php include "../../../include/book-an-appointment.php"; ?>
        </div>
      </div>
    </div>
  </section>
  
  <?php include "../../../include/contactstrip-new.php"; ?>
  
  <section>
    <div class="container">
      <div class="col-md-12 col-sm-12">
        <h2 class="htitle" id="faqs">Frequently Asked Questions</h2>
        <!-- FAQ Accordion generated dynamically -->
        %%Faq_html%%
      </div>
    </div>
  </section>
  
  <?php include "../../../include/footer1.php"; ?>
</body>
</html>
