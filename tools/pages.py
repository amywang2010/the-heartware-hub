"""Page content. Run tools/pages.py to write the HTML."""

from pathlib import Path

from build import foot, head

ROOT = Path(__file__).resolve().parent.parent


def page(name, title, desc, key, body):
    (ROOT / name).write_text(head(title, desc, key) + body + foot(), encoding="utf-8")
    print("wrote", name)


def demo_block():
    """The phone demo. Used on the home page and the app page; demo.js drives it."""
    return """
<div class="demo" data-demo>
  <div class="demo__stage">
    <div class="demo__phone">
      <div class="demo__screen">
        <div class="demo__bar"><span>Heartware</span><span class="demo__dot" data-demo-dot></span></div>
        <div class="demo__state" data-demo-state>Ready</div>
        <div class="demo__big" data-demo-big>&#8212;</div>
        <canvas class="demo__wave" data-demo-wave aria-label="Waveform of the recorded heart sound"></canvas>
        <div class="demo__kv"><span>Chest wall estimate</span><span><b data-demo-q>89%</b> quality</span></div>
        <div class="demo__verdict" data-demo-verdict>Press run to play a generated grade 2 murmur.</div>
        <button class="btn btn--sm" data-demo-run>Run the demo</button>
      </div>
    </div>
    <div>
      <ol class="demo__steps">
        <li class="demo__step on" data-demo-step><b>01</b><span>Listen for six seconds. One channel, 20 Hz to 2 kHz.</span></li>
        <li class="demo__step" data-demo-step><b>02</b><span>Estimate the chest wall from the recording. No tape measure, no input from the user.</span></li>
        <li class="demo__step" data-demo-step><b>03</b><span>Divide the murmur band by the wall it just measured.</span></li>
        <li class="demo__step" data-demo-step><b>04</b><span>Keep the take, or refuse it when contact is poor. Nothing uploads.</span></li>
      </ol>
      <p class="small" style="margin-top:1.2rem">This is a generated grade 2 murmur through a modelled chest wall, played in the browser. It is a demonstration of the interface, not a measurement of you.</p>
    </div>
  </div>
</div>
"""


