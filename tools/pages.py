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
    <p class="small" style="margin-top:1.4rem">A generated grade 2 murmur through a modelled chest wall, played in the browser. It shows the interface, it does not measure you.</p>
  </div>
</div>
"""


HOME = """
<section class="hero">
  <div class="deco deco--waves" style="left:0;right:0;bottom:0;height:64px;opacity:.5"></div>
  <div class="wrap hero__grid">
    <div class="hero__type">
      <span class="kicker kicker--wine">Stethoscope insert, Rev D</span>
      <h1 class="display">The heart sounds the same. <span class="display--wine">The chest is what changes.</span></h1>
      <p class="lede">A 45 gram insert drops into the stethoscope already in the room, works out the chest wall from the recording, and takes it out of the signal. Two people with the same murmur sit 1.73 dB apart. After correction, 0.25 dB.</p>
      <div class="hero__actions">
        <a class="btn btn--wine" href="evidence.html">See the evidence <span class="btn__arrow">&rarr;</span></a>
        <a class="btn btn--ghost" href="contact.html">Book a pilot call</a>
      </div>
    </div>
    <div class="hero__art">
      <div class="hero__frame">
        <img src="assets/img/product-cut.jpg" alt="Studio render of Rev D sectioned along its axis, seated in a stethoscope head" width="1200" height="900">
      </div>
      <div class="hero__badge"><i></i>45 g &middot; fits 44&ndash;48 mm heads</div>
    </div>
  </div>
</section>

<section class="band--ink sec--tight">
  <div class="wrap stats">
    <div><span class="stat__n">1.73 &rarr; 0.25</span><span class="stat__l">dB. Murmur level spread between two bodies, before and after correction. n = 600.</span></div>
    <div><span class="stat__n">3.7 mm</span><span class="stat__l">RMS error recovering the chest wall from the recording alone.</span></div>
    <div><span class="stat__n">6.0 dB</span><span class="stat__l">Room noise rejected by the reference capsule, bench measured.</span></div>
    <div><span class="stat__n">0</span><span class="stat__l">Fitted parameters. The correction is arithmetic, and a reviewer can read every line of it.</span></div>
  </div>
</section>

<section class="sec">
  <div class="wrap split split--57 split--top">
    <div>
      <h2 class="stmt">It measures the chest wall, then divides it back out.</h2>
      <p class="lede" style="margin-top:1.2rem">The chest behaves like a low-pass filter whose resonance falls as the wall thickens. The insert measures that from the recording itself and removes it in the same pass, so there is no second device and no input from the person holding it.</p>
      <div class="rows" style="margin-top:1.8rem">
        <div class="row"><span class="row__k">37 mm</span><span class="row__v">Chest wall estimated from a six second take, no tape measure.</span></div>
        <div class="row"><span class="row__k">0 parameters</span><span class="row__v">Nothing fitted to people, so nothing to inherit from a training set.</span></div>
        <div class="row"><span class="row__k">45 g</span><span class="row__v">Threaded by hand into 44, 46 and 48 mm heads. No adhesive, nothing drilled.</span></div>
      </div>
    </div>
    <figure class="pic pic--blush">
      <div class="pic__box" style="aspect-ratio:4/5"><img src="assets/img/product-band.jpg" alt="Studio render of the insert on its side, showing the collar and the gasket groove" width="1200" height="1500"></div>
      <figcaption>Rev D, printed and hand finished. The render is a studio image of the CAD, not a photograph of a tooled part.</figcaption>
    </figure>
  </div>
</section>

<section class="band--wine sec">
  <div class="wrap">
    <div class="split split--75 split--top">
      <div>
        <h2 class="display display--md">One patient is loud. One is quiet. Neither is more diseased.</h2>
        <p style="margin-top:1.1rem;max-width:44ch;color:rgba(251,247,240,.84)">A grade 2 murmur reaches the earpieces 1.73 dB apart in a 60 kg body and a 120 kg one, a third of the band a clinician listens in. The correction closes it to a quarter of a decibel.</p>
      </div>
      <div class="tiles">
        <div class="w6 heartwrap"><div class="heartstat heartstat--paper"><span class="heartstat__n">1.73 dB</span><span class="heartstat__l">apart, uncorrected</span></div></div>
        <div class="w6 heartwrap"><div class="heartstat heartstat--butter"><span class="heartstat__n">0.25 dB</span><span class="heartstat__l">apart, corrected</span></div></div>
      </div>
    </div>
  </div>
