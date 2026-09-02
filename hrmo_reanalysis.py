"""Re-run the noise-inflation analysis at the inflation factors implied by
the measured native qudit entangling gate of Hrmo et al., Nat. Commun. 14,
2242 (2023), arXiv:2206.04104 (referee requirement 1, Innsbruck-style
report; see reviews/referee3_innsbruck_experimentalist.md).

Hrmo et al. report a single-application light-shift entangling gate with
fidelities 99.6(1)% (d=2), 98.7(2)% (d=3), 93.7(3)% (d=5). Under the
paper's exposure convention a two-qudit gate of layer cost L deposits
2 L s (1 - 1/d^2) entanglement-infidelity on its two carriers, so a
measured gate infidelity eps implies per-carrier-layer strength
s = eps / (2 L (1 - 1/d^2)) and inflation factor

    f(d) = s_d / s_2 = (eps_d / eps_2) * (3/4) / (1 - 1/d^2) / L_rel(d)

where L_rel is the cost model's two-qudit multiplier normalized to d=2
(uniform: 1; ion: d-1). The f=1 rows of the paper's Table II assumed
equal per-layer strength across bases; this script reruns the demo grid
(N = 21, a = 2, r = 6, exact density matrices) at the measured f and its
+/-1 sigma band, and compares each f against the paper's published f*.

Writes results/hrmo_reanalysis.json. Run: python3 hrmo_reanalysis.py
"""

import json
import math
import os
import time
from concurrent.futures import ProcessPoolExecutor

from qudit_shor import (multiplicative_order, recovered_order, shor_config,
                        shor_run)

N, A = 21, 2

# Hrmo et al. 2023, Table 1: gate fidelity and 1-sigma error by dimension.
HRMO_EPS = {2: (0.004, 0.001), 3: (0.013, 0.002), 5: (0.063, 0.003)}

# Operating points of the paper's inflation study (Sec. VII).
POINTS = [("transmon_cal", 0.003), ("depolarizing", 0.005)]
COSTS = {"uniform": lambda d: 1.0, "ion": lambda d: float(d - 1)}
QUDITS = [3, 5]

# f* labels are read from results/noise_inflation.json (its `crossings`
# block is computed under the current channel). A hardcoded copy here
# went stale when the relaxation form changed; the verdicts never
# depended on it, only the labels. Run noise_inflation.py first.
def _load_f_star():
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        "results", "noise_inflation.json")
    cr = json.load(open(path))["crossings"]
    out = {}
    for m in ("transmon_cal", "depolarizing"):
        for c in ("uniform", "ion"):
            for d in (3, 5):
                key = f"{m}_{c}_d{d}"
                out[(m, c, d)] = (round(cr[key]["f_star"], 4)
                                  if key in cr and cr[key]["f_star"]
                                  is not None else None)
    return out


F_STAR = _load_f_star()

RESULTS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results")


def hrmo_f(d: int, cost: str):
    """Central inflation factor and 1-sigma from Hrmo gate infidelities."""
    eps_d, sig_d = HRMO_EPS[d]
    eps_2, sig_2 = HRMO_EPS[2]
    central = (eps_d / eps_2) * 0.75 / (1.0 - 1.0 / d ** 2) / COSTS[cost](d)
    rel = math.sqrt((sig_d / eps_d) ** 2 + (sig_2 / eps_2) ** 2)
    return central, central * rel


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


def main():
    os.makedirs(RESULTS, exist_ok=True)
    r = multiplicative_order(A, N)
    floors = {d: uniform_floor(d, r) for d in [2] + QUDITS}

    jobs = [(d, None, 0.0, "uniform") for d in [2] + QUDITS]
    for model, s in POINTS:
        jobs.append((2, model, s, "uniform"))
    variants = {}  # (model, cost, d) -> [(label, f, s_d), ...]
    for model, s2 in POINTS:
        for cost in COSTS:
            for d in QUDITS:
                f, sig = hrmo_f(d, cost)
                variants[(model, cost, d)] = [
                    ("lo", f - sig, s2 * (f - sig)),
                    ("central", f, s2 * f),
                    ("hi", f + sig, s2 * (f + sig)),
                ]
                jobs.extend((d, model, s2 * ff, cost)
                            for _, ff, _ in variants[(model, cost, d)])
    print(f"{len(jobs)} exact-DM runs", flush=True)

    t0 = time.time()
    with ProcessPoolExecutor(max_workers=4) as ex:
        runs = list(ex.map(one, jobs))
    print(f"all runs done in {time.time() - t0:.0f} s", flush=True)

    base = {x["d"]: x["success"] for x in runs if x["model"] is None}

    def signal(d, succ):
        return (succ - floors[d]) / (base[d] - floors[d])

    def lookup(d, model, s, cost):
        return next(x["success"] for x in runs
                    if x["d"] == d and x["model"] == model
                    and x["cost"] == cost and abs(x["strength"] - s) < 1e-12)

    out = {"N": N, "a": A, "r": r, "hrmo_eps": {str(k): v for k, v in HRMO_EPS.items()},
           "floors": floors, "noiseless": base, "runs": runs, "cells": []}

    print(f"\n{'channel':>13} {'cost':>8} {'d':>2} {'f (1s)':>16} {'f*':>5} "
          f"{'qudit sig (lo/c/hi)':>22} {'qubit':>6}  verdict")
    for model, s2 in POINTS:
        # qubit anchor: cost model is irrelevant at d=2 (multiplier 1)
        sig2 = signal(2, lookup(2, model, s2, "uniform"))
        for cost in COSTS:
            for d in QUDITS:
                vs = variants[(model, cost, d)]
                sigs = {lab: signal(d, lookup(d, model, s, cost))
                        for lab, _, s in vs}
                f, sig_f = hrmo_f(d, cost)
                fstar = F_STAR[(model, cost, d)]
                lost_c = sigs["central"] < sig2
                lost_lo = sigs["lo"] < sig2      # best case for the qudit
                verdict = ("LOST (even at -1 sigma)" if lost_lo and lost_c
                           else "lost (survives at -1 sigma)" if lost_c
                           else "SURVIVES")
                out["cells"].append({
                    "channel": model, "cost": cost, "d": d,
                    "f_central": f, "f_sigma": sig_f, "f_star": fstar,
                    "qubit_signal": sig2,
                    "qudit_signal": {k: v for k, v in sigs.items()},
                    "verdict": verdict})
                print(f"{model:>13} {cost:>8} {d:>2} "
                      f"{f:5.2f} +/- {sig_f:4.2f}  "
                      f"{'--' if fstar is None else f'{fstar:4.2f}':>5} "
                      f"{sigs['lo']:6.3f}/{sigs['central']:6.3f}/{sigs['hi']:6.3f}"
                      f"   {sig2:5.3f}  {verdict}")

    path = os.path.join(RESULTS, "hrmo_reanalysis.json")
    with open(path, "w") as fh:
        json.dump(out, fh, indent=1)
    print(f"\nwrote {path}")


if __name__ == "__main__":
    main()
