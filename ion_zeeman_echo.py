"""Echo sweep over the Zeeman-dephasing failure mode: how much
refocusing restores the qudit ordering?

Companion to ion_zeeman_demo.py, which shows unmitigated collective-B
dephasing on the 40Ca+ encoding reverses the qudit advantage outright.
Real ion hardware never runs unmitigated: shielding and echoes
suppress the slow, structured collective-B component while leaving a
near-flat residual (the per-particle depolarizing convention). This
script prices the transition: total noise = depolarizing residual at
the operating point (s = 0.005 per carrier-layer) PLUS Zeeman
dephasing at eps * 0.003, with eps sweeping from 1 (no echo) to 0
(perfect echo). The `ion_mix` channel composes the two exactly (they
commute). The crossing eps* where each qudit's floor-corrected signal
recovers the qubit's is the echo-suppression factor the platform must
deliver.

Demo instance (N = 21, a = 2, r = 6), exact density-matrix evolution,
uniform and ion cost models, d = 2, 3, 5.

Writes results/ion_zeeman_echo.json. Run: python3 ion_zeeman_echo.py
"""

import json
import os
import time
from concurrent.futures import ProcessPoolExecutor

import numpy as np

from qudit_shor import (multiplicative_order, recovered_order, shor_config,
                        shor_run)

N, A = 21, 2
BASES = [2, 3, 5]
COSTS = ["uniform", "ion"]
S_DEPOL = 0.005          # flat residual, the marked ion operating point
S_ZEEMAN = 0.003         # unmitigated collective-B rate (demo reversal point)
EPS = [1.0, 0.5, 0.2, 0.1, 0.05, 0.02, 0.0]

RESULTS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results")


def uniform_floor(d: int, r: int) -> float:
    m, _ = shor_config(d, N)
    D = d ** m
    return sum(recovered_order(y, D, A, N) == r for y in range(D)) / D


def one(args):
    d, eps, cost = args
    t0 = time.time()
    if eps is None:  # noiseless baseline
        res = shor_run(d, a=A, N=N, cost_model=cost)
    else:
        res = shor_run(d, "ion_mix", S_DEPOL, a=A, N=N, cost_model=cost,
                       zeeman_tau=eps * S_ZEEMAN)
    return {"d": d, "eps": eps, "cost": cost,
            "success": float(res["success"]),
            "elapsed_s": round(time.time() - t0, 1)}


def main():
    os.makedirs(RESULTS, exist_ok=True)
    r = multiplicative_order(A, N)
    floors = {d: uniform_floor(d, r) for d in BASES}

    jobs = [(d, None, "uniform") for d in BASES]
    jobs += [(d, e, cost) for cost in COSTS for e in EPS for d in BASES]
    with ProcessPoolExecutor(max_workers=4) as ex:
        runs = list(ex.map(one, jobs))

    base = {x["d"]: x["success"] for x in runs if x["eps"] is None}
    out = {"N": N, "a": A, "r": r, "s_depol": S_DEPOL, "s_zeeman": S_ZEEMAN,
           "eps": EPS, "rows": [], "crossings": {}}

    print(f"depol residual {S_DEPOL}, Zeeman = eps * {S_ZEEMAN}")
    print(f"{'cost':>8} {'eps':>5} " + " ".join(f"{'d='+str(d):>8}" for d in BASES))
    table = {}
    for cost in COSTS:
        for e in EPS:
            sigs = []
            for d in BASES:
                succ = next(x["success"] for x in runs
                            if x["d"] == d and x["cost"] == cost
                            and x["eps"] == e)
                sig = (succ - floors[d]) / (base[d] - floors[d])
                sigs.append(sig)
                table[(cost, e, d)] = sig
                out["rows"].append({"d": d, "cost": cost, "eps": e,
                                    "success": succ, "signal": sig})
            print(f"{cost:>8} {e:>5} " + " ".join(f"{x:8.3f}" for x in sigs))

    # crossing eps* (descending eps): largest eps at which qudit >= qubit
    for cost in COSTS:
        for d in (3, 5):
            diffs = [(e, table[(cost, e, d)] - table[(cost, e, 2)])
                     for e in EPS]
            star = None
            for (e1, d1), (e0, d0) in zip(diffs, diffs[1:]):
                if d1 < 0 <= d0:
                    t = d0 / (d0 - d1)
                    star = e0 + t * (e1 - e0)
                    break
            if diffs[0][1] >= 0:
                star = ">= 1 (never lost)"
            out["crossings"][f"{cost}_d{d}"] = star
            print(f"eps* {cost} d={d}: {star if isinstance(star, str) else f'{star:.3f}'}")

    path = os.path.join(RESULTS, "ion_zeeman_echo.json")
    with open(path, "w") as f:
        json.dump(out, f, indent=1)
    print(f"\nwrote {path}")


if __name__ == "__main__":
    main()
