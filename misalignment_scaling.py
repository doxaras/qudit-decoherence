"""Residual grid misalignment across the register-size scaling sweep.

Closes a referee objection against Sec. V of the paper. Shor's d = 3
signal is flat in register size, and we attribute that to decoder
tolerance. But D = d^m changes with m, so a sceptic can ask whether the
flatness is instead residual grid misalignment drifting favourably with
m -- exactly the confound that overturned the first version of this
study (docs/GRID_ALIGNMENT.md). If d = 3's misalignment fell as the
register grew, the flat signal would be an arithmetic artifact again.

Residual misalignment is a pure number-theoretic property of (d, m, r):
the mean distance of the r-1 target phases s/r from the nearest base-d
grid point, in grid units, exactly as pinned in
test_qudit_shor.py::test_grid_alignment. No simulation is involved, so
this costs milliseconds.

Writes results/misalignment_scaling.json. Run: python3 misalignment_scaling.py
"""

import json
import os

import numpy as np

from qudit_shor import multiplicative_order

RESULTS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results")

# The sweep of paper Fig. 3 / results/scaling_fair_1000.json, plus the
# second unbiased benchmark instance at its demo size.
SWEEP = {2: [6, 8, 10, 12], 3: [4, 5, 6, 7, 8], 5: [3, 4, 5]}
INSTANCES = [(21, 2), (29, 16)]


def residual(D: int, r: int) -> float:
    """Mean distance of the r-1 phases s/r to the nearest grid point."""
    x = D * np.arange(1, r) / r
    return float(np.abs(x - np.round(x)).mean())


def main():
    out = {"instances": [], "note": (
        "residual misalignment in grid units; 0 = exact alignment, "
        "0.5 = worst case")}

    for N, a in INSTANCES:
        r = multiplicative_order(a, N)
        entry = {"N": N, "a": a, "r": r, "per_base": {}}
        print(f"\nN = {N}, a = {a}, r = {r}")
        print(f"{'d':>2} {'m':>3} {'D':>6} {'aligned':>8} {'residual':>9}")
        for d, ms in SWEEP.items():
            rows = []
            for m in ms:
                D = d ** m
                rows.append({"m": m, "D": D, "exact_grid": D % r == 0,
                             "residual": residual(D, r)})
                print(f"{d:>2} {m:>3} {D:>6} {str(D % r == 0):>8} "
                      f"{rows[-1]['residual']:>9.4f}")
            vals = [x["residual"] for x in rows]
            entry["per_base"][str(d)] = {
                "rows": rows,
                "min": min(vals), "max": max(vals),
                "spread": max(vals) - min(vals),
                "constant_in_m": bool(max(vals) - min(vals) < 1e-12),
            }
        out["instances"].append(entry)

    print("\n=== Verdict: is residual misalignment constant across the sweep? ===")
    for entry in out["instances"]:
        for d, rec in entry["per_base"].items():
            flag = "CONSTANT" if rec["constant_in_m"] else "VARIES"
            print(f"  N={entry['N']} d={d}: {flag} "
                  f"(min {rec['min']:.4f}, max {rec['max']:.4f}, "
                  f"spread {rec['spread']:.2e})")

    path = os.path.join(RESULTS, "misalignment_scaling.json")
    with open(path, "w") as f:
        json.dump(out, f, indent=1)
    print(f"\nwrote {path}")


if __name__ == "__main__":
    main()
