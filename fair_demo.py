"""Demo-size noise sweep on the UNBIASED instance (N = 21, a = 2, r = 6).

This replaces experiments.py for publication purposes. Every earlier Shor
number in this repo used N = 15, whose multiplicative group is Z2 x Z4 and
therefore admits only power-of-two orders -- silently handing base 2 exact
grid alignment (r | D = 2^m always, never for d = 3 or 5). See
docs/MECHANISM.md.

N = 21, a = 2 has r = 6, which divides no power of 2, 3 or 5, so no base is
favoured. Three noise models are swept so the new figure is directly
comparable with the old one:

  transmon       idealized ladder (Gamma_k ~ k, (Delta level)^2 dephasing)
  transmon_cal   calibrated ladder (Gamma_k ~ k^0.7, max-level dephasing)
  depolarizing   per-particle, level-independent

Exact density-matrix evolution. Writes results/fair_demo.json.
Run: python3 fair_demo.py
"""

import json
import os
import time
from concurrent.futures import ProcessPoolExecutor

from qudit_shor import (multiplicative_order, recovered_order, shor_config,
                        shor_run)

N, A = 21, 2
# 0.001 and 0.01 bracket the measured two-qudit operating points of real
# hardware (ion ~1e-3, transmon ~1e-2); both are marked on the figure.
STRENGTHS = [0.001, 0.002, 0.005, 0.01, 0.02, 0.035, 0.05]
MODELS = ["transmon", "transmon_cal", "depolarizing"]
BASES = [2, 3, 5]


def uniform_floor(d):
    m, _ = shor_config(d, N)
    D = d ** m
    r = multiplicative_order(A, N)
    return sum(recovered_order(y, D, A, N) == r for y in range(D)) / D


def one(args):
    d, model, s = args
    t0 = time.time()
    res = shor_run(d, model, s, a=A, N=N)
    res.pop("probs", None)
    res["success"] = float(res["success"])
    res["elapsed_s"] = round(time.time() - t0, 1)
    return res


def main():
    os.makedirs("results", exist_ok=True)
    floors, baselines = {}, {}
    for d in BASES:
        floors[d] = uniform_floor(d)
        b = shor_run(d, a=A, N=N)
        baselines[d] = float(b["success"])
        print(f"d={d}: m={b['m']} w={b['w']} D={b['D']} r={b['r_true']} "
              f"qudits={b['n_qudits']} layers={b['n_layers']} "
              f"floor={floors[d]:.4f} noiseless={baselines[d]:.4f}", flush=True)

    jobs = [(d, model, s) for d in BASES for model in MODELS
            for s in STRENGTHS]
    runs = []
    with ProcessPoolExecutor(max_workers=3) as ex:
        for res in ex.map(one, jobs):
            d = res["d"]
            res["signal"] = ((res["success"] - floors[d])
                             / (baselines[d] - floors[d]))
            runs.append(res)
            print(f"d={d} {res['noise_model']:13s} s={res['strength']:<6g} "
                  f"success={res['success']:.4f} signal={res['signal']:6.3f} "
                  f"({res['elapsed_s']}s)", flush=True)

    with open("results/fair_demo.json", "w") as f:
        json.dump({"N": N, "a": A, "r": multiplicative_order(A, N),
                   "strengths": STRENGTHS, "models": MODELS, "bases": BASES,
                   "floors": floors, "baselines": baselines, "runs": runs},
                  f, indent=1)
    print("\nwrote results/fair_demo.json")


if __name__ == "__main__":
    main()
