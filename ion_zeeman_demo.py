"""Zeeman-structured ion dephasing: does the qudit advantage survive the
REAL anisotropy of the trapped-ion encoding?

Referee request (Innsbruck-style review, major comment 2): the
per-particle depolarizing channel flattens structure the platform
actually has — pair-dependent dephasing tracking the magnetic
sensitivity of specific Zeeman pairs. The `ion_zeeman` channel
(qudit_shor.py) implements collective-B dephasing on the Ringbauer
40Ca+ encoding exactly: pair (j,k) dephases at
strength * ((c_j - c_k)/(c_0 - c_1))^2 with c = g*m_J, spanning 1x to
49x across the d = 5 pairs. If the qudit ordering survives THIS
channel, the depolarizing convention was not doing the work.

Demo instance (N = 21, a = 2, r = 6), exact density-matrix evolution,
ion and uniform cost models, d = 2, 3, 5.

Writes results/ion_zeeman_demo.json. Run: python3 ion_zeeman_demo.py
"""

import json
import os
import time
from concurrent.futures import ProcessPoolExecutor

from qudit_shor import (multiplicative_order, recovered_order, shor_config,
                        shor_run)

N, A = 21, 2
BASES = [2, 3, 5]
COSTS = ["uniform", "ion"]
STRENGTHS = [0.001, 0.003, 0.005, 0.01]

RESULTS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results")


def uniform_floor(d: int, r: int) -> float:
    m, _ = shor_config(d, N)
    D = d ** m
    return sum(recovered_order(y, D, A, N) == r for y in range(D)) / D


def one(args):
    d, s, cost = args
    t0 = time.time()
    res = (shor_run(d, "ion_zeeman", s, a=A, N=N, cost_model=cost) if s
           else shor_run(d, a=A, N=N, cost_model=cost))
    return {"d": d, "strength": s, "cost": cost,
            "success": float(res["success"]),
            "elapsed_s": round(time.time() - t0, 1)}


def main():
    os.makedirs(RESULTS, exist_ok=True)
    r = multiplicative_order(A, N)
    floors = {d: uniform_floor(d, r) for d in BASES}

    jobs = [(d, 0.0, "uniform") for d in BASES]
    jobs += [(d, s, cost) for cost in COSTS for s in STRENGTHS for d in BASES]
    with ProcessPoolExecutor(max_workers=4) as ex:
        runs = list(ex.map(one, jobs))

    base = {x["d"]: x["success"] for x in runs if x["strength"] == 0.0}
    out = {"N": N, "a": A, "r": r, "strengths": STRENGTHS, "rows": []}
    print(f"{'cost':>8} {'s':>6} " + " ".join(f"{'d='+str(d):>8}" for d in BASES)
          + "   (floor-corrected signal)")
    for cost in COSTS:
        for s in STRENGTHS:
            sigs = []
            for d in BASES:
                succ = next(x["success"] for x in runs
                            if x["d"] == d and x["cost"] == cost
                            and x["strength"] == s)
                sig = (succ - floors[d]) / (base[d] - floors[d])
                sigs.append(sig)
                out["rows"].append({"d": d, "cost": cost, "strength": s,
                                    "success": succ, "signal": sig})
            print(f"{cost:>8} {s:>6} " + " ".join(f"{x:8.3f}" for x in sigs))

    path = os.path.join(RESULTS, "ion_zeeman_demo.json")
    with open(path, "w") as f:
        json.dump(out, f, indent=1)
    print(f"\nwrote {path}")


if __name__ == "__main__":
    main()