</section>

<section class="band--sky sec">
  <div class="wrap">
    <div class="split split--75" style="align-items:end;margin-bottom:clamp(1.6rem,3vw,2.6rem)">
      <h2 class="display display--md">Press run. It behaves like the phone app does.</h2>
      <p class="small" style="max-width:34ch;justify-self:end">Record, measure, correct, then keep or refuse. This runs on a generated murmur, so the interface can be judged without a device in your hand.</p>
    </div>
""" + demo_block() + """
  </div>
</section>

<section class="sec">
  <div class="wrap price">
    <div>
      <span class="kicker kicker--navy">Price</span>
      <p class="price__n" style="margin-top:.9rem">$38.25<small>per unit, app included. No capital equipment, no consumable, no fee per exam.</small></p>
      <p class="small" style="margin-top:1.2rem;max-width:32ch">Materials and machining come in under that, so the price survives a distributor margin rather than depending on one.</p>
    </div>
    <div>
      <p class="small" style="margin-bottom:.8rem">Next to what a clinic already buys, at list price, February 2026.</p>
      <ul class="pricelist">
        <li><span class="us">Heartware insert <span class="tiny">digital stethoscope not required</span></span><b class="us">$38.25</b></li>
        <li><span>Eko CORE 300 <span class="tiny">digital stethoscope</span></span><b>$199</b></li>
        <li><span>3M Littmann CORE <span class="tiny">digital stethoscope</span></span><b>$379</b></li>
        <li><span>Littmann 3200 <span class="tiny">digital stethoscope</span></span><b>$449</b></li>
      </ul>
      <p class="tiny" style="margin-top:1rem">The insert does not replace those instruments. It fits one the clinic already owns.</p>
    </div>
  </div>
</section>

<section class="sec">
  <div class="wrap">
    <div class="cta">
      <h2 class="display">Run a pilot, sell it, or build it into a head.</h2>
      <div class="cta__row">
        <a class="btn btn--wine" href="partnerships.html">How we work with partners <span class="btn__arrow">&rarr;</span></a>
        <a class="btn btn--ghost" href="contact.html">hello@heart-ware.org</a>
      </div>
    </div>
  </div>
</section>
"""


PRODUCT = """
<section class="ptop">
  <div class="wrap">
    <span class="kicker kicker--wine">Rev D &middot; 38.9 mm collar &middot; 45 g</span>
    <h1 class="display">The insert.</h1>
    <p class="lede">It replaces the back plate of the head, so the diaphragm, stem and tube stay as they are. Three printed revisions, fitted by hand to 44, 46 and 48 mm heads. It has not been tooled.</p>
    <div class="cta__row" style="margin-top:1.4rem">
      <a class="btn btn--navy" href="evidence.html">What it has been measured on</a>
      <a class="btn btn--ghost" href="contact.html">Ask for the drawings</a>
    </div>
  </div>
</section>

<section class="sec--tight">
  <div class="wrap">
    <figure class="pic pic--sage">
      <div class="pic__box" style="aspect-ratio:21/9"><img src="assets/img/product-cut.jpg" alt="Studio render of Rev D sectioned along its axis" width="1600" height="686"></div>
      <figcaption>Rev D, detail. Printed in graphite, thread cut after printing, gasket seated by hand.</figcaption>
    </figure>
  </div>
</section>

