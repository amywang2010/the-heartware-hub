"""Page content. Run tools/build.py to write the HTML."""

from pathlib import Path

from art import (
    chest_section,
    device_exploded,
    device_front,
    device_installed,
    device_side,
    icon_age,
    icon_bodies,
    icon_places,
    icon_remote,
    step_capture,
    step_correct,
    step_noise,
)
from build import NAV, foot, head

ROOT = Path(__file__).resolve().parent.parent


def page(name, title, desc, key, body):
    (ROOT / name).write_text(head(title, desc, key) + body + foot(), encoding="utf-8")
    print("wrote", name)


# --------------------------------------------------------------------------- #
# Home
# --------------------------------------------------------------------------- #
HOME = f"""
<section class="hero hero--plate">
  <img class="hero__bg" src="assets/img/product-cut.jpg" alt="The stock chestpiece cut open along its axis, showing the insert seated inside it." width="1100" height="825">
  <div class="wrap hero__inner">
    <div class="hero__grid">
      <div>
        <p class="eyebrow">Stethoscope insert · prototype 4</p>
        <h1>
          <span class="line">One murmur.</span>
          <span class="line">Two patients.</span>
          <span class="line">Two different</span>
          <span class="line">sounds.</span>
        </h1>
        <p class="hero__sub">
          The same grade 2 murmur arrives at the earpieces 1.73 dB apart in a 60 kg
          body and a 120 kg one — a third of the band a clinician is listening in.
          Heartware is a 14 mm insert that replaces the back plate of the stethoscope
          already in the room, measures the wall from the sound itself, and takes it
          back out. Same patient, same murmur, 0.25 dB apart.
        </p>
        <div class="hero__actions">
          <a class="btn btn--solid" href="evidence.html">
            Read the measurement
            <svg viewBox="0 0 16 16" aria-hidden="true"><path d="M2 8h11M9 4l4 4-4 4" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></svg>
          </a>
          <a class="btn btn--ghost" href="technology.html">How the correction works</a>
        </div>
        <div class="hero__meta">
          <div><b>Fits</b>44–48 mm chestpieces</div>
          <div><b>Adds</b>14 mm · 45 g</div>
          <div><b>Parts</b>$38.25 at 500 units</div>
        </div>
      </div>
      <p class="hero__cap">Rev D · the stock chestpiece cut along its axis, insert in place</p>
    </div>
  </div>
</section>

<section class="band" style="padding-block:clamp(3rem,5vw,4.4rem)">
  <div class="wrap">
    <p class="eyebrow" style="margin-bottom:2rem">What is on this page, in numbers</p>
    <div class="ledgerline">
      <div><span class="n">1.73 → 0.25</span><span class="k">dB, murmur spread before and after, n = 600</span></div>
      <div><span class="n">3.7 mm</span><span class="k">RMS error recovering chest wall thickness</span></div>
      <div><span class="n">6.0 dB</span><span class="k">room rejected by the reference capsule</span></div>
      <div><span class="n">0</span><span class="k">trained parameters in the correction</span></div>
    </div>
  </div>
</section>



<section>
  <div class="wrap">
    <div class="head reveal">
      <div>
        <p class="eyebrow"><b>01</b> The measurement</p>
        <h2>This is not a listening problem. It is a transfer function.</h2>
      </div>
      <p class="lede">
        A stethoscope hears the chest wall before it hears the heart. Fat, muscle and rib
        attenuate the highs, resonate the lows and add a path of their own — so the same
        valve arrives at a different amplitude in a 60 kg teenager and a 120 kg adult.
        A clinician comparing that sound to a remembered one has no way to subtract the
        difference.
      </p>
    </div>

    <div class="split split--top">
      <div class="stack">
        <p>
          Digital stethoscopes do not correct this. They reproduce the wall faithfully, at
          $250–600, which keeps them in cardiology departments while first contact happens
          in primary care, nursing homes and home visits, where the acoustic stethoscope is
          still the only instrument in the room.
        </p>
        <p>
          The fix is not a better microphone or a louder speaker. It is knowing what the
          wall did to the sound, and undoing it — per recording, from the recording.
        </p>
        <p class="smallprint">
          Every figure on this page is produced by the model in <code>research/</code>, and the
          model ships with the site: clone the repository, run it, get the same numbers.
        </p>
      </div>
      <figure class="figure reveal">
        <img src="assets/figures/fig-01-transfer.png" alt="Four transfer curves showing the same heart sound attenuated differently by 12, 20, 28 and 38 mm of chest wall." loading="lazy">
        <figcaption><b>FIG 01</b> The wall as a filter. A 38 mm wall loses 25 dB more than a 12 mm wall across the murmur band.</figcaption>
      </figure>
    </div>
  </div>
</section>

<section class="band-cream">
  <div class="wrap">
    <div class="head reveal">
      <div>
        <p class="eyebrow"><b>02</b> The method</p>
        <h2>Measure the wall. Then take it out.</h2>
      </div>
      <p class="lede">
        Three things happen between the chestpiece and the screen. None of them is a
        trained model, and none of them needs to know the patient's weight.
      </p>
    </div>

    <div class="steps">
      <div class="step reveal">
        {step_capture()}
        <h3>Characterise the path</h3>
        <p>
          The valve closures in the recording — S1 and S2 — are broadband transients. Their
          shape has passed through the wall, so the wall is written into them. Heartware
          fits the same physical model to those transients and recovers the thickness of the
          path to within a few millimetres.
        </p>
      </div>
      <div class="step reveal">
        {step_noise()}
        <h3>Separate the room</h3>
        <p>
          A second microphone sits behind a sealed cavity. It hears the room and not the
          heart, so the room can be subtracted rather than filtered. The signal-quality
          score is computed from the same two channels.
        </p>
      </div>
      <div class="step reveal">
        {step_correct()}
        <h3>Invert, or refuse</h3>
        <p>
          The wall's response is inverted with a regularised filter, so the correction stops
          pushing where the noise floor sits. Below a quality threshold the app returns no
          finding at all and asks for another recording.
        </p>
      </div>
    </div>
  </div>
</section>

<section>
  <div class="wrap">
    <div class="head reveal">
      <div>
        <p class="eyebrow"><b>03</b> Evidence</p>
        <h2>The correction is arithmetic. Arithmetic can be checked.</h2>
      </div>
      <p class="lede">
        Four results from the model in this repository, with the figures, the sample size
        and the failure cases. Every number regenerates from
        <code>research/thoracic_model.py</code>.
      </p>
    </div>

    <div class="split split--top">
      <figure class="figure reveal">
        <img src="assets/figures/fig-03-body.png" alt="Murmur level by body type, before and after correction. Before, it falls with body size; after, it is flat." loading="lazy">
        <figcaption><b>FIG 03</b> The same murmur across three body types: 1.73 dB of spread before, 0.25 dB after.</figcaption>
      </figure>
      <div class="stack">
        <div class="cards" style="grid-template-columns:1fr">
          <div class="card">
            <span class="card__num">01 · RECOVERY</span>
            <h3>3.7 mm</h3>
            <p>RMS error recovering chest-wall thickness from the recording alone, across 600 synthetic subjects. 86% within 5 mm. Nothing about the patient is supplied to the estimator.</p>
          </div>
          <div class="card">
            <span class="card__num">02 · ABLATION</span>
            <h3>1.69 → 0.25 dB</h3>
            <p>Correcting with <em>one</em> assumed thickness — the obvious shortcut — barely improves on doing nothing. The per-recording estimate is what removes the body dependence.</p>
          </div>
        </div>
        <a class="btn btn--ghost" href="evidence.html">
          All six figures and the claims ledger
          <svg viewBox="0 0 16 16" aria-hidden="true"><path d="M2 8h11M9 4l4 4-4 4" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></svg>
        </a>
      </div>
    </div>
  </div>
</section>

<section class="band-warm">
  <div class="wrap">
    <div class="head reveal">
      <div>
        <p class="eyebrow"><b>04</b> The part</p>
        <h2>Not another instrument. Six parts and a collar.</h2>
      </div>
      <p class="lede">
        The insert threads into the cup of the stethoscope a clinic already owns. Interchangeable
        collars seat it in 44, 46 and 48 mm heads; the acoustic path stays the manufacturer's.
        Remove it and the instrument is exactly what it was.
      </p>
    </div>

    <div class="plates">
      <figure class="plate reveal">
        <div class="shot">
          <img src="assets/img/product-unit.jpg" alt="The insert on its own: threaded collar, acoustic base, port lip and LED ring." width="1000" height="1000" loading="lazy">
        </div>
        <figcaption class="figcap">Fig. A · Rev D, stock chestpiece removed</figcaption>
      </figure>
      <div class="plates__note">
        <p>
          The collar threads where the back plate was. The port carries the sound 3 mm to a
          pair of MEMS microphones, one on the port and one behind a sealed cavity, and the
          difference between them is the room. The cell, the logic board and the lid stack
          behind it.
        </p>
        <a class="btn btn--ghost" href="product.html">The full specification</a>
      </div>
    </div>
  </div>
</section>

<section>
  <div class="wrap">
    <div class="cta reveal">
      <div>
        <h2>One clinic, one protocol, one echocardiogram.</h2>
        <p>
          The engineering record exists: three printed revisions, a working microphone chain,
          an app that gates its own output. What is missing is the study that turns a
          correction into a clinical claim — paired recordings and echo in a site that
          already reads echoes.
        </p>
      </div>
      <div class="cta__actions">
        <a class="btn btn--light" href="partnerships.html">Pilot and partnership</a>
        <a class="btn btn--ghost btn--on-red" href="contact.html">Talk to us</a>
      </div>
    </div>
  </div>
</section>
"""

