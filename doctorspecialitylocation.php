<!DOCTYPE html>

<html lang="en">
<head>
<script src="https://www.googletagmanager.com/gtag/js?id=G-79Z2DRYPBW"></script>
<script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){dataLayer.push(arguments);}
    gtag('js', new Date());
    gtag('config', 'G-79Z2DRYPBW');
  </script>
<meta charset="utf-8"/>
<title>%%TITLE%%</title>
<meta content="%%META_DESCRIPTION%%" name="description">
<meta content="index, follow" name="robots"/>
<meta content="%%OG_TITLE%%" property="og:title">
<meta content="%%OG_DESCRIPTION%%" property="og:description"/>
<meta content="%%OG_URL%%" property="og:url"/>
<meta content="https://www.medicoverhospitals.in/images/logo.png" property="og:image"/>
<meta content="132" property="og:image:width"/>
<meta content="80" property="og:image:height"/>
<link href="%%CANONICAL_URL%%" rel="canonical"/>
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
    $('.mn_nav>li>button').click(function() {
      if ($(window).width() <= 575){
        $('html, body').animate({
            scrollTop: $($(this).attr('data-target')).offset().top - 150
        }, 500);
      } else if ($(window).width() <= 767){
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
<section class="doc-list-card">
<div class="container">
<div class="row g-3 g-xl-4">
<div class="col-xl-9 col-lg-8">
<div class="row">
<div class="col-md-8 col-lg-8 col-xl-8 col-sm-12">
<h1>%%H1%%</h1>
</div>
<div class="col-md-4 col-sm-12">
<div class="form-group card-label">
<?php $speciality= "%%speciality_look_up%%";  include("../../include/locationdropdown.php"); ?>
</div>
</div>
</div>
<?php
                                    $location="%%Location_look_up%%";
                                    $speciality="%%speciality_look_up%%";
                                    include("../../include/doctors-newdisplay.php");?>
  %%Main_content%%
</div>


<div class="col-xl-3 col-lg-4" id="book-an-appointment">
<div class="d-none d-lg-block mb-4">
<div class="section_optns d-block position-relative">
%%DESKTOP_STRIP%%
</div>
</div>

<script defer="" type="text/javascript">
            $(document).ready(function() {
              $('.section_optns a').on('click', function(e) {
                e.preventDefault();
                var target = $(this).attr("href");
                if (target) {
                  var targetElement = $(target);
                  if (targetElement.length) {
                    var offset = $(window).width() >= 1200 ? 100 : 150;
                    $('html, body').animate({
                      scrollTop: targetElement.offset().top - offset
                    }, 800);
                    
                    // Update active state
                    $('.section_optns a').removeClass('active');
                    $(this).addClass('active');
                    
                    // Update URL without page jump
                    if (history.pushState) {
                      history.pushState(null, null, target);
                    }
                  }
                }
              });
              
              // Set active state on scroll
              $(window).on('scroll', function() {
                var scrollPosition = $(window).scrollTop();
                $('.section_optns a').each(function() {
                  var target = $(this).attr('href');
                  if (target) {
                    var targetElement = $(target);
                    if (targetElement.length) {
                      var offset = $(window).width() >= 1200 ? 100 : 150;
                      if (targetElement.offset().top - offset <= scrollPosition && 
                          targetElement.offset().top + targetElement.height() > scrollPosition) {
                        $('.section_optns a').removeClass('active');
                        $(this).addClass('active');
                      }
                    }
                  }
                });
              });
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
<div class="faq_item" id="faq-1">
%%Faq_html%%
</div>
</div>
</div>
</section> <?php include "../../include/footer1.php" ;?></meta></meta></head></html>