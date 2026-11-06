/* ============================================================
   Heartware — site behaviour
   Charts, scroll states, the chest-wall demo, tabs.
   No dependencies.
   ============================================================ */

const reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
const $  = (s, r = document) => r.querySelector(s);
const $$ = (s, r = document) => [...r.querySelectorAll(s)];

/* ------------------------------------------------------------
   Validation numbers
   The intervals are the reported ones. When the confusion
   matrix is entered below, the page recomputes every interval
   from the counts and the reported values become a check.
   ------------------------------------------------------------ */
const VALIDATION = {
  // tp, fn, tn, fp — fill from the validation run. null = not entered.
  counts: { tp: null, fn: null, tn: null, fp: null },
  reported: {
    sens: { lo: 84.6, hi: 93.4 },
    spec: { lo: 89.6, hi: 95.3 },
    acc:  { lo: 89.1, hi: 93.9 }
  }
};

function wilson(k, n, z = 1.959964) {
  if (!n) return null;
  const p = k / n;
  const den = 1 + (z * z) / n;
  const centre = (p + (z * z) / (2 * n)) / den;
  const half = (z / den) * Math.sqrt((p * (1 - p)) / n + (z * z) / (4 * n * n));
  return { p, lo: Math.max(0, centre - half) * 100, hi: Math.min(1, centre + half) * 100 };
}

function derived() {
  const c = VALIDATION.counts;
  const total = ['tp', 'fn', 'tn', 'fp'].every(k => typeof c[k] === 'number');
  if (!total) return null;
  const pos = c.tp + c.fn;
  const neg = c.tn + c.fp;
  return {
    sens: wilson(c.tp, pos),
    spec: wilson(c.tn, neg),
    acc:  wilson(c.tp + c.tn, pos + neg),
    counts: c
  };
}

const METRIC_COPY = {
  sens: { label: 'Sensitivity', hint: 'of true positives found' },
  spec: { label: 'Specificity', hint: 'of true negatives cleared' },
  acc:  { label: 'Accuracy', hint: 'of all recordings classified correctly' }
};

function buildMetrics() {
  const d = derived();
  $$('.metric').forEach(card => {
    const key = card.dataset.metric;
    const rangeEl = $('[data-range]', card);
    const band = $('.ci-band', card);
    const tick = $('.ci-tick', card);
    const v = (d && d[key]) || VALIDATION.reported[key];

    rangeEl.textContent = `${v.lo.toFixed(1)}–${v.hi.toFixed(1)}%`;

    // the track is a 70–100% window: an interval plot zoomed to where
    // these numbers actually live, with both ends labelled in the card
    const T0 = 70, T1 = 100, SPAN = T1 - T0;
    const pos = x => Math.max(0, Math.min(100, ((x - T0) / SPAN) * 100));
    requestAnimationFrame(() => {
      band.style.left = `${pos(v.lo)}%`;
      band.style.width = `${Math.max(1.2, pos(v.hi) - pos(v.lo))}%`;
      if (d && tick) {
        tick.style.left = `${pos(v.p * 100)}%`;
        tick.style.opacity = '1';
      } else if (tick) {
        tick.remove();
      }
    });

    if (d && d.counts) {
      const ci = $('.metric-ci', card);
      ci.textContent = `95% Wilson interval · ${d[key].p * 100 < 100 ? (d[key].p * 100).toFixed(1) + '% from the counts' : ''}`;
    }
  });
}

/* ------------------------------------------------------------
   Nav, progress, mobile menu
   ------------------------------------------------------------ */
const nav = $('#nav');
const progressBar = $('#progress-bar');
const navLinks = $('#nav-links');
const navToggle = $('#nav-toggle');