<section class="sec">
  <div class="wrap split split--64 split--top">
    <div>
      <h2 class="display display--md">Everything measurable, in four drawers.</h2>
      <p class="lede" style="margin-top:.9rem">Open a drawer for the numbers behind it. Nothing here is a target dressed as a specification: where a figure is bench measured it says so, and where it is a design value it says that instead.</p>
    </div>
    <div class="acc">
      <details>
        <summary>Dimensions <span>38.9 mm collar</span></summary>
        <div class="acc__in">
          <div class="rows">
            <div class="row"><span class="row__k">Collar diameter</span><span class="row__v">38.9 mm, threaded M40 &times; 0.75, 4.5 mm engagement.</span></div>
            <div class="row"><span class="row__k">Body height</span><span class="row__v">17.2 mm below the back plate, 11.4 mm above it.</span></div>
            <div class="row"><span class="row__k">Mass</span><span class="row__v">45 g assembled, including the board and the gasket.</span></div>
            <div class="row"><span class="row__k">Head fit</span><span class="row__v">44, 46 and 48 mm single and double heads, tested on 11 models across three manufacturers.</span></div>
            <div class="row"><span class="row__k">Clearance</span><span class="row__v">Keeps the diaphragm plane unchanged, so the acoustic load on the skin is the head's own.</span></div>
          </div>
        </div>
      </details>
      <details>
        <summary>Materials and finish <span>printed, then machined</span></summary>
        <div class="acc__in">
          <div class="rows">
            <div class="row"><span class="row__k">Housing</span><span class="row__v">PA12, laser sintered. Graphite anodised aluminium collar.</span></div>
            <div class="row"><span class="row__k">Sealing</span><span class="row__v">Silicone face gasket, 60 Shore A, plus an O-ring groove at the collar.</span></div>
            <div class="row"><span class="row__k">Ingress</span><span class="row__v">IPX4 once closed, bench tested on three assemblies.</span></div>
            <div class="row"><span class="row__k">Cleaning</span><span class="row__v">Alcohol wipes on the outer surfaces. Not autoclavable, and the page will keep saying so.</span></div>
          </div>
        </div>
      </details>
      <details>
        <summary>Electronics <span>two capsules, one board</span></summary>
        <div class="acc__in">
          <div class="rows">
            <div class="row"><span class="row__k">Capsules</span><span class="row__v">Two MEMS microphones. The port capsule sits at the cup, the reference capsule behind a sealed cavity on the same board.</span></div>
            <div class="row"><span class="row__k">Band</span><span class="row__v">20 Hz to 2 kHz, sampled at 8 kHz. The murmur band of interest sits between 40 and 600 Hz.</span></div>
            <div class="row"><span class="row__k">Noise rejection</span><span class="row__v">6.0 dB of room noise removed by the difference of the two capsules, bench measured.</span></div>
            <div class="row"><span class="row__k">Link</span><span class="row__v">BLE to the phone. Recording, correction and storage all run on the phone; the insert sends audio and nothing else.</span></div>
            <div class="row"><span class="row__k">Power</span><span class="row__v">Sealed cell, 40 hours of recording, charged through the case.</span></div>
          </div>
        </div>
      </details>
      <details>
        <summary>Regulatory status <span>prototype</span></summary>
        <div class="acc__in">
          <p>A prototype. Not a medical device, not cleared, and not for diagnosis. The route is not chosen yet, and the page will not pretend otherwise.</p>
          <p>What exists: bench measurements, simulation, and recordings from people under a protocol. What does not: a paired clinical study, a quality system, and a predicate.</p>
        </div>
      </details>
    </div>
  </div>
</section>

<section class="sec band--paper2">
  <div class="wrap price">
    <div>
      <p class="price__n">$38.25<small>a unit, app included. The bill of materials is smaller than that, which is the point of the whole shape.</small></p>
    </div>
    <div>
      <h2 class="display display--sm">Why it can be this cheap</h2>
      <p class="small" style="margin-top:.6rem">One printed housing, one board, two capsules and a gasket. No display, no battery pack, no dock, and no second instrument in the room. The phone the clinician already carries does the computing.</p>
      <ul class="pricelist" style="margin-top:1.4rem">
        <li><span class="us">Heartware insert</span><b class="us">$38.25</b></li>
        <li><span>Eko CORE 300</span><b>$199</b></li>
        <li><span>3M Littmann CORE</span><b>$379</b></li>
        <li><span>Littmann 3200</span><b>$449</b></li>
      </ul>
      <p class="tiny" style="margin-top:1rem">Comparator prices are list prices, February 2026.</p>
    </div>
  </div>
</section>
"""


TECH = """
<section class="ptop">
  <div class="wrap">
    <span class="kicker kicker--navy">The method</span>
    <h1 class="display">Two microphones, one division.</h1>
    <p class="lede">A stethoscope hears the heart through a filter made of tissue. The method measures that filter from the same recording and divides it out, which is why it needs no second device and no prior scan.</p>
  </div>
</section>

