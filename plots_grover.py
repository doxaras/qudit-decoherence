"""Grover vs Shor: the mechanism test. Run: python3 plots_grover.py"""

import json
import os


def _scaling_fair_path():
    p = "results/scaling_fair_1000.json"
    return p if os.path.exists(p) else "results/scaling_fair.json"


import matplotlib.pyplot as plt
import numpy as np

from plots import BASELINE, INK, INK2, MUTED, SERIES, SURFACE, style_axis

W = {2: 5, 3: 3, 5: 2}          # N = 21 work-register widths
TITLES = {"transmon_cal": "Transmon ladder, calibrated",
          "depolarizing": "Uniform depolarizing (per particle)"}


def interp(pts, x):
    pts = sorted(pts)
    xs = [p[0] for p in pts]
    ys = [p[1] for p in pts]
    return np.interp(x, xs, ys) if xs[0] <= x <= xs[-1] else np.nan


def main():
    grov = json.load(open("results/grover.json"))["scaling"]
    shor = json.load(open(_scaling_fair_path()))["runs"]

    fig, axes = plt.subplots(1, 2, figsize=(10.5, 4.6), sharey=True)
    fig.patch.set_facecolor(SURFACE)

    for ax, nm in zip(axes, ("transmon_cal", "depolarizing")):
        style_axis(ax)
        ax.axhline(0, color=INK2, linewidth=1.2)

        cg = {d: [(r["bits"], r["signal"]) for r in grov
                  if r["noise_model"] == nm and r["d"] == d] for d in (2, 5)}
        cs = {d: [(r["m"] * np.log2(d), r["signal"]) for r in shor
                  if r["regime"] == nm and r["d"] == d] for d in (2, 5)}

        xs = np.linspace(6.5, 8.5, 40)
        for curves, lab, style, col in (
                (cs, "Shor — width AND depth compress", "-", SERIES[5]),
                (cg, "Grover — only width compresses", "--", SERIES[3])):
            ys = [interp(curves[5], x) - interp(curves[2], x) for x in xs]
            ax.plot(xs, ys, style, color=col, linewidth=2.2, label=lab)

        ax.set_xlabel("problem size, log₂ (search space / phase grid)  [bits]",
                      fontsize=9.5, color=INK2)
        ax.set_title(TITLES[nm], fontsize=11, color=INK, pad=8)

    axes[0].set_ylabel("ququint advantage over qubits\n"
                       "(signal $d{=}5$ − signal $d{=}2$)",
                       fontsize=9.5, color=INK2)
    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(handles, labels, frameon=False, fontsize=9, labelcolor=INK2,
               loc="upper center", ncol=2, bbox_to_anchor=(0.5, 0.93))

    fig.suptitle("Removing depth compression shrinks the qudit advantage "
                 "but does not remove it",
                 fontsize=12, color=INK, y=1.0)
    fig.tight_layout(rect=(0, 0.03, 1, 0.87))
    fig.text(0.5, 0.005,
             "fixed per-layer strength: ladder 0.003, depolarizing 0.005 — "
             "at or below today's per-gate error "
             "(transmon two-qudit ~10$^{-2}$, ion ~10$^{-3}$)",
             ha="center", fontsize=8.5, color=MUTED)
    fig.savefig("results/grover.png", dpi=180, facecolor=SURFACE,
                bbox_inches="tight")
    print("wrote results/grover.png")


if __name__ == "__main__":
    main()
