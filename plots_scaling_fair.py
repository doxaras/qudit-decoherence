"""Register-size scaling on the unbiased instance (2x2 regimes).

Run: python3 plots_scaling_fair.py
"""

import glob
import json
import os


def _scaling_fair_path():
    p = "results/scaling_fair_1000.json"
    return p if os.path.exists(p) else "results/scaling_fair.json"


import numpy as np

import matplotlib.pyplot as plt
from plots import BASELINE, INK, INK2, MUTED, SERIES, SURFACE, style_axis

PANELS = [
    ("depolarizing", "Uniform depolarizing\n(ions / NV / photonics, per particle)"),
    ("transmon", "Transmon ladder, idealized\n($\\Gamma_k \\propto k$, $(\\Delta\\mathrm{level})^2$ dephasing)"),
    ("transmon_cal", "Transmon ladder, calibrated\n(devices as measured)"),
    ("transmon_cal_lowcharge",
     "Transmon ladder, calibrated\n(high-$E_J/E_C$: charge noise engineered away)"),
]


def main():
    with open(_scaling_fair_path()) as f:
        data = json.load(f)
    runs, bl = list(data["runs"]), dict(data["baselines"])
    # Points measured outside the main sweep: the fifth qutrit size
    # (d=3, m=8, 1000 traj) and any scaling_fair_d<d>_m<m>.json. Merged by
    # override on (d, m, regime) so a re-measurement at higher statistics
    # REPLACES the original point -- appending would double-count it into
    # every fit drawn from these runs.
    extra = ["results/scaling_fair_m8.json"]
    extra += sorted(glob.glob("results/scaling_fair_d*_m*.json"))
    for path in extra:
        if not os.path.exists(path):
            continue
        with open(path) as f:
            sup = json.load(f)
        bl[f"{sup['d']},{sup['m']}"] = sup["baseline"]
        replaced = {(r["d"], r["m"], r["regime"]) for r in sup["runs"]}
        runs = [r for r in runs
                if (r["d"], r["m"], r["regime"]) not in replaced]
        runs += sup["runs"]

    def signal(r):
        b = bl[f"{r['d']},{r['m']}"]
        span = b["success"] - r["floor"]
        return (r["success"] - r["floor"]) / span, r["stderr"] / span

    fig, axes = plt.subplots(2, 2, figsize=(10.5, 8), sharex=True, sharey=True)
    fig.patch.set_facecolor(SURFACE)

    for ax, (regime, title) in zip(axes.flat, PANELS):
        style_axis(ax)
        ax.axhline(0, color=BASELINE, linewidth=1)
        ends = []
        for d in (2, 3, 5):
            pts = sorted((r["m"] * np.log2(d), *signal(r)) for r in runs
                         if r["regime"] == regime and r["d"] == d)
            xs = [p[0] for p in pts]
            ys = [p[1] for p in pts]
            es = [p[2] for p in pts]
            ax.errorbar(xs, ys, yerr=es, color=SERIES[d], linewidth=2,
                        marker="o", markersize=6, markeredgecolor=SURFACE,
                        markeredgewidth=1, capsize=3, elinewidth=1,
                        ecolor=MUTED, label=f"$d = {d}$")
            ends.append([d, xs[-1], ys[-1]])
        ends.sort(key=lambda e: e[2])
        for i in range(1, len(ends)):
            if ends[i][2] - ends[i - 1][2] < 0.06:
                ends[i][2] = ends[i - 1][2] + 0.06
        for d, x_end, y_lab in ends:
            ax.annotate(f"$d = {d}$", xy=(x_end, y_lab), xytext=(7, 0),
                        textcoords="offset points", va="center",
                        fontsize=9, color=INK2)
        ax.set_title(title, fontsize=10, color=INK, pad=8)
        ax.set_ylim(0, 1.02)

    for ax in axes[1]:
        ax.set_xlabel("phase-estimation precision, log₂ D (bits)",
                      fontsize=9.5, color=INK2)
    for ax in axes[:, 0]:
        ax.set_ylabel("success above random guessing\n"
                      "(1 = noiseless, 0 = fully mixed)",
                      fontsize=9.5, color=INK2)
    axes[0, 0].legend(frameon=False, fontsize=9, labelcolor=INK2,
                      loc="lower left")

    fig.suptitle(f"Shor scaling with the grid-alignment confound removed "
                 f"($N = {data['N']}$, $a = {data['a']}$, $r = 6$): "
                 f"the qudit lead holds at every size",
                 fontsize=12, color=INK, y=0.995)
    fig.tight_layout(rect=(0, 0.025, 1, 0.97))
    fig.text(0.5, 0.005,
             "fixed per-layer strength: ladder 0.003, depolarizing 0.005 — "
             "at or below today's per-gate error "
             "(transmon two-qudit ~10$^{-2}$, ion ~10$^{-3}$)",
             ha="center", fontsize=8.5, color=MUTED)
    fig.savefig("results/scaling_fair.png", dpi=180, facecolor=SURFACE,
                bbox_inches="tight")
    print("wrote results/scaling_fair.png")


if __name__ == "__main__":
    main()
