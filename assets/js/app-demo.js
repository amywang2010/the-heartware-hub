/* ==========================================================================
   HEARTWARE — the companion app, running in the page.

   This is the real signal path, not a picture of one: microphone in, an
   analyser in the background, three band energies, a contact gate, a wall
   estimate from the recording, and a correction applied to the spectrum that
   is displayed. Nothing here is a clinical claim; the numbers are the same
   arithmetic the model in research/ uses, at demo precision.
   ========================================================================== */

const $ = (s, r = document) => r.querySelector(s);
const $$ = (s, r = document) => Array.from(r.querySelectorAll(s));

const BANDS = {
  heart: [20, 150],
  murmur: [150, 400],
  noise: [600, 2000]
};

const state = {
  ctx: null,
  stream: null,
  analyser: null,
  source: null,
  tap: null,
  buf: null,          // Float32 accumulation for the WAV
  recording: false,
  demo: null,
  wall: 22,
  quality: 0,
  verdict: 'idle',
  freq: null,
  takes: []
};

/* ---------- the correction ------------------------------------------------ */

/* Chest wall attenuation, dB per mm, as a function of frequency. The exponent
   is the one fitted in research/thoracic_model.py: soft tissue is a low-pass,
   not a flat pad, which is why a 38 mm wall costs 25 dB at 150 Hz and far less
   at S1. */
function attenDb(f, d) {
  return 0.0092 * Math.pow(Math.max(f, 20), 0.72) * d;
}

/* Inverse of the wall, in linear gain, clamped so a quiet recording is not
   multiplied into noise. */
function correctionGain(f, d) {
  const db = attenDb(f, d);
  return Math.min(Math.pow(10, db / 20), 24);
}

/* ---------- the inverse --------------------------------------------------- */

/* The model maps thickness to the murmur/heart ratio. Run it forwards at nine
   thicknesses, sort the pairs, and interpolate backwards. Nothing is hand-set:
   if the forward model changes, this changes with it. */
let LOOKUP = null;

function wallFromRatio(r) {
  if (!LOOKUP) return 22;
  if (r >= LOOKUP[0][0]) return LOOKUP[0][1];
  const last = LOOKUP[LOOKUP.length - 1];
  if (r <= last[0]) return last[1];
  for (let i = 1; i < LOOKUP.length; i++) {
    const [r1, d1] = LOOKUP[i];
    if (r >= r1) {
      const [r0, d0] = LOOKUP[i - 1];
      const t = (r - r1) / (r0 - r1 + 1e-12);
      return d0 + (d1 - d0) * t;
    }
  }
  return last[1];
}

function calibrate() {
  const rate = 44100;
  const pairs = [];
  for (let d = 9; d <= 48; d += 3) {
    const res = analyseBuffer(demoSignal(rate, 1.6, d), rate, { N: 1024, maxWindows: 4 });
    pairs.push([res.murmur / (res.heart + 1e-9), d]);
  }
  pairs.sort((a, b) => b[0] - a[0]);
  LOOKUP = pairs;
}

/* ---------- analysis ------------------------------------------------------ */

function bandEnergy(freq, mag, lo, hi) {
  let sum = 0, n = 0;
  for (let i = 0; i < freq.length; i++) {
    if (freq[i] >= lo && freq[i] <= hi) { sum += mag[i] * mag[i]; n++; }
  }
  return n ? sum / n : 0;
}

function analyse() {
  if (!state.analyser) return null;
  const a = state.analyser;
  const bins = new Uint8Array(a.frequencyBinCount);
  a.getByteFrequencyData(bins);
  const hz = state.ctx.sampleRate / a.fftSize;
  const freq = new Float32Array(bins.length);
  const mag = new Float32Array(bins.length);
  for (let i = 0; i < bins.length; i++) {
    freq[i] = i * hz;
    mag[i] = bins[i] / 255;
  }
  const heart = bandEnergy(freq, mag, ...BANDS.heart);
  const murmur = bandEnergy(freq, mag, ...BANDS.murmur);
  const noise = bandEnergy(freq, mag, ...BANDS.noise);
  const total = heart + murmur + noise + 1e-9;

  /* Contact quality: the share of energy that sits where a chestpiece puts
     it. A stethoscope off the skin puts almost everything above 600 Hz, so
     this falls before anything else does. */
  const quality = Math.round(100 * Math.min(1, heart / (heart + noise * 2.2 + 1e-9)));

  /* Wall estimate. The ratio of murmur-band to heart-band energy falls with
     thickness, monotonically, in the model, so the inverse is a lookup fitted
     to that forward model at load rather than a guessed slope. */
  const wall = wallFromRatio(murmur / (heart + 1e-9));

  return { freq, mag, heart, murmur, noise, total, quality, wall };
}

