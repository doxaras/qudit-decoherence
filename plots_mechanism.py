"""The mechanism-closing figure: signal splits by algorithm, fidelity does not.

Left column: floor-corrected decoded signal vs damage-weighted exposure --
the same abscissa for every point, yet Grover and Shor refuse to share a
curve (Shor's families are nearly flat: the decoder absorbs damage).
Right column: end-state fidelity on the same abscissa, log scale -- both
algorithms, all bases and sizes, on one exponential with amplitude ~1.

Run: python3 plots_mechanism.py  ->  results/mechanism.png
"""

import json

import matplotlib
matplotlib.use("Agg")
import matplotlib.lines as mlines
import matplotlib.pyplot as plt
import numpy as np

from exposure_collapse import abscissas, ent_fidelity, fit_exp, fit_nested, \
    load_points
from plots import BASELINE, INK, INK2, MUTED, SERIES, SURFACE, style_axis

TITLES = {"transmon_cal": "Transmon ladder, calibrated",
          "depolarizing": "Uniform depolarizing (per particle)"}
MARKERS = {"shor": "o", "grover": "^"}


def damage_x(p):
    return p["n_qudits"] * p["n_layers"] * (1 - ent_fidelity(p["d"], p["model"],
                                                             p["strength"]))


def main():
    sig_pts = load_points()
    fid_pts = json.load(open("results/fidelity_collapse.json"))["points"]

    fig, axes = plt.subplots(2, 2, figsize=(10.5, 8.2), sharex="col")
    fig.patch.set_facecolor(SURFACE)

    for row, model in enumerate(("transmon_cal", "depolarizing")):
        # ---- left: decoded signal, linear scale, per-algorithm fits
        ax = axes[row][0]
        style_axis(ax)
        sub = [p for p in sig_pts if p["model"] == model]
        x = np.array([abscissas(p)["X1_ent_infid"] for p in sub])
        y = np.array([p["signal"] for p in sub])
        algs = [p["alg"] for p in sub]
        for p, xi, yi in zip(sub, x, y):
            ax.plot(xi, yi, MARKERS[p["alg"]], color=SERIES[p["d"]],
                    markersize=6, markeredgecolor=SURFACE,
                    markeredgewidth=0.6, zorder=3)
        nest = fit_nested(x, y, algs)["shared_A_per_alg_k"]
        xs = np.linspace(0, x.max() * 1.02, 120)
        for alg, ls in (("shor", "-"), ("grover", "--")):
            ax.plot(xs, nest["A"] * np.exp(-nest["k"][alg] * xs), ls,
                    color=INK2, linewidth=1.4, zorder=2)
        pooled = fit_exp(x, y)
        ax.annotate(f"one curve: $R^2 = {pooled['r2']:.2f}$\n"
                    f"per-algorithm $k$: $R^2 = "
                    f"{fit_nested(x, y, algs)['shared_A_per_alg_k']['r2']:.2f}$",
                    xy=(0.97, 0.85), xycoords="axes fraction", ha="right",
                    fontsize=9, color=INK2)
        ax.set_ylabel(f"{TITLES[model]}\n\nfloor-corrected signal",
                      fontsize=9.5, color=INK2)
        ax.set_ylim(-0.05, 1.0)
        if row == 0:
            ax.set_title("Decoded signal — the algorithms split",
                         fontsize=11, color=INK, pad=8)

        # ---- right: end-state fidelity, log scale, one pooled fit
        ax = axes[row][1]
        style_axis(ax)
        sub = [p for p in fid_pts if p["model"] == model]
        x = np.array([damage_x(p) for p in sub])
        y = np.array([p["fidelity"] for p in sub])
        for p, xi, yi in zip(sub, x, y):
            ax.plot(xi, yi, MARKERS[p["alg"]], color=SERIES[p["d"]],
                    markersize=6, markeredgecolor=SURFACE,
                    markeredgewidth=0.6, zorder=3)
        f = fit_exp(x, y)
        xs = np.linspace(0, x.max() * 1.02, 120)
        ax.plot(xs, f["A"] * np.exp(-f["k"] * xs), "-", color=INK2,
                linewidth=1.4, zorder=2)
        ax.set_yscale("log")
        ax.annotate(f"$A = {f['A']:.2f}$, $R^2 = {f['r2']:.2f}$",
                    xy=(0.97, 0.85), xycoords="axes fraction", ha="right",
                    fontsize=9, color=INK2)
        ax.set_ylabel("end-state fidelity", fontsize=9.5, color=INK2)
        if row == 0:
            ax.set_title("End-state fidelity — one curve",
                         fontsize=11, color=INK, pad=8)

    for ax in axes[1]:
        ax.set_xlabel("damage-weighted exposure\n"
                      "carriers × layers × $(1 - F_{\\mathrm{e}})$",
                      fontsize=9.5, color=INK2)

    handles = [mlines.Line2D([], [], marker=MARKERS[a], linestyle=ls,
                             color=INK2, markersize=6, linewidth=1.4,
                             label=lab)
               for a, lab, ls in (("shor", "Shor (fit —)", "-"),
                                  ("grover", "Grover (fit – –)", "--"))]
    handles += [mlines.Line2D([], [], marker="s", linestyle="none",
                              color=SERIES[d], markersize=7, label=f"$d = {d}$")
                for d in (2, 3, 5)]
    fig.legend(handles=handles, frameon=False, fontsize=9, labelcolor=INK2,
               loc="upper center", ncol=5, bbox_to_anchor=(0.5, 0.945))

    fig.suptitle("Damage-weighted exposure is a law for state decay; "
                 "the decoder separates the algorithms",
                 fontsize=12.5, color=INK, y=0.985)
    fig.tight_layout(rect=(0, 0, 1, 0.92))
    fig.savefig("results/mechanism.png", dpi=180, facecolor=SURFACE,
                bbox_inches="tight")
    print("wrote results/mechanism.png")


if __name__ == "__main__":
    main()