# --------------------------------------------------------------------------- #
# Technology
# --------------------------------------------------------------------------- #
TECH = f"""
<section class="page-head">
  <div class="wrap">
    <p class="eyebrow">Technology</p>
    <h1>From the chestpiece<br>to a <em>finding</em>.</h1>
    <p class="lede">
      Five stages. The physics is the part we can defend hardest, because it is arithmetic:
      a reviewer can check it, and it cannot encode a training set.
    </p>
  </div>
</section>

<section style="padding-top:0">
  <div class="wrap">
    <div class="pipeline" data-tabs>
      <button role="tab" id="t1" aria-controls="p1" aria-selected="true">
        <span class="p-num">01</span><span class="p-name">Acoustic capture</span>
        <span class="p-sub">Two microphones, one channel</span>
      </button>
      <button role="tab" id="t2" aria-controls="p2" aria-selected="false" tabindex="-1">
        <span class="p-num">02</span><span class="p-name">Room rejection</span>
        <span class="p-sub">The second microphone</span>
      </button>
      <button role="tab" id="t3" aria-controls="p3" aria-selected="false" tabindex="-1">
        <span class="p-num">03</span><span class="p-name">Thoracic correction</span>
        <span class="p-sub">Physics, not a model</span>
      </button>
      <button role="tab" id="t4" aria-controls="p4" aria-selected="false" tabindex="-1">
        <span class="p-num">04</span><span class="p-name">Analysis</span>
        <span class="p-sub">Bands, timing, findings</span>
      </button>
      <button role="tab" id="t5" aria-controls="p5" aria-selected="false" tabindex="-1">
        <span class="p-num">05</span><span class="p-name">Clinical interface</span>
        <span class="p-sub">The working app</span>
      </button>
    </div>

    <div id="p1" role="tabpanel" aria-labelledby="t1" class="panel">
      <div class="panel__text">
        <h3>Two MEMS microphones look into the stock acoustic channel.</h3>
        <p>
          The port microphone sits at the cup's own 3 mm channel, so the sound path is the
          manufacturer's rather than one we invented. The reference microphone sits behind a
          sealed cavity on the same board. Both are TDK ICS-43434: 24-bit, 65 dB SNR,
          20 Hz–2 kHz.
        </p>
        <p>
          That upper limit is deliberate. Murmurs live between 150 and 400 Hz; above 2 kHz
          there is lung and not much else, and everything added there is noise the
          correction would have to amplify.
        </p>
        <ul class="spec-list">
          <li><span>Transducers</span><span>2 × TDK ICS-43434</span></li>
          <li><span>Word length</span><span>24-bit</span></li>
          <li><span>Bandwidth</span><span>20 Hz – 2 kHz</span></li>
          <li><span>SNR</span><span>65 dB</span></li>
          <li><span>Port</span><span>3 mm, aligned to the cup</span></li>
        </ul>
      </div>
      <div class="diagram">{step_capture()}
        <p class="small" style="margin-top:1rem">
          The port sees heart plus room. The reference sees room. Their difference is the
          signal — and the size of that difference is also the quality score.
        </p>
      </div>
    </div>

    <div id="p2" role="tabpanel" aria-labelledby="t2" class="panel" hidden>
      <div class="panel__text">
        <h3>The room is subtracted, not filtered.</h3>
        <p>
          Noise cancellation usually means guessing which part of a signal is noise. With a
          second microphone behind a sealed cavity there is nothing to guess: that channel
          contains the room and not the heart, so it can be used as a reference and removed
          adaptively.
        </p>
        <p>
          This matters more in the places we are aiming at than in a quiet cardiology
          department: a fan, a corridor, a shared ward, a home visit with a television on.
        </p>
        <ul class="spec-list">
          <li><span>Method</span><span>Adaptive two-channel subtraction</span></li>
          <li><span>Reference</span><span>Sealed cavity, same board</span></li>
          <li><span>Output</span><span>Clean signal + per-frame quality</span></li>
        </ul>
      </div>
      <div class="diagram">{step_noise()}
        <p class="small" style="margin-top:1rem">
          Bench measurement of the achieved cancellation is scheduled, not yet reported.
          We will publish the figure with the method when it is measured.
        </p>
      </div>
    </div>

    <div id="p3" role="tabpanel" aria-labelledby="t3" class="panel" hidden>
      <div class="panel__text">
        <h3>The chest wall is a filter. We fit it, then invert it.</h3>
        <p>
          Absorption rises as a power law with frequency and grows with path length; the wall
          also resonates, and the resonance falls as the wall thickens. Those two terms are
          enough to describe what the body did to the sound.
        </p>
        <p>
          The estimator fits that model to the valve closures in the recording — allowing an
          arbitrary gain, tilt and curvature for the unknown source — and reads the thickness
          off the residual shape. The operator is never asked how thick the patient's chest is,
          because that is the one number nobody in the room knows.
        </p>
        <ul class="spec-list">
          <li><span>Trained parameters</span><span>0</span></li>
          <li><span>Input</span><span>The recording</span></li>
          <li><span>Inverse</span><span>Regularised (Wiener)</span></li>
          <li><span>Failure mode</span><span>Refuses below quality threshold</span></li>
        </ul>
      </div>
      <div class="diagram">{step_correct()}
        <p class="small" style="margin-top:1rem">
          The demonstration on the Evidence page is this model running in your browser.
          The Python that produced the figures is in the repository.
        </p>
      </div>
    </div>

    <div id="p4" role="tabpanel" aria-labelledby="t4" class="panel" hidden>
      <div class="panel__text">
        <h3>What the corrected signal is asked for.</h3>
        <p>
          The corrected recording is split into the heart band (20–150 Hz), the murmur band
          (150–400 Hz) and the lung band (100–2000 Hz). S1 and S2 are located, the systolic
          interval is measured, and an energy ratio in the murmur band — anchored to the
          patient's own S1 and S2 — is what a finding is built from.
        </p>
        <p>
          Because the anchor is the same valve closures used for the correction, a reading
          cannot be improved by pressing harder, turning up the volume or moving closer.
        </p>
        <div class="note-box">
          <b>Where learning stops.</b> The correction is analytic: there is no learned layer
          to inherit a demographic from. Classification against echocardiography is the next
          study, and it is the one the pilot is built to run.
        </div>
      </div>
      <div class="diagram">
        <ul class="spec-list">
          <li><span>Heart band</span><span>20–150 Hz</span></li>
          <li><span>Murmur band</span><span>150–400 Hz</span></li>
          <li><span>Lung band</span><span>100–2000 Hz</span></li>
          <li><span>Timing</span><span>S1, S2, systolic interval</span></li>
          <li><span>Output</span><span>Site · band · likelihood · quality</span></li>
        </ul>
      </div>
    </div>

    <div id="p5" role="tabpanel" aria-labelledby="t5" class="panel" hidden>
      <div class="panel__text">
        <h3>The app is the instrument's face.</h3>
        <p>
          Record, look at the finding, keep the examination, export it. The refusal state is
          not an error dialog: it is a first-class screen, because a confident wrong normal
          is the failure that matters in a screening tool used by non-specialists.
        </p>
        <p class="small">
          The phone on the right is a working interface demo, not a video. Every tab works.
        </p>
        <a class="btn btn--ghost" href="product.html#app">Open it at full size</a>
      </div>
      <div class="diagram" style="display:grid;place-items:center">
        <p class="small" style="text-align:center">
          The interface demo lives on the product page, where it belongs.<br>
          <a href="product.html#app">Go to the app →</a>
        </p>
      </div>
    </div>
  </div>
</section>

<section class="band-cream">
  <div class="wrap">
    <div class="head reveal">
      <div>
        <p class="eyebrow">Interactive</p>
        <h2>You never tell it<br>how thick the <em>chest</em> is.</h2>
      </div>
      <p class="lede">
        Set the true chest wall — anything from 9 to 45 mm, the range the estimator was
        tested over. The device is not given that number. It recovers the wall from the
        recording, and you see the error before you see the correction.
      </p>
    </div>

    <div class="explorer reveal" data-explorer>
      <div class="explorer__head">
        <div class="wall">
          <label for="wall-range">True chest wall</label>
          <input id="wall-range" type="range" min="9" max="45" step="1" value="22" data-wall>
          <output data-wall-true>22 mm</output>
        </div>
        <div class="small" style="text-align:right">
          <span class="tiny">hidden from the device</span><br>
          <b>10–45 mm tested</b>
        </div>
      </div>

      <div class="trace">
        <div class="trace__grid"></div>
        <canvas aria-label="Murmur-band envelope, before and after correction"></canvas>
      </div>

      <dl class="readout">
        <div>
          <dt>Estimated wall</dt>
          <dd><span data-est>—</span><small>press characterise</small></dd>
        </div>
        <div>
          <dt>Murmur band</dt>
          <dd><span data-gain>0.0 dB</span><small>as recorded</small></dd>
        </div>
        <div>
          <dt>Quality</dt>
          <dd><span data-quality>0.00</span><small>check contact</small></dd>
        </div>
      </dl>

      <div class="explorer__actions">
        <button class="btn btn--solid btn--sm" data-char>Characterise the wall</button>
        <div class="seg" role="group" aria-label="Signal">
          <button data-mode="raw" aria-selected="true">As recorded</button>
          <button data-mode="corrected" aria-selected="false">Corrected</button>
        </div>
        <span class="tiny">Model output · not a patient</span>
      </div>
    </div>
  </div>
</section>
"""

