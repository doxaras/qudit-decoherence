"""Register-size scaling study via quantum trajectories.

Tests the prediction from docs/THEORY.md: on per-particle-noise platforms
the qudit advantage should GROW with problem size (noise exposure scales
with qudits x layers, and qudits compress both), while on ladder platforms
qubits should stay ahead regardless of size.

Sweeps the control-register size m (phase-estimation precision D = d^m) at
fixed noise strength, one strength per model, all bases. Writes
results/scaling.json. Run: python3 scaling_experiment.py
"""

import json
import os
import time
from concurrent.futures import ProcessPoolExecutor

from trajectories import shor_trajectories

SIZES = {2: [6, 8, 10, 12], 3: [4, 5, 6, 7], 5: [3, 4, 5]}
MODELS = [("depolarizing", 0.005), ("transmon", 0.003)]
N_TRAJ = 400
N_TRAJ_BIG = 200          # for the one very deep config
BIG = {(2, 12)}


def one_point(args):
    d, m, model, strength = args
    n_traj = N_TRAJ_BIG if (d, m) in BIG else N_TRAJ
    seed = hash((d, m, model, int(strength * 1e6))) % (2 ** 32)
    t0 = time.time()
    res = shor_trajectories(d, m, model, strength, n_traj=n_traj, seed=seed)
    res["elapsed_s"] = round(time.time() - t0, 1)
    return res


def main():
    os.makedirs("results", exist_ok=True)

    # exact noiseless baselines (single pure-state run each)
    baselines = {}
    for d, ms in SIZES.items():
        for m in ms:
            r = shor_trajectories(d, m)
            baselines[f"{d},{m}"] = r
            print(f"baseline d={d} m={m}: success={r['success']:.4f} "
                  f"floor={r['floor']:.4f}", flush=True)

    points = [(d, m, model, s) for d, ms in SIZES.items() for m in ms
              for model, s in MODELS]
    results = []
    with ProcessPoolExecutor(max_workers=6) as ex:
        for res in ex.map(one_point, points):
            results.append(res)
            b = baselines[f"{res['d']},{res['m']}"]
            span = b["success"] - res["floor"]
            sig = (res["success"] - res["floor"]) / span
            print(f"d={res['d']} m={res['m']:2d} {res['noise_model']:13s} "
                  f"s={res['strength']:<6g} success={res['success']:.4f}"
                  f"±{res['stderr']:.4f} signal={sig:.3f} "
                  f"({res['elapsed_s']}s, {res['n_traj']} traj)", flush=True)

    with open("results/scaling.json", "w") as f:
        json.dump({"sizes": SIZES, "models": MODELS,
                   "baselines": baselines, "runs": results}, f, indent=1)
    print("\nwrote results/scaling.json")


if __name__ == "__main__":
    main()
