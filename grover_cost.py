"""Grover cost sensitivity, measured across sizes so it can be size-matched.

The cost block in grover_study.py runs one register size per base, which
cannot be read across bases: M = d^n never matches, so at n = 6/4/3 the
ququint is searching 125 items against the qubit's 64 and pays 9 Grover
iterations instead of 6. This runs the full size ladder under each cost
model so signals can be interpolated onto a common log2(M) axis, the same
way the scaling studies are read.

Writes results/grover_cost.json. Run: python3 grover_cost.py
"""

import json
import os
import time
from concurrent.futures import ProcessPoolExecutor

import numpy as np

from grover import grover_run

SIZES = {2: [4, 6, 8], 3: [3, 4, 5], 5: [2, 3, 4]}
REGIMES = [("transmon_cal", 0.003), ("depolarizing", 0.005)]
COSTS = ["uniform", "ion", "pavlidis"]
N_MARKED = 8


def one(args):
    d, n, cm, model, s = args
    t0 = time.time()
    base = grover_run(d, n, n_marked=N_MARKED, cost_model=cm)
    r = grover_run(d, n, model, s, n_marked=N_MARKED, cost_model=cm)
    span = base["success"] - r["floor"]
    r["baseline"] = base["success"]
    r["signal"] = (r["success"] - r["floor"]) / span
    r["signal_err"] = r["stderr"] / span
    r["bits"] = float(np.log2(r["M"]))
    r["elapsed_s"] = round(time.time() - t0, 1)
    return r


def main():
    os.makedirs("results", exist_ok=True)
    pts = [(d, n, cm, m, s) for m, s in REGIMES for cm in COSTS
           for d, ns in SIZES.items() for n in ns]
    runs = []
    with ProcessPoolExecutor(max_workers=4) as ex:
        for r in ex.map(one, pts):
            runs.append(r)
            print(f"{r['noise_model']:13s} {r['cost_model']:9s} d={r['d']} "
                  f"n={r['n']} bits={r['bits']:5.2f} "
                  f"layers={r['n_layers']:7.1f} "
                  f"signal={r['signal']:6.3f}±{r['signal_err']:.3f} "
                  f"({r['elapsed_s']}s)", flush=True)

    with open("results/grover_cost.json", "w") as f:
        json.dump({"sizes": SIZES, "regimes": REGIMES, "costs": COSTS,
                   "n_marked": N_MARKED, "runs": runs}, f, indent=1)
    print("\nwrote results/grover_cost.json")


if __name__ == "__main__":
    main()
