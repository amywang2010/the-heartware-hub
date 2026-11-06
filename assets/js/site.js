/* ============================================================
   Heartware — page behaviour
   Hero staging, the heart cursor light, the chest-wall demo,
   app tabs, reveals. No dependencies.
   ============================================================ */

const $  = (s, r = document) => r.querySelector(s);
const $$ = (s, r = document) => [...r.querySelectorAll(s)];
const reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

/* ------------------------------------------------------------
   Nav, progress bar, mobile menu
   ------------------------------------------------------------ */
const nav = $('#nav');
const bar = $('#progress-bar');
const navLinks = $('#nav-links');
const navToggle = $('#nav-toggle');

function onScroll() {
  const y = window.scrollY;
  if (nav) nav.classList.toggle('is-scrolled', y > 40);
  if (bar) {
    const h = document.documentElement.scrollHeight - window.innerHeight;
    bar.style.width = `${h > 0 ? Math.min(100, (y / h) * 100) : 0}%`;
  }
  stageHero(y);
}

function setMenu(open) {
  if (!navLinks) return;
  navLinks.classList.toggle('open', open);
  navToggle?.setAttribute('aria-expanded', String(open));
  document.body.style.overflow = open ? 'hidden' : '';
}
navToggle?.addEventListener('click', () => setMenu(!navLinks.classList.contains('open')));
$$('#nav-links a').forEach((a) => a.addEventListener('click', () => setMenu(false)));
document.addEventListener('keydown', (e) => {
  if (e.key === 'Escape' && navLinks?.classList.contains('open')) setMenu(false);
});

/* ------------------------------------------------------------
   Hero: second panel fades in while the pin is held
   ------------------------------------------------------------ */
const hero = $('.hero');
function stageHero() {
  if (!hero) return;
  const run = Math.max(1, hero.offsetHeight - window.innerHeight);
  const p = Math.min(1, Math.max(0, -hero.getBoundingClientRect().top / run));
  hero.classList.toggle('is-stage-2', p > 0.3);
  const copy = $('#hero-copy-1');
  if (copy && !reduced) copy.style.setProperty('--p', p.toFixed(3));
}

/* ------------------------------------------------------------
   Pointer: warm glow everywhere, a heart-shaped light in the hero
   ------------------------------------------------------------ */
const glow = $('#cursor-glow');
const spot = $('#spot');
const spotHeart = $('#spot-heart');
const pin = $('.hero-pin');

const pointerState = { x: innerWidth / 2, y: innerHeight * 0.45, tx: innerWidth / 2, ty: innerHeight * 0.45, active: false };

if (glow && !reduced && matchMedia('(pointer:fine)').matches) {
  window.addEventListener('pointermove', (e) => {
    pointerState.tx = e.clientX;
    pointerState.ty = e.clientY;
    if (!pointerState.active) {
      pointerState.active = true;
      glow.style.opacity = '1';
    }
  }, { passive: true });
  window.addEventListener('pointerleave', () => { glow.style.opacity = '0'; });

  if (spot) {
    pin?.addEventListener('pointerenter', () => { spot.style.opacity = '1'; });
    pin?.addEventListener('pointerleave', () => { spot.style.opacity = '0'; });
  }

  const tick = () => {
    pointerState.x += (pointerState.tx - pointerState.x) * 0.14;
    pointerState.y += (pointerState.ty - pointerState.y) * 0.14;

    glow.style.transform = `translate3d(${pointerState.x}px, ${pointerState.y}px, 0)`;

    if (spot && spotHeart && pin) {
      const r = pin.getBoundingClientRect();
      const lx = pointerState.x - r.left;
      const ly = pointerState.y - r.top;
      spotHeart.style.transform = `translate3d(${lx}px, ${ly}px, 0) rotate(${(pointerState.x - pointerState.y) * 0.004}deg)`;
      spot.style.opacity = (ly > 0 && ly < r.height) ? spot.style.opacity : '0';
    }
    requestAnimationFrame(tick);
  };
  requestAnimationFrame(tick);
}

/* ------------------------------------------------------------
   Reveals
   ------------------------------------------------------------ */
if ('IntersectionObserver' in window && !reduced) {
  const io = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.classList.add('is-in');
        io.unobserve(entry.target);
      }
    });
  }, { rootMargin: '0px 0px -8% 0px', threshold: 0.12 });
  $$('[data-reveal]').forEach((el) => io.observe(el));
} else {
  $$('[data-reveal]').forEach((el) => el.classList.add('is-in'));
}

/* ------------------------------------------------------------
   Counters
   ------------------------------------------------------------ */
const counted = new WeakSet();
function runCounter(el) {
  if (counted.has(el)) return;
  counted.add(el);
  const target = parseFloat(el.dataset.count);
  if (Number.isNaN(target)) return;
  const tail = el.innerHTML.replace(/^[\d.,]+/, '');
  const dec = (el.dataset.decimals | 0);
  const dur = 1100;
  const start = performance.now();
  const step = (now) => {
    const t = Math.min(1, (now - start) / dur);
    const e = 1 - Math.pow(1 - t, 3);
    el.innerHTML = (target * e).toFixed(dec) + tail;
    if (t < 1) requestAnimationFrame(step);
    else el.innerHTML = target + tail;
  };
  if (reduced) el.innerHTML = target + tail;
  else requestAnimationFrame(step);
}