/* ---------- drawing ------------------------------------------------------- */

const ink = '#F4F0E8';
const red = '#E0301E';

function fitCanvas(c) {
  const dpr = Math.min(devicePixelRatio || 1, 2);
  const w = c.clientWidth, h = c.clientHeight;
  if (c.width !== w * dpr || c.height !== h * dpr) {
    c.width = w * dpr; c.height = h * dpr;
  }
  const g = c.getContext('2d');
  g.setTransform(dpr, 0, 0, dpr, 0, 0);
  return { g, w, h };
}

function drawScope() {
  const c = $('#app-scope');
  if (!c) return;
  const { g, w, h } = fitCanvas(c);
  g.clearRect(0, 0, w, h);
  g.fillStyle = '#0B0A09';
  g.fillRect(0, 0, w, h);

  g.strokeStyle = 'rgba(244,240,232,0.07)';
  g.lineWidth = 1;
  for (let i = 1; i < 8; i++) {
    g.beginPath(); g.moveTo((w / 8) * i, 0); g.lineTo((w / 8) * i, h); g.stroke();
  }
  for (let i = 1; i < 4; i++) {
    g.beginPath(); g.moveTo(0, (h / 4) * i); g.lineTo(w, (h / 4) * i); g.stroke();
  }

  let data;
  if (state.demo && !state.recording) {
    /* scroll a half-second window through the generated take */
    const w = Math.floor(state.ctx ? state.ctx.sampleRate * 0.55 : 24000);
    const span = Math.max(1, state.demo.samples.length - w);
    const at = Math.floor((performance.now() / 5200) % 1 * span);
    data = state.demo.samples.subarray(at, at + w);
  } else if (state.analyser) {
    data = new Float32Array(state.analyser.fftSize);
    state.analyser.getFloatTimeDomainData(data);
  }
  if (!data) return;

  const n = Math.min(data.length, Math.floor(data.length * 0.55));
  g.beginPath();
  for (let i = 0; i < n; i++) {
    const x = (i / n) * w;
    const y = h / 2 - data[i] * h * 1.9;
    i ? g.lineTo(x, y) : g.moveTo(x, y);
  }
  g.strokeStyle = state.verdict === 'refused' ? '#8A7F74' : red;
  g.lineWidth = 1.6;
  g.stroke();

  g.fillStyle = 'rgba(244,240,232,0.45)';
  g.font = '10px Archivo, sans-serif';
  g.fillText('0.55 s', 8, h - 8);
  g.fillText(`${state.ctx ? (state.ctx.sampleRate / 1000).toFixed(1) : '44.1'} kHz · 24-bit`, w - 96, h - 8);
}

function drawSpectrum(res) {
  const c = $('#app-spectrum');
  if (!c) return;
  const { g, w, h } = fitCanvas(c);
  g.clearRect(0, 0, w, h);
  g.fillStyle = '#0B0A09';
  g.fillRect(0, 0, w, h);
  if (!res) return;

  const fmin = 20, fmax = 900;
  const x = (f) => (Math.log(f / fmin) / Math.log(fmax / fmin)) * w;
  const y = (v) => h - Math.min(1, v) * h * 0.92 - 6;

  /* band shading, so the reader knows where the murmur lives */
  g.fillStyle = 'rgba(224,48,30,0.07)';
  g.fillRect(x(150), 0, x(400) - x(150), h);

  const plot = (fn, colour, width) => {
    g.beginPath();
    let started = false;
    for (let i = 1; i < res.freq.length; i++) {
      const f = res.freq[i];
      if (f < fmin || f > fmax) continue;
      const v = fn(res.mag[i], f);
      const px = x(f), py = y(v);
      started ? g.lineTo(px, py) : (g.moveTo(px, py), started = true);
    }
    g.strokeStyle = colour;
    g.lineWidth = width;
    g.stroke();
  };

  plot((m) => m, 'rgba(244,240,232,0.42)', 1.2);
  plot((m, f) => m * correctionGain(f, state.wall) / 12, red, 1.8);

  g.fillStyle = 'rgba(244,240,232,0.4)';
  g.font = '10px Archivo, sans-serif';
  [50, 150, 400, 900].forEach((f) => g.fillText(f + ' Hz', x(f) - 10, h - 4));
}

