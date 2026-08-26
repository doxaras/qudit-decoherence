"""d = 7 matched control dimension: price the acceptance-set gift.

Round-4 referee point: the d = 7 demo register (m = 3, D = 343) enters
the comparison with an acceptance set of |A| = 48 outcomes for r = 6
against the qubit's 8 at D = 64 -- a 6x decoder-tolerance gift at zero
exposure cost. This is exactly the confound the matched-D control
(matched_D.py) prices for the ququint, but that control stops at
d = 5. No qubit register hits D = 343 exactly; m = 8 (D = 256) and
m = 9 (D = 512) bracket it, with m = 9 the natural partner.

Same conventions as d7_demo.py: unbiased instance (N = 21, a = 2,
r = 6), uniform cost, 1000 trajectories/point, the three demo noise
points. Also tabulates |A|(D) for every register in the comparison.

Writes results/d7_matched_D.json. Run: python3 d7_matched_D.py
"""

import json
import os
import sys
import time
import zlib
from concurrent.futures import ProcessPoolExecutor

from qudit_shor import multiplicative_order, recovered_order, shor_config
from trajectories import shor_trajectories

N, A = 21, 2
CONFIGS = [(2, 8), (2, 9)]              # (d, m); D = 256, 512
NOISE = [("depolarizing", 0.005), ("transmon_cal", 0.005),
         ("transmon_cal", 0.003)]
N_TRAJ = int(sys.argv[1]) if len(sys.argv) > 1 else 1000
# registers whose acceptance sets get tabulated alongside the new runs
ACCEPT_REGS = [(2, 6), (2, 8), (2, 9), (3, 4), (5, 3), (7, 3)]


def one_point(args):
    d, m, model, s = args
    seed = zlib.crc32(f"d7matched,{d},{m},{model},{int(s * 1e6)}".encode())
    t0 = time.time()
    res = shor_trajectories(d, m, model, s, n_traj=N_TRAJ, seed=seed,
                            a=A, N=N, cost_model="uniform")
    res["elapsed_s"] = round(time.time() - t0, 1)
    return res


def main():
    os.makedirs("results", exist_ok=True)
    r = multiplicative_order(A, N)

    accept = {}
    for d, m in ACCEPT_REGS:
        D = d ** m
        accept[f"{d},{m}"] = {
            "D": D,
            "A_size": sum(recovered_order(y, D, A, N) == r for y in range(D))}
        print(f"|A| at d={d}, m={m} (D={D}): "
              f"{accept[f'{d},{m}']['A_size']}", flush=True)

    baselines = {}
    for d, m in CONFIGS:
        b = shor_trajectories(d, m, a=A, N=N)
        baselines[f"{d},{m}"] = b
        print(f"baseline d={d} m={m}: success={b['success']:.4f} "
              f"floor={b['floor']:.4f}", flush=True)

    points = [(d, m, model, s) for d, m in CONFIGS for model, s in NOISE]
    results = []
    with ProcessPoolExecutor(max_workers=3) as ex:
        for res in ex.map(one_point, points):
            b = baselines[f"{res['d']},{res['m']}"]
            span = b["success"] - res["floor"]
            res["signal"] = (res["success"] - res["floor"]) / span
            res["signal_err"] = res["stderr"] / span
            results.append(res)
            print(f"d={res['d']} m={res['m']} {res['noise_model']:13s} "
                  f"s={res['strength']:<6g} "
                  f"success={res['success']:.4f}±{res['stderr']:.4f} "
                  f"signal={res['signal']:.3f}±{res['signal_err']:.3f} "
                  f"({res['elapsed_s']}s)", flush=True)

    with open("results/d7_matched_D.json", "w") as f:
        json.dump({"N": N, "a": A, "r": r, "configs": CONFIGS,
                   "noise": NOISE, "n_traj": N_TRAJ,
                   "acceptance_sets": accept,
                   "baselines": baselines, "runs": results}, f, indent=1)
    print("wrote results/d7_matched_D.json")


if __name__ == "__main__":
    main()
