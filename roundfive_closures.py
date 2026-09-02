"""Close the four deferred round-5 referee items with committed runs.

Part A (R5-R2-M4)  pavlidis3: a d^3-scaled entangler charge. Pavlidis &
    Floratos price the modular multiply-accumulate at depth 21 d^3 q^2
    where the paper's `pavlidis` model uses the 4 d^2 q adder rows; the
    dominant Shor gate is MMAC-class. Multiplier d^3/8 (=1 at d=2), the
    d^3 analog of `pavlidis`' d^2/4. Demo Shor grid, exact rho.

Part B (R5-R1-M2)  timed ion cost: Hrmo's light-shift gate is d
    interleaved LS pulses, so its wall-clock ratio to the d=2 gate is
    d/2 before counting the d local permutations. `timed_ls` charges
    d/2 per entangling gate (the LS-only reading); the with-locals
    reading ~d is bracketed from above by `ion` (d-1, = d at large d,
    harsher than d/2 at d=3: 2 vs 1.5). Demo Shor grid, exact rho.

Part C (R5-R1-M6)  state-preparation error: mirror of the readout
    model. The initial state is computational-basis product
    (|0...0> controls, |x=1> work), so misprep is a classical confusion
    on each carrier's prepared level with the same (1+k) structure as
    readout; the circuit then runs on the mixed product state, exact
    rho. Sweep eps_prep = 0..0.04.

Part D (R5-R1-M6b)  sequential-shelving readout charge on the ion QPE
    prediction table: controls are read first, in order; the k-th
    control idles through k*(d-1) prior detection rounds, each costing
    depolarizing damage delta = t_round/T2 (3 ms / 100 ms = 0.03,
    Ringbauer shielded figures -- the same convention the Discussion
    quotes as "a few percent per idling carrier"). Applied per control
    carrier after the circuit, before scoring.

Part E (R5-R3-M4)  exponent 0.8 row: the echo-with-relaxation-
    subtraction reading of Blok's table gives max-level exponent ~0.78;
    Table VI sweeps only upward from 1.1. One row below.

Run: python3 roundfive_closures.py          (parts A-E, exact rho, ~min)
Writes results/roundfive_closures.json
"""

import json
import os
import time
from concurrent.futures import ProcessPoolExecutor

import numpy as np

from qudit_shor import (GATE_COST_MODELS, apply_channel, apply_cost_model,
                        build_shor_gates, channels_by_cost, control_probs,
                        depolarizing_superop, multiplicative_order,
                        readout_confusion, recovered_order, run_circuit,
                        shor_config, shor_run)

GATE_COST_MODELS["pavlidis3"] = (lambda d: 1.0, lambda d: d ** 3 / 8.0)
GATE_COST_MODELS["timed_ls"] = (lambda d: 1.0, lambda d: d / 2.0)

N, A = 21, 2
S = 0.005
MODELS = ["transmon_cal", "depolarizing"]
RESULTS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results")


def floor_and_base(d):
    m, w = shor_config(d, N)
    D = d ** m
    r = multiplicative_order(A, N)
    fl = sum(recovered_order(y, D, A, N) == r for y in range(D)) / D
    base = shor_run(d, a=A, N=N)["success"]
    return fl, float(base)


def shor_cell(args):
    d, model, cost, kw = args
    t0 = time.time()
    res = shor_run(d, model, S, a=A, N=N, cost_model=cost, **kw)
    return {"d": d, "model": model, "cost": cost, **kw,
            "success": float(res["success"]),
            "n_layers": res["n_layers"],
            "elapsed_s": round(time.time() - t0, 1)}


def prep_error_run(d, model, cost, eps):
    """Shor with a (1+k)-structured state-preparation confusion."""
    m, w = shor_config(d, N)
    dims = [d] * (m + w)
    gates = apply_cost_model(build_shor_gates(d, m, w, A, N), d, cost)
    C = readout_confusion(d, eps)  # C[i, j] = P(read i | true j) reused as
    # P(prepared i | intended j): same (1+k) escalation structure.
    site_diag = []
    for site in range(m + w):
        intended = 0 if site < m else (1 if site == m + w - 1 else 0)
        site_diag.append(C[:, intended])
    # product of diagonal single-site density matrices
    rho = site_diag[0]
    for p in site_diag[1:]:
        rho = np.kron(rho, p)
    Dtot = int(np.prod(dims))
    rho = np.diag(rho.astype(complex)).reshape(dims + dims)
    E = channels_by_cost(d, gates, model, S, 1.0) if S > 0 else None
    rho = run_circuit(dims, gates, rho, E)
    probs = control_probs(rho, d, m, w)
    D = d ** m
    r = multiplicative_order(A, N)
    succ = sum(probs[y] for y in range(D)
               if recovered_order(y, D, A, N) == r)
    return float(succ)


