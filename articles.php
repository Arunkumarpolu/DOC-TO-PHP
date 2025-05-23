<!DOCTYPE html>
<html lang="en">
<head>
    <script src="https://www.googletagmanager.com/gtag/js?id=G-79Z2DRYPBW"></script>
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
    <meta name="description" content="%%META_DESCRIPTION%%" />
    <meta property="og:title" content="%%TITLE%%" />
    <meta property="og:description" content="%%META_DESCRIPTION%%" />
    <meta property="og:type" content="website" />
    <meta property="og:url" content="%%OG_URL%%" />
    <meta property="og:image" content="%%image_url%%" />
    <meta property="og:image:width" content="900" />
    <meta property="og:image:height" content="300" />
    <link rel="canonical" href="%%CANONICAL_URL%%" />
    %%BREADCRUMB_SCHEMA%%
 
    %%FAQ_SCHEMA%%

  <?php include("../include/header-article-mobile.php");?>

    %%breadcrumbbar%%

    <!-- Mobile Navigation -->
    <section class="goto-sec d-lg-none">
      <div class="container position-relative">
        <ul class="mn_nav"> 
          %%MOBILE_STRIP%%
        </ul>
      <div id="mobile_btn" class="d-lg-none"><i class="fa fa-bars"></i>
      </div>
      </div>
    </section>

    <script type="text/javascript">
  $(document).ready(function() {
    // Bind click events for mobile and desktop navigation items
    $('.mn_nav > li > button, .mn_nav > li > a, .section_optns a').on('click', function(e) {
      e.preventDefault();
      // For mobile buttons, use data-target; for desktop links, use href.
      var target = $(this).attr("data-target") || $(this).attr("href");
      scrollToSection(target);
      // Update the "current" class for visual feedback
      $('.mn_nav > li > button.current, .mn_nav > li > a.current, .section_optns a.current').removeClass('current');
      $(this).addClass('current');
    });

    // Update navigation "current" state on scroll
    $(window).scroll(function() {
      var scrollDistance = $(window).scrollTop();
      $('.sec-scrl').each(function() {
        if ($(this).position().top - getOffset() <= scrollDistance + 1) {
          $('.mn_nav > li > button.current, .mn_nav > li > a.current, .section_optns a.current').removeClass('current');
          var sectionId = $(this).attr('id');
          $('.mn_nav > li > button[data-target="#' + sectionId + '"], ' +
            '.mn_nav > li > a[data-target="#' + sectionId + '"], ' +
            '.section_optns a[href="#' + sectionId + '"]').addClass('current');
        }
      });
    }).scroll();
  });

  function getOffset() {
    // Adjust offset based on window width: modify these values as needed
    var isMobile = $(window).width() <= 992;
    return isMobile ? 145 : 200;
  }

  function scrollToSection(sectionId) {
    // Remove the leading '#' (if present) to get the element ID
    var targetId = sectionId.charAt(0) === '#' ? sectionId.substring(1) : sectionId;
    var section = document.getElementById(targetId);
    if (section) {
      var sectionTop = $(section).offset().top - getOffset();
      $('html, body').stop().animate({
        scrollTop: sectionTop
      }, 600, function() {
        // Update the URL hash without abrupt jump
        history.pushState(null, null, '#' + targetId);
      });
    }
  }
</script>

    <style>
      .article-infos figure figcaption {
        position: absolute;
        left: 0;
        top: 0;
        font-size: 24px;
        color: #000;
        font-weight: 600;
        right: 0;
        bottom: 0;
        margin: auto;
        width: 50%;
        height: 80px;
        text-align: center;display:flex;align-items:center;justify-content:center
      }

      .article-infos>figure {
        display:block
      }
      @media screen and (max-width:767px){
        .article-infos figure figcaption{
          font-size:20px;width:80%
        }
      }
      @media screen and (max-width:400px){
        .article-infos figure figcaption{
          font-size:16px;width:100%
        }
      }
    </style>
    <section class="article-details">
      <div class="container">
        <div class="row g-3 gx-4 mt-0">
          <div class="col-xl-9 col-lg-8 mt-0 article-infos doc-full-info">
            <figure class="position-relative">
              <img alt="%%alt_text%%" class="img-fluid rounded-0" src="%%image_url%%" title="%%alt_text%%">
            </figure>
          
            <div class="article_info mt-3 mb-4">
              <div class="top d-flex justify-content-between align-items-center">
                <ul class="d-flex">
                  <li>
                    <i class="fa-regular fa-eye"></i> %%views%%
                  </li>
                  <li>
                    <i class="fa-regular fa-clock"></i> %%time_to_read%%
                  </li>
                </ul>             
              </div>
              <div class="btm d-flex align-items-center mt-3 mt-md-2">
                <span>
                <i class="fa-regular fa-calendar me-1"></i> %%published_date%% </span>
                <span>
                <i class="fa-regular fa-user me-1"></i> Team Medicover </span>
                <span>
                  <i class="fa-solid fa-layer-group me-1"></i><a href="%%category_url%%">%%category_text%%</a></span>
                </div>
            </div>
            %%Main_content%%

            <h2 class="mb-4 sec-scrl" id="faqs">Frequently Asked Questions</h2>
            <div class="accordion cstm-accordion mb-4 pb-2" id="faqaccord">
            %%Faq_html%%
            </div>
          </div>

            <div class="col-xl-3 col-lg-4 article-side mt-0 sec-scrl" id="book-an-appointment">
            <!-- Desktop Navigation -->
            %%DESKTOP_STRIP%%

            <?php include "../include/book-an-appointment.php" ?>
            <div class="appointment-form-side category_sidelist mt-lg-4 d-none d-lg-block">
              <?php include('../include/articles-categories.php'); ?>
            </div>
          </div>
        </div>
      </div>
    </section>
    <?php $category="%%category_text%%"; include("../include/relatedblog.php");?>
    <?php include("../include/footer-articles.php");?>
</body>
</html>
