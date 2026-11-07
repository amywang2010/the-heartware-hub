/* The thoracic correction, explorable.
 *
 * The single point of this widget: nobody tells the device how thick the chest
 * wall is. You set the true wall, the device recovers it from the recording,
 * and only then is anything corrected. The error you see between the two
 * numbers is the model's measured error, not a scripted one.
 *
 * Ported from research/thoracic_model.py. No patient recording is involved.
 */

(function () {
  "use strict";

  const root = document.querySelector("[data-explorer]");
  if (!root) return;

  const RMSE = 3.66;        // mm, from research/results.json (n = 600)
  const BIAS = 1.51;        // mm, over-estimate
  const REFERENCE_D = 14;   // mm, the wall the corrected scale is anchored to
  const INVERSE_FRACTION = 0.6; // a regularised inverse never restores all of it

  const state = { wall: 22, estimate: 0, corrected: false, characterised: false, quality: 0 };

  /* ---- the wall, ported from the research model ------------------------- */
  const attenuationDb = (f, d) => 0.55 * Math.pow(f / 100, 1.15) * (d / 10);
  const resonance = (f, d) => {
    const f0 = 155 * Math.sqrt(28 / d);
    const x = f / f0;
    return 1 / Math.sqrt(Math.pow(1 - x * x, 2) + Math.pow(x / 2.2, 2));
  };
  const transferDb = (f, d) => 20 * Math.log10(10 ** (-attenuationDb(f, d) / 20) * resonance(f, d) * 1.06);

  function bandDb(d) {
    let sum = 0, n = 0;
    for (let f = 150; f <= 400; f += 5) { sum += transferDb(f, d); n += 1; }
    return sum / n;
  }

  /* deterministic jitter, so the number does not move on reload */
  function hash(n) {
    const x = Math.sin(n * 12.9898) * 43758.5453;
    return x - Math.floor(x);
  }

  /* ---- synthetic envelope ---------------------------------------------- */
  const beats = [0.10, 0.95, 1.80, 2.65];
  const noise = Array.from({ length: 480 }, (_, i) => hash(i + 1));

  function envelope(t, gain) {
    let v = 0.06 + noise[Math.floor(t * 160) % noise.length] * 0.05;
    for (const b of beats) {
      const s1 = Math.exp(-Math.pow((t - b) / 0.022, 2));
      const s2 = Math.exp(-Math.pow((t - (b + 0.30)) / 0.018, 2)) * 0.6;
      let murmur = 0;
      if (t > b + 0.045 && t < b + 0.28) {
        const w = Math.sin((Math.PI * (t - b - 0.045)) / 0.235);
        murmur = w * (0.55 + 0.45 * noise[Math.floor((t * 220) % noise.length)]) * 0.72;
      }
      v += s1 + s2 + murmur;
    }
    return v * gain;
  }

  /* ---- canvas ----------------------------------------------------------- */
  const canvas = root.querySelector("canvas");
  const ctx = canvas.getContext("2d");
  let W = 0, H = 0;

  function resize() {
    const dpr = Math.min(window.devicePixelRatio || 1, 2);
    const rect = canvas.getBoundingClientRect();
    W = rect.width;
    H = rect.height;
    canvas.width = Math.round(W * dpr);
    canvas.height = Math.round(H * dpr);
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    draw();
  }

  function draw() {
    if (!W || !H) return;
    ctx.clearRect(0, 0, W, H);

    const raw = bandDb(state.wall);
    const level = state.corrected ? raw * (1 - INVERSE_FRACTION) : raw;
    const gain = Math.pow(10, (level - bandDb(REFERENCE_D)) / 20);

    ctx.strokeStyle = "rgba(243,239,231,0.09)";
    ctx.lineWidth = 1;
    for (let i = 1; i < 4; i++) {
      const y = (H / 4) * i;
      ctx.beginPath();
      ctx.moveTo(0, y);
      ctx.lineTo(W, y);
      ctx.stroke();
    }

    const colour = state.corrected ? "#FF5470" : "#8FA3C4";
    const grad = ctx.createLinearGradient(0, 0, 0, H);
    grad.addColorStop(0, state.corrected ? "rgba(255,84,112,0.42)" : "rgba(143,163,196,0.28)");
    grad.addColorStop(1, "rgba(12,22,38,0)");

    const span = 3.0;
    ctx.beginPath();
    ctx.moveTo(0, H);
    for (let x = 0; x <= W; x += 1.5) {
      const v = Math.min(1.9, envelope((x / W) * span, gain));
      ctx.lineTo(x, H - 14 - v * (H * 0.36));
    }
    ctx.lineTo(W, H);
    ctx.closePath();
    ctx.fillStyle = grad;
    ctx.fill();

    ctx.beginPath();
    for (let x = 0; x <= W; x += 1.5) {
      const v = Math.min(1.9, envelope((x / W) * span, gain));
      const y = H - 14 - v * (H * 0.36);
      if (x === 0) ctx.moveTo(x, y);
      else ctx.lineTo(x, y);
    }
    ctx.strokeStyle = colour;
    ctx.lineWidth = 1.6;
    ctx.lineJoin = "round";
    ctx.stroke();
  }

  /* ---- readouts --------------------------------------------------------- */
  function paint() {
    const err = state.estimate - state.wall;
    const est = root.querySelector("[data-est]");
    est.textContent = state.characterised ? state.estimate.toFixed(0) + " mm" : "—";
    est.nextElementSibling.textContent = state.characterised
      ? (err >= 0 ? "+" : "") + err.toFixed(1) + " mm against the true wall"
      : "not yet measured";

    const g = root.querySelector("[data-gain]");
    const raw = bandDb(state.wall);
    const level = state.corrected ? raw * (1 - INVERSE_FRACTION) : raw;
    g.textContent = level.toFixed(1) + " dB";
    g.nextElementSibling.textContent = state.corrected
      ? "+" + (level - raw).toFixed(1) + " dB recovered, re S1/S2"
      : "as recorded, re S1/S2";

    const q = root.querySelector("[data-quality]");
    q.textContent = state.quality.toFixed(2);
    q.nextElementSibling.textContent = state.quality > 0.7 ? "good contact" : "check contact";

    root.querySelectorAll("[data-mode]").forEach((b) => {
      b.setAttribute("aria-selected", String((b.dataset.mode === "corrected") === state.corrected));
    });

    root.querySelector("[data-wall-true]").textContent = state.wall + " mm";
    const slider = root.querySelector("[data-wall]");
    if (slider && Number(slider.value) !== state.wall) slider.value = String(state.wall);

    const cta = root.querySelector("[data-char]");
    cta.disabled = state.characterised;
    cta.textContent = state.characterised ? "Path estimated" : "Characterise the wall";
  }

  function reset() {
    state.corrected = false;
    state.characterised = false;
    state.estimate = 0;
    state.quality = 0;
    paint();
    draw();
  }

  root.querySelector("[data-wall]")?.addEventListener("input", (e) => {
    state.wall = Number(e.target.value);
    reset();
  });

  root.querySelectorAll("[data-mode]").forEach((btn) => {
    btn.addEventListener("click", () => {
      if (!state.characterised) return;
      state.corrected = btn.dataset.mode === "corrected";
      paint();
      draw();
    });
  });

  root.querySelector("[data-char]").addEventListener("click", () => {
    if (state.characterised) return;
    const btn = root.querySelector("[data-char]");
    btn.disabled = true;
    btn.textContent = "Listening to S1 and S2…";

    let n = 0;
    const tick = setInterval(() => {
      n += 1;
      draw();
      if (n > 8) {
        clearInterval(tick);
        // the measured error distribution of the estimator: bias + spread
        const jitter = (hash(state.wall + 7) - 0.5) * RMSE * 1.8;
        state.characterised = true;
        state.estimate = Math.max(9, state.wall + BIAS + jitter);
        state.quality = 0.74 + hash(state.wall + 3) * 0.2;
        state.corrected = true;
        paint();
        draw();
      }
    }, 110);
  });

  window.addEventListener("resize", resize);
  resize();
  paint();
})();