<section class="sec--tight">
  <div class="wrap steps">
    <div class="step rise"><span class="step__n">01</span><h3>Two capsules, one difference</h3><p>The port capsule sits at the cup. The reference capsule sits behind a sealed cavity on the same board. Room noise reaches both and cancels; the heart reaches one. That difference is 6.0 dB of noise gone before any processing.</p></div>
    <div class="step rise"><span class="step__n">02</span><h3>Estimate the wall</h3><p>The chest wall is a low-pass filter whose resonance falls as the wall thickens. The recording carries that resonance, so the wall can be estimated from it: 3.7 mm RMS against calipers, no tape measure and no input from the user.</p></div>
    <div class="step rise"><span class="step__n">03</span><h3>Divide it out</h3><p>The transfer function implied by the estimated wall is inverted and applied to the murmur band. The sound that reaches the app has the body taken out of it, and the correction is one line of arithmetic.</p></div>
  </div>
</section>

<section class="band--ink sec">
  <div class="deco deco--diag" style="right:0;top:0;width:38%;height:100%;opacity:.16;color:var(--sky)"></div>
  <div class="wrap split split--57 split--top">
    <div>
      <h2 class="display display--md">One division, and nothing hidden inside it.</h2>
      <p class="formula" style="margin-top:1.6rem">H&#770;(f) = H(f) / T(f, d&#770;)</p>
      <p class="small" style="margin-top:1rem;max-width:36ch">H is the recording. T is the transfer function the chest wall implies at the estimated thickness. The hat on d means estimated, and the estimate is the only uncertain term in the line.</p>
    </div>
    <div>
      <div class="rows">
        <div class="row"><span class="row__k">Wall estimate</span><span class="row__v">3.7 mm RMS error, calipers as reference.</span></div>
        <div class="row"><span class="row__k">Murmur spread after</span><span class="row__v">0.25 dB between a 60 kg body and a 120 kg one.</span></div>
        <div class="row"><span class="row__k">Model wrong by 15 to 30%</span><span class="row__v">The method degrades gracefully. A wrong physical model costs decibels, it does not fail silently.</span></div>
        <div class="row"><span class="row__k">Fitted to people</span><span class="row__v">Nothing. There is no training set to inherit a demographic bias from.</span></div>
      </div>
    </div>
  </div>
</section>

<section class="sec">
  <div class="wrap split split--75 split--top">
    <div>
      <h2 class="display display--md">You can check it in an afternoon.</h2>
      <p class="lede" style="margin-top:1rem">That is the claim worth testing first. A learned correction can only be taken on trust. This one can be read.</p>
    </div>
    <div class="acc">
      <details open><summary>Read the arithmetic<span>one page</span></summary><div class="acc__in"><p>The correction is an analytic transfer function, not a network. Send a recording and the parameters used with it and the whole chain can be recomputed by hand or in a spreadsheet.</p></div></details>
      <details><summary>Rerun the bench set<span>111 recordings</span></summary><div class="acc__in"><p>Every claim on the evidence page comes from a set that can be rerun. The recordings, the protocol and the analysis are available under an NDA.</p></div></details>
      <details><summary>Put it on a known patient<span>the real test</span></summary><div class="acc__in"><p>A pilot with echo booked alongside is the only test that settles whether the corrected sound tracks the echo. That is what the pilot section is for.</p></div></details>
    </div>
  </div>
</section>
"""


APP = """
<section class="ptop">
  <div class="wrap">
    <span class="kicker kicker--wine">Companion app</span>
    <h1 class="display">The phone is the instrument's screen.</h1>
    <p class="lede">It adds no model and no cloud account. It stores the thing a second reader would want to hear, and refuses when the recording is not worth keeping.</p>
  </div>
</section>

<section class="band--navy sec">
  <div class="wrap">
    <div class="split split--75" style="align-items:end;margin-bottom:clamp(1.6rem,3vw,2.4rem)">
      <h2 class="display display--md">Run it here before you run it on a patient.</h2>
      <p class="small" style="max-width:32ch;justify-self:end;color:rgba(251,247,240,.72)">Four phases, six seconds of audio, and the numbers the app shows while it works.</p>
    </div>
""" + demo_block() + """
  </div>
</section>

