"""Gate-cost sensitivity for Shor on the unbiased instance.

Run: python3 plots_cost_fair.py
"""

import json

import matplotlib.pyplot as plt
import numpy as np

from plots import BASELINE, GRID, INK, INK2, MUTED, SERIES, SURFACE

STRENGTH = 0.005
COST_LABELS = {"uniform": "uniform\n(native qudit gate)",
               "ion": "ion\n(2(d−1) MS gates)",
               "pavlidis": "pavlidis\n(d² decomposition)"}
NOISE = [("depolarizing", "ions / per-particle noise"),
         ("transmon_cal", "transmon / calibrated ladder")]


def main():
    with open("results/cost_fair.json") as f:
        data = json.load(f)
    runs, costs = data["runs"], data["costs"]

    fig, axes = plt.subplots(1, 2, figsize=(10.5, 4.6), sharey=True)
    fig.patch.set_facecolor(SURFACE)
    x = np.arange(len(costs))
    width = 0.27

    for ax, (nm, title) in zip(axes, NOISE):
        ax.set_facecolor(SURFACE)
        for side in ("top", "right", "left"):
            ax.spines[side].set_visible(False)
        ax.spines["bottom"].set_color(BASELINE)
        ax.tick_params(colors=MUTED, labelsize=9)
        ax.grid(axis="y", color=GRID, linewidth=0.8)
        ax.set_axisbelow(True)
        ax.axhline(0, color=BASELINE, linewidth=1.2)

        for j, d in enumerate((2, 3, 5)):
            vals = [next(r["signal"] for r in runs if r["noise"] == nm
                         and r["cost"] == cm and r["d"] == d
                         and r["strength"] == STRENGTH) for cm in costs]
            bars = ax.bar(x + (j - 1) * width, vals, width * 0.9,
                          color=SERIES[d], label=f"$d = {d}$")
            for b, v in zip(bars, vals):
                ax.annotate(f"{v:.2f}",
                            xy=(b.get_x() + b.get_width() / 2, v),
                            xytext=(0, 3 if v >= 0 else -12),
                            textcoords="offset points", ha="center",
                            fontsize=8, color=INK2)

        ax.set_xticks(x)
        ax.set_xticklabels([COST_LABELS[c] for c in costs], fontsize=8.5,
                           color=INK2)
        ax.set_title(title, fontsize=11, color=INK, pad=8)

    axes[0].set_ylabel("success above random guessing\n"
                       "(1 = noiseless, 0 = fully mixed)",
                       fontsize=9.5, color=INK2)
    axes[1].legend(frameon=False, fontsize=9, labelcolor=INK2,
                   loc="upper right", ncol=3)

    fig.suptitle(f"Unbiased Shor ($N = {data['N']}$, $r = {data['r']}$) obeys the same rule as "
                 f"phase estimation:\nqudits win iff the entangling gate is native",
                 fontsize=11.5, color=INK, y=1.02)
    fig.tight_layout(rect=(0, 0, 1, 0.94))
    fig.savefig("results/cost_fair.png", dpi=180, facecolor=SURFACE,
                bbox_inches="tight")
    print("wrote results/cost_fair.png")


if __name__ == "__main__":
    main()
