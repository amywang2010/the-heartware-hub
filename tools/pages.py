"""Page content. Run tools/pages.py to write the HTML."""

from pathlib import Path

from build import foot, head

ROOT = Path(__file__).resolve().parent.parent


def page(name, title, desc, key, body):
    (ROOT / name).write_text(head(title, desc, key) + body + foot(), encoding="utf-8")
    print("wrote", name)


INK = "#0e2233"
NAVY = "#114471"
NAVY_D = "#0b2f50"
WINE = "#971a2c"
BUTTER = "#f7dda2"
BLUSH = "#f5cfc7"
SAGE = "#cfe0cd"
SKY = "#c9dff0"
LILAC = "#ded5f2"
PAPER = "#fbf6ec"
PAPER2 = "#f2e9db"

TXT = f'font-family="Figtree,Arial,sans-serif"'


def fig_side():
    """Flat side elevation with the two dimensions that matter."""
    return f"""
<svg viewBox="0 0 520 430" role="img" aria-label="Side elevation of the insert: 38.9 millimetre collar, 17.2 millimetre body, gasket at the face">
  <g stroke="{INK}" stroke-width="3" stroke-linejoin="round">
    <rect x="96" y="74" width="328" height="26" rx="13" fill="{NAVY_D}"/>
    <rect x="132" y="100" width="256" height="196" rx="22" fill="{NAVY}"/>
    <rect x="150" y="296" width="220" height="46" rx="10" fill="{WINE}"/>
    <rect x="164" y="342" width="192" height="16" rx="8" fill="{BUTTER}"/>
  </g>
  <g stroke="rgba(251,246,236,.35)" stroke-width="3" stroke-linecap="round">
    <path d="M176 130v136M232 130v136M288 130v136M344 130v136"/>
  </g>
  <g stroke="rgba(251,246,236,.55)" stroke-width="2" stroke-linecap="round">
    <path d="M154 302v34M172 302v34M190 302v34M208 302v34M226 302v34M244 302v34M262 302v34M280 302v34M298 302v34M316 302v34M334 302v34M352 302v34"/>
  </g>
  <g stroke="{WINE}" stroke-width="2.5" fill="none">
    <path d="M74 100h-16M74 342h-16M74 100v242M74 100l-7 9M74 100l7 9M74 342l-7 -9M74 342l7 -9"/>
    <path d="M132 56v-18M388 56v-18M132 38h256M132 38l9 -7M132 38l9 7M388 38l-9 -7M388 38l-9 7"/>
  </g>
  <g fill="{WINE}" {TXT} font-size="15" font-weight="700">
    <text x="26" y="228" transform="rotate(-90 26 228)" text-anchor="middle">17.2 mm</text>
    <text x="260" y="26" text-anchor="middle">38.9 mm collar</text>
  </g>
  <g {TXT} font-size="14" font-weight="600" fill="{INK}">
    <text x="426" y="96">body</text>
    <text x="426" y="114" fill="rgba(14,34,51,.62)">PA12, 45 g</text>
    <text x="426" y="290">collar</text>
    <text x="426" y="308" fill="rgba(14,34,51,.62)">M40 x 0.75</text>
    <text x="426" y="352">gasket</text>
    <text x="426" y="370" fill="rgba(14,34,51,.62)">60 Shore A</text>
  </g>
  <g stroke="rgba(14,34,51,.35)" stroke-width="2" stroke-dasharray="5 5">
    <path d="M388 90h32M404 284h16M356 350h64"/>
  </g>
</svg>
"""


def fig_cut():
    """Section: what is inside, and where the sound goes."""
    return f"""
<svg viewBox="0 0 660 430" role="img" aria-label="Section through Rev D: outer housing, cavity, microphone board at the base, sealing gasket and threaded collar">
  <g stroke="{INK}" stroke-width="3" stroke-linejoin="round">
    <path d="M158 96h344v244H158z" fill="{NAVY}"/>
    <path d="M188 126h284v150H188z" fill="{PAPER}"/>
    <rect x="210" y="222" width="240" height="34" rx="8" fill="{WINE}"/>
    <circle cx="268" cy="239" r="9" fill="{BUTTER}"/>
    <circle cx="392" cy="239" r="9" fill="{BUTTER}"/>
    <rect x="158" y="340" width="344" height="38" rx="8" fill="{WINE}"/>
    <rect x="176" y="378" width="308" height="14" rx="7" fill="{BUTTER}"/>
  </g>
  <g stroke="{WINE}" stroke-width="3" stroke-linecap="round" fill="none" opacity=".85">
    <path d="M330 372v-38"/><path d="M330 334l-9 11M330 334l9 11"/>
    <path d="M250 372v-72"/><path d="M250 300l-8 10M250 300l8 10"/>
    <path d="M410 372v-72"/><path d="M410 300l-8 10M410 300l8 10"/>
  </g>
  <g stroke="rgba(251,246,236,.4)" stroke-width="2" stroke-dasharray="8 7">
    <path d="M188 170h284"/>
  </g>
  <g {TXT} font-size="14" font-weight="600" fill="{INK}">
    <text x="146" y="74">housing</text>
    <text x="146" y="208" text-anchor="end">cavity</text>
    <text x="470" y="244">mic board</text>
    <text x="146" y="366" text-anchor="end">collar</text>
    <text x="470" y="392">gasket</text>
  </g>
  <g stroke="rgba(14,34,51,.35)" stroke-width="2" stroke-dasharray="5 5">
    <path d="M206 70l44 26M318 204l54 20M448 240h16M250 362l-56 4M470 386l-58 -2"/>
  </g>
  <text x="330" y="418" text-anchor="middle" {TXT} font-size="13" fill="rgba(14,34,51,.6)">sound enters at the face, the board records it, the collar holds the head</text>
</svg>
"""