let lastY = 0;
function onScroll() {
  const y = window.scrollY;
  nav.classList.toggle('scrolled', y > 40);

  const h = document.documentElement.scrollHeight - window.innerHeight;
  progressBar.style.width = `${h > 0 ? Math.min(100, (y / h) * 100) : 0}%`;

  const heroInner = $('#hero-inner');
  if (heroInner && y < window.innerHeight * 1.2 && !reduced) {
    heroInner.style.transform = `translateY(${y * 0.16}px)`;
    heroInner.style.opacity = String(Math.max(0, 1 - y / (window.innerHeight * 0.72)));
  }
  lastY = y;
}
window.addEventListener('scroll', onScroll, { passive: true });
onScroll();

navToggle?.addEventListener('click', () => {
  const open = navLinks.classList.toggle('open');
  navToggle.setAttribute('aria-expanded', String(open));
});
$$('#nav-links a').forEach(a => a.addEventListener('click', () => {
  navLinks.classList.remove('open');
  navToggle?.setAttribute('aria-expanded', 'false');
}));

/* active section */
const sectionIds = ['problem', 'physics', 'device', 'app', 'evidence', 'comparison', 'team'];
const navMap = new Map();
$$('#nav-links a').forEach(a => navMap.set(a.getAttribute('href').slice(1), a));
if ('IntersectionObserver' in window) {
  const spy = new IntersectionObserver(entries => {
    entries.forEach(e => {
      const link = navMap.get(e.target.id);
      if (!link) return;
      if (e.isIntersecting) {
        navMap.forEach(l => l.classList.remove('active'));
        link.classList.add('active');
      }
    });
  }, { rootMargin: '-45% 0px -50% 0px' });
  sectionIds.forEach(id => { const el = document.getElementById(id); if (el) spy.observe(el); });
}

/* ------------------------------------------------------------
   Reveal
   ------------------------------------------------------------ */
if (!reduced && 'IntersectionObserver' in window) {
  const revealer = new IntersectionObserver((entries, obs) => {
    entries.forEach(e => {
      if (!e.isIntersecting) return;
      const delay = Number(e.target.dataset.delay || 0);
      setTimeout(() => e.target.classList.add('in'), delay);
      obs.unobserve(e.target);
    });
  }, { rootMargin: '0px 0px -8% 0px', threshold: 0.12 });

  $$('[data-reveal]').forEach((el, i) => {
    const siblings = [...el.parentElement.children].filter(c => c.hasAttribute('data-reveal'));
    el.dataset.delay = String(Math.min(6, siblings.indexOf(el)) * 70);
    revealer.observe(el);
  });
} else {
  $$('[data-reveal]').forEach(el => el.classList.add('in'));
}

/* ------------------------------------------------------------
   Counters
   ------------------------------------------------------------ */
$$('[data-count]').forEach(el => {
  const target = parseFloat(el.dataset.count);
  const decimals = Number(el.dataset.decimals || 0);
  const suffix = el.dataset.suffix || '';
  const frame = () => {
    const start = performance.now();
    const dur = 1100;
    const step = now => {
      const t = Math.min(1, (now - start) / dur);
      const eased = 1 - Math.pow(1 - t, 3);
      el.textContent = (target * eased).toFixed(decimals) + suffix;
      if (t < 1) requestAnimationFrame(step);
    };
    requestAnimationFrame(step);
  };
  if (reduced) { el.textContent = target.toFixed(decimals) + suffix; return; }
  if ('IntersectionObserver' in window) {
    const io = new IntersectionObserver((entries, obs) => {
      if (entries[0].isIntersecting) { frame(); obs.disconnect(); }
    }, { threshold: 0.6 });
    io.observe(el);
  } else frame();
});

/* ------------------------------------------------------------
   Hero pointer glow
   ------------------------------------------------------------ */
const glow = $('#hero-glow');
if (glow && !reduced && window.matchMedia('(hover:hover)').matches) {
  let raf = null, mx = 0, my = 0;
  window.addEventListener('pointermove', e => {
    mx = e.clientX; my = e.clientY;
    if (raf) return;
    raf = requestAnimationFrame(() => {
      glow.style.left = `${mx}px`;
      glow.style.top = `${my}px`;
      raf = null;
    });
  }, { passive: true });
}

