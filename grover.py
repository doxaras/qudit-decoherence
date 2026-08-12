"""Grover search on qudit registers -- a falsification test of our mechanism.

Why this algorithm specifically. Our claim is that the qudit advantage comes
from compressing *width and depth* at matched problem size under a
per-carrier noise budget. In Shor and eigenstate QPE those two compress
together -- a base-5 register has both fewer carriers and a shorter
schedule -- so those experiments cannot say which one does the work.

Grover separates them. The iteration count is (pi/4) sqrt(M) regardless of
base, so the number of oracle calls is *base-independent* while the width
still shrinks as log_d M. Prediction registered before running: qudits win,
by less than in QPE. A null result would mean our effect was depth all
along and the "fewer carriers" half of the story is wrong.

Two further properties make it a clean control:

  * Grid alignment cannot exist here. There is no target phase, no order,
    no continued fractions -- the confound that overturned our Shor result
    (docs/GRID_ALIGNMENT.md) is structurally absent, and the random floor
    is exactly 1/M instead of the ~28% continued fractions hands out.
  * It is amplitude-critical rather than phase-critical, so it probes a
    different failure mode under decoherence.

Structure of one iteration, base d, n qudits, search space M = d^n:

    oracle      diag(1,...,-1,...,1)          phase flip on the marked item
    diffuser    F^{ox n} (2|0><0| - I) F^{-ox n}

Cost accounting. The oracle and the |0><0| reflection are diagonal
operations on all n qudits at once. Applying them as a single dense
unitary is exact, but charging them one time-layer would hand a free ride
to whichever base packs more carriers into that one gate -- precisely the
base with the *most* qudits, i.e. d = 2. Both are therefore charged
(n - 1) layers, the two-qudit-gate count of the standard multi-controlled
decomposition, while still being applied exactly. Our gate list carries
(sites, U, cost) as separate fields, so this is honest rather than a
fudge: the unitary is exact and the noise exposure is that of the
decomposition.

A marked item on high levels decays faster than one on |0...0> under
ladder noise, which is a real d-dependent effect, so every measurement
averages over a sample of marked items rather than fixing one.

Run: python3 grover.py   (self-check)
"""

from __future__ import annotations

import numpy as np

from qudit_shor import (apply_channel, apply_unitary, apply_unitary_vec,
                        apply_cost_model, channels_by_cost, fourier)


def optimal_iterations(M: int) -> int:
    """The standard (pi/4) sqrt(M) rounded to the nearest integer."""
    return max(1, int(round(np.pi / 4.0 * np.sqrt(M))))


def grover_gates(d: int, n: int, marked: int, iterations: int):
    """Gate list for Grover search over M = d^n items.

    Returns (sites, U, cost) triples in the same convention as
    build_shor_gates: `cost` is the number of time-layers the gate occupies,
    and every qudit idles through that many layers of noise.
    """
    M = d ** n
    sites = tuple(range(n))
    F = fourier(d)

    oracle = np.eye(M, dtype=complex)
    oracle[marked, marked] = -1.0

    reflect0 = -np.eye(M, dtype=complex)      # 2|0><0| - I
    reflect0[0, 0] = 1.0

    multi_cost = float(max(n - 1, 1))         # decomposition depth

    gates = [((q,), F, 1.0) for q in range(n)]          # uniform superposition
    for _ in range(iterations):
        gates.append((sites, oracle, multi_cost))
        gates += [((q,), F.conj().T, 1.0) for q in range(n)]
        gates.append((sites, reflect0, multi_cost))
        gates += [((q,), F, 1.0) for q in range(n)]
    return gates


def _marked_sample(M: int, n_marked: int, seed: int) -> list[int]:
    """A reproducible sample of marked items, never the all-zero state.

    |0...0> is the diffuser's own reflection axis and sits at the bottom of
    the damping ladder, so it is the least representative item there is.
    """
    rng = np.random.default_rng(seed)
    pool = np.arange(1, M)
    if n_marked >= len(pool):
        return pool.tolist()
    return sorted(rng.choice(pool, size=n_marked, replace=False).tolist())


