"""
Builds the pages from one shell.

    python tools/pages.py

The output is plain HTML in the repository root; there is no runtime build step.
"""

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

NAV = [
    ("product.html", "The insert"),
    ("technology.html", "How it works"),
    ("app.html", "The app"),
    ("evidence.html", "Evidence"),
    ("clinical.html", "In the clinic"),
    ("partnerships.html", "Work with us"),
    ("about.html", "About"),
]

# The mark is a heart with the trace of a heart sound running through it. One
# colour, no gradient, legible at 20 px.
LOGO = """<svg class="brand__mark" viewBox="0 0 48 44" aria-hidden="true" focusable="false"><path d="M24 41.4C21.7 39.6 3 27.6 3 15.1 3 8.3 8.2 3 14.7 3c4.3 0 7.8 2.1 9.3 5.3C25.5 5.1 29 3 33.3 3 39.8 3 45 8.3 45 15.1c0 12.5-18.7 24.5-21 26.3Z" fill="currentColor"/><path d="M11 20.6h6.2l2.7-7 4.1 13.6 2.9-6.6H37" fill="none" stroke="#fffdf7" stroke-width="3.1" stroke-linecap="round" stroke-linejoin="round"/></svg>"""


def head(title, description, page):
    nav_links = "\n".join(
        f'        <a href="{href}">{label}</a>' for href, label in NAV
    )
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} · Heartware</title>
<meta name="description" content="{description}">
<meta property="og:title" content="{title} · Heartware">
<meta property="og:description" content="{description}">
<meta property="og:type" content="website">
<link rel="icon" href="assets/img/logo-mark.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,400;12..96,600;12..96,800&family=Gabarito:wght@500;600;700&family=Archivo:wght@400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/css/site.css">
<script>document.documentElement.classList.add('js');</script>
</head>
<body data-page="{page}">
<svg width="0" height="0" aria-hidden="true" style="position:absolute">
  <clipPath id="heart-clip" clipPathUnits="objectBoundingBox">
    <path d="M.5 1C.48 .98 0 .68 0 .34 0 .14 .14 .02 .31 .02c.09 0 .16 .05 .19 .12C.53 .07 .6 .02 .69 .02c.17 0 .31 .12 .31 .32 0 .34-.48 .64-.5 .66Z"/>
  </clipPath>
</svg>
<header class="nav" data-open="false">
  <div class="nav__in">
    <a class="brand" href="index.html" aria-label="Heartware, home">
      {LOGO}
      <span class="brand__word">Heartware</span>
    </a>
    <button class="nav__toggle" aria-expanded="false">Menu</button>
    <nav class="nav__links" aria-label="Primary">
{nav_links}
        <a class="btn btn--sm" href="contact.html">Talk to us</a>
    </nav>
  </div>
</header>
<main>
"""


def foot():
    return f"""</main>

<footer class="foot">
  <div class="wrap">
    <div class="foot__top">
      <div>
        <a class="brand brand--big" href="index.html" aria-label="Heartware, home">
          {LOGO}
          <span class="brand__word">Heartware</span>
        </a>
        <p class="foot__line">A stethoscope insert that takes the chest wall out of the recording, so a heart sounds the same in every body.</p>
      </div>
      <nav class="foot__cols" aria-label="Footer">
        <div>
          <h4>The product</h4>
          <ul>
            <li><a href="product.html">The insert</a></li>
            <li><a href="technology.html">How it works</a></li>
            <li><a href="app.html">The app</a></li>
            <li><a href="evidence.html">Evidence</a></li>
          </ul>
        </div>
        <div>
          <h4>Who we talk to</h4>
          <ul>
            <li><a href="clinical.html">Clinicians</a></li>
            <li><a href="partnerships.html">Distributors</a></li>
            <li><a href="partnerships.html">Manufacturers</a></li>
            <li><a href="contact.html">Investors</a></li>
          </ul>
        </div>
        <div>
          <h4>Say hello</h4>
          <ul>
            <li><a href="mailto:hello@heart-ware.org">hello@heart-ware.org</a></li>
            <li><a href="contact.html">Book a pilot call</a></li>
            <li><a href="about.html">Boston, Massachusetts</a></li>
          </ul>
        </div>
      </nav>
    </div>
    <div class="foot__base">
      <span>© <span data-year>2026</span> Heartware</span>
      <span>A prototype. Not a medical device, and not for diagnosis.</span>
    </div>
  </div>
</footer>
<script src="assets/js/site.js" defer></script>
<script src="assets/js/demo.js" defer></script>
</body>
</html>
"""


def write(name, body, title, description, page):
    (ROOT / name).write_text(
        head(title, description, page) + body + foot(), encoding="utf-8"
    )
    print("wrote", name)
