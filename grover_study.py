"""Grover: does the qudit advantage survive when depth stops compressing?

See grover.py for why this algorithm is the right falsification test.
Registered prediction, made before running: qudits win, by less than in
eigenstate QPE, because Grover compresses width but not oracle count.

Two parts:

  A. scaling -- signal vs log2(M), the matched-problem-size axis. This is
     the primary measurement: a single demo point cannot be read directly
     because M = d^n never matches across bases (the ququint at n = 3
     searches 125 items against the qubit's 64 at n = 6, and pays for it
     with 9 Grover iterations instead of 6).
  B. cost sensitivity at demo size -- does the same native-gate condition
     govern Grover as governs Shor and QPE?

Writes results/grover.json. Run: python3 grover_study.py
"""

import json
import os
import time
from concurrent.futures import ProcessPoolExecutor

import numpy as np

from grover import grover_run

SIZES = {2: [4, 6, 8], 3: [3, 4, 5], 5: [2, 3, 4]}
REGIMES = [("transmon_cal", 0.003), ("depolarizing", 0.005)]
N_MARKED = 8

DEMO_N = {2: 6, 3: 4, 5: 3}
COSTS = ["uniform", "ion", "pavlidis"]
DEMO_STRENGTHS = [0.002, 0.005, 0.01]
DEMO_MARKED = 12


def scaling_point(args):
    d, n, model, s = args
    t0 = time.time()
    base = grover_run(d, n, n_marked=N_MARKED)
    r = grover_run(d, n, model, s, n_marked=N_MARKED)
    span = base["success"] - r["floor"]
    r["baseline"] = base["success"]
    r["signal"] = (r["success"] - r["floor"]) / span
    r["signal_err"] = r["stderr"] / span
    r["bits"] = float(np.log2(r["M"]))
    r["elapsed_s"] = round(time.time() - t0, 1)
    return r


def cost_point(args):
    d, cm, model, s = args
    n = DEMO_N[d]
    t0 = time.time()
    base = grover_run(d, n, n_marked=DEMO_MARKED, cost_model=cm)
    r = grover_run(d, n, model, s, n_marked=DEMO_MARKED, cost_model=cm)
    span = base["success"] - r["floor"]
    r["baseline"] = base["success"]
    r["signal"] = (r["success"] - r["floor"]) / span
    r["signal_err"] = r["stderr"] / span
    r["bits"] = float(np.log2(r["M"]))
    r["elapsed_s"] = round(time.time() - t0, 1)
    return r


def main():
    os.makedirs("results", exist_ok=True)

    print("=== A. scaling (uniform cost) ===", flush=True)
    pts = [(d, n, m, s) for m, s in REGIMES
           for d, ns in SIZES.items() for n in ns]
    scaling = []
    with ProcessPoolExecutor(max_workers=4) as ex:
        for r in ex.map(scaling_point, pts):
            scaling.append(r)
            print(f"{r['noise_model']:13s} d={r['d']} n={r['n']} "
                  f"M={r['M']:4d} bits={r['bits']:5.2f} T={r['iterations']:2d} "
                  f"layers={r['n_layers']:6.0f} "
                  f"signal={r['signal']:6.3f}±{r['signal_err']:.3f} "
                  f"({r['elapsed_s']}s)", flush=True)

    print("\n=== B. cost sensitivity (demo size) ===", flush=True)
    pts = [(d, cm, m, s) for m, _ in REGIMES for cm in COSTS
           for s in DEMO_STRENGTHS for d in (2, 3, 5)]
    cost = []
    with ProcessPoolExecutor(max_workers=4) as ex:
        for r in ex.map(cost_point, pts):
            cost.append(r)
            print(f"{r['noise_model']:13s} {r['cost_model']:9s} d={r['d']} "
                  f"s={r['strength']:<6g} layers={r['n_layers']:7.1f} "
                  f"signal={r['signal']:6.3f}±{r['signal_err']:.3f} "
                  f"({r['elapsed_s']}s)", flush=True)

    with open("results/grover.json", "w") as f:
        json.dump({"sizes": SIZES, "regimes": REGIMES, "n_marked": N_MARKED,
                   "demo_n": DEMO_N, "costs": COSTS,
                   "demo_strengths": DEMO_STRENGTHS,
                   "scaling": scaling, "cost": cost}, f, indent=1)
    print("\nwrote results/grover.json")


if __name__ == "__main__":
    main()
