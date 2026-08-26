"""Thermal excitation and top-level leakage on the calibrated ladder.

Round-4 referee point R1-M6: the calibrated ladder's single jump
operator is downward-only and truncated at d-1, so it has no thermal
excitation (transmons run at nbar ~ 0.01-0.05) and it artificially
confines the top level of every qudit -- a d=5 transmon's |4> leaks
to |5>, but the model's cannot. Both omissions favor qudits (upward
matrix elements grow as sqrt(k)); the referee asks for the nbar at
which the d = 3 and d = 5 uniform-cost advantages vanish.

This extends every carrier to d+1 levels. Relaxation keeps the
calibrated k^0.7 ladder, now including decay from the leak level d;
thermal excitation adds an upward jump with detailed-balance rates
nbar * Gamma_(k+1 -> k), whose top rung k = d-1 -> d IS leakage out
of the encoded manifold; dephasing keeps the max-level law over all
d+1 levels (nested, so the computational block is unchanged). Gates
act as identity on the leak level. A control outcome containing any
leaked carrier is decoded as a failure. At nbar = 0 the model reduces
exactly to the paper's channel (the leak level is never populated) --
the invariance control below.

The qubit is charged the same physics: its |1> leaks to |2| at rate
nbar * 2^0.7 * s per layer, and it has the most carriers and layers.
Which register loses more per unit nbar is therefore a measurement,
not an assumption.

Unbiased instance (N = 21, a = 2, r = 6), uniform cost, s = 0.003,
quantum trajectories. Writes results/ladder_thermal.json.
Run: python3 ladder_thermal.py
"""

import json
import os
import sys
import time
import zlib
from concurrent.futures import ProcessPoolExecutor

import numpy as np
from scipy.linalg import expm

from plots import uniform_floor
from qudit_shor import (_dissipator, _mds_dephasing_jumps, apply_cost_model,
                        apply_unitary_vec, build_shor_gates, dephasing_matrix,
                        kraus_from_superop, multiplicative_order,
                        recovered_order, shor_config, shor_run)

N, A = 21, 2
BASES = [2, 3, 5]
S = 0.003
NBARS = [0.0, 0.01, 0.02, 0.05, 0.1, 0.2, 0.4]
N_TRAJ = int(sys.argv[1]) if len(sys.argv) > 1 else 1000
CHUNK = 250

RESULTS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results")


def thermal_generator(d: int, s: float, nbar: float) -> np.ndarray:
    """Lindblad generator, one time-layer, on d+1 levels: calibrated
    ladder + detailed-balance thermal up-jumps."""
    dd = d + 1
    down = np.diag(np.sqrt(np.arange(1.0, dd) ** 0.7), 1)
    L = s * _dissipator(down)
    if nbar > 0:
        up = np.diag(np.sqrt(np.arange(1.0, dd) ** 0.7), -1)
        L = L + s * nbar * _dissipator(up)
    for Ld in _mds_dephasing_jumps(dephasing_matrix(dd, s)):
        L = L + _dissipator(Ld)
    return L


def embed_gates(gates, d: int):
    """Lift a base-d gate list to d+1 levels (identity on the leak level).

    Gates act on 1 to 1+w sites (controlled modular multiplication spans
    the whole work register); the computational sub-block of the
    (d+1)-ary index space is the mixed-radix image of the d-ary indices.
    """
    dd = d + 1
    comp_cache = {}
    out = []
    for sites, U, cost in gates:
        k = len(sites)
        if k not in comp_cache:
            comp = np.zeros(d ** k, dtype=np.intp)
            for i in range(d ** k):
                digits = []
                x = i
                for _ in range(k):
                    x, dg = divmod(x, d)
                    digits.append(dg)
                y = 0
                for dg in reversed(digits):
                    y = y * dd + dg
                comp[i] = y
            comp_cache[k] = comp
        comp = comp_cache[k]
        Ue = np.eye(dd ** k, dtype=complex)
        Ue[np.ix_(comp, comp)] = U
        out.append((sites, Ue, cost))
    return out


