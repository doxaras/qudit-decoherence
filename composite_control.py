"""Composite-dimension control, round 2: d = 6 on an alignment-neutral
instance.

Round-2 referee point (Gottesman): d = 4 is a PRIME POWER — GF(4)
exists and qudit stabilizer machinery works over it — so d = 4 cannot
retire the primality question. The dimension where the algebra
genuinely fails (Z_d not a field) is composite non-prime-power: d = 6.
Moreover, on the N = 21 (r = 6) demo instance d = 6 at m = 3 has
D = 216 divisible by r — exactly grid-aligned — so that instance is
useless for this control. We therefore run the second unbiased
benchmark, N = 29, a = 16 (r = 7), where no base d = 2..6 is aligned
(residual misalignment is printed per base for confirmation).

d = 2..6, uniform cost, both marked operating points, 1000
trajectories per point (registers reach 6^3 * 6^2 = 7776 total
dimensions, beyond comfortable exact DM at d = 6).

Writes results/composite_control.json. Run: python3 composite_control.py
"""

import json
import os
import time
import zlib
from concurrent.futures import ProcessPoolExecutor

import numpy as np

from qudit_shor import multiplicative_order, shor_config
from trajectories import shor_trajectories

N, A = 29, 16
BASES = [2, 3, 4, 5, 6]
POINTS = [("transmon_cal", 0.003), ("depolarizing", 0.005)]
N_TRAJ = 1000

RESULTS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results")


def residual(D: int, r: int) -> float:
    x = D * np.arange(1, r) / r
    return float(np.abs(x - np.round(x)).mean())


def one(args):
    d, model, s = args
    m, _ = shor_config(d, N)
    seed = zlib.crc32(f"{d},{N},{model},composite".encode()) % (2 ** 32)
    t0 = time.time()
    if model is None:
        res = shor_trajectories(d, m, a=A, N=N)
    else:
        res = shor_trajectories(d, m, model, s, n_traj=N_TRAJ, seed=seed,
                                a=A, N=N)
    res["model"] = model
    res["elapsed_s"] = round(time.time() - t0, 1)
    return res


def main():
    os.makedirs(RESULTS, exist_ok=True)
    r = multiplicative_order(A, N)
    print(f"N={N} a={A} r={r}")
    for d in BASES:
        m, w = shor_config(d, N)
        D = d ** m
        print(f"  d={d}: m={m} w={w} D={D} aligned={D % r == 0} "
              f"residual={residual(D, r):.4f}")

    jobs = [(d, None, 0.0) for d in BASES]
    jobs += [(d, model, s) for d in BASES for model, s in POINTS]
    with ProcessPoolExecutor(max_workers=5) as ex:
        runs = list(ex.map(one, jobs))

    base = {x["d"]: x for x in runs if x["model"] is None}
    out = {"N": N, "a": A, "r": r, "n_traj": N_TRAJ, "rows": []}
    print(f"\n{'model':>13} " + " ".join(f"{'d='+str(d):>14}" for d in BASES)
          + "   (signal ± err)")
    for model, s in POINTS:
        cells = []
        for d in BASES:
            x = next(y for y in runs if y["d"] == d and y["model"] == model)
            b = base[d]
            span = b["success"] - b["floor"]
            sig = (x["success"] - b["floor"]) / span
            err = x["stderr"] / span
            m, _ = shor_config(d, N)
            out["rows"].append({"d": d, "model": model, "strength": s,
                                "success": float(x["success"]),
                                "stderr": float(x["stderr"]),
                                "floor": b["floor"],
                                "baseline": b["success"], "span": span,
                                "signal": sig, "signal_err": err,
                                "residual": residual(d ** m, r)})
            cells.append(f"{sig:7.3f}±{err:.3f}")
        print(f"{model:>13} " + " ".join(f"{c:>14}" for c in cells))

    path = os.path.join(RESULTS, "composite_control.json")
    with open(path, "w") as f:
        json.dump(out, f, indent=1)
    print(f"\nwrote {path}")


if __name__ == "__main__":
    main()