HOME = """
<section class="hero">
  <div class="deco waves" style="left:-4%;bottom:-6px;right:-4%;height:110px;opacity:.22"></div>
  <div class="deco blob" style="width:30rem;height:30rem;right:-9rem;top:-8rem;background:var(--butter);opacity:.6"></div>
  <div class="deco dots" style="left:1.5rem;bottom:3rem;width:130px;height:110px;color:var(--red);opacity:.5"></div>
  <div class="wrap hero__grid">
    <div class="hero__type">
      <span class="kicker kicker--red"><i class="kicker__dot"></i>Stethoscope insert, Rev D</span>
      <h1 class="display">The heart sounds the same. <span class="hl">The chest is what changes.</span></h1>
      <p class="lede">A 45 gram insert drops into the stethoscope already in the room, works out the chest wall from the recording, and takes it out of the signal. Two people with the same murmur sit 1.73 dB apart. After correction, 0.25 dB.</p>
      <div class="hero__actions">
        <a class="btn btn--red" href="evidence.html">See the evidence <span class="btn__arrow">&rarr;</span></a>
        <a class="btn btn--ghost" href="contact.html">Book a pilot call</a>
      </div>
    </div>
    <div class="hero__art">
      <div class="hero__frame">
        <img src="assets/img/product-cut.jpg" alt="CAD render of Rev D sectioned along its axis, seated in a stethoscope head" width="1200" height="900">
      </div>
      <div class="hero__badge"><i></i>45 g &middot; fits 44&ndash;48 mm heads</div>
    </div>
  </div>
</section>

<section class="band band--ink sec--tight">
  <div class="wrap stats">
    <div><span class="stat__n">1.73 &rarr; 0.25</span><span class="stat__l">dB. Murmur level spread between two bodies, before and after correction. n = 600.</span></div>
    <div><span class="stat__n">3.7 mm</span><span class="stat__l">RMS error recovering the chest wall from the recording alone.</span></div>
    <div><span class="stat__n">6.0 dB</span><span class="stat__l">Room noise rejected by the reference capsule, bench measured.</span></div>
    <div><span class="stat__n">0</span><span class="stat__l">Trained parameters in the correction. It is arithmetic, and a reviewer can read it.</span></div>
  </div>
</section>

<section class="sec">
  <div class="wrap">
    <div class="head">
      <div>
        <span class="kicker kicker--ghost">What it does</span>
        <h2 class="display display--md">A small part doing <span class="mark">one job</span> properly.</h2>
      </div>
      <p class="head__aside">It does not make the stethoscope smarter, and it does not diagnose anything. It removes a known variable: the tissue between the chestpiece and the heart.</p>
    </div>
    <div class="tiles">
      <div class="tile tile--red w7 tile--tall rise">
        <div>
          <h3>It measures the wall, then reverses it.</h3>
          <p>The chest behaves like a low-pass filter whose resonance falls as the wall thickens. The insert measures that from the recording and divides it back out, in the same pass.</p>
        </div>
        <span class="tile__n">37 mm</span>
      </div>
      <div class="tile tile--lilac w5 tile--tall rise">
        <h3>Two microphones, one difference</h3>
        <p>The port capsule sits at the cup. A reference capsule sits behind a sealed cavity on the same board. Room noise reaches both and cancels; the heart reaches one.</p>
        <span class="tile__n" style="font-size:clamp(2rem,4vw,3rem)">6.0 dB</span>
      </div>
      <div class="tile tile--mint w4 rise"><h3>Fits the head you own</h3><p>38.9 mm collar, threaded into 44, 46 and 48 mm single and double heads. No adhesive and nothing drilled.</p></div>
      <div class="tile tile--butter w4 rise"><h3>Nothing leaves the phone</h3><p>Capture, correction, storage and export run on the device. There is no server in the path and nothing to breach.</p></div>
      <div class="tile tile--ink w4 rise"><h3>It refuses bad contact</h3><p>Below 45 per cent contact the app returns no reading. A confident normal that is wrong is the failure that hurts someone.</p></div>
    </div>
  </div>
</section>

<section class="sec">
  <div class="wrap">
    <div class="head">
      <div>
        <span class="kicker kicker--ghost">In the room</span>
        <h2 class="display display--md">Five minutes at the sink, then it is part of the instrument.</h2>
      </div>
      <p class="head__aside">The insert replaces the back plate of the head, so the diaphragm, stem and tube stay as they are. That is why the cost of adoption is a minute and not a capital request.</p>
    </div>
    <div class="steps">
      <div class="step rise"><span class="step__n">1</span><div><h3>Unscrew the back plate</h3><p>Every 44 to 48 mm head comes apart the same way, and the insert takes the plate's place with the stock collar holding it.</p></div></div>
      <div class="step rise"><span class="step__n">2</span><div><h3>Thread it in by hand</h3><p>Sealed with a silicone face gasket and an O-ring groove. No tool, no adhesive, IPX4 once closed.</p></div></div>
      <div class="step rise"><span class="step__n">3</span><div><h3>Record, look, decide</h3><p>A six second take, a wall estimate, a corrected sound and a quality score. The stethoscope still works with the insert out.</p></div></div>
    </div>
  </div>
</section>

<section class="band band--red sec">
  <div class="deco dots" style="right:2rem;top:2rem;width:180px;height:120px;opacity:.35;color:var(--paper)"></div>
  <div class="wrap">
    <div class="head" style="margin-bottom:1.4rem">
      <div>
        <span class="kicker">Same murmur, two bodies</span>
        <h2 class="display display--md">One patient is loud. One is quiet. Neither is more diseased.</h2>
      </div>
      <p class="head__aside" style="color:rgba(255,253,247,.82)">A grade 2 murmur reaches the earpieces 1.73 dB apart in a 60 kg body and a 120 kg one, which is a third of the band a clinician listens in. The correction closes it to a quarter of a decibel.</p>
      <div class="tiles">
      <div class="w4 heartwrap"><div class="heartstat heartstat--paper"><span class="heartstat__n">1.73 dB</span><span class="heartstat__l">apart, uncorrected</span></div></div>
      <div class="w4 heartwrap"><div class="heartstat heartstat--butter"><span class="heartstat__n">0.25 dB</span><span class="heartstat__l">apart, corrected</span></div></div>
      <div class="tile w4" style="background:transparent;color:var(--paper);box-shadow:inset 0 0 0 2px rgba(255,253,247,.55)">
        <p style="font-size:1.02rem;max-width:32ch">The number that matters is not the improvement. It is that the improvement holds for every body type in the set.</p>
      </div>
    </div>
  </div>
</section>

<section class="sec">
  <div class="wrap">
    <div class="head">
      <div>
        <span class="kicker kicker--red">The app</span>
        <h2 class="display display--md">Press run. It behaves like the phone app does.</h2>
      </div>
      <p class="head__aside">Record, measure, correct, then keep or refuse. This runs in the page on a generated murmur, so the interface can be judged without a device in your hand.</p>
    </div>
    """ + demo_block() + """
  </div>
</section>

<section class="sec--tight">
  <div class="wrap">
    <div class="tiles">
      <div class="tile tile--butter w5 tile--tall">
        <h3>What it costs</h3>
        <p>$38.25 in parts at 500 units. $59 as a pilot unit with the app included. No capital equipment, no consumables, no fee per exam.</p>
        <span class="tile__n">$38.25</span>
      </div>
      <div class="tile tile--paper w7" style="box-shadow:inset 0 0 0 2px var(--ink)">
        <h3 style="max-width:22ch">Next to what a clinic already buys</h3>
        <div class="bars" style="margin-top:1.2rem">
          <div class="bar bar--us"><div class="bar__top"><span class="bar__name">Heartware insert<span>parts, at 500 units</span></span><span class="bar__p">$38.25</span></div><div class="bar__track"><div class="bar__fill" style="width:9%"></div></div></div>
          <div class="bar"><div class="bar__top"><span class="bar__name">Eko CORE 300<span>digital stethoscope</span></span><span class="bar__p">$199</span></div><div class="bar__track"><div class="bar__fill" style="width:46%"></div></div></div>
          <div class="bar"><div class="bar__top"><span class="bar__name">3M Littmann CORE<span>digital stethoscope</span></span><span class="bar__p">$379</span></div><div class="bar__track"><div class="bar__fill" style="width:87%"></div></div></div>
        </div>
        <p class="tiny" style="margin-top:1rem">List prices, February 2026. The insert does not replace those instruments. It fits one the clinic already owns.</p>
      </div>
    </div>
  </div>
</section>

<section class="sec">
  <div class="wrap">
    <div class="cta">
      <div class="deco waves" style="left:0;right:0;bottom:-10px;height:100px;opacity:.25;filter:invert(1)"></div>
      <span class="kicker" style="background:var(--ink);color:var(--paper)">Three ways in</span>
      <h2 class="display" style="margin-top:1rem">Run a pilot, sell it, or build it into a head.</h2>
      <div class="cta__row">
        <a class="btn" href="partnerships.html">How we work with partners <span class="btn__arrow">&rarr;</span></a>
        <a class="btn btn--ghost" href="contact.html">hello@heart-ware.org</a>
      </div>
    </div>
  </div>
</section>
"""