/* ------------------------------------------------------------
   App tabs
   ------------------------------------------------------------ */
const shots = { heart: './assets/img/app_heart.webp', lungs: './assets/img/app_lungs.webp', other: './assets/img/app_other.webp' };
const shot = $('#app-shot');
$$('.tabs button').forEach(btn => {
  btn.addEventListener('click', () => {
    if (btn.getAttribute('aria-selected') === 'true') return;
    $$('.tabs button').forEach(b => b.setAttribute('aria-selected', String(b === btn)));
    $$('.panel').forEach(p => { p.hidden = p.id !== `panel-${btn.id.split('-')[1]}`; });

    const key = btn.dataset.shot;
    if (!shot || !shots[key]) return;
    shot.classList.add('swapping');
    const next = new Image();
    next.onload = () => {
      shot.src = shots[key];
      shot.classList.remove('swapping');
    };
    next.src = shots[key];
  });
});

/* ------------------------------------------------------------
   Chest-wall model (illustrative, single absorption coefficient)
   a(f) = A * (f / 250)^0.7  dB per mm
   ------------------------------------------------------------ */
const A_DB_PER_MM = 0.5;
const absorption = f => A_DB_PER_MM * Math.pow(f / 250, 0.7);
const lossDb = (f, d) => absorption(f) * d;

/* murmur source spectrum, arbitrary units: broad bump around 260 Hz */
function source(f) {
  const peak = Math.exp(-Math.pow((Math.log(f / 260)) / 0.55, 2));
  const lowRoll = 1 / (1 + Math.pow(140 / f, 4));
  return 0.98 * peak * lowRoll + 0.05;
}

const state = { d: 28 };

const chestSlider = $('#chestwall');
const chestOut = $('#chestwall-out');
const out250 = $('#attn-250');
const outRec = $('#attn-rec');
const outGain = $('#attn-gain');

function demoNumbers() {
  const d = state.d;
  const a250 = lossDb(250, d);
  out250.textContent = `−${a250.toFixed(1)} dB`;
  outRec.textContent = `${(a250 * 0.85).toFixed(1)} dB`;
  const net = 20 - a250;
  outGain.textContent = net >= 0 ? `+${net.toFixed(1)} dB` : `−${Math.abs(net).toFixed(1)} dB`;
  outGain.style.color = net >= 0 ? 'var(--green)' : 'var(--red)';
}

chestSlider?.addEventListener('input', e => {
  state.d = Number(e.target.value);
  chestOut.textContent = `${state.d} mm`;
  demoNumbers();
  drawSpectrum();
});
demoNumbers();

/* ------------------------------------------------------------
   Canvas helpers
   ------------------------------------------------------------ */
function prep(canvas) {
  if (!canvas) return null;
  const dpr = Math.min(2, window.devicePixelRatio || 1);
  const w = canvas.clientWidth || canvas.width;
  const h = canvas.clientHeight || (canvas.width * 9) / 16;
  const ratio = canvas.height / canvas.width;
  canvas.width = Math.round(w * dpr);
  canvas.height = Math.round(w * ratio * dpr);
  const ctx = canvas.getContext('2d');
  ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
  ctx.clearRect(0, 0, w, w * ratio);
  return { ctx, w, h: w * ratio };
}

const INK = 'rgba(232,238,244,.92)';
const DIM = 'rgba(150,175,193,.55)';
const FAINT = 'rgba(150,175,193,.16)';

