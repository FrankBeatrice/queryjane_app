// Add your javascript here
// Don't forget to add it into respective layouts where this js file is needed
$(document).ready(function() {
  AOS.init( {
    // uncomment below for on-scroll animations to played only once
    // once: true  
  }); // initialize animate on scroll library
});


// Light Box
$(document).on("click", '[data-toggle="lightbox"]', function(event) {
  event.preventDefault();
  $(this).ekkoLightbox();
});

// Scroll Top
$(function () {
  $('[data-toggle="tooltip"]').tooltip()

  $("#scrolltop").click(function () {
    $("html,body").animate({ scrollTop: $("#top").offset().top }, "1000");
    return false
  })
})

$(window).scroll(function () {
  if ($(this).scrollTop() > 500) {
    $('#scrolltop:hidden').stop(true, true).fadeIn();
  } else {
    $('#scrolltop').stop(true, true).fadeOut();
  }
});

