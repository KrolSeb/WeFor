window.addEventListener('load', function() {
    document.querySelector('.navbar-scroll-into-top').addEventListener('click', function(e) {
      e.preventDefault();
      document.querySelector('.top').scrollIntoView({ behavior: 'smooth' });
    });

    document.querySelector('.navbar-scroll-into-main-content').addEventListener('click', function(e) {
      e.preventDefault();
      document.querySelector('.main-content').scrollIntoView({ behavior: 'smooth' });
    });

    document.querySelector('.button-scroll-into-main-content').addEventListener('click', function(e) {
      e.preventDefault();
      document.querySelector('.main-content').scrollIntoView({ behavior: 'smooth' });
    });
});