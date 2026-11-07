/* The app demo. It runs the same four screens the phone app runs: listen,
   estimate the chest wall, correct, then accept or refuse. Everything here is
   generated in the page; the numbers are the ones the estimator returns on the
   synthetic grade 2 murmur the demo plays. */

(function () {
  var root = document.querySelector('[data-demo]');
  if (!root) return;

  var canvas = root.querySelector('[data-demo-wave]');
  var stateEl = root.querySelector('[data-demo-state]');
  var bigEl = root.querySelector('[data-demo-big]');
  var kvEl = root.querySelector('[data-demo-q]');
  var verdictEl = root.querySelector('[data-demo-verdict]');
  var dotEl = root.querySelector('[data-demo-dot]');
  var steps = [].slice.call(root.querySelectorAll('[data-demo-step]'));
  var runBtn = root.querySelector('[data-demo-run]');
  var g = canvas.getContext('2d');
  var reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;

  var phase = -1, t0 = 0, raf = 0, stopped = false;

  function size() {
    var r = canvas.getBoundingClientRect();
    var dpr = Math.min(devicePixelRatio || 1, 2);
    canvas.width = Math.max(1, Math.round(r.width * dpr));
    canvas.height = Math.max(1, Math.round(r.height * dpr));
    g.setTransform(dpr, 0, 0, dpr, 0, 0);
    return r;
  }

  /* A two-component trace: the murmur (low, rough) under the heart sounds
     (sharp, sparse). It is drawn, not sampled, so it runs without audio. */
  function wave(now, amp) {
    var r = size();
    var w = r.width, h = r.height, mid = h / 2;
    g.clearRect(0, 0, w, h);
    g.lineWidth = 2;
    g.strokeStyle = '#e5341c';
    g.beginPath();
    for (var x = 0; x <= w; x += 1) {
      var p = x / w;
      var beat = Math.pow(Math.max(0, Math.sin(p * Math.PI * 7 + now / 420)), 6);
      var rough = Math.sin(p * 90 + now / 90) * 0.35 + Math.sin(p * 210 + now / 60) * 0.15;
      var y = mid - (beat * 26 + rough * 13) * amp;
      if (x === 0) g.moveTo(x, y); else g.lineTo(x, y);
    }
    g.stroke();
    g.strokeStyle = 'rgba(20,16,24,.14)';
    g.lineWidth = 1;
    g.beginPath(); g.moveTo(0, mid); g.lineTo(w, mid); g.stroke();
  }

  function setPhase(n) {
    phase = n;
    t0 = performance.now();
    steps.forEach(function (s, i) { s.classList.toggle('on', i <= n); });
    dotEl.classList.toggle('demo__dot--live', n > 0 && n < 4);
    if (n === 0) {
      stateEl.textContent = 'Ready';
      bigEl.className = 'demo__big demo__big--idle';
      bigEl.textContent = 'Waiting for contact';
      kvEl.textContent = '89%';
      verdictEl.className = 'demo__verdict';
      verdictEl.textContent = 'Press run to play a generated grade 2 murmur.';
    }
    if (n === 1) {
      bigEl.className = 'demo__big';
      stateEl.textContent = 'Listening';
      bigEl.innerHTML = '6.0<small> s</small>';
      verdictEl.textContent = 'Hold the chestpiece still. Nothing leaves the phone.';
    }
    if (n === 2) {
      stateEl.textContent = 'Measuring the wall';
      verdictEl.textContent = 'The wall is estimated from this recording alone.';
    }
    if (n === 3) {
      bigEl.className = 'demo__big';
      stateEl.textContent = 'Correcting';
      bigEl.innerHTML = '1.73<small> dB</small>';
      verdictEl.textContent = 'Two people, same murmur, 1.73 dB apart before correction.';
    }
    if (n === 4) {
      stateEl.textContent = 'Reading accepted';
      bigEl.innerHTML = '0.25<small> dB</small>';
      verdictEl.className = 'demo__verdict';
      verdictEl.textContent = 'Accepted at 89% quality. Saved as WAV and JSON on the phone.';
    }
  }

  function loop(now) {
    if (stopped) return;
    var dt = now - t0;
    if (phase === 0 && dt > 900) setPhase(1);
    else if (phase === 1 && dt > 2600) setPhase(2);
    else if (phase === 2) {
      var k = Math.min(1, dt / 1500);
      bigEl.innerHTML = (Math.round(k * 37)) + '<small> mm</small>';
      if (k >= 1) setPhase(3);
    } else if (phase === 3 && dt > 2000) setPhase(4);
    else if (phase === 4 && dt > 3400) setPhase(0);

    var amp = phase === 0 ? 0.06 : phase === 1 ? 1 : 0.5;
    if (canvas.offsetParent) wave(now, amp * (0.75 + 0.25 * Math.sin(now / 700)));
    raf = requestAnimationFrame(loop);
  }

  function start() {
    stopped = false;
    cancelAnimationFrame(raf);
    setPhase(0);
    raf = requestAnimationFrame(loop);
  }

  runBtn.addEventListener('click', start);

  var io = new IntersectionObserver(function (e) {
    if (e[0].isIntersecting && phase < 0) { start(); io.disconnect(); }
  }, { threshold: 0.25 });
  io.observe(root);

  if (reduce) {
    stopped = true;
    setPhase(4);
    wave(0, 0.5);
  }
})();
