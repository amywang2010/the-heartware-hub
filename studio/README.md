# studio

The photographs and the product loop on the site are rendered here, from
`stage.html`, by `render.mjs`. Nothing is imported from the old `viz/` model in
`eigenpulse-cuff`; that model was rejected, so this is a separate build.

```bash
node studio/render.mjs stills   # five stills, PNG, into assets/img
node studio/render.mjs video    # 150 frames at 25 fps, h264, 6 s loop
```

Rendering needs a Chromium with WebGL. There is no GPU on this machine, so it
falls back to SwiftShader: about 40 s per still and about 6 minutes for the loop.
`node_modules` is a junction to `eigenpulse-cuff/viz/node_modules` because
Playwright is installed there; it is gitignored and must be recreated on a fresh
clone (`mklink /J heartware-hub\node_modules eigenpulse-cuff\viz\node_modules`).

## What the model is

Millimetres, 1 unit = 1 mm, camera at 1 unit = 1 cm. Stock parts: a 43.4 mm cup,
a moulded polymer rim, a polished reflector with a thin membrane over it, and an
angled stem with a 4.5 mm bore. Our parts: a threaded collar at the 38.9 mm
seat, an acoustic base carrying a 3 mm port, a microphone board with two
ICS-43434s and a sealed reference cavity, a 300 mAh cell, a logic board with the
nRF52840, and a lid with the LED ring and the etched mark.

## What failed on the way, so nobody repeats it

1. **The first render had no chestpiece.** `buildInstrument()` in the old model
   returns `{inst, head, ...}` and the head is *not* in `inst`; it was added to
   the scene separately. Framing the returned group produced a red tube with
   nothing on the end. This is why the studio is a fresh build.
2. **The rim lathe capped the whole face.** A profile that starts at `x = 0`
   closes over the diaphragm, so the head rendered as a black disc. Every ring
   profile now starts and ends at the same inner radius.
3. **The dome floated 20 mm above the head**, because its position was computed
   from a sphere-cap radius that had already been scaled. The diaphragm is now a
   lathe of a cosine arc, so its edge sits under the rim by construction.
4. **`membrane` at 94 % transmission with opacity 0.35 reads as smoked glass.**
   A stethoscope diaphragm is nearly invisible over a mirror; it is now 0.09
   opacity over a `roughness 0.035` reflector.
5. **The insert was modelled at 23 mm deep.** The specification says 14 mm. It is
   compressed to 14.3 mm and the exploded view spacing is computed from that.
6. **The first explode offsets were applied twice** to parts that were also in
   the index-based bands, which threw the cell and the lid out of the frame.

## What is still not a photograph

These are renders. They are not photographs of a physical prototype, because
there is no photographed prototype in the repository, and the site says
"rendered" in the captions where it matters. What is missing to make them look
photographed: a real HDRI captured in a studio (RoomEnvironment is synthetic and
the metal reads slightly flat), a depth-of-field pass (the corners are as sharp
as the centre), and surface imperfection maps (dust, machining marks, a used
diaphragm). Those three would close most of the remaining gap.

The loop is a turntable at 25 fps, 1280x720, 640 KB. It has no audio.
