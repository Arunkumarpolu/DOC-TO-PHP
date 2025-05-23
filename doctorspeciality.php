<!DOCTYPE html>
<html lang="en">

<head>
  <script src="https://www.googletagmanager.com/gtag/js?id=G-79Z2DRYPBW"></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    
    function gtag() {
      dataLayer.push(arguments);
    }
    gtag("js", new Date());
    gtag("config", "G-79Z2DRYPBW");
  </script>
  <meta charset="UTF-8">
  <title>%%TITLE%%</title>
  <meta name="description" content="%%META_DESCRIPTION%%" />
  <meta name="robots" content="index, follow">
  <meta property="og:title" content="%%TITLE%%" />
  <meta property="og:description" content="%%OG_DESCRIPTION%%" />
  <meta property="og:type" content="website" />
  <meta property="og:url" content="%%OG_URL%%" />
  <meta property="og:image" content="https://www.medicoverhospitals.in/images/logo.png">
  <meta property="og:image:width" content="132">
  <meta property="og:image:height" content="80">
  <link rel="canonical" href="%%CANONICAL_URL%%" />
  %%BREADCRUMB_SCHEMA%%
 
    %%FAQ_SCHEMA%%

  <?php include "../../include/header-specialist.php"; ?>


  %%breadcrumbbar%%
  

  <section class="goto-sec goto-mob d-lg-none">
    <div class="container">
      <ul class="mn_nav">
  %%MOBILE_STRIP%%

  </ul>
    </div>
  </section>


  <script type="text/javascript">
    $(".mn_nav>li>button").click(function() {
      if ($(window).width() <= 575) {
        $("html, body").animate({
          scrollTop: $($(this).attr("data-target")).offset().top - 150
        }, 500);
      } else if ($(window).width() <= 767) {
        $("html, body").animate({
          scrollTop: $($(this).attr("data-target")).offset().top - 135
        }, 500);
      } else {
        $("html, body").animate({
          scrollTop: $($(this).attr("data-target")).offset().top - 120
        }, 500);
      }
      $(this).parent().siblings().children().removeClass("current");
      $(this).addClass("current");
      return false;
    });
  </script>
  <section class="card-custom-box">
    <div class="container">
      <div class="row g-3 g-xl-4">
        <div class="col-xl-9 col-lg-8">
          <div class="row">
            <div class="col-md-8 col-lg-8 col-xl-8 col-sm-12">
              <h1>%%H1%%</h1>
            </div>
            <div class="col-md-4 col-sm-12">
              <div class="form-group card-label">
                <?php $speciality = "%%speciality_look_up%%";  include("../../include/locationdropdown.php"); ?>
              </div>
            </div>
          </div>
          <?php	include("../../include/doctors-display-newindex.php"); ?>
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
              function scrollToSection(hash) {
                if (!hash) return;
                var target = $(hash);
                if (target.length) {
                  var offset = target.offset().top - 100;
                  if ($(window).width() <= 991) {
                    offset = target.offset().top - 150;
                  }
                  $('html, body').animate({
                    scrollTop: offset
                  }, 800);
                }
              }

              // Handle section option clicks
              $(".section_optns a").on("click", function(e) {
                e.preventDefault();
                var hash = $(this).attr("href");
                scrollToSection(hash);
                
                // Update active state
                $(".section_optns a").removeClass("active");
                $(this).addClass("active");
              });

              // Handle initial hash in URL
              if (window.location.hash) {
                scrollToSection(window.location.hash);
                $(".section_optns a[href='" + window.location.hash + "']").addClass("active");
              }
            });
          </script>

          <?php include "../../include/book-an-appointment.php"; ?>

        </div>
      </div>
    </div>
  </section> <?php include "../../include/contactstrip-new.php" ;?>
  <section>
    <div class="container">
      <div class="col-md-12 col-sm-12">
        <h2 class="htitle" id="faqs">Frequently Asked Questions</h2>
        <div>
        %%Faq_html%%
        </div>
      </div>
  </section> <?php include "../../include/footer1.php" ;?>