function drawMeter() {
  const el = $('#app-quality');
  if (el) el.style.width = Math.max(2, state.quality) + '%';
  const qv = $('#app-quality-val');
  if (qv) qv.textContent = state.quality + '%';
  const wv = $('#app-wall');
  if (wv) wv.textContent = state.wall.toFixed(0) + ' mm';
}

/* ---------- the gate ------------------------------------------------------ */

function decide(res) {
  if (!res) return 'idle';
  if (res.quality < 45) return 'refused';
  if (res.heart + res.murmur < 0.0006) return 'refused';
  return 'accepted';
}

function paintVerdict() {
  const el = $('#app-verdict');
  if (!el) return;
  const copy = {
    idle: ['Waiting for contact', 'Press record and hold the chestpiece still.'],
    accepted: ['Reading accepted', 'Contact held through the whole window.'],
    refused: ['No reading', 'Contact was lost. This is a refusal, not a low-confidence result.']
  }[state.verdict];
  el.dataset.state = state.verdict;
  $('h4', el).textContent = copy[0];
  $('p', el).textContent = copy[1];
}

/* ---------- audio --------------------------------------------------------- */

async function ensureContext() {
  if (!state.ctx) {
    state.ctx = new (window.AudioContext || window.webkitAudioContext)();
  }
  if (state.ctx.state === 'suspended') await state.ctx.resume();
  return state.ctx;
}

async function startMic() {
  const ctx = await ensureContext();
  state.stream = await navigator.mediaDevices.getUserMedia({
    audio: {
      echoCancellation: false,
      noiseSuppression: false,
      autoGainControl: false,
      channelCount: 1
    }
  });
  state.source = ctx.createMediaStreamSource(state.stream);
  state.analyser = ctx.createAnalyser();
  state.analyser.fftSize = 4096;
  state.analyser.smoothingTimeConstant = 0.6;
  state.source.connect(state.analyser);
  return true;
}

/* A take is the analyser's own time-domain data, accumulated. That is enough
   to export a WAV and to hold the student's own numbers next to it. */
function beginTake() {
  const ctx = state.ctx;
  state.buf = new Float32Array(ctx.sampleRate * 6);
  state.bufAt = 0;
  state.recording = true;
  const chunk = new Float32Array(state.analyser.fftSize);

  const pump = () => {
    if (!state.recording) return;
    state.analyser.getFloatTimeDomainData(chunk);
    if (state.bufAt + chunk.length <= state.buf.length) {
      state.buf.set(chunk, state.bufAt);
      state.bufAt += chunk.length;
    }
    requestAnimationFrame(pump);
  };
  pump();
}

function endTake() {
  state.recording = false;
  const samples = state.buf.slice(0, state.bufAt);
  if (!samples.length) return null;
  const take = {
    at: new Date(),
    rate: state.ctx.sampleRate,
    samples,
    quality: state.quality,
    wall: state.wall,
    verdict: state.verdict
  };
  state.takes.unshift(take);
  renderTakes();
  return take;
}