def fig_head():
    """The insert in a head, with the parts it leaves alone."""
    return f"""
<svg viewBox="0 0 560 440" role="img" aria-label="The insert threaded into a stethoscope head, with the diaphragm, stem and tube unchanged">
  <g stroke="{INK}" stroke-width="3" stroke-linejoin="round">
    <ellipse cx="230" cy="238" rx="146" ry="96" fill="{NAVY}"/>
    <ellipse cx="230" cy="300" rx="146" ry="30" fill="{BLUSH}"/>
    <path d="M204 300h52v34a26 26 0 0 1-52 0z" fill="{NAVY_D}"/>
    <rect x="212" y="126" width="36" height="58" rx="8" fill="{WINE}"/>
    <rect x="196" y="96" width="68" height="34" rx="8" fill="{NAVY_D}"/>
    <rect x="352" y="214" width="104" height="30" rx="15" fill="{NAVY_D}"/>
  </g>
  <path d="M456 244c58 0 62-58 30-78" fill="none" stroke="{WINE}" stroke-width="20" stroke-linecap="round"/>
  <g stroke="rgba(251,246,236,.45)" stroke-width="2">
    <path d="M118 262h224M230 190v144"/>
  </g>
  <g {TXT} font-size="14" font-weight="600" fill="{INK}">
    <text x="196" y="70">insert, threaded by hand</text>
    <text x="196" y="88" fill="rgba(14,34,51,.62)">5 minutes, no tool</text>
    <text x="392" y="372">head, stem and tube</text>
    <text x="392" y="390" fill="rgba(14,34,51,.62)">unchanged</text>
    <text x="96" y="344" fill="rgba(14,34,51,.62)">diaphragm plane</text>
  </g>
  <g stroke="rgba(14,34,51,.35)" stroke-width="2" stroke-dasharray="5 5">
    <path d="M198 74l14 26M394 366l-42 -30M96 336l40 6"/>
  </g>
</svg>
"""


def ring():
    """The circle of text that turns around the hero panel."""
    return f"""
<div class="hero__ring" aria-hidden="true">
  <svg viewBox="0 0 120 120">
    <defs><path id="ringpath" d="M60,60 m-46,0 a46,46 0 1,1 92,0 a46,46 0 1,1 -92,0"/></defs>
    <text><textPath href="#ringpath">45 GRAMS · REV D · NO ADAPTER · 5 MINUTES · </textPath></text>
  </svg>
</div>
"""


def ticker():
    bit = (
        '<span>45 grams</span><b>&hearts;</b><span>44, 46 and 48 mm heads</span><b>&hearts;</b>'
        '<span>$38.25 a unit</span><b>&hearts;</b><span>no capital equipment</span><b>&hearts;</b>'
        '<span>five minutes to fit</span><b>&hearts;</b><span>not a medical device</span><b>&hearts;</b>'
    )
    return f'<div class="ticker" aria-hidden="true"><div class="ticker__in">{bit}{bit}</div></div>'


def wave(fill, bg, flip=False):
    """A torn edge between two colour fields, so bands do not meet in a line."""
    cls = "wave wave--flip" if flip else "wave"
    return (
        f'<div class="{cls}" style="background:{bg}" aria-hidden="true">'
        '<svg viewBox="0 0 1440 90" preserveAspectRatio="none">'
        f'<path fill="{fill}" d="M0,38 C210,82 380,6 640,24 C880,40 1030,86 1240,66 C1320,58 1380,38 1440,30 L1440,90 L0,90 Z"/>'
        "</svg></div>"
    )


def heart_outline(color="rgba(248,241,228,.2)"):
    return (
        '<svg class="heartout" viewBox="0 0 100 92" aria-hidden="true">'
        '<path d="M50 88C47 85 2 60 2 31 2 12 16 2 33 2c8 0 14 5 17 10C53 7 59 2 67 2c17 0 31 10 31 29 0 29-45 54-48 57Z" '
        f'fill="none" stroke="{color}" stroke-width="1.6"/></svg>'
    )


def demo_block():
    """The phone demo. demo.js runs it on its own; the button restarts it."""
    return f"""
<div class="demo" data-demo>
  <div class="phone">
    <div class="screen">
      <div class="screen__top"><span>Heartware</span><span>Rev D</span></div>
      <div class="screen__pat">Bed 4 &middot; M, 68</div>
      <div class="screen__meta">Aortic area, seated, 6 s</div>
      <div class="screen__state"><i></i><span data-demo-state>Listening</span></div>
      <div class="screen__big" data-demo-big>6.0<small>s</small></div>
      <canvas class="screen__wave" data-demo-wave width="560" height="150" aria-label="Waveform of the recorded heart sound"></canvas>
      <div class="screen__gate">
        <span>Chest wall <b data-demo-wall>37 mm</b> &middot; contact <b data-demo-q>89%</b></span>
        <span class="screen__bar"><b data-demo-bar></b></span>
      </div>
      <div class="screen__verdict" data-demo-verdict data-tone="ok">Contact is good. Holding the take.</div>
      <button class="screen__btn" data-demo-run>Run it again</button>
    </div>
  </div>
  <div>
    <ol class="demo__list">
      <li class="on" data-demo-step><b>01</b><span>Six seconds, one channel, 20 Hz to 2 kHz. The waveform is drawn as it arrives.</span></li>
      <li data-demo-step><b>02</b><span>The chest wall is estimated from the recording. No tape measure, no input from the person holding it.</span></li>
      <li data-demo-step><b>03</b><span>The murmur band is divided by the wall it just measured, so the number that remains is the heart's.</span></li>
      <li data-demo-step><b>04</b><span>Contact below 45 per cent returns nothing. The take is refused, not guessed at.</span></li>
    </ol>
    <p class="small" style="margin-top:1.2rem;max-width:42ch">A generated grade 2 murmur through a modelled chest wall, played in the browser. It shows the interface and runs itself. It does not measure you.</p>
  </div>
</div>
"""


