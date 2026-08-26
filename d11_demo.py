"""d = 11 and d = 13: the primes past the break-even bar.

The d = 7 grid (d7_demo.py) found the native-gate window narrowing:
d = 7 clears nothing at the gate level (its Jankovic bar is 5.70
against a uniform layer ratio of 3.80) yet still beats the qubit on
both channels, the criterion being conservative under our calibrated
relaxation. The next primes sharpen the question. At d = 11 the demo
register collapses to m = w = 2 (D = 121, 4 carriers, 9 uniform
layers), and the layer ratio 57/9 = 6.3 sits far below the bar
(11²−1)/(3 log2 11) = 11.56; at d = 13 the bar is 15.13, further
still. Meanwhile the ladder's per-event damage
keeps climbing with the max-level law. Whether the algorithm-level
advantage survives at these dimensions is decided here, on the same
unbiased instance and conventions as d7_demo.py.

Both bases have residual misalignment exactly 0.300 (121 ≡ 169 ≡ 1
mod 6), identical to bases 3, 5, 7 — printed below as a check, so the
comparison stays alignment-fair.

Quantum trajectories, 1000/point; the qubit comparators live in
results/d7_demo.json (same instance, noise points, seeds convention).
Writes results/d11_demo.json. Run: python3 d11_demo.py
"""

import json
import os
import sys
import time
import zlib
from concurrent.futures import ProcessPoolExecutor

import numpy as np

from qudit_shor import noise_superop, shor_config
from trajectories import shor_trajectories

N, A = 21, 2
BASES = [11, 13]
NOISE = [("depolarizing", 0.005), ("transmon_cal", 0.005),
         ("transmon_cal", 0.003)]
COSTS = ["uniform", "ion", "pavlidis"]
N_TRAJ = int(sys.argv[1]) if len(sys.argv) > 1 else 1000
R = 6


def misalignment(d: int) -> float:
    m, _ = shor_config(d, N)
    D = d ** m
    off = [(D * s / R) % 1.0 for s in range(1, R)]
    return float(np.mean([min(x, 1 - x) for x in off]))


def damage_rate(d: int) -> float:
    s0 = 1e-6
    S = noise_superop(d, "transmon_cal", s0)
    return float((1.0 - np.trace(S).real / d ** 2) / s0)


def one_point(args):
    d, model, s, cost = args
    m, _ = shor_config(d, N)
    seed = zlib.crc32(f"{d},{model},{int(s * 1e6)},{cost}".encode()) % (2 ** 32)
    t0 = time.time()
    res = shor_trajectories(d, m, model, s, n_traj=N_TRAJ, seed=seed,
                            a=A, N=N, cost_model=cost)
    res["cost_model"] = cost
    res["elapsed_s"] = round(time.time() - t0, 1)
    return res


def main():
    os.makedirs("results", exist_ok=True)
    for d in BASES:
        m, w = shor_config(d, N)
        bar = (d ** 2 - 1) / (3 * np.log2(d))
        print(f"d={d}: m={m} w={w} D={d ** m}  misalign={misalignment(d):.3f} "
              f"ladder damage {damage_rate(d):.3f}/s  "
              f"jankovic bar {bar:.2f}", flush=True)

    baselines = {}
    for d in BASES:
        m, w = shor_config(d, N)
        r = shor_trajectories(d, m, a=A, N=N)
        baselines[str(d)] = r
        print(f"baseline d={d}: success={r['success']:.4f} "
              f"floor={r['floor']:.4f} layers={r['n_layers']:g}", flush=True)

    points = [(d, model, s, cost) for d in BASES
              for model, s in NOISE for cost in COSTS]
    results = []
    with ProcessPoolExecutor(max_workers=2) as ex:
        for res in ex.map(one_point, points):
            b = baselines[str(res["d"])]
            span = b["success"] - res["floor"]
            res["signal"] = (res["success"] - res["floor"]) / span
            res["signal_err"] = res["stderr"] / span
            results.append(res)
            print(f"d={res['d']} {res['noise_model']:13s} "
                  f"s={res['strength']:<6g} {res['cost_model']:9s} "
                  f"layers={res['n_layers']:7.2f} "
                  f"signal={res['signal']:6.3f}±{res['signal_err']:.3f} "
                  f"({res['elapsed_s']}s)", flush=True)

    qubit = {}
    try:
        d7 = json.load(open("results/d7_demo.json"))
        for r in d7["runs"]:
            if r["d"] == 2:
                b = d7["baselines"]["2"]
                span = b["success"] - r["floor"]
                qubit[f"{r['noise_model']},{r['strength']},{r['cost_model']}"] = \
                    (r["success"] - r["floor"]) / span
    except FileNotFoundError:
        pass

    print("\n=== vs the d=2 comparator (from d7_demo.json) ===")
    for model, s in NOISE:
        for cost in COSTS:
            q = qubit.get(f"{model},{s},{cost}")
            row = {r["d"]: r["signal"] for r in results
                   if r["noise_model"] == model and r["strength"] == s
                   and r["cost_model"] == cost}
            qs = f"{q:.3f}" if q is not None else "  -- "
            print(f"{model:13s} s={s:<6g} {cost:9s} d2={qs} "
                  + " ".join(f"d{d}={row[d]:.3f}" for d in BASES), flush=True)

    with open("results/d11_demo.json", "w") as f:
        json.dump({"N": N, "a": A, "r": R, "bases": BASES, "noise": NOISE,
                   "costs": COSTS, "n_traj": N_TRAJ,
                   "misalignment": {d: misalignment(d) for d in BASES},
                   "ladder_damage_per_s": {d: damage_rate(d) for d in BASES},
                   "baselines": baselines, "runs": results}, f, indent=1)
    print("wrote results/d11_demo.json")


if __name__ == "__main__":
    main()
