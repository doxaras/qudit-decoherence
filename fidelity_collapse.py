"""Does END-STATE FIDELITY collapse where decoded signal does not?

exposure_collapse.py showed that in damage units (exposure x per-layer
entanglement infidelity of the channel) the Grover families collapse onto
one exponential almost exactly, while the Shor families do not -- Shor
d=3's decoded signal sits flat while its exposure triples. The proposed
explanation: continued-fraction order recovery is an error-tolerant
decoder whose tolerance grows with register size, so Shor's *signal*
stops tracking the physical decay of its *state*.

This is directly testable. Here we re-run the same grid of circuits and
record fidelity of the pre-measurement state to the noiseless state,
F = <psi_ideal| rho |psi_ideal>, instead of decoded success:

  * Grover: exact density-matrix evolution (registers are small), fidelity
    averaged over the same marked-item sample as grover_study.
  * Shor (N=21, a=2, the unbiased instance of scaling_fair): Monte Carlo
    wavefunction trajectories; averaging |<psi_ideal|psi_traj>|^2 over
    trajectories is an unbiased estimator of <psi_ideal|rho|psi_ideal>.

If fidelity from both algorithms lands on one damage-unit exponential,
the residual structure in the signal collapse is entirely the decoder
transfer function and the mechanism claim closes. If Shor's *fidelity* is
also anomalous, the residual is physics we have not identified.

Writes results/fidelity_collapse.json, then prints the collapse fits.
Run: python3 fidelity_collapse.py            (~20-40 min, 5 workers)
     python3 fidelity_collapse.py analyze    (re-analyze existing JSON)
"""

import json
import os


def _scaling_fair_path():
    p = "results/scaling_fair_1000.json"
    return p if os.path.exists(p) else "results/scaling_fair.json"

import sys
import time
import zlib
from concurrent.futures import ProcessPoolExecutor

import numpy as np

from exposure_collapse import ent_fidelity, fit_exp, fit_nested
from grover import _marked_sample, grover_gates, optimal_iterations
from qudit_shor import (apply_channel, apply_cost_model, apply_unitary,
                        apply_unitary_vec, build_shor_gates, channels_by_cost,
                        shor_config)
from trajectories import _kraus_sets, _sample_kraus

N_SHOR, A_SHOR = 21, 2
SHOR_SIZES = {2: [6, 8, 10, 12], 3: [4, 5, 6, 7], 5: [3, 4, 5]}
GROVER_SIZES = {2: [4, 6, 8], 3: [3, 4, 5], 5: [2, 3, 4]}
REGIMES = [("transmon_cal", 0.003), ("depolarizing", 0.005)]
N_TRAJ = 200
N_TRAJ_BIG = 100                  # the one very deep config (d=2, m=12)
BIG = {(2, 12)}
OUT = "results/fidelity_collapse.json"


def _seed(*key) -> int:
    return zlib.crc32(",".join(map(str, key)).encode())


def shor_fidelity(d: int, m: int, model: str, strength: float,
                  n_traj: int, seed: int) -> dict:
    """Trajectory estimate of <psi_ideal|rho|psi_ideal> at end of circuit."""
    _, w = shor_config(d, N_SHOR)
    dims = [d] * (m + w)
    n = len(dims)
    gates = apply_cost_model(build_shor_gates(d, m, w, A_SHOR, N_SHOR), d,
                             "uniform")
    psi0 = np.zeros(d ** n, complex)
    psi0[1] = 1.0                 # control = |0...0>, work = |x=1>
    psi0 = psi0.reshape(dims)

    ideal = psi0
    for sites, U, _ in gates:
        ideal = apply_unitary_vec(ideal, U, sites, dims)
    ideal_flat = ideal.reshape(-1).conj()

    costs = {cost for _, _, cost in gates}
    kraus_sets = _kraus_sets(d, model, strength, costs)
    rng = np.random.default_rng(seed)
    fids = np.empty(n_traj)
    for k in range(n_traj):
        t = psi0
        for sites, U, cost in gates:
            t = apply_unitary_vec(t, U, sites, dims)
            for q in range(n):
                t = _sample_kraus(t, q, n, kraus_sets[cost], rng, dims)
        fids[k] = np.abs(ideal_flat @ t.reshape(-1)) ** 2

    return {"alg": "shor", "d": d, "size": m,
            "bits": m * np.log2(d), "n_qudits": n,
            "n_layers": sum(c for _, _, c in gates),
            "model": model, "strength": strength,
            "fidelity": float(fids.mean()),
            "stderr": float(fids.std(ddof=1) / np.sqrt(n_traj)),
            "n_traj": n_traj}


