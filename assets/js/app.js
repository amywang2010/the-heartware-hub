/* The companion app, demonstrated.
 *
 * Every screen here is real interface: tabs, recording, the refusal state,
 * saved examinations, export. The readings are produced by the model in this
 * page from a chosen body, not from a patient — the card says so, and so does
 * the panel under it.
 */

(function () {
  "use strict";

  const root = document.querySelector("[data-app]");
  if (!root) return;

  const SITES = [
    { site: "Aortic area", band: "150–400 Hz", note: "0.21 s before S2" },
    { site: "Pulmonary area", band: "120–380 Hz", note: "0.19 s before S2" },
    { site: "Apex", band: "150–420 Hz", note: "0.24 s before S2" },
  ];

  const state = {
    tab: "record",
    recording: false,
    result: null,
    contact: "good",
    exams: [
      {
        id: "HW-0412",
        name: "Examination 0412",
        age: "2 days ago",
        site: "Aortic area",
        quality: 0.91,
        finding: "Systolic murmur, grade 2",
      },
      {
        id: "HW-0411",
        name: "Examination 0411",
        age: "2 days ago",
        site: "Apex",
        quality: 0.87,
        finding: "Systolic murmur, grade 1",
      },
      {
        id: "HW-0409",
        name: "Examination 0409",
        age: "6 days ago",
        site: "Lung fields",
        quality: 0.93,
        finding: "No significant finding",
      },
    ],
    open: null,
  };

  const $ = (sel) => root.querySelector(sel);

  function wave(el) {
    const c = el.tagName === "CANVAS" ? el : el.querySelector("canvas");
    if (!c) return;
    const ctx = c.getContext("2d");
    const dpr = Math.min(window.devicePixelRatio || 1, 2);
    const rect = c.getBoundingClientRect();
    c.width = rect.width * dpr;
    c.height = rect.height * dpr;
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    const W = rect.width;
    const H = rect.height;
    ctx.clearRect(0, 0, W, H);

    const beats = [0.06, 0.34, 0.62, 0.9];
    const noisy = state.contact === "loose";
    ctx.beginPath();
    for (let x = 0; x <= W; x++) {
      const t = x / W;
      let v = 0;
      for (const b of beats) {
        v += Math.exp(-Math.pow((t - b) / 0.008, 2));
        v += Math.exp(-Math.pow((t - b - 0.18) / 0.007, 2)) * 0.55;
        if (t > b + 0.03 && t < b + 0.17) {
          v +=
            0.32 *
            Math.sin((Math.PI * (t - b - 0.03)) / 0.14) *
            (0.5 + 0.5 * Math.sin(t * 900 + x));
        }
      }
      v += noisy ? (Math.random() - 0.5) * 0.85 : (Math.random() - 0.5) * 0.09;
      const y = H / 2 - v * (H * 0.42);
      if (x === 0) ctx.moveTo(x, y);
      else ctx.lineTo(x, y);
    }
    ctx.strokeStyle = state.recording ? "#FF5470" : "#7F94B5";
    ctx.lineWidth = 1.2;
    ctx.stroke();
  }

  function paintWave() {
    root.querySelectorAll("canvas[data-wave]").forEach(wave);
  }

  function render() {
    root.querySelectorAll("[data-panel]").forEach((p) => {
      p.hidden = p.dataset.panel !== state.tab;
    });
    root.querySelectorAll(".app-nav button").forEach((b) => {
      b.setAttribute("aria-selected", String(b.dataset.tab === state.tab));
    });

    $("#app-title").textContent =
      state.tab === "record"
        ? "New examination"
        : state.tab === "findings"
        ? "Findings"
        : state.tab === "records"
        ? "Saved examinations"
        : "Device";

    // record screen
    const res = $("#record-result");
    if (state.result) {
      res.hidden = false;
      $("#res-site").textContent = state.result.site;
      $("#res-band").textContent = state.result.band;
      $("#res-note").textContent = state.result.note;
      $("#res-quality").textContent = state.result.quality.toFixed(2);
      $("#res-title").textContent = state.result.title;
      $("#res-card").classList.toggle("is-refused", state.result.refused);
    } else {
      res.hidden = true;
    }

    $("#record-cta").textContent = state.recording
      ? "Listening…"
      : state.result
      ? "Record again"
      : "Record";
    $("#record-cta").disabled = state.recording;

    // findings
    const found = state.exams.filter((e) => !/^No significant/.test(e.finding));
    $("#findings-count").textContent = String(found.length);
    $("#findings-list").innerHTML = found.length
      ? found
          .map(
            (e) => `
        <div class="app-row">
          <div><b>${e.finding}</b><span>${e.site} · ${e.age}</span></div>
          <span class="app-chip ${e.quality > 0.9 ? "" : "app-chip--red"}">${e.quality.toFixed(2)}</span>
        </div>`
          )
          .join("")
      : `<div class="app-empty">No findings yet.</div>`;

    // records
    $("#records-list").innerHTML = state.exams
      .map(
        (e) => `
      <div class="app-row" data-record="${e.id}" role="button" tabindex="0">
        <div><b>${e.name}</b><span>${e.site} · ${e.age}</span></div>
        <span class="app-chip">${e.quality.toFixed(2)}</span>
      </div>`
      )
      .join("");

    $("#records-list")
      .querySelectorAll("[data-record]")
      .forEach((row) =>
        row.addEventListener("click", () => {
          state.open = state.exams.find((e) => e.id === row.dataset.record);
          render();
        })
      );

    const detail = $("#record-detail");
    if (state.open) {
      detail.hidden = false;
      $("#detail-title").textContent = state.open.name;
      $("#detail-site").textContent = state.open.site;
      $("#detail-finding").textContent = state.open.finding;
      $("#detail-quality").textContent = state.open.quality.toFixed(2);
    } else {
      detail.hidden = true;
    }

    paintWave();
  }

  root.querySelectorAll(".app-nav button").forEach((b) => {
    b.addEventListener("click", () => {
      state.tab = b.dataset.tab;
      render();
    });
  });

  $("#contact-toggle").addEventListener("click", () => {
    state.contact = state.contact === "good" ? "loose" : "good";
    $("#contact-toggle").textContent =
      state.contact === "good" ? "Good contact" : "Loose contact";
    $("#contact-toggle").setAttribute(
      "aria-pressed",
      String(state.contact === "loose")
    );
    if (state.result) {
      state.result = null;
      render();
    }
  });

  $("#record-cta").addEventListener("click", () => {
    if (state.recording) return;
    state.recording = true;
    state.result = null;
    render();

    let n = 0;
    const waveTimer = setInterval(() => {
      paintWave();
      n += 1;
      if (n > 14) clearInterval(waveTimer);
    }, 90);

    setTimeout(() => {
      clearInterval(waveTimer);
      state.recording = false;
      const site = SITES[Math.floor(Math.random() * SITES.length)];
      const loose = state.contact === "loose";
      state.result = loose
        ? {
            refused: true,
            title: "Signal too poor — record again",
            site: "—",
            band: "—",
            note: "contact lost",
            quality: 0.21,
          }
        : {
            refused: false,
            title: "Systolic murmur, grade 2",
            site: site.site,
            band: site.band,
            note: site.note,
            quality: 0.86 + Math.random() * 0.11,
          };
      render();
    }, 1450);
  });

  $("#save-exam").addEventListener("click", () => {
    if (!state.result || state.result.refused) return;
    const n = 413 + state.exams.length;
    state.exams.unshift({
      id: "HW-0" + n,
      name: "Examination 0" + n,
      age: "just now",
      site: state.result.site,
      quality: state.result.quality,
      finding: state.result.title,
    });
    state.result = null;
    state.tab = "records";
    render();
  });

  window.addEventListener("resize", paintWave);
  render();
})();