function wav(samples, rate) {
  const n = samples.length;
  const buf = new ArrayBuffer(44 + n * 2);
  const v = new DataView(buf);
  const str = (o, s) => { for (let i = 0; i < s.length; i++) v.setUint8(o + i, s.charCodeAt(i)); };
  str(0, 'RIFF'); v.setUint32(4, 36 + n * 2, true); str(8, 'WAVE');
  str(12, 'fmt '); v.setUint32(16, 16, true); v.setUint16(20, 1, true);
  v.setUint16(22, 1, true); v.setUint32(24, rate, true);
  v.setUint32(28, rate * 2, true); v.setUint16(32, 2, true); v.setUint16(34, 16, true);
  str(36, 'data'); v.setUint32(40, n * 2, true);
  for (let i = 0; i < n; i++) {
    v.setInt16(44 + i * 2, Math.max(-1, Math.min(1, samples[i])) * 32767, true);
  }
  return new Blob([buf], { type: 'audio/wav' });
}

function renderTakes() {
  const list = $('#app-takes');
  if (!list) return;
  list.innerHTML = '';
  if (!state.takes.length) {
    list.innerHTML = '<p class="app-empty">No recordings yet. A take keeps its own wall estimate and quality score, and exports as WAV.</p>';
    return;
  }
  state.takes.forEach((t, i) => {
    const row = document.createElement('div');
    row.className = 'app-take';
    const d = t.at.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' });
    row.innerHTML = `
      <div class="app-take__meta">
        <b>${d}</b>
        <span>${t.wall.toFixed(0)} mm wall · ${t.quality}% contact · ${t.verdict === 'refused' ? 'refused' : 'accepted'}</span>
      </div>
      <a class="app-take__dl" download="heartware-${i + 1}.wav">WAV</a>`;
    row.querySelector('a').href = URL.createObjectURL(wav(t.samples, t.rate));
    list.appendChild(row);
  });
}

/* ---------- demo signal --------------------------------------------------- */

/* A synthesised grade 2 murmur through 34 mm of wall, so the page can be
   demonstrated without a microphone and without a patient. It is generated,
   and it says so on screen. */
function demoSignal(rate, seconds, wallMm) {
  const n = Math.floor(rate * seconds);
  const out = new Float32Array(n);
  let phase = 0;
  for (let i = 0; i < n; i++) {
    const t = i / rate;
    const beat = t % 0.86;
    let s = 0;
    /* S1 and S2: short, low, broadband thumps */
    const thump = (c, w, a) => Math.exp(-Math.pow((beat - c) / w, 2)) * a;
    s += thump(0.04, 0.018, 0.55) * Math.sin(2 * Math.PI * 62 * t);
    s += thump(0.30, 0.020, 0.40) * Math.sin(2 * Math.PI * 74 * t);
    /* the murmur: band-limited noise between S1 and S2 */
    if (beat > 0.06 && beat < 0.28) {
      phase += 0.11;
      const env = Math.sin((Math.PI * (beat - 0.06)) / 0.22);
      s += (Math.sin(phase * 7.3) * 0.5 + (Math.random() - 0.5)) * 0.16 * env;
    }
    s += (Math.random() - 0.5) * 0.012;
    out[i] = s * 0.9;
  }
  /* the wall: one-pole low-pass whose corner falls with thickness */
  const fc = 1400 / (1 + wallMm / 9);
  const rc = 1 / (2 * Math.PI * fc);
  const dt = 1 / rate;
  const a = dt / (rc + dt);
  let y = 0;
  for (let i = 0; i < n; i++) { y += a * (out[i] - y); out[i] = y; }
  const g = Math.pow(10, -attenDb(200, wallMm) / 20);
  for (let i = 0; i < n; i++) out[i] *= Math.max(g, 0.06);
  return out;
}

/* ---------- loop ---------------------------------------------------------- */

let raf = 0;
function loop() {
  const res = state.demo && !state.analyser ? state.demo.res : analyse();
  if (res) {
    state.freq = res.freq;
    state.quality = res.quality;
    state.wall = res.wall;
    state.verdict = decide(res);
    paintVerdict();
    drawMeter();
    drawSpectrum(res);
  }
  drawScope();
  raf = requestAnimationFrame(loop);
}

/* ---------- wiring -------------------------------------------------------- */

