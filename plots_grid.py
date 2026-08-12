"""Render the grid-alignment figure. Run: python3 plots_grid.py

One instance per alignment class. The bar whose base can represent s/r
exactly (r | D = d^m) is marked with a hatch and a ring -- identity is never
carried by colour alone.
"""

import json

import matplotlib.pyplot as plt
import numpy as np

from plots import BASELINE, GRID, INK, INK2, MUTED, SERIES, SURFACE

NOISE = [("transmon_cal", "transmon / calibrated ladder"),
         ("depolarizing", "ions / per-particle noise")]
BASES = [2, 3, 5]


def main():
    with open("results/grid_alignment.json") as f:
        data = json.load(f)
    runs, meta = data["runs"], data["meta"]

    order = sorted({(r["r"], r["N"], r["a"]) for r in runs})
    labels, aligned = [], []
    for r_, N, a in order:
        who = [d for d in BASES if meta[f"{N},{a},{d}"]["exact_grid"]]
        aligned.append(who[0] if who else None)
        tag = f"aligned: $d\\!=\\!{who[0]}$" if who else "aligned: none"
        labels.append(f"$r = {r_}$\n$N\\!=\\!{N},\\ a\\!=\\!{a}$\n{tag}")

    fig, axes = plt.subplots(1, 2, figsize=(13.6, 5.0), sharey=True)
    fig.patch.set_facecolor(SURFACE)
    x = np.arange(len(order))
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

        for j, d in enumerate(BASES):
            vals, errs, hatches = [], [], []
            for i, (r_, N, a) in enumerate(order):
                run = next(z for z in runs if z["d"] == d and z["N"] == N
                           and z["a"] == a and z["noise_model"] == nm)
                mm = meta[f"{N},{a},{d}"]
                span = mm["baseline"] - mm["floor"]
                vals.append(run["signal"])
                errs.append(run["stderr"] / span)
                hatches.append(aligned[i] == d)
            bars = ax.bar(x + (j - 1) * width, vals, width * 0.9,
                          color=SERIES[d], label=f"$d = {d}$",
                          yerr=errs, ecolor=MUTED, capsize=2,
                          error_kw={"elinewidth": 1})
            for b, on in zip(bars, hatches):
                if on:
                    b.set_hatch("////")
                    b.set_edgecolor(SURFACE)
                    b.set_linewidth(2)

        ax.set_xticks(x)
        ax.set_xticklabels(labels, fontsize=8, color=INK2)
        ax.set_title(title, fontsize=11, color=INK, pad=8)
        ax.set_ylim(0, 1.15)

    axes[0].set_ylabel("success above random guessing\n"
                       "(1 = noiseless, 0 = fully mixed)",
                       fontsize=9.5, color=INK2)
    handles, lab = axes[0].get_legend_handles_labels()
    hatch_key = plt.Rectangle((0, 0), 1, 1, facecolor=BASELINE,
                              edgecolor=SURFACE, linewidth=2, hatch="////")
    axes[0].legend(handles + [hatch_key], lab + ["exact grid ($r \\mid D$)"],
                   frameon=False, fontsize=8.5, labelcolor=INK2,
                   loc="upper left", ncol=2)

    fig.suptitle("Grid alignment, not decoherence, decides who wins Shor: "
                 "the base that can represent $s/r$ exactly always leads",
                 fontsize=12, color=INK, y=1.0)
    fig.tight_layout(rect=(0, 0.03, 1, 0.94))
    fig.text(0.5, 0.005,
             "fixed per-layer strength: ladder 0.003, depolarizing 0.005 — "
             "at or below today's per-gate error "
             "(transmon two-qudit ~10$^{-2}$, ion ~10$^{-3}$)",
             ha="center", fontsize=8.5, color=MUTED)
    fig.savefig("results/grid_alignment.png", dpi=180, facecolor=SURFACE,
                bbox_inches="tight")
    print("wrote results/grid_alignment.png")


if __name__ == "__main__":
    main()
