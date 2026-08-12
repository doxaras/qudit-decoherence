"""Register-size scaling under the CALIBRATED transmon noise model.

Re-runs the Shor and generic-QPE scaling studies with noise fitted to
published per-level coherence data (Gamma_k ~ k^0.7; max-level dephasing
law), in two regimes:

  transmon_cal            devices as measured (dephase_ratio = 1)
  transmon_cal_lowcharge  high-E_J/E_C limit of Wang et al. 2024, where
                          T2-echo approaches the T1 limit: charge-noise
                          dephasing switched off (dephase_ratio = 0),
                          leaving only the relaxation ladder.

Writes results/scaling_calibrated.json. Run: python3 scaling_calibrated.py
"""

import json
import os
import time
from concurrent.futures import ProcessPoolExecutor

from qpe_generic import qpe_trajectories
from trajectories import shor_trajectories

SIZES = {2: [6, 8, 10, 12], 3: [4, 5, 6, 7], 5: [3, 4, 5]}
STRENGTH = 0.003
REGIMES = [("transmon_cal", 1.0), ("transmon_cal_lowcharge", 0.0)]
ALGOS = ["shor", "qpe"]
N_TRAJ = 400
N_TRAJ_BIG = 200
BIG = {(2, 12)}


def one_point(args):
    algo, d, m, regime, dephase_ratio = args
    n_traj = N_TRAJ_BIG if (d, m) in BIG else N_TRAJ
    seed = hash((algo, d, m, regime)) % (2 ** 32)
    fn = shor_trajectories if algo == "shor" else qpe_trajectories
    t0 = time.time()
    res = fn(d, m, "transmon_cal", STRENGTH, n_traj=n_traj, seed=seed,
             dephase_ratio=dephase_ratio)
    res["algo"] = algo
    res["regime"] = regime
    res["elapsed_s"] = round(time.time() - t0, 1)
    return res


def main():
    os.makedirs("results", exist_ok=True)

    baselines = {}
    for algo in ALGOS:
        fn = shor_trajectories if algo == "shor" else qpe_trajectories
        for d, ms in SIZES.items():
            for m in ms:
                baselines[f"{algo},{d},{m}"] = fn(d, m)
    print(f"{len(baselines)} noiseless baselines computed", flush=True)

    points = [(algo, d, m, regime, dr)
              for algo in ALGOS
              for regime, dr in REGIMES
              for d, ms in SIZES.items() for m in ms]

    results = []
    with ProcessPoolExecutor(max_workers=6) as ex:
        for res in ex.map(one_point, points):
            results.append(res)
            b = baselines[f"{res['algo']},{res['d']},{res['m']}"]
            span = b["success"] - res["floor"]
            sig = (res["success"] - res["floor"]) / span
            print(f"{res['algo']:5s} {res['regime']:22s} d={res['d']} "
                  f"m={res['m']:2d} success={res['success']:.4f}"
                  f"±{res['stderr']:.4f} signal={sig:.3f} "
                  f"({res['elapsed_s']}s)", flush=True)

    with open("results/scaling_calibrated.json", "w") as f:
        json.dump({"sizes": SIZES, "strength": STRENGTH, "regimes": REGIMES,
                   "algos": ALGOS, "baselines": baselines,
                   "runs": results}, f, indent=1)
    print("\nwrote results/scaling_calibrated.json")


if __name__ == "__main__":
    main()
