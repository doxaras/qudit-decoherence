"""Register-size scaling for Shor on the UNBIASED instance (N=21, a=2, r=6).

Re-runs both earlier scaling studies -- the idealized-noise one
(scaling_experiment.py) and the hardware-calibrated one
(scaling_calibrated.py) -- on an instance whose order divides no power of
2, 3 or 5, so that no base gets free grid alignment. See docs/MECHANISM.md
for why every N = 15 Shor number in this repo is confounded.

Four noise regimes, one figure panel each:

  depolarizing            per-particle, s = 0.005
  transmon                idealized ladder, s = 0.003
  transmon_cal            calibrated ladder, s = 0.003
  transmon_cal_lowcharge  calibrated ladder, charge dephasing off
                          (high-E_J/E_C limit of Wang et al. 2024)

Quantum trajectories. Writes results/scaling_fair.json.

Run: python3 scaling_fair.py            400 trajectories/point (default)
     python3 scaling_fair.py 1000       publication statistics, ->
                                        results/scaling_fair_1000.json
"""

import json
import os
import sys
import time
from concurrent.futures import ProcessPoolExecutor

from trajectories import shor_trajectories

N, A = 21, 2
SIZES = {2: [6, 8, 10, 12], 3: [4, 5, 6, 7], 5: [3, 4, 5]}
# (label, noise_model passed to the simulator, strength, dephase_ratio)
REGIMES = [
    ("depolarizing", "depolarizing", 0.005, 1.0),
    ("transmon", "transmon", 0.003, 1.0),
    ("transmon_cal", "transmon_cal", 0.003, 1.0),
    ("transmon_cal_lowcharge", "transmon_cal", 0.003, 0.0),
]
N_TRAJ = int(sys.argv[1]) if len(sys.argv) > 1 else 400
N_TRAJ_BIG = N_TRAJ // 2          # the one very deep config (d=2, m=12)
BIG = {(2, 12)}
OUT = ("results/scaling_fair.json" if N_TRAJ == 400
       else f"results/scaling_fair_{N_TRAJ}.json")


def one_point(args):
    label, model, strength, dephase_ratio, d, m = args
    n_traj = N_TRAJ_BIG if (d, m) in BIG else N_TRAJ
    seed = hash((label, d, m)) % (2 ** 32)
    t0 = time.time()
    res = shor_trajectories(d, m, model, strength, n_traj=n_traj, seed=seed,
                            a=A, N=N, dephase_ratio=dephase_ratio)
    res["regime"] = label
    res["elapsed_s"] = round(time.time() - t0, 1)
    return res


def main():
    os.makedirs("results", exist_ok=True)

    baselines = {}
    for d, ms in SIZES.items():
        for m in ms:
            r = shor_trajectories(d, m, a=A, N=N)
            baselines[f"{d},{m}"] = r
            print(f"baseline d={d} m={m}: success={r['success']:.4f} "
                  f"floor={r['floor']:.4f} layers={r['n_layers']:.0f}",
                  flush=True)

    points = [(label, model, s, dr, d, m)
              for label, model, s, dr in REGIMES
              for d, ms in SIZES.items() for m in ms]

    results = []
    with ProcessPoolExecutor(max_workers=5) as ex:
        for res in ex.map(one_point, points):
            b = baselines[f"{res['d']},{res['m']}"]
            span = b["success"] - res["floor"]
            res["signal"] = (res["success"] - res["floor"]) / span
            results.append(res)
            print(f"{res['regime']:22s} d={res['d']} m={res['m']:2d} "
                  f"success={res['success']:.4f}±{res['stderr']:.4f} "
                  f"signal={res['signal']:6.3f} ({res['elapsed_s']}s)",
                  flush=True)

    with open(OUT, "w") as f:
        json.dump({"N": N, "a": A, "sizes": SIZES, "regimes": REGIMES,
                   "n_traj": N_TRAJ, "baselines": baselines,
                   "runs": results}, f, indent=1)
    print(f"\nwrote {OUT}")


if __name__ == "__main__":
    main()
