"""Gate-cost sensitivity: does the qudit advantage survive realistic gate costs?

Our default cost model charges every gate one time-layer regardless of d,
which is the assumption most favourable to qudits. Two published cost
structures charge more (see GATE_COST_MODELS in qudit_shor.py):

  ion       a fully entangling two-qudit gate costs 2(d-1) Molmer-Sorensen
            gates on trapped ions (Ringbauer 2022) -- normalized to (d-1).
  pavlidis  qudit QFT-domain arithmetic carries an explicit d^2 depth factor
            (Pavlidis & Floratos 2017) -- normalized to d^2/4, all gates.

Total Shor circuit cost (time-layers) for N = 15:

    cost model    d=2    d=3    d=5
    uniform      51.0   26.0   15.0      qudits 3.4x cheaper
    ion          51.0   44.0   42.0      advantage nearly gone
    pavlidis     51.0   58.5   93.8      advantage REVERSED

Writes results/cost_sensitivity.json. Run: python3 cost_sensitivity.py
"""

import json
import os
import time
from concurrent.futures import ProcessPoolExecutor

from plots import uniform_floor
from qpe_generic import good_phase_mask, qpe_run_exact
from qudit_shor import shor_run

COSTS = ["uniform", "ion", "pavlidis"]
NOISE = ["depolarizing", "transmon_cal"]
STRENGTHS = [0.002, 0.005, 0.01]
BASES = [2, 3, 5]
QPE_M = {2: 6, 3: 4, 5: 3}


def one(args):
    algo, nm, cm, d, s = args
    t0 = time.time()
    if algo == "shor":
        r = shor_run(d, nm, s, cost_model=cm)
    else:
        r = qpe_run_exact(d, QPE_M[d], nm, s, cost_model=cm)
    return dict(algo=algo, noise=nm, cost=cm, d=d, strength=s,
                success=float(r["success"]), elapsed_s=round(time.time() - t0, 1))


def main():
    os.makedirs("results", exist_ok=True)
    shor_floor = {d: uniform_floor(d) for d in BASES}
    shor_base = {d: shor_run(d)["success"] for d in BASES}
    qpe_floor = {d: float(good_phase_mask(d ** QPE_M[d]).mean()) for d in BASES}
    qpe_base = {d: qpe_run_exact(d, QPE_M[d])["success"] for d in BASES}
    print("baselines computed", flush=True)

    jobs = [(algo, nm, cm, d, s)
            for algo in ("shor", "qpe") for nm in NOISE
            for cm in COSTS for s in STRENGTHS for d in BASES]

    results = []
    with ProcessPoolExecutor(max_workers=6) as ex:
        for r in ex.map(one, jobs):
            d = r["d"]
            fl = shor_floor[d] if r["algo"] == "shor" else qpe_floor[d]
            bs = shor_base[d] if r["algo"] == "shor" else qpe_base[d]
            r["signal"] = (r["success"] - fl) / (bs - fl)
            results.append(r)
            print(f"{r['algo']:5s} {r['noise']:13s} {r['cost']:9s} "
                  f"d={d} s={r['strength']:<6g} signal={r['signal']:6.3f} "
                  f"({r['elapsed_s']}s)", flush=True)

    with open("results/cost_sensitivity.json", "w") as f:
        json.dump({"costs": COSTS, "noise": NOISE, "strengths": STRENGTHS,
                   "qpe_m": QPE_M, "shor_floor": shor_floor,
                   "shor_base": shor_base, "qpe_floor": qpe_floor,
                   "qpe_base": qpe_base, "runs": results}, f, indent=1)
    print("\nwrote results/cost_sensitivity.json")


if __name__ == "__main__":
    main()
