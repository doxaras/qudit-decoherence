"""Interpolate between eigenstate QPE and Shor to isolate the mechanism.

Shor's work register starts in |x=1>, an equal superposition of the r = 4
eigenstates of the modular multiplier -- so Shor is phase estimation on a
4-fold eigenstate superposition. Running QPE on a K-fold superposition
therefore sweeps continuously from eigenstate QPE (K = 1, control and work
in a product state) to a Shor-like regime (K = 4, two bits of control-work
entanglement), with the circuit, metric and noise held fixed.

If the mechanism claim is right -- that the qudit disadvantage in Shor comes
from the work register carrying which-path information about the control --
then the ququint advantage should fall monotonically as K (equivalently, the
control-work entanglement entropy log2 K) increases.

Writes results/interpolation.json. Run: python3 interpolation_experiment.py
"""

import json
import os
import time
from concurrent.futures import ProcessPoolExecutor

from qpe_generic import control_work_entropy, qpe_superposition_trajectories

KS = [1, 2, 3, 4]
BASES = [2, 3, 5]
M = {2: 6, 3: 4, 5: 3}
NOISE = ["transmon_cal", "depolarizing"]
COSTS = ["uniform", "ion"]
STRENGTH = 0.005
N_TRAJ = 1000


def one(args):
    d, K, nm, cm = args
    t0 = time.time()
    r = qpe_superposition_trajectories(d, M[d], K, nm, STRENGTH,
                                       n_traj=N_TRAJ,
                                       seed=hash((d, K, nm, cm)) % (2 ** 32),
                                       cost_model=cm)
    r["elapsed_s"] = round(time.time() - t0, 1)
    return r


def main():
    os.makedirs("results", exist_ok=True)

    baselines, entropies = {}, {}
    for d in BASES:
        for K in KS:
            baselines[f"{d},{K}"] = qpe_superposition_trajectories(d, M[d], K)
            entropies[f"{d},{K}"] = control_work_entropy(d, M[d], K)
    print("baselines + entropies computed", flush=True)

    jobs = [(d, K, nm, cm) for nm in NOISE for cm in COSTS
            for K in KS for d in BASES]
    results = []
    with ProcessPoolExecutor(max_workers=6) as ex:
        for r in ex.map(one, jobs):
            b = baselines[f"{r['d']},{r['K']}"]
            span = b["success"] - r["floor"]
            r["signal"] = (r["success"] - r["floor"]) / span
            r["signal_err"] = r["stderr"] / span
            r["entropy_bits"] = entropies[f"{r['d']},{r['K']}"]
            results.append(r)
            print(f"{r['noise_model']:13s} {r['cost_model']:8s} "
                  f"K={r['K']} (S={r['entropy_bits']:.2f} bits) d={r['d']}: "
                  f"signal={r['signal']:.3f}±{r['signal_err']:.3f} "
                  f"({r['elapsed_s']}s)", flush=True)

    with open("results/interpolation.json", "w") as f:
        json.dump({"Ks": KS, "bases": BASES, "m": M, "noise": NOISE,
                   "costs": COSTS, "strength": STRENGTH, "n_traj": N_TRAJ,
                   "baselines": baselines, "entropies": entropies,
                   "runs": results}, f, indent=1)
    print("\nwrote results/interpolation.json")


if __name__ == "__main__":
    main()