HOME = f"""
<section class="hero">
  <div class="ghostword" style="right:-1.5rem;bottom:-2.5rem">heart</div>
  <div class="dots" style="color:#a9c8dd;width:18rem;height:11rem;right:2rem;top:1.4rem;opacity:.35"></div>
  <svg class="audiowave" viewBox="0 0 1440 160" preserveAspectRatio="none" aria-hidden="true"><path d="M0 120 C 90 120 90 40 180 40 S 270 120 360 120 S 450 40 540 40 S 630 120 720 120 S 810 40 900 40 S 990 120 1080 120 S 1170 40 1260 40 S 1350 120 1440 120" fill="none" stroke="#f7dda2" stroke-width="2"/></svg>
  <div class="blob" style="width:32rem;height:32rem;left:-13rem;top:-12rem;background:rgba(247,221,162,.12)"></div>
  <div class="wrap">
    <div class="hero__type">
      <p class="tag tag--wine"><i></i>Rev D &middot; stethoscope insert</p>
      <h1 class="poster">The heart sounds the same. <span class="hl">The chest is what changes.</span></h1>
    </div>
    <div class="hero__grid">
      <div class="hero__copy">
        <p class="lede">A 45 gram insert drops into the stethoscope already in the room, works out the chest wall from the recording, and takes it out of the signal. Two people with the same murmur sit 1.73 dB apart. After correction, 0.25 dB.</p>
        <div class="cta__row">
          <a class="btn btn--wine" href="evidence.html">See the evidence <span class="btn__arrow">&rarr;</span></a>
          <a class="btn btn--butter" href="contact.html">Book a pilot call</a>
        </div>
        <p class="tiny" style="margin-top:1.1rem;color:rgba(248,241,228,.62)">Fits the head you already own. No adapter and no second device.</p>
      </div>
      <div class="hero__art">
        <div class="artcard">{fig_head()}</div>
        {ring()}
        <div class="sticker" style="right:-1.4rem;top:-1.5rem;transform:rotate(7deg)">$38.25<small>a unit</small></div>
      </div>
    </div>
    <div class="hero__stats">
      <div><b>45 g</b><span>assembled</span></div>
      <div><b>38.9 mm</b><span>collar</span></div>
      <div><b>44 / 46 / 48</b><span>millimetre heads</span></div>
      <div><b>5 min</b><span>by hand, reversible</span></div>
    </div>
  </div>
</section>

{wave(PAPER, NAVY)}

{ticker()}

<section class="sec">
  <div class="wrap">
    <div class="split split--57" style="align-items:end;margin-bottom:clamp(2rem,4vw,3.2rem)">
      <h2 class="h2">Three numbers, no adjectives.</h2>
      <p class="small" style="justify-self:end;max-width:34ch">Bench and simulation. The size of each set sits on the evidence page, next to the number it belongs to.</p>
    </div>
    <div class="figures">
      <div class="figure figure--plain">
        <span class="figure__n">3.7<small>mm</small></span>
        <h3>Chest wall, recovered from the recording alone.</h3>
        <p class="small">RMS error against the measured wall, across the bench set. No second device, no tape measure, no input from the person holding the stethoscope.</p>
      </div>
      <div class="figure figure--rise">
        <span class="figure__n">1.73<small>dB</small></span>
        <h3>The distance between two bodies.</h3>
        <p class="small">The same murmur through a 60 kg chest and a 120 kg one. One division takes it to 0.25 dB.</p>
      </div>
      <div class="figure figure--drop">
        <span class="figure__n">45<small>%</small></span>
        <h3>Contact gate.</h3>
        <p class="small">Below it the app returns nothing, rather than a number it cannot stand behind.</p>
      </div>
    </div>
  </div>
</section>

<section class="sec" style="padding-top:0">
  <div class="wrap split split--57 split--top">
    <div class="statement">
      <h2 class="h2">It measures the chest wall, then divides it back out.</h2>
      <p class="lede">The chest behaves like a low pass filter whose resonance falls as the wall thickens. The insert measures that from the take itself and removes it in the same pass, so there is no second device and no calibration step.</p>
      <div class="cta__row">
        <a class="btn btn--ink" href="technology.html">How the arithmetic works <span class="btn__arrow">&rarr;</span></a>
      </div>
    </div>
    <div class="artcard" style="background:{SAGE};transform:rotate(-1.6deg);box-shadow:12px 12px 0 rgba(16,42,58,.22)">{fig_cut()}</div>
  </div>
</section>

{wave(WINE, PAPER)}

<section class="band band--wine sec">
  <div class="ghostword" style="left:-2rem;bottom:-3.5rem;-webkit-text-stroke-color:rgba(248,241,228,.14)">same</div>
  <div class="wrap split split--57">
    <div>
      <h2 class="display" style="max-width:15ch">One patient is loud. One is quiet. <span class="hl">Neither is more diseased.</span></h2>
      <p class="on-dark" style="margin-top:1.2rem;max-width:42ch">A grade 2 murmur reaches the earpieces 1.73 dB apart in a 60 kg body and a 120 kg one, a third of the band a clinician listens in. The correction closes it to a quarter of a decibel.</p>
    </div>
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:1.2rem">
      <div class="heartbox"><div><p class="heartbox__n">1.73 dB</p><p class="heartbox__l">apart, uncorrected</p></div></div>
      <div class="heartbox" style="background:{BUTTER}"><div><p class="heartbox__n">0.25 dB</p><p class="heartbox__l">apart, corrected</p></div></div>
    </div>
  </div>
</section>

{wave(SKY, WINE)}

<section class="band band--sky sec">
  <div class="ghostword ghostword--ink" style="right:-1rem;top:-1rem">app</div>
  <div class="wrap">
    <div class="split split--57" style="align-items:end;margin-bottom:clamp(1.8rem,3vw,2.6rem)">
      <h2 class="display" style="max-width:15ch">This is the app, running. It needs nothing from you.</h2>
      <p class="small" style="justify-self:end;max-width:32ch">Record, measure, correct, keep or refuse. It plays a generated murmur, so the interface can be judged without a device in your hand.</p>
    </div>
    {demo_block()}
  </div>
</section>

{wave(PAPER, SKY)}
{wave(BUTTER, PAPER)}

<section class="band band--butter sec">
  <div class="tri" style="width:20rem;height:18rem;right:-5rem;bottom:-6rem;background:rgba(151,26,44,.14)"></div>
  <div class="wrap price">
    <div>
      <p class="tag tag--wine" style="transform:rotate(-3deg)">Price</p>
      <p class="price__n" style="margin-top:1.2rem">$38.25<small>Per unit, app included. No capital equipment, no consumable, no fee per exam. Materials and machining come in under that.</small></p>
    </div>
    <div>
      <p class="small" style="margin-bottom:1rem">Next to what a clinic already buys. List price, February 2026.</p>
      <ul class="pricelist">
        <li class="us"><span>Heartware insert <span class="tiny">fits the head you own</span></span><b>$38.25</b></li>
        <li><span>Eko CORE 300 <span class="tiny">digital stethoscope</span></span><b>$199</b></li>
        <li><span>3M Littmann CORE <span class="tiny">digital stethoscope</span></span><b>$379</b></li>
        <li><span>Littmann 3200 <span class="tiny">digital stethoscope</span></span><b>$449</b></li>
      </ul>
    </div>
  </div>
</section>

{wave(PAPER, BUTTER)}

<section class="sec">
  <div class="wrap">
    <div class="cta">
      {heart_outline()}
      <div class="ghostword" style="right:-2rem;bottom:-4rem;-webkit-text-stroke-color:rgba(248,241,228,.1)">go</div>
      <h2>Run a pilot, sell it, or build it into a head.</h2>
      <p class="on-dark" style="margin-top:1.2rem;max-width:38ch">Three ways in, each a small first step. Every one starts with a sentence and an email address.</p>
      <div class="cta__row">
        <a class="btn btn--butter" href="partnerships.html">How we work with partners <span class="btn__arrow">&rarr;</span></a>
        <a class="btn btn--ghost" href="contact.html">hello@heart-ware.org</a>
      </div>
    </div>
  </div>
</section>
"""


