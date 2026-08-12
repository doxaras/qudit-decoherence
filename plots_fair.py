"""Render the unbiased-instance demo sweep. Run: python3 plots_fair.py"""

import json

import matplotlib.pyplot as plt

from plots import BASELINE, INK, INK2, MUTED, SERIES, SURFACE, style_axis

# Measured two-qudit gate error per entangling operation on real hardware.
# Ions: Ringbauer 2022 / Hrmo 2023 report ~1e-3 for qudit MS gates.
# Transmons: Goss 2022 / Fischer 2023 qutrit CZ fidelities put it near 1e-2.
OPERATING_POINTS = {
    "transmon": [(1e-2, "transmons today")],
    "transmon_cal": [(1e-2, "transmons today")],
    "depolarizing": [(1e-3, "ions today")],
}

TITLES = {
    "transmon": "Transmon-like noise, idealized\n($\\Gamma_k \\propto k$, dephasing $\\propto (\\Delta\\mathrm{level})^2$)",
    "transmon_cal": "Transmon noise, calibrated\n($\\Gamma_k \\propto k^{0.7}$, max-level dephasing)",
    "depolarizing": "Uniform depolarizing\n(per particle, level-independent)",
}


def main():
    with open("results/fair_demo.json") as f:
        data = json.load(f)
    runs = data["runs"]

    fig, axes = plt.subplots(1, 3, figsize=(13.5, 4.4), sharey=True)
    fig.patch.set_facecolor(SURFACE)

    for ax, model in zip(axes, data["models"]):
        style_axis(ax)
        ax.axhline(0, color=BASELINE, linewidth=1)
        ends = []
        for d in data["bases"]:
            pts = sorted((r["strength"], r["signal"]) for r in runs
                         if r["noise_model"] == model and r["d"] == d)
            xs = [p[0] for p in pts]
            ys = [p[1] for p in pts]
            ax.plot(xs, ys, color=SERIES[d], linewidth=2, marker="o",
                    markersize=6, markeredgecolor=SURFACE, markeredgewidth=1,
                    label=f"$d = {d}$")
            ends.append([d, xs[-1], ys[-1]])
        ends.sort(key=lambda e: e[2])
        for i in range(1, len(ends)):
            if ends[i][2] - ends[i - 1][2] < 0.07:
                ends[i][2] = ends[i - 1][2] + 0.07
        for d, x_end, y_lab in ends:
            ax.annotate(f"$d = {d}$", xy=(x_end, y_lab), xytext=(7, 0),
                        textcoords="offset points", va="center",
                        fontsize=9, color=INK2)
        for x_op, lab in OPERATING_POINTS.get(model, []):
            ax.axvline(x_op, color=INK2, linewidth=1, linestyle=(0, (4, 3)),
                       zorder=0)
            ax.annotate(lab, xy=(x_op, 0.0), xycoords=("data", "axes fraction"),
                        xytext=(4, 6), textcoords="offset points",
                        fontsize=8, color=INK2)
        ax.set_xscale("log")
        ax.set_xlabel("noise strength per time-layer", fontsize=9.5,
                      color=INK2)
        ax.set_title(TITLES[model], fontsize=10, color=INK, pad=8)

    axes[0].set_ylabel("success above random guessing\n"
                       "(1 = noiseless, 0 = fully mixed)",
                       fontsize=9.5, color=INK2)
    axes[0].legend(frameon=False, fontsize=9, labelcolor=INK2,
                   loc="lower left")

    fig.suptitle(f"Order finding on an unbiased instance "
                 f"($N = {data['N']}$, $a = {data['a']}$, $r = {data['r']}$ — "
                 f"exactly representable in no base): qudits lead everywhere",
                 fontsize=12, color=INK, y=1.0)
    fig.tight_layout(rect=(0, 0, 1, 0.93))
    fig.savefig("results/fair_demo.png", dpi=180, facecolor=SURFACE,
                bbox_inches="tight")
    print("wrote results/fair_demo.png")


if __name__ == "__main__":
    main()