PRODUCT = """
<section class="phero">
  <div class="deco semi" style="right:-4rem;top:-2rem;width:26rem;height:13rem;background:var(--mint)"></div>
  <div class="wrap">
    <span class="kicker">Rev D &middot; 38.9 mm collar &middot; 45 g</span>
    <h1 class="display">The insert.</h1>
    <p class="lede">It replaces the back plate of the head, so the diaphragm, stem and tube stay exactly as they are. Three printed revisions, fitted by hand to 44, 46 and 48 mm heads. It has not been tooled.</p>
  </div>
</section>

<section class="sec--tight">
  <div class="wrap tiles">
    <figure class="fig w7 rise">
      <div class="fig__img" style="background:var(--lilac)"><img src="assets/img/product-cut.jpg" alt="Rev D sectioned along the axis, seated in a stethoscope head" width="1200" height="900"></div>
      <figcaption><b>Figure 1</b> Sectioned along the axis, seated in the head it was fitted to.</figcaption>
    </figure>
    <figure class="fig w5 rise">
      <div class="fig__img" style="background:var(--butter)"><img src="assets/img/product-unit.jpg" alt="The insert on its own, threaded collar up" width="1200" height="1200"></div>
      <figcaption><b>Figure 2</b> On its own: collar, turned body, port.</figcaption>
    </figure>
    <figure class="fig w5 rise">
      <div class="fig__img" style="background:var(--mint)"><img src="assets/img/product-detail.jpg" alt="The base plate from below, four screws and the indicator lens" width="1200" height="900"></div>
      <figcaption><b>Figure 3</b> Base plate: four screws, relief groove, indicator lens.</figcaption>
    </figure>
    <figure class="fig w7 rise">
      <div class="fig__img" style="background:var(--lilac)"><img src="assets/img/product-band.jpg" alt="Rev D in a full stethoscope head, seen from the side" width="1300" height="500"></div>
      <figcaption><b>Figure 4</b> In a full head, from the side.</figcaption>
    </figure>
    <p class="tiny w12" style="margin-top:.4rem">All four are CAD renders of the printed revision. They are the closest thing we have to a photograph until a finished part exists, and they are not a substitute for one.</p>
  </div>
</section>

<section class="sec">
  <div class="wrap">
    <div class="head">
      <div>
        <span class="kicker kicker--ghost">Dimensions</span>
        <h2 class="display display--md">How it seats.</h2>
      </div>
      <p class="head__aside">Every number below was measured on a printed part, by hand, with calipers. Nothing here is a target.</p>
    </div>
    <div class="tiles">
      <div class="card card--butter w7">
        <table class="spec spec--big">
          <tr><td>Seat diameter</td><td>38.9 mm</td></tr>
          <tr><td>Fits chestpieces</td><td>44, 46 and 48 mm, single and double heads</td></tr>
          <tr><td>Retention</td><td>Stock stem collar. No adhesive, nothing drilled</td></tr>
          <tr><td>Depth behind the back plate</td><td>14 mm</td></tr>
          <tr><td>Acoustic port</td><td>3 mm, aligned to the cup</td></tr>
          <tr><td>Sealing</td><td>Silicone face gasket with an O-ring groove, IPX4</td></tr>
          <tr><td>Mass</td><td>45 g</td></tr>
        </table>
      </div>
      <div class="card card--lilac w5">
        <h3 class="display display--sm">What is inside</h3>
        <table class="spec" style="margin-top:1rem">
          <tr><td>Microphones</td><td>2 &times; TDK ICS-43434</td></tr>
          <tr><td>Audio</td><td>24-bit, 20 Hz to 2 kHz</td></tr>
          <tr><td>Radio</td><td>nRF52840, Bluetooth 5</td></tr>
          <tr><td>Storage</td><td>16 MB ring buffer</td></tr>
          <tr><td>Battery</td><td>300 mAh Li-Po, USB-C</td></tr>
          <tr><td>Runtime</td><td>About 20 h streaming, 100 exams</td></tr>
        </table>
        <p class="small" style="margin-top:1rem">Two channels, so room noise is rejected before anything is stored.</p>
      </div>
    </div>
  </div>
</section>
"""

PRODUCT += """
<section class="sec">
  <div class="wrap">
    <div class="head">
      <div>
        <span class="kicker kicker--ghost">Cost</span>
        <h2 class="display display--md">Cheaper than the instrument it fits into.</h2>
      </div>
      <p class="head__aside">A price with no comparator is just a number, so here it is next to what a clinic would otherwise buy to get a recording.</p>
    </div>
    <div class="tiles">
      <div class="card card--paper w7" style="box-shadow:inset 0 0 0 2px var(--ink)">
        <div class="bars">
          <div class="bar bar--us"><div class="bar__top"><span class="bar__name">Heartware insert<span>parts, at 500 units</span></span><span class="bar__p">$38.25</span></div><div class="bar__track"><div class="bar__fill" style="width:8%"></div></div></div>
          <div class="bar"><div class="bar__top"><span class="bar__name">Eko CORE 300<span>digital stethoscope</span></span><span class="bar__p">$199</span></div><div class="bar__track"><div class="bar__fill" style="width:41%"></div></div></div>
          <div class="bar"><div class="bar__top"><span class="bar__name">3M Littmann CORE<span>digital stethoscope</span></span><span class="bar__p">$379</span></div><div class="bar__track"><div class="bar__fill" style="width:78%"></div></div></div>
          <div class="bar"><div class="bar__top"><span class="bar__name">Eko CORE 500<span>digital stethoscope</span></span><span class="bar__p">$449</span></div><div class="bar__track"><div class="bar__fill" style="width:92%"></div></div></div>
        </div>
      </div>
      <div class="card card--mint w5">
        <h3 class="display display--sm">$59 a pilot unit</h3>
        <p class="small" style="margin-top:.8rem">Components come to $38.25 from the bill of materials at 500 units. The pilot price includes the app and the protocol, and there is no consumable and no subscription.</p>
        <p class="small" style="margin-top:.8rem">A clinic that already owns a stethoscope needs nothing else.</p>
      </div>
    </div>
  </div>
</section>

<section class="sec--tight">
  <div class="wrap">
    <div class="cta">
      <span class="kicker" style="background:var(--ink);color:var(--paper)">Before you ask</span>
      <h2 class="display" style="margin-top:1rem">This is a prototype, and the page says so.</h2>
      <p class="lede" style="color:rgba(255,253,247,.86);margin-top:1rem;max-width:52ch">Not a medical device, not cleared, and not for diagnosis. What exists is a printed insert that fits a stethoscope it was not designed for, and a correction that has been tested in simulation.</p>
      <div class="cta__row">
        <a class="btn" href="evidence.html">What has been measured <span class="btn__arrow">&rarr;</span></a>
        <a class="btn btn--ghost" href="contact.html">Ask for the drawings</a>
      </div>
    </div>
  </div>
</section>
"""


