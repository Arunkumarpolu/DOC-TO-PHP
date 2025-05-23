<!DOCTYPE html>
<html lang="en">
  <head>
    <!-- Google tag (gtag.js) -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-79Z2DRYPBW"></script>
    <script>
      window.dataLayer = window.dataLayer || [];

      function gtag() {
        dataLayer.push(arguments);
      }
      gtag('js', new Date());
      gtag('config', 'G-79Z2DRYPBW');
    </script>
    <meta charset="UTF-8">	
<title>%%TITLE%%</title>
<meta name="description" content="%%META_DESCRIPTION%%">
<meta name="keywords" content="">
<meta name="author" content="Medicover Hospitals">
<link rel="canonical" href="%%CANONICAL_URL%%"/>
<meta property="og:title" content="%%OG_TITLE">
<meta property="og:description" content="%%OG_DESCRIPTION%%">
<meta property="og:image" content="https://www.medicoverhospitals.in/images/resources/medicover-hospitals-logo.webp">
<meta property="og:image:width" content="132"/>
<meta property="og:image:height" content="80"/>
<meta property="og:url" content="%%OG_URL%%">

<!-- <script> -->
%%FAQ_SCHEMA%%

%%BREADCRUMB_SCHEMA%%
    <?php include "../include//header1.php" ?>

    %%breadcrumbbar%%
    <section class="goto-sec2 d-lg-none">
      <div class="container position-relative">
        <ul class="mn_nav">
        %%MOBILE_STRIP%%
        </ul>
      </div>
    </section>
    <script type="text/javascript" defer>
      $(document).ready(function() {
        $('.mn_nav>li>button, .mn_nav>li>a').on('click', function(e) {
          e.preventDefault();
          var target = $(this).attr("data-target") || $(this).attr("href");
          scrollToSection(target);
          // Remove 'current' class from all buttons and add to the clicked one
          $('.mn_nav>li>button.current, .mn_nav>li>a.current').removeClass('current');
          $(this).addClass('current');
        });
        $(window).scroll(function() {
          var scrollDistance = $(window).scrollTop();
          $('.sec-scrl').each(function(i) {
            if ($(this).position().top - getOffset() <= scrollDistance + 1) {
              $('.mn_nav>li>button.current, .mn_nav>li>a.current').removeClass('current');
              var sectionId = $(this).attr('id');
              $('.mn_nav>li>button[data-target="#' + sectionId + '"], .mn_nav>li>a[data-target="#' + sectionId + '"]').addClass('current');
            }
          });
        }).scroll();
      });

      function getOffset() {
        // Adjust offset for desktop and mobile views
        var isMobile = $(window).width() <= 992;
        return isMobile ? 145 : 200; // Adjust values as needed
      }

      function scrollToSection(sectionId) {
        var sectionAndPart = sectionId.split('#');
        var section = document.getElementById(sectionAndPart[0].replace('#', ''));
        if (section) {
          var sectionTop = $(section).offset().top - getOffset();
          $('html, body').stop().animate({
            scrollTop: sectionTop
          }, 600, function() {
            // Update the URL with both section and part identifiers
            var newUrl = window.location.href.split('#')[0] + '#' + sectionAndPart.join('');
            history.pushState(null, null, newUrl);
          });
        }
      }
    </script>
    <section class="diseases-detail">
      <div class="container">
        <div class="card top-banner-card banner-card-background3 top-banner-card-padding">
          <div class="card-body">
            <div class="blog-view">
              <div class="blog blog-single-post">
                <h1 id="overview">%%H1%%</h1>
              </div>
            </div>
          </div>
        </div>
        <div class="row g-3 g-xl-4 mt-0">
          <div class="col-xl-9 col-lg-8">
            <div class="card main-card">
              <div class="card-body">
                <div class="blog-view">
                  <div class="blog blog-single-post">
                    <div class="blog-content">
                      <div class="row">
                        <div class="col-12 col-lg-7  content-col">
                        %%Main_content%%
                        <div class="col-12 col-lg-5  image-col">
                            <img src="images2/articl2.webp" class="img-fluid" alt="Alt Text" onerror="handleImageError(this)">
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
          <div class="col-xl-3 col-lg-4 sec-scrl" id="book-an-appointment">
              %%DESKTOP_STRIP%%
             <?php include "../include/book-an-appointment.php" ?>
          </div>
        </div>
      </div>
    </section>
<script>
  function handleImageError(img) {
    const imageCol = img.closest('.image-col');
    const blogContent = img.closest('.blog-content');
    if (!blogContent) return;

    const contentCol = blogContent.querySelector('.content-col');

    // Hide the image column
    if (imageCol) {
      imageCol.style.display = 'none';
    }

    // Expand the content column
    if (contentCol) {
      contentCol.classList.remove('col-lg-7');
      contentCol.classList.add('col-lg-12');
    }
  }
</script>


    <?php include "../include/contactstrip-new.php" ?>

<!-- faq-section *****  faq-section   **********  faq-section **** -->
<section id="faqs">
    <div class="container">
      <h2>Frequently Asked Questions</h2>
      %%Faq_html%%
      <hr>
<div class="container-fluid disclaimer"><p>Disclaimer: The information provided herein is accurate, updated and complete as per the best practices of the Company. Please note that this information should not be treated as a replacement for physical medical consultation or advice. We do not guarantee the accuracy and the completeness of the information so provided. The absence of any information and/or warning to any drug shall not be considered and assumed as an implied assurance of the Company. We do not take any responsibility for the consequences arising out of the aforementioned information and strongly recommend you for a physical consultation in case of any queries or doubts.</p></div></div>

    </div>
</section> 
    <?php include "../include/footer1.php" ?>