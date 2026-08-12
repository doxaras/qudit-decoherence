"""TRUE collective-B dephasing vs the local (per-carrier) variant.

Round-2 referee point (both Gottesman and Innsbruck): the `ion_zeeman`
channel applies the Zeeman jump independently to every carrier — LOCAL
magnetic-field noise carrying the collective-B sensitivity structure.
Genuine collective dephasing (a single field fluctuation common to the
whole string, the dominant reality in one trap) couples to the TOTAL
Zeeman shift C(x) = sum_i c_{x_i}: coherence (x, y) between product
basis states decays at rate proportional to (C(x) - C(y))^2. It has a
decoherence-free subspace (C(x) = C(y) pairs untouched) but
superdecoheres coherences spanning many carriers — and the qubit
register is the WIDEST, so the sign of the correction to the local
result is not obvious a priori.

Because the collective generator is diagonal in the product basis, one
layer of it is an elementwise mask on the density matrix:
rho_{xy} *= exp(-s * t * ((C(x)-C(y)) / (c0-c1))^2), exact for any
layer count t. Same normalization as `ion_zeeman`: the single-carrier
0<->1 pair dephases at s per layer, identical for every d.

Demo instance (N = 21, a = 2, r = 6), exact density-matrix evolution,
uniform and ion cost models, d = 2, 3, 5, same strengths as
ion_zeeman_demo.py so the two tables are directly comparable.

Writes results/collective_zeeman.json. Run: python3 collective_zeeman.py
"""

import json
import os
import time
from concurrent.futures import ProcessPoolExecutor

import numpy as np

from qudit_shor import (ZEEMAN_COEFF, apply_cost_model, apply_unitary,
                        build_shor_gates, control_probs, initial_state,
                        multiplicative_order, recovered_order, shor_config)

N, A = 21, 2
BASES = [2, 3, 5]
COSTS = ["uniform", "ion"]
STRENGTHS = [0.001, 0.003, 0.005, 0.01]

RESULTS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results")


def total_coeff(dims):
    """C(x) = sum_i c_{x_i} over all product basis states, flat order."""
    c = np.asarray(ZEEMAN_COEFF)
    C = np.zeros(1)
    for d in dims:
        C = (C[:, None] + c[:d][None, :]).reshape(-1)
    return C


def shor_run_collective(d: int, s: float, cost_model: str) -> float:
    """Success probability under collective-B dephasing at rate s/layer."""
    m, w = shor_config(d, N)
    dims = [d] * (m + w)
    gates = apply_cost_model(build_shor_gates(d, m, w, A, N), d, cost_model)
    rho = initial_state(dims, m, d, w)
    Dtot = int(np.prod(dims))

    C = total_coeff(dims)
    delta01 = abs(ZEEMAN_COEFF[0] - ZEEMAN_COEFF[1])
    rate = ((C[:, None] - C[None, :]) / delta01) ** 2  # Dtot x Dtot
    masks = {}
    if s > 0:
        for t in {c for _, _, c in gates}:
            masks[t] = np.exp(-s * t * rate)

    for sites, U, t in gates:
        rho = apply_unitary(rho, U, sites, dims)
        if masks:
            rho = (rho.reshape(Dtot, Dtot) * masks[t]).reshape(rho.shape)

    probs = control_probs(rho, d, m, w)
    D = d ** m
    r = multiplicative_order(A, N)
    return float(sum(probs[y] for y in range(D)
                     if recovered_order(y, D, A, N) == r))


def uniform_floor(d: int, r: int) -> float:
    m, _ = shor_config(d, N)
    D = d ** m
    return sum(recovered_order(y, D, A, N) == r for y in range(D)) / D


def one(args):
    d, s, cost = args
    t0 = time.time()
    succ = shor_run_collective(d, s, cost)
    return {"d": d, "strength": s, "cost": cost, "success": succ,
            "elapsed_s": round(time.time() - t0, 1)}


def main():
    os.makedirs(RESULTS, exist_ok=True)
    r = multiplicative_order(A, N)
    floors = {d: uniform_floor(d, r) for d in BASES}

    jobs = [(d, 0.0, "uniform") for d in BASES]
    jobs += [(d, s, cost) for cost in COSTS for s in STRENGTHS for d in BASES]
    with ProcessPoolExecutor(max_workers=4) as ex:
        runs = list(ex.map(one, jobs))

    base = {x["d"]: x["success"] for x in runs if x["strength"] == 0.0}
    out = {"N": N, "a": A, "r": r, "strengths": STRENGTHS, "rows": []}
    print("collective-B (common-mode) Zeeman dephasing, floor-corrected signal")
    print(f"{'cost':>8} {'s':>6} " + " ".join(f"{'d='+str(d):>8}" for d in BASES))
    for cost in COSTS:
        for s in STRENGTHS:
            sigs = []
            for d in BASES:
                succ = next(x["success"] for x in runs
                            if x["d"] == d and x["cost"] == cost
                            and x["strength"] == s)
                sig = (succ - floors[d]) / (base[d] - floors[d])
                sigs.append(sig)
                out["rows"].append({"d": d, "cost": cost, "strength": s,
                                    "success": succ, "signal": sig})
            print(f"{cost:>8} {s:>6} " + " ".join(f"{x:8.3f}" for x in sigs))

    path = os.path.join(RESULTS, "collective_zeeman.json")
    with open(path, "w") as f:
        json.dump(out, f, indent=1)
    print(f"\nwrote {path}")


if __name__ == "__main__":
    main()