<section class="sec">
  <div class="wrap split split--57 split--top">
    <div>
      <h2 class="display display--md">What it does at each step.</h2>
      <p class="lede" style="margin-top:1rem">The interface is small on purpose. A clinician should be able to read the state of a recording from across a room, and should never have to guess whether a take was good.</p>
    </div>
    <div class="rows">
      <div class="row"><span class="row__k">Listening</span><span class="row__v">A six second take on one channel. The waveform is drawn as it arrives, so a bad seal is visible before the take ends.</span></div>
      <div class="row"><span class="row__k">Measuring</span><span class="row__v">The wall estimate climbs as the take fills. No user input, no calibration step.</span></div>
      <div class="row"><span class="row__k">Correcting</span><span class="row__v">The gain applied to the murmur band, shown as a number rather than hidden in a settings menu.</span></div>
      <div class="row"><span class="row__k">Accepting</span><span class="row__v">A quality score and a decision. Below 45 per cent contact the app returns nothing and asks for another take.</span></div>
      <div class="row"><span class="row__k">Storing</span><span class="row__v">WAV and JSON on the phone, exportable to the record the clinic already uses.</span></div>
    </div>
  </div>
</section>
"""


EVIDENCE = """
<section class="ptop">
  <div class="wrap">
    <span class="kicker kicker--navy">Evidence</span>
    <h1 class="display">Six results, and where each one comes from.</h1>
    <p class="lede">Nothing on this page is a clinical claim. These are bench and simulation results, with the size of the set and the method named so a reviewer can decide what they are worth.</p>
  </div>
</section>

<section class="band--ink sec">
  <div class="wrap">
    <div class="ledger">
      <div class="ledger__row ledger__head"><span>Claim</span><span>Where it comes from</span><span>Status</span></div>
      <div class="ledger__row"><span>Murmur spread falls from 1.73 to 0.25 dB</span><span>Simulation, 600 body models</span><span>In silico</span></div>
      <div class="ledger__row"><span>Chest wall recovered to 3.7 mm RMS</span><span>Bench, 111 recordings</span><span>Measured</span></div>
      <div class="ledger__row"><span>6.0 dB room noise rejected</span><span>Bench, two capsules, quiet and noisy room</span><span>Measured</span></div>
      <div class="ledger__row"><span>The correction needs no fitted parameters</span><span>Method, one analytic line</span><span>Readable</span></div>
      <div class="ledger__row"><span>The gate refuses poor contact</span><span>Bench, staged poor contact</span><span>Measured</span></div>
      <div class="ledger__row"><span>It finds a murmur a clinician would miss</span><span>Nobody has shown this</span><span>Not claimed</span></div>
    </div>
    <p style="margin-top:1.6rem;max-width:56ch;color:rgba(251,247,240,.7)">The last line is the one that matters. An instrument that makes a murmur easier to hear is not the same thing as an instrument that finds disease, and only a paired study can tell you which you built.</p>
  </div>
</section>

<section class="sec">
  <div class="wrap">
    <h2 class="display display--md" style="max-width:20ch">What the pilot would add.</h2>
    <p class="lede" style="margin-top:1rem">Twenty to forty patients with an echo already booked, recorded before the echo is read. That produces the one number the bench cannot: agreement with the reference the clinic already trusts.</p>
    <div class="strip" style="margin-top:clamp(1.8rem,4vw,3rem)">
      <div><span class="strip__n">01</span><h3>Agreement</h3><p>Does the corrected sound track the echo grade, across body types.</p></div>
      <div><span class="strip__n">02</span><h3>Repeatability</h3><p>Two operators, same patient, same room. The variance that matters day to day.</p></div>
      <div><span class="strip__n">03</span><h3>Refusals</h3><p>How often the gate says no, and whether those refusals were right.</p></div>
      <div><span class="strip__n">04</span><h3>Time</h3><p>Added minutes per patient, measured rather than estimated.</p></div>
    </div>
  </div>
</section>
"""


CLINICAL = """
<section class="ptop">
  <div class="wrap">
    <span class="kicker kicker--wine">In the clinic</span>
    <h1 class="display">The same heart, on any chest.</h1>
    <p class="lede">A stethoscope is the cheapest test in medicine and the one most sensitive to who is holding it and who is lying under it. The insert takes the second variable out.</p>
  </div>
</section>

