"""Render the calibrated-noise scaling figure (2 algorithms x 2 regimes).

Run: python3 plots_calibrated.py
"""

import json

import numpy as np

import matplotlib.pyplot as plt
from plots import BASELINE, INK, INK2, MUTED, SERIES, SURFACE, style_axis

PANELS = [
    ("shor", "transmon_cal", "Shor order finding\ntransmon noise as measured"),
    ("shor", "transmon_cal_lowcharge",
     "Shor order finding\nhigh-$E_J/E_C$: charge noise engineered away"),
    ("qpe", "transmon_cal", "Eigenstate phase estimation\ntransmon noise as measured"),
    ("qpe", "transmon_cal_lowcharge",
     "Eigenstate phase estimation\nhigh-$E_J/E_C$: charge noise engineered away"),
]


def main():
    with open("results/scaling_calibrated.json") as f:
        data = json.load(f)
    runs, bl = data["runs"], data["baselines"]

    def signal(r):
        b = bl[f"{r['algo']},{r['d']},{r['m']}"]
        span = b["success"] - r["floor"]
        return (r["success"] - r["floor"]) / span, r["stderr"] / span

    fig, axes = plt.subplots(2, 2, figsize=(10.5, 8), sharex=True, sharey=True)
    fig.patch.set_facecolor(SURFACE)

    for ax, (algo, regime, title) in zip(axes.flat, PANELS):
        style_axis(ax)
        ax.axhline(0, color=BASELINE, linewidth=1)
        ends = []
        for d in (2, 3, 5):
            pts = sorted((r["m"] * np.log2(d), *signal(r)) for r in runs
                         if r["algo"] == algo and r["regime"] == regime
                         and r["d"] == d)
            xs = [p[0] for p in pts]
            ys = [p[1] for p in pts]
            es = [p[2] for p in pts]
            ax.errorbar(xs, ys, yerr=es, color=SERIES[d], linewidth=2,
                        marker="o", markersize=6, markeredgecolor=SURFACE,
                        markeredgewidth=1, capsize=3, elinewidth=1,
                        ecolor=MUTED, label=f"d = {d}")
            ends.append([d, xs[-1], ys[-1]])
        ends.sort(key=lambda e: e[2])
        for i in range(1, len(ends)):
            if ends[i][2] - ends[i - 1][2] < 0.06:
                ends[i][2] = ends[i - 1][2] + 0.06
        for d, x_end, y_lab in ends:
            ax.annotate(f"d = {d}", xy=(x_end, y_lab), xytext=(7, 0),
                        textcoords="offset points", va="center",
                        fontsize=9, color=INK2)
        ax.set_title(title, fontsize=10, color=INK, pad=8)
        ax.set_ylim(0, 1.02)

    for ax in axes[1]:
        ax.set_xlabel("phase-estimation precision, log₂ D (bits)",
                      fontsize=9.5, color=INK2)
    for ax in axes[:, 0]:
        ax.set_ylabel("success above random guessing\n(1 = noiseless, 0 = fully mixed)",
                      fontsize=9.5, color=INK2)
    axes[0, 0].legend(frameon=False, fontsize=9, labelcolor=INK2,
                      loc="lower left")

    fig.suptitle("Calibrated transmon noise: the qubit advantage survives only in Shor, "
                 "and only at small scale",
                 fontsize=12.5, color=INK, y=0.99)
    fig.tight_layout(rect=(0, 0, 1, 0.97))
    fig.savefig("results/scaling_calibrated.png", dpi=180,
                facecolor=SURFACE, bbox_inches="tight")
    print("wrote results/scaling_calibrated.png")


if __name__ == "__main__":
    main()
