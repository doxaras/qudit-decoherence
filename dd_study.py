"""Does echo (dynamical decoupling) change who wins? Task #5.

No real transmon runs a long circuit without refocusing. DD suppresses the
dephasing half of the ladder channel while leaving relaxation untouched
(it cannot undo T1), so the honest question is not "does DD help" -- it
always does -- but **whether it helps qubits or qudits more**, i.e. whether
refocused hardware narrows or widens the gap we measure.

`dephase_scale` sweeps from 1 (free evolution) to 0 (perfect echo, the
T1 limit). This is the same knob that defines the `transmon_cal_lowcharge`
regime, which is exactly the dephase_scale = 0 end point -- there reached
by device engineering (high E_J/E_C, Wang et al. 2024), here by pulses.

DD is not free: a d-level system needs more refocusing pulses than a qubit
to average out all d(d-1)/2 coherences, and each pulse carries error. We
bracket that cost with the two cost models already in the repo -- `uniform`
(DD pulses are free, the optimistic limit) and `ion` (pulse count grows as
d-1, the pessimistic limit) -- rather than inventing a new one.

Writes results/dd.json. Run: python3 dd_study.py
"""

import json
import os
import time
from concurrent.futures import ProcessPoolExecutor

from plots import uniform_floor
from qpe_generic import good_phase_mask, qpe_run_exact
from qudit_shor import shor_run

N, A = 21, 2
SCALES = [1.0, 0.75, 0.5, 0.25, 0.0]
COSTS = ["uniform", "ion"]
STRENGTH = 0.005
BASES = [2, 3, 5]
QPE_M = {2: 6, 3: 4, 5: 3}


def one(args):
    algo, cm, d, scale = args
    t0 = time.time()
    kw = dict(cost_model=cm, dephase_scale=scale)
    if algo == "shor":
        r = shor_run(d, "transmon_cal", STRENGTH, a=A, N=N, **kw)
    else:
        r = qpe_run_exact(d, QPE_M[d], "transmon_cal", STRENGTH, **kw)
    return dict(algo=algo, cost=cm, d=d, dephase_scale=scale,
                success=float(r["success"]),
                elapsed_s=round(time.time() - t0, 1))


def main():
    os.makedirs("results", exist_ok=True)
    floors = {("shor", d): uniform_floor(d, A, N) for d in BASES}
    floors.update({("qpe", d): float(good_phase_mask(d ** QPE_M[d]).mean())
                   for d in BASES})
    base = {("shor", d): float(shor_run(d, a=A, N=N)["success"])
            for d in BASES}
    base.update({("qpe", d): float(qpe_run_exact(d, QPE_M[d])["success"])
                 for d in BASES})
    print("baselines computed", flush=True)

    jobs = [(algo, cm, d, s) for algo in ("shor", "qpe") for cm in COSTS
            for d in BASES for s in SCALES]
    runs = []
    with ProcessPoolExecutor(max_workers=4) as ex:
        for r in ex.map(one, jobs):
            key = (r["algo"], r["d"])
            r["signal"] = ((r["success"] - floors[key])
                           / (base[key] - floors[key]))
            runs.append(r)
            print(f"{r['algo']:5s} {r['cost']:8s} d={r['d']} "
                  f"scale={r['dephase_scale']:<5g} "
                  f"signal={r['signal']:6.3f} ({r['elapsed_s']}s)", flush=True)

    with open("results/dd.json", "w") as f:
        json.dump({"N": N, "a": A, "scales": SCALES, "costs": COSTS,
                   "strength": STRENGTH, "qpe_m": QPE_M,
                   "floors": {f"{k[0]},{k[1]}": v for k, v in floors.items()},
                   "baselines": {f"{k[0]},{k[1]}": v for k, v in base.items()},
                   "runs": runs}, f, indent=1)
    print("\nwrote results/dd.json")


if __name__ == "__main__":
    main()