<section class="sec--tight">
  <div class="wrap split split--64 split--top" style="align-items:start">
    <div class="pairs">
      <div><h3>What comes back</h3><p>A recording, a wall estimate and a murmur level. Not a description of what someone thought they heard.</p></div>
      <div><h3>The quiet patient</h3><p>A thick chest stops reading as a quiet murmur, so the same lesion sounds similar in a 60 kg and a 120 kg body.</p></div>
      <div><h3>The handover</h3><p>The next clinician hears the sound itself, with the site and quality attached, instead of a sentence.</p></div>
      <div><h3>The refusal</h3><p>Poor contact returns nothing. The instrument is allowed to say it did not get a reading.</p></div>
      <div><h3>The ward round</h3><p>The stethoscope in the pocket is the one that gets the insert. No cart, no network, no change to the round.</p></div>
      <div><h3>Five minutes</h3><p>Threaded in by hand at the sink, then it is part of the instrument for the rest of the shift.</p></div>
    </div>
    <figure class="pic pic--lilac">
      <div class="pic__box" style="aspect-ratio:4/5"><img src="assets/img/product-band.jpg" alt="Studio render of the assembled insert from the side" width="1200" height="1500"></div>
      <figcaption>Rev D, assembled. 45 g, which is lighter than the head it screws into.</figcaption>
    </figure>
  </div>
</section>

<section class="band--wine sec">
  <div class="wrap">
    <h2 class="display display--md" style="max-width:20ch">One protocol, one room, twenty patients.</h2>
    <div class="split split--57" style="margin-top:clamp(1.6rem,3vw,2.6rem)">
      <div>
        <h3 class="display display--sm">We bring</h3>
        <ul class="small" style="margin-top:.8rem;color:rgba(251,247,240,.86);display:grid;gap:.5rem">
          <li>Twenty to forty inserts, on loan for the length of the pilot.</li>
          <li>The protocol, the recording template and the analysis.</li>
          <li>A person on the phone when something does not work.</li>
        </ul>
      </div>
      <div>
        <h3 class="display display--sm">You need</h3>
        <ul class="small" style="margin-top:.8rem;color:rgba(251,247,240,.86);display:grid;gap:.5rem">
          <li>Enough echo-booked patients to reach twenty.</li>
          <li>One person to own it, and a room to record in.</li>
          <li>Permission to publish the result, whichever way it goes.</li>
        </ul>
      </div>
    </div>
    <p style="margin-top:1.8rem;color:rgba(251,247,240,.8);max-width:52ch">No fee, no exclusivity, and no requirement that the result be flattering. If it does not work, that is worth knowing in month one.</p>
    <div class="cta__row"><a class="btn btn--ghost" href="contact.html">Start that conversation</a></div>
  </div>
</section>
"""


PARTNER = """
<section class="ptop">
  <div class="wrap">
    <span class="kicker kicker--navy">Work with us</span>
    <h1 class="display">Three conversations, none of them a pitch deck.</h1>
    <p class="lede">Pick the one that matches you. Each is a small first step, and each says what it costs before you ask.</p>
  </div>
</section>

<section class="sec--tight">
  <div class="wrap">
    <div class="acc">
      <details open>
        <summary>Run a pilot in your clinic<span>20 to 40 patients</span></summary>
        <div class="acc__in">
          <p>We bring twenty to forty inserts on loan, the protocol, the recording template and the analysis. You record patients who already have an echo booked, before the echo is read. Then we write up what happened, including the parts that did not work.</p>
          <p>No fee, no exclusivity, and no requirement that the result be flattering. If it does not work, you should know in month one, and so should we.</p>
          <p><a href="mailto:hello@heart-ware.org?subject=Pilot">hello@heart-ware.org</a> with the word pilot in the subject line.</p>
        </div>
      </details>
      <details>
        <summary>Sell it to clinics<span>five demo units</span></summary>
        <div class="acc__in">
          <p>We ship five demo units and a price list. You take them to the accounts you already call on, and tell us what the objection is. There is no first-year minimum, because a minimum would make us ship to a shelf instead of to a room.</p>
          <p>If it sells, we talk about territory. If it does not, you keep the demos and we learn why.</p>
          <p><a href="mailto:hello@heart-ware.org?subject=Distribution">hello@heart-ware.org</a> with the territories you cover.</p>
        </div>
      </details>
      <details>
        <summary>Build it into a head<span>licensing</span></summary>
        <div class="acc__in">
          <p>You have the tooling, the supply chain and the regulatory experience. We have the part, the method and the evidence for it. The conversation starts with the design files and the bench data, not with a valuation.</p>
          <p>We are one person with a printed part, and we would rather say so than pretend otherwise.</p>
          <p><a href="mailto:hello@heart-ware.org?subject=Licensing">hello@heart-ware.org</a> with who you are and what you make.</p>
        </div>
      </details>
    </div>
  </div>
</section>

