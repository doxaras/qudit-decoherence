"""Quasi-static and correlated versions of the calibrated ladder.

Round-4 referee points R1-M4 and R1-M5: the paper's quasi-static and
common-mode controls exist only for the ion Zeeman channel, yet the
calibrated ladder's own stated microscopic mechanism -- charge
dispersion -- is 1/f and quasi-static on gate timescales, and
transmons sharing a feedline or a TLS bath acquire spatially
correlated dephasing. Both substitutions are made here, on the
paper's own dephasing structure.

The calibrated dephasing is realized by diagonal jumps
L_m = diag(c_m); the level vectors v_j = (c_1(j), c_2(j), ...) from
that Euclidean embedding are exactly the sensitivity vectors a
quasi-static model needs: a static offset vector xi (drawn once per
shot) gives level j the phase rate xi . v_j, and Gaussian averaging
reproduces pair damping exp[-sigma^2 |v_j-v_k|^2 L^2 / 2] -- the
quasi-static counterpart of the Markovian exp[-Gamma_phi(j,k) L],
with the SAME pair structure. Relaxation stays Markovian and local
throughout (T1 decay genuinely is), so the only variables are the
temporal character of the dephasing (markov vs quasi-static) and its
spatial correlation (local vs common-mode):

    markov_local   the paper's channel (reference)
    markov_common  one Lindblad field per register: superdecoherence,
                   with decoherence-free pairs (R1-M5)
    qs_local       per-carrier static offsets, trajectories (R1-M4)
    qs_common      one static offset for the register (M4 x M5)

Normalization follows ion_zeeman_quasistatic.py: sigma is set ONCE,
by matching the Markovian 0<->1 dephasing damage over the d = 2
uniform-cost circuit (sigma^2 = s / L2), then held fixed across every
base and cost model. One apparatus, one bath.

Demo instance (N = 21, a = 2, r = 6), s = 0.003 (the marked transmon
operating point, as tab:exponent), uniform and ion costs.

Writes results/ladder_quasistatic.json.
Run: python3 ladder_quasistatic.py
"""

import json
import os
import sys
import time
import zlib
from concurrent.futures import ProcessPoolExecutor

import numpy as np

from plots import uniform_floor
from qudit_shor import (_mds_dephasing_jumps, apply_channel, apply_cost_model,
                        apply_unitary, apply_unitary_vec, build_shor_gates,
                        control_probs, dephasing_matrix, initial_state,
                        layer_count, multiplicative_order, noise_superop_pow,
                        recovered_order, shor_config, shor_run)
from trajectories import _kraus_sets, _sample_kraus, good_outcome_mask

N, A = 21, 2
BASES = [2, 3, 5]
COSTS = ["uniform", "ion"]
S = 0.003
N_TRAJ = int(sys.argv[1]) if len(sys.argv) > 1 else 1000

RESULTS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results")


def level_vectors(d: int) -> np.ndarray:
    """v_j at unit rate: rows are levels, columns the diagonal jumps."""
    jumps = _mds_dephasing_jumps(dephasing_matrix(d, 1.0))
    return np.stack([np.real(np.diag(L)) for L in jumps], axis=1)


def sigma_matched() -> float:
    """sigma^2 = s / L2: quasi-static (0,1) damage over the d=2 uniform
    circuit equals the Markovian channel's."""
    m2, w2 = shor_config(2, N)
    L2 = layer_count(apply_cost_model(build_shor_gates(2, m2, w2, A, N),
                                      2, "uniform"))
    return float(np.sqrt(S / L2))


# --- exact density-matrix runs (markov_local / markov_common) --------------

