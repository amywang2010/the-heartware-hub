"""Figures for the Evidence page. Reads results.json; never invents a number."""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import FuncFormatter

import thoracic_model as tm

HERE = Path(__file__).resolve().parent
FIG = HERE.parent / "assets" / "figures"
FIG.mkdir(parents=True, exist_ok=True)

CREAM = "#FFF8F4"
INK = "#1B1015"
RED = "#C8102E"
HOT = "#F0426A"
NAVY = "#12306B"
SKY = "#4C77B8"
MUTED = "#8B7B84"
SAND = "#E9D9D2"

plt.rcParams.update(
    {
        "figure.facecolor": CREAM,
        "axes.facecolor": CREAM,
        "savefig.facecolor": CREAM,
        "font.family": "DejaVu Sans",
        "font.size": 11,
        "axes.edgecolor": SAND,
        "axes.labelcolor": INK,
        "text.color": INK,
        "xtick.color": MUTED,
        "ytick.color": MUTED,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.linewidth": 1.0,
        "xtick.direction": "out",
        "ytick.direction": "out",
        "figure.dpi": 200,
    }
)

R = json.loads((HERE / "results.json").read_text())
COR = R["corrected"]


def save(fig, name):
    fig.savefig(FIG / name, bbox_inches="tight", pad_inches=0.28)
    plt.close(fig)
    print("wrote", name)


# --------------------------------------------------------------------------- #
# 1. What the wall does to a spectrum
# --------------------------------------------------------------------------- #
def fig_transfer():
    f = np.logspace(np.log10(20), np.log10(1200), 700)
    depths = [12, 20, 28, 38]
    fig, ax = plt.subplots(figsize=(7.2, 4.3))

    ax.axvspan(150, 400, color=RED, alpha=0.055, lw=0)

    handles = []
    for d, shade in zip(depths, ["#F7B7B7", HOT, RED, "#6E0A18"]):
        g = 20 * np.log10(tm.transfer(f, d) + 1e-12)
        (ln,) = ax.plot(f, g, color=shade, lw=2.6 if d == 28 else 1.9, zorder=3)
        handles.append(ln)

    ax.legend(
        handles,
        [f"{d} mm wall" for d in depths],
        frameon=False,
        loc="lower left",
        fontsize=10,
        handlelength=2.2,
        labelcolor=INK,
    )

    ax.set_xscale("log")
    ax.set_xlim(20, 1600)
    ax.set_ylim(-34, 9)
    ax.set_xticks([20, 50, 100, 200, 400, 1000])
    ax.get_xaxis().set_major_formatter(FuncFormatter(lambda v, _: f"{v:g}"))
    ax.set_xlabel("frequency, Hz", labelpad=8)
    ax.set_ylabel("gain through the wall, dB", labelpad=8)
    ax.grid(axis="y", color=SAND, lw=0.8, alpha=0.8)
    ax.set_axisbelow(True)
    ax.text(
        272, 7.2, "M U R M U R   B A N D", color=RED, fontsize=8.5,
        fontweight="bold", ha="center", va="top"
    )

    save(fig, "fig-01-transfer.png")


# --------------------------------------------------------------------------- #
# 2. Thickness recovered from the signal alone
# --------------------------------------------------------------------------- #
def fig_identity():
    rows = tm.run(n_subjects=320, seed=4242)
    d = np.array([r["d"] for r in rows])
    dh = np.array([r["d_hat"] for r in rows])

    fig, ax = plt.subplots(figsize=(5.4, 5.0))
    ax.fill_between([8, 46], [3, 41], [13, 51], color=RED, alpha=0.07, lw=0)
    ax.plot([8, 46], [8, 46], color=NAVY, lw=1.4, ls=(0, (4, 3)))
    ax.scatter(d, dh, s=17, color=RED, alpha=0.45, edgecolors="none", zorder=3)
    ax.set_xlim(8, 46)
    ax.set_ylim(8, 46)
    ax.set_aspect("equal")
    ax.set_xlabel("true wall thickness, mm", labelpad=8)
    ax.set_ylabel("estimated from the recording, mm", labelpad=8)
    ax.text(9.2, 43.5, "± 5 mm", color=RED, fontsize=10, fontweight="bold")
    ax.annotate(
        f"r = {COR['thickness_r']:.2f}\nRMS error {COR['thickness_rmse']:.1f} mm",
        xy=(38, 14),
        fontsize=10.5,
        color=INK,
        ha="right",
        va="center",
        bbox=dict(boxstyle="round,pad=0.5", fc=CREAM, ec=SAND),
    )
    ax.grid(color=SAND, lw=0.7, alpha=0.7)
    ax.set_axisbelow(True)
    save(fig, "fig-02-identity.png")