TECH = """
<section class="phero">
  <div class="deco dots" style="right:2rem;top:3rem;width:170px;height:120px;color:var(--red);opacity:.5"></div>
  <div class="wrap">
    <span class="kicker kicker--red">The method</span>
    <h1 class="display">The wall is a filter. <span class="hl hl--blue">Divide it out.</span></h1>
    <p class="lede">Five things happen between the chestpiece and the screen. Four of them are engineering. The fifth is the one that decides whether a clinician trusts the reading.</p>
  </div>
</section>

<section class="sec">
  <div class="wrap">
    <div class="steps">
      <div class="step rise"><span class="step__n">1</span><div><h3>Acoustic capture</h3><p>Two MEMS microphones look into the stock acoustic channel. The port capsule sits at the cup's own 3 mm port, so the sound path is the manufacturer's rather than one we invented.</p></div></div>
      <div class="step rise"><span class="step__n">2</span><div><h3>Reference channel</h3><p>The second capsule sits behind a sealed cavity on the same board. Room noise reaches both capsules; the heart reaches only one. Subtracting them rejects 6.0 dB of room noise before anything is stored.</p></div></div>
      <div class="step rise"><span class="step__n">3</span><div><h3>Thoracic correction</h3><p>The chest wall is a low-pass filter whose resonance falls as it thickens. From the recording alone, the insert estimates the wall to 3.7 mm RMS, then divides the murmur band by the filter that wall implies.</p></div></div>
      <div class="step rise"><span class="step__n">4</span><div><h3>Analysis</h3><p>Bands, timing and a quality score. No learned layer, so there is no training set to inherit a demographic from and nothing a reviewer has to take on trust.</p></div></div>
      <div class="step rise"><span class="step__n">5</span><div><h3>Clinical interface</h3><p>The reading is a recording, a wall estimate and a margin. It does not name a valve lesion, because naming one from a single channel has not been validated.</p></div></div>
    </div>
  </div>
</section>

<section class="band band--blue sec">
  <div class="deco semi" style="left:-3rem;bottom:0;width:18rem;height:9rem;background:rgba(255,253,247,.14)"></div>
  <div class="wrap">
    <div class="head">
      <div>
        <span class="kicker">The arithmetic</span>
        <h2 class="display display--md">One division, and nothing hidden inside it.</h2>
      </div>
      <p class="head__aside" style="color:rgba(255,253,247,.8)">The correction has no parameters that were fitted to people. That is the claim, and it is checkable in an afternoon with the code.</p>
    </div>
    <div class="tiles">
      <div class="card card--ink w7" style="padding:clamp(1.4rem,4vw,2.6rem);align-self:start">
        <p style="font-family:var(--display);font-size:clamp(1.3rem,3.2vw,2.1rem);font-weight:800;letter-spacing:-.03em;line-height:1.1;color:var(--paper)">H&#770;(f) = H(f) / T(f, d&#770;)</p>
        <p class="small" style="margin-top:1rem;color:rgba(255,253,247,.78)">H is the recording. T is the transfer function the chest wall implies at the estimated thickness. The hat on d means estimated, and the estimate is the only uncertain thing in the line.</p>
      </div>
      <div class="card w5" style="background:rgba(255,253,247,.12);color:var(--paper)">
        <h3 class="display display--sm">Where the error goes</h3>
        <table class="spec" style="margin-top:1rem">
          <tr><td>Wall estimate</td><td>3.7 mm RMS</td></tr>
          <tr><td>Murmur spread after</td><td>0.25 dB</td></tr>
          <tr><td>Model wrong by 15 to 30%</td><td>1.75 to 2.80 dB</td></tr>
        </table>
        <p class="small" style="margin-top:1rem;color:rgba(255,253,247,.78)">The method degrades gracefully: a wrong physical model costs decibels, it does not fail silently.</p>
      </div>
    </div>
  </div>
</section>

<section class="sec">
  <div class="wrap">
    <div class="head">
      <div>
        <span class="kicker kicker--ghost">Limits</span>
        <h2 class="display display--md">What this does not fix.</h2>
      </div>
      <p class="head__aside">A page that claims everything is a page nobody believes. These are the things still open, in the order they worry us.</p>
    </div>
    <div class="tiles">
      <div class="tile tile--pink w6"><h3>Diagnosis</h3><p>It does not say what is wrong with the heart. Valve disease detection needs paired recordings with echocardiography, and that study has not been run.</p></div>
      <div class="tile tile--butter w6"><h3>Placement</h3><p>A recording from the wrong intercostal space is still a recording from the wrong space. The app asks for the site and stores it; it does not correct for it.</p></div>
      <div class="tile tile--mint w6"><h3>Contact pressure</h3><p>Pressure changes the low band. The gate refuses poor contact but the repeatability protocol across operators is still being written.</p></div>
      <div class="tile tile--lilac w6"><h3>The physical model</h3><p>It is a model, fitted to four thicknesses. It holds in simulation and on the bench. It has not been checked against imaging in people.</p></div>
    </div>
  </div>
</section>
"""


