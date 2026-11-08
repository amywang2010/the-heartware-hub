/* The phone demo. It runs itself: listen, measure, correct, hold.
   One loop takes about nine seconds and then starts again. */

(function () {
  var roots = document.querySelectorAll('[data-demo]');
  if (!roots.length) return;

  var reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;

  function setup(root) {
    var state = root.querySelector('[data-demo-state]');
    var big = root.querySelector('[data-demo-big]');
    var canvas = root.querySelector('[data-demo-wave]');
    var wall = root.querySelector('[data-demo-wall]');
    var q = root.querySelector('[data-demo-q]');
    var bar = root.querySelector('[data-demo-bar]');
    var verdict = root.querySelector('[data-demo-verdict]');
    var button = root.querySelector('[data-demo-run]');
    var steps = [].slice.call(root.querySelectorAll('[data-demo-step]'));
    if (!big || !canvas) return;

    var ctx = canvas.getContext('2d');
    var t = 0;
    var phase = 0;           /* 0 listen, 1 measure, 2 correct, 3 hold */
    var started = 0;
    var timer = 0;
    var raf = 0;
    var running = false;

    var copy = [
      { state: 'Listening', tone: 'ok', text: 'Recording. Hold the chestpiece still.' },
      { state: 'Measuring', tone: 'ok', text: 'Estimating the chest wall from the take.' },
      { state: 'Correcting', tone: 'ok', text: 'Dividing the murmur band by the wall.' },
      { state: 'Held', tone: 'ok', text: 'Contact is good. Holding the take.' }
    ];

    function setPhase(n) {
      phase = n;
      state.textContent = copy[n].state;
      verdict.setAttribute('data-tone', copy[n].tone);
      verdict.textContent = copy[n].text;
      steps.forEach(function (el, i) { el.classList.toggle('on', i === n); });
      if (n === 0) {
        wall.textContent = '— mm';
        q.textContent = 'measuring';
        bar.style.width = '0%';
        bar.style.background = 'rgba(14,34,51,.25)';
      }
      if (n === 1) {
        wall.textContent = '37 mm';
        q.textContent = '89%';
        bar.style.width = '89%';
        bar.style.background = '#971a2c';
      }
    }

    function setBig(value, unit) {
      big.innerHTML = value + '<small>' + unit + '</small>';
    }

    function draw() {
      var w = canvas.width, h = canvas.height;
      ctx.clearRect(0, 0, w, h);
      var mid = h / 2;
      var amp = phase === 0 ? 20 : phase === 1 ? 15 : 9;
      ctx.lineWidth = 3;
      ctx.lineJoin = 'round';
      ctx.strokeStyle = phase === 3 ? '#971a2c' : '#971a2c';
      ctx.beginPath();
      for (var x = 0; x <= w; x += 3) {
        var p = (x + t * 1.9) / w;
        var beat = Math.pow(Math.max(0, Math.sin(p * Math.PI * 6)), 8);
        var hiss = Math.sin(p * 210 + t * 0.02) * 0.9 + Math.sin(p * 97 - t * 0.01) * 0.7;
        var y = mid + Math.sin(p * 74 + t * 0.03) * 3 + hiss * 4 - beat * amp;
        if (x === 0) ctx.moveTo(x, y); else ctx.lineTo(x, y);
      }
      ctx.stroke();

      /* the murmur band, drawn under the trace while listening */
      if (phase === 0) {
        ctx.globalAlpha = 0.28;
        ctx.fillStyle = '#971a2c';
        ctx.fillRect(0, mid + 10, w, 6);
        ctx.globalAlpha = 1;
      }
    }

    function tick(now) {
      if (!started) started = now;
      var elapsed = now - started;
      t = elapsed / 16;

      if (phase === 0) {
        var s = Math.min(6, elapsed / 560);
        setBig(s.toFixed(1), 's');
      }

      if (phase === 1) setBig('37', 'mm wall');
      if (phase === 2) setBig('1.73', 'dB before');
      if (phase === 3) setBig('0.25', 'dB after');

      draw();
      raf = requestAnimationFrame(tick);
    }

    function schedule() {
      clearTimeout(timer);
      timer = setTimeout(function () {
        if (phase === 3) { start(); return; }
        setPhase(phase + 1);
        schedule();
      }, phase === 0 ? 3600 : 1600);
    }

    function start() {
      cancelAnimationFrame(raf);
      clearTimeout(timer);
      started = 0;
      setPhase(0);
      setBig('0.0', 's');
      running = true;
      raf = requestAnimationFrame(tick);
      schedule();
    }

    function stop() {
      running = false;
      cancelAnimationFrame(raf);
      clearTimeout(timer);
    }

    if (button) button.addEventListener('click', start);

    /* It only runs while it is on screen, and it parks on the result if the
       reader has asked for less motion. */
    if (reduce) {
      setPhase(3);
      setBig('0.25', 'dB after');
      draw();
      return;
    }

    if ('IntersectionObserver' in window) {
      var io = new IntersectionObserver(function (entries) {
        entries.forEach(function (e) {
          if (e.isIntersecting && !running) start();
          else if (!e.isIntersecting && running) stop();
        });
      }, { threshold: 0.25 });
      io.observe(root);
    } else {
      start();
    }
  }

  roots.forEach(setup);
})();
