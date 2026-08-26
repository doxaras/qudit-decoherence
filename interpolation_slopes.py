"""Recompute the entanglement-interpolation slopes the paper quotes.

The falsified-mechanism paragraph in Sec.~\\ref{sec:mechanism} quotes
the slope of the ququint advantage (signal at d=5 minus signal at d=2)
against control--work entanglement entropy, fitted over K = 1..4 for
each of the four noise/cost conditions. Like the size-scaling numbers
before scaling_claims.py existed, that slope was originally produced by
ad-hoc analysis; this script is the committed step that regenerates it
from results/interpolation.json.

Weighted least squares of (signal_5 - signal_2) on entropy bits, one
fit per (noise, cost) condition; per-base signal slopes are recorded
too so the d=5-vs-d=2 attribution is checkable.

Run: python3 interpolation_slopes.py [results_dir]
Writes <results_dir>/interpolation_slopes.json
"""

import json
import os
import sys

import numpy as np

ROOT = os.path.dirname(os.path.abspath(__file__))


def wfit(x, y, err):
    x, y = np.asarray(x, float), np.asarray(y, float)
    w = 1.0 / np.asarray(err, float) ** 2
    W, Wx, Wy = w.sum(), (w * x).sum(), (w * y).sum()
    Wxx, Wxy = (w * x * x).sum(), (w * x * y).sum()
    det = W * Wxx - Wx * Wx
    slope = (W * Wxy - Wx * Wy) / det
    intercept = (Wxx * Wy - Wx * Wxy) / det
    return {"slope": slope, "slope_se": float(np.sqrt(W / det)),
            "intercept": intercept}


def main():
    resdir = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "results")
    if not os.path.isabs(resdir):
        resdir = os.path.join(ROOT, resdir)
    with open(os.path.join(resdir, "interpolation.json")) as f:
        data = json.load(f)
    runs = data["runs"]

    out = {"results_dir": resdir, "advantage_slopes": {},
           "per_base_slopes": {}}
    print(f"=== entanglement-interpolation slopes from "
          f"{os.path.basename(resdir)} ===\n")
    for noise in data["noise"]:
        for cost in data["costs"]:
            key = f"{noise}_{cost}"
            sel = [r for r in runs
                   if r["noise_model"] == noise and r["cost_model"] == cost]

            per = {}
            for d in data["bases"]:
                rows = sorted((r for r in sel if r["d"] == d),
                              key=lambda r: r["K"])
                per[str(d)] = wfit([r["entropy_bits"] for r in rows],
                                   [r["signal"] for r in rows],
                                   [r["signal_err"] for r in rows])
            out["per_base_slopes"][key] = per

            pts = []
            for K in data["Ks"]:
                r5 = next(r for r in sel if r["d"] == 5 and r["K"] == K)
                r2 = next(r for r in sel if r["d"] == 2 and r["K"] == K)
                pts.append((0.5 * (r5["entropy_bits"] + r2["entropy_bits"]),
                            r5["signal"] - r2["signal"],
                            float(np.hypot(r5["signal_err"],
                                           r2["signal_err"]))))
            adv = wfit(*zip(*pts))
            adv["points"] = [{"bits": p[0], "advantage": p[1], "err": p[2]}
                             for p in pts]
            out["advantage_slopes"][key] = adv
            print(f"-- {noise}, {cost} --")
            print(f"   d=5-d=2 advantage: {adv['slope']:+.4f}"
                  f"+-{adv['slope_se']:.4f}/bit   " + "  ".join(
                      f"{p['bits']:.2f}b {p['advantage']:+.3f}"
                      for p in adv["points"]))
            print("   per-base signal slopes: " + "  ".join(
                f"d={d}: {per[str(d)]['slope']:+.4f}"
                f"+-{per[str(d)]['slope_se']:.4f}"
                for d in data["bases"]))
            print()

    path = os.path.join(resdir, "interpolation_slopes.json")
    with open(path, "w") as f:
        json.dump(out, f, indent=1)
    print(f"wrote {path}")


if __name__ == "__main__":
    main()
