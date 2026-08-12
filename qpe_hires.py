"""Eigenstate-QPE scaling at publication statistics, four noise regimes.

The QPE results were never touched by the grid-alignment confound (the
golden-ratio target phase is far from any small-denominator fraction in
every base), so they need no re-run for correctness -- only for statistics,
and for regime coverage matching the Shor study in scaling_fair.py.

Run: python3 qpe_hires.py [n_traj]     default 1000
Writes results/qpe_hires_<n_traj>.json.
"""

import json
import os
import sys
import time
from concurrent.futures import ProcessPoolExecutor

from qpe_generic import qpe_trajectories

SIZES = {2: [6, 8, 10, 12], 3: [4, 5, 6, 7], 5: [3, 4, 5]}
REGIMES = [
    ("depolarizing", "depolarizing", 0.005, 1.0),
    ("transmon", "transmon", 0.003, 1.0),
    ("transmon_cal", "transmon_cal", 0.003, 1.0),
    ("transmon_cal_lowcharge", "transmon_cal", 0.003, 0.0),
]
N_TRAJ = int(sys.argv[1]) if len(sys.argv) > 1 else 1000
N_TRAJ_BIG = N_TRAJ // 2
BIG = {(2, 12)}
OUT = f"results/qpe_hires_{N_TRAJ}.json"


def one_point(args):
    label, model, strength, dephase_ratio, d, m = args
    n_traj = N_TRAJ_BIG if (d, m) in BIG else N_TRAJ
    seed = hash((label, d, m)) % (2 ** 32)
    t0 = time.time()
    res = qpe_trajectories(d, m, model, strength, n_traj=n_traj, seed=seed,
                           dephase_ratio=dephase_ratio)
    res["regime"] = label
    res["elapsed_s"] = round(time.time() - t0, 1)
    return res


def main():
    os.makedirs("results", exist_ok=True)
    baselines = {}
    for d, ms in SIZES.items():
        for m in ms:
            baselines[f"{d},{m}"] = qpe_trajectories(d, m)
    print(f"{len(baselines)} noiseless baselines, {N_TRAJ} traj/point",
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
            res["signal_err"] = res["stderr"] / span
            results.append(res)
            print(f"{res['regime']:22s} d={res['d']} m={res['m']:2d} "
                  f"signal={res['signal']:6.3f}±{res['signal_err']:.3f} "
                  f"({res['elapsed_s']}s)", flush=True)

    with open(OUT, "w") as f:
        json.dump({"sizes": SIZES, "regimes": REGIMES, "n_traj": N_TRAJ,
                   "baselines": baselines, "runs": results}, f, indent=1)
    print(f"\nwrote {OUT}")


if __name__ == "__main__":
    main()
