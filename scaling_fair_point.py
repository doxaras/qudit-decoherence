"""One register-size scaling point, same protocol as scaling_fair.py.

Measures a single (d, m) point on the unbiased instance (N = 21, a = 2)
under the study's four noise regimes, and writes it to its own file so it
can be merged over the main sweep. Two uses:

  * adding a size the main sweep never reached (d = 3, m = 9)
  * re-measuring an under-sampled point at higher statistics
    (d = 2, m = 12, originally 500 trajectories)

Merging is by override on (d, m, regime) -- see plots_scaling_fair.py --
so a re-measurement replaces the original rather than double-counting it
into the fits.

Unlike scaling_fair_m8.py this seeds deterministically: Python salts
str.__hash__ per process, so hash((label, d, m)) is not reproducible
across runs. crc32 of the same tuple is.

Run: python3 scaling_fair_point.py <d> <m> [n_traj]
Writes results/scaling_fair_d<d>_m<m>.json
"""

import json
import os
import sys
import time
import zlib
from concurrent.futures import ProcessPoolExecutor

from trajectories import shor_trajectories

N, A = 21, 2
REGIMES = [
    ("depolarizing", "depolarizing", 0.005, 1.0),
    ("transmon", "transmon", 0.003, 1.0),
    ("transmon_cal", "transmon_cal", 0.003, 1.0),
    ("transmon_cal_lowcharge", "transmon_cal", 0.003, 0.0),
]

D = int(sys.argv[1])
M = int(sys.argv[2])
N_TRAJ = int(sys.argv[3]) if len(sys.argv) > 3 else 1000


def one_point(args):
    label, model, strength, dephase_ratio = args
    seed = zlib.crc32(f"{label},{D},{M}".encode()) % (2 ** 32)
    t0 = time.time()
    res = shor_trajectories(D, M, model, strength, n_traj=N_TRAJ, seed=seed,
                            a=A, N=N, dephase_ratio=dephase_ratio)
    res["regime"] = label
    res["seed"] = seed
    res["elapsed_s"] = round(time.time() - t0, 1)
    return res


def main():
    os.makedirs("results", exist_ok=True)
    out = f"results/scaling_fair_d{D}_m{M}.json"
    base = shor_trajectories(D, M, a=A, N=N)
    print(f"baseline d={D} m={M}: success={base['success']:.4f} "
          f"floor={base['floor']:.4f} layers={base['n_layers']:.0f} "
          f"dim={D ** base['n_qudits']} traj={N_TRAJ}", flush=True)

    results = []
    with ProcessPoolExecutor(max_workers=4) as ex:
        for res in ex.map(one_point, REGIMES):
            span = base["success"] - res["floor"]
            res["signal"] = (res["success"] - res["floor"]) / span
            results.append(res)
            print(f"{res['regime']:22s} success={res['success']:.4f}"
                  f"±{res['stderr']:.4f} signal={res['signal']:6.3f} "
                  f"({res['elapsed_s']}s)", flush=True)

    with open(out, "w") as f:
        json.dump({"N": N, "a": A, "d": D, "m": M, "n_traj": N_TRAJ,
                   "baseline": base, "runs": results}, f, indent=1)
    print(f"\nwrote {out}")


if __name__ == "__main__":
    main()
