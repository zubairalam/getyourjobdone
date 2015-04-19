// Generated by CoffeeScript 1.7.1
(function() {
  $(document).ready(function() {
    $('[data-toggle=tooltip]').tooltip();
    $(window).scroll(function() {
      if ($(this).scrollTop() > 50) {
        $("#back-to-top").fadeIn();
      } else {
        $("#back-to-top").fadeOut();
      }
    });
    $("#back-to-top").click(function() {
      $("#back-to-top").tooltip("hide");
      $("body,html").animate({
        scrollTop: 0
      }, 800);
      return false;
    });
    $("#back-to-top").tooltip("show");
  });

}).call(this);
$(document).ready(function () {
    /* ======= jQuery Placeholder ======= */
    $('input, textarea').placeholder();

    /* ======= jQuery FitVids - Responsive Video ======= */
    $(".video-container").fitVids();

    /* ======= FAQ accordion ======= */
    function toggleIcon(e) {
        $(e.target)
            .prev('.panel-heading')
            .find('.panel-title a')
            .toggleClass('active')
            .find("i.fa")
            .toggleClass('fa-plus-square fa-minus-square');
    }

    $('.panel').on('hidden.bs.collapse', toggleIcon);
    $('.panel').on('shown.bs.collapse', toggleIcon);

    /* ======= Fixed header when scrolled ======= */

    $(window).bind('scroll', function () {
        if ($(window).scrollTop() > 50) {
            $('#header').addClass('navbar-fixed-top');
        }
        else {
            $('#header').removeClass('navbar-fixed-top');
        }
    });
});