PRODUCT = f"""
<section class="ptop sec--tight" style="position:relative;overflow:hidden">
  <div class="blob" style="width:22rem;height:22rem;right:-7rem;top:-8rem;background:{BLUSH};opacity:.65"></div>
  <div class="wrap split split--57">
    <div>
      <span class="chip chip--wine"><i></i>Rev D &middot; 38.9 mm collar &middot; 45 g</span>
      <h1 class="mega" style="margin-top:1rem">The insert.</h1>
      <p class="lede" style="margin-top:1rem">It replaces the back plate of the head, so the diaphragm, stem and tube stay as they are. Three printed revisions, fitted by hand to 44, 46 and 48 mm heads. It has not been tooled.</p>
      <div class="cta__row" style="margin-top:1.4rem">
        <a class="btn btn--wine" href="evidence.html">What it has been measured on</a>
        <a class="btn" href="contact.html">Ask for the drawings</a>
      </div>
    </div>
    <div class="artcard" style="transform:rotate(1.6deg)">{fig_side()}</div>
  </div>
</section>

<section class="sec" style="padding-top:0">
  <div class="wrap mosaic">
    <div class="card card--butter m4">
      <span class="card__k">Mass</span>
      <p class="card__n">45 g</p>
      <p class="small" style="margin-top:.5rem">Assembled, board and gasket included. Lighter than the head it screws into, so it does not move the centre of gravity enough to notice.</p>
    </div>
    <div class="card card--sage m4">
      <span class="card__k">Fit</span>
      <p class="card__n">44 / 46 / 48</p>
      <p class="small" style="margin-top:.5rem">Millimetre heads, single and double, tested on 11 models across three manufacturers. The list ships with the units.</p>
    </div>
    <div class="card card--lilac m4">
      <span class="card__k">Install</span>
      <p class="card__n">5 min</p>
      <p class="small" style="margin-top:.5rem">Threaded by hand at the sink. No tool, no adhesive, nothing drilled, and it comes back off the same way.</p>
    </div>
  </div>
</section>

<section class="sec" style="background:{SKY}">
  <div class="wrap split split--57 split--top">
    <div>
      <h2 class="display">Everything measurable, in four drawers.</h2>
      <p class="lede" style="margin-top:1rem">Open one for the numbers behind it. Where a figure is bench measured it says so; where it is a design value it says that instead.</p>
    </div>
    <div class="acc">
      <details open>
        <summary>Dimensions<span>38.9 mm collar</span></summary>
        <div class="acc__in">
          <div class="rows">
            <div class="row"><span class="row__k">Collar</span><span class="row__v">38.9 mm, threaded M40 &times; 0.75, 4.5 mm engagement.</span></div>
            <div class="row"><span class="row__k">Height</span><span class="row__v">17.2 mm below the back plate, 11.4 mm above it.</span></div>
            <div class="row"><span class="row__k">Mass</span><span class="row__v">45 g assembled, board and gasket included.</span></div>
            <div class="row"><span class="row__k">Clearance</span><span class="row__v">Diaphragm plane unchanged, so the acoustic load on the skin stays the head's own.</span></div>
          </div>
        </div>
      </details>
      <details>
        <summary>Materials and finish<span>printed, then machined</span></summary>
        <div class="acc__in">
          <div class="rows">
            <div class="row"><span class="row__k">Housing</span><span class="row__v">PA12, laser sintered. Collar in anodised aluminium, graphite.</span></div>
            <div class="row"><span class="row__k">Sealing</span><span class="row__v">Silicone face gasket, 60 Shore A, plus an O-ring groove at the collar.</span></div>
            <div class="row"><span class="row__k">Ingress</span><span class="row__v">IPX4 once closed, bench tested on three assemblies.</span></div>
            <div class="row"><span class="row__k">Cleaning</span><span class="row__v">Alcohol wipes on the outer surfaces. Not autoclavable.</span></div>
          </div>
        </div>
      </details>
      <details>
        <summary>Electronics<span>one channel, one board</span></summary>
        <div class="acc__in">
          <div class="rows">
            <div class="row"><span class="row__k">Channel</span><span class="row__v">One, 20 Hz to 2 kHz, 48 kHz sample rate, 16 bit.</span></div>
            <div class="row"><span class="row__k">Microphones</span><span class="row__v">Reference capsule plus the signal capsule. The difference is what carries the wall estimate.</span></div>
            <div class="row"><span class="row__k">Battery</span><span class="row__v">70 mAh, a week of clinic use, charged over USB-C.</span></div>
            <div class="row"><span class="row__k">Storage</span><span class="row__v">On the phone, not on the insert. Nothing leaves the room unless someone exports it.</span></div>
          </div>
        </div>
      </details>
      <details>
        <summary>Regulatory status<span>prototype</span></summary>
        <div class="acc__in">
          <div class="rows">
            <div class="row"><span class="row__k">Status</span><span class="row__v">Prototype. Not a medical device, not cleared, not for diagnosis.</span></div>
            <div class="row"><span class="row__k">Evidence</span><span class="row__v">Simulation and bench, on 111 recordings. No patient data yet.</span></div>
            <div class="row"><span class="row__k">Next</span><span class="row__v">A pilot with 20 to 40 echo-booked patients, at a site that wants the answer either way.</span></div>
          </div>
        </div>
      </details>
    </div>
  </div>
</section>
"""


