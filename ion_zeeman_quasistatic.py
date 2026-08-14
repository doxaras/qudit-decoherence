"""Quasi-static (non-Markovian) Zeeman field noise, with and without echo.

Referee objection (Innsbruck-style report, M6a and minor 9): the paper
models magnetic-field noise on the 40Ca+ encoding with a Lindblad
generator, and concedes in the text that this "stands in for the
unrefocused effect of what is, in the laboratory, quasi-static noise."
That substitution is not cosmetic. Quasi-static noise

  * decays as exp[-(t/T2)^2], not exp[-t/T2] -- damage accumulates with
    the SQUARE of the circuit depth, so the Markovian stand-in
    misestimates it at every depth except the one it was matched at; and
  * is removable by refocusing pulses, which is precisely the property a
    Lindblad generator destroys.

The referee's conclusion was that no ion group operates in the regime
the paper models, because a pi-pulse removes it. This script tests that
claim rather than assuming it, by simulating the actual physics: a field
offset drawn once per shot from a Gaussian and held constant, integrated
over that Gaussian by quadrature rather than sampled (see H and M for
why the obvious quadrature rule is the wrong one here).

The refocusing algebra (see `refocus_coeffs`) is where the referee's
argument breaks. Level j carries Zeeman coefficient c_j; a refocusing
sequence that permutes levels leaves the effective coefficient
c~_j = mean over the sequence of c_{pi(j)}, and refocuses perfectly iff
c~ is constant in j. For the 40Ca+ encoding:

  * d = 2: one pi-pulse (the level swap) gives c~ = const exactly. The
    qubit is perfectly refocused, as the referee says.
  * d >= 3: NO two-interval echo refocuses, for any permutation. The
    minimum sequence length that refocuses exactly is d intervals -- and
    that minimum is over all permutation sequences, not just powers of a
    single pulse (verified by exhaustive search at d = 3 and d = 5).

So the mitigation the referee invokes is not d-independent on this
encoding: the qubit gets it for one pulse, the qudit needs d. This
script prices all three regimes -- unmitigated, single echo, and the
d-interval sequence with its pulses charged as exposure -- against the
same flat depolarizing residual the rest of the paper uses.

Normalization: sigma is fixed once, by matching the Markovian model's
0<->1 damage at rate S_ZEEMAN over the d = 2 uniform-cost circuit, and
then held FIXED across every base and cost model. One apparatus, one
field. Every cross-base difference is then a property of the circuit and
the encoding, not of a rescaled noise strength.

Demo instance (N = 21, a = 2, r = 6), exact density-matrix evolution.

Writes results/ion_zeeman_quasistatic.json.
Run: python3 ion_zeeman_quasistatic.py
"""

import itertools
import json
import os
import time
from concurrent.futures import ProcessPoolExecutor

import numpy as np

from qudit_shor import (ZEEMAN_COEFF, apply_channel, apply_cost_model,
                        apply_unitary, build_shor_gates, control_probs,
                        depolarizing_superop, initial_state, layer_count,
                        multiplicative_order, noise_superop_pow,
                        recovered_order, shor_config, shor_run)

N, A = 21, 2
BASES = [2, 3, 5]
COSTS = ["uniform", "ion"]
S_DEPOL = 0.005        # flat residual at the marked ion operating point
S_ZEEMAN = 0.003       # Markovian rate the paper's demo reversal uses

# Gaussian average over the static offset, by the trapezoid rule in units
# of sigma. NOT Gauss-Hermite: the integrand here is cos(a x) e^{-x^2/2}
# with a = sigma * (level splitting) * (circuit depth) reaching ~24 in
# the d=3 ion-cost circuit, and no practical Gauss-Hermite order
# resolves that -- 15 nodes returns 0.98 where the true value is 6e-55,
# and raising the order makes it worse before it makes it better.
# The trapezoid rule on a Gaussian is a DFT, so its error is pure
# aliasing, ~exp(-(2pi/H - a)^2/2): at H = 0.2 that is below 1e-12 for
# every a up to 24. Verified against the closed form in the header of
# the results file.
H = 0.2                # node spacing, in units of sigma
M = 35                 # nodes run from -M*H to +M*H sigma (+-7 sigma)

