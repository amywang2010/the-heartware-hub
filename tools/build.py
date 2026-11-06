"""
Builds the eight pages from one shell.

    python tools/build.py

The output is plain HTML in the repository root; there is no runtime build step.
Edit this file and re-run, or edit the HTML directly (it will be overwritten).
"""

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

NAV = [
    ("technology.html", "Technology"),
    ("product.html", "Product"),
    ("clinical.html", "Clinical impact"),
    ("evidence.html", "Evidence"),
    ("partnerships.html", "Partnerships"),
    ("about.html", "About"),
]


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
<link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,300..700;1,9..144,300..600&family=Instrument+Sans:wght@400;500;600&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/css/base.css">
<link rel="stylesheet" href="assets/css/pages.css">
<script>document.documentElement.classList.add('js');</script>
</head>
<body data-page="{page}">
<header class="nav" data-open="false">
  <div class="nav__inner">
    <a class="brand" href="index.html" aria-label="Heartware, home">
      <img src="assets/img/logo-mark.png" alt="" width="64" height="36">
      <span class="brand__word"><b>Heart</b>ware</span>
    </a>
    <button class="nav__toggle" aria-expanded="false" aria-label="Menu"><span></span></button>
    <nav class="nav__links" aria-label="Primary">
{nav_links}
        <a class="nav__cta" href="contact.html">Talk to us</a>
    </nav>
  </div>
</header>
<main>
"""


def foot():
    return """</main>
<footer class="footer">
  <div class="wrap">
    <div class="footer__grid">
      <div class="footer__brand">
        <img src="assets/img/logo-full.png" alt="Heartware" width="196" height="160">
        <p>A stethoscope insert that corrects for the chest wall, so every body gives the same heart and lung signal.</p>
      </div>
      <div>
        <h4>Product</h4>
        <ul>
          <li><a href="technology.html">Technology</a></li>
          <li><a href="product.html">The insert</a></li>
          <li><a href="product.html#specs">Specifications</a></li>
          <li><a href="evidence.html">Evidence</a></li>
        </ul>
      </div>
      <div>
        <h4>Company</h4>
        <ul>
          <li><a href="about.html">About</a></li>
          <li><a href="clinical.html">Clinical impact</a></li>
          <li><a href="partnerships.html">Partnerships</a></li>
          <li><a href="contact.html">Contact</a></li>
        </ul>
      </div>
      <div>
        <h4>Contact</h4>
        <ul>
          <li><a href="mailto:hello@heart-ware.org">hello@heart-ware.org</a></li>
          <li><a href="contact.html">Request a pilot</a></li>
          <li><a href="evidence.html#method">Method and code</a></li>
        </ul>
      </div>
    </div>
    <div class="footer__base">
      <span>© <span data-year>2026</span> Heartware. Prototype — not a medical device. Not for diagnostic use.</span>
      <span>Boston, Massachusetts</span>
    </div>
  </div>
</footer>
<script src="assets/js/site.js" defer></script>
<script src="assets/js/explorer.js" defer></script>
<script src="assets/js/app.js" defer></script>
</body>
</html>
"""


def write(name, body, title, description, page):
    (ROOT / name).write_text(
        head(title, description, page) + body + foot(), encoding="utf-8"
    )
    print("wrote", name)