TECH = f"""
<section class="ptop sec--tight" style="position:relative;overflow:hidden">
  <div class="blob" style="width:24rem;height:24rem;left:-8rem;top:-9rem;background:{SKY};opacity:.8"></div>
  <div class="wrap">
    <span class="chip chip--butter"><i></i>How it works</span>
    <h1 class="mega" style="margin-top:1rem;max-width:20ch">Two microphones, one division.</h1>
    <p class="lede" style="margin-top:1rem">The chest wall is a filter sitting between the heart and every microphone you can put on the skin. The insert does not try to model the filter in advance. It measures it from the take, and divides by it.</p>
  </div>
</section>

<section class="sec--tight">
  <div class="wrap split split--57 split--top">
    <div class="card card--butter">
      <span class="card__k">The whole method</span>
      <p class="formula" style="font-family:var(--disp);font-weight:800;letter-spacing:-.04em;font-size:clamp(2.1rem,4.4vw,3.3rem);line-height:1.05;margin-top:.6rem">H&#770;(f) = H(f) / T(f, d&#770;)</p>
      <p class="small" style="margin-top:1rem">H(f) is what the capsules recorded, T is the transmission of the wall, and d&#770; is the wall thickness estimated from the same take. Nothing else is fitted, and nothing is applied that a reviewer cannot read.</p>
    </div>
    <div class="artcard" style="background:{SAGE};transform:rotate(-1.4deg);box-shadow:12px 12px 0 rgba(16,42,58,.22)">{fig_cut()}</div>
  </div>
</section>

<section class="sec" style="background:{SKY}">
  <div class="wrap">
    <h2 class="display" style="max-width:20ch">What happens in the six seconds.</h2>
    <div class="steps" style="margin-top:1.6rem">
      <div class="step rise"><span class="step__n">1</span><h3>Listen</h3><p>One channel, 20 Hz to 2 kHz. The reference capsule sits behind the face gasket and hears the room.</p></div>
      <div class="step rise"><span class="step__n">2</span><h3>Measure</h3><p>The low frequency slope of the take gives the wall. 3.7 mm RMS, against a measured wall, on 111 recordings.</p></div>
      <div class="step rise"><span class="step__n">3</span><h3>Divide</h3><p>The murmur band is corrected by the estimated transmission. It is a division, not a model.</p></div>
      <div class="step rise"><span class="step__n">4</span><h3>Decide</h3><p>Contact above 45 per cent keeps the take. Below it, the app says so and offers nothing.</p></div>
    </div>
  </div>
</section>

<section class="sec" style="background:{NAVY};color:{PAPER};position:relative;overflow:hidden">
  <div class="blob" style="width:26rem;height:26rem;right:-9rem;bottom:-11rem;background:rgba(201,223,240,.14)"></div>
  <div class="wrap split split--57 split--top">
    <div>
      <h2 class="display" style="max-width:16ch">You can check it in an afternoon.</h2>
      <p class="on-dark" style="margin-top:1rem;max-width:42ch">None of this asks to be taken on trust. The bench recordings, the estimator and the spreadsheet behind every number on this site are available to anyone who asks, under an NDA if the CAD comes too.</p>
    </div>
    <div class="acc">
      <details open>
        <summary>Reproduce the spread<span>two recordings</span></summary>
        <div class="acc__in"><p class="small on-dark">Take the two bench recordings of the same synthetic murmur through 60 mm and 110 mm walls. Measure the murmur band level in each. That difference is the 1.73 dB. Apply the correction. That is the 0.25 dB.</p></div>
      </details>
      <details>
        <summary>Check the estimator<span>111 recordings</span></summary>
        <div class="acc__in"><p class="small on-dark">The wall estimate is a slope fit over 20 to 120 Hz. It has no trained weights and no lookup table: given the same recording it returns the same number, and the residual against the measured wall is 3.7 mm RMS.</p></div>
      </details>
      <details>
        <summary>Break it<span>a wall that is not there</span></summary>
        <div class="acc__in"><p class="small on-dark">Hold the insert off the skin. The estimator should return a wall of near zero and the gate should refuse the take. If it returns a confident number instead, the method is wrong and you should say so.</p></div>
      </details>
    </div>
  </div>
</section>
"""


APP = f"""
<section class="ptop sec--tight" style="position:relative;overflow:hidden">
  <div class="blob" style="width:20rem;height:20rem;right:-6rem;top:-8rem;background:{LILAC};opacity:.7"></div>
  <div class="wrap">
    <span class="chip chip--sky"><i></i>Companion app</span>
    <h1 class="mega" style="margin-top:1rem;max-width:16ch">The screen the insert talks to.</h1>
    <p class="lede" style="margin-top:1rem">One recording screen, one result, and a refusal when the take is not worth keeping. No account, no dashboard, no model of you.</p>
  </div>
</section>

<section class="sec--tight">
  <div class="wrap">{demo_block()}</div>
</section>

<section class="sec" style="background:{PAPER2}">
  <div class="wrap mosaic">
    <div class="card card--sky m4"><span class="card__k">Offline</span><p class="card__n">0</p><h3 style="margin-top:.6rem">Bytes sent.</h3><p class="small">The take stays on the phone. Export is a file someone chooses to send, not a sync that happens anyway.</p></div>
    <div class="card card--butter m4"><span class="card__k">Refusal</span><p class="card__n">45%</p><h3 style="margin-top:.6rem">Contact gate.</h3><p class="small">Poor contact, loose gasket, a coat over the chest: the app returns nothing rather than a number it cannot defend.</p></div>
    <div class="card card--sage m4"><span class="card__k">Weight</span><p class="card__n">1</p><h3 style="margin-top:.6rem">Number per take.</h3><p class="small">The corrected murmur level, the wall estimate and the quality score. Not a grade, not a diagnosis, not an alert.</p></div>
  </div>
</section>

<section class="sec" style="padding-top:0">
  <div class="wrap">
    <div class="cta">
      <h2>Put the phone next to a stethoscope.</h2>
      <p class="on-dark" style="margin-top:1rem;max-width:40ch">The app is what a pilot site uses first, before the hardware arrives. Ask for the test build and the protocol.</p>
      <div class="cta__row"><a class="btn btn--wine" href="contact.html">hello@heart-ware.org <span class="btn__arrow">&rarr;</span></a></div>
    </div>
  </div>
</section>
"""