function axes(ctx, w, h, xLabel, yLabel) {
  const pad = { l: 46, r: 12, t: 14, b: 40 };
  ctx.save();
  ctx.strokeStyle = FAINT;
  ctx.lineWidth = 1;
  for (let i = 0; i <= 4; i++) {
    const y = pad.t + ((h - pad.t - pad.b) * i) / 4;
    ctx.beginPath(); ctx.moveTo(pad.l, y); ctx.lineTo(w - pad.r, y); ctx.stroke();
  }
  ctx.strokeStyle = 'rgba(150,175,193,.35)';
  ctx.beginPath();
  ctx.moveTo(pad.l, pad.t); ctx.lineTo(pad.l, h - pad.b); ctx.lineTo(w - pad.r, h - pad.b);
  ctx.stroke();
  ctx.fillStyle = DIM;
  ctx.font = '10px "JetBrains Mono", monospace';
  ctx.textAlign = 'left';
  ctx.fillText(yLabel, 4, pad.t + 9);
  ctx.textAlign = 'right';
  ctx.fillText(xLabel, w - pad.r, h - 5);
  ctx.restore();
  return pad;
}

function xTicks(ctx, h, list, X) {
  ctx.fillStyle = DIM;
  ctx.font = '10px "JetBrains Mono", monospace';
  list.forEach((f, i) => {
    ctx.textAlign = i === list.length - 1 ? 'right' : 'center';
    ctx.fillText(String(f), X(f) + (i === list.length - 1 ? 4 : 0), h - 22);
  });
}

/* Figure 1: attenuation at three body compositions */
function drawAttenuation() {
  const canvas = $('#fig-attenuation');
  const p = prep(canvas);
  if (!p) return;
  const { ctx, w, h } = p;
  const pad = axes(ctx, w, h, 'frequency, Hz', 'dB');
  const fMin = 50, fMax = 700;
  const dbMax = 55;
  const X = f => pad.l + ((f - fMin) / (fMax - fMin)) * (w - pad.l - pad.r);
  const Y = db => h - pad.b - (db / dbMax) * (h - pad.t - pad.b);

  const sets = [
    { d: 15, color: '#4fd1a5', label: '15 mm' },
    { d: 28, color: '#35c9ff', label: '28 mm' },
    { d: 48, color: '#ff5f6a', label: '48 mm' }
  ];

  // ticks
  xTicks(ctx, h, [100, 250, 400, 700], X);
  ctx.fillStyle = DIM;
  ctx.font = '10px "JetBrains Mono", monospace';
  ctx.textAlign = 'right';
  [0, 20, 40].forEach(db => ctx.fillText(String(db), pad.l - 8, Y(db) + 3));

  // 250 Hz marker
  ctx.strokeStyle = 'rgba(232,189,119,.4)';
  ctx.setLineDash([3, 4]);
  ctx.beginPath(); ctx.moveTo(X(250), pad.t); ctx.lineTo(X(250), h - pad.b); ctx.stroke();
  ctx.setLineDash([]);

  sets.forEach(s => {
    ctx.beginPath();
    for (let f = fMin; f <= fMax; f += 4) {
      const db = Math.min(dbMax, lossDb(f, s.d));
      const x = X(f), y = Y(db);
      f === fMin ? ctx.moveTo(x, y) : ctx.lineTo(x, y);
    }
    ctx.strokeStyle = s.color;
    ctx.lineWidth = 2;
    ctx.lineJoin = 'round';
    ctx.stroke();
    ctx.lineTo(X(fMax), Y(0)); ctx.lineTo(X(fMin), Y(0)); ctx.closePath();
    ctx.fillStyle = s.color.replace(')', ',.07)').replace('rgb', 'rgba');
    if (s.color.startsWith('#')) {
      const r = parseInt(s.color.slice(1, 3), 16), g = parseInt(s.color.slice(3, 5), 16), b = parseInt(s.color.slice(5, 7), 16);
      ctx.fillStyle = `rgba(${r},${g},${b},.07)`;
    }
    ctx.fill();
  });

  ctx.fillStyle = 'rgba(232,189,119,.85)';
  ctx.font = '10px "JetBrains Mono", monospace';
  ctx.textAlign = 'left';
  ctx.fillText('250 Hz', X(250) + 6, pad.t + 10);
}
drawAttenuation();

