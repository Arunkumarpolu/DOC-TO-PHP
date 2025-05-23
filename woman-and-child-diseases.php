<!DOCTYPE html>
<html lang="en">
<head>
<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-79Z2DRYPBW"></script>
<script>
window.dataLayer = window.dataLayer || [];
function gtag(){dataLayer.push(arguments);}
gtag('js', new Date());
gtag('config', 'G-79Z2DRYPBW');
</script>
<meta charset="UTF-8">
<title>%%TITLE%%</title>
<meta name="description" content="%%META_DESCRIPTION%%">
<meta property="og:title" content="%%OG_TITLE%%" />
<meta property="og:description" content="%%OG_DESCRIPTION%%"/>
<meta property="og:image" content="https://www.medicoverhospitals.in/woman-and-child/images/logo.png" />
<meta property="og:image:width" content="319"/>
<meta property="og:image:height" content="77"/>
<link rel="canonical" href="%%CANONICAL_URL%%">
%%BREADCRUMB_SCHEMA%%

%%FAQ_SCHEMA%%



<?php include "../includes/header-new.php" ?>

%%breadcrumbbar%%

<section class="goto-sec goto-mob d-lg-none bg-white">
<div class="container position-relative">
<ul class="mn_nav">
%%MOBILE_STRIP%%
</ul>
</div>
</section>

<script type="text/javascript">
$('.mn_nav>li>a').click(function(){
  if ($(window).width() <= 401){
	$('html, body').animate({
      scrollTop: $( $(this).attr('href') ).offset().top - 190
  }, 500);
} else if ($(window).width() <= 575){
	$('html, body').animate({
      scrollTop: $( $(this).attr('href') ).offset().top - 160
  }, 500);
} else if ($(window).width() <= 767){
	$('html, body').animate({
      scrollTop: $( $(this).attr('href') ).offset().top - 135
  }, 500);
} else {
  $('html, body').animate({
      scrollTop: $( $(this).attr('href') ).offset().top - 120
  }, 500);
}
  $(this).parent().siblings().children().removeClass('current');
  $(this).addClass('current');
  return false;
});
</script>

<section>
<div class="container">
<div class="row g-3 gx-4 mt-0">
<div class="col-xl-9 col-lg-8 article-infos doc-full-info mt-0">
<div class="card">
<div class="card-body">
<figure class="mb-3"><img src="../images/diseases/wc-%%slug%%-bnr.webp" alt="%%ALT_txt%%" title="%%ALT_txt%%" width="1440" /></figure>
%%Main_content%%

</div>
</div>
</div>
<div class="col-xl-3 col-lg-4 mt-4 mt-lg-0 left_form" id="appointment">
%%DESKTOP_STRIP%%
<script type="text/javascript" defer>
$('.mn_nav>li>button').click(function(){
if ($(window).width() <= 575){
$('html, body').animate({
scrollTop: $( $(this).attr('data-target') ).offset().top - 160
}, 500);
} else if ($(window).width() <= 767){
$('html, body').animate({
scrollTop: $( $(this).attr('data-target') ).offset().top - 135
}, 500);
} else {
$('html, body').animate({
scrollTop: $( $(this).attr('data-target') ).offset().top - 120
}, 500);
}
$(this).parent().siblings().children().removeClass('current');
$(this).addClass('current');
return false;
});
//Desktop
$('.section_optns>a').click(function(){
$('body,html').animate({
scrollTop: $($(this).attr('href')).offset().top - 170
}, 500);
});
</script>
<?php include '../includes/book-appointment-new.php' ?>
</div>
</div>
</div>
</section>

<?php include("../includes/appointment-phone-cta.php");?>

<section>
<div class="container" id="faqs">
<h2 class="mb-3">Frequently Asked Questions</h2>
%%Faq_html%%
</div>
</section>


<?php include "../../include/footer1.php" ?>