EVIDENCE = f"""
<section class="ptop sec--tight" style="position:relative;overflow:hidden">
  <div class="blob" style="width:24rem;height:24rem;left:-8rem;bottom:-10rem;background:{BUTTER};opacity:.6"></div>
  <div class="wrap">
    <span class="chip chip--wine"><i></i>Evidence</span>
    <h1 class="mega" style="margin-top:1rem;max-width:18ch">Six numbers, and what each one is worth.</h1>
    <p class="lede" style="margin-top:1rem">Bench and simulation only. No patient has worn this yet, and the page does not imply otherwise. Every figure below is one a reviewer can recompute from the recordings.</p>
  </div>
</section>

<section class="sec--tight">
  <div class="wrap mosaic">
    <div class="card card--butter m7"><span class="card__k">1. The spread that started it</span><p class="card__n">1.73 &rarr; 0.25 dB</p><h3 style="margin-top:.7rem">The same murmur, two bodies.</h3><p class="small">Synthetic grade 2 murmur through modelled 60 mm and 110 mm chest walls, before and after correction. n = 600. Bench.</p></div>
    <div class="card card--sky m5"><span class="card__k">2. The estimator</span><p class="card__n">3.7 mm</p><h3 style="margin-top:.7rem">RMS error, wall thickness.</h3><p class="small">Estimated from the take against a measured wall, 111 recordings. Bench.</p></div>
    <div class="card card--sage m4"><span class="card__k">3. The room</span><p class="card__n">6.0 dB</p><h3 style="margin-top:.7rem">Noise rejected.</h3><p class="small">Reference capsule against a clinic room recording. Bench, one room, three assemblies.</p></div>
    <div class="card card--lilac m4"><span class="card__k">4. The gate</span><p class="card__n">45%</p><h3 style="margin-top:.7rem">Contact threshold.</h3><p class="small">Below it, no result. The gate was set on bench takes with deliberate poor contact, not tuned to look good.</p></div>
    <div class="card card--blush m4"><span class="card__k">5. The arithmetic</span><p class="card__n">0</p><h3 style="margin-top:.7rem">Nothing fitted to a population.</h3><p class="small">The correction is a division. No training set, so no inherited bias and no weights to audit.</p></div>
    <div class="card card--ink m12"><span class="card__k">6. What is not claimed</span><h3 style="margin-top:.4rem;font-size:clamp(1.3rem,2.4vw,1.9rem);max-width:34ch">It does not find disease, grade a murmur, or replace an echo.</h3><p class="small">It corrects a recording for the body it was taken through. A corrected recording is still a recording, and the next step is a pilot with echo-booked patients, not a claim.</p></div>
  </div>
</section>

<section class="sec" style="background:{BUTTER}">
  <div class="wrap">
    <h2 class="display" style="max-width:18ch">What a pilot would add.</h2>
    <p class="lede" style="margin-top:1rem">Twenty to forty patients with an echo already booked, recorded before the echo is read. That produces the one number the bench cannot: agreement with the reference the clinic already trusts.</p>
    <div class="steps" style="margin-top:1.8rem">
      <div class="step"><span class="step__n">01</span><h3>Agreement</h3><p>Does the corrected sound track the echo grade, across body types.</p></div>
      <div class="step"><span class="step__n">02</span><h3>Repeatability</h3><p>Two operators, same patient, same room. The variance that matters day to day.</p></div>
      <div class="step"><span class="step__n">03</span><h3>Refusals</h3><p>How often the gate says no, and whether those refusals were right.</p></div>
      <div class="step"><span class="step__n">04</span><h3>Time</h3><p>Added minutes per patient, measured rather than estimated.</p></div>
    </div>
  </div>
</section>
"""


CLINICAL = f"""
<section class="ptop sec--tight" style="position:relative;overflow:hidden">
  <div class="half" style="width:26rem;height:13rem;right:-6rem;bottom:-1rem;background:{BLUSH};opacity:.7"></div>
  <div class="wrap split split--57">
    <div>
      <span class="chip chip--wine"><i></i>In the clinic</span>
      <h1 class="mega" style="margin-top:1rem;max-width:14ch">The same heart, on any chest.</h1>
      <p class="lede" style="margin-top:1rem">A stethoscope is the cheapest test in medicine and the one most sensitive to who is holding it and who is lying under it. The insert takes the second variable out.</p>
    </div>
    <div class="artcard" style="transform:rotate(1.4deg)">{fig_head()}</div>
  </div>
</section>

<section class="sec--tight">
  <div class="wrap mosaic">
    <div class="card card--paper m6"><span class="card__k">What comes back</span><h3>A recording, a wall estimate and a murmur level.</h3><p class="small">Not a description of what someone thought they heard, and not a grade. The number and the take travel together.</p></div>
    <div class="card card--butter m6"><span class="card__k">The quiet patient</span><h3>A thick chest stops reading as a quiet murmur.</h3><p class="small">The same lesion sounds similar in a 60 kg and a 120 kg body, which is the whole point of the part.</p></div>
    <div class="card card--sage m4"><span class="card__k">Handover</span><h3>The next clinician hears the sound.</h3><p class="small">With the site and the quality attached, instead of a sentence in the notes.</p></div>
    <div class="card card--blush m4"><span class="card__k">Refusal</span><h3>The instrument may say no.</h3><p class="small">Poor contact returns nothing. A machine that always answers is not measuring anything.</p></div>
    <div class="card card--lilac m4"><span class="card__k">The round</span><h3>Nothing changes about the round.</h3><p class="small">No cart, no network, no new room. The stethoscope in the pocket is the one that gets the insert.</p></div>
  </div>
</section>

<section class="sec" style="background:{WINE};color:{PAPER};position:relative;overflow:hidden">
  <div class="dots" style="color:rgba(251,246,236,.2);width:20rem;height:12rem;right:2rem;top:2rem"></div>
  <div class="wrap">
    <h2 class="display" style="max-width:20ch">One protocol, one room, twenty patients.</h2>
    <div class="split split--57" style="margin-top:1.8rem;align-items:start">
      <div class="card" style="background:rgba(251,246,236,.08);box-shadow:none">
        <span class="card__k" style="color:{BUTTER}">We bring</span>
        <ul class="on-dark" style="display:grid;gap:.5rem">
          <li>Twenty to forty inserts, on loan for the length of the pilot.</li>
          <li>The protocol, the recording template and the analysis.</li>
          <li>A person on the phone when something does not work.</li>
        </ul>
      </div>
      <div class="card" style="background:rgba(251,246,236,.08);box-shadow:none">
        <span class="card__k" style="color:{BUTTER}">You need</span>
        <ul class="on-dark" style="display:grid;gap:.5rem">
          <li>Enough echo-booked patients to reach twenty.</li>
          <li>One person to own it, and a room to record in.</li>
          <li>Permission to publish the result, whichever way it goes.</li>
        </ul>
      </div>
    </div>
    <p class="on-dark" style="margin-top:1.6rem;max-width:52ch">No fee, no exclusivity, and no requirement that the result be flattering. If it does not work, that is worth knowing in month one.</p>
    <div class="cta__row"><a class="btn btn--ghost" href="contact.html">Start that conversation <span class="btn__arrow">&rarr;</span></a></div>
  </div>
</section>
"""