if ('IntersectionObserver' in window) {
  const co = new IntersectionObserver((entries) => {
    entries.forEach((e) => {
      if (e.isIntersecting) { runCounter(e.target); co.unobserve(e.target); }
    });
  }, { threshold: 0.5 });
  $$('[data-count]').forEach((el) => co.observe(el));
} else {
  $$('[data-count]').forEach(runCounter);
}

/* ------------------------------------------------------------
   The chest-wall demo
   ------------------------------------------------------------ */
const FIG = {
  fMin: 40,
  fMax: 900,
  yMin: -52,
  yMax: 28
};

// relative source spectrum at the valve, dB
function sourceDb(f) {
  const x = Math.log2(f / 210);
  return Math.max(-46, 3.5 - 7.2 * x * x);
}
// soft-tissue absorption, dB. 0.05 dB/mm at 100 Hz, rising as f^1.4
function lossDb(f, d) {
  return 0.05 * d * Math.pow(f / 100, 1.4);
}

const spec = $('#fig-spectrum');
const slider = $('#chestwall');
const out = $('#chestwall-out');
const r250 = $('#attn-250');
const rRec = $('#attn-rec');
const rGain = $('#attn-gain');

function drawSpectrum() {
  if (!spec) return;
  const dpr = Math.min(window.devicePixelRatio || 1, 2);
  const w = spec.clientWidth || 620;
  const h = Math.round(w * (400 / 620));
  if (spec.width !== Math.round(w * dpr) || spec.height !== Math.round(h * dpr)) {
    spec.width = Math.round(w * dpr);
    spec.height = Math.round(h * dpr);
    spec.style.height = h + 'px';
  }
  const ctx = spec.getContext('2d');
  ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
  ctx.clearRect(0, 0, w, h);

  const pad = { l: 44, r: 58, t: 18, b: 30 };
  const iw = w - pad.l - pad.r;
  const ih = h - pad.t - pad.b;
  const d = parseFloat(slider?.value || 28);

  const X = (f) => pad.l + (Math.log(f / FIG.fMin) / Math.log(FIG.fMax / FIG.fMin)) * iw;
  const Y = (db) => pad.t + ih - ((Math.max(FIG.yMin, Math.min(FIG.yMax, db)) - FIG.yMin) / (FIG.yMax - FIG.yMin)) * ih;

  // grid
  ctx.font = '10px "JetBrains Mono", monospace';
  ctx.fillStyle = 'rgba(196,174,178,.55)';
  ctx.strokeStyle = 'rgba(255,255,255,.07)';
  ctx.lineWidth = 1;
  [50, 100, 200, 400, 800].forEach((f) => {
    const x = Math.round(X(f)) + 0.5;
    ctx.beginPath(); ctx.moveTo(x, pad.t); ctx.lineTo(x, pad.t + ih); ctx.stroke();
    ctx.textAlign = 'center';
    ctx.fillText(f >= 1000 ? (f / 1000) + 'k' : String(f), x, h - 10);
  });
  ctx.textAlign = 'right';
  for (let db = -40; db <= 20; db += 20) {
    const y = Math.round(Y(db)) + 0.5;
    ctx.beginPath(); ctx.moveTo(pad.l, y); ctx.lineTo(pad.l + iw, y); ctx.stroke();
    ctx.fillText(db + ' dB', pad.l - 8, y + 3);
  }

  const series = (fn, from = FIG.fMin, to = FIG.fMax) => {
    const pts = [];
    for (let i = 0; i <= 180; i++) {
      const f = from * Math.pow(to / from, i / 180);
      pts.push([X(f), Y(fn(f))]);
    }
    return pts;
  };
  const line = (pts, stroke, width, dash = []) => {
    ctx.beginPath();
    pts.forEach(([x, y], i) => (i ? ctx.lineTo(x, y) : ctx.moveTo(x, y)));
    ctx.setLineDash(dash);
    ctx.strokeStyle = stroke;
    ctx.lineWidth = width;
    ctx.stroke();
    ctx.setLineDash([]);
    return pts;
  };

  const src = series((f) => sourceDb(f));
  const skin = series((f) => sourceDb(f) - lossDb(f, d));
  const inv = series((f) => sourceDb(f) - lossDb(f, d) * 0.94);
  const gain = series((f) => sourceDb(f) - lossDb(f, d) + 20);

  // fill under the attenuated curve
  const grad = ctx.createLinearGradient(0, pad.t, 0, pad.t + ih);
  grad.addColorStop(0, 'rgba(255,61,99,.34)');
  grad.addColorStop(1, 'rgba(226,18,59,.02)');
  ctx.beginPath();
  skin.forEach(([x, y], i) => (i ? ctx.lineTo(x, y) : ctx.moveTo(x, y)));
  ctx.lineTo(X(FIG.fMax), pad.t + ih);
  ctx.lineTo(X(FIG.fMin), pad.t + ih);
  ctx.closePath();
  ctx.fillStyle = grad;
  ctx.fill();

  line(gain, 'rgba(255,255,255,.2)', 1.2, [2, 5]);
  line(src, 'rgba(255,255,255,.42)', 1.2, [4, 5]);
  line(inv, 'rgba(157,180,255,.95)', 2, [6, 5]);

  // the attenuated curve, with a soft glow
  ctx.save();
  ctx.shadowColor = 'rgba(255,61,99,.6)';
  ctx.shadowBlur = 14;
  line(skin, '#FF3D63', 2.6);
  ctx.restore();

  // 250 Hz marker
  const xm = X(250);
  ctx.beginPath();
  ctx.setLineDash([3, 4]);
  ctx.moveTo(xm, pad.t); ctx.lineTo(xm, pad.t + ih);
  ctx.strokeStyle = 'rgba(255,201,212,.28)';
  ctx.lineWidth = 1;
  ctx.stroke();
  ctx.setLineDash([]);
  ctx.beginPath();
  ctx.arc(xm, Y(sourceDb(250) - lossDb(250, d)), 3.4, 0, Math.PI * 2);
  ctx.fillStyle = '#fff';
  ctx.fill();

  // inline labels
  ctx.font = '10px "JetBrains Mono", monospace';
  ctx.textAlign = 'left';
  ctx.fillStyle = 'rgba(255,61,99,.95)';
  ctx.fillText('at the skin', X(FIG.fMax) - 2, Y(sourceDb(FIG.fMax) - lossDb(FIG.fMax, d)) - 10);
  ctx.fillStyle = 'rgba(157,180,255,.95)';
  ctx.fillText('after inversion', X(FIG.fMax) - 2, Y(sourceDb(FIG.fMax) - lossDb(FIG.fMax, d) * 0.94) - 26);

  if (out) out.textContent = `${d} mm`;
  if (r250) r250.textContent = `−${lossDb(250, d).toFixed(1)} dB`;
  if (rRec) rRec.textContent = `+${(lossDb(250, d) * 0.94).toFixed(1)} dB`;
  if (rGain) rGain.textContent = `−${(lossDb(800, d) - lossDb(250, d)).toFixed(0)} dB tilt`;
}

