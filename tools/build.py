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
    ("partnerships.html", "Work with us"),
    ("about.html", "About"),
]

# The mark comes out of the supplied logo file, so the site uses the company's
# own drawing. The wordmark is set in type: Heart in wine, ware in navy, exactly
# as the logo has it.
MARK = (
    '<img class="brand__mark" src="assets/img/logo-mark.png" alt="" '
    'width="319" height="183" decoding="async">'
)
LOGO = MARK + '<span class="brand__word"><span class="brand__heart">Heart</span><span class="brand__rest">ware</span></span>'


def head(title, description, page):
    nav_links = "\n".join(
        f'      <a href="{href}">{label}</a>' for href, label in NAV
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
<link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wdth,wght@12..96,75..100,300..800&family=Bagel+Fat+One&family=Figtree:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/css/site.css">
<script>document.documentElement.classList.add('js');</script>
</head>
<body data-page="{page}">
<svg width="0" height="0" aria-hidden="true" style="position:absolute">
  <clipPath id="heart-clip" clipPathUnits="objectBoundingBox">
    <path d="M.5 .98C.47 .95 .02 .66 .02 .34 .02 .13 .16 .01 .33 .01c.08 0 .14 .05 .17 .11C.53 .06 .59 .01 .67 .01c.17 0 .31 .12 .31 .33 0 .32-.45 .61-.48 .64Z"/>
  </clipPath>
</svg>
<header class="nav" data-open="false">
  <div class="wrap nav__in">
    <a class="brand" href="index.html" aria-label="Heartware, home">
      {LOGO}
    </a>
    <button class="nav__toggle" aria-expanded="false">Menu</button>
    <nav class="nav__links" aria-label="Primary">
{nav_links}
      <a class="btn btn--wine btn--sm" href="contact.html">Talk to us</a>
    </nav>
  </div>
</header>
<main>
"""


def foot():
    return f"""
</main>
<footer class="foot">
  <div class="blob" style="width:34rem;height:34rem;right:-12rem;top:-14rem;background:rgba(151,26,44,.32)"></div>
  <div class="dots" style="color:rgba(251,246,236,.22);inset:auto 0 0 0;height:8rem"></div>
  <div class="wrap">
    <div class="foot__top">
      <div>
        <p class="foot__mega"><em>Heart</em>ware</p>
        <p class="foot__tag">Innovating cardiac care</p>
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