def grover_fidelity(d: int, n: int, model: str, strength: float,
                    n_marked: int = 8, seed: int = 7) -> dict:
    """Exact density-matrix fidelity, averaged over the marked-item sample."""
    M = d ** n
    T = optimal_iterations(M)
    dims = [d] * n
    fids, layers = [], None
    for marked in _marked_sample(M, n_marked, seed):
        gates = apply_cost_model(grover_gates(d, n, marked, T), d, "uniform")
        layers = sum(c for _, _, c in gates)
        E = channels_by_cost(d, gates, model, strength, 1.0)

        psi = np.zeros(M, complex)
        psi[0] = 1.0
        psi = psi.reshape(dims)
        rho = np.zeros((M, M), complex)
        rho[0, 0] = 1.0
        rho = rho.reshape(dims + dims)
        for sites, U, cost in gates:
            psi = apply_unitary_vec(psi, U, sites, dims)
            rho = apply_unitary(rho, U, sites, dims)
            for q in range(n):
                rho = apply_channel(rho, E[cost], q, dims)
        v = psi.reshape(-1)
        fids.append(float(np.real(v.conj() @ rho.reshape(M, M) @ v)))

    fids = np.array(fids)
    return {"alg": "grover", "d": d, "size": n,
            "bits": n * np.log2(d), "n_qudits": n, "n_layers": layers,
            "model": model, "strength": strength,
            "fidelity": float(fids.mean()),
            "stderr": float(fids.std(ddof=1) / np.sqrt(len(fids))),
            "n_traj": 0}


def one_point(args):
    t0 = time.time()
    if args[0] == "shor":
        _, d, m, model, s = args
        n_traj = N_TRAJ_BIG if (d, m) in BIG else N_TRAJ
        res = shor_fidelity(d, m, model, s, n_traj, _seed(model, d, m))
    else:
        _, d, n, model, s = args
        res = grover_fidelity(d, n, model, s)
    res["elapsed_s"] = round(time.time() - t0, 1)
    print(f"{res['alg']:6s} {res['model']:12s} d={res['d']} "
          f"size={res['size']:2d} F={res['fidelity']:.4f}"
          f"±{res['stderr']:.4f} ({res['elapsed_s']}s)", flush=True)
    return res


# ----------------------------------------------------------------------
# analysis: same fits as exposure_collapse, with fidelity as the ordinate
# ----------------------------------------------------------------------

def analyze(points):
    signal = load_signals()
    for model, s in REGIMES:
        sub = [p for p in points if p["model"] == model]
        y = [p["fidelity"] for p in sub]
        algs = [p["alg"] for p in sub]
        x = [p["n_qudits"] * p["n_layers"]
             * (1 - ent_fidelity(p["d"], model, p["strength"])) for p in sub]
        print(f"\n=== {model}: fidelity vs damage-unit exposure "
              f"({len(sub)} points) ===")
        f = fit_exp(x, y)
        print(f"pooled: A = {f['A']:.3f}  k = {f['k']:.4f}  "
              f"R^2 = {f['r2']:.3f}")
        nest = fit_nested(x, y, algs)
        for mname, mres in nest.items():
            print(f"  {mname:22s} R^2 = {mres['r2']:.3f}")
        print(f"{'family':14s} {'k(fid)':>8s} {'R^2 loglin':>11s} "
              f"{'fid range':>15s} {'sig range':>15s}")
        for alg in ("grover", "shor"):
            for d in (2, 3, 5):
                fam = [(xi, p) for xi, p in zip(x, sub)
                       if p["alg"] == alg and p["d"] == d]
                if len(fam) < 3:
                    continue
                fx = np.array([xi for xi, _ in fam])
                fy = np.array([p["fidelity"] for _, p in fam])
                ly = np.log(np.maximum(fy, 1e-12))
                slope, icpt = np.polyfit(fx, ly, 1)
                r2 = 1 - np.sum((ly - (slope * fx + icpt)) ** 2) \
                    / np.sum((ly - ly.mean()) ** 2)
                sig = [signal.get((alg, d, p["size"], model)) for _, p in fam]
                sigtxt = (f"{min(sig):.3f}..{max(sig):.3f}"
                          if None not in sig else "n/a")
                print(f"{alg} d={d:8d} {-slope:8.4f} {r2:11.3f} "
                      f"{fy.min():7.4f}..{fy.max():.4f} {sigtxt:>15s}")


def load_signals():
    out = {}
    g = json.load(open("results/grover.json"))
    for r in g["scaling"]:
        out[("grover", r["d"], r["n"], r["noise_model"])] = r["signal"]
    s = json.load(open(_scaling_fair_path()))
    for r in s["runs"]:
        if r["regime"] in ("transmon_cal", "depolarizing"):
            out[("shor", r["d"], r["m"], r["noise_model"])] = r["signal"]
    return out


def main():
    if len(sys.argv) > 1 and sys.argv[1] == "analyze":
        analyze(json.load(open(OUT))["points"])
        return

    os.makedirs("results", exist_ok=True)
    points = [("shor", d, m, model, s)
              for model, s in REGIMES
              for d, ms in SHOR_SIZES.items() for m in ms]
    points += [("grover", d, n, model, s)
               for model, s in REGIMES
               for d, ns in GROVER_SIZES.items() for n in ns]
    # deepest configs first so the pool stays balanced
    points.sort(key=lambda p: -(p[1] ** p[2]))

    t0 = time.time()
    with ProcessPoolExecutor(max_workers=5) as ex:
        results = list(ex.map(one_point, points))
    print(f"\ntotal {round(time.time() - t0)}s")

    with open(OUT, "w") as fh:
        json.dump({"N_shor": N_SHOR, "a_shor": A_SHOR,
                   "shor_sizes": SHOR_SIZES, "grover_sizes": GROVER_SIZES,
                   "regimes": REGIMES, "n_traj": N_TRAJ,
                   "points": results}, fh, indent=1)
    print(f"wrote {OUT}")
    analyze(results)


if __name__ == "__main__":
    main()
