/* Heartware — shared behaviour: nav, reveals, pipeline, compare bars. */

(function () {
  "use strict";

  /* ------------------------------------------------------------- mobile nav */
  const nav = document.querySelector(".nav");
  const toggle = nav && nav.querySelector(".nav__toggle");
  if (nav && toggle) {
    toggle.addEventListener("click", () => {
      const open = nav.dataset.open === "true";
      nav.dataset.open = open ? "false" : "true";
      toggle.setAttribute("aria-expanded", String(!open));
    });
    nav.querySelectorAll(".nav__links a").forEach((a) =>
      a.addEventListener("click", () => {
        nav.dataset.open = "false";
        toggle.setAttribute("aria-expanded", "false");
      })
    );
    document.addEventListener("keydown", (e) => {
      if (e.key === "Escape" && nav.dataset.open === "true") {
        nav.dataset.open = "false";
        toggle.setAttribute("aria-expanded", "false");
        toggle.focus();
      }
    });
  }

  /* ---------------------------------------------------------------- reveals */
  const revealables = document.querySelectorAll(".reveal, .compare");
  if ("IntersectionObserver" in window && revealables.length) {
    const io = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add("is-in");
            io.unobserve(entry.target);
          }
        });
      },
      { rootMargin: "-8% 0px -12% 0px", threshold: 0.08 }
    );
    revealables.forEach((el) => io.observe(el));
  } else {
    revealables.forEach((el) => el.classList.add("is-in"));
  }

  /* ------------------------------------------------------------------ tabs */
  document.querySelectorAll("[data-tabs]").forEach((group) => {
    const buttons = Array.from(group.querySelectorAll("[role='tab']"));
    const panels = buttons
      .map((b) => document.getElementById(b.getAttribute("aria-controls")))
      .filter(Boolean);

    const select = (index) => {
      buttons.forEach((b, i) => {
        const on = i === index;
        b.setAttribute("aria-selected", String(on));
        b.tabIndex = on ? 0 : -1;
      });
      panels.forEach((p, i) => {
        p.hidden = i !== index;
      });
    };

    buttons.forEach((b, i) => {
      b.addEventListener("click", () => select(i));
      b.addEventListener("keydown", (e) => {
        if (e.key === "ArrowRight") select((i + 1) % buttons.length);
        if (e.key === "ArrowLeft") select((i - 1 + buttons.length) % buttons.length);
      });
    });
    select(Math.max(0, buttons.findIndex((b) => b.getAttribute("aria-selected") === "true")));
  });

  /* -------------------------------------------------------------- counters */
  document.querySelectorAll("[data-count]").forEach((el) => {
    const target = parseFloat(el.dataset.count);
    const suffix = el.dataset.suffix || "";
    const decimals = (el.dataset.count.split(".")[1] || "").length;
    let done = false;

    const run = () => {
      if (done) return;
      done = true;
      const start = performance.now();
      const dur = 1100;
      const tick = (now) => {
        const p = Math.min(1, (now - start) / dur);
        const eased = 1 - Math.pow(1 - p, 3);
        el.textContent = (target * eased).toFixed(decimals) + suffix;
        if (p < 1) requestAnimationFrame(tick);
        else el.textContent = target.toFixed(decimals) + suffix;
      };
      requestAnimationFrame(tick);
    };

    if ("IntersectionObserver" in window) {
      const io = new IntersectionObserver(
        (entries) => entries.forEach((e) => e.isIntersecting && run()),
        { threshold: 0.4 }
      );
      io.observe(el);
    } else run();
  });

  /* --------------------------------------------------------- current page */
  const here = location.pathname.split("/").pop() || "index.html";
  document.querySelectorAll(".nav__links a").forEach((a) => {
    const target = a.getAttribute("href");
    if (target === here || (here === "" && target === "index.html")) {
      a.setAttribute("aria-current", "page");
    }
  });

  /* ------------------------------------------------------- year in footer */
  document.querySelectorAll("[data-year]").forEach((el) => {
    el.textContent = String(new Date().getFullYear());
  });
})();