# --------------------------------------------------------------------------- #
# 3. The body dependence, removed
# --------------------------------------------------------------------------- #
def fig_body():
    cells = COR["cells"]
    x = np.arange(len(cells))
    raw = [c["raw"] for c in cells]
    cor = [c["corrected"] for c in cells]

    fig, ax = plt.subplots(figsize=(6.6, 4.2))
    for i in x:
        ax.plot([i, i], [raw[i], cor[i]], color=SAND, lw=2.4, zorder=1)
    raw_line = ax.plot(x, raw, color=MUTED, lw=2.2, marker="o", ms=7, zorder=3)[0]
    cor_line = ax.plot(x, cor, color=RED, lw=3.0, marker="o", ms=8, zorder=4)[0]

    for i in x:
        ax.annotate(
            f"{cor[i]-raw[i]:+.1f} dB",
            (i, cor[i]),
            xytext=(0, 13),
            textcoords="offset points",
            ha="center",
            fontsize=10,
            color=RED,
            fontweight="bold",
        )
        ax.annotate(
            f"{raw[i]:.1f}",
            (i, raw[i]),
            xytext=(0, -17),
            textcoords="offset points",
            ha="center",
            fontsize=10,
            color=MUTED,
        )

    ax.set_xticks(x)
    ax.set_xticklabels([f"BMI {c['bmi']:.0f}" for c in cells], color=INK, fontsize=11)
    ax.set_ylabel("murmur level, dB re S1/S2", labelpad=8)
    ax.set_ylim(min(raw) - 1.2, max(cor) + 1.8)
    ax.grid(axis="y", color=SAND, lw=0.8, alpha=0.8)
    ax.set_axisbelow(True)
    ax.legend(
        [raw_line, cor_line],
        ["as the ear receives it", "corrected per recording"],
        frameon=False,
        loc="lower left",
        bbox_to_anchor=(0, -0.36),
        ncol=2,
        fontsize=9.5,
        labelcolor=INK,
    )
    ax.text(
        1.0,
        max(cor) + 1.4,
        f"spread {COR['spread']:.2f} dB",
        ha="right",
        fontsize=10,
        color=RED,
        fontweight="bold",
    )
    save(fig, "fig-03-body.png")


# --------------------------------------------------------------------------- #
# 4. Ablation: what actually does the work
# --------------------------------------------------------------------------- #
def fig_ablation():
    rows = sorted(R["ablations"], key=lambda a: -a["spread"])
    labels = [r["name"] for r in rows]
    vals = [r["spread"] for r in rows]
    y = np.arange(len(rows))[::-1]

    fig, ax = plt.subplots(figsize=(6.8, 3.4))
    colors = [MUTED if v > 1 else SKY for v in vals]
    colors[-1] = RED
    ax.barh(y, vals, color=colors, height=0.52, zorder=3)
    for yy, v, r in zip(y, vals, rows):
        ax.text(v + 0.04, yy, f"{v:.2f} dB", va="center", fontsize=10.5,
                color=RED if r is rows[-1] else INK, fontweight="bold")
    ax.set_yticks(y)
    ax.set_yticklabels(labels, color=INK, fontsize=10.5)
    ax.set_xlabel("spread in murmur level across body types, dB", labelpad=8)
    ax.set_xlim(0, max(vals) * 1.32)
    ax.grid(axis="x", color=SAND, lw=0.8, alpha=0.8)
    ax.set_axisbelow(True)
    save(fig, "fig-04-ablation.png")


