"""Grid alignment as a first-class experimental variable.

Phase estimation concentrates probability on the phases s/r. When r divides
the control dimension D = d^m those phases sit exactly on grid points and
the interference peaks are perfectly sharp; otherwise they smear across
neighbouring outcomes and are far more fragile under noise. Which base gets
that gift is decided by the arithmetic of the instance, not by the physics.

order_confound.py established the effect on three instances. This is the
full series -- one instance per alignment class, including one that favours
each base and two that favour none:

    N = 21, a = 4   r = 3   exact grid for d = 3 only
    N = 15, a = 7   r = 4   exact grid for d = 2 only   (the original)
    N = 33, a = 4   r = 5   exact grid for d = 5 only
    N = 21, a = 2   r = 6   exact grid for NO base
    N = 29, a = 16  r = 7   exact grid for NO base

Prediction if grid alignment drives the result: the winner is whichever
base divides r, and the two unbiased instances are decided by physics.

Uses the trajectory engine rather than exact density matrices because the
d = 5 registers for N = 29 and N = 33 need 6 ququints (dim 15625, a 3.9 GB
density matrix). Writes results/grid_alignment.json.
Run: python3 grid_alignment.py
"""

import json
import os
import time
import zlib
from concurrent.futures import ProcessPoolExecutor

from qudit_shor import multiplicative_order, shor_config
from trajectories import shor_trajectories

INSTANCES = [(21, 4), (15, 7), (33, 4), (21, 2), (29, 16)]
BASES = [2, 3, 5]
NOISE = [("transmon_cal", 0.003), ("depolarizing", 0.005)]
N_TRAJ = 400


def one(args):
    d, a, N, model, s = args
    seed = zlib.crc32(f"{d},{a},{N},{model}".encode()) % (2 ** 32)
    t0 = time.time()
    res = shor_trajectories(d, m_for(d, N), model, s, n_traj=N_TRAJ,
                            seed=seed, a=a, N=N)
    res["a"], res["N"] = a, N
    res["elapsed_s"] = round(time.time() - t0, 1)
    return res


def m_for(d, N):
    m, _ = shor_config(d, N)
    return m


def main():
    os.makedirs("results", exist_ok=True)

    meta = {}
    for N, a in INSTANCES:
        r = multiplicative_order(a, N)
        for d in BASES:
            m = m_for(d, N)
            b = shor_trajectories(d, m, a=a, N=N)
            key = f"{N},{a},{d}"
            meta[key] = {"r": r, "D": d ** m, "m": m, "w": b["w"],
                         "exact_grid": (d ** m) % r == 0,
                         "floor": b["floor"], "baseline": b["success"]}
            print(f"N={N} a={a} r={r} d={d}: D={d**m} "
                  f"grid={str(meta[key]['exact_grid']):5s} "
                  f"floor={b['floor']:.3f} noiseless={b['success']:.3f}",
                  flush=True)

    jobs = [(d, a, N, model, s) for N, a in INSTANCES
            for model, s in NOISE for d in BASES]
    results = []
    with ProcessPoolExecutor(max_workers=4) as ex:
        for res in ex.map(one, jobs):
            mm = meta[f"{res['N']},{res['a']},{res['d']}"]
            res["r"] = mm["r"]
            res["exact_grid"] = mm["exact_grid"]
            res["signal"] = ((res["success"] - mm["floor"])
                             / (mm["baseline"] - mm["floor"]))
            results.append(res)
            print(f"N={res['N']:2d} a={res['a']:2d} r={res['r']} "
                  f"{res['noise_model']:13s} d={res['d']} "
                  f"grid={str(res['exact_grid']):5s} "
                  f"signal={res['signal']:6.3f}±"
                  f"{res['stderr'] / (mm['baseline'] - mm['floor']):.3f} "
                  f"({res['elapsed_s']}s)", flush=True)

    with open("results/grid_alignment.json", "w") as f:
        json.dump({"instances": INSTANCES, "noise": NOISE, "n_traj": N_TRAJ,
                   "meta": meta, "runs": results}, f, indent=1)
    print("\nwrote results/grid_alignment.json")


if __name__ == "__main__":
    main()