# --------------------------------------------------------------------------- #
# Product
# --------------------------------------------------------------------------- #
PRODUCT = f"""
<section class="page-head">
  <div class="wrap">
    <p class="eyebrow">Product</p>
    <h1>A retrofit,<br>not a <em>replacement</em>.</h1>
    <p class="lede">
      The insert replaces the back plate of the head already in the room. The diaphragm, the
      stem, the tube and the feel stay exactly as they were — which is why the adoption cost
      is five minutes and not a capital request.
    </p>
  </div>
</section>

<section style="padding-top:0">
  <div class="wrap">
    <div class="plates plates--three">
      <figure class="plate reveal">
        <div class="shot">
          <img src="assets/img/product-cut.jpg" alt="The stock chestpiece cut along its axis, showing the insert seated inside." width="1100" height="825" loading="lazy">
        </div>
        <figcaption class="figcap">Fig. A · Cut along the axis, insert in place</figcaption>
      </figure>
      <figure class="plate reveal">
        <div class="shot">
          <img src="assets/img/product-unit.jpg" alt="The insert on its own." width="1000" height="1000" loading="lazy">
        </div>
        <figcaption class="figcap">Fig. B · The insert alone</figcaption>
      </figure>
      <figure class="plate reveal">
        <div class="shot">
          <img src="assets/img/product-macro.jpg" alt="The reflector and the insert collar, close." width="1100" height="825" loading="lazy">
        </div>
        <figcaption class="figcap">Fig. C · Reflector and collar, close</figcaption>
      </figure>
      <div class="plate reveal">
        <div style="max-width:46ch">
          <h3 style="margin-bottom:.8rem">It threads into the cup you already own.</h3>
          <p class="small">
            Interchangeable collars seat the insert in 44, 46 and 48 mm single- and double-head
            chestpieces. Retention is the stock stem collar; sealing is a silicone face gasket
            with an O-ring groove rated to IPX4. Nothing is drilled, nothing is glued, and the
            stethoscope works with the insert removed.
          </p>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="band-black" id="specs">
  <div class="wrap">
    <div class="viewer">
      <div class="viewer__text">
        <p class="eyebrow">Turn it over</p>
        <h2>The insert, not the stethoscope around it.</h2>
        <p>
          The part that replaced the back plate, on its own: the threaded collar, the machined
          base with the 3 mm port, the cell and boards, the polymer lid with the LED ring.
          Drag to rotate: this is the model the stills are rendered from.
        </p>
        <ul class="spec-list">
          <li><span>Collar</span><span>38.9 mm, threads in 44-48 mm</span></li>
          <li><span>Port</span><span>3 mm, aligned to the cup</span></li>
          <li><span>Depth</span><span>14 mm behind the back plate</span></li>
        </ul>
      </div>
      <div class="viewer__frame">
        <iframe src="studio/stage.html?embed=1&view=unit&hide=stock" title="The insert, rotatable" loading="lazy"></iframe>
        <p class="viewer__hint">Drag to rotate · revision D</p>
      </div>
    </div>
  </div>
</section>

<section class="band-black">
  <div class="wrap">
    <div class="head reveal">
      <div>
        <p class="eyebrow">Specification</p>
        <h2>What is inside<br>the <em>housing</em>.</h2>
      </div>
      <p class="lede">
        Third printed revision. Dimensions, radio and audio chain are fixed; tooling and
        battery certification are the next engineering step.
      </p>
    </div>

    <div class="split split--top">
      <table class="table">
        <thead><tr><th>Mechanical</th><th></th></tr></thead>
        <tbody>
          <tr><td>Seat diameter</td><td>38.9 mm</td></tr>
          <tr><td>Fits chestpieces</td><td>44–48 mm</td></tr>
          <tr><td>Depth behind back plate</td><td>14 mm</td></tr>
          <tr><td>Mass</td><td>45 g</td></tr>
          <tr><td>Sealing</td><td>Silicone gasket, IPX4</td></tr>
          <tr><td>Acoustic port</td><td>3 mm, aligned to the cup</td></tr>
          <tr><td>Assembly</td><td>Threaded collar, no adhesive</td></tr>
        </tbody>
      </table>
      <table class="table">
        <thead><tr><th>Electrical</th><th></th></tr></thead>
        <tbody>
          <tr><td>Microphones</td><td>2 × TDK ICS-43434</td></tr>
          <tr><td>Audio</td><td>24-bit, 20 Hz – 2 kHz</td></tr>
          <tr><td>Radio</td><td>nRF52840 · Bluetooth 5</td></tr>
          <tr><td>Storage</td><td>16 MB, offline ring buffer</td></tr>
          <tr><td>Battery</td><td>300 mAh Li-Po, USB-C</td></tr>
          <tr><td>Runtime</td><td>~20 h streaming, ~100 exams</td></tr>
          <tr><td>Board</td><td>38.9 mm, four layers</td></tr>
        </tbody>
      </table>
    </div>

    <div class="spec2">
      <div>
        <span class="spec2__k">Room rejection, two capsules</span>
        <span class="spec2__v">6.0 dB</span>
        <p>
          Simulated in <code>research/noise_rejection.py</code>: room noise at 0.72 coherence
          between the port capsule and the sealed reference, 4 dB of heart-sound leakage into
          the reference, removed by a normalised LMS over 48 taps. Twenty trials, spread 0.1 dB.
          A bench figure with a real chestpiece will replace it, and will be published with the
          rig it was measured on.
        </p>
      </div>
      <div>
        <span class="spec2__k">Streaming rate</span>
        <span class="spec2__v">358 kbit/s</span>
        <p>
          16 kHz, 16-bit mono, 20 ms packets, 40 per cent BLE overhead. Arithmetic from the
          format, not a measurement: the nRF52840 link has the headroom, and the number that
          matters for the battery is the 15 mA average, which comes from the 300 mAh cell over
          a 20 h session.
        </p>
      </div>
    </div>
  </div>
</section>

<section id="app">
  <div class="wrap">
    <div class="head reveal">
      <div>
        <p class="eyebrow">Companion app</p>
        <h2>Record, read, keep,<br>or <em>refuse</em>.</h2>
      </div>
      <p class="lede">
        Four screens, all of them working. Press record. Then switch the contact to loose and
        press it again — that is the state that matters.
      </p>
    </div>

    <div class="appdemo">
      <div class="phone reveal" data-app>
        <div class="phone__notch"></div>
        <div class="phone__screen">
          <div class="app-head">
            <span class="app-title">Heartware</span>
            <div class="app-h" id="app-title">New examination</div>
          </div>

          <div class="app-body" data-panel="record">
            <div class="wavebox">
              <canvas data-wave aria-label="Live waveform"></canvas>
              <div class="wlabel"><span>Port</span><span id="contact-label">23 dB SNR</span></div>
            </div>

            <div class="app-row">
              <div><b>Contact</b><span>chestpiece on skin</span></div>
              <button class="app-chip" id="contact-toggle" aria-pressed="false">Good contact</button>
            </div>

            <div id="record-result" hidden>
              <div class="app-note" id="res-card">
                <b id="res-title">—</b>
                <div style="margin-top:.4rem">
                  Site <b id="res-site">—</b> · Band <b id="res-band">—</b> · Quality
                  <b id="res-quality">—</b>
                </div>
                <div class="tiny" style="margin-top:.3rem"><span id="res-note">—</span></div>
              </div>
              <button class="app-btn" id="save-exam">Save to record</button>
            </div>

            <button class="app-btn" id="record-cta">Record</button>
            <p class="tiny" style="margin-top:.7rem">
              Interface demo. Readings are generated by the model on this page — not a patient.
            </p>
          </div>

          <div class="app-body" data-panel="findings" hidden>
            <p class="tiny" style="margin-bottom:.5rem">
              <b id="findings-count">0</b> findings in this session
            </p>
            <div id="findings-list"></div>
            <p class="tiny" style="margin-top:.8rem">
              A finding carries its site, its band, its likelihood and its quality. Without all
              four it is not shown.
            </p>
          </div>

          <div class="app-body" data-panel="records" hidden>
            <div id="records-list"></div>
            <div id="record-detail" hidden>
              <div class="app-note" style="margin-top:.8rem">
                <b id="detail-title">—</b>
                <div style="margin-top:.35rem">
                  Site <b id="detail-site">—</b> · Quality <b id="detail-quality">—</b>
                </div>
                <div class="tiny" style="margin-top:.3rem" id="detail-finding">—</div>
              </div>
            </div>
            <p class="tiny" style="margin-top:.8rem">
              Stored on the phone, timestamped, exportable. No patient identifiers.
            </p>
          </div>

          <div class="app-body" data-panel="settings" hidden>
            <div class="app-row"><div><b>Battery</b><span>USB-C</span></div><span class="app-chip">84%</span></div>
            <div class="app-row"><div><b>Firmware</b><span>nRF52840</span></div><span class="app-chip">0.9.3</span></div>
            <div class="app-row"><div><b>Microphones</b><span>port + reference</span></div><span class="app-chip">both live</span></div>
            <div class="app-row"><div><b>Bandwidth</b><span>20 Hz – 2 kHz</span></div><span class="app-chip">24-bit</span></div>
            <div class="app-row"><div><b>Export</b><span>WAV + JSON</span></div><span class="app-chip">ready</span></div>
            <p class="tiny" style="margin-top:.9rem">
              Prototype firmware. Not a certified medical device.
            </p>
          </div>

          <nav class="app-nav" aria-label="App">
            <button data-tab="record" aria-selected="true">
              <svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="7"/></svg>Record
            </button>
            <button data-tab="findings" aria-selected="false">
              <svg viewBox="0 0 24 24"><path d="M4 16l4-5 3 3 4-7 5 9"/></svg>Findings
            </button>
            <button data-tab="records" aria-selected="false">
              <svg viewBox="0 0 24 24"><path d="M5 5h14v14H5z"/><path d="M9 9h6M9 13h6"/></svg>Records
            </button>
            <button data-tab="settings" aria-selected="false">
              <svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="3"/><path d="M12 3v3M12 18v3M3 12h3M18 12h3"/></svg>Device
            </button>
          </nav>
        </div>
      </div>

      <div class="stack">
        <div class="card">
          <span class="card__num">REFUSAL</span>
          <h3>No reading is a reading.</h3>
          <p>
            When contact is lost the app does not lower its confidence and carry on. It returns
            nothing and asks for another recording, because the failure that hurts a patient is
            a confident normal.
          </p>
        </div>
        <p style="margin-top:1.6rem"><a class="btn btn--solid" href="app.html">Open the app &rarr;</a></p>
        <div class="card">
          <span class="card__num">RECORD</span>
          <h3>Every examination is evidence later.</h3>
          <p>
            Site, timestamp, quality and waveform are stored on the phone with no patient
            identifiers, and export as WAV and JSON — so a specialist can second-read the actual
            sound rather than a description of it.
          </p>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="band-warm">
  <div class="wrap">
    <div class="head reveal">
      <div>
        <p class="eyebrow">Cost</p>
        <h2>What it costs,<br>and what it <em>replaces</em>.</h2>
      </div>
      <p class="lede">
        A price with no comparator is a number. These comparators are list prices for
        instruments that require replacing the stethoscope a clinic already owns.
      </p>
    </div>

    <div class="compare reveal">
      <div class="compare__row compare__row--us">
        <div class="compare__name">Heartware insert<small>parts, at 500 units</small></div>
        <div class="compare__bar"><span style="width:7.6%"></span></div>
        <div class="compare__price">$38.25</div>
      </div>
      <div class="compare__row">
        <div class="compare__name">Eko CORE 300<small>digital stethoscope</small></div>
        <div class="compare__bar"><span style="width:39.8%"></span></div>
        <div class="compare__price">$199</div>
      </div>
      <div class="compare__row">
        <div class="compare__name">3M Littmann CORE<small>digital stethoscope</small></div>
        <div class="compare__bar"><span style="width:75.8%"></span></div>
        <div class="compare__price">$379</div>
      </div>
      <div class="compare__row">
        <div class="compare__name">Eko CORE 500<small>digital stethoscope</small></div>
        <div class="compare__bar"><span style="width:89.8%"></span></div>
        <div class="compare__price">$449</div>
      </div>
      <div class="compare__row">
        <div class="compare__name">Littmann 3200<small>discontinued</small></div>
        <div class="compare__bar"><span style="width:97%"></span></div>
        <div class="compare__price">$485</div>
      </div>
    </div>

    <p class="tiny" style="margin-top:1.4rem;max-width:60ch">
      Component cost from the bill of materials at 500 units. Target list price is $59, sold
      through distributors and directly to pilot sites. No consumables, no per-exam fee.
    </p>
  </div>
</section>
"""