APP_PAGE = """
<section class="phero">
  <div class="deco blob" style="right:-6rem;bottom:-6rem;width:22rem;height:22rem;background:var(--lilac);opacity:.75"></div>
  <div class="wrap">
    <span class="kicker kicker--red">Companion app</span>
    <h1 class="display">Record it, correct it, <span class="mark">decide</span> whether to keep it.</h1>
    <p class="lede">The phone is the instrument's screen. It does not add a model or a cloud account; it stores the thing a second reader would want to hear, and refuses when the recording is not worth keeping.</p>
  </div>
</section>

<section class="band band--lilac sec">
  <div class="wrap">
    """ + demo_block() + """
    <p class="small" style="margin-top:1.6rem;max-width:62ch">The interactive above is the same interface, running on a generated murmur and a modelled chest wall. It is here so the four screens can be judged in ten seconds, not read about in four paragraphs.</p>
  </div>
</section>

<section class="sec">
  <div class="wrap">
    <div class="head">
      <div>
        <span class="kicker kicker--ghost">Behaviour</span>
        <h2 class="display display--md">What it does at each step.</h2>
      </div>
      <p class="head__aside">Everything below runs on the phone. There is no account to make, no server to trust and no upload to forget about.</p>
    </div>
    <div class="tiles">
      <div class="tile tile--butter w6"><h3>Record</h3><p>Six seconds, one channel, 20 Hz to 2 kHz. The waveform, the wall estimate and the quality score are stored as one object, so a reading is never separated from the conditions that produced it.</p></div>
      <div class="tile tile--mint w6"><h3>Correct</h3><p>Divides the murmur band by the wall it just estimated. The corrected trace and the raw trace are both kept, so the correction can always be audited against what was heard.</p></div>
      <div class="tile tile--lilac w6"><h3>Keep</h3><p>Exports WAV and JSON together. A colleague hears the same sound rather than a description of it, and the file opens without this app.</p></div>
      <div class="tile tile--red w6"><h3>Refuse</h3><p>Under 45 per cent contact there is no reading, only a prompt to try again. A false reassurance is the failure that hurts a patient, so the default is to say nothing.</p></div>
    </div>
  </div>
</section>

<section class="sec">
  <div class="wrap">
    <div class="head">
      <div>
        <span class="kicker kicker--ghost">Under the interface</span>
        <h2 class="display display--md">What runs where.</h2>
      </div>
    </div>
    <div class="rows">
      <div class="row"><span class="row__k">Capture</span><p class="row__v">Web Audio on the demo; the I2S front end on the device. 48 kHz, 24-bit.</p></div>
      <div class="row"><span class="row__k">Analysis</span><p class="row__v">FFT 4096, three bands, one quality score.</p></div>
      <div class="row"><span class="row__k">Gate</span><p class="row__v">Contact under 45 per cent returns nothing.</p></div>
      <div class="row"><span class="row__k">Output</span><p class="row__v">WAV and JSON, stored on the device.</p></div>
      <div class="row"><span class="row__k">Upload</span><p class="row__v">None. There is no server in this path.</p></div>
    </div>
    <p class="small" style="margin-top:1.4rem;max-width:64ch">The demo page is single channel, so it shows the correction and the gate but not the differential front end. The firmware build adds the second microphone.</p>
  </div>
</section>
"""


EVIDENCE = """
<section class="phero">
  <div class="deco semi" style="right:1rem;top:-6rem;width:20rem;height:10rem;background:var(--butter)"></div>
  <div class="wrap">
    <span class="kicker">Six results, six limits</span>
    <h1 class="display">Every number, and where it came from.</h1>
    <p class="lede">Each result below carries its sample size, the method that produced it, and the thing it does not prove. Two of these results argue against the product, and they are on this page for that reason.</p>
  </div>
</section>

<section class="sec">
  <div class="wrap tiles">
    <article class="tile tile--lilac w7 tile--tall rise">
      <div><span class="kicker kicker--ghost">Result 1 &middot; in silico</span>
        <h3 style="margin-top:.9rem;font-size:clamp(1.5rem,3vw,2.2rem)">The wall can be recovered from the recording.</h3>
        <p>600 synthetic subjects, walls from 9 to 45 mm, murmur present in half. The estimator sees one three-second recording and nothing else. RMS error 3.7 mm, correlation 0.75, 86 per cent within 5 mm.</p>
      </div>
      <span class="tile__n">3.7 mm</span>
    </article>
    <article class="tile tile--red w5 tile--tall rise">
      <div><span class="kicker" style="background:var(--paper);color:var(--red)">Result 2 &middot; in silico</span>
        <h3 style="margin-top:.9rem;font-size:clamp(1.5rem,3vw,2.2rem)">Correction removes the body dependence.</h3>
        <p>Same murmur, same grade, different habitus. 1.73 dB spread before, 0.25 dB after.</p>
      </div>
      <span class="tile__n">1.73 &rarr; 0.25</span>
    </article>
    <article class="tile tile--mint w4"><h3>The shortcut fails</h3><p>Scaling by body mass or BMI leaves 1.4 dB of spread. Only the per-record estimate closes it, which is why the insert measures instead of asking.</p></article>
    <article class="tile tile--butter w4"><h3>A wrong model costs decibels</h3><p>With the physical model deliberately wrong by 15 to 30 per cent, spread lands at 1.75 to 2.80 dB against 1.93 dB exact. It degrades; it does not collapse.</p></article>
    <article class="tile tile--ink w4"><h3>Bench, not bedside</h3><p>The 6.0 dB noise rejection was measured on the bench, two capsules, one speaker. No patient was in the room.</p></article>
  </div>
</section>

<section class="band band--ink sec">
  <div class="wrap">
    <div class="head">
      <div>
        <span class="kicker" style="background:var(--paper);color:var(--ink)">The ledger</span>
        <h2 class="display display--md">Every claim, and what stands behind it.</h2>
      </div>
      <p class="head__aside">If a row says not claimed, it is not claimed anywhere on this site.</p>
    </div>
    <div class="rows">
      <div class="row"><span class="row__k">Wall thickness from the recording</span><p class="row__v">In silico, n = 600, RMS 3.7 mm</p></div>
      <div class="row"><span class="row__k">Body dependence removed</span><p class="row__v">In silico, n = 600, 1.73 to 0.25 dB</p></div>
      <div class="row"><span class="row__k">Seats in 44 to 48 mm heads</span><p class="row__v">Three printed revisions, fitted by hand</p></div>
      <div class="row"><span class="row__k">Second microphone cancels room noise</span><p class="row__v">Architecture built; 6.0 dB on the bench</p></div>
      <div class="row"><span class="row__k">Finds valve disease an uncorrected recording misses</span><p class="row__v">Not claimed. Needs paired recordings with echo</p></div>
      <div class="row"><span class="row__k">Sensitivity, specificity or AUC</span><p class="row__v">Not claimed. No such study exists yet</p></div>
    </div>
  </div>
</section>

<section class="sec">
  <div class="wrap">
    <div class="head">
      <div>
        <span class="kicker kicker--ghost">Still missing</span>
        <h2 class="display display--md">What would make this a product.</h2>
      </div>
      <p class="head__aside">Written down so nobody has to guess how far along this is.</p>
    </div>
    <div class="tiles">
      <div class="tile tile--pink w6"><h3>The clinical study</h3><p>Twenty to forty patients with an echo already booked. Paired recordings, blinded analysis, and a result that either supports the correction or does not.</p></div>
      <div class="tile tile--butter w6"><h3>The photograph</h3><p>A finished part in a real chestpiece. Everything on this site is a render until then, and a render is not evidence of a product.</p></div>
      <div class="tile tile--mint w6"><h3>The regulatory route</h3><p>510(k), exempt, or software only. Not decided, and not decided by us alone.</p></div>
      <div class="tile tile--lilac w6"><h3>The tooling</h3><p>Injection moulding and a contract manufacturer. The current housing is printed, which is why the fit is by hand.</p></div>
    </div>
  </div>
</section>
"""