RESULTS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results")


# --- refocusing algebra ----------------------------------------------------

def refocus_coeffs(d: int, mode: str) -> tuple[np.ndarray, int]:
    """Effective Zeeman coefficients under a refocusing sequence.

    A sequence of level permutations pi_1..pi_L, each held for an equal
    share of the idle window and undone at the end so the computation is
    untouched, leaves level j with mean phase c~_j = (1/L) sum_l
    c_{pi_l(j)}. Returns (c~, L) with L the number of intervals, i.e. the
    number of refocusing pulses the sequence costs.

      none  L = 1, c~ = c (no pulses)
      echo  L = 2, best two-interval sequence (exhaustive over all
            permutations, minimising the worst residual pair splitting)
      dd    L = d, the cyclic shift, which refocuses exactly
    """
    c = np.asarray(ZEEMAN_COEFF[:d], dtype=float)
    if mode == "none":
        return c, 1
    if mode == "echo":
        best = min((0.5 * (c + c[list(p)]) for p in
                    itertools.permutations(range(d))),
                   key=lambda ct: float(np.max(ct) - np.min(ct)))
        return best, 2
    if mode.startswith("dd"):
        shifts = [np.roll(np.arange(d), -k) for k in range(d)]
        return np.mean([c[s] for s in shifts], axis=0), d
    raise ValueError(f"unknown refocus mode {mode!r}")


def collective_decay(cvec: np.ndarray, gamma_tau: float) -> np.ndarray:
    """Per-layer coherence decay of a COLLECTIVE Markovian field.

    One field for the whole string means one Lindblad jump operator
    J ~ diag(cvec) on the full register, and a single diagonal jump acts
    on a density matrix elementwise: rho_ab -> exp(-(J_a - J_b)^2 / 2)
    rho_ab. So the D x D decay matrix below IS the channel -- no
    superoperator is ever formed, which is what makes the collective case
    affordable at these register sizes.

    Normalised exactly as `qudit_shor.ion_zeeman_superop`: a pair of
    basis states differing in ONE carrier's 0<->1 level decays at
    gamma_tau per layer, for every d. Note the collective consequence
    that a pair differing in k carriers decays at k^2 gamma_tau rather
    than k gamma_tau -- superdecoherence, and the reason this control is
    not the paper's Sec. VII channel, which is the local (uncorrelated)
    one. Both are physically meaningful; what matters here is that the
    Markovian control and the quasi-static model share the SAME spatial
    correlation, so the only variable between them is the temporal one.
    """
    ref = abs(ZEEMAN_COEFF[0] - ZEEMAN_COEFF[1])
    diff = (cvec[:, None] - cvec[None, :]) / ref
    return np.exp(-gamma_tau * diff ** 2)


# --- quasi-static evolution ------------------------------------------------

