/* Heartware — live phonocardiogram demo.
   Everything drawn here is synthesised from a fixed model in this file.
   No patient recording is used or implied. */

(function () {
  const cv = document.getElementById('pc-canvas');
  if (!cv) return;
  const ctx = cv.getContext('2d');
  const $ = (id) => document.getElementById(id);

  const SR = 480;              // samples per second in the model
  const WINDOW = 3;            // seconds on screen
  const N = SR * WINDOW;
  const raw = new Float32Array(N);
  const cor = new Float32Array(N);
  const T = 60 / 72;           // 72 bpm

  let head = 0;
  let t = 0;
  let playing = false;
  let mode = 'both';           // raw | cor | both
  let wall = 28;
  let W = 1100, H = 260;

  const reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  function attenuation(mm) {
    // one absorption coefficient, one path: 1.0 at 12 mm, ~0.10 at 48 mm
    return Math.exp(-0.064 * (mm - 12));
  }

  function sample(at) {
    const ph = at % T;
    const s1 = Math.exp(-(ph * ph) / (2 * 0.010 * 0.010)) * Math.sin(2 * Math.PI * 45 * at);
    const d2 = ph - 0.34;
    const s2 = 0.72 * Math.exp(-(d2 * d2) / (2 * 0.008 * 0.008)) * Math.sin(2 * Math.PI * 70 * d2);
    const dm = ph - 0.17;
    const env = Math.exp(-(dm * dm) / (2 * 0.075 * 0.075));
    const murmur = 0.9 * env * (0.62 + 0.38 * Math.sin(2 * Math.PI * 2.7 * at)) *
      (Math.sin(2 * Math.PI * 258 * at) + 0.45 * Math.sin(2 * Math.PI * 322 * at)) * 0.72;
    const room = (Math.random() - 0.5) * 0.10 + 0.03 * Math.sin(2 * Math.PI * 60 * at);
    const a = attenuation(wall);
    const y = s1 + s2 + murmur * a + room;
    // the correction divides out the estimated path, and carries the amplified floor with it
    const yc = s1 + s2 + murmur * 1.0 + room * (1 + (1 - a) * 1.6);
    return [y, yc];
  }

  function push(dt) {
    const n = Math.max(1, Math.round(dt * SR));
    for (let i = 0; i < n; i++) {
      t += 1 / SR;
      const [a, b] = sample(t);
      raw[head] = a;
      cor[head] = b;
      head = (head + 1) % N;
    }
  }

  // rate comes from a 40 ms envelope, so the murmur's own oscillation cannot
  // be mistaken for a valve closure
  const smooth = new Float32Array(N);
  const HALF = Math.round(SR * 0.02);
  function envelope() {
    for (let i = 0; i < N; i++) {
      let s = 0;
      for (let k = -HALF; k <= HALF; k++) s += Math.abs(raw[(head + i + k + N) % N]);
      smooth[i] = s / (2 * HALF + 1);
    }
  }

  function detectRate() {
    envelope();
    // autocorrelation of the envelope over plausible beat intervals
    let best = 0, bestLag = 0;
    const lo = Math.round(SR * 0.4), hi = Math.round(SR * 1.6);
    for (let lag = lo; lag < hi; lag++) {
      let s = 0;
      for (let i = 0; i + lag < N; i++) s += smooth[i] * smooth[i + lag];
      if (s > best) { best = s; bestLag = lag; }
    }
    if (!bestLag) return null;
    const bpm = Math.round(60 / (bestLag / SR));
    return bpm > 35 && bpm < 200 ? bpm : null;
  }

  function quality(snrDb) {
    return Math.max(0.18, Math.min(0.97, (snrDb - 2) / 26));
  }

  function snr() {
    const a = attenuation(wall);
    return 20 * Math.log10((0.9 * a) / 0.05);
  }

  function fit() {
    const r = cv.getBoundingClientRect();
    if (!r.width) return;
    const dpr = Math.min(window.devicePixelRatio || 1, 2);
    W = r.width;
    H = r.height;
    cv.width = Math.round(W * dpr);
    cv.height = Math.round(H * dpr);
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
  }

  function trace(arr, color, width, amp) {
    ctx.beginPath();
    for (let x = 0; x <= W; x += 2) {
      const i = Math.floor((x / W) * (N - 1));
      const v = arr[(head + i) % N];
      const y = H * 0.52 - v * amp;
      if (x === 0) ctx.moveTo(x, y); else ctx.lineTo(x, y);
    }
    ctx.strokeStyle = color;
    ctx.lineWidth = width;
    ctx.lineJoin = 'round';
    ctx.stroke();
  }

  function draw() {
    ctx.clearRect(0, 0, W, H);

    // grid
    ctx.strokeStyle = 'rgba(255,255,255,.06)';
    ctx.lineWidth = 1;
    for (let i = 1; i < 6; i++) {
      const x = (W / 6) * i;
      ctx.beginPath(); ctx.moveTo(x, 0); ctx.lineTo(x, H); ctx.stroke();
    }
    ctx.strokeStyle = 'rgba(255,255,255,.09)';
    ctx.beginPath(); ctx.moveTo(0, H * 0.52); ctx.lineTo(W, H * 0.52); ctx.stroke();

    const amp = H * 0.30;

    if (mode !== 'cor') {
      ctx.shadowBlur = 0;
      trace(raw, 'rgba(255,255,255,.26)', 1.1, amp * 1.55);
    }
    if (mode !== 'raw') {
      ctx.shadowColor = 'rgba(255,61,99,.55)';
      ctx.shadowBlur = 14;
      trace(cor, '#FF4A6B', 1.9, amp * 1.25);
      ctx.shadowBlur = 0;
    }

    // playhead
    const g = ctx.createLinearGradient(W - 60, 0, W, 0);
    g.addColorStop(0, 'rgba(255,61,99,0)');
    g.addColorStop(1, 'rgba(255,61,99,.14)');
    ctx.fillStyle = g;
    ctx.fillRect(W - 60, 0, 60, H);
  }

  function readouts() {
    const qRaw = quality(snr());
    const qCor = quality(20 * Math.log10(0.9 / 0.05));
    $('pc-wall-out').textContent = wall + ' mm';
    $('pc-loss').textContent = '−' + Math.abs(20 * Math.log10(attenuation(wall))).toFixed(0) + ' dB';
    $('pc-band').textContent = wall > 40 ? '150–400 Hz · buried' : '150–400 Hz · clear';

    const rate = detectRate();
    if (rate) $('pc-hr').textContent = rate;

    const q = mode === 'raw' ? qRaw : qCor;
    $('pc-q').textContent = q.toFixed(2);
    $('pc-q').classList.toggle('is-bad', q < 0.5);
  }

  let last = 0;
  function frame(now) {
    const dt = Math.min(0.05, (now - last) / 1000 || 0.016);
    last = now;
    if (playing) push(dt);
    draw();
    if (playing) readouts();
    if (playing) requestAnimationFrame(frame);
  }

  function start() {
    playing = true;
    last = performance.now();
    $('pc-play').setAttribute('aria-pressed', 'true');
    $('pc-play').querySelector('span').textContent = 'Pause';
    requestAnimationFrame(frame);
  }

  function stop() {
    playing = false;
    $('pc-play').setAttribute('aria-pressed', 'false');
    $('pc-play').querySelector('span').textContent = 'Play';
  }

  $('pc-play').addEventListener('click', () => (playing ? stop() : start()));

  document.querySelectorAll('.seg button').forEach((b) => {
    b.addEventListener('click', () => {
      mode = b.dataset.mode;
      document.querySelectorAll('.seg button').forEach((o) =>
        o.setAttribute('aria-pressed', String(o === b)));
      draw();
      readouts();
    });
  });

  $('pc-wall').addEventListener('input', (e) => {
    wall = Number(e.target.value);
    if (!playing) { draw(); readouts(); }
    else readouts();
  });

  fit();
  push(3);
  draw();
  readouts();
  window.addEventListener('resize', () => { fit(); draw(); });

  // Only run when on screen; the section is far down the page.
  if ('IntersectionObserver' in window && !reduced) {
    new IntersectionObserver((entries) => {
      entries.forEach((e) => { if (!e.isIntersecting && playing) stop(); });
    }, { threshold: 0 }).observe(cv);
  }
  if (reduced) { $('pc-play').disabled = true; }
})();