# --------------------------------------------------------------------------- #
# Clinical
# --------------------------------------------------------------------------- #
CLINICAL = f"""
<section class="page-head">
  <div class="wrap">
    <p class="eyebrow">Clinical impact</p>
    <h1>Designed for the diversity<br>of the human body. Built for<br>wherever care <em>happens</em>.</h1>
    <p class="lede">
      A stethoscope is the most widely distributed diagnostic instrument in medicine. It is
      also the one whose accuracy depends most on the body in front of it.
    </p>
  </div>
</section>

<section style="padding-top:0">
  <div class="wrap">
    <div class="stories">
      <div class="story reveal">
        {icon_bodies()}
        <h3>Different anatomies</h3>
        <p>
          The published auscultation figure — 44% of significant valve disease detected in
          patients over 65 — was found to be useful only below a BMI of 25. Above it, the
          authors call auscultation a poor screen. That is not a failure of attention. It is
          a transfer function that nobody was correcting.
        </p>
      </div>
      <div class="story reveal">
        {icon_age()}
        <h3>Different stages of life</h3>
        <p>
          Age thickens and stiffens the wall and lowers its resonance, at the same time as the
          murmurs worth hearing become quieter and the lungs become harder to clear. A
          correction that is estimated per recording follows the body as it changes, rather
          than a fixed filter tuned on young chests.
        </p>
      </div>
      <div class="story reveal">
        {icon_places()}
        <h3>Different healthcare environments</h3>
        <p>
          Rural clinics, community health centres, nursing homes and resource-constrained
          hospitals share one constraint: the stethoscope is what is in the room. A $59 part
          with no consumables and no capital equipment fits a budget line that already exists.
        </p>
      </div>
      <div class="story reveal">
        {icon_remote()}
        <h3>Different ways of receiving care</h3>
        <p>
          An examination can be recorded, stored and shared, so a frontline worker can send a
          specialist the sound itself rather than a description of it. The same record supports
          review between appointments — the part of care where a murmur is usually lost.
        </p>
      </div>
    </div>
  </div>
</section>

<section class="band-cream">
  <div class="wrap">
    <div class="split split--top">
      <div class="stack">
        <p class="eyebrow">Where it is used</p>
        <h2 style="max-width:16ch">First contact, not the echo lab.</h2>
        <p>
          The people who benefit first are the ones who examine a chest in ten minutes:
          primary care clinicians, community health workers, nurses in long-term care, and the
          patients in front of them.
        </p>
        <p>
          Three things change. The reading arrives corrected, so the same murmur is
          comparable across bodies. The decision happens at first contact, rather than
          spending a referral to find out whether a referral was needed. And the examination
          becomes a record that can be second-read and trended.
        </p>
      </div>
      <div class="stack">
        <div class="card">
          <span class="card__num">THE ENCOUNTER</span>
          <h3>Five minutes, once per stethoscope.</h3>
          <p>
            Thread the collar, seat the insert, confirm both microphones in the app. The
            instrument keeps its weight, its stem and its acoustic path, which is the reason a
            clinician will actually carry it.
          </p>
        </div>
        <div class="card">
          <span class="card__num">THE RECORD</span>
          <h3>Site, timestamp, quality, waveform.</h3>
          <p>
            Stored locally, exported as WAV and JSON. A cardiologist can review the sound, not
            a summary of it — which is also the only honest way to build a validation dataset.
          </p>
        </div>
      </div>
    </div>
  </div>
</section>

<section>
  <div class="wrap">
    <div class="head reveal">
      <div>
        <p class="eyebrow">Clinical advisors</p>
        <h2>Reviewed by people who<br>examine patients for a <em>living</em>.</h2>
      </div>
      <p class="lede">
        The findings language, the site of the recording and the refusal threshold are
        reviewed by clinicians rather than written by engineers.
      </p>
    </div>
    <div class="people">
      <div class="person reveal">
        <h4>Dr. He Huan</h4>
        <span class="role">Clinical advisor</span>
        <p>Reviews the findings language and the recording protocol; the app's wording is written to read like a clinical note.</p>
      </div>
      <div class="person reveal">
        <h4>Dr. Yu Dongping</h4>
        <span class="role">Clinical advisor</span>
        <p>Reviews the site-of-recording taxonomy and the interface, including what the app should refuse to report.</p>
      </div>
      <div class="person reveal">
        <h4>Jiahe Wang</h4>
        <span class="role">Clinical protocol · MLPAO MLA/T</span>
        <p>Owns how a recording is taken — from which site, at what contact pressure — and runs the recording sessions.</p>
      </div>
    </div>
  </div>
</section>

<section class="band-warm">
  <div class="wrap">
    <div class="cta reveal">
      <div>
        <h2>A pilot is one protocol and one room.</h2>
        <p>
          We are looking for a site that already performs echocardiography and would run paired
          recordings — corrected and uncorrected — on the same patients. That study is the
          difference between an engineering record and a clinical claim.
        </p>
      </div>
      <div class="cta__actions">
        <a class="btn btn--light" href="partnerships.html">How a pilot works</a>
        <a class="btn btn--ghost" href="contact.html">Start a conversation</a>
      </div>
    </div>
  </div>
</section>
"""

