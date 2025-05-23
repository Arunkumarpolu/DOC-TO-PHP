<!DOCTYPE html>
<html lang="en">
<head>
  <!-- Google tag (gtag.js) -->
  <script src="https://www.googletagmanager.com/gtag/js?id=G-79Z2DRYPBW"></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){dataLayer.push(arguments);}
    gtag('js', new Date());
    gtag('config', 'G-79Z2DRYPBW');
  </script>
  <meta charset="UTF-8">  
  <title>%%TITLE%%</title>
  <meta name="description" content="%%META_DESCRIPTION%%">

  <!-- responsive meta -->  
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta http-equiv="X-UA-Compatible" content="IE=edge">   
  <meta property="og:locale" content="en_US"/>
  <meta property="og:type" content="website">
  <meta property="og:title" content="%%OG_TITLE%%">
  <meta property="og:description" content="%%OG_DESCRIPTION%%">
  <meta property="og:url" content="%%OG_URL%%">
  <meta property="og:site_name" content="Best Hospitals in India | Medicover Hospitals">
  <meta property="og:image" content="https://www.medicoverhospitals.in/images/resources/medicover-hospitals-logo.webp">
  <meta property="og:image:width" content="132"/>
  <meta property="og:image:height" content="80"/>
  <!--canonical-->
  <link rel="canonical" href="%%CANONICAL_URL%%"/>
 
  <!-- <script> -->
  
  %%BREADCRUMB_SCHEMA%%

  %%FAQ_SCHEMA%%

  <?php include "../../../include/header-symptoms-mob.php" ?>

%%breadcrumbbar%%

<section class="goto-sec d-lg-none">
  <div class="container position-relative">
    <ul class="mn_nav"> 
    %%MOBILE_STRIP%%
    </ul>
    <div id="mobile_btn" class="d-lg-none"><i class="fa fa-bars"></i></div>
  </div>
</section>

<script type="text/javascript">
  $('.mn_nav>li>button').click(function() {
    if ($(window).width() <= 575) {
      $('html, body').animate({
          scrollTop: $($(this).attr('data-target')).offset().top - 150
      }, 500);
    } else if ($(window).width() <= 767) {
      $('html, body').animate({
          scrollTop: $($(this).attr('data-target')).offset().top - 135
      }, 500);
    } else {
      $('html, body').animate({
          scrollTop: $($(this).attr('data-target')).offset().top - 120
      }, 500);
    }
    $(this).parent().siblings().children().removeClass('current');
    $(this).addClass('current');
    return false;
  });
</script>


<section class="specialist-detail-section">
  <div class="container">
    <div class="row g-3 g-xl-4">
      <div class="col-xl-9 col-lg-8">
        <div class="card">
          <div class="card-body">
            <div class="diseases">
              <div class="blog-content">
              %%Main_content%%
                </div> <!-- .blog-content -->
              </div> <!-- .blog-content -->
            </div> <!-- .diseases -->
          </div> <!-- .card-body -->
        </div> <!-- .card -->

      <div class="col-xl-3 col-lg-4 sec-scrl" id="book-an-appointment">
        <a href="%%CTA_URL%%">
          <button type="button" class="btn" style="background-color: rgb(244,129,32); font-size: 13px; font-weight: bold; color: white;">
            %%CTA_TEXT%%
          </button>
        </a>
        <hr>
        <div class="btn-group d-none d-lg-block">
        %%DESKTOP_STRIP%%
        </div>
        <script defer="" type="text/javascript">
          $(document).ready(function() {
            $('.section_optns>a').on('click', function(e) {
              e.preventDefault();
              var target = $(this).attr("href");
              scrollToSection(target);
            });
          });
            function scrollToSection(sectionId) {
            // Remove the leading '#' to get the actual id
            var targetId = sectionId.substring(1);
            var section = document.getElementById(targetId);
            
            if (section) {
              // You can adjust the offset value as needed.
              var sectionTop = $(section).offset().top - 200;
              $('html, body').stop().animate({
                scrollTop: sectionTop
              }, 600, function() {
                // Update the URL with the new hash
                history.pushState(null, null, sectionId);
              });
            }
          }

        </script>

        <?php include "../../../include/book-an-appointment.php"; ?>
      </div> <!-- .col-xl-3 -->
      </div>
    </div> <!-- .row -->
  </div> <!-- .container -->
</section>

<?php include "../../../include/contactstrip-new.php"; ?>

<section>
    <div class="container" id="faqs">
      <h2 class="mb-4 sec-scrl" id="faqs">Frequently Asked Questions</h2>
      %%Faq_html%%
    </div>
  </section>

<?php include "../../../include/footer1.php" ?>