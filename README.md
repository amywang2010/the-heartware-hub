# heart-ware.org

Static site for Heartware. No framework, no trackers. GitHub Pages serves `main`
at the repository root, with `CNAME` pointing heart-ware.org here.

## Pages

```
index.html          positioning, the measurement, the method, the proof strip
technology.html     capture → room rejection → correction → analysis → interface
product.html        drawings, specification, the working app demo, cost
clinical.html       the four patient stories, advisors
evidence.html       six figures, the claims ledger, milestones, method
partnerships.html   pilot, distribution, OEM, unit economics
about.html          reasoning and team
contact.html        who to write to, and what to say
404.html            not-found page
```

## Layout

```
assets/css/base.css     tokens, type, layout, header, footer
assets/css/pages.css    page components: pipeline, explorer, phone, ledger, timeline
assets/js/site.js       nav, reveals, tabs, counters
assets/js/explorer.js   the thoracic-correction demonstration
assets/js/app.js        the companion-app demonstration
assets/img/             the logo, in its original colours
assets/figures/         the six figures on the Evidence page
research/               the model, the experiment, the plotting code
tools/                  the page builder and the line artwork
```

## The numbers

Every figure on the Evidence page is produced by:

```bash
python research/thoracic_model.py     # writes research/results.json
python research/make_figures.py       # writes assets/figures/*.png
```

Nothing on the site is typed by hand from memory. If a number is not in
`research/results.json` or in the published reference it cites, it should not be
on a page. The claims ledger on `evidence.html` is the contract: if a claim is
not in that table, it is not made anywhere on the site.

The model validates the *arithmetic* of the inversion. It is not patient data and
supports no diagnostic claim. Sensitivity and specificity against echocardiography
require a paired-recording study that has not been run.

## Editing the pages

The eight pages share one shell (header, footer, fonts) and are generated from
`tools/pages.py` and `tools/build.py`:

```bash
cd tools && python pages.py
```

Editing the HTML directly also works, but re-running the builder overwrites it.