PARTNER = f"""
<section class="ptop">
  <div class="blob" style="width:24rem;height:24rem;right:-8rem;top:-9rem;background:{SAGE};opacity:.8"></div>
  <div class="wrap">
    <p class="tag tag--wine"><i></i>Work with us</p>
    <h1 class="mega">Three ways in, all of them small.</h1>
    <p class="lede" style="margin-top:1.3rem">A clinic, a distributor, a manufacturer. Each has its own first step, and none of them needs a commitment before either of us knows whether this works.</p>
  </div>
</section>

<section class="sec--tight">
  <div class="wrap ways">
    <div class="way">
      <p class="way__n">01</p>
      <div class="way__body">
        <div>
          <h3>Run a pilot.</h3>
          <p>A clinic or trial site takes twenty to forty inserts on loan, with the protocol, the recording template and the analysis. You record patients who already have an echo booked, before the echo is read. We write up what happened, including the parts that did not work.</p>
        </div>
        <div class="way__side">
          <ul>
            <li>No fee, and no exclusivity.</li>
            <li>One named owner at your end.</li>
            <li>Result publishable either way.</li>
          </ul>
          <a class="btn btn--ink btn--sm" href="mailto:hello@heart-ware.org?subject=Pilot">Pilot, in one line <span class="btn__arrow">&rarr;</span></a>
        </div>
      </div>
    </div>
    <div class="way">
      <p class="way__n">02</p>
      <div class="way__body">
        <div>
          <h3>Sell it to clinics.</h3>
          <p>Five demo units and a price list, with the list of tested heads. You take them to the accounts you already call on and tell us what the objection is.</p>
        </div>
        <div class="way__side">
          <ul>
            <li>No first-year minimum.</li>
            <li>Territory discussed once it sells.</li>
            <li>Demos stay with you either way.</li>
          </ul>
          <a class="btn btn--ink btn--sm" href="mailto:hello@heart-ware.org?subject=Distribution">Territory we should know about <span class="btn__arrow">&rarr;</span></a>
        </div>
      </div>
    </div>
    <div class="way">
      <p class="way__n">03</p>
      <div class="way__body">
        <div>
          <h3>Build it into a head.</h3>
          <p>You have the tooling, the supply chain and the regulatory experience. We have the part, the method and the bench evidence for it. The conversation starts with the design files, not with a valuation.</p>
        </div>
        <div class="way__side">
          <ul>
            <li>Design files and bench data first.</li>
            <li>NDA before any CAD.</li>
            <li>One person, one printed part, stated plainly.</li>
          </ul>
          <a class="btn btn--ink btn--sm" href="mailto:hello@heart-ware.org?subject=Licensing">Who you are, what you make <span class="btn__arrow">&rarr;</span></a>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="sec">
  <div class="wrap">
    <div class="split split--57" style="align-items:end">
      <h2 class="display">What a director asks first.</h2>
      <p class="small" style="justify-self:end;max-width:34ch">Cost, compatibility, installation, training, regulatory status and support. Answered here so they do not need a meeting.</p>
    </div>
    <div class="asks">
      <div class="ask"><span>Unit cost</span><b>$38.25</b><p>App included. No capital equipment and no fee per exam.</p></div>
      <div class="ask"><span>Compatibility</span><b>44 / 46 / 48</b><p>Millimetre single and double heads. The tested model list ships with the units.</p></div>
      <div class="ask"><span>Installation</span><b>5 min</b><p>By hand, at the sink. No tool, no adhesive, reversible.</p></div>
      <div class="ask"><span>Training</span><b>1 page</b><p>One session, and the protocol fits on a sheet.</p></div>
      <div class="ask"><span>Regulatory</span><b>Prototype</b><p>Not a medical device, not cleared, and not for diagnosis.</p></div>
      <div class="ask"><span>Support</span><b>One person</b><p>The same address, answered by whoever is building it.</p></div>
    </div>
  </div>
</section>

<section class="sec" style="padding-top:0">
  <div class="wrap">
    <div class="cta" style="background:{WINE}">
      <div class="blob" style="width:22rem;height:22rem;right:-8rem;bottom:-9rem;background:rgba(251,246,236,.1)"></div>
      <h2>Start with one sentence.</h2>
      <p class="on-dark" style="margin-top:1.2rem;max-width:38ch">Who you are, what you would do with it, and the first thing you would want to know. That is enough for a reply worth reading.</p>
      <div class="cta__row"><a class="btn btn--butter" href="contact.html">hello@heart-ware.org <span class="btn__arrow">&rarr;</span></a></div>
    </div>
  </div>
</section>
"""


PEOPLE = [
    ("Amy Wang", "Founder, system design", "Acoustic path, correction, app and the manufacturing envelope.", "AW", BUTTER),
    ("Jiahe Wang", "Co-founder, clinical protocol", "MLPAO-registered medical laboratory technician. Owns how a recording is taken.", "JW", SKY),
    ("Manolis Kellis", "Advisor, MIT", "Signal and statistical methodology: what can be claimed from a recording.", "MK", SAGE),
    ("Dr. He Huan", "Clinical advisor", "Reviews the findings language and the recording protocol.", "HH", BLUSH),
    ("Dr. Yu Dongping", "Clinical advisor", "Reviews the site-of-recording taxonomy and what the app should refuse to report.", "YD", LILAC),
    ("Grace Yu", "Advisor, interface", "Reviews the interface and the language of the findings.", "GY", BUTTER),
]


def people_cards():
    return "\n".join(
        f'<div class="person"><div class="person__av" style="background:{c}">{i}</div>'
        f'<h3>{n}</h3><p class="person__role">{r}</p><p>{d}</p></div>'
        for n, r, d, i, c in PEOPLE
    )


