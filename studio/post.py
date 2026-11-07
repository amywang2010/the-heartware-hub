"""
POST.PY -- the difference between a render and a photograph.

Three things a WebGL render does not have: depth of field, grain, and the
falloff of a real lens. Each still is rendered twice, once with its material
and once as linear depth, and this file uses the depth map to blur the parts of
the frame that are not on the focal plane, then adds grain and a vignette at the
size the site actually displays them.

    python studio/post.py
"""

from pathlib import Path
import numpy as np
from PIL import Image, ImageFilter

ROOT = Path(__file__).resolve().parent.parent
IMG = ROOT / "assets" / "img"

# view -> (focus plane in normalised depth, blur strength in px at 1/2 scale)
# These are renders and they are presented as renders. The earlier stills were
# dressed as photographs -- heavy defocus, film grain, a vignette -- and that
# dressing is what made them read as counterfeit rather than as studio stills.
# What is left is a light sharpen, so the edges resolve at display size.
SHOTS = {
    "unit": (0.500, 1.3),
    "cut": (0.480, 1.5),
    "detail": (0.520, 1.7),
    "band": (0.500, 1.3),
}

LEVELS = 9


def dof(rgb: Image.Image, depth: Image.Image, focus: float, strength: float) -> Image.Image:
    d = np.asarray(depth.convert("L"), dtype=np.float32) / 255.0
    w, h = rgb.size
    # the depth pass is rendered at the same size, but guard anyway
    if depth.size != rgb.size:
        d = np.asarray(depth.convert("L").resize(rgb.size), dtype=np.float32) / 255.0
    span = max(0.02, float(np.abs(d - focus).max()))
    coc = np.clip(np.abs(d - focus) / span, 0, 1) ** 0.75

    out = np.asarray(rgb, dtype=np.float32).copy()
    acc = np.zeros_like(out)
    mask_sum = np.zeros((h, w), dtype=np.float32)

    for i in range(LEVELS):
        lo, hi = i / LEVELS, (i + 1) / LEVELS
        radius = strength * ((lo + hi) / 2) ** 1.6
        band = ((coc >= lo) & (coc < hi)).astype(np.float32)
        if band.sum() == 0:
            continue
        m = Image.fromarray((band * 255).astype(np.uint8), "L")
        if radius >= 0.6:
            m = m.filter(ImageFilter.GaussianBlur(radius * 0.6))
        b = np.asarray(m, dtype=np.float32)[..., None] / 255.0
        blurred = np.asarray(
            rgb.filter(ImageFilter.GaussianBlur(max(radius, 0.3))), dtype=np.float32
        )
        acc += blurred * b
        mask_sum += b[..., 0]

    have = mask_sum > 1e-4
    out[have] = acc[have] / mask_sum[have][..., None]
    return Image.fromarray(np.clip(out, 0, 255).astype(np.uint8), "RGB")


def sharpen(rgb: Image.Image, amount: float = 1.0, radius: float = 1.1) -> Image.Image:
    """A lens resolves detail; a WebGL frame at this size looks soft next to one."""
    blur = rgb.filter(ImageFilter.GaussianBlur(radius))
    a = np.asarray(rgb, dtype=np.float32)
    b = np.asarray(blur, dtype=np.float32)
    out = a + amount * (a - b)
    return Image.fromarray(np.clip(out, 0, 255).astype(np.uint8), "RGB")


def grain(rgb: Image.Image, amount: float = 1.1) -> Image.Image:
    a = np.asarray(rgb, dtype=np.float32)
    rng = np.random.default_rng(7)
    n = rng.normal(0, 1, a.shape[:2]).astype(np.float32)
    # grain is strongest in the midtones, almost absent in the deep shadows
    lum = a.mean(axis=2) / 255.0
    weight = (0.35 + 0.9 * np.sin(np.clip(lum, 0, 1) * np.pi))[..., None]
    a = a + n[..., None] * amount * weight
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8), "RGB")


def vignette(rgb: Image.Image, strength: float = 0.0) -> Image.Image:
    w, h = rgb.size
    y, x = np.mgrid[0:h, 0:w].astype(np.float32)
    cx, cy = w / 2, h / 2
    r = np.sqrt(((x - cx) / cx) ** 2 + ((y - cy) / cy) ** 2) / np.sqrt(2)
    v = (1.0 - strength * np.clip(r, 0, 1) ** 2.4)[..., None]
    a = np.asarray(rgb, dtype=np.float32) * v
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8), "RGB")


def grade(rgb: Image.Image) -> Image.Image:
    a = np.asarray(rgb, dtype=np.float32) / 255.0
    # lift the blacks a touch and warm the highlights, the way tungsten does
    a = a ** 1.04
    a[..., 0] *= 1.035
    a[..., 2] *= 0.975
    return Image.fromarray(np.clip(a * 255, 0, 255).astype(np.uint8), "RGB")


def main():
    for view, (focus, strength) in SHOTS.items():
        src = IMG / f"product-{view}.png"
        dep = IMG / f"product-{view}.depth.png"
        if not src.exists():
            print("skip", view)
            continue
        rgb = Image.open(src).convert("RGB")
        half = rgb.resize((rgb.width // 2, rgb.height // 2), Image.LANCZOS)
        depth = Image.open(dep)
        out = dof(half, depth, focus, strength)
        out = sharpen(out)
        out = grade(out)
        out = grain(out)
        out = vignette(out)
        out.save(IMG / f"product-{view}.jpg", quality=88, optimize=True,
                 progressive=True, subsampling=1)
        kb = (IMG / f"product-{view}.jpg").stat().st_size / 1024
        print(f"{view}: {out.size[0]}x{out.size[1]} {kb:.0f} KB")


if __name__ == "__main__":
    main()
