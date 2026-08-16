"""Ladder-channel sensitivity to the per-level coherence exponents.

Referee objection (Innsbruck-style report, major comment 4): the
calibrated ladder fixes relaxation at Gamma_k ~ k^0.7 and pure dephasing
at max(j,k)^1.1, exponents fit essentially to d = 3 pair ratios (Blok
2021: 1 : 2.0 : 2.3, which the channel reproduces as 1 : 2.14 : 2.14),
and then applies them at d = 5 and 7 -- where the headline ququint
results live. Peterer et al. 2015 measured the sequential transmon
ladder to the fourth level and disagrees:

    T1  : 84 / 41 / 30 / 22 us      -> Gamma_21/Gamma_10 = 2.05 (k^1.0,
                                        not the k^0.7 / 1.7 used here)
    T2  : 72 / 32 / 12 / <2 us      -> pair rates 1 : 2.25 : 6.0 : >36
                                        against 1 : 2.14 : 3.35 : 4.59
                                        under max-level^1.1

No single power law fits that dephasing escalation (it accelerates:
exponent 1.6 matches the 2<->3 pair, 2.6 matches 3<->4, neither matches
both), so rather than refit we sweep the exponent across the range
Peterer admits and ask whether the paper's conclusions survive the
harshest reading.

Grid: dephasing exponent 1.1 (paper), 1.6, 2.0, 2.6, plus a combined
worst case that also moves relaxation to Peterer's k^1.0. Demo instance
(N = 21, a = 2, r = 6), exact density matrices, ladder operating point
s = 0.003, `uniform` and `ion` cost, d = 2, 3, 5.

d = 2 is a control: the channel is normalized so the 0<->1 subspace is
bit-for-bit identical to the qubit channel, so every d = 2 cell must be
invariant across the sweep. Any drift there is a bug.

Writes results/ladder_exponent_sensitivity.json.
Run: python3 ladder_exponent_sensitivity.py
"""

import json
import os
import sys
import time
import zlib
from concurrent.futures import ProcessPoolExecutor

from qudit_shor import (multiplicative_order, recovered_order, shor_config,
                        shor_run)
from trajectories import shor_trajectories

N, A = 21, 2
STRENGTH = 0.003          # calibrated-ladder operating point
COSTS = ["uniform", "ion"]

# `python3 ladder_exponent_sensitivity.py traj [n]` extends the sweep to
# d = 7, which is out of exact-DM reach (16807-dimensional), using
# quantum trajectories for every base so the columns stay comparable.
TRAJ = len(sys.argv) > 1 and sys.argv[1] == "traj"
N_TRAJ = int(sys.argv[2]) if len(sys.argv) > 2 else 1000
DIMS = [2, 3, 5, 7] if TRAJ else [2, 3, 5]

# (label, damping_exponent, dephase_exponent)
CONFIGS = [
    ("paper (0.7 / 1.1)",        0.7, 1.1),
    ("dephase 1.6",              0.7, 1.6),
    ("dephase 2.0",              0.7, 2.0),
    ("dephase 2.6",              0.7, 2.6),
    ("Peterer worst (1.0/2.6)",  1.0, 2.6),
]

RESULTS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results")


def uniform_floor(d: int, r: int) -> float:
    m, _ = shor_config(d, N)
    D = d ** m
    return sum(recovered_order(y, D, A, N) == r for y in range(D)) / D


def one(args):
    label, damp, deph, d, cost = args
    t0 = time.time()
    m, _ = shor_config(d, N)
    seed = zlib.crc32(f"{d},{cost},{int(deph * 100)},{int(damp * 100)}"
                      .encode()) % (2 ** 32)
    if TRAJ:
        res = (shor_trajectories(d, m, a=A, N=N, cost_model=cost)
               if label is None else
               shor_trajectories(d, m, "transmon_cal", STRENGTH,
                                 n_traj=N_TRAJ, seed=seed, a=A, N=N,
                                 cost_model=cost,
                                 damping_exponent=damp,
                                 dephase_exponent=deph))
    elif label is None:                    # noiseless baseline
        res = shor_run(d, a=A, N=N, cost_model=cost)
    else:
        res = shor_run(d, "transmon_cal", STRENGTH, a=A, N=N,
                       cost_model=cost,
                       damping_exponent=damp, dephase_exponent=deph)
    return {"label": label, "damping": damp, "dephase": deph, "d": d,
            "cost": cost, "success": float(res["success"]),
            "stderr": float(res.get("stderr", 0.0)),
            "elapsed_s": round(time.time() - t0, 1)}


def main():
    os.makedirs(RESULTS, exist_ok=True)
    r = multiplicative_order(A, N)
    floors = {d: uniform_floor(d, r) for d in DIMS}

    jobs = [(None, 0.0, 0.0, d, cost) for cost in COSTS for d in DIMS]
    jobs += [(lab, damp, deph, d, cost)
             for lab, damp, deph in CONFIGS for cost in COSTS for d in DIMS]
    print(f"{len(jobs)} exact-DM runs", flush=True)

    t0 = time.time()
    with ProcessPoolExecutor(max_workers=4) as ex:
        runs = list(ex.map(one, jobs))
    print(f"done in {time.time() - t0:.0f} s\n", flush=True)

    base = {(x["d"], x["cost"]): x["success"]
            for x in runs if x["label"] is None}

    def signal(d, cost, succ):
        return (succ - floors[d]) / (base[(d, cost)] - floors[d])

    out = {"N": N, "a": A, "r": r, "strength": STRENGTH, "floors": floors,
           "configs": [{"label": l, "damping": dm, "dephase": dp}
                       for l, dm, dp in CONFIGS],
           "runs": runs, "table": []}

    for cost in COSTS:
        print(f"--- {cost} cost, ladder s={STRENGTH} "
              f"(floor-corrected signal) ---")
        print(f"{'exponents':>26} " + "".join(f"d={d}".rjust(9) for d in DIMS)
              + "   verdict")
        for lab, damp, deph in CONFIGS:
            sigs = {}
            for d in DIMS:
                s = next(x["success"] for x in runs
                         if x["label"] == lab and x["d"] == d
                         and x["cost"] == cost)
                sigs[d] = signal(d, cost, s)
            best = max(DIMS, key=lambda d: sigs[d])
            qudit_wins = any(sigs[d] > sigs[2] for d in DIMS if d != 2)
            verdict = (f"qudit ({best}) wins" if qudit_wins
                       else "QUBIT WINS")
            out["table"].append({"cost": cost, "label": lab,
                                 "damping": damp, "dephase": deph,
                                 "signal": {str(d): sigs[d] for d in DIMS},
                                 "best_d": best, "qudit_wins": qudit_wins})
            print(f"{lab:>26} "
                  + "".join(f"{sigs[d]:9.3f}" for d in DIMS)
                  + f"   {verdict}")
        print()

    out["mode"] = f"trajectories ({N_TRAJ}/point)" if TRAJ else "exact DM"
    name = ("ladder_exponent_sensitivity_d7.json" if TRAJ
            else "ladder_exponent_sensitivity.json")
    path = os.path.join(RESULTS, name)
    with open(path, "w") as f:
        json.dump(out, f, indent=1)
    print(f"wrote {path}")


if __name__ == "__main__":
    main()
