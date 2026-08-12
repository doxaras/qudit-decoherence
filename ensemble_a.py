"""Ensemble over the multiplicative group: Shor signal averaged over ALL
valid bases a at fixed N, as the algorithm actually samples them.

Referee request (Floratos-style review, major comment 4): the paper
benchmarks fixed (N, a) pairs, but Shor draws a uniformly from the units
of Z_N; since the outcome is sensitive to the arithmetic of r =
ord_a(N), the honest cross-dimension comparison is the ensemble average
over a — which the grid-alignment theory (Sec. III) should predict
class by class.

N = 21: units {2,4,5,8,10,11,13,16,17,19,20}, orders r in {2,3,6}
(lambda(21) = 6). r = 2 aligns with every base (r | d^m for d even...
actually r=2 divides D only for d=2; for odd d never), r = 3 aligns
with base 3, r = 6 aligns with no base (the paper's unbiased class).

Exact density-matrix evolution, uniform (native-entangler) cost model,
both marked operating points: calibrated ladder at s = 0.003 and
per-particle depolarizing at s = 0.005. Writes results/ensemble_a.json.

Run: python3 ensemble_a.py
"""

import json
import os
import time
from concurrent.futures import ProcessPoolExecutor
from math import gcd

import numpy as np

from qudit_shor import (multiplicative_order, recovered_order, shor_config,
                        shor_run)

N = 21
BASES = [2, 3, 5]
POINTS = [("transmon_cal", 0.003), ("depolarizing", 0.005)]
A_LIST = [a for a in range(2, N) if gcd(a, N) == 1]

RESULTS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results")


def residual(D: int, r: int) -> float:
    """Mean distance of the r-1 phases s/r to the nearest grid point."""
    x = D * np.arange(1, r) / r
    return float(np.abs(x - np.round(x)).mean())


def uniform_floor(d: int, a: int, r: int) -> float:
    m, _ = shor_config(d, N)
    D = d ** m
    return sum(recovered_order(y, D, a, N) == r for y in range(D)) / D


def one(args):
    a, d, model, s = args
    t0 = time.time()
    res = shor_run(d, model, s, a=a, N=N) if model else shor_run(d, a=a, N=N)
    return {"a": a, "d": d, "model": model, "strength": s,
            "success": float(res["success"]),
            "elapsed_s": round(time.time() - t0, 1)}


def main():
    os.makedirs(RESULTS, exist_ok=True)
    orders = {a: multiplicative_order(a, N) for a in A_LIST}

    jobs = []
    for a in A_LIST:
        for d in BASES:
            jobs.append((a, d, None, 0.0))                 # noiseless baseline
            for model, s in POINTS:
                jobs.append((a, d, model, s))
    print(f"N = {N}: {len(A_LIST)} bases a, {len(jobs)} exact-DM runs")

    t0 = time.time()
    with ProcessPoolExecutor(max_workers=6) as ex:
        runs = list(ex.map(one, jobs))
    print(f"all runs done in {time.time() - t0:.0f} s")

    base_succ = {(x["a"], x["d"]): x["success"] for x in runs if x["model"] is None}
    rows = []
    for x in runs:
        if x["model"] is None:
            continue
        a, d = x["a"], x["d"]
        r = orders[a]
        m, _ = shor_config(d, N)
        D = d ** m
        fl = uniform_floor(d, a, r)
        bs = base_succ[(a, d)]
        span = bs - fl
        sig = (x["success"] - fl) / span if abs(span) > 1e-12 else float("nan")
        rows.append({"a": a, "r": r, "d": d, "model": x["model"],
                     "strength": x["strength"], "success": x["success"],
                     "floor": fl, "baseline": bs, "span": span,
                     "signal": sig, "usable": span > 0.15,
                     "aligned": D % r == 0, "residual": residual(D, r)})

    # ---- ensemble summary -------------------------------------------------
    out = {"N": N, "a_list": A_LIST, "orders": orders, "rows": rows,
           "summary": {}}
    print(f"\n{'model':>13} {'d':>2} {'mean sig':>9} {'mean sig(usable)':>17} "
          f"{'mean succ':>10} {'n_usable':>9}")
    for model, s in POINTS:
        for d in BASES:
            sel = [x for x in rows if x["model"] == model and x["d"] == d]
            usable = [x for x in sel if x["usable"]]
            ms = float(np.mean([x["signal"] for x in sel]))
            msu = float(np.mean([x["signal"] for x in usable])) if usable else float("nan")
            msc = float(np.mean([x["success"] for x in sel]))
            out["summary"][f"{model}_d{d}"] = {
                "mean_signal_all": ms, "mean_signal_usable": msu,
                "mean_success": msc, "n_usable": len(usable), "n": len(sel)}
            print(f"{model:>13} {d:>2} {ms:>9.3f} {msu:>17.3f} "
                  f"{msc:>10.3f} {len(usable):>9}")

    # ---- per order-class breakdown (alignment prediction test) ------------
    print("\nper r-class (signal, usable instances only; * = r | D exact "
          "alignment):")
    for model, s in POINTS:
        print(f"  {model} @ {s}")
        for r in sorted(set(orders.values())):
            line = f"    r={r} (n_a={sum(1 for v in orders.values() if v == r)}):"
            for d in BASES:
                sel = [x for x in rows if x["model"] == model and x["d"] == d
                       and x["r"] == r and x["usable"]]
                if sel:
                    star = "*" if sel[0]["aligned"] else " "
                    line += f"  d={d}: {np.mean([x['signal'] for x in sel]):.3f}{star}"
                else:
                    line += f"  d={d}:   ----"
            print(line)

    path = os.path.join(RESULTS, "ensemble_a.json")
    with open(path, "w") as f:
        json.dump(out, f, indent=1)
    print(f"\nwrote {path}")


if __name__ == "__main__":
    main()