CLINICAL = """
<section class="phero">
  <div class="deco dots" style="right:2rem;bottom:1rem;width:150px;height:100px;color:var(--blue);opacity:.45"></div>
  <div class="wrap">
    <span class="kicker kicker--red">In the clinic</span>
    <h1 class="display">The same heart, <span class="hl">on any chest.</span></h1>
    <p class="lede">A stethoscope is the cheapest test in medicine and the one most sensitive to who is holding it and who is lying under it. The insert takes the second variable out.</p>
  </div>
</section>

<section class="sec">
  <div class="wrap tiles">
    <div class="card card--ink w7">
      <h2 class="display display--sm">What changes at the bedside</h2>
      <div class="rows" style="margin-top:1.2rem">
        <div class="row"><span class="row__k">The reading</span><p class="row__v">A recording, a wall estimate and a margin. Not a description of what someone thought they heard.</p></div>
        <div class="row"><span class="row__k">The quiet patient</span><p class="row__v">A thick chest wall no longer reads as a quiet murmur, so the same lesion sounds similar in a 60 kg and a 120 kg body.</p></div>
        <div class="row"><span class="row__k">The handover</span><p class="row__v">The next clinician hears the sound itself, with the site and quality attached, instead of a sentence.</p></div>
        <div class="row"><span class="row__k">The refusal</span><p class="row__v">Poor contact returns nothing. The instrument is allowed to say it did not get a reading.</p></div>
      </div>
    </div>
    <div class="card card--lilac w5">
      <h2 class="display display--sm">Where it gets used</h2>
      <div class="rows" style="margin-top:1.2rem">
        <div class="row"><span class="row__k">Ward round</span><p class="row__v">The stethoscope in the pocket is the one that gets the insert.</p></div>
        <div class="row"><span class="row__k">Outpatient clinic</span><p class="row__v">A recording survives the appointment and can be reviewed later.</p></div>
        <div class="row"><span class="row__k">Outreach</span><p class="row__v">No network needed. Capture and storage are on the phone.</p></div>
      </div>
    </div>
  </div>
</section>

<section class="band band--red sec">
  <div class="wrap">
    <div class="head">
      <div>
        <span class="kicker" style="background:var(--paper);color:var(--red)">The pilot</span>
        <h2 class="display display--md">One protocol, one room, twenty patients.</h2>
      </div>
      <p class="head__aside" style="color:rgba(255,253,247,.82)">Enough to answer the only question that matters at this stage: does the corrected recording agree with the echo that was already ordered?</p>
    </div>
    <div class="tiles">
      <div class="card card--paper w6"><h3 class="display display--sm" style="color:var(--ink)">We bring</h3>
        <ul class="stack" style="margin-top:.8rem;color:var(--ink)">
          <li>Inserts for the site, matched to the heads you use</li>
          <li>The recording protocol and the analysis</li>
          <li>A written report for your team, including the parts that did not work</li>
        </ul>
      </div>
      <div class="card w6" style="background:rgba(255,253,247,.14);color:var(--paper)"><h3 class="display display--sm">You need</h3>
        <ul class="stack" style="margin-top:.8rem;color:rgba(255,253,247,.9)">
          <li>Twenty to forty patients with an echo already booked</li>
          <li>One clinician lead and an hour of training</li>
          <li>Permission to use the echo report, anonymised</li>
        </ul>
      </div>
    </div>
  </div>
</section>

<section class="sec--tight"><div class="wrap"><div class="cta">
  <span class="kicker" style="background:var(--ink);color:var(--paper)">Talk to a person</span>
  <h2 class="display" style="margin-top:1rem">Tell us what your clinic already has.</h2>
  <div class="cta__row"><a class="btn" href="contact.html">Book a pilot call <span class="btn__arrow">&rarr;</span></a><a class="btn btn--ghost" href="mailto:pilots@heart-ware.org">pilots@heart-ware.org</a></div>
</div></div></section>
"""


