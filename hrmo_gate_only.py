"""Gate-only variant of the Hrmo noise-inflation re-analysis.

hrmo_reanalysis.py inflates the qudit's *entire* per-carrier-layer
strength by the measured factor f, which charges idle carriers and
single-qudit gates the same penalty as the entangling gate that f was
measured on. The paper's own inputs argue against that scope: measured
single-qudit per-pulse error is nearly flat in d and shielded idle
coherence is ~100 ms across all transitions (Sec. VII), so nothing
supports inflating the ~2/3 of carrier-layers that sit outside a
two-qudit gate.

This script reruns the same grid with f applied only where it was
measured: the participants of each two-qudit gate take strength f*s
through that gate's layers, spectators and single-qudit-gate layers
stay at the base strength s. Together with hrmo_reanalysis.json the two
bracket the truth (global inflation charges too much, gate-only perhaps
too little if a platform's idle noise also grows with d).

Writes results/hrmo_gate_only.json. Run: python3 hrmo_gate_only.py
"""

import json
import os
import time
from concurrent.futures import ProcessPoolExecutor

from hrmo_reanalysis import (COSTS, HRMO_EPS, POINTS, QUDITS, RESULTS,
                             hrmo_f, uniform_floor, N, A)
from qudit_shor import multiplicative_order, shor_run


def one(args):
    d, model, s, cost, gate_s = args
    t0 = time.time()
    if model is None:
        res = shor_run(d, a=A, N=N, cost_model=cost)
    else:
        res = shor_run(d, model, s, a=A, N=N, cost_model=cost,
                       gate_strength=gate_s)
    return {"d": d, "model": model, "strength": s, "cost": cost,
            "gate_strength": gate_s, "success": float(res["success"]),
            "elapsed_s": round(time.time() - t0, 1)}


def main():
    os.makedirs(RESULTS, exist_ok=True)
    r = multiplicative_order(A, N)
    floors = {d: uniform_floor(d, r) for d in [2] + QUDITS}

    jobs = [(d, None, 0.0, "uniform", None) for d in [2] + QUDITS]
    for model, s2 in POINTS:
        jobs.append((2, model, s2, "uniform", None))
    variants = {}  # (model, cost, d) -> [(label, f, gate_s), ...]
    for model, s2 in POINTS:
        for cost in COSTS:
            for d in QUDITS:
                f, sig = hrmo_f(d, cost)
                variants[(model, cost, d)] = [
                    ("lo", f - sig, s2 * (f - sig)),
                    ("central", f, s2 * f),
                    ("hi", f + sig, s2 * (f + sig)),
                ]
                jobs.extend((d, model, s2, cost, gs)
                            for _, _, gs in variants[(model, cost, d)])
    print(f"{len(jobs)} exact-DM runs", flush=True)

    t0 = time.time()
    with ProcessPoolExecutor(max_workers=4) as ex:
        runs = list(ex.map(one, jobs))
    print(f"all runs done in {time.time() - t0:.0f} s", flush=True)

    base = {x["d"]: x["success"] for x in runs if x["model"] is None}

    def signal(d, succ):
        return (succ - floors[d]) / (base[d] - floors[d])

    def lookup(d, model, cost, gate_s):
        return next(x["success"] for x in runs
                    if x["d"] == d and x["model"] == model
                    and x["cost"] == cost
                    and (x["gate_strength"] is None) == (gate_s is None)
                    and (gate_s is None
                         or abs(x["gate_strength"] - gate_s) < 1e-12))

    out = {"N": N, "a": A, "r": r,
           "hrmo_eps": {str(k): v for k, v in HRMO_EPS.items()},
           "inflation_scope": "two-qudit gate participants only",
           "floors": floors, "noiseless": base, "runs": runs, "cells": []}

    print(f"\n{'channel':>13} {'cost':>8} {'d':>2} {'f (1s)':>16} "
          f"{'qudit sig (lo/c/hi)':>22} {'qubit':>6}  verdict")
    for model, s2 in POINTS:
        sig2 = signal(2, lookup(2, model, "uniform", None))
        for cost in COSTS:
            for d in QUDITS:
                vs = variants[(model, cost, d)]
                sigs = {lab: signal(d, lookup(d, model, cost, gs))
                        for lab, _, gs in vs}
                f, sig_f = hrmo_f(d, cost)
                lost_c = sigs["central"] < sig2
                lost_lo = sigs["lo"] < sig2
                verdict = ("LOST (even at -1 sigma)" if lost_lo and lost_c
                           else "lost (survives at -1 sigma)" if lost_c
                           else "SURVIVES")
                out["cells"].append({
                    "channel": model, "cost": cost, "d": d,
                    "f_central": f, "f_sigma": sig_f,
                    "qubit_signal": sig2,
                    "qudit_signal": dict(sigs),
                    "verdict": verdict})
                print(f"{model:>13} {cost:>8} {d:>2} "
                      f"{f:5.2f} +/- {sig_f:4.2f}  "
                      f"{sigs['lo']:6.3f}/{sigs['central']:6.3f}/"
                      f"{sigs['hi']:6.3f}   {sig2:5.3f}  {verdict}")

    path = os.path.join(RESULTS, "hrmo_gate_only.json")
    with open(path, "w") as fh:
        json.dump(out, fh, indent=1)
    print(f"\nwrote {path}")


if __name__ == "__main__":
    main()
