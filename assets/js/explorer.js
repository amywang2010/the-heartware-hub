/* The thoracic correction, explorable.
 *
 * The point of this widget: the operator never tells the device how thick the
 * chest wall is. You pick a body, the device estimates the path from the
 * recording, and only then is the correction applied.
 *
 * The numbers come from the same model as research/thoracic_model.py, which is
 * in the repository. Nothing here is a patient recording.
 */

(function () {
  "use strict";

  const root = document.querySelector("[data-explorer]");
  if (!root) return;

  // raw / cor are the measured murmur levels for these three body thirds from
  // research/results.json, so the widget cannot drift from the figures.
  const BODIES = {
    slim: { label: "Athletic", mass: "62 kg", d: 14, bias: 0.9, raw: -9.31, cor: -8.34 },
    mid: { label: "Average", mass: "78 kg", d: 22, bias: 1.6, raw: -10.01, cor: -8.09 },
    broad: { label: "Broad", mass: "118 kg", d: 31, bias: 2.4, raw: -11.04, cor: -8.14 },
  };

  const FS = 8000;
  const state = {
    body: "mid",
    corrected: false,
    characterised: false,
    estimate: 0,
    quality: 0,
  };

  /* ---- the wall, ported from the research model ------------------------- */
  const attenuationDb = (f, d) => 0.55 * Math.pow(f / 100, 1.15) * (d / 10);
  const resonance = (f, d) => {
    const f0 = 155 * Math.sqrt(28 / d);
    const x = f / f0;
    return 1 / Math.sqrt(Math.pow(1 - x * x, 2) + Math.pow(x / 2.2, 2));
  };
  const transferDb = (f, d) =>
    20 * Math.log10(
      10 ** (-attenuationDb(f, d) / 20) * resonance(f, d) * 1.06
    );

  /* ---- synthetic envelope ---------------------------------------------- */
  const beats = [0.10, 0.95, 1.80, 2.65];
  const noise = Array.from({ length: 480 }, () => Math.random());

  function envelope(t, gain) {
    let v = 0.06 + noise[Math.floor(t * 160) % noise.length] * 0.05;
    for (const b of beats) {
      const s1 = Math.exp(-Math.pow((t - b) / 0.022, 2));
      const s2 = Math.exp(-Math.pow((t - (b + 0.30)) / 0.018, 2)) * 0.6;
      let murmur = 0;
      if (t > b + 0.045 && t < b + 0.28) {
        const w = Math.sin((Math.PI * (t - b - 0.045)) / 0.235);
        murmur =
          w *
          (0.55 + 0.45 * noise[Math.floor((t * 220) % noise.length)]) *
          0.72;
      }
      v += s1 * 1.0 + s2 + murmur;
    }
    return v * gain;
  }

  /* ---- canvas ----------------------------------------------------------- */
  const canvas = root.querySelector("canvas");
  const ctx = canvas.getContext("2d");
  let W = 0;
  let H = 0;

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

    const body = BODIES[state.body];
    // Amplitude ratio taken from the measured murmur levels, not from the raw
    // filter gain: the regularised inverse does not restore the full transfer.
    const wallGain = state.corrected
      ? 1
      : Math.pow(10, (body.raw - body.cor) / 20);
    const span = 3.0;

    // baseline
    ctx.strokeStyle = "rgba(255,255,255,0.10)";
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
    grad.addColorStop(0, state.corrected ? "rgba(255,84,112,0.45)" : "rgba(143,163,196,0.32)");
    grad.addColorStop(1, "rgba(12,22,38,0)");

    ctx.beginPath();
    ctx.moveTo(0, H);
    for (let x = 0; x <= W; x += 1.5) {
      const t = (x / W) * span;
      const v = Math.min(1.9, envelope(t, wallGain));
      const y = H - 14 - v * (H * 0.36);
      ctx.lineTo(x, y);
    }
    ctx.lineTo(W, H);
    ctx.closePath();
    ctx.fillStyle = grad;
    ctx.fill();

    ctx.beginPath();
    for (let x = 0; x <= W; x += 1.5) {
      const t = (x / W) * span;
      const v = Math.min(1.9, envelope(t, wallGain));
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
    const body = BODIES[state.body];

    root.querySelector("[data-body-label]").textContent = body.label;
    root.querySelector("[data-body-mass]").textContent = body.mass;

    const est = root.querySelector("[data-est]");
    est.textContent = state.characterised
      ? state.estimate.toFixed(0) + " mm"
      : "—";
    est.nextElementSibling.textContent = state.characterised
      ? "recovered from the recording"
      : "press characterise";

    const g = root.querySelector("[data-gain]");
    const level = state.corrected ? body.cor : body.raw;
    g.textContent = level.toFixed(2) + " dB";
    g.nextElementSibling.textContent = state.corrected
      ? "+" + (body.cor - body.raw).toFixed(1) + " dB · re S1/S2"
      : "as recorded · re S1/S2";

    const q = root.querySelector("[data-quality]");
    q.textContent = state.quality.toFixed(2);
    q.nextElementSibling.textContent =
      state.quality > 0.7 ? "good contact" : "check contact";

    root.querySelectorAll("[data-body]").forEach((b) => {
      b.setAttribute("aria-selected", String(b.dataset.body === state.body));
    });
    root.querySelectorAll("[data-mode]").forEach((b) => {
      b.setAttribute("aria-selected", String((b.dataset.mode === "corrected") === state.corrected));
    });

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

  root.querySelectorAll("[data-body]").forEach((btn) => {
    btn.addEventListener("click", () => {
      state.body = btn.dataset.body;
      reset();
    });
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
    const body = BODIES[state.body];
    btn.disabled = true;
    btn.textContent = "Listening to S1 and S2…";

    let n = 0;
    const tick = setInterval(() => {
      n += 1;
      draw();
      if (n > 8) {
        clearInterval(tick);
        state.characterised = true;
        state.estimate = body.d + body.bias;
        state.quality = 0.74 + Math.random() * 0.2;
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
