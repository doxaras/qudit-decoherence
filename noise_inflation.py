"""Noise-inflation threshold: how much extra per-layer noise kills the
qudit advantage?

Referee request (Gottesman-style review, major comment 3): the paper's
channels charge every base the same per-layer strength s; on real
hardware the per-gate error itself may grow with d beyond the layer
multipliers. Sweep an inflation factor f applied to the QUDIT's
per-layer strength only, s_d = f * s_2, and report the critical f*
at which the qudit's floor-corrected signal drops to the qubit's.
This converts the paper's binary condition into a threshold: a
platform whose measured per-gate noise ratio sits below f* keeps the
advantage.

Demo instance (N = 21, a = 2, r = 6), exact density-matrix evolution,
both marked operating points, uniform and ion cost models, d = 3, 5.

Writes results/noise_inflation.json. Run: python3 noise_inflation.py
"""

import json
import os
import time
from concurrent.futures import ProcessPoolExecutor

import numpy as np

from qudit_shor import (multiplicative_order, recovered_order, shor_config,
                        shor_run)

N, A = 21, 2
POINTS = [("transmon_cal", 0.003), ("depolarizing", 0.005)]
COSTS = ["uniform", "ion"]
QUDITS = [3, 5]
FACTORS = [1.0, 1.5, 2.0, 2.5, 3.0, 4.0, 5.0, 6.0]

RESULTS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results")


def uniform_floor(d: int, r: int) -> float:
    m, _ = shor_config(d, N)
    D = d ** m
    return sum(recovered_order(y, D, A, N) == r for y in range(D)) / D


def one(args):
    d, model, s, cost = args
    t0 = time.time()
    res = (shor_run(d, model, s, a=A, N=N, cost_model=cost) if model
           else shor_run(d, a=A, N=N, cost_model=cost))
    return {"d": d, "model": model, "strength": s, "cost": cost,
            "success": float(res["success"]),
            "elapsed_s": round(time.time() - t0, 1)}


def crossing(fs, sig_d, sig_2):
    """First f where the qudit signal falls to the qubit's (linear interp)."""
    diff = np.asarray(sig_d) - sig_2
    for i in range(1, len(fs)):
        if diff[i - 1] >= 0 > diff[i]:
            t = diff[i - 1] / (diff[i - 1] - diff[i])
            return fs[i - 1] + t * (fs[i] - fs[i - 1])
    return None  # no crossing inside the sweep


def main():
    os.makedirs(RESULTS, exist_ok=True)
    r = multiplicative_order(A, N)
    floors = {d: uniform_floor(d, r) for d in [2] + QUDITS}

    jobs = []
    for cost in COSTS:
        for d in [2] + QUDITS:
            jobs.append((d, None, 0.0, cost))               # noiseless
        for model, s in POINTS:
            for d in [2] + QUDITS:
                if d == 2:
                    jobs.append((d, model, s, cost))        # qubit anchor
                else:
                    jobs.extend((d, model, s * f, cost) for f in FACTORS)
    print(f"{len(jobs)} exact-DM runs", flush=True)

    t0 = time.time()
    with ProcessPoolExecutor(max_workers=4) as ex:
        runs = list(ex.map(one, jobs))
    print(f"all runs done in {time.time() - t0:.0f} s", flush=True)

    base = {(x["d"], x["cost"]): x["success"] for x in runs if x["model"] is None}

    def signal(d, cost, succ):
        span = base[(d, cost)] - floors[d]
        return (succ - floors[d]) / span

    out = {"N": N, "a": A, "r": r, "factors": FACTORS, "runs": runs,
           "crossings": {}}
    print(f"\n{'model':>13} {'cost':>8} {'d':>2} "
          + " ".join(f"f={f:<4}" for f in FACTORS) + "  f*")
    for model, s in POINTS:
        for cost in COSTS:
            s2 = next(signal(2, cost, x["success"]) for x in runs
                      if x["d"] == 2 and x["model"] == model
                      and x["cost"] == cost)
            for d in QUDITS:
                sigs = [signal(d, cost, x["success"]) for f in FACTORS
                        for x in runs
                        if x["d"] == d and x["model"] == model
                        and x["cost"] == cost
                        and abs(x["strength"] - s * f) < 1e-12]
                fstar = crossing(FACTORS, sigs, s2)
                key = f"{model}_{cost}_d{d}"
                out["crossings"][key] = {"f_star": fstar, "qubit_signal": s2,
                                         "qudit_signals": sigs}
                print(f"{model:>13} {cost:>8} {d:>2} "
                      + " ".join(f"{x:5.2f}" for x in sigs)
                      + f"  {'>' + str(FACTORS[-1]) if fstar is None else f'{fstar:.2f}'}"
                      + f"   (qubit {s2:.2f})")

    path = os.path.join(RESULTS, "noise_inflation.json")
    with open(path, "w") as f:
        json.dump(out, f, indent=1)
    print(f"\nwrote {path}")


if __name__ == "__main__":
    main()
