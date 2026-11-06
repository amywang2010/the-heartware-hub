# heart-ware.org

Static site for Heartware. No build step, no framework, no trackers. GitHub Pages
serves `main` at the repository root, with `CNAME` pointing heart-ware.org here.

## Layout

```
index.html              the page
404.html                not-found page
assets/css/site.css     all styles
assets/js/site.js       charts, reveals, tabs, the chest-wall demo
assets/js/hero3d.js     the three.js chestpiece in the hero
assets/vendor/          three.js r169 (module build) + RoomEnvironment
assets/img/             app captures (from the film), exploded view (SVG), poster
assets/film/            the 42.6 s film, 1280×720, no audio
```

## Editing the validation numbers

All three intervals come from `VALIDATION` at the top of `assets/js/site.js`.
Enter the confusion matrix there:

```js
counts: { tp: 0, fn: 0, tn: 0, fp: 0 },
```

When all four are numbers, every interval is recomputed from those counts in the
browser with the Wilson score method, the point estimate appears as a tick on each
bar, and the hard-coded `reported` values stay as the check. If the counts are
absent, the page shows the reported intervals only.

## Local preview

```
python -m http.server 8123
```

Then open <http://localhost:8123/>. The hero imports three.js as an ES module, so it
must be served over http rather than opened from disk.

## Honesty rules used on this page

- Every performance number is either a published result (cited, with DOI) or ours
  (labelled as validated on held-out recordings, not against echocardiography).
- The physics figures are labelled as a model, not a measurement.
- The device is described as a research prototype; no clearance is implied.
- Prices are manufacturer prices, with the date checked, and our figure is a
  component cost rather than a retail price.
