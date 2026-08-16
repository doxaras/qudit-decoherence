"""d = 7 demo point: does the seventh dimension clear the rising bar?

The paper leaves d = 7 untested and notes the break-even curve of
Jankovic et al. suggests the bar rises steeply. Quantitatively: at d = 7
a qudit register must clear a gate-efficiency ratio of
(d^2-1)/(3 log2 d) = 5.70, while its uniform-cost layer ratio on the
demo instance is only 57/15 = 3.80 -- so the gate-level criterion
predicts d = 7 LOSES to the qubit under ladder dephasing even with a
native entangler, the first dimension where the native-gate condition
itself is predicted to be insufficient. This runs the algorithm-level
check: all four bases, both channels, all three cost models, on the
unbiased instance (N = 21, a = 2, r = 6; base 7 is never aligned, with
mean residual misalignment 0.300, identical to bases 3 and 5).

Quantum trajectories (demo registers are small; 1000/point). Writes
results/d7_demo.json. Run: python3 d7_demo.py
"""

import json
import os
import sys
import time
import zlib
from concurrent.futures import ProcessPoolExecutor

from qudit_shor import shor_config
from trajectories import shor_trajectories

N, A = 21, 2
BASES = [2, 3, 5, 7]
# (noise_model, strength): tab:cost common strength, plus the marked
# transmon operating point.
NOISE = [("depolarizing", 0.005), ("transmon_cal", 0.005),
         ("transmon_cal", 0.003)]
COSTS = ["uniform", "ion", "pavlidis"]
N_TRAJ = int(sys.argv[1]) if len(sys.argv) > 1 else 1000


def one_point(args):
    d, model, s, cost = args
    m, _ = shor_config(d, N)
    seed = zlib.crc32(f"{d},{model},{int(s * 1e6)},{cost}".encode()) % (2 ** 32)
    t0 = time.time()
    res = shor_trajectories(d, m, model, s, n_traj=N_TRAJ, seed=seed,
                            a=A, N=N, cost_model=cost)
    res["cost_model"] = cost
    res["elapsed_s"] = round(time.time() - t0, 1)
    return res


def main():
    os.makedirs("results", exist_ok=True)
    baselines = {}
    for d in BASES:
        m, w = shor_config(d, N)
        r = shor_trajectories(d, m, a=A, N=N)
        baselines[str(d)] = r
        print(f"baseline d={d} (m={m}, w={w}): success={r['success']:.4f} "
              f"floor={r['floor']:.4f}", flush=True)

    points = [(d, model, s, cost) for d in BASES
              for model, s in NOISE for cost in COSTS]
    results = []
    with ProcessPoolExecutor(max_workers=4) as ex:
        for res in ex.map(one_point, points):
            b = baselines[str(res["d"])]
            span = b["success"] - res["floor"]
            res["signal"] = (res["success"] - res["floor"]) / span
            results.append(res)
            print(f"d={res['d']} {res['noise_model']:13s} "
                  f"s={res['strength']:<6g} {res['cost_model']:9s} "
                  f"layers={res['n_layers']:6.1f} "
                  f"success={res['success']:.4f}±{res['stderr']:.4f} "
                  f"signal={res['signal']:6.3f} ({res['elapsed_s']}s)",
                  flush=True)

    with open("results/d7_demo.json", "w") as f:
        json.dump({"N": N, "a": A, "bases": BASES, "noise": NOISE,
                   "costs": COSTS, "n_traj": N_TRAJ,
                   "baselines": baselines, "runs": results}, f, indent=1)
    print("\nwrote results/d7_demo.json")


if __name__ == "__main__":
    main()