# --------------------------------------------------------------------------- #
# Evidence
# --------------------------------------------------------------------------- #
EVIDENCE = f"""
<section class="page-head">
  <div class="wrap">
    <p class="eyebrow"><b>03</b> Evidence</p>
    <h1>Every number, and<br>where it comes from.</h1>
    <p class="lede">
      Six results, each one reproduced by a script in this repository. Run them and you get
      the same figures, to the digit, on your own machine.
    </p>
  </div>
</section>

<section style="padding-top:0">
  <div class="wrap">
    <div class="index-nav reveal">
      <a href="#recovery"><span>01</span><b>Recovering the wall</b></a>
      <a href="#body"><span>02</span><b>Removing the body dependence</b></a>
      <a href="#ablation"><span>03</span><b>What does the work</b></a>
      <a href="#robust"><span>04</span><b>When the model is wrong</b></a>
    </div>
  </div>
</section>

<section id="recovery" style="padding-top:1rem">
  <div class="wrap">
    <div class="head reveal">
      <div>
        <p class="eyebrow">01 — Recovery</p>
        <h2>3.7 mm, without<br>being <em>told</em>.</h2>
      </div>
      <p class="lede">
        600 synthetic subjects, walls from 9 to 45 mm, murmur present in half. The estimator
        sees one three-second recording and nothing else.
      </p>
    </div>
    <div class="split split--top">
      <figure class="figure reveal">
        <img src="assets/figures/fig-02-identity.png" alt="Estimated against true chest-wall thickness for 320 subjects, clustered along the identity line." loading="lazy">
        <figcaption><b>FIG 02</b> Estimated against true thickness. RMS error 3.7 mm; 86% within 5 mm; correlation 0.75.</figcaption>
      </figure>
      <div class="stack">
        <p>
          The fit allows an arbitrary gain, tilt and curvature for the unknown source spectrum
          — otherwise the estimator would be reading the heart, not the wall — and the
          residual shape then identifies the path.
        </p>
        <p>
          The bias is +1.5 mm, meaning the method tends to over-estimate by about the width of
          a fingertip. That matters for the correction: over-estimating over-corrects, which
          is why the inverse is regularised rather than exact.
        </p>
        <div class="note-box">
          <b>Read this correctly.</b> This validates the arithmetic of the inversion. It says
          nothing about whether a corrected recording finds disease an uncorrected one misses.
        </div>
      </div>
    </div>
  </div>
</section>

<section id="body" class="band-cream">
  <div class="wrap">
    <div class="head reveal">
      <div>
        <p class="eyebrow">02 — Body dependence</p>
        <h2>The same murmur,<br>the same <em>level</em>.</h2>
      </div>
      <p class="lede">
        Split by body habitus. Before correction the murmur falls away as the wall thickens;
        after correction the three levels sit within a quarter of a decibel.
      </p>
    </div>
    <div class="split split--top">
      <figure class="figure reveal">
        <img src="assets/figures/fig-03-body.png" alt="Murmur level by BMI group: falling with body size when uncorrected, flat when corrected." loading="lazy">
        <figcaption><b>FIG 03</b> Murmur level in dB against the patient's own S1/S2. Spread 1.73 dB before, 0.25 dB after.</figcaption>
      </figure>
      <figure class="figure reveal">
        <img src="assets/figures/fig-05-waveform.png" alt="The 150-400 Hz envelope of one recording, before and after correction, on the same scale." loading="lazy">
        <figcaption><b>FIG 05</b> One subject, 30 mm wall: the envelope of the murmur band on the same scale. +4.5 dB.</figcaption>
      </figure>
    </div>
    <p class="tiny" style="margin-top:1.6rem;max-width:66ch">
      The measure is a ratio against the patient's own valve closures, so it cannot be
      improved by pressing harder or turning up the volume. Body groups are thirds of a
      synthetic BMI distribution, mean 22.2, 29.0 and 36.1.
    </p>
  </div>
</section>

<section id="ablation">
  <div class="wrap">
    <div class="head reveal">
      <div>
        <p class="eyebrow">03 — Ablation</p>
        <h2>The obvious shortcut<br>does not <em>work</em>.</h2>
      </div>
      <p class="lede">
        Four ways to build the same correction. Assuming one wall thickness for every patient
        — the cheap version — leaves the body dependence almost exactly where it was.
      </p>
    </div>
    <div class="split split--top">
      <figure class="figure reveal">
        <img src="assets/figures/fig-04-ablation.png" alt="Bar chart: spread in murmur level for four correction strategies." loading="lazy">
        <figcaption><b>FIG 04</b> Spread in murmur level across body types. Only the per-record estimate closes it.</figcaption>
      </figure>
      <div class="stack">
        <p>
          <b>One fixed thickness</b> gains 1.82 dB on average but leaves 1.69 dB of spread:
          it lifts everyone, so the difference between bodies survives.
        </p>
        <p>
          <b>Ignoring the resonance</b> — modelling absorption only — does better than a fixed
          thickness but still leaves 0.60 dB, because the resonance is where the thickness
          information lives.
        </p>
        <p>
          <b>Estimating per recording</b> is the only variant that reduces the spread to
          0.25 dB, at a mean gain of 1.93 dB.
        </p>
      </div>
    </div>
  </div>
</section>

<section id="robust" class="band-cream">
  <div class="wrap">
    <div class="head reveal">
      <div>
        <p class="eyebrow">04 — Robustness</p>
        <h2>What happens when<br>the physics is <em>wrong</em>.</h2>
      </div>
      <p class="lede">
        The generator and the estimator were made to disagree about absorption and about the
        resonance. The correction survives all six, which is the useful property of a
        physical model: it degrades, it does not collapse.
      </p>
    </div>
    <div class="split split--top">
      <figure class="figure reveal">
        <img src="assets/figures/fig-06-robustness.png" alt="Murmur gain under six deliberate model errors, all between 1.5 and 2.8 dB." loading="lazy">
        <figcaption><b>FIG 06</b> Gain with the model deliberately wrong by 15–30%. Range 1.75–2.80 dB against 1.93 dB exact.</figcaption>
      </figure>
      <div class="stack">
        <table class="table">
          <thead><tr><th>Deliberate error</th><th>Thickness RMS</th><th>Gain</th></tr></thead>
          <tbody>
            <tr><td>Absorption +20%</td><td>3.20 mm</td><td>1.92 dB</td></tr>
            <tr><td>Absorption −20 %</td><td>4.09 mm</td><td>2.17 dB</td></tr>
            <tr><td>Exponent +15 %</td><td>4.61 mm</td><td>2.30 dB</td></tr>
            <tr><td>Exponent −15 %</td><td>4.09 mm</td><td>2.17 dB</td></tr>
            <tr><td>Resonance Q −30 %</td><td>6.58 mm</td><td>2.80 dB</td></tr>
            <tr><td>Resonance Q +30 %</td><td>3.39 mm</td><td>1.75 dB</td></tr>
          </tbody>
        </table>
        <p class="tiny">150 subjects per row, generator and estimator disagreeing by the stated amount.</p>
      </div>
    </div>
  </div>
</section>

<section>
  <div class="wrap">
    <div class="head reveal">
      <div>
        <p class="eyebrow">Claims ledger</p>
        <h2>Every claim, and<br>what stands behind <em>it</em>.</h2>
      </div>
      <p class="lede">
        If a claim is not in this table it is not made anywhere on the site. Where the evidence
        is missing, the row says so.
      </p>
    </div>

    <div class="ledger">
      <div class="ledger__row">
        <span class="ledger__mark">✓</span>
        <div class="ledger__claim">The chest wall behaves as a low-pass filter whose resonance falls with thickness</div>
        <div class="ledger__ev">Physical model, four thicknesses, Fig 01</div>
        <div class="ledger__state state-yes">Supported</div>
      </div>
      <div class="ledger__row">
        <span class="ledger__mark">✓</span>
        <div class="ledger__claim">Wall thickness is recoverable from the recording alone</div>
        <div class="ledger__ev">In-silico, n = 600, RMS 3.7 mm</div>
        <div class="ledger__state state-yes">Supported</div>
      </div>
      <div class="ledger__row">
        <span class="ledger__mark">✓</span>
        <div class="ledger__claim">Per-record correction removes the body dependence of murmur level</div>
        <div class="ledger__ev">In-silico, n = 600, 1.73 → 0.25 dB</div>
        <div class="ledger__state state-yes">Supported</div>
      </div>
      <div class="ledger__row">
        <span class="ledger__mark">✓</span>
        <div class="ledger__claim">The insert seats in 44–48 mm chestpieces and the instrument still works without it</div>
        <div class="ledger__ev">Three printed revisions, fitted by hand</div>
        <div class="ledger__state state-yes">Measured</div>
      </div>
      <div class="ledger__row">
        <span class="ledger__mark">~</span>
        <div class="ledger__claim">The second microphone cancels room noise</div>
        <div class="ledger__ev">Architecture built; dB figure not yet measured</div>
        <div class="ledger__state state-part">Partial</div>
      </div>
      <div class="ledger__row">
        <span class="ledger__mark">~</span>
        <div class="ledger__claim">The method survives error in the physical model</div>
        <div class="ledger__ev">In-silico, six deliberate errors, Fig 06</div>
        <div class="ledger__state state-part">Partial</div>
      </div>
      <div class="ledger__row">
        <span class="ledger__mark">×</span>
        <div class="ledger__claim">A corrected recording finds valve disease an uncorrected one misses</div>
        <div class="ledger__ev">Requires paired recordings with echocardiography</div>
        <div class="ledger__state state-no">Not yet tested</div>
      </div>
      <div class="ledger__row">
        <span class="ledger__mark">×</span>
        <div class="ledger__claim">Sensitivity, specificity or AUC against echo</div>
        <div class="ledger__ev">Not claimed anywhere on this site</div>
        <div class="ledger__state state-no">Not claimed</div>
      </div>
    </div>
  </div>
</section>

<section class="band-navy">
  <div class="wrap">
    <div class="head reveal">
      <div>
        <p class="eyebrow">Milestones</p>
        <h2 style="color:#fff">Done, under way,<br>and <em style="color:#FFB3BE">next</em>.</h2>
      </div>
      <p class="lede">
        Three revisions shipped, a fourth in tooling, and one study between the design and
        the shelf.
      </p>
    </div>

    <div class="timeline">
      <div class="tl">
        <p class="tl__when">Completed</p>
        <h4 style="color:#fff">The device exists</h4>
        <ul>
          <li>Three printed housing revisions, 38.9 mm seat</li>
          <li>Fitted to 44–48 mm single and double heads</li>
          <li>Dual-microphone chain capturing at 24-bit</li>
          <li>Firmware streaming over Bluetooth 5 with a ring buffer</li>
          <li>App that records, segments, corrects and gates</li>
          <li>More than 100 people have handled the unit</li>
        </ul>
      </div>
      <div class="tl">
        <p class="tl__when">Under way</p>
        <h4 style="color:#fff">The measurements</h4>
        <ul>
          <li>Bench measurement of two-microphone cancellation</li>
          <li>Contact-pressure protocol and repeatability across operators</li>
          <li>Recording sessions across body types</li>
          <li>Photograph of the insert seated in a real chestpiece</li>
        </ul>
      </div>
      <div class="tl tl--future">
        <p class="tl__when">Next</p>
        <h4 style="color:#fff">The clinical claim</h4>
        <ul>
          <li>Paired recording and echo study at a partner site</li>
          <li>Regulatory pathway: 510(k), exempt, or software-only</li>
          <li>Injection-mould tooling and a contract manufacturer</li>
          <li>Pilot units at $59 with the app included</li>
        </ul>
      </div>
    </div>
  </div>
</section>

<section id="method">
  <div class="wrap">
    <div class="head reveal">
      <div>
        <p class="eyebrow">Method</p>
        <h2>Check the <em>arithmetic</em>.</h2>
      </div>
      <p class="lede">
        The model, the estimator and the figures are one Python file and one plotting file.
        Run them and every number on this page regenerates.
      </p>
    </div>
    <div class="split split--top">
      <div class="stack">
        <table class="table">
          <tbody>
            <tr><td>Model and experiment</td><td><code>research/thoracic_model.py</code></td></tr>
            <tr><td>Figures</td><td><code>research/make_figures.py</code></td></tr>
            <tr><td>Output</td><td><code>research/results.json</code></td></tr>
            <tr><td>Seed</td><td>20261106 · reproducible</td></tr>
          </tbody>
        </table>
      </div>
      <div class="stack">
        <p class="small">
          The experiment generates a heart sound with noise, passes it through a modelled
          chest wall of known thickness, adds a room, and then hides the thickness from the
          estimator. Every reported number is computed from that pipeline, not written down
          by hand.
        </p>
        <div class="note-box">
          <b>The next run is the clinical one.</b> Paired recordings with echocardiography in
          a site that already reads echoes. The protocol, the capture sheet and the analysis
          ship with the model, so the day the first twenty pairs exist the result is a table,
          not a start-up.
        </div>
      </div>
    </div>
  </div>
</section>
"""

