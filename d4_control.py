"""Composite-dimension control: d = 4 alongside the primes.

Referee request (Gottesman-style review, major comment 4): nothing in
the algorithms or channels uses primality, so the prime restriction
(d = 2, 3, 5, 7) is inherited from the fault-tolerance motivation, not
tested. A d = 4 point isolates carrier count from number theory: if
the advantage tracks width-and-depth compression, d = 4 should land
between d = 3 and d = 5; if primality mattered dynamically, it should
misbehave.

Demo instance (N = 21, a = 2, r = 6; r divides no power of 2, 3, 4 or
5, so d = 4 is as unaligned as the others — residual misalignment is
reported for confirmation). Exact density-matrix evolution, uniform
cost, both marked operating points.

Writes results/d4_control.json. Run: python3 d4_control.py
"""

import json
import os
import time
from concurrent.futures import ProcessPoolExecutor

import numpy as np

from qudit_shor import (multiplicative_order, recovered_order, shor_config,
                        shor_run)

N, A = 21, 2
BASES = [2, 3, 4, 5]
POINTS = [("transmon_cal", 0.003), ("depolarizing", 0.005)]

RESULTS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results")


def residual(D: int, r: int) -> float:
    x = D * np.arange(1, r) / r
    return float(np.abs(x - np.round(x)).mean())


def uniform_floor(d: int, r: int) -> float:
    m, _ = shor_config(d, N)
    D = d ** m
    return sum(recovered_order(y, D, A, N) == r for y in range(D)) / D


def one(args):
    d, model, s = args
    t0 = time.time()
    res = shor_run(d, model, s, a=A, N=N) if model else shor_run(d, a=A, N=N)
    return {"d": d, "model": model, "strength": s,
            "success": float(res["success"]),
            "elapsed_s": round(time.time() - t0, 1)}


def main():
    os.makedirs(RESULTS, exist_ok=True)
    r = multiplicative_order(A, N)
    jobs = [(d, None, 0.0) for d in BASES]
    jobs += [(d, model, s) for d in BASES for model, s in POINTS]

    with ProcessPoolExecutor(max_workers=4) as ex:
        runs = list(ex.map(one, jobs))

    base = {x["d"]: x["success"] for x in runs if x["model"] is None}
    floors = {d: uniform_floor(d, r) for d in BASES}

    out = {"N": N, "a": A, "r": r, "rows": []}
    print(f"{'d':>2} {'m':>2} {'D':>4} {'resid':>6} {'model':>13} "
          f"{'succ':>6} {'signal':>7}")
    for model, s in POINTS:
        for d in BASES:
            m, _ = shor_config(d, N)
            D = d ** m
            succ = next(x["success"] for x in runs
                        if x["d"] == d and x["model"] == model)
            sig = (succ - floors[d]) / (base[d] - floors[d])
            out["rows"].append({"d": d, "m": m, "D": D,
                                "residual": residual(D, r),
                                "model": model, "strength": s,
                                "success": succ, "floor": floors[d],
                                "baseline": base[d], "signal": sig})
            print(f"{d:>2} {m:>2} {D:>4} {residual(D, r):>6.3f} {model:>13} "
                  f"{succ:>6.3f} {sig:>7.3f}")

    path = os.path.join(RESULTS, "d4_control.json")
    with open(path, "w") as f:
        json.dump(out, f, indent=1)
    print(f"\nwrote {path}")


if __name__ == "__main__":
    main()
