"""Fifth qutrit scaling point: d = 3, m = 8 (D = 6561, 12.7 bits).

The paper's qutrit flat-slope observation (-0.006 +/- 0.004 signal/bit
under the calibrated ladder) rests on four sizes spanning 6.3-11.1 bits,
and the Limitations concede four points cannot separate a flat trend
from a slow one. This adds a fifth point 1.6 bits deeper than the
previous largest -- and deeper in precision than any register in the
study -- under the same four regimes and protocol as scaling_fair.py
(N = 21, a = 2; 500 trajectories, the deep-config statistics used at
d = 2, m = 12).

Writes results/scaling_fair_m8.json. Run: python3 scaling_fair_m8.py
"""

import json
import os
import sys
import time
from concurrent.futures import ProcessPoolExecutor

from trajectories import shor_trajectories

N, A = 21, 2
D, M = 3, 8
REGIMES = [
    ("depolarizing", "depolarizing", 0.005, 1.0),
    ("transmon", "transmon", 0.003, 1.0),
    ("transmon_cal", "transmon_cal", 0.003, 1.0),
    ("transmon_cal_lowcharge", "transmon_cal", 0.003, 0.0),
]
N_TRAJ = int(sys.argv[1]) if len(sys.argv) > 1 else 500


def one_point(args):
    label, model, strength, dephase_ratio = args
    seed = hash((label, D, M)) % (2 ** 32)
    t0 = time.time()
    res = shor_trajectories(D, M, model, strength, n_traj=N_TRAJ, seed=seed,
                            a=A, N=N, dephase_ratio=dephase_ratio)
    res["regime"] = label
    res["elapsed_s"] = round(time.time() - t0, 1)
    return res


def main():
    os.makedirs("results", exist_ok=True)
    base = shor_trajectories(D, M, a=A, N=N)
    print(f"baseline d={D} m={M}: success={base['success']:.4f} "
          f"floor={base['floor']:.4f} layers={base['n_layers']:.0f}",
          flush=True)

    results = []
    with ProcessPoolExecutor(max_workers=4) as ex:
        for res in ex.map(one_point, REGIMES):
            span = base["success"] - res["floor"]
            res["signal"] = (res["success"] - res["floor"]) / span
            results.append(res)
            print(f"{res['regime']:22s} success={res['success']:.4f}"
                  f"±{res['stderr']:.4f} signal={res['signal']:6.3f} "
                  f"({res['elapsed_s']}s)", flush=True)

    with open("results/scaling_fair_m8.json", "w") as f:
        json.dump({"N": N, "a": A, "d": D, "m": M, "n_traj": N_TRAJ,
                   "baseline": base, "runs": results}, f, indent=1)
    print("\nwrote results/scaling_fair_m8.json")


if __name__ == "__main__":
    main()