<section class="band--ink sec">
  <div class="wrap split split--64 split--top">
    <div>
      <h2 class="display display--md">What a director needs to know.</h2>
      <p style="margin-top:1rem;max-width:36ch;color:rgba(251,247,240,.72)">Cost, compatibility, installation, training and regulatory status on one page, because those are the five questions that get asked first.</p>
    </div>
    <div class="rows">
      <div class="row"><span class="row__k">Unit cost</span><span class="row__v">$38.25, app included.</span></div>
      <div class="row"><span class="row__k">Compatibility</span><span class="row__v">44, 46 and 48 mm single and double heads. A list of tested models ships with the units.</span></div>
      <div class="row"><span class="row__k">Capital equipment</span><span class="row__v">None. It fits the stethoscope the clinic already owns.</span></div>
      <div class="row"><span class="row__k">Installation</span><span class="row__v">Five minutes, threaded by hand. No tool and no adhesive.</span></div>
      <div class="row"><span class="row__k">Training</span><span class="row__v">One session. The protocol is a page long.</span></div>
      <div class="row"><span class="row__k">Regulatory status</span><span class="row__v">Prototype. Not a medical device, not cleared, not for diagnosis.</span></div>
    </div>
  </div>
</section>

<section class="sec">
  <div class="wrap split split--75 split--top">
    <h2 class="display display--md" style="max-width:14ch">What we will not do.</h2>
    <ul style="display:grid;gap:1rem;max-width:52ch">
      <li class="small" style="font-size:1.02rem;color:var(--ink)">Claim it finds disease. It corrects a recording, and a recording is not a diagnosis.</li>
      <li class="small" style="font-size:1.02rem;color:var(--ink)">Put a unit in a clinic without a protocol and a named lead. That is how a pilot becomes a drawer.</li>
      <li class="small" style="font-size:1.02rem;color:var(--ink)">Give a date for tooling we have not paid for.</li>
    </ul>
  </div>
</section>
"""


ABOUT = """
<section class="ptop">
  <div class="wrap split split--64 split--top">
    <div>
      <span class="kicker kicker--plain">About</span>
      <h1 class="display">It started with two recordings that should have matched.</h1>
      <p class="lede">Same murmur, same grade, two patients. One was audible at the door, one needed the room quiet and the chestpiece pressed hard. The difference was not the heart. It was the tissue in front of it.</p>
    </div>
    <figure class="pic pic--blush">
      <div class="pic__box" style="aspect-ratio:1"><img src="assets/img/product-cut.jpg" alt="Studio render of the sectioned insert" width="1200" height="1200"></div>
      <figcaption>Rev D in section, seated in a head.</figcaption>
    </figure>
  </div>
</section>

<section class="sec--tight">
  <div class="wrap split split--75 split--top">
    <div>
      <h2 class="display display--sm">Why a physical part, and not an app</h2>
      <p class="small" style="margin-top:.7rem">The chest wall is a filter, and it sits between the heart and every microphone you could put on the skin. Software can correct it only if it knows what the filter was, and the only place that information exists is the recording itself. So the device measures the wall, and the software divides by it.</p>
      <h2 class="display display--sm" style="margin-top:1.8rem">Why it is not a model</h2>
      <p class="small" style="margin-top:.7rem">A learned correction would need recordings paired with imaging from thousands of bodies, and it would be impossible to say which part of the answer came from the physics and which from the training set. This is one division, and it can be checked with a calculator.</p>
    </div>
    <div class="rows">
      <div class="row"><span class="row__k">Rev D</span><span class="row__v">Printed, hand fitted, workable.</span></div>
      <div class="row"><span class="row__k">Hands on it</span><span class="row__v">More than 100 people.</span></div>
      <div class="row"><span class="row__k">The evidence</span><span class="row__v">Simulation and bench.</span></div>
      <div class="row"><span class="row__k">The study</span><span class="row__v">Not started.</span></div>
      <div class="row"><span class="row__k">Tooling</span><span class="row__v">Not paid for.</span></div>
    </div>
  </div>
</section>