# --------------------------------------------------------------------------- #
# Partnerships
# --------------------------------------------------------------------------- #
PARTNER = """
<section class="page-head">
  <div class="wrap">
    <p class="eyebrow">Partnerships</p>
    <h1>Three ways to<br>work with <em>us</em>.</h1>
    <p class="lede">
      A pilot site, a distribution partner, or a manufacturer who wants the insert as a factory
      variant. Each is a different conversation and each has a different next step.
    </p>
  </div>
</section>

<section style="padding-top:0">
  <div class="wrap">
    <div class="cards">
      <div class="card reveal">
        <span class="card__num">01 · CLINICAL</span>
        <h3>Run the study</h3>
        <p>
          A site that already performs echocardiography records the same patient twice —
          corrected and uncorrected — and keeps the echo report. We supply the inserts, the
          protocol and the analysis; the site supplies the room and the reads.
        </p>
        <p class="tiny">Needs: one clinician lead, an echo list, and a data agreement.</p>
      </div>
      <div class="card reveal">
        <span class="card__num">02 · DISTRIBUTION</span>
        <h3>Sell the part</h3>
        <p>
          Regional distributors and group purchasing organisations already sell stethoscopes
          and gloves into the same rooms. The insert is a consumable decision at $59 rather
          than a capital request, with no per-exam fee to explain.
        </p>
        <p class="tiny">Needs: a pilot reference site and a price list.</p>
      </div>
      <div class="card reveal">
        <span class="card__num">03 · OEM</span>
        <h3>Ship it as a variant</h3>
        <p>
          Because the insert replaces a back plate rather than changing the instrument, a
          stethoscope manufacturer can offer it without redesigning a head. A royalty per unit
          is the only path to six-figure volume without a salesforce.
        </p>
        <p class="tiny">Needs: a tooling partner and a licensing term sheet.</p>
      </div>
    </div>
  </div>
</section>

<section class="band-cream">
  <div class="wrap">
    <div class="head reveal">
      <div>
        <p class="eyebrow">The institutional case</p>
        <h2>What a director needs<br>to <em>know</em>.</h2>
      </div>
      <p class="lede">
        Cost, compatibility, purpose, implementation and how to arrange a pilot — on one page,
        without hunting.
      </p>
    </div>

    <div class="split split--top">
      <table class="table">
        <tbody>
          <tr><td>Unit cost</td><td>$38.25 in parts at 500 units</td></tr>
          <tr><td>Target price</td><td>$59, app included</td></tr>
          <tr><td>Consumables</td><td>None</td></tr>
          <tr><td>Capital equipment</td><td>None — fits the stethoscope you own</td></tr>
          <tr><td>Compatibility</td><td>44–48 mm single and double heads</td></tr>
          <tr><td>Installation</td><td>Five minutes, threaded collar</td></tr>
          <tr><td>Training</td><td>One session; the instrument feels the same</td></tr>
          <tr><td>Data</td><td>On the phone; WAV and JSON export; no identifiers</td></tr>
        </tbody>
      </table>
      <div class="stack">
        <h3>What a pilot involves</h3>
        <p class="small">
          Twenty to forty patients who are already scheduled for an echocardiogram. Each is
          recorded with and without correction, blinded to the echo result. The analysis
          reports whether the correction changes the finding, and how often the app refuses to
          answer at all — both outcomes are results, and the second is the one that protects
          patients.
        </p>
        <div class="note-box">
          <b>What we bring.</b> Inserts for the site, the recording protocol, the analysis and
          the write-up. <b>What we ask.</b> A named clinical lead and access to the echo report.
        </div>
      </div>
    </div>
  </div>
</section>

<section>
  <div class="wrap">
    <div class="head reveal">
      <div>
        <p class="eyebrow">Commercial</p>
        <h2>Three revenue lines,<br>in order of <span class="accent">realism</span>.</h2>
      </div>
      <p class="lede">A device has to be worth buying once before anything recurring is credible, so the first line is the only one that matters this year.</p>
    </div>
    <div class="cards">
      <div class="card reveal">
        <span class="card__num">YEAR 1–2</span>
        <h3>Units</h3>
        <p>
          Sold through medical distributors and directly to pilot sites, at $59 with the app
          included. A clinic already buys stethoscopes; this is a line on an existing order.
        </p>
      </div>
      <div class="card reveal">
        <span class="card__num">YEAR 2+</span>
        <h3>Clinic tier</h3>
        <p>
          Multi-user records, trend views and EMR export, sold per site rather than per exam.
          Per-exam pricing is what stops a screening tool being used in a ten-minute visit.
        </p>
      </div>
      <div class="card reveal">
        <span class="card__num">YEAR 3+</span>
        <h3>OEM licence</h3>
        <p>
          A royalty per unit with a stethoscope manufacturer shipping the insert as a factory
          variant. This is where the volume is, and it is why the design fits a stock head.
        </p>
      </div>
    </div>

    <div class="note-box" style="margin-top:2.4rem;max-width:70ch">
      <b>The first hundred people who held it asked for the same thing:</b> proof that the
      correction changes what a clinician hears. That is the pilot, and it is the only thing
      standing between the design and the shelf.
    </div>
  </div>
</section>

<section class="band-warm">
  <div class="wrap">
    <div class="cta reveal">
      <div>
        <h2>Start with the study, not the purchase order.</h2>
        <p>
          If you run a clinic, a trial or a production line, the useful first conversation is
          about whether the correction changes what you hear — not about volume.
        </p>
      </div>
      <div class="cta__actions">
        <a class="btn btn--light" href="contact.html">Request a pilot</a>
        <a class="btn btn--ghost" href="evidence.html">Read the evidence first</a>
      </div>
    </div>
  </div>
</section>
"""

