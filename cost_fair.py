"""Gate-cost sensitivity for Shor on the UNBIASED instance (N=21, a=2, r=6).

Same grid as cost_sensitivity.py -- three cost models x two noise models x
three strengths x three bases -- but on an instance where no base gets free
grid alignment. The QPE half of the original study needs no re-run: its
golden-ratio target phase was chosen from the start to be far from any
small-denominator fraction in every base, so it was never confounded.

Writes results/cost_fair.json. Run: python3 cost_fair.py
"""

import json
import os
import time
from concurrent.futures import ProcessPoolExecutor

from plots import uniform_floor
from qudit_shor import multiplicative_order, shor_run

N, A = 21, 2
COSTS = ["uniform", "ion", "pavlidis"]
NOISE = ["depolarizing", "transmon_cal"]
STRENGTHS = [0.002, 0.005, 0.01]
BASES = [2, 3, 5]


def one(args):
    nm, cm, d, s = args
    t0 = time.time()
    r = shor_run(d, nm, s, a=A, N=N, cost_model=cm)
    return dict(noise=nm, cost=cm, d=d, strength=s,
                success=float(r["success"]), layers=r["n_layers"],
                elapsed_s=round(time.time() - t0, 1))


def main():
    os.makedirs("results", exist_ok=True)
    floors = {d: uniform_floor(d, A, N) for d in BASES}
    bases = {d: float(shor_run(d, a=A, N=N)["success"]) for d in BASES}
    for d in BASES:
        print(f"d={d}: floor={floors[d]:.4f} noiseless={bases[d]:.4f}",
              flush=True)

    jobs = [(nm, cm, d, s) for nm in NOISE for cm in COSTS
            for s in STRENGTHS for d in BASES]
    results = []
    with ProcessPoolExecutor(max_workers=4) as ex:
        for r in ex.map(one, jobs):
            d = r["d"]
            r["signal"] = (r["success"] - floors[d]) / (bases[d] - floors[d])
            results.append(r)
            print(f"{r['noise']:13s} {r['cost']:9s} d={d} "
                  f"s={r['strength']:<6g} layers={r['layers']:6.1f} "
                  f"signal={r['signal']:6.3f} ({r['elapsed_s']}s)", flush=True)

    with open("results/cost_fair.json", "w") as f:
        json.dump({"N": N, "a": A, "r": multiplicative_order(A, N),
                   "costs": COSTS, "noise": NOISE, "strengths": STRENGTHS,
                   "floors": floors, "baselines": bases, "runs": results},
                  f, indent=1)
    print("\nwrote results/cost_fair.json")


if __name__ == "__main__":
    main()
