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
<meta name="keywords" content=" ">
<meta property="og:locale" content="en_US"/>
<meta property="og:type" content="website">
<meta property="og:title" content="%%OG_TITLE%%">
<meta property="og:description" content="%%OG_DESCRIPTION%%">
<meta property="og:url" content="%%OG_URL%%">
<meta property="og:site_name" content="Best Hospitals in India | Medicover Hospitals">
<meta property="og:image" content="https://www.medicoverhospitals.in/images/resources/medicover-hospitals-logo.webp">
<meta property="og:image:width" content="132"/>
<meta property="og:image:height" content="80"/>
<link rel="canonical" href="%%CANONICAL_URL%%"/>
<meta name="ahrefs-site-verification" content="2aa5c2b30ea29d31895e7ca3aa8bc07b9c46ed3db95ab0a9ecf176798b8b4854">
%%FAQ_SCHEMA%%

%%BREADCRUMB_SCHEMA%%

<?php include "../include/header-symptoms-mob.php" ?>

%%breadcrumbbar%%

<section class="goto-sec d-lg-none">
<div class="container position-relative">
<ul class="mn_nav">
%%MOBILE_STRIP%%
</ul>
</div>
</section>

<section class="card-custom-box">
<div class="container">
<div class="row g-3 g-xl-4">
<div class="col-xl-9 col-lg-8">
<div class="card">
<div class="card-body">
<div class="blog-content">
%%Main_content%%
</div>
</div>
</div>
</div>
<div class="col-xl-3 col-lg-4" id="book-an-appointment">

%%DESKTOP_STRIP%%

</div>



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
<?php include "../include/book-an-appointment.php" ?>
</div>
</div>
</div>
</section>

<?php include "../include/contactstrip-new.php" ?>

<section>
<div id="faqs" class="container">
<h2 class="mb-3">Frequently Asked Questions</h2>
%%Faq_html%%
<hr>
<?php include("../include/disclaimer.php");?>
</div>
</section>

<?php include("../include/footer1.php");?>