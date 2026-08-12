"""Render the dynamical-decoupling figure. Run: python3 plots_dd.py"""

import json

import matplotlib.pyplot as plt

from plots import BASELINE, INK, INK2, MUTED, SERIES, SURFACE, style_axis

COST_LABEL = {"uniform": "native qudit gate (uniform cost)",
              "ion": "2(d−1) MS gates (ion cost)"}
COST_COLOR = {"uniform": SERIES[5], "ion": SERIES[3]}
PANELS = [("shor", "Shor order finding"),
          ("qpe", "Eigenstate phase estimation")]


def main():
    with open("results/dd.json") as f:
        data = json.load(f)
    runs = data["runs"]

    fig, axes = plt.subplots(1, 2, figsize=(10.5, 4.5), sharey=True)
    fig.patch.set_facecolor(SURFACE)

    for ax, (algo, title) in zip(axes, PANELS):
        style_axis(ax)
        ax.axhline(0, color=INK2, linewidth=1.2)
        for cm in data["costs"]:
            xs, ys = [], []
            for s in data["scales"]:
                sig = {r["d"]: r["signal"] for r in runs
                       if r["algo"] == algo and r["cost"] == cm
                       and r["dephase_scale"] == s}
                xs.append(s)
                ys.append(sig[5] - sig[2])
            ax.plot(xs, ys, color=COST_COLOR[cm], linewidth=2, marker="o",
                    markersize=6, markeredgecolor=SURFACE, markeredgewidth=1,
                    label=COST_LABEL[cm])
            ax.annotate(f"{ys[-1]:+.2f}", xy=(xs[-1], ys[-1]),
                        xytext=(-2, 8), textcoords="offset points",
                        fontsize=8.5, color=INK2, ha="center")
            ax.annotate(f"{ys[0]:+.2f}", xy=(xs[0], ys[0]),
                        xytext=(20, -13), textcoords="offset points",
                        fontsize=8.5, color=INK2, ha="center")
        ax.invert_xaxis()          # left = free evolution, right = full echo
        ax.set_xlabel("dephasing remaining after refocusing\n"
                      "(1 = no DD,  0 = perfect echo / T₁ limit)",
                      fontsize=9.5, color=INK2)
        ax.set_title(title, fontsize=11, color=INK, pad=8)

    axes[0].set_ylabel("ququint advantage over qubits\n"
                       "(signal $d{=}5$ − signal $d{=}2$)",
                       fontsize=9.5, color=INK2)
    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(handles, labels, frameon=False, fontsize=9, labelcolor=INK2,
               loc="upper center", ncol=2, bbox_to_anchor=(0.5, 0.94))

    fig.suptitle("Echo helps qudits more than qubits — enough to flip the "
                 "verdict under linear-in-$d$ gate cost",
                 fontsize=12, color=INK, y=1.0)
    fig.tight_layout(rect=(0, 0, 1, 0.88))
    fig.savefig("results/dd.png", dpi=180, facecolor=SURFACE,
                bbox_inches="tight")
    print("wrote results/dd.png")


if __name__ == "__main__":
    main()