def run_markov(d: int, cost_model: str, common: bool) -> np.ndarray:
    m, w = shor_config(d, N)
    n = m + w
    dims = [d] * n
    gates = apply_cost_model(build_shor_gates(d, m, w, A, N), d, cost_model)
    costs = {g[2] for g in gates}

    if not common:
        E = {c: noise_superop_pow(d, "transmon_cal", S, c) for c in costs}
        decay = None
    else:
        # local Markovian relaxation + one collective dephasing field:
        # basis state a carries V_a = sum_q v(level_q); coherence (a, b)
        # decays at s * |V_a - V_b|^2 / 2 per layer.
        E = {c: noise_superop_pow(d, "transmon_cal", S, c, dephase_ratio=0.0)
             for c in costs}
        v = level_vectors(d)
        D = d ** n
        V = np.zeros((D, len(v[0])))
        idx = np.arange(D)
        for q in range(n):
            V += v[(idx // d ** (n - 1 - q)) % d]
        sq = (V ** 2).sum(axis=1)
        dist2 = sq[:, None] + sq[None, :] - 2.0 * (V @ V.T)
        decay = {c: np.exp(-S * c * 0.5 * np.maximum(dist2, 0.0))
                 for c in costs}

    D = d ** n
    rho = initial_state(dims, m, d, w)
    for sites, U, cost in gates:
        rho = apply_unitary(rho, U, sites, dims)
        if decay is not None:
            rho = (rho.reshape(D, D) * decay[cost]).reshape(dims + dims)
        for q in range(n):
            rho = apply_channel(rho, E[cost], q, dims)
    return control_probs(rho, d, m, w)


# --- trajectory runs (qs_local / qs_common) --------------------------------

def run_quasistatic(d: int, cost_model: str, common: bool, sigma: float,
                    n_traj: int, seed: int) -> dict:
    m, w = shor_config(d, N)
    n = m + w
    dims = [d] * n
    gates = apply_cost_model(build_shor_gates(d, m, w, A, N), d, cost_model)
    costs = {g[2] for g in gates}
    v = level_vectors(d)                      # (d, k)
    k = v.shape[1]

    # Markovian relaxation only; dephasing comes from the static offsets
    kraus_sets = _kraus_sets(d, "transmon_cal", S, costs, dephase_ratio=0.0)

    Dc, Dw = d ** m, d ** w
    good = good_outcome_mask(d, m, A, N)
    psi0 = np.zeros(Dc * Dw, complex)
    psi0[1] = 1.0
    psi0 = psi0.reshape(dims)

    rng = np.random.default_rng(seed)
    successes = np.empty(n_traj)
    shape = [1] * n
    for t_i in range(n_traj):
        if common:
            theta = np.tile(v @ rng.normal(0.0, sigma, size=k), (n, 1))
        else:
            theta = rng.normal(0.0, sigma, size=(n, k)) @ v.T  # (n, d)
        phases = [np.exp(-1j * theta[q]) for q in range(n)]
        t = psi0
        for sites, U, cost in gates:
            t = apply_unitary_vec(t, U, sites, dims)
            for q in range(n):
                sh = list(shape)
                sh[q] = d
                t = t * (phases[q] ** cost).reshape(sh)
                t = _sample_kraus(t, q, n, kraus_sets[cost], rng, dims)
        probs = np.abs(t.reshape(Dc, Dw)) ** 2
        successes[t_i] = probs.sum(axis=1)[good].sum()

    return {"success": float(successes.mean()),
            "stderr": float(successes.std(ddof=1) / np.sqrt(n_traj)),
            "n_traj": n_traj}


def one(job):
    d, cost, mode, sigma = job
    t0 = time.time()
    if mode.startswith("markov"):
        probs = run_markov(d, cost, mode.endswith("common"))
        r = multiplicative_order(A, N)
        m, _ = shor_config(d, N)
        succ = float(sum(probs[y] for y in range(d ** m)
                         if recovered_order(y, d ** m, A, N) == r))
        out = {"success": succ, "stderr": 0.0, "n_traj": 0}
    else:
        seed = zlib.crc32(f"ladderqs,{d},{cost},{mode}".encode())
        out = run_quasistatic(d, cost, mode.endswith("common"), sigma,
                              N_TRAJ, seed)
    out.update({"d": d, "cost": cost, "mode": mode,
                "elapsed_s": round(time.time() - t0, 1)})
    return out


def main():
    os.makedirs(RESULTS, exist_ok=True)
    sigma = sigma_matched()
    print(f"sigma = {sigma:.6f} (s = {S} matched on the d=2 uniform circuit)")

    floors = {d: uniform_floor(d, A, N) for d in BASES}
    bases = {d: float(shor_run(d, a=A, N=N)["success"]) for d in BASES}

    modes = ["markov_local", "markov_common", "qs_local", "qs_common"]
    jobs = [(d, cost, mode, sigma)
            for mode in modes for cost in COSTS for d in BASES]
    results = []
    with ProcessPoolExecutor(max_workers=5) as ex:
        for r in ex.map(one, jobs):
            d = r["d"]
            span = bases[d] - floors[d]
            r["signal"] = (r["success"] - floors[d]) / span
            r["signal_err"] = r["stderr"] / span
            results.append(r)
            err = f"±{r['signal_err']:.3f}" if r["n_traj"] else "(exact)"
            print(f"{r['mode']:13s} {r['cost']:8s} d={d} "
                  f"signal={r['signal']:6.3f} {err} ({r['elapsed_s']}s)",
                  flush=True)

    print("\n=== ladder demo cells: temporal x spatial structure ===")
    for cost in COSTS:
        for mode in modes:
            sig = {r["d"]: r["signal"] for r in results
                   if r["mode"] == mode and r["cost"] == cost}
            win = max(sig, key=sig.get)
            print(f"   {cost:8s} {mode:13s} "
                  + " ".join(f"d{d}={sig[d]:.3f}" for d in BASES)
                  + f"   winner d={win}")

    with open(os.path.join(RESULTS, "ladder_quasistatic.json"), "w") as f:
        json.dump({"N": N, "a": A, "strength": S, "sigma": sigma,
                   "n_traj": N_TRAJ, "modes": modes, "costs": COSTS,
                   "floors": floors, "baselines": bases,
                   "runs": results}, f, indent=1)
    print("wrote results/ladder_quasistatic.json")


if __name__ == "__main__":
    main()
