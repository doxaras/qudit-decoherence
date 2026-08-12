"""Generic quantum phase estimation on qudit registers, beyond Shor.

Shor's order finding is one member of the phase-estimation family; the
same circuit skeleton (superposed control register -> controlled powers of
a unitary -> inverse QFT) underlies quantum chemistry energy estimation,
HHL, amplitude estimation, and discrete logs. This module swaps the
modular multipliers for controlled powers of an *arbitrary* unitary U on a
16-dimensional "molecule" and reruns the qubit/qutrit/ququint decoherence
comparison, to test whether the scaling conclusions are Shor-specific.

Setup
-----
* U acts on a SYSTEM_DIM = 16 space, built from a random (seeded)
  eigenbasis with random eigenphases; the target eigenphase is pinned to
  the golden-ratio conjugate phi* = 0.6180339887, which is far from every
  fraction with a small base-2/3/5 denominator, so no base is accidentally
  favored by the phase being exactly representable.
* The work register embeds the 16 states into w qudits (d^w >= 16:
  4 qubits / 3 qutrits / 2 ququints), identity on leakage states, exactly
  mirroring the Shor experiment.
* The work register starts in the target eigenvector; the control register
  estimates phi.

Success metric: the measured y gives phi_hat = y / d^m; success is
|phi_hat - phi*| <= 2^-(BITS+1) (mod 1), i.e. phi correct to BITS bits.
The random floor is ~2^-BITS, identical for every base up to
discretization -- cleaner than Shor's continued-fraction floor.
"""

from __future__ import annotations

import numpy as np

from qudit_shor import (apply_unitary_vec, build_qft_gates, control_probs,
                        fourier, run_circuit)
from trajectories import run_success

SYSTEM_DIM = 16
PHI_TARGET = 0.6180339887498949  # golden-ratio conjugate
BITS = 5                          # success = phi estimated to 5 bits


def make_system(seed: int = 42):
    """Random unitary on SYSTEM_DIM states with the target eigenphase pinned.

    Returns (eigenvectors V, eigenphases phis in [0,1)); U = V diag(e^{2 pi i
    phis}) V^dag. phis[0] = PHI_TARGET; the work register starts in V[:, 0].
    """
    rng = np.random.default_rng(seed)
    A = rng.normal(size=(SYSTEM_DIM, SYSTEM_DIM)) \
        + 1j * rng.normal(size=(SYSTEM_DIM, SYSTEM_DIM))
    V = np.linalg.qr(A)[0]            # Haar-ish random eigenbasis
    phis = rng.uniform(size=SYSTEM_DIM)
    phis[0] = PHI_TARGET
    return V, phis


def u_power_embedded(V: np.ndarray, phis: np.ndarray, k: int,
                     Dw: int) -> np.ndarray:
    """U^k on the system, embedded in the Dw-dim work space (identity on
    leakage states)."""
    Uk = (V * np.exp(2j * np.pi * k * phis)) @ V.conj().T
    out = np.eye(Dw, dtype=complex)
    out[:SYSTEM_DIM, :SYSTEM_DIM] = Uk
    return out


def cu_gate(d: int, w: int, V: np.ndarray, phis: np.ndarray,
            base_power: int) -> np.ndarray:
    """Controlled-U^(c * base_power): block diagonal over control digit c."""
    Dw = d ** w
    U = np.zeros((d * Dw, d * Dw), complex)
    for c in range(d):
        U[c * Dw:(c + 1) * Dw, c * Dw:(c + 1) * Dw] = \
            u_power_embedded(V, phis, c * base_power, Dw)
    return U


def qpe_config(d: int):
    """Work qudits for the 16-dim system (control size m is free)."""
    w = 1
    while d ** w < SYSTEM_DIM:
        w += 1
    return w


