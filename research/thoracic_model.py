"""
Thoracic correction: model definition and validation experiment.

Every number on the Evidence page comes from this file. Run it and the figures and
`results.json` regenerate; nothing on the site is typed by hand.

    python research/thoracic_model.py
    python research/make_figures.py

WHAT THIS IS
    A forward model of the chest wall as an acoustic filter between the valve and
    the microphone, and an estimator that recovers that filter from the recording
    itself. The experiment asks two questions:

      1. Can the correction estimate the wall without being told anything about
         the patient? (If it needed the thickness, the product would be pointless.)
      2. Does removing the wall make a murmur arrive at the same level regardless
         of the body it passed through?

WHAT THIS IS NOT
    Not patient data. No echocardiogram, no recorded human. It validates the
    arithmetic of the inversion and nothing about diagnostic accuracy. Sensitivity
    against echo is a clinical study and is not claimed anywhere.
"""

from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
OUT = HERE / "results.json"

FS = 8000.0
DUR = 3.0
N = int(FS * DUR)
FREQS = np.fft.rfftfreq(N, 1.0 / FS)

FIT_LO, FIT_HI = 60.0, 700.0
FIT = (FREQS >= FIT_LO) & (FREQS <= FIT_HI)
MURMUR = (FREQS >= 150.0) & (FREQS <= 400.0)
ANCHOR = (FREQS >= 20.0) & (FREQS <= 150.0)

D_GRID = np.arange(8.0, 46.01, 0.5)  # mm
ASSUMED = dict(alpha0=0.55, exponent=1.15, q=2.2)
WIENER = 0.02

SEG = 0.06  # seconds of each S1 used to characterise the wall
SEG_N = int(SEG * FS)


# --------------------------------------------------------------------------- #
# The forward model
# --------------------------------------------------------------------------- #

def attenuation_db(f, d_mm, alpha0=0.55, exponent=1.15):
    """Soft-tissue absorption in dB: a power law in frequency, linear in path.

    alpha0 is dB per cm at 100 Hz. The exponent above one is what makes the wall a
    low-pass rather than a flat pad, and it is the part that grows with fat.
    """
    return alpha0 * (f / 100.0) ** exponent * (d_mm / 10.0)


def resonance(f, d_mm, q=2.2, f_ref=155.0, d_ref=28.0):
    """Chest-wall mass-spring resonance. More mass, lower resonance."""
    f0 = f_ref * math.sqrt(d_ref / d_mm)
    x = f / f0
    return 1.0 / np.sqrt((1.0 - x * x) ** 2 + (x / q) ** 2)


def transfer(f, d_mm, alpha0=0.55, exponent=1.15, q=2.2):
    """Magnitude response of the chest wall, normalised to 100 Hz."""
    a = 10.0 ** (-attenuation_db(f, d_mm, alpha0, exponent) / 20.0)
    r = resonance(f, d_mm, q)
    a0 = 10.0 ** (-attenuation_db(np.array([100.0]), d_mm, alpha0, exponent)[0] / 20.0)
    r0 = resonance(np.array([100.0]), d_mm, q)[0]
    return (a * r) / (a0 * r0)


# --------------------------------------------------------------------------- #
# Estimating the wall from the recording
# --------------------------------------------------------------------------- #

SMOOTH_OCT = 0.15
NUISANCE = 2  # gain, tilt and curvature of the unknown source spectrum

_F = FREQS[FIT]
_LF = np.log2(_F)


def _projector(order=NUISANCE):
    q, _ = np.linalg.qr(
        np.column_stack([np.ones(_F.size)] + [_LF**p for p in range(1, order + 1)])
    )
    return np.eye(_F.size) - q @ q.T


_P = _projector()


def _smooth(y):
    step = _LF[1] - _LF[0]
    sig = SMOOTH_OCT / step
    rad = int(3 * sig) + 1
    kern = np.exp(-0.5 * (np.arange(-rad, rad + 1) / sig) ** 2)
    kern /= kern.sum()
    return np.convolve(np.pad(y, rad, mode="edge"), kern, mode="valid")