def control_map(d: int, m: int):
    """good-outcome mask over (d+1)^m control outcomes; leaked -> False."""
    dd = d + 1
    r = multiplicative_order(A, N)
    Dc = d ** m
    mask = np.zeros(dd ** m, dtype=bool)
    for cp in range(dd ** m):
        digits = [(cp // dd ** (m - 1 - i)) % dd for i in range(m)]
        if any(g == d for g in digits):
            continue
        y = 0
        for g in digits:
            y = y * d + g
        mask[cp] = recovered_order(y, Dc, A, N) == r
    return mask


def chunk_run(args):
    d, nbar, chunk, n_traj = args
    m, w = shor_config(d, N)
    n = m + w
    dd = d + 1
    dims = [dd] * n
    gates = embed_gates(
        apply_cost_model(build_shor_gates(d, m, w, A, N), d, "uniform"), d)
    costs = {g[2] for g in gates}
    L = thermal_generator(d, S, nbar)
    kraus = {c: [(K, K.conj().T @ K) for K in kraus_from_superop(expm(c * L))]
             for c in costs}

    good = control_map(d, m)
    psi0 = np.zeros(dd ** n, complex)
    psi0[1] = 1.0
    psi0 = psi0.reshape(dims)

    seed = zlib.crc32(f"thermal,{d},{nbar},{chunk}".encode())
    rng = np.random.default_rng(seed)
    successes = np.empty(n_traj)
    t0 = time.time()
    for k in range(n_traj):
        t = psi0
        for sites, U, cost in gates:
            t = apply_unitary_vec(t, U, sites, dims)
            for q in range(n):
                t = _sample(t, q, n, kraus[cost], rng, dims)
        probs = np.abs(t.reshape(dd ** m, dd ** w)) ** 2
        successes[k] = probs.sum(axis=1)[good].sum()
    return d, nbar, chunk, successes.tolist(), round(time.time() - t0, 1)


def _sample(t, site, n, kraus, rng, dims):
    others = [ax for ax in range(n) if ax != site]
    rho_q = np.tensordot(t, t.conj(), axes=(others, others))
    probs = np.array([max(np.real(np.trace(M @ rho_q)), 0.0)
                      for _, M in kraus])
    probs /= probs.sum()
    K, _ = kraus[rng.choice(len(kraus), p=probs)]
    t = apply_unitary_vec(t, K, (site,), dims)
    return t / np.linalg.norm(t)


def main():
    os.makedirs(RESULTS, exist_ok=True)
    floors = {d: uniform_floor(d, A, N) for d in BASES}
    bases = {d: float(shor_run(d, a=A, N=N)["success"]) for d in BASES}

    n_chunks = N_TRAJ // CHUNK
    jobs = [(d, nbar, c, CHUNK)
            for d in BASES for nbar in NBARS for c in range(n_chunks)]
    acc = {}
    with ProcessPoolExecutor(max_workers=6) as ex:
        for d, nbar, chunk, succ, dt in ex.map(chunk_run, jobs):
            acc.setdefault((d, nbar), []).extend(succ)
            done = len(acc[(d, nbar)])
            if done == N_TRAJ:
                print(f"d={d} nbar={nbar:<5g} done ({dt}s/chunk)", flush=True)

    runs = []
    print(f"\n{'nbar':>6} " + " ".join(f"{'d=' + str(d):>15}" for d in BASES))
    for nbar in NBARS:
        row = []
        for d in BASES:
            s_arr = np.array(acc[(d, nbar)])
            span = bases[d] - floors[d]
            sig = (s_arr.mean() - floors[d]) / span
            err = s_arr.std(ddof=1) / np.sqrt(len(s_arr)) / span
            runs.append({"d": d, "nbar": nbar,
                         "success": float(s_arr.mean()),
                         "stderr": float(s_arr.std(ddof=1)
                                         / np.sqrt(len(s_arr))),
                         "signal": float(sig), "signal_err": float(err),
                         "n_traj": len(s_arr)})
            row.append(f"{sig:7.3f}±{err:.3f}")
        print(f"{nbar:>6g} " + " ".join(f"{c:>15}" for c in row))

    # crossing estimates: where does d's signal fall to the qubit's?
    thresholds = {}
    for d in (3, 5):
        gap = []
        for nbar in NBARS:
            sd = next(r["signal"] for r in runs
                      if r["d"] == d and r["nbar"] == nbar)
            s2 = next(r["signal"] for r in runs
                      if r["d"] == 2 and r["nbar"] == nbar)
            gap.append(sd - s2)
        gap = np.array(gap)
        x = np.array(NBARS)
        cross = None
        for i in range(len(x) - 1):
            if gap[i] > 0 >= gap[i + 1]:
                cross = float(x[i] + (x[i + 1] - x[i])
                              * gap[i] / (gap[i] - gap[i + 1]))
                break
        thresholds[f"d{d}"] = {"gaps": gap.tolist(), "nbar_cross": cross}
        print(f"d={d} vs qubit: gap {gap[0]:+.3f} at nbar=0 -> "
              f"{gap[-1]:+.3f} at nbar={NBARS[-1]}; "
              + (f"crossing at nbar ~ {cross:.3f}" if cross
                 else "no crossing in range"))

    with open(os.path.join(RESULTS, "ladder_thermal.json"), "w") as f:
        json.dump({"N": N, "a": A, "strength": S, "nbars": NBARS,
                   "cost_model": "uniform", "n_traj": N_TRAJ,
                   "floors": floors, "baselines": bases,
                   "thresholds": thresholds, "runs": runs}, f, indent=1)
    print("wrote results/ladder_thermal.json")


if __name__ == "__main__":
    main()