if (slider) {
  slider.addEventListener('input', drawSpectrum);
  drawSpectrum();
  window.addEventListener('resize', () => { if (!reduced) drawSpectrum(); });
  // redraw once fonts have settled, so the labels are not in the fallback face
  if (document.fonts?.ready) document.fonts.ready.then(drawSpectrum);
}

/* ------------------------------------------------------------
   App tabs
   ------------------------------------------------------------ */
const SHOTS = {
  heart: { src: './assets/img/app_heart.webp', alt: 'Heartware app showing a phonocardiogram with S1 and S2 marked and a systolic murmur at the aortic site.' },
  lungs: { src: './assets/img/app_lungs.webp', alt: 'Heartware app showing a lung examination with the right base selected and no crackles reported.' },
  other: { src: './assets/img/app_other.webp', alt: 'Heartware app showing bowel sounds at nine per minute and no bruit.' }
};

const tabs = $$('.tabs [role="tab"]');
const shot = $('#app-shot');

function selectTab(id) {
  tabs.forEach((t) => {
    const on = t.id === id;
    t.setAttribute('aria-selected', String(on));
    t.tabIndex = on ? 0 : -1;
    const panel = document.getElementById(t.getAttribute('aria-controls'));
    if (panel) panel.hidden = !on;
  });
  const key = document.getElementById(id)?.dataset.shot;
  if (shot && key && SHOTS[key]) {
    shot.style.opacity = '0';
    setTimeout(() => {
      shot.src = SHOTS[key].src;
      shot.alt = SHOTS[key].alt;
      shot.style.opacity = '1';
    }, 140);
  }
}

if (shot) {
  shot.style.transition = 'opacity .28s ease';
  tabs.forEach((t, i) => {
    t.addEventListener('click', () => selectTab(t.id));
    t.addEventListener('keydown', (e) => {
      if (e.key !== 'ArrowRight' && e.key !== 'ArrowLeft') return;
      e.preventDefault();
      const next = tabs[(i + (e.key === 'ArrowRight' ? 1 : -1) + tabs.length) % tabs.length];
      next.focus();
      selectTab(next.id);
    });
  });
}

/* ------------------------------------------------------------
   Video: only fetch the file when it is played
   ------------------------------------------------------------ */
const film = $('#film-video');
film?.addEventListener('play', () => {
  if (film.preload === 'none') { film.preload = 'metadata'; film.load(); }
}, { once: true });

window.addEventListener('scroll', onScroll, { passive: true });
window.addEventListener('resize', onScroll);
onScroll();