PARTNER = """
<section class="phero">
  <div class="deco waves" style="left:-2%;right:-2%;bottom:-1rem;height:90px;opacity:.2"></div>
  <div class="wrap">
    <span class="kicker kicker--red">Work with us</span>
    <h1 class="display">Three conversations, none of them a pitch.</h1>
    <p class="lede">We are past the drawing and short of the tooling. Whichever of the three you are, the next step is small: a room with patients in it, five units on a shelf, or an hour with the design files open on the table.</p>
  </div>
</section>

<section class="sec">
  <div class="wrap tiles">
    <article class="card card--lilac w4 rise">
      <span class="kicker kicker--ghost">Clinicians</span>
      <h2 class="display display--sm" style="margin-top:1rem">Run a pilot in your clinic</h2>
      <p class="small" style="margin-top:.8rem">Twenty to forty patients who already have an echo booked. We bring the inserts, the recording protocol and the analysis, and we write up what happened, including what did not work.</p>
      <p class="small" style="margin-top:.8rem">No fee, no exclusivity, and no requirement that the result be flattering.</p>
      <p style="margin-top:1.4rem"><a class="btn btn--sm" href="mailto:pilots@heart-ware.org">pilots@heart-ware.org</a></p>
    </article>
    <article class="card card--mint w4 rise">
      <span class="kicker kicker--ghost">Distributors</span>
      <h2 class="display display--sm" style="margin-top:1rem">Sell it where you sell stethoscopes</h2>
      <p class="small" style="margin-top:.8rem">Start with five demo units and a price list. Your reps need to have used the thing before they can explain it, so the first five are for them, not for stock.</p>
      <p class="small" style="margin-top:.8rem">No minimum in the first year. If it sells, we can talk about a territory in the second.</p>
      <p style="margin-top:1.4rem"><a class="btn btn--sm" href="mailto:hello@heart-ware.org">hello@heart-ware.org</a></p>
    </article>
    <article class="card card--butter w4 rise">
      <span class="kicker kicker--ghost">Manufacturers</span>
      <h2 class="display display--sm" style="margin-top:1rem">Build it into your own head</h2>
      <p class="small" style="margin-top:.8rem">A licensing conversation with the design files and the bench data in the room. You have the tooling, the supply chain and the regulatory experience; we have the part, the method and the evidence for it.</p>
      <p class="small" style="margin-top:.8rem">We are one person with a printed part, and we would rather say so than pretend otherwise.</p>
      <p style="margin-top:1.4rem"><a class="btn btn--sm" href="mailto:hello@heart-ware.org">hello@heart-ware.org</a></p>
    </article>
  </div>
</section>

<section class="sec">
  <div class="wrap">
    <div class="head">
      <div>
        <span class="kicker kicker--ghost">If you run the budget</span>
        <h2 class="display display--md">What a director needs to know.</h2>
      </div>
      <p class="head__aside">Cost, compatibility, installation, training and regulatory status on one screen, because those are the five questions that get asked first.</p>
    </div>
    <div class="tiles">
      <div class="card card--ink w7">
        <div class="rows" style="margin-top:0">
          <div class="row"><span class="row__k">Unit cost</span><p class="row__v">$38.25 in parts at 500 units. $59 a pilot unit, app included.</p></div>
          <div class="row"><span class="row__k">Compatibility</span><p class="row__v">44, 46 and 48 mm single and double heads. A list of tested models ships with the units.</p></div>
          <div class="row"><span class="row__k">Capital equipment</span><p class="row__v">None. It fits the stethoscope the clinic already owns.</p></div>
          <div class="row"><span class="row__k">Installation</span><p class="row__v">Five minutes, threaded by hand, no tool and no adhesive.</p></div>
          <div class="row"><span class="row__k">Training</span><p class="row__v">One session. The protocol is a page long.</p></div>
          <div class="row"><span class="row__k">Regulatory status</span><p class="row__v">Prototype. Not a medical device, not cleared, not for diagnosis. The route is not chosen yet.</p></div>
        </div>
      </div>
      <div class="card card--paper w5" style="box-shadow:inset 0 0 0 2px var(--ink);align-self:start">
        <h3 class="display display--sm">What we will not do</h3>
        <ul class="stack" style="margin-top:1rem">
          <li>Claim it finds disease. It corrects a recording.</li>
          <li>Put a unit in a clinic without a protocol and a named lead.</li>
          <li>Give a date for tooling we have not paid for.</li>
        </ul>
      </div>
    </div>
  </div>
</section>
"""


ABOUT = """
<section class="phero">
  <div class="deco blob" style="right:-5rem;top:-5rem;width:20rem;height:20rem;background:var(--mint);opacity:.7"></div>
  <div class="wrap">
    <span class="kicker">About</span>
    <h1 class="display">It started with two recordings that should have matched.</h1>
    <p class="lede">Same murmur, same grade, two patients. One was audible at the door, one needed the room quiet and the chestpiece pressed hard. The difference was not the heart. It was the tissue in front of it.</p>
  </div>
</section>

<section class="sec">
  <div class="wrap tiles">
    <div class="card card--butter w7">
      <h2 class="display display--sm">Why a physical part, and not an app</h2>
      <p class="stack" style="margin-top:1rem">The chest wall is a filter, and it sits between the heart and every microphone you could put on the skin. Software can only correct it if it knows what the filter was, and the only place that information exists is the recording itself.</p>
      <p>So the device measures the wall, and the software divides by it. Putting a second microphone behind a sealed cavity is what makes the room noise cancel; putting it in a phone case would not.</p>
      <h2 class="display display--sm" style="margin-top:1.6rem">Why it is not a model</h2>
      <p>A learned correction would need recordings paired with imaging from thousands of bodies, and it would be impossible to say which part of the answer came from the physics and which from the training set. This one is a division. It can be checked with a calculator.</p>
    </div>
    <div class="card card--lilac w5">
      <h2 class="display display--sm">Where it is now</h2>
      <div class="rows" style="margin-top:1rem">
        <div class="row"><span class="row__k">Rev D</span><p class="row__v">Printed, hand fitted, workable</p></div>
        <div class="row"><span class="row__k">Hands on it</span><p class="row__v">More than 100 people</p></div>
        <div class="row"><span class="row__k">The evidence</span><p class="row__v">Simulation and bench</p></div>
        <div class="row"><span class="row__k">The study</span><p class="row__v">Not started</p></div>
        <div class="row"><span class="row__k">Tooling</span><p class="row__v">Not paid for</p></div>
      </div>
    </div>
  </div>
</section>

<section class="sec">
  <div class="wrap">
    <div class="head head--one">
      <div>
        <span class="kicker kicker--red">The people</span>
        <h2 class="display display--md">Small, and clear about who does what.</h2>
      </div>
    </div>
    <div class="people">
      <article class="person"><h3>Founder &middot; system design</h3><p>Acoustic path, correction, app and the manufacturing envelope. Built the current insert and wrote the analysis that sets its error budget.</p></article>
      <article class="person"><h3>Co-founder &middot; clinical protocol</h3><p>MLPAO-registered medical laboratory assistant and technician. Owns how a recording is taken: which site, at what contact pressure, and who runs the sessions.</p></article>
      <article class="person"><h3>Advisor &middot; computational biology</h3><p>Professor of computational biology. Advises on signal and statistical methodology: what can be claimed from a recording, and what cannot.</p></article>
    </div>
  </div>
</section>

<section class="band band--ink sec">
  <div class="wrap">
    <div class="head">
      <div><span class="kicker" style="background:var(--butter);color:var(--ink)">How we work</span>
      <h2 class="display display--md">Three rules, and a fourth.</h2></div>
    </div>
    <div class="steps">
      <div class="step"><span class="step__n">1</span><div><h3>Measure before claiming</h3><p>Every number on this site has a method and a sample size next to it, including the ones that do not flatter us.</p></div></div>
      <div class="step"><span class="step__n">2</span><div><h3>Refusing is a feature</h3><p>A device that always answers is a device that sometimes lies. The app returns nothing when contact is poor.</p></div></div>
      <div class="step"><span class="step__n">3</span><div><h3>Say what is not done</h3><p>The clinical study, the tooling, the photograph and the regulatory route are all openly missing.</p></div></div>
      <div class="step"><span class="step__n">4</span><div><h3>Ship the prototype, not a promise</h3><p>The part exists, fits real heads and can be held. That is the whole of the claim.</p></div></div>
    </div>
  </div>
</section>
"""


