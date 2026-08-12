"""Render the gate-cost sensitivity figure. Run: python3 plots_cost.py"""

import json

import matplotlib.pyplot as plt
import numpy as np

from plots import BASELINE, GRID, INK, INK2, MUTED, SERIES, SURFACE

STRENGTH = 0.005
COSTS = ["uniform", "ion", "pavlidis"]
COST_LABELS = ["uniform\n(native qudit gate)", "ion\n(2(d−1) MS gates)",
               "pavlidis\n(d² decomposition)"]
NOISE = [("depolarizing", "ions / per-particle noise"),
         ("transmon_cal", "transmon / calibrated ladder")]


def main():
    with open("results/cost_sensitivity.json") as f:
        runs = json.load(f)["runs"]

    def sig(algo, nm, cm, d):
        return next(r["signal"] for r in runs if r["algo"] == algo
                    and r["noise"] == nm and r["cost"] == cm
                    and r["strength"] == STRENGTH and r["d"] == d)

    fig, axes = plt.subplots(1, 2, figsize=(10.5, 4.6), sharey=True)
    fig.patch.set_facecolor(SURFACE)
    x = np.arange(len(COSTS))
    width = 0.36

    for ax, algo, title in zip(axes, ("shor", "qpe"),
                               ("Shor order finding",
                                "Eigenstate phase estimation")):
        ax.set_facecolor(SURFACE)
        for side in ("top", "right", "left"):
            ax.spines[side].set_visible(False)
        ax.spines["bottom"].set_color(BASELINE)
        ax.tick_params(colors=MUTED, labelsize=9)
        ax.grid(axis="y", color=GRID, linewidth=0.8)
        ax.set_axisbelow(True)
        ax.axhline(0, color=BASELINE, linewidth=1.2)

        for i, (nm, lab) in enumerate(NOISE):
            vals = [sig(algo, nm, cm, 5) - sig(algo, nm, cm, 2) for cm in COSTS]
            bars = ax.bar(x + (i - 0.5) * width, vals, width * 0.92,
                          color=SERIES[2 if i == 0 else 3], label=lab)
            for b, v in zip(bars, vals):
                ax.annotate(f"{v:+.2f}",
                            xy=(b.get_x() + b.get_width() / 2, v),
                            xytext=(0, 3 if v >= 0 else -12),
                            textcoords="offset points", ha="center",
                            fontsize=8.5, color=INK)
        ax.set_xticks(x)
        ax.set_xticklabels(COST_LABELS, fontsize=8.5, color=INK2)
        ax.set_title(title, fontsize=11, color=INK, pad=8)

    axes[0].set_ylabel("ququint advantage over qubits\n(signal $d{=}5$ − signal $d{=}2$)",
                       fontsize=9.5, color=INK2)
    axes[0].legend(frameon=False, fontsize=8.5, labelcolor=INK2,
                   loc="lower left")
    fig.suptitle("Does the qudit advantage survive realistic gate costs? "
                 "Only if entangling cost grows no faster than linearly in d",
                 fontsize=11.5, color=INK, y=1.0)
    fig.tight_layout(rect=(0, 0, 1, 0.95))
    fig.savefig("results/cost_sensitivity.png", dpi=180, facecolor=SURFACE,
                bbox_inches="tight")
    print("wrote results/cost_sensitivity.png")


if __name__ == "__main__":
    main()
