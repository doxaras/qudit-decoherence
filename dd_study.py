"""Does reduced dephasing change who wins? Task #5.

`dephase_scale` sweeps the pure-dephasing rate from 1 (devices as
measured) to 0 (the T1 limit). CAVEAT (post-review): this models
*device engineering* -- the high-E_J/E_C regime of Wang et al. 2024,
where charge dispersion is suppressed at the hardware level (the
`transmon_cal_lowcharge` end point). It does NOT model echo/dynamical
decoupling: the channel's dephasing generator is Markovian (white
noise), which no pulse sequence suppresses -- and on a
sensitivity-ordered qudit no two-interval echo refocuses at d >= 3 at
all (see the permutation analysis of ion_zeeman_quasistatic.py /
paper Sec. VIII, which is the honest treatment of pulsed refocusing,
including its per-pulse charge). The cost "bracket" below via the
`uniform`/`ion` entangling-gate models is likewise not a DD-pulse cost
model; single-qudit refocusing pulses are charged properly only in the
Sec. VIII analysis.

So read results/dd.json as: how the verdict moves as a platform's idle
dephasing is engineered down toward its T1 limit. Since dephasing is
the ladder component that grows fastest with d, reducing it helps
qudits more by construction.

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