_CACHE: dict = {}


def basis_functions(**kw):
    """Model spectra, projected into the subspace orthogonal to the nuisance."""
    key = tuple(sorted(kw.items()))
    if key not in _CACHE:
        _CACHE[key] = np.column_stack(
            [_P @ _smooth(np.log(transfer(_F, d, **kw) ** 2 + 1e-14)) for d in D_GRID]
        )
    return _CACHE[key]


def segment_spectrum(x, onsets):
    """Average periodogram over the S1 transients.

    The wall is characterised from valve closure, not from the murmur. Estimating
    from the murmur would be circular: the murmur is the thing being recovered.
    Segments are Hann-windowed and averaged, which is what makes a single three
    second recording enough.
    """
    win = np.hanning(SEG_N)
    psd = np.zeros(SEG_N // 2 + 1)
    used = 0
    for b in onsets:
        i = int(b * FS)
        if i + SEG_N < N:
            psd += np.abs(np.fft.rfft(x[i : i + SEG_N] * win)) ** 2
            used += 1
    if used == 0:
        return None
    f = np.fft.rfftfreq(SEG_N, 1.0 / FS)
    return np.interp(FREQS, f, np.sqrt(psd / used))


def estimate_thickness(mag_spectrum, **kw):
    """Recover wall thickness in mm from one recording.

    The source is unknown, so the fit allows an arbitrary smooth source envelope
    (gain, tilt, curvature) and projects it out before scoring. What survives is
    shape: the wall's resonance position and its curvature.
    """
    y = _P @ _smooth(np.log(mag_spectrum[FIT] ** 2 + 1e-14))
    resid = ((y[:, None] - basis_functions(**(kw or ASSUMED))) ** 2).sum(axis=0)
    return float(D_GRID[int(np.argmin(resid))])


def correct(x, d_mm, lam=WIENER, **kw):
    """Regularised inverse of the wall.

    An exact inverse would restore the source and amplify the noise floor with it,
    so the filter is Wiener-weighted: where the wall attenuates more than the noise
    floor sits, the correction stops pushing. Level is renormalised after, because
    the clinician's ear should hear a corrected murmur, not a louder one.
    """
    h = transfer(FREQS, d_mm, **(kw or ASSUMED))
    w = h / (h * h + lam)
    spec = np.fft.rfft(x) * w
    spec /= np.sqrt(np.mean(w**2))
    return np.fft.irfft(spec, n=N)


# --------------------------------------------------------------------------- #
# Signal synthesis
# --------------------------------------------------------------------------- #

def _burst(rng, n, cutoff, decay):
    """A valve closure: broadband onset, fast decay, gentle roll-off.

    Noise through a one-pole low-pass, so the transient carries energy across the
    analysis band. A single tone would carry no information about a filter.
    """
    w = rng.normal(size=n)
    y = np.zeros(n)
    a = math.exp(-2 * math.pi * cutoff / FS)
    for i in range(1, n):
        y[i] = (1 - a) * w[i] + a * y[i - 1]
    y *= np.exp(-np.arange(n) / (decay * FS))
    y -= np.mean(y)
    return y / (np.max(np.abs(y)) + 1e-12)


def heart_sound(rng, murmur_gain, period):
    t = np.arange(N) / FS
    x = np.zeros(N)
    onsets = []
    for beat in np.arange(0.0, DUR - 0.4, period):
        i1 = int((beat + 0.06) * FS)
        if i1 + SEG_N < N:
            x[i1 : i1 + SEG_N] += _burst(rng, SEG_N, 260.0, 0.030)
            onsets.append(beat + 0.06)
        i2 = int((beat + 0.36) * FS)
        n2 = int(0.07 * FS)
        if i2 + n2 < N:
            x[i2 : i2 + n2] += 0.62 * _burst(rng, n2, 340.0, 0.022)
        if murmur_gain > 0:
            win = (t > beat + 0.10) & (t < beat + 0.34)
            if win.sum() < 64:
                continue
            band = rng.normal(size=int(win.sum()))
            spec = np.fft.rfft(band)
            f = np.fft.rfftfreq(band.size, 1.0 / FS)
            spec[(f < 150) | (f > 400)] = 0.0
            band = np.fft.irfft(spec, n=band.size)
            band /= np.max(np.abs(band)) + 1e-12
            masked = np.zeros(N)
            masked[win] = murmur_gain * np.hanning(band.size) * band
            x += masked
    return x, onsets


def room_noise(rng, level):
    n = rng.normal(size=N)
    spec = np.fft.rfft(n)
    spec *= 1.0 / np.sqrt(1.0 + (FREQS / 45.0) ** 2)
    spec += rng.normal(size=spec.size) * 0.02
    spec[np.abs(FREQS - 50.0) < 1.5] *= 12.0
    spec[np.abs(FREQS - 150.0) < 1.5] *= 6.0
    n = np.fft.irfft(spec, n=N)
    return level * n / np.std(n)


def apply_filter(x, d_mm, **kw):
    spec = np.fft.rfft(x) * transfer(FREQS, d_mm, **kw)
    return np.fft.irfft(spec, n=N)


# --------------------------------------------------------------------------- #
# Metrics
# --------------------------------------------------------------------------- #

def band_energy(x, mask):
    return float(np.sum(np.abs(np.fft.rfft(x)[mask]) ** 2))


def murmur_ratio(x):
    """Murmur band against the S1/S2 anchor, in dB.

    Scale-free on purpose: the number cannot be improved by turning the volume up
    or by pressing harder.
    """
    return 10.0 * math.log10(band_energy(x, MURMUR) / (band_energy(x, ANCHOR) + 1e-12))


def thickness_for(bmi, age, rng):
    """Wall thickness from habitus and age, with the scatter real people have."""
    d = 8.0 * np.exp(0.030 * bmi) + 0.035 * max(0.0, age - 40)
    return float(np.clip(d + rng.normal(0, 1.6), 9.0, 45.0))


# --------------------------------------------------------------------------- #
# Population sweep
# --------------------------------------------------------------------------- #

def run(n_subjects=600, seed=20261106, truth_kw=None, assumed_kw=None):
    rng = np.random.default_rng(seed)
    truth_kw = truth_kw or {}
    assumed_kw = assumed_kw or {}
    rows = []
    for _ in range(n_subjects):
        bmi = float(np.clip(rng.normal(29.0, 6.5), 17.0, 48.0))
        age = float(np.clip(rng.normal(58.0, 17.0), 18.0, 92.0))
        d = thickness_for(bmi, age, rng)
        period = 60.0 / float(np.clip(rng.normal(74, 11), 48, 118))

        has_murmur = rng.random() < 0.5
        src, onsets = heart_sound(rng, 0.30 if has_murmur else 0.0, period)
        rec = apply_filter(src, d, **truth_kw) + room_noise(rng, 0.20)

        spec = segment_spectrum(rec, onsets)
        d_hat = estimate_thickness(spec, **assumed_kw) if spec is not None else float("nan")

        rows.append(
            dict(
                bmi=bmi,
                age=age,
                d=d,
                d_hat=d_hat,
                murmur=has_murmur,
                raw=murmur_ratio(rec),
                corrected=murmur_ratio(correct(rec, d_hat, **assumed_kw)),
                fixed=murmur_ratio(correct(rec, 20.0, **assumed_kw)),
            )
        )
    return rows


def _cells(rows, key):
    bmi = np.array([r["bmi"] for r in rows])
    lo, hi = np.quantile(bmi, [1 / 3, 2 / 3])
    tert = np.where(bmi <= lo, 0, np.where(bmi <= hi, 1, 2))
    out = []
    for k in range(3):
        sel = tert == k
        out.append(
            {
                "bmi": round(float(np.mean(bmi[sel])), 1),
                "raw": round(float(np.mean([r["raw"] for r, s in zip(rows, sel) if s])), 2),
                "corrected": round(
                    float(np.mean([r[key] for r, s in zip(rows, sel) if s])), 2
                ),
                "n": int(sel.sum()),
            }
        )
    return out


def summarise(rows, key="corrected"):
    d = np.array([r["d"] for r in rows])
    dh = np.array([r["d_hat"] for r in rows])
    y = np.array([r[key] for r in rows])
    raw = np.array([r["raw"] for r in rows])
    cells = _cells(rows, key)
    return {
        "n": len(rows),
        "thickness_rmse": round(float(np.sqrt(np.mean((dh - d) ** 2))), 2),
        "thickness_bias": round(float(np.mean(dh - d)), 2),
        "thickness_r": round(float(np.corrcoef(d, dh)[0, 1]), 3),
        "thickness_within_5mm": round(float(np.mean(np.abs(dh - d) <= 5.0)), 3),
        "gain_db": round(float(np.mean(y - raw)), 2),
        "cells": cells,
        "spread": round(max(c["corrected"] for c in cells) - min(c["corrected"] for c in cells), 2),
    }


def main():
    rows = run()
    s_cor = summarise(rows, "corrected")
    s_raw = summarise(rows, "raw")
    s_fix = summarise(rows, "fixed")

    # the wall has a resonance; pretending it does not is what a purely
    # attenuation-based correction does, and the resonance is the part that
    # carries the thickness information
    flat_rows = run(truth_kw={}, assumed_kw=dict(ASSUMED, q=1e6), n_subjects=300)

    ablations = [
        {
            "name": "No correction",
            "detail": "the recording as the ear receives it",
            "gain_db": 0.0,
            "spread": s_raw["spread"],
        },
        {
            "name": "One fixed thickness",
            "detail": "20 mm assumed for every patient",
            "gain_db": s_fix["gain_db"],
            "spread": s_fix["spread"],
        },
        {
            "name": "Resonance ignored",
            "detail": "absorption modelled, the wall's resonance not",
            "gain_db": summarise(flat_rows)["gain_db"],
            "spread": summarise(flat_rows)["spread"],
        },
        {
            "name": "Estimated per recording",
            "detail": "this work: the wall recovered from the signal",
            "gain_db": s_cor["gain_db"],
            "spread": s_cor["spread"],
        },
    ]

    robustness = []
    for label, kw in [
        ("absorption +20 %", {"alpha0": 0.55 * 1.2}),
        ("absorption -20 %", {"alpha0": 0.55 * 0.8}),
        ("exponent +15 %", {"exponent": 1.15 * 1.15}),
        ("exponent -15 %", {"exponent": 1.15 * 0.85}),
        ("resonance Q -30 %", {"q": 2.2 * 0.7}),
        ("resonance Q +30 %", {"q": 2.2 * 1.3}),
    ]:
        r = run(truth_kw=kw, assumed_kw=ASSUMED, seed=99, n_subjects=150)
        robustness.append(
            {
                "label": label,
                "rmse": round(float(np.sqrt(np.mean([(x["d_hat"] - x["d"]) ** 2 for x in r]))), 2),
                "gain_db": round(float(np.mean([x["corrected"] - x["raw"] for x in r])), 2),
                "spread": summarise(r)["spread"],
            }
        )

    result = {
        "model": {
            "n": s_cor["n"],
            "fit_band_hz": [FIT_LO, FIT_HI],
            "murmur_band_hz": [150, 400],
            "thickness_grid_mm": [float(D_GRID[0]), float(D_GRID[-1]), 0.5],
            "wiener_lambda": WIENER,
            "segment_ms": int(SEG * 1000),
            "seed": 20261106,
        },
        "corrected": s_cor,
        "raw": s_raw,
        "ablations": ablations,
        "robustness": robustness,
    }
    OUT.write_text(json.dumps(result, indent=2))
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