def build_qpe_gates(d: int, m: int, w: int, V: np.ndarray,
                    phis: np.ndarray):
    """Same skeleton and cost model as build_shor_gates: control qudit i is
    wired to power d**i (little-endian), inverse QFT is the reversed-dagger
    no-swap circuit, controlled-U costs w time-layers."""
    gates = []
    for i in range(m):
        gates.append(((i,), fourier(d), 1))
    for i in range(m):
        sites = (i,) + tuple(range(m, m + w))
        gates.append((sites, cu_gate(d, w, V, phis, d ** i), w))
    for sites, U, cost in reversed(build_qft_gates(d, m)):
        gates.append((sites, U.conj().T, cost))
    return gates


def good_phase_mask(D: int, phi: float = PHI_TARGET,
                    bits: int = BITS) -> np.ndarray:
    """Outcomes y whose phase estimate y/D is within 2^-(bits+1) of phi."""
    y = np.arange(D)
    dist = np.abs(y / D - phi)
    dist = np.minimum(dist, 1 - dist)
    return dist <= 2.0 ** -(bits + 1)


def _prepare(d: int, m: int, seed: int, cost_model: str = "uniform"):
    from qudit_shor import apply_cost_model
    w = qpe_config(d)
    dims = [d] * (m + w)
    V, phis = make_system(seed)
    gates = apply_cost_model(build_qpe_gates(d, m, w, V, phis), d, cost_model)
    Dc, Dw = d ** m, d ** w
    psi0 = np.zeros((Dc, Dw), complex)
    psi0[0, :SYSTEM_DIM] = V[:, 0]   # control |0..0>, work = eigenvector
    return dims, gates, Dc, Dw, psi0.reshape(dims), good_phase_mask(Dc)


def qpe_run_exact(d: int, m: int, noise_model: str | None = None,
                  strength: float = 0.0, seed: int = 42,
                  dephase_ratio: float = 1.0,
                  cost_model: str = "uniform",
                  readout_eps: float = 0.0, **noise_kw) -> dict:
    """Exact density-matrix QPE run (small registers only)."""
    from qudit_shor import channels_by_cost
    dims, gates, Dc, Dw, psi0, good = _prepare(d, m, seed, cost_model)
    rho = np.einsum("i,j->ij", psi0.reshape(-1),
                    psi0.reshape(-1).conj()).reshape(dims + dims)
    E = None
    if noise_model and strength > 0:
        E = channels_by_cost(d, gates, noise_model, strength, dephase_ratio,
                             **noise_kw)
    rho = run_circuit(dims, gates, rho, E)
    w = len(dims) - m
    probs = control_probs(rho, d, m, w)
    if readout_eps > 0:
        from qudit_shor import apply_readout, readout_confusion
        probs = apply_readout(probs, d, m, readout_confusion(d, readout_eps))
    return {"d": d, "m": m, "success": float(probs[good].sum()),
            "floor": float(good.mean()), "probs": probs}


# --- Interpolating between eigenstate QPE and Shor -------------------------
# Shor's work register starts in |x=1>, which is an equal superposition of the
# r eigenstates of the modular multiplier -- so Shor IS phase estimation on an
# r-fold eigenstate superposition (r = 4 for a = 7, N = 15). Eigenstate QPE
# (K = 1) leaves the control and work registers in a product state; a K-fold
# superposition entangles them, and the work register then carries which-path
# information about the control. Sweeping K interpolates continuously between
# the two algorithms with everything else held fixed, so it isolates the
# mechanism responsible for their opposite orderings under ladder noise.
#
# Target phases are chosen mutually well separated (offsets 0.23/0.47/0.71
# from the golden-ratio conjugate) so their success windows never overlap and
# none sits near a nice fraction of any base.

SUPERPOSITION_OFFSETS = [0.0, 0.23, 0.47, 0.71]


def make_system_multi(seed: int = 42, n_targets: int = 4):
    """Random unitary with `n_targets` well-separated pinned eigenphases."""
    V, phis = make_system(seed)
    for j in range(n_targets):
        phis[j] = (PHI_TARGET + SUPERPOSITION_OFFSETS[j]) % 1.0
    return V, phis