def part_ABE():
    print("== Parts A/B (cost models) and E (exponent 0.8), exact rho ==",
          flush=True)
    fb = {d: floor_and_base(d) for d in (2, 3, 5)}
    jobs = []
    for cost in ("pavlidis3", "timed_ls"):
        for model in MODELS:
            for d in (3, 5):
                jobs.append((d, model, cost, {}))
    for cost in ("uniform", "ion", "pavlidis"):
        for d in (2, 3, 5):
            jobs.append((d, "transmon_cal", cost,
                         {"damping_exponent": 0.7, "dephase_exponent": 0.8}))
    out = []
    with ProcessPoolExecutor(max_workers=6) as ex:
        for c in ex.map(shor_cell, jobs):
            d = c["d"]
            fl, base = fb[d]
            c["signal"] = (c["success"] - fl) / (base - fl)
            out.append(c)
            tag = "exp0.8" if "dephase_exponent" in c else c["cost"]
            print(f"  d={d} {c['model']:13s} {tag:10s} "
                  f"signal={c['signal']:.3f} layers={c['n_layers']:.1f} "
                  f"({c['elapsed_s']}s)", flush=True)
    return {"floors_bases": {str(d): fb[d] for d in fb}, "cells": out}


def part_C():
    print("== Part C: state-preparation error sweep, exact rho ==",
          flush=True)
    fb = {d: floor_and_base(d) for d in (2, 3, 5)}
    out = []
    for eps in (0.0, 0.01, 0.02, 0.04):
        for cost in ("uniform", "ion"):
            for model in MODELS:
                row = {"eps_prep": eps, "cost": cost, "model": model}
                for d in (2, 3, 5):
                    t0 = time.time()
                    s = prep_error_run(d, model, cost, eps)
                    fl, base = fb[d]
                    row[f"signal_d{d}"] = (s - fl) / (base - fl)
                out.append(row)
                print(f"  eps={eps:<5g} {cost:8s} {model:13s} "
                      f"{row['signal_d2']:.3f}/{row['signal_d3']:.3f}/"
                      f"{row['signal_d5']:.3f}", flush=True)
    return out


def part_D():
    print("== Part D: shelving-readout charge on the QPE prediction "
          "pairs ==", flush=True)
    from qpe_generic import PHI_TARGET, _prepare, good_phase_mask
    DELTA = 0.03  # per detection round: 3 ms at 100 ms shielded coherence
    PAIRS = [(4, [(5, 2), (2, 5)]), (5, [(5, 3), (2, 7)]),
             (6, [(5, 4), (2, 9)])]
    STR = [0.001, 0.005]
    out = []
    for bits, regs in PAIRS:
        for d, m in regs:
            if d ** (m + 1) > 4 * 10 ** 6:
                continue
            for s in STR:
                t0 = time.time()
                dims, gates, Dc, Dw, psi0, _ = _prepare(d, m, 42, "ion")
                good = good_phase_mask(Dc, PHI_TARGET, bits)
                rho = np.einsum("i,j->ij", psi0.reshape(-1),
                                psi0.reshape(-1).conj()).reshape(dims + dims)
                E = channels_by_cost(d, gates, "depolarizing", s, 1.0)
                rho = run_circuit(dims, gates, rho, E)
                w = len(dims) - m
                probs0 = control_probs(rho, d, m, w)
                # controls read first, in order; control k waits k*(d-1)
                # rounds, each depositing DELTA of depolarizing damage
                for k in range(m):
                    rounds = k * (d - 1)
                    if rounds == 0:
                        continue
                    p_eff = 1.0 - (1.0 - DELTA) ** rounds
                    rho = apply_channel(rho, depolarizing_superop(d, p_eff),
                                        k, dims)
                probs1 = control_probs(rho, d, m, w)
                out.append({"bits": bits, "d": d, "m": m, "s": s,
                            "success_uncharged": float(probs0[good].sum()),
                            "success_charged": float(probs1[good].sum()),
                            "floor": float(good.mean()),
                            "elapsed_s": round(time.time() - t0, 1)})
                r = out[-1]
                print(f"  b={bits} d={d} m={m} s={s:<6g} "
                      f"{r['success_uncharged']:.3f} -> "
                      f"{r['success_charged']:.3f}  ({r['elapsed_s']}s)",
                      flush=True)
    return {"delta_per_round": DELTA, "cells": out}


def main():
    os.makedirs(RESULTS, exist_ok=True)
    data = {"N": N, "a": A, "strength": S,
            "AB_E": part_ABE(), "C_prep": part_C(), "D_readout": part_D()}
    path = os.path.join(RESULTS, "roundfive_closures.json")
    with open(path, "w") as f:
        json.dump(data, f, indent=1)
    print(f"wrote {path}", flush=True)


if __name__ == "__main__":
    main()