CONTACT = """
<section class="phero">
  <div class="deco dots" style="right:1rem;top:2rem;width:200px;height:130px;color:var(--red);opacity:.4"></div>
  <div class="wrap">
    <span class="kicker kicker--red">Contact</span>
    <h1 class="display">Tell us which of the three you are.</h1>
    <p class="lede">No form, because a form would put a queue between you and the person who can answer. Pick the address that matches you and it lands in the right inbox.</p>
  </div>
</section>

<section class="sec">
  <div class="wrap tiles">
    <article class="card card--lilac w4">
      <span class="kicker kicker--ghost">Clinic or trial</span>
      <h2 class="display display--sm" style="margin-top:1rem">You have patients and an echo list.</h2>
      <p class="small" style="margin-top:.7rem">Tell us the heads you use and how many patients you could enrol. We will send a protocol before we ask for a meeting.</p>
      <p style="margin-top:1.2rem"><a class="btn" href="mailto:pilots@heart-ware.org">pilots@heart-ware.org</a></p>
    </article>
    <article class="card card--mint w4">
      <span class="kicker kicker--ghost">Distribution</span>
      <h2 class="display display--sm" style="margin-top:1rem">You sell to clinics already.</h2>
      <p class="small" style="margin-top:.7rem">Tell us the territory and the stethoscope brands you carry. We start with five demo units, and the price list comes with them.</p>
      <p style="margin-top:1.2rem"><a class="btn" href="mailto:hello@heart-ware.org">hello@heart-ware.org</a></p>
    </article>
    <article class="card card--butter w4">
      <span class="kicker kicker--ghost">Manufacturing</span>
      <h2 class="display display--sm" style="margin-top:1rem">You build heads, or you fund them.</h2>
      <p class="small" style="margin-top:.7rem">Licensing, tooling or investment. The design files and the bench data are available under an NDA, and the deck is short.</p>
      <p style="margin-top:1.2rem"><a class="btn" href="mailto:hello@heart-ware.org">hello@heart-ware.org</a></p>
    </article>
  </div>
</section>

<section class="sec">
  <div class="wrap">
    <div class="tiles">
      <div class="card card--ink w7">
        <h2 class="display display--sm">What happens next</h2>
        <div class="rows" style="margin-top:1rem">
          <div class="row"><span class="row__k">Within two working days</span><p class="row__v">A reply from a person, with the protocol or the price list attached.</p></div>
          <div class="row"><span class="row__k">Then a call</span><p class="row__v">Thirty minutes, no deck, with the questions we cannot answer yet written down.</p></div>
          <div class="row"><span class="row__k">If it fits</span><p class="row__v">Units ship with the protocol and a named contact for the duration of the pilot.</p></div>
        </div>
      </div>
      <div class="card card--butter w5" style="align-self:start">
        <h2 class="display display--sm">Or just write to us</h2>
        <p style="margin-top:.8rem;font-family:var(--display);font-weight:800;font-size:clamp(1.1rem,2.4vw,1.6rem);letter-spacing:-.03em;word-break:break-word">hello@heart-ware.org</p>
        <p class="small" style="margin-top:.8rem">Boston, Massachusetts. We answer email faster than anything else.</p>
      </div>
    </div>
  </div>
</section>
"""


if __name__ == "__main__":
    page("index.html", "A stethoscope insert that corrects for the chest wall",
         "Heartware is a 45 g insert that measures the chest wall from the recording and corrects for it, so a heart sounds the same in every body.",
         "home", HOME)
    page("technology.html", "How the correction works",
         "Two microphones, a filtered reference channel and one division: how Heartware estimates the chest wall and removes it.",
         "tech", TECH)
    page("product.html", "The insert, Rev D",
         "Dimensions, seating, electronics and cost of the printed stethoscope insert.",
         "product", PRODUCT)
    page("clinical.html", "In the clinic",
         "What changes at the bedside when the chest wall is taken out of the recording.",
         "clinical", CLINICAL)
    page("evidence.html", "Evidence",
         "Six results, their sample sizes and the limits of each. Including the two that argue against the product.",
         "evidence", EVIDENCE)
    page("partnerships.html", "Work with us",
         "Pilot a clinic, distribute the insert, or license it into a stethoscope head.",
         "partners", PARTNER)
    page("about.html", "About",
         "Why the correction is a physical part, and what is still missing.",
         "about", ABOUT)
    page("contact.html", "Contact",
         "Pilot enquiries, distribution and manufacturing, to the person who owns the question.",
         "contact", CONTACT)
    page("app.html", "The app",
         "The companion app running in the page: listen, measure, correct, keep or refuse.",
         "app", APP_PAGE)
