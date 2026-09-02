"""Quantum-trajectory (Monte Carlo wavefunction) simulation of qudit Shor.

The exact density-matrix simulator in qudit_shor.py is limited to ~3000
Hilbert dimensions by memory (rho is dim^2 complex numbers). This engine
propagates pure states and samples the noise stochastically, which costs
dim numbers per trajectory and lets us scale the control register far
enough to study how the qubit/qutrit/ququint comparison changes with
problem size.

Unravelling: after every gate, each qudit independently passes through the
per-layer channel E^cost. For each qudit we draw one Kraus operator K_i of
that channel with probability p_i = Tr(K_i^dag K_i rho_q) (rho_q = the
qudit's reduced density matrix, cheap to extract from the state tensor),
apply it, and renormalize. Averaging |psi><psi| over trajectories
reproduces the exact channel; success probabilities converge with
statistical error ~ 1/sqrt(n_traj) (each trajectory contributes its full
outcome distribution, not a single sampled outcome, so the variance is
well below Bernoulli).
"""

from __future__ import annotations

import numpy as np

from qudit_shor import (
    apply_cost_model, apply_readout, apply_unitary_vec, build_shor_gates,
    kraus_from_superop, multiplicative_order, noise_superop_pow,
    readout_confusion, recovered_order, shor_config,
)


def _kraus_sets(d: int, noise_model: str, strength: float,
                costs: set[int], dephase_ratio: float = 1.0, **noise_kw):
    """For each gate cost c, the Kraus ops (and K^dag K) of E^c."""
    sets = {}
    for c in costs:
        Ec = noise_superop_pow(d, noise_model, strength, c, dephase_ratio,
                               **noise_kw)
        kraus = [(K, K.conj().T @ K) for K in kraus_from_superop(Ec)]
        # Guard: the eigenvalue cut in kraus_from_superop must not have
        # truncated the channel -- sum K^dag K = I, or sampling is biased.
        comp = sum(KdK for _, KdK in kraus)
        defect = float(np.abs(comp - np.eye(d)).max())
        if defect > 1e-8:
            raise RuntimeError(
                f"Kraus completeness violated ({defect:.1e}) for "
                f"{noise_model} d={d} s={strength} cost={c}")
        sets[c] = kraus
    return sets


def _reduced_dm(t: np.ndarray, site: int, n: int) -> np.ndarray:
    others = [ax for ax in range(n) if ax != site]
    return np.tensordot(t, t.conj(), axes=(others, others))


def _sample_kraus(t: np.ndarray, site: int, n: int, kraus, rng,
                  dims: list[int]) -> np.ndarray:
    rho_q = _reduced_dm(t, site, n)
    probs = np.array([max(np.real(np.trace(M @ rho_q)), 0.0)
                      for _, M in kraus])
    probs /= probs.sum()
    i = rng.choice(len(kraus), p=probs)
    K, _ = kraus[i]
    t = apply_unitary_vec(t, K, (site,), dims)  # not unitary; renormalize
    return t / np.linalg.norm(t)


def good_outcome_mask(d: int, m: int, a: int, N: int) -> np.ndarray:
    D = d ** m
    r_true = multiplicative_order(a, N)
    return np.array([recovered_order(y, D, a, N) == r_true
                     for y in range(D)])


def run_success(dims: list[int], d: int, gates, psi0: np.ndarray,
                Dc: int, Dw: int, good: np.ndarray,
                noise_model: str | None = None, strength: float = 0.0,
                n_traj: int = 400, seed: int = 0,
                dephase_ratio: float = 1.0, readout_eps: float = 0.0,
                m: int | None = None, **noise_kw) -> dict:
    """Generic trajectory driver: run any gate list from psi0 and score the
    probability of landing in the `good` set of control-register outcomes.

    With noise_model=None runs a single deterministic pure-state simulation
    (exact). Returns mean success, standard error, and trajectory count.
    """
    n = len(dims)
    kraus_sets = None
    if noise_model and strength > 0:
        costs = {cost for _, _, cost in gates}
        kraus_sets = _kraus_sets(d, noise_model, strength, costs,
                                 dephase_ratio, **noise_kw)

    C = None
    if readout_eps > 0:
        if m is None:
            raise ValueError("readout_eps needs the control width m")
        C = readout_confusion(d, readout_eps)

    rng = np.random.default_rng(seed)
    runs = 1 if kraus_sets is None else n_traj
    successes = np.empty(runs)
    for k in range(runs):
        t = psi0
        for sites, U, cost in gates:
            t = apply_unitary_vec(t, U, sites, dims)
            if kraus_sets is not None:
                for q in range(n):
                    t = _sample_kraus(t, q, n, kraus_sets[cost], rng, dims)
        probs = np.abs(t.reshape(Dc, Dw)) ** 2
        y = probs.sum(axis=1)
        if C is not None:
            y = apply_readout(y, d, m, C)
        successes[k] = y[good].sum()

    mean = float(successes.mean())
    stderr = float(successes.std(ddof=1) / np.sqrt(runs)) if runs > 1 else 0.0
    return {"success": mean, "stderr": stderr, "n_traj": runs}


def shor_trajectories(d: int, m: int, noise_model: str | None = None,
                      strength: float = 0.0, n_traj: int = 400,
                      seed: int = 0, a: int = 7, N: int = 15,
                      dephase_ratio: float = 1.0,
                      cost_model: str = "uniform",
                      readout_eps: float = 0.0, **noise_kw) -> dict:
    """Monte Carlo estimate of Shor success probability at register size m."""
    _, w = shor_config(d, N)
    dims = [d] * (m + w)
    gates = apply_cost_model(build_shor_gates(d, m, w, a, N), d, cost_model)
    Dc, Dw = d ** m, d ** w
    good = good_outcome_mask(d, m, a, N)

    psi0 = np.zeros(Dc * Dw, complex)
    psi0[1] = 1.0  # control = |0...0>, work = |x=1>
    psi0 = psi0.reshape(dims)

    out = run_success(dims, d, gates, psi0, Dc, Dw, good, noise_model,
                      strength, n_traj, seed, dephase_ratio, readout_eps, m,
                      **noise_kw)
    out.update({
        "d": d, "m": m, "w": w, "D": Dc,
        "n_qudits": len(dims),
        "n_gates": len(gates),
        "n_layers": sum(c for _, _, c in gates),
        "noise_model": noise_model,
        "strength": strength,
        "cost_model": cost_model,
        "floor": float(good.mean()),
    })
    return out