def grover_run(d: int, n: int, noise_model: str | None = None,
               strength: float = 0.0, iterations: int | None = None,
               n_marked: int = 8, seed: int = 7,
               dephase_ratio: float = 1.0, cost_model: str = "uniform",
               readout_eps: float = 0.0, **noise_kw) -> dict:
    """Exact density-matrix Grover, averaged over a sample of marked items."""
    M = d ** n
    T = optimal_iterations(M) if iterations is None else iterations
    dims = [d] * n

    successes, layers = [], None
    for marked in _marked_sample(M, n_marked, seed):
        gates = apply_cost_model(grover_gates(d, n, marked, T), d, cost_model)
        layers = sum(c for _, _, c in gates)
        E = None
        if noise_model and strength > 0:
            E = channels_by_cost(d, gates, noise_model, strength,
                                 dephase_ratio, **noise_kw)

        rho = np.zeros((M, M), complex)
        rho[0, 0] = 1.0
        rho = rho.reshape(dims + dims)
        for sites, U, cost in gates:
            rho = apply_unitary(rho, U, sites, dims)
            if E is not None:
                for q in range(n):
                    rho = apply_channel(rho, E[cost], q, dims)

        probs = np.real(np.diag(rho.reshape(M, M)))
        if readout_eps > 0:
            from qudit_shor import apply_readout, readout_confusion
            probs = apply_readout(probs, d, n, readout_confusion(d,
                                                                 readout_eps))
        successes.append(float(probs[marked]))

    successes = np.array(successes)
    return {
        "d": d, "n": n, "M": M, "iterations": T,
        "n_qudits": n, "n_layers": layers,
        "noise_model": noise_model, "strength": strength,
        "cost_model": cost_model, "readout_eps": readout_eps,
        "success": float(successes.mean()),
        "stderr": float(successes.std(ddof=1) / np.sqrt(len(successes)))
        if len(successes) > 1 else 0.0,
        "floor": 1.0 / M,
        "n_marked": len(successes),
    }


def grover_trajectories(d: int, n: int, noise_model: str | None = None,
                        strength: float = 0.0, iterations: int | None = None,
                        n_traj: int = 400, seed: int = 0, n_marked: int = 8,
                        marked_seed: int = 7, dephase_ratio: float = 1.0,
                        cost_model: str = "uniform") -> dict:
    """Monte Carlo Grover for registers too large for a density matrix."""
    from trajectories import run_success

    M = d ** n
    T = optimal_iterations(M) if iterations is None else iterations
    dims = [d] * n

    means, errs, layers = [], [], None
    for i, marked in enumerate(_marked_sample(M, n_marked, marked_seed)):
        gates = apply_cost_model(grover_gates(d, n, marked, T), d, cost_model)
        layers = sum(c for _, _, c in gates)
        psi0 = np.zeros(M, complex)
        psi0[0] = 1.0
        good = np.zeros(M, bool)
        good[marked] = True
        out = run_success(dims, d, gates, psi0.reshape(dims), M, 1, good,
                          noise_model, strength, n_traj, seed + i,
                          dephase_ratio)
        means.append(out["success"])
        errs.append(out["stderr"])

    means = np.array(means)
    # total error: spread across marked items plus each item's own MC error
    between = means.std(ddof=1) / np.sqrt(len(means)) if len(means) > 1 else 0.0
    within = np.sqrt(np.sum(np.array(errs) ** 2)) / len(errs)
    return {
        "d": d, "n": n, "M": M, "iterations": T,
        "n_qudits": n, "n_layers": layers,
        "noise_model": noise_model, "strength": strength,
        "cost_model": cost_model,
        "success": float(means.mean()),
        "stderr": float(np.hypot(between, within)),
        "floor": 1.0 / M,
        "n_traj": n_traj, "n_marked": len(means),
    }


if __name__ == "__main__":
    print("noiseless Grover (exact), averaged over marked items:")
    for d, n in ((2, 6), (3, 4), (5, 3)):
        r = grover_run(d, n)
        print(f"  d={d} n={n} M={r['M']:4d} T={r['iterations']:2d} "
              f"layers={r['n_layers']:6.0f} floor={r['floor']:.4f} "
              f"success={r['success']:.4f}±{r['stderr']:.4f}")
