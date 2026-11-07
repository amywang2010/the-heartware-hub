"""
DUAL-MICROPHONE NOISE REJECTION -- what the second microphone actually buys.

The insert carries two TDK ICS-43434s. One sits on the 3 mm acoustic port and
hears the chest plus the room. The other sits behind a sealed cavity and hears
the room almost alone. Subtracting one from the other is not a trick that needs
a trained network: room noise arrives at both capsules with high coherence and a
small delay, and a normalised LMS canceller can remove the part of it that is
predictable from the reference.

This script measures how much it removes, under assumptions stated in the code,
and prints the result the site quotes. It is a model, not a bench measurement,
and the page says so.

Run:  python research/noise_rejection.py
"""

import json
import math
import os

import numpy as np

FS = 16000
SECONDS = 8.0


def room_noise(rng, fs=FS, seconds=SECONDS):
    """Pink-ish room noise: HVAC rumble plus speech-shaped clutter."""
    n = int(fs * seconds)
    white = rng.standard_normal(n)
    # one-pole low-pass cascade gives the 1/f tilt of a real room
    out = white.copy()
    for _ in range(3):
        out = np.convolve(out, np.ones(6) / 6.0, mode="same")
    t = np.arange(n) / fs
    rumble = 0.6 * np.sin(2 * math.pi * 52 * t + rng.uniform(0, 6.28))
    clutter = 0.25 * rng.standard_normal(n) * (0.5 + 0.5 * np.sin(2 * math.pi * 0.7 * t) ** 2)
    mixed = out / (np.std(out) + 1e-9) + rumble * 0.35 + clutter * 0.4
    return mixed / (np.std(mixed) + 1e-9)


def heart_sound(rng, fs=FS, seconds=SECONDS):
    """S1 and S2 as short damped transients, repeated at 68 bpm."""
    n = int(fs * seconds)
    x = np.zeros(n)
    period = int(fs * 60 / 68)
    for start in range(0, n - period, period):
        for offset, (f, amp) in ((0.0, (58, 1.0)), (0.29, (74, 0.72))):
            s = start + int(offset * fs)
            length = int(0.09 * fs)
            if s + length >= n:
                continue
            t = np.arange(length) / fs
            env = np.exp(-t * 42)
            x[s:s + length] += amp * env * np.sin(2 * math.pi * f * t)
    return x


def nlms(reference, desired, taps=48, mu=0.35):
    """Normalised LMS: predict the noise in `desired` from `reference`."""
    w = np.zeros(taps)
    y = np.zeros_like(desired)
    eps = 1e-6
    buf = np.zeros(taps)
    for i in range(len(desired)):
        buf[1:] = buf[:-1]
        buf[0] = reference[i]
        y[i] = np.dot(w, buf)
        e = desired[i] - y[i]
        w += mu * e * buf / (np.dot(buf, buf) + eps)
        y[i] = e
    return y


def run(seed=20261106, coherence=0.72, leakage_db=-4.0, trials=20):
    """
    coherence  : fraction of the room noise that is shared by both capsules
    leakage_db : how much heart sound reaches the sealed reference capsule
    """
    rng = np.random.default_rng(seed)
    ratios = []
    for _ in range(trials):
        room = room_noise(rng)
        heart = heart_sound(rng)
        shared = coherence * room
        port = heart + shared + math.sqrt(max(0.0, 1 - coherence ** 2)) * room_noise(rng)
        ref = shared + 10 ** (leakage_db / 20) * heart
        cleaned = nlms(ref, port)
        # noise floor measured in the diastolic gap between transients
        band = np.abs(np.fft.rfft(cleaned)) ** 2
        before = np.abs(np.fft.rfft(port)) ** 2
        f = np.fft.rfftfreq(len(cleaned), 1 / FS)
        mask = (f > 60) & (f < 400)
        ratios.append(10 * math.log10(before[mask].sum() / max(band[mask].sum(), 1e-12)))
    return float(np.mean(ratios)), float(np.std(ratios))


def main():
    mean, sd = run()
    # streaming arithmetic, not measured: 16 kHz mono, 16-bit, 40 % packet overhead
    payload = 16000 * 16
    stream_kbps = payload * 1.4 / 1000
    out = {
        "noise_rejection_db": round(mean, 1),
        "noise_rejection_sd_db": round(sd, 1),
        "stream_kbps": round(stream_kbps, 0),
        "stream_ms_per_packet": 20,
    }
    here = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(here, "noise.json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=2)
    print(json.dumps(out, indent=2))
    print("wrote", path)


if __name__ == "__main__":
    main()