# --------------------------------------------------------------------------- #
# About
# --------------------------------------------------------------------------- #
ABOUT = """
<section class="page-head">
  <div class="wrap">
    <p class="eyebrow">About</p>
    <h1>The instrument should<br>adapt to the body,<br>not the <em>reverse</em>.</h1>
    <p class="lede">
      Heartware began with a simple observation: the same murmur is described differently in
      different bodies, and the difference is in the instrument, not the ear.
    </p>
  </div>
</section>

<section style="padding-top:0">
  <div class="wrap">
    <div class="split split--top">
      <div class="stack">
        <p>
          Every commercial answer to this problem is a new instrument. A clinic that already
          owns a drawer of stethoscopes does not buy a fourth for a nurse who has ten minutes.
          So the design started from the constraint instead: change the back plate, keep
          everything else.
        </p>
        <p>
          The second decision was to make the correction arithmetic rather than learned. A
          model with no trained parameters cannot encode the demographics of whoever happened
          to be in a dataset, and a reviewer can check it with a pencil. In a field where
          algorithmic bias is a stated concern, that is the whole point.
        </p>
        <p>
          The third was the refusal. The strongest feedback from the clinicians who handled the
          prototype was that a false reassurance is worse than no reading, so the app returns
          nothing below its quality threshold and asks for another recording.
        </p>
      </div>
      <div class="stack">
        <div class="card">
          <span class="card__num">STAGE</span>
          <h3>Prototype</h3>
          <p>
            A working insert, recordings from people, an app that returns gated findings.
            The design is at revision D and the next milestone is the paired study, which is
            what the pilot section is for.
          </p>
        </div>
        <div class="card">
          <span class="card__num">WHAT WE NEED</span>
          <h3>A clinical site with echocardiography</h3>
          <p>
            Validation, regulatory advice, manufacturing tooling, and distribution into public
            systems. None of those is solved by money alone, which is why the ask is specific.
          </p>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="band-cream">
  <div class="wrap">
    <div class="head reveal">
      <div>
        <p class="eyebrow">Team</p>
        <h2>The people<br>who built it.</h2>
      </div>
      <p class="lede">
        Engineering, clinical protocol and review. Everyone on this list has handled the
        device or read the analysis.
      </p>
    </div>
    <div class="people">
      <div class="person reveal">
        <h4>Amy Wang</h4>
        <span class="role">Founder · system design</span>
        <p>Acoustic path, correction, app and the manufacturing envelope. Built the current insert and wrote the analysis that sets its error budget.</p>
      </div>
      <div class="person reveal">
        <h4>Jiahe Wang</h4>
        <span class="role">Co-founder · clinical protocol</span>
        <p>MLPAO-registered medical laboratory assistant/technician. Owns how a recording is taken and runs the recording sessions.</p>
      </div>
      <div class="person reveal">
        <h4>Manolis Kellis</h4>
        <span class="role">Advisor · MIT</span>
        <p>Professor of computational biology. Advises on signal and statistical methodology: what can be claimed from a recording, and what cannot.</p>
      </div>
      <div class="person reveal">
        <h4>Dr. He Huan</h4>
        <span class="role">Clinical advisor</span>
        <p>Reviews the findings language and the recording protocol so a reading reads like a clinical note.</p>
      </div>
      <div class="person reveal">
        <h4>Dr. Yu Dongping</h4>
        <span class="role">Clinical advisor</span>
        <p>Reviews the site-of-recording taxonomy and the interface, including what the app should refuse to report.</p>
      </div>
      <div class="person reveal">
        <h4>Grace Yu</h4>
        <span class="role">Advisor · interface</span>
        <p>Reviews the interface and the language of the findings with the clinician advisors.</p>
      </div>
    </div>
    <p class="tiny" style="margin-top:1.6rem;max-width:64ch">
      More than a hundred people — students, nurses, physicians and volunteers — have handled
      the unit or given structured feedback. Their input changed three things: the insert became
      a threaded retrofit rather than a clip, the findings moved from a single flag to a site
      plus a likelihood, and the app gained its refusal state.
    </p>
  </div>
</section>

<section>
  <div class="wrap">
    <div class="cta reveal">
      <div>
        <h2>Twenty to forty patients already booked for an echo is all we need to start.</h2>
        <p>
          The study is a paired recording: corrected and uncorrected, blinded, read against the
          cardiologist's report. Email the clinical lead and we will send the protocol and the
          two-page data agreement the same day.
        </p>
      </div>
      <div class="cta__actions">
        <a class="btn btn--light" href="contact.html">Get in touch</a>
        <a class="btn btn--ghost" href="evidence.html">The evidence</a>
      </div>
    </div>
  </div>
</section>
"""