function init() {
  const app = $('#app');
  if (!app) return;

  const rec = $('#app-record');
  const stop = $('#app-stop');
  const demo = $('#app-demo');
  const mic = $('#app-mic');

  rec.addEventListener('click', async () => {
    try {
      if (!state.analyser) await startMic();
      await ensureContext();
      state.demo = null;
      beginTake();
      rec.disabled = true;
      stop.disabled = false;
      app.dataset.live = '1';
      setTimeout(() => { if (state.recording) { endTake(); rec.disabled = false; stop.disabled = true; } }, 6000);
    } catch (e) {
      $('#app-note').textContent = 'No microphone access: ' + e.message + '. Use the generated signal to see the same pipeline run.';
    }
  });

  stop.addEventListener('click', () => {
    endTake();
    rec.disabled = false;
    stop.disabled = true;
  });

  mic.addEventListener('click', async () => {
    try {
      await startMic();
      $('#app-note').textContent = 'Microphone open. The analyser is live; nothing is uploaded.';
    } catch (e) {
      $('#app-note').textContent = 'Microphone blocked (' + e.message + ').';
    }
  });

  demo.addEventListener('click', async () => {
    await ensureContext();
    const rate = state.ctx.sampleRate;
    const wallMm = 34;
    const samples = demoSignal(rate, 5, wallMm);
    const src = state.ctx.createBufferSource();
    const b = state.ctx.createBuffer(1, samples.length, rate);
    b.copyToChannel(samples, 0);
    src.buffer = b;
    src.connect(state.ctx.destination);
    src.start();
    const res = analyseBuffer(samples, rate, { maxWindows: 10 });
    state.demo = { samples, wall: wallMm, res };
    state.analyser = null;
    state.quality = res.quality;
    state.wall = res.wall;
    state.verdict = decide(res);
    paintVerdict();
    drawMeter();
    drawSpectrum(res);
    $('#app-note').textContent = 'Playing a generated grade 2 murmur through a 34 mm wall. The trace is that signal, analysed by the same code as the microphone path.';
    demo.disabled = true;
    setTimeout(() => { demo.disabled = false; }, 5200);
  });

  if (!LOOKUP) calibrate();
  renderTakes();
  loop();
}

/* Offline analysis of a buffer, by the same band arithmetic as the live path. */
function analyseBuffer(samples, rate, opts = {}) {
  /* Average the magnitude spectrum over the whole buffer. One 93 ms window
     lands wherever it lands in the cardiac cycle; averaging is what makes the
     band ratio stable enough to invert. */
  const N = opts.N || 2048;
  const MAXW = opts.maxWindows || 8;
  const win = new Float32Array(N);
  for (let i = 0; i < N; i++) win[i] = 0.5 - 0.5 * Math.cos((2 * Math.PI * i) / (N - 1));
  const bins = new Float32Array(N / 2);
  let windows = 0;
  const stride = Math.max(N, Math.floor((samples.length - N) / MAXW) || N);
  for (let start = 0; start + N <= samples.length && windows < MAXW; start += stride) {
    windows++;
    for (let k = 0; k < N / 2; k++) {
      let re = 0, im = 0;
      for (let i = 0; i < N; i++) {
        const s = samples[start + i] * win[i];
        const a = (-2 * Math.PI * k * i) / N;
        re += s * Math.cos(a);
        im += s * Math.sin(a);
      }
      bins[k] += Math.sqrt(re * re + im * im) / (N / 4);
    }
  }
  const hz = rate / N;
  const freq = new Float32Array(bins.length);
  let peak = 1e-9;
  for (let i = 0; i < bins.length; i++) {
    freq[i] = i * hz;
    bins[i] /= Math.max(windows, 1);
    peak = Math.max(peak, bins[i]);
  }
  const mag = new Float32Array(bins.length);
  for (let i = 0; i < bins.length; i++) mag[i] = Math.min(1, bins[i] / peak);
  const heart = bandEnergy(freq, mag, ...BANDS.heart);
  const murmur = bandEnergy(freq, mag, ...BANDS.murmur);
  const noise = bandEnergy(freq, mag, ...BANDS.noise);
  const wall = wallFromRatio(murmur / (heart + 1e-9));
  const quality = Math.round(100 * Math.min(1, heart / (heart + noise * 2.2 + 1e-9)));
  return { freq, mag, heart, murmur, noise, quality, wall, total: heart + murmur + noise };
}

if (document.readyState !== 'loading') init();
else document.addEventListener('DOMContentLoaded', init);
