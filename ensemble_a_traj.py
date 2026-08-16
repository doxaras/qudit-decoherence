"""Multiplicative-group ensemble at arbitrary modulus, by trajectories.

Companion to ensemble_a.py (N = 21, exact DM): Shor draws a uniformly
from the units of Z_N, so the cross-dimension comparison is scored as
an ensemble average over all valid a. N = 33 (lambda = 10) carries the
order classes r in {2, 5, 10}: r = 5 exactly aligned in base 5, r = 2
in base 2, r = 10 in no base — alignment gifts in BOTH directions plus
an unbiased class. N = 55 (lambda = 20) adds r in {2, 4, 5, 10, 20}.

Registers reach 15625 total dimensions (d = 5, m = w = 3), beyond
comfortable exact-DM size, so this uses the trajectory engine with the
within-modulus convention of the paper: 400 trajectories per point
(same as results/same_n_control.json). Both marked operating points,
uniform (native-entangler) cost model.

Writes results/ensemble_a_n<N>.json.
Run: python3 ensemble_a_traj.py [N]   (default N = 33)
"""

import json
import os
import sys
import time
import zlib
from concurrent.futures import ProcessPoolExecutor
from math import gcd

import numpy as np

from qudit_shor import multiplicative_order, shor_config
from trajectories import shor_trajectories

BASES = [2, 3, 5]
POINTS = [("transmon_cal", 0.003), ("depolarizing", 0.005)]
N_TRAJ = 400

RESULTS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results")


def residual(D: int, r: int) -> float:
    x = D * np.arange(1, r) / r
    return float(np.abs(x - np.round(x)).mean())


def one(args):
    a, d, N, model, s = args
    m, _ = shor_config(d, N)
    seed = zlib.crc32(f"{a},{d},{N},{model}".encode()) % (2 ** 32)
    t0 = time.time()
    res = shor_trajectories(d, m, model, s, n_traj=N_TRAJ, seed=seed,
                            a=a, N=N)
    res["a"], res["model"], res["strength"] = a, model, s
    res["elapsed_s"] = round(time.time() - t0, 1)
    return res


def main():
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 33
    A_LIST = [a for a in range(2, N) if gcd(a, N) == 1]
    os.makedirs(RESULTS, exist_ok=True)
    orders = {a: multiplicative_order(a, N) for a in A_LIST}
    print(f"N = {N}: {len(A_LIST)} bases a, order classes "
          f"{sorted(set(orders.values()))}, {N_TRAJ} traj/point", flush=True)

    # noiseless meta: floor + baseline per (a, d)
    meta = {}
    for a in A_LIST:
        r = orders[a]
        for d in BASES:
            m, _ = shor_config(d, N)
            b = shor_trajectories(d, m, a=a, N=N)
            D = d ** m
            meta[(a, d)] = {"r": r, "D": D, "floor": b["floor"],
                            "baseline": b["success"],
                            "span": b["success"] - b["floor"],
                            "aligned": D % r == 0,
                            "residual": residual(D, r)}
    print("meta done", flush=True)

    jobs = [(a, d, N, model, s) for a in A_LIST for d in BASES
            for model, s in POINTS]
    rows = []
    t0 = time.time()
    with ProcessPoolExecutor(max_workers=6) as ex:
        for res in ex.map(one, jobs):
            a, d = res["a"], res["d"]
            mm = meta[(a, d)]
            span = mm["span"]
            sig = ((res["success"] - mm["floor"]) / span
                   if abs(span) > 1e-12 else float("nan"))
            rows.append({"a": a, "r": mm["r"], "d": d,
                         "model": res["model"], "strength": res["strength"],
                         "success": float(res["success"]),
                         "stderr": float(res["stderr"]),
                         "floor": mm["floor"], "baseline": mm["baseline"],
                         "span": span, "signal": sig,
                         "signal_err": (float(res["stderr"]) / span
                                        if abs(span) > 1e-12 else float("nan")),
                         "usable": span > 0.15, "aligned": mm["aligned"],
                         "residual": mm["residual"]})
            x = rows[-1]
            print(f"a={a:2d} r={x['r']:2d} d={d} {x['model']:13s} "
                  f"signal={x['signal']:6.3f}±{x['signal_err']:.3f} "
                  f"span={span:.3f} aligned={str(x['aligned']):5s} "
                  f"({x['elapsed_s'] if 'elapsed_s' in x else res['elapsed_s']}s)",
                  flush=True)
    print(f"all runs done in {time.time() - t0:.0f} s", flush=True)

    out = {"N": N, "n_traj": N_TRAJ, "a_list": A_LIST,
           "orders": {str(k): v for k, v in orders.items()},
           "rows": rows, "summary": {}}
    print(f"\n{'model':>13} {'d':>2} {'mean sig(usable)':>17} "
          f"{'mean succ':>10} {'n_usable':>9}")
    for model, s in POINTS:
        for d in BASES:
            sel = [x for x in rows if x["model"] == model and x["d"] == d]
            usable = [x for x in sel if x["usable"]]
            msu = (float(np.mean([x["signal"] for x in usable]))
                   if usable else float("nan"))
            msc = float(np.mean([x["success"] for x in sel]))
            out["summary"][f"{model}_d{d}"] = {
                "mean_signal_usable": msu, "mean_success": msc,
                "n_usable": len(usable), "n": len(sel)}
            print(f"{model:>13} {d:>2} {msu:>17.3f} {msc:>10.3f} "
                  f"{len(usable):>9}")

    print("\nper r-class (signal, usable only; * = exact alignment):")
    for model, s in POINTS:
        print(f"  {model} @ {s}")
        for r in sorted(set(orders.values())):
            n_a = sum(1 for v in orders.values() if v == r)
            line = f"    r={r:2d} (n_a={n_a}):"
            for d in BASES:
                sel = [x for x in rows if x["model"] == model and x["d"] == d
                       and x["r"] == r and x["usable"]]
                if sel:
                    star = "*" if sel[0]["aligned"] else " "
                    line += (f"  d={d}: "
                             f"{np.mean([x['signal'] for x in sel]):.3f}{star}")
                else:
                    line += f"  d={d}:   ----"
            print(line)

    path = os.path.join(RESULTS, f"ensemble_a_n{N}.json")
    with open(path, "w") as f:
        json.dump(out, f, indent=1)
    print(f"\nwrote {path}")


if __name__ == "__main__":
    main()