# --------------------------------------------------------------------------- #
# Contact
# --------------------------------------------------------------------------- #
CONTACT = """
<section class="page-head">
  <div class="wrap">
    <p class="eyebrow">Contact</p>
    <h1>Tell us which<br>of the three you <em>are</em>.</h1>
    <p class="lede">
      A pilot site, a distributor, or a manufacturer. Each gets a different reply, so the
      first line of your email is the most useful thing in it.
    </p>
  </div>
</section>

<section style="padding-top:0">
  <div class="wrap">
    <div class="split split--top">
      <div class="stack">
        <table class="table">
          <tbody>
            <tr><td>Email</td><td><a href="mailto:hello@heart-ware.org">hello@heart-ware.org</a></td></tr>
            <tr><td>Pilot enquiries</td><td><a href="mailto:pilots@heart-ware.org">pilots@heart-ware.org</a></td></tr>
            <tr><td>Based in</td><td>Boston, Massachusetts</td></tr>
            <tr><td>Reply time</td><td>Within a week</td></tr>
          </tbody>
        </table>
        <div class="note-box">
          <b>Not a medical device.</b> The prototype is not certified for diagnostic use and
          must not be used to make clinical decisions. It is a research instrument.
        </div>
      </div>
      <div class="stack">
        <h3>If you run a clinic or a trial</h3>
        <p class="small">
          Tell us whether you have echocardiography on site, roughly how many murmurs you see a
          month, and who would be the clinical lead. That is enough to scope a pilot.
        </p>
        <h3>If you distribute</h3>
        <p class="small">
          Tell us which markets and which buying groups. We will send the specification, the
          price list and the pilot reference when there is one.
        </p>
        <h3>If you manufacture</h3>
        <p class="small">
          Tell us whether you mould housings for stethoscopes today. The insert is a back-plate
          variant, so the tooling conversation is smaller than it sounds.
        </p>
      </div>
    </div>
  </div>
</section>
"""



# --------------------------------------------------------------------------- #
# App
# --------------------------------------------------------------------------- #
APP_PAGE = """
<section class="page-head page-head--dark">
  <div class="wrap">
    <p class="eyebrow"><b>04</b> The app</p>
    <h1>Record. Correct.<br>Or refuse.</h1>
    <p class="lede">
      This is the companion app, running in this page. Open the microphone and it will show you
      what your own chest wall does to a heart sound; press the generated signal and it will
      run a generated grade 2 murmur through a modelled chest wall and correct it, without a patient in the room.
    </p>
  </div>
</section>

<section id="app" class="app-shell">
  <div class="wrap app-grid">
    <div class="app-panel">
      <div class="app-panel__head">
        <span class="app-tag">Live</span>
        <span class="app-hint">20-900 Hz · FFT 4096 · wavelet-free</span>
      </div>
      <canvas id="app-scope" class="app-scope"></canvas>
      <canvas id="app-spectrum" class="app-spectrum"></canvas>
      <div class="app-legend">
        <span><i class="k-grey"></i>As the chestpiece hears it</span>
        <span><i class="k-red"></i>Wall removed</span>
      </div>
    </div>

    <aside class="app-side">
      <div class="app-meter">
        <div class="app-meter__row"><b>Contact</b><span id="app-quality-val">0%</span></div>
        <div class="app-meter__track"><span id="app-quality"></span></div>
      </div>
      <div class="app-read">
        <div><span>Wall estimate</span><b id="app-wall">—</b></div>
        <div><span>Trained parameters</span><b>0</b></div>
      </div>
      <div id="app-verdict" class="app-verdict" data-state="idle">
        <h4>Waiting for contact</h4>
        <p>Press record and hold the chestpiece still.</p>
      </div>
      <div class="app-actions">
        <button id="app-record" class="btn btn--solid" type="button">Record 6 s</button>
        <button id="app-stop" class="btn btn--ghost" type="button" disabled>Stop</button>
        <button id="app-mic" class="btn btn--ghost" type="button">Open microphone</button>
        <button id="app-demo" class="btn btn--ghost" type="button">Generated signal</button>
      </div>
      <p id="app-note" class="app-note">Microphone audio never leaves the browser. Nothing is uploaded, stored or sent anywhere.</p>
      <div id="app-takes" class="app-takes"></div>
    </aside>
  </div>
</section>

<section>
  <div class="wrap split split--top">
    <div class="stack">
      <h2>What the four screens do.</h2>
      <p>
        <b>Record</b> captures six seconds and stores the waveform, the wall estimate and the
        quality score together, so a reading is never separated from the conditions that
        produced it. <b>Correct</b> divides the spectrum by the wall it just measured.
        <b>Keep</b> exports the take as WAV and JSON, so a second reader hears the same sound
        rather than a description of it. <b>Refuse</b> returns nothing below the contact
        threshold: a false reassurance is the failure that hurts a patient.
      </p>
      <p>
        The correction is the same arithmetic as the model in <code>research/</code>, at demo
        precision. There is no learned layer, so there is nothing in it to inherit a
        demographic from.
      </p>
    </div>
    <div class="stack">
      <h3>What runs where</h3>
      <ul class="spec-list">
        <li><span>Capture</span><span>Web Audio, 48 kHz mono</span></li>
        <li><span>Analysis</span><span>FFT 4096, three bands</span></li>
        <li><span>Gate</span><span>Contact &lt; 45% refuses</span></li>
        <li><span>Output</span><span>WAV + JSON</span></li>
        <li><span>Upload</span><span>None</span></li>
      </ul>
      <p class="smallprint">
        The firmware build adds the second microphone and the two-channel noise rejection.
        This page has one channel, so it shows the correction and the gate, not the
        differential front end.
      </p>
    </div>
  </div>
</section>
<script src="assets/js/app-demo.js" defer></script>
"""


if __name__ == "__main__":
    page("index.html", "A stethoscope insert that corrects for the chest wall",
         "Heartware is a modular insert that measures the chest wall from the recording and inverts it, so every body gives the same heart and lung signal.",
         "home", HOME)
    page("technology.html", "Technology", "Two microphones, two-channel noise rejection, and a physics-based thoracic correction.", "tech", TECH)
    page("product.html", "Product", "The insert, its drawings, its specification and the working app.", "product", PRODUCT)
    page("clinical.html", "Clinical impact", "Designed for the diversity of the human body, built for wherever care happens.", "clinical", CLINICAL)
    page("evidence.html", "Evidence", "What is measured, what is modelled, and what is not yet known.", "evidence", EVIDENCE)
    page("partnerships.html", "Partnerships", "Pilot, distribution and OEM licensing.", "partners", PARTNER)
    page("about.html", "About", "The team and the reasoning behind the design.", "about", ABOUT)
    page("contact.html", "Contact", "Pilot enquiries, distribution and manufacturing.", "contact", CONTACT)
    page("app.html", "The app", "The companion app running in the page: record, correct, keep or refuse.", "app", APP_PAGE)
