"""Render a register-size scaling figure.

Run: python3 plots_scaling.py [results/scaling.json results/scaling.png "title"]
Defaults render the Shor scaling study; pass the QPE JSON for the generic
phase-estimation variant.
"""

import json
import sys

import numpy as np

from plots import (BASELINE, INK, INK2, MODEL_TITLES, MUTED, SERIES, SURFACE,
                   style_axis)
import matplotlib.pyplot as plt


def main(json_path="results/scaling.json", png_path="results/scaling.png",
         title="Does the qudit advantage grow with problem size?"):
    with open(json_path) as f:
        data = json.load(f)

    sizes = {int(k): v for k, v in data["sizes"].items()}
    fig, axes = plt.subplots(1, 2, figsize=(10.5, 4.4), sharey=True)
    fig.patch.set_facecolor(SURFACE)

    for ax, (model, strength) in zip(axes, data["models"]):
        style_axis(ax)
        ax.axhline(0, color=BASELINE, linewidth=1)
        ends = []
        for d, ms in sizes.items():
            xs, ys, es = [], [], []
            for m in ms:
                b = data["baselines"][f"{d},{m}"]
                r = next(x for x in data["runs"]
                         if x["d"] == d and x["m"] == m
                         and x["noise_model"] == model)
                span = b["success"] - r["floor"]
                xs.append(m * np.log2(d))
                ys.append((r["success"] - r["floor"]) / span)
                es.append(r["stderr"] / span)
            ax.errorbar(xs, ys, yerr=es, color=SERIES[d], linewidth=2,
                        marker="o", markersize=6, markeredgecolor=SURFACE,
                        markeredgewidth=1, capsize=3, elinewidth=1,
                        ecolor=MUTED, label=f"d = {d}")
            ends.append([d, xs[-1], ys[-1]])
        ends.sort(key=lambda e: e[2])
        for i in range(1, len(ends)):
            if ends[i][2] - ends[i - 1][2] < 0.07:
                ends[i][2] = ends[i - 1][2] + 0.07
        for d, x_end, y_lab in ends:
            ax.annotate(f"d = {d}", xy=(x_end, y_lab), xytext=(8, 0),
                        textcoords="offset points", va="center",
                        fontsize=9, color=INK2)
        ax.set_title(MODEL_TITLES[model] + f"\nstrength {strength}/layer",
                     fontsize=10, color=INK, pad=10)
        ax.set_xlabel("phase-estimation precision, log₂ D (bits)",
                      fontsize=9.5, color=INK2)

    axes[0].set_ylim(-0.12, 1.05)
    axes[0].set_ylabel("success above random guessing\n(1 = noiseless, 0 = fully mixed)",
                       fontsize=9.5, color=INK2)
    axes[0].legend(frameon=False, fontsize=9, labelcolor=INK2,
                   loc="lower left")
    fig.suptitle(title, fontsize=12, color=INK, x=0.5, y=1.0)
    fig.tight_layout(rect=(0, 0, 1, 0.96))
    fig.savefig(png_path, dpi=180, facecolor=SURFACE, bbox_inches="tight")
    print(f"wrote {png_path}")


if __name__ == "__main__":
    main(*sys.argv[1:4])