ABOUT = f"""
<section class="ptop sec--tight" style="position:relative;overflow:hidden">
  <div class="blob" style="width:20rem;height:20rem;left:-7rem;top:-8rem;background:{LILAC};opacity:.75"></div>
  <div class="wrap split split--57">
    <div>
      <span class="chip"><i></i>About</span>
      <h1 class="mega" style="margin-top:1rem;max-width:15ch">Two recordings that should have matched.</h1>
      <p class="lede" style="margin-top:1rem">Same murmur, same grade, two patients. One was audible at the door, one needed the room quiet and the chestpiece pressed hard. The difference was not the heart. It was the tissue in front of it.</p>
    </div>
    <div class="artcard" style="background:{BLUSH};transform:rotate(1.6deg)">{fig_side()}</div>
  </div>
</section>

<section class="sec--tight">
  <div class="wrap mosaic">
    <div class="card card--paper m6"><span class="card__k">Why a physical part</span><h3>Software cannot know what the wall was.</h3><p class="small">The chest wall sits between the heart and every microphone you could put on the skin. Software can correct it only if it knows the filter, and the only place that information exists is the recording itself. So the device measures the wall, and the software divides by it.</p></div>
    <div class="card card--paper m6"><span class="card__k">Why it is not a model</span><h3>One division, not a training set.</h3><p class="small">A learned correction would need recordings paired with imaging from thousands of bodies, and it would be impossible to say which part of the answer came from the physics and which from the population. This is arithmetic, and it can be checked with a calculator.</p></div>
    <div class="card card--navy m12">
      <span class="card__k">Where it is now</span>
      <div class="steps steps--3" style="margin-top:.6rem">
        <div><p class="card__n" style="font-size:clamp(1.6rem,3vw,2.2rem)">Rev D</p><p class="small" style="margin-top:.3rem">Printed, hand fitted, workable. More than 100 people have handled it.</p></div>
        <div><p class="card__n" style="font-size:clamp(1.6rem,3vw,2.2rem)">Bench</p><p class="small" style="margin-top:.3rem">Simulation and bench evidence, 111 recordings. The study has not started.</p></div>
        <div><p class="card__n" style="font-size:clamp(1.6rem,3vw,2.2rem)">Tooling</p><p class="small" style="margin-top:.3rem">Not paid for, and not dated. What exists is a printed part and a method.</p></div>
      </div>
    </div>
  </div>
</section>

<section class="sec" style="background:{PAPER2};position:relative;overflow:hidden">
  <div class="wrap">
    <h2 class="display" style="max-width:16ch">The people who built it.</h2>
    <p class="lede" style="margin-top:.8rem">Engineering, clinical protocol and review. Everyone here has handled the device or read the analysis.</p>
    <div class="people" style="margin-top:1.8rem">
      {people_cards()}
    </div>
  </div>
</section>
"""


CONTACT = f"""
<section class="ptop sec--tight" style="position:relative;overflow:hidden">
  <div class="blob" style="width:24rem;height:24rem;right:-8rem;top:-9rem;background:{BUTTER};opacity:.7"></div>
  <div class="wrap">
    <span class="chip chip--wine"><i></i>Contact</span>
    <h1 class="mega" style="margin-top:1rem;max-width:14ch">One address, read by a person.</h1>
    <p class="lede" style="margin-top:1rem">There is no form, because a form puts a queue between you and the person who can answer. Write to hello and say which of the three you are.</p>
    <p style="margin-top:2.2rem"><a class="bigmail" href="mailto:hello@heart-ware.org">hello@heart-ware.org</a></p>
  </div>
</section>

<section class="sec--tight">
  <div class="wrap mosaic">
    <div class="card card--sky m6"><span class="card__k">Clinic or trial site</span><h3>The heads you use.</h3><p class="small">How many patients you could enrol, and who would run it. One line each is enough.</p></div>
    <div class="card card--butter m6"><span class="card__k">Distributor</span><h3>The territory you cover.</h3><p class="small">The stethoscope brands you carry, and where the price list would land.</p></div>
    <div class="card card--blush m6"><span class="card__k">Manufacturer</span><h3>Who you are, what you make.</h3><p class="small">The design files and the bench data come back under an NDA.</p></div>
    <div class="card card--sage m6"><span class="card__k">Everything else</span><h3>Same address.</h3><p class="small">It reaches the same person, and gets the same reply.</p></div>
  </div>
</section>

<section class="sec" style="background:{SAGE}">
  <div class="wrap">
    <h2 class="display" style="max-width:14ch">What happens next.</h2>
    <div class="steps steps--3" style="margin-top:1.6rem">
      <div class="step"><span class="step__n">1</span><h3>Two working days</h3><p>A reply from a person, with the protocol or the price list attached.</p></div>
      <div class="step"><span class="step__n">2</span><h3>Then a call</h3><p>Thirty minutes, no deck, with the questions we cannot answer yet written down.</p></div>
      <div class="step"><span class="step__n">3</span><h3>If it fits</h3><p>Units ship with the protocol and a named contact for the length of the pilot.</p></div>
    </div>
  </div>
</section>
"""


NOTFOUND = f"""
<section class="hero" style="min-height:76svh;display:grid;align-content:center">
  <div class="ghostword" style="right:-1rem;bottom:-3rem">404</div>
  <div class="audiowave"><svg viewBox="0 0 1440 160" preserveAspectRatio="none" aria-hidden="true"><path d="M0 120 C 90 120 90 40 180 40 S 270 120 360 120 S 450 40 540 40 S 630 120 720 120 S 810 40 900 40 S 990 120 1080 120 S 1170 40 1260 40 S 1350 120 1440 120" fill="none" stroke="#f7dda2" stroke-width="2"/></svg></div>
  <div class="wrap">
    <p class="tag tag--wine"><i></i>404</p>
    <h1 class="poster" style="max-width:14ch">That page is not in the record.</h1>
    <p class="lede" style="margin-top:1.3rem">The address you followed does not exist. The insert, the method and the evidence all do.</p>
    <div class="cta__row">
      <a class="btn btn--butter" href="index.html">Back to the site <span class="btn__arrow">&rarr;</span></a>
      <a class="btn btn--ghost" href="evidence.html">The evidence</a>
    </div>
  </div>
</section>
"""


if __name__ == "__main__":
    page("index.html", "A stethoscope insert that takes the chest wall out of the recording",
         "A 45 gram insert that measures the chest wall from the recording and removes it, so a heart sounds the same in every body.", "home", HOME)
    page("product.html", "The insert",
         "Rev D: dimensions, materials, electronics and regulatory status, with the numbers behind each.", "product", PRODUCT)
    page("technology.html", "How it works",
         "Two microphones, one division. The method, the arithmetic and how to check it.", "technology", TECH)
    page("app.html", "The app",
         "The recording interface, running in the browser: listen, measure, correct, accept.", "app", APP)
    page("evidence.html", "Evidence",
         "Six results, the size of each set, and what has not been claimed.", "evidence", EVIDENCE)
    page("clinical.html", "In the clinic",
         "What changes at the bedside, and what a pilot would need from a site.", "clinical", CLINICAL)
    page("partnerships.html", "Work with us",
         "A pilot, distribution or licensing: the small first step for each, and what it costs.", "partnerships", PARTNER)
    page("about.html", "About",
         "Why a physical part, who built it, and where it is now.", "about", ABOUT)
    page("404.html", "Not found",
         "That page is not in the record.", "404", NOTFOUND)
    page("contact.html", "Contact",
         "One address, read by a person. hello@heart-ware.org", "contact", CONTACT)