# --------------------------------------------------------------------------- #
# 5. One recording, before and after
# --------------------------------------------------------------------------- #
def fig_waveform():
    rng = np.random.default_rng(88)
    src, onsets = tm.heart_sound(rng, 0.30, 0.82)
    d = 30.0
    rec = tm.apply_filter(src, d) + tm.room_noise(rng, 0.18)
    spec = tm.segment_spectrum(rec, onsets)
    d_hat = tm.estimate_thickness(spec)
    cor = tm.correct(rec, d_hat)

    def envelope(x):
        spec = np.fft.rfft(x)
        band = (tm.FREQS < 150) | (tm.FREQS > 400)
        spec[band] = 0
        y = np.abs(np.fft.irfft(spec, n=tm.N))
        k = 40
        return np.convolve(y, np.ones(k) / k, mode="same")

    t = np.arange(tm.N) / tm.FS
    lo, hi = 0.0, 1.6
    sel = (t >= lo) & (t <= hi)
    e_raw = envelope(rec)
    e_cor = envelope(cor)
    scale = np.max(e_cor[sel]) * 1.08

    fig, axes = plt.subplots(2, 1, figsize=(8.0, 4.6), sharex=True,
                             gridspec_kw=dict(hspace=0.22))
    for ax, y, c, label in [
        (axes[0], e_raw, MUTED, "as recorded"),
        (axes[1], e_cor, RED, "corrected"),
    ]:
        ax.fill_between(t[sel], 0, y[sel] / scale, color=c, alpha=0.18, lw=0)
        ax.plot(t[sel], y[sel] / scale, color=c, lw=1.5)
        ax.set_yticks([])
        ax.set_ylim(0, 1.18)
        ax.text(hi - 0.02, 1.1, label, ha="right", va="top",
                color=c, fontsize=11, fontweight="bold")
        ax.spines["left"].set_visible(False)
    axes[1].set_xlabel("seconds", labelpad=8)
    axes[0].set_title(
        f"one patient, {d:.0f} mm wall · estimated {d_hat:.0f} mm · "
        f"murmur band {tm.murmur_ratio(cor) - tm.murmur_ratio(rec):+.1f} dB · "
        f"150-400 Hz envelope, one scale",
        fontsize=10,
        color=MUTED,
        loc="left",
        pad=10,
    )
    save(fig, "fig-05-waveform.png")


# --------------------------------------------------------------------------- #
# 6. Robustness to the model being wrong
# --------------------------------------------------------------------------- #
def fig_robustness():
    rows = R["robustness"]
    labels = [r["label"] for r in rows]
    y = np.arange(len(rows))[::-1]

    fig, ax = plt.subplots(figsize=(6.8, 3.2))
    for yy, r in zip(y, rows):
        ax.plot([r["gain_db"], COR["gain_db"]], [yy, yy], color=SAND, lw=2)
        ax.scatter(r["gain_db"], yy, s=70, color=RED, zorder=3)
    ax.axvline(COR["gain_db"], color=NAVY, lw=1.2, ls=(0, (4, 3)), zorder=2)
    ax.set_yticks(y)
    ax.set_yticklabels(labels, color=INK, fontsize=10)
    ax.set_xlabel("murmur gain with the model deliberately wrong, dB", labelpad=8)
    ax.set_xlim(0, 3.4)
    ax.grid(axis="x", color=SAND, lw=0.8, alpha=0.8)
    ax.set_axisbelow(True)
    ax.text(COR["gain_db"], y[0] + 0.55, "exact model", color=NAVY,
            fontsize=9.5, ha="center")
    save(fig, "fig-06-robustness.png")


if __name__ == "__main__":
    fig_transfer()
    fig_identity()
    fig_body()
    fig_ablation()
    fig_waveform()
    fig_robustness()
