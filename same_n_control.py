"""Grid alignment isolated at FIXED register size.

grid_alignment.py varies the modulus N, and N sets the work-register width
w = ceil(log_d N). Between N = 15 and N = 21 base 2 gains a work qubit
(w: 4 -> 5) while bases 3 and 5 do not, so a sceptic can object that the
qubit's deficit on the unbiased instances is bought by a wider register
rather than by grid misalignment.

This removes the objection. Two moduli each host an aligned and an
unaligned order:

    N = 33   a = 4   r = 5    exact grid for d = 5   (5 | 125)
    N = 33   a = 2   r = 10   exact grid for NO base
    N = 55   a = 16  r = 5    exact grid for d = 5
    N = 55   a = 4   r = 10   exact grid for NO base

Within each modulus the two instances run on identical registers, identical
gate counts and identical noise exposure -- the ONLY difference is which
base can represent s/r exactly. Any ordering change is therefore grid
alignment and nothing else.

Why only d = 5 is isolated this way: a within-N control for base 2 needs an
order that divides 2^m, i.e. r = 4 (r = 2 and r = 1 are trivial). At every
modulus large enough to also carry a non-power-of-two order, r = 4 is
recovered by continued fractions from a *uniformly random* outcome more
often than from the actual noiseless run -- the floor exceeds the baseline
and the metric inverts (measured: N = 35, 39, 55, 65). That is itself a
consequence of running D >= 64 below the textbook D >= N^2 regime, and it
is why the N = 15, r = 4 instance the project started from is the only
base-2-aligned instance with a usable dynamic range.

Writes results/same_n_control.json. Run: python3 same_n_control.py
"""

import json
import os
import time
from concurrent.futures import ProcessPoolExecutor

from qudit_shor import multiplicative_order, shor_config
from trajectories import shor_trajectories

# (N, a) pairs; each modulus contributes one aligned and one unaligned order
INSTANCES = [(33, 4), (33, 2), (55, 16), (55, 4)]
BASES = [2, 3, 5]
NOISE = [("transmon_cal", 0.003), ("depolarizing", 0.005)]
N_TRAJ = 400


def one(args):
    d, a, N, model, s = args
    m, _ = shor_config(d, N)
    seed = hash((d, a, N, model)) % (2 ** 32)
    t0 = time.time()
    res = shor_trajectories(d, m, model, s, n_traj=N_TRAJ, seed=seed,
                            a=a, N=N)
    res["a"], res["N"] = a, N
    res["elapsed_s"] = round(time.time() - t0, 1)
    return res


def main():
    os.makedirs("results", exist_ok=True)
    meta = {}
    for N, a in INSTANCES:
        r = multiplicative_order(a, N)
        for d in BASES:
            m, _ = shor_config(d, N)
            b = shor_trajectories(d, m, a=a, N=N)
            key = f"{N},{a},{d}"
            meta[key] = {"r": r, "D": d ** m, "m": m, "w": b["w"],
                         "n_layers": b["n_layers"],
                         "exact_grid": (d ** m) % r == 0,
                         "floor": b["floor"], "baseline": b["success"]}
            mm = meta[key]
            print(f"N={N} a={a:2d} r={r:2d} d={d}: m={mm['m']} w={mm['w']} "
                  f"layers={mm['n_layers']:.0f} "
                  f"grid={str(mm['exact_grid']):5s} floor={mm['floor']:.3f} "
                  f"noiseless={mm['baseline']:.3f} "
                  f"span={mm['baseline'] - mm['floor']:.3f}", flush=True)

    jobs = [(d, a, N, model, s) for N, a in INSTANCES
            for model, s in NOISE for d in BASES]
    results = []
    with ProcessPoolExecutor(max_workers=4) as ex:
        for res in ex.map(one, jobs):
            mm = meta[f"{res['N']},{res['a']},{res['d']}"]
            span = mm["baseline"] - mm["floor"]
            res["r"] = mm["r"]
            res["exact_grid"] = mm["exact_grid"]
            res["signal"] = (res["success"] - mm["floor"]) / span
            res["signal_err"] = res["stderr"] / span
            results.append(res)
            print(f"N={res['N']} a={res['a']:2d} r={res['r']:2d} "
                  f"{res['noise_model']:13s} d={res['d']} "
                  f"grid={str(res['exact_grid']):5s} "
                  f"signal={res['signal']:6.3f}±{res['signal_err']:.3f} "
                  f"({res['elapsed_s']}s)", flush=True)

    with open("results/same_n_control.json", "w") as f:
        json.dump({"instances": INSTANCES, "noise": NOISE, "n_traj": N_TRAJ,
                   "meta": meta, "runs": results}, f, indent=1)
    print("\nwrote results/same_n_control.json")


if __name__ == "__main__":
    main()
