/* Small things: the menu, the year, sections arriving, and a caption that
   turns around the part as you scroll past it. */

(function () {
  var nav = document.querySelector('.nav');
  var toggle = document.querySelector('.nav__toggle');
  if (nav && toggle) {
    toggle.addEventListener('click', function () {
      var open = nav.getAttribute('data-open') === 'true';
      nav.setAttribute('data-open', String(!open));
      toggle.setAttribute('aria-expanded', String(!open));
    });
  }

  document.querySelectorAll('[data-year]').forEach(function (n) {
    n.textContent = new Date().getFullYear();
  });

  var here = location.pathname.split('/').pop() || 'index.html';
  document.querySelectorAll('.nav__links a').forEach(function (a) {
    if (a.getAttribute('href') === here) a.setAttribute('aria-current', 'page');
  });

  var reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  var risers = document.querySelectorAll('.rise');
  if (!('IntersectionObserver' in window) || reduce) {
    risers.forEach(function (n) { n.classList.add('in'); });
  } else {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); }
      });
    }, { rootMargin: '0px 0px -12% 0px', threshold: 0.06 });
    risers.forEach(function (n) { io.observe(n); });
  }

  var orbit = document.querySelector('[data-orbit]');
  if (orbit && !reduce) {
    var spin = 0, ticking = false;
    var move = function () {
      var box = orbit.getBoundingClientRect();
      var p = 1 - (box.top + box.height / 2) / innerHeight;
      spin = p * 300;
      orbit.style.transform = 'rotate(' + spin.toFixed(2) + 'deg)';
      ticking = false;
    };
    addEventListener('scroll', function () {
      if (!ticking) { ticking = true; requestAnimationFrame(move); }
    }, { passive: true });
    move();
  }
})();