/* Interactive spectrum */
function drawSpectrum() {
  const canvas = $('#fig-spectrum');
  const p = prep(canvas);
  if (!p) return;
  const { ctx, w, h } = p;
  const pad = axes(ctx, w, h, 'frequency, Hz', 'amplitude');
  const fMin = 50, fMax = 700;
  const X = f => pad.l + ((f - fMin) / (fMax - fMin)) * (w - pad.l - pad.r);
  const Y = a => h - pad.b - Math.max(0, Math.min(1, a)) * (h - pad.t - pad.b);
  const dB = db => Math.pow(10, -db / 20);

  xTicks(ctx, h, [100, 250, 400, 700], X);

  const curves = [
    { label: 'at the valve', color: 'rgba(150,175,193,.55)', dash: [4, 4], fn: f => source(f) },
    { label: 'received', color: '#ff5f6a', dash: [], fn: f => source(f) * dB(lossDb(f, state.d)) },
    { label: 'corrected', color: '#35c9ff', dash: [], fn: f => Math.min(1.15, source(f) * dB(lossDb(f, state.d)) * dB(-lossDb(f, state.d) * 0.85)) }
  ];

  curves.forEach(c => {
    ctx.beginPath();
    for (let f = fMin; f <= fMax; f += 3) {
      const x = X(f), y = Y(c.fn(f));
      f === fMin ? ctx.moveTo(x, y) : ctx.lineTo(x, y);
    }
    ctx.strokeStyle = c.color;
    ctx.lineWidth = c === curves[1] ? 2 : 1.7;
    ctx.setLineDash(c.dash);
    ctx.stroke();
    ctx.setLineDash([]);
  });

  // legend, bottom-right of the plot with a backdrop so it never sits on a curve
  const lx = w - pad.r - 118,
        lyTop = h - pad.b - 62;
  ctx.fillStyle = 'rgba(9,14,18,.82)';
  ctx.strokeStyle = 'rgba(150,175,193,.18)';
  ctx.lineWidth = 1;
  ctx.beginPath();
  ctx.roundRect(lx, lyTop, 110, 54, 6);
  ctx.fill();
  ctx.stroke();
  ctx.font = '10px "JetBrains Mono", monospace';
  ctx.textAlign = 'left';
  curves.forEach((c, i) => {
    const y = lyTop + 14 + i * 14;
    ctx.fillStyle = c.color;
    ctx.fillRect(lx + 10, y - 3, 12, 2);
    ctx.fillText(c.label, lx + 30, y + 1);
  });
}
drawSpectrum();

/* ------------------------------------------------------------
   CI bands + price bars on view
   ------------------------------------------------------------ */
buildMetrics();

if ('IntersectionObserver' in window) {
  const bars = new IntersectionObserver((entries, obs) => {
    entries.forEach(e => {
      if (!e.isIntersecting) return;
      const el = e.target;
      if (el.classList.contains('bar')) {
        const v = Number(el.dataset.value);
        const max = Number(el.dataset.max || 500);
        requestAnimationFrame(() => { el.style.width = `${(v / max) * 100}%`; });
      }
      if (el.classList.contains('metric')) el.classList.add('in');
      obs.unobserve(el);
    });
  }, { threshold: 0.35 });
  $$('.bar').forEach(b => bars.observe(b));
  $$('.metric').forEach(m => bars.observe(m));
} else {
  $$('.bar').forEach(el => { el.style.width = `${(Number(el.dataset.value) / Number(el.dataset.max || 500)) * 100}%`; });
}

/* redraw canvases on resize, debounced */
let rt = null;
window.addEventListener('resize', () => {
  clearTimeout(rt);
  rt = setTimeout(() => { drawAttenuation(); drawSpectrum(); }, 180);
});
