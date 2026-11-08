/* Small things: the menu, the year, sections arriving, and a caption that
   turns around the part as you scroll past it. */

(function () {
  var nav = document.querySelector('.nav');
  var toggle = document.querySelector('.nav__toggle');
  if (nav && toggle) {
    var close = function () {
      nav.setAttribute('data-open', 'false');
      toggle.setAttribute('aria-expanded', 'false');
      document.body.style.overflow = '';
    };
    toggle.addEventListener('click', function () {
      var open = nav.getAttribute('data-open') === 'true';
      nav.setAttribute('data-open', String(!open));
      toggle.setAttribute('aria-expanded', String(!open));
      document.body.style.overflow = open ? '' : 'hidden';
    });
    nav.querySelectorAll('.nav__links a').forEach(function (a) {
      a.addEventListener('click', close);
    });
    addEventListener('keydown', function (e) {
      if (e.key === 'Escape') close();
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

  /* The seal around the part turns as the page moves, so the words walk
     around the drawing instead of spinning on their own. */
  var seal = document.querySelector('.hero__ring svg');
  if (seal && !reduce) {
    var ticking = false;
    var turn = function () {
      seal.style.transform = 'rotate(' + (scrollY * 0.16).toFixed(2) + 'deg)';
      ticking = false;
    };
    addEventListener('scroll', function () {
      if (!ticking) { ticking = true; requestAnimationFrame(turn); }
    }, { passive: true });
    turn();
  }
})();
