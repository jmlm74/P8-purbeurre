(function($) {
  "use strict"; // Start of use strict
  console.log("corejs loaded !")
  // Smooth scrolling using jQuery easing
  $('a.js-scroll-trigger[href*="#"]:not([href="#"])').click(function() {
    if (location.pathname.replace(/^\//, '') == this.pathname.replace(/^\//, '') && location.hostname == this.hostname) {
      var target = $(this.hash);
      target = target.length ? target : $('[name=' + this.hash.slice(1) + ']');
      if (target.length) {
        $('html, body').animate({
          scrollTop: (target.offset().top - 72)
        }, 1000, "easeInOutExpo");
        return false;
      }
    }
  });

  // Closes responsive menu when a scroll trigger link is clicked
  $('.js-scroll-trigger').click(function() {
    $('.navbar-collapse').collapse('hide');
  });

  // Activate scrollspy to add active class to navbar items on scroll
  $('body').scrollspy({
    target: '#mainNav',
    offset: 75
  });

  // Collapse Navbar
  var navbarCollapse = function() {
    if ($("#mainNav").offset().top > 100) {
      $("#mainNav").addClass("navbar-scrolled");
    } else {
      $("#mainNav").removeClass("navbar-scrolled");
    }
  };
  // Collapse now if page is not at top
  navbarCollapse();
  // Collapse the navbar when page is scrolled
  $(window).scroll(navbarCollapse);

  // Magnific popup calls
  $('#portfolio').magnificPopup({
    delegate: 'a',
    type: 'image',
    tLoading: 'Loading image #%curr%...',
    mainClass: 'mfp-img-mobile',
    gallery: {
      enabled: true,
      navigateByImgClick: true,
      preload: [0, 1]
    },
    image: {
      tError: '<a href="%url%">The image #%curr%</a> could not be loaded.'
    }
  });

  // change background at every load
  var images = ['/static/dist/assets/img/photo1.jpg','/static/dist/assets/img/photo2.jpg','/static/dist/assets/img/photo3.jpg'];
  var image = images[Math.floor(Math.random() * images.length)];
  var origin = window.location.origin;
  var newimage = origin + image
  $('.masthead').css({'background-image': 'url(' + newimage + ')'});
  var n = image.search("photo2");
  if (n != -1){
    $('.masthead h4').css('color','yellow');
    $('.masthead li').css('color','yellow');
  }
  $('.masthead').css('height','120vh');

  // search --> more than 4 chars
  $('#searchform_nav').submit(function(e){
    if ($("#search_menu").val().length < 5){
      return false;
    }
  });

})(jQuery); // End of use strict
