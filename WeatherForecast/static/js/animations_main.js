window.addEventListener('load', function() {

    /*scroll to top - dodać na końcu
    document.querySelector('.js-scroll-to-top').addEventListener('click', function(e) {
      e.preventDefault();
      document.querySelector('header').scrollIntoView({ behavior: 'smooth' });
    });
    */

    document.querySelector('.navbar-scroll-into-top').addEventListener('click', function(e) {
      e.preventDefault();
      document.querySelector('.top').scrollIntoView({ behavior: 'smooth' });
    });

    document.querySelector('.navbar-scroll-into-presentation').addEventListener('click', function(e) {
      e.preventDefault();
      document.querySelector('.presentation').scrollIntoView({ behavior: 'smooth' });
    });

    document.querySelector('.button-scroll-into-presentation').addEventListener('click', function(e) {
      e.preventDefault();
      document.querySelector('.presentation').scrollIntoView({ behavior: 'smooth' });
    });

    document.querySelector('.button-scroll-into-video').addEventListener('click', function(e) {
      e.preventDefault();
      document.querySelector('.video').scrollIntoView({ behavior: 'smooth' });
    });
});