<section class="sec band--paper2">
  <div class="wrap">
    <h2 class="display display--md" style="max-width:16ch">The people who built it.</h2>
    <p class="small" style="margin-top:.8rem;max-width:44ch">Engineering, clinical protocol and review. Everyone on this list has handled the device or read the analysis.</p>
    <div class="tiles" style="margin-top:2rem">
      <div class="w4"><h3 class="display display--sm">Amy Wang</h3><p class="tiny" style="color:var(--wine);font-weight:600;margin-top:.2rem">Founder, system design</p><p class="small" style="margin-top:.5rem">Acoustic path, correction, app and the manufacturing envelope.</p></div>
      <div class="w4"><h3 class="display display--sm">Jiahe Wang</h3><p class="tiny" style="color:var(--wine);font-weight:600;margin-top:.2rem">Co-founder, clinical protocol</p><p class="small" style="margin-top:.5rem">MLPAO-registered medical laboratory technician. Owns how a recording is taken.</p></div>
      <div class="w4"><h3 class="display display--sm">Manolis Kellis</h3><p class="tiny" style="color:var(--wine);font-weight:600;margin-top:.2rem">Advisor, MIT</p><p class="small" style="margin-top:.5rem">Signal and statistical methodology: what can be claimed from a recording.</p></div>
      <div class="w4"><h3 class="display display--sm">Dr. He Huan</h3><p class="tiny" style="color:var(--wine);font-weight:600;margin-top:.2rem">Clinical advisor</p><p class="small" style="margin-top:.5rem">Reviews the findings language and the recording protocol.</p></div>
      <div class="w4"><h3 class="display display--sm">Dr. Yu Dongping</h3><p class="tiny" style="color:var(--wine);font-weight:600;margin-top:.2rem">Clinical advisor</p><p class="small" style="margin-top:.5rem">Reviews the site-of-recording taxonomy and what the app should refuse to report.</p></div>
      <div class="w4"><h3 class="display display--sm">Grace Yu</h3><p class="tiny" style="color:var(--wine);font-weight:600;margin-top:.2rem">Advisor, interface</p><p class="small" style="margin-top:.5rem">Reviews the interface and the language of the findings.</p></div>
    </div>
  </div>
</section>
"""


CONTACT = """
<section class="ptop">
  <div class="wrap">
    <span class="kicker kicker--wine">Contact</span>
    <h1 class="display">One address, read by a person.</h1>
    <p class="lede">There is no form, because a form builds a queue between you and the person who can answer. Write to hello and say which of the three you are.</p>
    <p style="margin-top:1.4rem"><a class="price__n" style="font-size:clamp(1.6rem,3.6vw,2.8rem);text-decoration:none" href="mailto:hello@heart-ware.org">hello@heart-ware.org</a></p>
  </div>
</section>

<section class="sec--tight">
  <div class="wrap">
    <h2 class="display display--sm" style="max-width:22ch">What to put in the message. One line each is enough.</h2>
    <div class="pairs" style="margin-top:1.4rem">
      <div><h3>Clinic or trial</h3><p>The heads you use, how many patients you could enrol, and who would run it.</p></div>
      <div><h3>Distributor</h3><p>The territory, the stethoscope brands you carry, and where the price list would land.</p></div>
      <div><h3>Manufacturer</h3><p>Who you are and what you make. The design files and bench data come back under an NDA.</p></div>
      <div><h3>Everything else</h3><p>Same address. It reaches the same person.</p></div>
    </div>
  </div>
</section>

<section class="band--navy sec">
  <div class="wrap split split--75 split--top">
    <h2 class="display display--md" style="max-width:14ch">What happens next.</h2>
    <div class="rows">
      <div class="row"><span class="row__k">Within two working days</span><span class="row__v">A reply from a person, with the protocol or the price list attached.</span></div>
      <div class="row"><span class="row__k">Then a call</span><span class="row__v">Thirty minutes, no deck, with the questions we cannot answer yet written down.</span></div>
      <div class="row"><span class="row__k">If it fits</span><span class="row__v">Units ship with the protocol and a named contact for the length of the pilot.</span></div>
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
         "Run the recording interface in the browser: listen, measure, correct, accept.", "app", APP)
    page("evidence.html", "Evidence",
         "Six results, the size of each set, and what has not been claimed.", "evidence", EVIDENCE)
    page("clinical.html", "In the clinic",
         "What changes at the bedside, and what a pilot would need from a site.", "clinical", CLINICAL)
    page("partnerships.html", "Work with us",
         "Pilot, distribution and licensing, with the small first step for each.", "partnerships", PARTNER)
    page("about.html", "About",
         "Why a physical part, who built it, and where it is now.", "about", ABOUT)
    page("contact.html", "Contact",
         "One address, read by a person.", "contact", CONTACT)
