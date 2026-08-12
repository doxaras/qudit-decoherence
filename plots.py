"""Render figures from results/results.json. Run: python3 plots.py"""

import json

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from qudit_shor import multiplicative_order, recovered_order, shor_config


def uniform_floor(d: int, a: int = 7, N: int = 15) -> float:
    """Success probability of a uniformly random outcome (continued
    fractions still 'recover' the order surprisingly often at demo size)."""
    m, _ = shor_config(d, N)
    D = d ** m
    r = multiplicative_order(a, N)
    return sum(recovered_order(y, D, a, N) == r for y in range(D)) / D

# Reference dataviz palette (light mode)
SURFACE = "#fcfcfb"
INK = "#0b0b0b"
INK2 = "#52514e"
MUTED = "#898781"
GRID = "#e1e0d9"
BASELINE = "#c3c2b7"
SERIES = {2: "#2a78d6", 3: "#eb6834", 5: "#1baf7a"}  # slots 1-3

MODEL_TITLES = {
    "transmon": "Transmon-like noise\n(level-k decay rate ∝ k, dephasing ∝ (Δlevel)²)",
    "depolarizing": "Uniform depolarizing\n(same per-qudit rate, level-independent)",
}


def style_axis(ax):
    ax.set_facecolor(SURFACE)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    for side in ("left", "bottom"):
        ax.spines[side].set_color(BASELINE)
    ax.tick_params(colors=MUTED, labelsize=9)
    ax.grid(axis="y", color=GRID, linewidth=0.8)
    ax.set_axisbelow(True)


def main():
    with open("results/results.json") as f:
        data = json.load(f)

    runs = data["runs"]
    baselines = {r["d"]: r["success"] for r in runs if r["noise_model"] is None}
    floors = {d: uniform_floor(d) for d in data["bases"]}

    # ---- Figure 1: floor-corrected success vs noise strength, per model
    fig, axes = plt.subplots(1, 2, figsize=(10.5, 4.4), sharey=True)
    fig.patch.set_facecolor(SURFACE)

    for ax, model in zip(axes, data["models"]):
        style_axis(ax)
        ax.axhline(0, color=BASELINE, linewidth=1)
        ends = []
        for d in data["bases"]:
            span = baselines[d] - floors[d]
            xs = [0.0] + data["strengths"]
            ys = [1.0] + [(r["success"] - floors[d]) / span for r in runs
                          if r["noise_model"] == model and r["d"] == d]
            ax.plot(xs, ys, color=SERIES[d], linewidth=2, marker="o",
                    markersize=6, markeredgecolor=SURFACE, markeredgewidth=1,
                    label=f"d = {d}")
            ends.append([d, xs[-1], ys[-1]])
        # direct end labels, dodged vertically so they never collide
        ends.sort(key=lambda e: e[2])
        for i in range(1, len(ends)):
            if ends[i][2] - ends[i - 1][2] < 0.07:
                ends[i][2] = ends[i - 1][2] + 0.07
        for d, x_end, y_lab in ends:
            ax.annotate(f"d = {d}", xy=(x_end, y_lab), xytext=(8, 0),
                        textcoords="offset points", va="center",
                        fontsize=9, color=INK2)
        ax.set_title(MODEL_TITLES[model], fontsize=10.5, color=INK, pad=10)
        ax.set_xlabel("noise strength per time-layer", fontsize=9.5, color=INK2)
        ax.set_xlim(-0.001, max(data["strengths"]) * 1.16)
        ax.set_ylim(-0.12, 1.05)

    axes[0].set_ylabel("success above random guessing\n(1 = noiseless, 0 = fully mixed)",
                       fontsize=9.5, color=INK2)
    axes[0].legend(frameon=False, fontsize=9, labelcolor=INK2, loc="lower left")
    fig.suptitle("Order finding for N = 15 under decoherence: qubits vs qutrits vs ququints",
                 fontsize=12, color=INK, x=0.5, y=1.0)
    fig.tight_layout(rect=(0, 0, 1, 0.97))
    fig.savefig("results/success_vs_noise.png", dpi=180,
                facecolor=SURFACE, bbox_inches="tight")
    print("wrote results/success_vs_noise.png")

    # ---- Figure 2: resource counts (single-measure bars, single hue)
    res = {r["d"]: r for r in runs if r["noise_model"] is None}
    metrics = [("n_qudits", "physical qudits"),
               ("n_gates", "gates"),
               ("n_layers", "serial time-layers")]
    fig, axes = plt.subplots(1, 3, figsize=(9.5, 3.2))
    fig.patch.set_facecolor(SURFACE)
    for ax, (key, title) in zip(axes, metrics):
        style_axis(ax)
        ax.grid(False)
        labels = [f"d = {d}" for d in data["bases"]]
        vals = [res[d][key] for d in data["bases"]]
        bars = ax.bar(labels, vals, width=0.55, color="#2a78d6")
        for b, v in zip(bars, vals):
            ax.annotate(str(v), xy=(b.get_x() + b.get_width() / 2, v),
                        xytext=(0, 3), textcoords="offset points",
                        ha="center", fontsize=9.5, color=INK)
        ax.set_title(title, fontsize=10, color=INK)
        ax.set_yticks([])
        ax.spines["left"].set_visible(False)
        ax.tick_params(axis="x", labelsize=9.5, labelcolor=INK2)
    fig.suptitle("Same problem (N = 15), shrinking circuit", fontsize=11.5,
                 color=INK, y=1.02)
    fig.tight_layout()
    fig.savefig("results/resources.png", dpi=180,
                facecolor=SURFACE, bbox_inches="tight")
    print("wrote results/resources.png")


if __name__ == "__main__":
    main()
