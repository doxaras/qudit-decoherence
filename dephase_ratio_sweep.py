"""Sweep the ladder channel's T2/T1 balance and re-score Table III.

Round-4 referee point (R1-M3a): `dephase_ratio` -- the weight of pure
dephasing relative to relaxation in the calibrated ladder channel --
defaults to 1.0 everywhere, which fixes T2 = T1 on the qubit subspace
by construction. Real transmons span roughly T2 = 0.3 T1 to 2 T1, and
dephasing is the part of the ladder that scales worst with d, so this
constant sits on the causal path to every ladder verdict.

This sweeps dephase_ratio over 0.2-5 and recomputes the ladder rows of
the central cost table (tab:cost; unbiased instance N = 21, a = 2,
r = 6, s = 0.005, exact density matrices) two ways:

  * raw: same strength s at every ratio. Turning up the ratio makes
    the whole channel noisier for every base at once.
  * matched: s rescaled so the QUBIT's per-carrier-layer damage
    1 - F_e(2) is the same as at ratio 1.0. This isolates the effect
    the referee is pointing at -- the d-dependent *structure* of
    dephasing -- from the overall noise level.

Writes results/dephase_ratio_sweep.json.
Run: python3 dephase_ratio_sweep.py
"""

import json
import os
import time
from concurrent.futures import ProcessPoolExecutor

import numpy as np

from plots import uniform_floor
from qudit_shor import noise_superop, shor_run

N, A = 21, 2
S = 0.005
RATIOS = [0.2, 0.5, 1.0, 2.0, 5.0]
COSTS = ["uniform", "ion", "pavlidis"]
BASES = [2, 3, 5]
S0 = 1e-6  # probe strength for the damage-rate coefficients


def damage_rate(d: int, ratio: float) -> float:
    """Per-carrier-layer entanglement infidelity per unit strength."""
    Sop = noise_superop(d, "transmon_cal", S0, dephase_ratio=ratio)
    return float((1.0 - np.trace(Sop).real / d ** 2) / S0)


def one(args):
    d, cost, ratio, s, tag = args
    t0 = time.time()
    r = shor_run(d, "transmon_cal", s, a=A, N=N, cost_model=cost,
                 dephase_ratio=ratio)
    return dict(d=d, cost=cost, ratio=ratio, strength=s, mode=tag,
                success=float(r["success"]), layers=r["n_layers"],
                elapsed_s=round(time.time() - t0, 1))


def main():
    os.makedirs("results", exist_ok=True)
    rates = {f"{d},{ratio}": damage_rate(d, ratio)
             for d in BASES for ratio in RATIOS}
    print("per-carrier-layer damage rates Delta(d, ratio):")
    for ratio in RATIOS:
        row = [rates[f"{d},{ratio}"] for d in BASES]
        print(f"  ratio={ratio:<4g} d=2/3/5: "
              + "/".join(f"{x:.4f}" for x in row)
              + f"   (d=3)/(d=2)={row[1]/row[0]:.3f}"
              + f" (d=5)/(d=2)={row[2]/row[0]:.3f}", flush=True)

    floors = {d: uniform_floor(d, A, N) for d in BASES}
    bases = {d: float(shor_run(d, a=A, N=N)["success"]) for d in BASES}

    jobs = [(d, cost, ratio, S, "raw")
            for ratio in RATIOS for cost in COSTS for d in BASES]
    jobs += [(d, cost, ratio,
              S * rates["2,1.0"] / rates[f"2,{ratio}"], "matched")
             for ratio in RATIOS if ratio != 1.0
             for cost in COSTS for d in BASES]

    results = []
    with ProcessPoolExecutor(max_workers=4) as ex:
        for r in ex.map(one, jobs):
            d = r["d"]
            r["signal"] = ((r["success"] - floors[d])
                           / (bases[d] - floors[d]))
            results.append(r)
            print(f"{r['mode']:7s} ratio={r['ratio']:<4g} {r['cost']:9s} "
                  f"d={d} s={r['strength']:.5f} "
                  f"signal={r['signal']:6.3f} ({r['elapsed_s']}s)",
                  flush=True)

    print("\n=== ladder rows of tab:cost vs dephase_ratio ===")
    for mode in ("raw", "matched"):
        print(f"-- {mode} --")
        for ratio in RATIOS:
            if mode == "matched" and ratio == 1.0:
                continue
            for cost in COSTS:
                sig = {r["d"]: r["signal"] for r in results
                       if r["mode"] == mode and r["ratio"] == ratio
                       and r["cost"] == cost}
                win = max(sig, key=sig.get)
                print(f"   ratio={ratio:<4g} {cost:9s} "
                      + " ".join(f"d{d}={sig[d]:.3f}" for d in BASES)
                      + f"   winner d={win}")

    with open("results/dephase_ratio_sweep.json", "w") as f:
        json.dump({"N": N, "a": A, "strength": S, "ratios": RATIOS,
                   "costs": COSTS, "bases": BASES,
                   "damage_rates": rates, "floors": floors,
                   "baselines": bases, "runs": results}, f, indent=1)
    print("wrote results/dephase_ratio_sweep.json")


if __name__ == "__main__":
    main()