def zeeman_weight_vector(d: int, c_eff: np.ndarray, n: int) -> np.ndarray:
    """Total Zeeman coefficient of each computational basis state.

    The field is common-mode: one offset for the whole string, so a basis
    state's phase rate is the sum of its carriers' level coefficients.
    """
    D = d ** n
    cvec = np.zeros(D)
    for q in range(n):
        cvec += c_eff[(np.arange(D) // d ** (n - 1 - q)) % d]
    return cvec


def run_quasistatic_node(d: int, cost_model: str, c_eff: np.ndarray,
                         delta: float, s_depol: float,
                         extra_layers: float) -> np.ndarray:
    """Control distribution at ONE fixed field offset (the inner integrand).

    The offset is constant within a shot, so its phases do not compose
    into a per-layer channel: they are carried through the circuit at
    fixed delta, and only the resulting distributions are averaged.

    `extra_layers` charges refocusing pulses: each pulse is one more
    single-qudit layer of depolarizing exposure per gate, which is what
    the d-interval sequence costs and a single echo nearly doesn't.
    """
    m, w = shor_config(d, N)
    n = m + w
    dims = [d] * n
    gates = apply_cost_model(build_shor_gates(d, m, w, A, N), d, cost_model)
    D = d ** n
    cvec = zeeman_weight_vector(d, c_eff, n)

    depol = {c: noise_superop_pow(d, "depolarizing", s_depol, c + extra_layers)
             for c in {g[2] for g in gates}} if s_depol > 0 else None

    rho = initial_state(dims, m, d, w)
    for sites, U, cost in gates:
        rho = apply_unitary(rho, U, sites, dims)
        if delta != 0.0:
            # rho_ab -> e^{-i delta t c_a} rho_ab e^{+i delta t c_b}: two
            # rank-1 broadcasts, never the D x D phase matrix. Rebind
            # rather than multiply in place -- after apply_unitary's
            # moveaxis the tensor is not contiguous, so reshape may hand
            # back a copy and an in-place write would be silently dropped.
            ph = np.exp(-1j * delta * cost * cvec)
            rho = ((rho.reshape(D, D) * ph[:, None])
                   * ph.conj()[None, :]).reshape(dims + dims)
        if depol is not None:
            for q in range(n):
                rho = apply_channel(rho, depol[cost], q, dims)
    return control_probs(rho, d, m, w)


def quadrature(sigma: float, flat: bool):
    """Nodes and weights of the Gaussian average over the static offset."""
    if flat or sigma == 0.0:      # exactly refocused: no field dependence
        return np.zeros(1), np.ones(1)
    x = np.arange(-M, M + 1) * H
    wt = np.exp(-x ** 2 / 2.0)
    return sigma * x, wt / wt.sum()


def run_markovian(d: int, cost_model: str, c_eff: np.ndarray, gamma: float,
                  s_depol: float, extra_layers: float) -> np.ndarray:
    """Same circuit and same collective field, but Lindblad in time.

    This is the paper's stand-in, made comparable: identical spatial
    correlation to `run_quasistatic_node`, identical exposure convention,
    identical refocused coefficient vector. The only difference left is
    that the field decorrelates instantly instead of being held fixed
    within a shot -- which is precisely the substitution under review.
    """
    m, w = shor_config(d, N)
    n = m + w
    dims = [d] * n
    gates = apply_cost_model(build_shor_gates(d, m, w, A, N), d, cost_model)
    D = d ** n
    cvec = zeeman_weight_vector(d, c_eff, n)
    flat = float(np.max(c_eff) - np.min(c_eff)) < 1e-12

    decay = {} if not flat else None
    depol = {c: noise_superop_pow(d, "depolarizing", s_depol, c + extra_layers)
             for c in {g[2] for g in gates}} if s_depol > 0 else None

    rho = initial_state(dims, m, d, w)
    for sites, U, cost in gates:
        rho = apply_unitary(rho, U, sites, dims)
        if decay is not None:
            if cost not in decay:
                decay[cost] = collective_decay(cvec, gamma * cost)
            rho = (rho.reshape(D, D) * decay[cost]).reshape(dims + dims)
        if depol is not None:
            for q in range(n):
                rho = apply_channel(rho, depol[cost], q, dims)
    return control_probs(rho, d, m, w)


# --- scoring ---------------------------------------------------------------

def uniform_floor(d: int, r: int) -> float:
    m, _ = shor_config(d, N)
    Dc = d ** m
    return sum(recovered_order(y, Dc, A, N) == r for y in range(Dc)) / Dc


def score(probs: np.ndarray, d: int, r: int) -> float:
    m, _ = shor_config(d, N)
    return float(sum(probs[y] for y in range(d ** m)
                     if recovered_order(y, d ** m, A, N) == r))


def extra_layers_for(mode: str, L: int) -> float:
    """Exposure charged for the refocusing pulses themselves.

    "dd" idealises them as free, which is the most generous reading of
    the passive-DD constructions the referee cites; "dd_charged" pays one
    extra single-qudit layer per pulse per gate, which is what the naive
    d-interval sequence actually costs.
    """
    return float(L - 1) if mode == "dd_charged" else 0.0


def one(job):
    """One quadrature node (or one whole Markovian run)."""
    d, cost, mode, channel, delta = job
    t0 = time.time()
    c_eff, L = refocus_coeffs(d, mode)
    extra = extra_layers_for(mode, L)
    if channel == "quasistatic":
        probs = run_quasistatic_node(d, cost, c_eff, delta, S_DEPOL, extra)
    else:
        probs = run_markovian(d, cost, c_eff, S_ZEEMAN, S_DEPOL, extra)
    return {"d": d, "cost": cost, "mode": mode, "channel": channel,
            "delta": delta, "success": score(probs, d, multiplicative_order(A, N)),
            "elapsed_s": round(time.time() - t0, 1)}


def main():
    os.makedirs(RESULTS, exist_ok=True)
    r = multiplicative_order(A, N)
    floors = {d: uniform_floor(d, r) for d in BASES}

    # sigma is set ONCE, on the qubit, and then never rescaled: match the
    # Markovian 0<->1 damage exp(-gamma L) over the d=2 uniform circuit
    # with the quasi-static exp(-sigma^2 (c0-c1)^2 L^2 / 2).
    m2, w2 = shor_config(2, N)
    L2 = layer_count(apply_cost_model(build_shor_gates(2, m2, w2, A, N),
                                      2, "uniform"))
    dc = abs(ZEEMAN_COEFF[0] - ZEEMAN_COEFF[1])
    sigma = float(np.sqrt(2.0 * S_ZEEMAN / (dc ** 2 * L2)))
    print(f"d=2 uniform circuit: {L2:g} layers -> sigma = {sigma:.5f} "
          f"(matched to Markovian gamma = {S_ZEEMAN})")

    print("\n--- refocusing algebra (worst pair splitting, qubit pair = 1) ---")
    algebra = {}
    for d in BASES + [7]:
        row = {}
        for mode in ("none", "echo", "dd"):
            c_eff, L = refocus_coeffs(d, mode)
            row[mode] = {"intervals": L,
                         "splitting": float(np.max(c_eff) - np.min(c_eff)) / dc}
        algebra[d] = row
        print(f"  d={d}: none {row['none']['splitting']:6.2f} | "
              f"echo(L=2) {row['echo']['splitting']:6.3f} | "
              f"dd(L={d}) {row['dd']['splitting']:.1e}")

    modes = ["none", "echo", "dd", "dd_charged"]

    # Fan out over quadrature nodes, not over cells: an exactly-refocused
    # cell collapses to a single node, so cell-level parallelism would
    # leave workers idle behind the one 71-node cell that dominates.
    cells, jobs = [], []
    for ch in ("quasistatic", "markovian"):
        for cost in COSTS:
            for mode in modes:
                for d in BASES:
                    c_eff, _ = refocus_coeffs(d, mode)
                    flat = float(np.max(c_eff) - np.min(c_eff)) < 1e-12
                    if ch == "markovian":
                        nodes, wts = np.zeros(1), np.ones(1)
                    else:
                        nodes, wts = quadrature(sigma, flat)
                    cells.append({"channel": ch, "cost": cost, "mode": mode,
                                  "d": d, "weights": wts.tolist(),
                                  "first": len(jobs), "n_nodes": len(nodes)})
                    jobs += [(d, cost, mode, ch, float(x)) for x in nodes]
    print(f"\n{len(jobs)} exact-DM runs over {len(cells)} cells "
          f"({sum(1 for c in cells if c['n_nodes'] > 1)} need quadrature)",
          flush=True)

    t0 = time.time()
    with ProcessPoolExecutor(max_workers=4) as ex:
        runs = list(ex.map(one, jobs))
    print(f"done in {time.time() - t0:.0f} s\n", flush=True)

    # combine each cell's nodes into its Gaussian-averaged success
    cell_success = {}
    for c in cells:
        span = runs[c["first"]:c["first"] + c["n_nodes"]]
        c["success"] = float(np.dot(c["weights"],
                                    [x["success"] for x in span]))
        cell_success[(c["channel"], c["cost"], c["mode"], c["d"])] = c["success"]

    # Quadrature convergence, on the record: re-integrate the single
    # worst-conditioned cell (d=3, ion cost, unmitigated -- the largest
    # sigma*splitting*depth in the grid) at half the node spacing. The
    # trapezoid rule's error here is aliasing, so halving H must move the
    # answer by nothing at all if H = 0.2 was already fine.
    global H, M
    coarse = next(c for c in cells if c["channel"] == "quasistatic"
                  and c["cost"] == "ion" and c["mode"] == "none"
                  and c["d"] == 3)
    H_fine = H / 2
    (H, M), keep = (H_fine, 2 * M), (H, M)   # halve spacing, hold +-7 sigma
    fine_nodes, fine_wts = quadrature(sigma, False)
    H, M = keep
    with ProcessPoolExecutor(max_workers=4) as ex:
        fine = list(ex.map(one, [(3, "ion", "none", "quasistatic", float(x))
                                 for x in fine_nodes]))
    fine_val = float(np.dot(fine_wts, [x["success"] for x in fine]))
    conv = {"cell": "d=3 ion none", "H": H, "H_fine": H_fine,
            "n_coarse": coarse["n_nodes"], "n_fine": len(fine_nodes),
            "coarse": coarse["success"], "fine": fine_val,
            "abs_diff": abs(coarse["success"] - fine_val)}
    print(f"quadrature convergence on {conv['cell']}: "
          f"H={H} ({conv['n_coarse']} nodes) {conv['coarse']:.9f} vs "
          f"H={H_fine} ({conv['n_fine']} nodes) {fine_val:.9f}  "
          f"|diff| = {conv['abs_diff']:.2e}\n", flush=True)

    base = {}
    for cost in COSTS:
        for d in BASES:
            base[(d, cost)] = float(shor_run(d, a=A, N=N,
                                             cost_model=cost)["success"])

    def sig(d, cost, succ):
        return (succ - floors[d]) / (base[(d, cost)] - floors[d])

    out = {"N": N, "a": A, "r": r, "sigma": sigma, "s_depol": S_DEPOL,
           "s_zeeman": S_ZEEMAN, "quad_h": H, "quad_halfwidth": M * H,
           "layers_d2_uniform": L2, "floors": floors, "algebra": algebra,
           "convergence": conv, "cells": cells, "verdicts": []}

    for ch in ("quasistatic", "markovian"):
        print(f"=== {ch} field noise + depolarizing residual "
              f"s={S_DEPOL} (floor-corrected signal) ===")
        for cost in COSTS:
            print(f"{cost:>11} " + "".join(f"{'d='+str(d):>9}" for d in BASES))
            for mode in modes:
                row = {d: sig(d, cost, cell_success[(ch, cost, mode, d)])
                       for d in BASES}
                best = max((d for d in BASES if d != 2), key=lambda d: row[d])
                verdict = "qudit" if row[best] > row[2] else "QUBIT"
                out["verdicts"].append({"channel": ch, "cost": cost,
                                        "mode": mode,
                                        "signals": {str(d): row[d] for d in BASES},
                                        "verdict": verdict, "best_qudit": best})
                print(f"{mode:>11} " + "".join(f"{row[d]:9.3f}" for d in BASES)
                      + f"   -> {verdict} ({'d='+str(best)})")
            print()

    path = os.path.join(RESULTS, "ion_zeeman_quasistatic.json")
    with open(path, "w") as f:
        json.dump(out, f, indent=1)
    print(f"wrote {path}")


if __name__ == "__main__":
    main()