def good_phase_mask_multi(D: int, phases, bits: int = BITS) -> np.ndarray:
    """Outcomes within 2^-(bits+1) of ANY of the target phases."""
    y = np.arange(D)
    mask = np.zeros(D, bool)
    for phi in phases:
        dist = np.abs(y / D - phi)
        mask |= np.minimum(dist, 1 - dist) <= 2.0 ** -(bits + 1)
    return mask


def _prepare_multi(d: int, m: int, K: int, seed: int,
                   cost_model: str = "uniform"):
    from qudit_shor import apply_cost_model
    w = qpe_config(d)
    dims = [d] * (m + w)
    V, phis = make_system_multi(seed, n_targets=len(SUPERPOSITION_OFFSETS))
    gates = apply_cost_model(build_qpe_gates(d, m, w, V, phis), d, cost_model)
    Dc, Dw = d ** m, d ** w
    psi0 = np.zeros((Dc, Dw), complex)
    psi0[0, :SYSTEM_DIM] = V[:, :K].sum(axis=1) / np.sqrt(K)
    good = good_phase_mask_multi(Dc, [phis[j] for j in range(K)])
    return dims, gates, Dc, Dw, psi0.reshape(dims), good


def control_work_entropy(d: int, m: int, K: int, seed: int = 42) -> float:
    """Entanglement entropy (bits) of the control:work cut after the
    controlled-U stage, noiseless. Equals log2(K) for K equally weighted
    eigenstates once the phase branches are resolved by the control."""
    dims, gates, Dc, Dw, psi0, _ = _prepare_multi(d, m, K, seed)
    t = psi0
    # apply everything up to (but excluding) the inverse QFT
    n_pre = m + m
    for sites, U, _ in gates[:n_pre]:
        t = apply_unitary_vec(t, U, sites, dims)
    psi = t.reshape(Dc, Dw)
    s = np.linalg.svd(psi, compute_uv=False)
    p = s ** 2
    p = p[p > 1e-14]
    return float(-(p * np.log2(p)).sum())


def qpe_superposition_trajectories(d: int, m: int, K: int,
                                   noise_model: str | None = None,
                                   strength: float = 0.0, n_traj: int = 400,
                                   seed: int = 0, system_seed: int = 42,
                                   dephase_ratio: float = 1.0,
                                   cost_model: str = "uniform") -> dict:
    """QPE on a K-fold eigenstate superposition (K=1 eigenstate ... K=4 Shor-like)."""
    from trajectories import run_success
    dims, gates, Dc, Dw, psi0, good = _prepare_multi(d, m, K, system_seed,
                                                     cost_model)
    out = run_success(dims, d, gates, psi0, Dc, Dw, good, noise_model,
                      strength, n_traj, seed, dephase_ratio)
    out.update({
        "d": d, "m": m, "K": K, "w": len(dims) - m, "D": Dc,
        "n_qudits": len(dims), "n_gates": len(gates),
        "n_layers": sum(c for _, _, c in gates),
        "noise_model": noise_model, "strength": strength,
        "cost_model": cost_model, "floor": float(good.mean()),
    })
    return out


def qpe_trajectories(d: int, m: int, noise_model: str | None = None,
                     strength: float = 0.0, n_traj: int = 400,
                     seed: int = 0, system_seed: int = 42,
                     dephase_ratio: float = 1.0,
                     cost_model: str = "uniform",
                     readout_eps: float = 0.0) -> dict:
    """Monte Carlo QPE run, same interface as shor_trajectories."""
    dims, gates, Dc, Dw, psi0, good = _prepare(d, m, system_seed, cost_model)
    out = run_success(dims, d, gates, psi0, Dc, Dw, good, noise_model,
                      strength, n_traj, seed, dephase_ratio, readout_eps, m)
    out.update({
        "d": d, "m": m, "w": len(dims) - m, "D": Dc,
        "n_qudits": len(dims),
        "n_gates": len(gates),
        "n_layers": sum(c for _, _, c in gates),
        "noise_model": noise_model,
        "strength": strength,
        "cost_model": cost_model,
        "floor": float(good.mean()),
    })
    return out
