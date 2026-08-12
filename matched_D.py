"""Matched control dimension: the demo-grid comparison with D equalized.

Round-2 referee point (Gottesman): the demo-size grid (Table I and its
descendants) compares D = 64/81/125, and Sec. VII shows decoder
tolerance grows linearly in D — the ququint enters the central table
with 2x the qubit's acceptance set (|A| = 16 vs 8). This script prices
that confound directly: d = 2 at m = 7 gives D = 128, matching the
ququint's 125 within 2.4%, and d = 3 at m = 4/5 brackets it (81/243).

Unbiased instance (N = 21, a = 2, r = 6), exact density-matrix
evolution, uniform cost, both marked operating points.

Writes results/matched_D.json. Run: python3 matched_D.py
"""

import json
import os
import time
from concurrent.futures import ProcessPoolExecutor

import numpy as np

from qudit_shor import (apply_cost_model, build_shor_gates, channels_by_cost,
                        control_probs, initial_state, multiplicative_order,
                        recovered_order, run_circuit, shor_config)

N, A = 21, 2
CONFIGS = [(2, 6), (2, 7), (3, 4), (3, 5), (5, 3)]  # (d, m); D = 64..243
POINTS = [("transmon_cal", 0.003), ("depolarizing", 0.005)]

RESULTS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results")


def shor_run_m(d: int, m: int, model, s: float) -> float:
    """shor_run with explicit control-register size m (uniform cost)."""
    _, w = shor_config(d, N)
    dims = [d] * (m + w)
    gates = apply_cost_model(build_shor_gates(d, m, w, A, N), d, "uniform")
    rho = initial_state(dims, m, d, w)
    E = channels_by_cost(d, gates, model, s) if model and s > 0 else None
    rho = run_circuit(dims, gates, rho, E)
    probs = control_probs(rho, d, m, w)
    D = d ** m
    r = multiplicative_order(A, N)
    return float(sum(probs[y] for y in range(D)
                     if recovered_order(y, D, A, N) == r))


def one(args):
    d, m, model, s = args
    t0 = time.time()
    succ = shor_run_m(d, m, model, s)
    return {"d": d, "m": m, "model": model, "strength": s, "success": succ,
            "elapsed_s": round(time.time() - t0, 1)}


def main():
    os.makedirs(RESULTS, exist_ok=True)
    r = multiplicative_order(A, N)
    floors = {}
    for d, m in CONFIGS:
        D = d ** m
        floors[(d, m)] = sum(recovered_order(y, D, A, N) == r
                             for y in range(D)) / D

    jobs = [(d, m, None, 0.0) for d, m in CONFIGS]
    jobs += [(d, m, model, s) for d, m in CONFIGS for model, s in POINTS]
    with ProcessPoolExecutor(max_workers=3) as ex:
        runs = list(ex.map(one, jobs))

    base = {(x["d"], x["m"]): x["success"] for x in runs if x["model"] is None}
    out = {"N": N, "a": A, "r": r, "rows": []}
    print(f"{'d':>2} {'m':>2} {'D':>4} {'floor':>6} " +
          " ".join(f"{mo:>13}" for mo, _ in POINTS))
    for d, m in CONFIGS:
        D = d ** m
        cells = []
        for model, s in POINTS:
            succ = next(x["success"] for x in runs
                        if x["d"] == d and x["m"] == m and x["model"] == model)
            span = base[(d, m)] - floors[(d, m)]
            sig = (succ - floors[(d, m)]) / span
            out["rows"].append({"d": d, "m": m, "D": D, "model": model,
                                "strength": s, "success": succ,
                                "floor": floors[(d, m)],
                                "baseline": base[(d, m)], "signal": sig})
            cells.append(f"{sig:13.3f}")
        print(f"{d:>2} {m:>2} {D:>4} {floors[(d, m)]:>6.3f} " + " ".join(cells))

    path = os.path.join(RESULTS, "matched_D.json")
    with open(path, "w") as f:
        json.dump(out, f, indent=1)
    print(f"\nwrote {path}")


if __name__ == "__main__":
    main()
