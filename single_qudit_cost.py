"""Charging single-qudit gates a d-dependent cost, and bounding the bias.

Referee objection (Innsbruck-style report, M2b and minor 2): under both
`uniform` and `ion` a single-qudit gate costs one layer regardless of d.
Ringbauer's randomized benchmarking -- the measurement the paper quotes
approvingly -- gives an average per-CLIFFORD error of 2(2)e-3 at d = 3
and 1.0(2)e-2 at d = 5, a 5x rise, because a d = 5 Clifford takes ~3x
more laser pulses. Per pulse the error is flat in d; per operation it is
not, and circuits are built from operations. The referee's demand was
explicit: either charge single-qudit gates a measured d-dependent cost,
or state that the models omit it and bound the resulting bias.

This is the charge, and the bound. The objection has more teeth than the
referee spelled out, because the exposure share of single-qudit gates
GROWS with d in this circuit family: the order-finding circuit spends 2m
of its gates on single-qudit Fourier rotations (m in the state
preparation, m in the inverse QFT) out of 2m + m*w + m(m-1)/2 layers,
which is 21% at d = 2, 31% at d = 3 and 40% at d = 5. So a d-dependent
single-qudit charge hits the qudit twice -- each rotation costs more and
there are proportionally more of them.

Parameterisation. The single-qudit layer cost is taken as
mu_1(d) = (d/2)^alpha, normalised to 1 at d = 2 like every other cost in
the paper, and alpha is swept. What the measurement actually pins is the
d = 3 : d = 5 ratio, not the absolute scale:

  alpha = 0     the paper's present convention (no charge)
  alpha = 2.15  reproduces the measured ~3x pulse-count ratio, (5/3)^a = 3
  alpha = 3.15  reproduces the measured 5x per-Clifford error ratio

Both calibrated values are extrapolated down to d = 2, which Ringbauer's
qudit benchmarking does not measure; that extrapolation is the reason
this is reported as a sweep with a critical alpha per cell rather than as
one more row of the cost table.

Grid: both channels x three cost models x d = 2, 3, 5 at the tabulated
s = 0.005, exact density matrices, demo instance (N = 21, a = 2, r = 6).

Writes results/single_qudit_cost.json. Run: python3 single_qudit_cost.py
"""

import json
import os
import time
from concurrent.futures import ProcessPoolExecutor

import numpy as np

from qudit_shor import (apply_channel, apply_cost_model, apply_unitary,
                        build_shor_gates, control_probs, initial_state,
                        layer_count, multiplicative_order, noise_superop_pow,
                        recovered_order, shor_config, shor_run)

N, A = 21, 2
BASES = [2, 3, 5]
COSTS = ["uniform", "ion", "pavlidis"]
MODELS = ["depolarizing", "transmon_cal"]
S = 0.005

# (5/3)^2.15 = 3.0 (measured pulse-count ratio)
# (5/3)^3.15 = 5.0 (measured per-Clifford error ratio)
ALPHAS = [0.0, 0.5, 1.0, 1.5, 2.0, 2.15, 2.5, 3.0, 3.15, 3.5, 4.0]
CALIBRATED = {2.15: "pulse-count ratio (~3x, d=5 vs d=3)",
              3.15: "per-Clifford error ratio (5x, d=5 vs d=3)"}

RESULTS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results")


def charge_1q(gates, d: int, alpha: float):
    """Multiply every single-qudit gate's layer cost by (d/2)^alpha.

    Applied on top of the chosen cost model, which already fixed the
    two-qudit charge; normalised to 1 at d = 2 like every other cost
    multiplier in the paper.
    """
    mu = (d / 2.0) ** alpha
    return [(sites, U, cost * mu if len(sites) == 1 else cost)
            for sites, U, cost in gates]


def build(d: int, cost_model: str, alpha: float):
    m, w = shor_config(d, N)
    gates = charge_1q(apply_cost_model(build_shor_gates(d, m, w, A, N),
                                       d, cost_model), d, alpha)
    return m, w, gates


def run(d: int, model: str | None, strength: float, cost_model: str,
        alpha: float):
    m, w, gates = build(d, cost_model, alpha)
    n = m + w
    dims = [d] * n
    chans = ({c: noise_superop_pow(d, model, strength, c)
              for c in {g[2] for g in gates}}
             if model and strength > 0 else None)
    rho = initial_state(dims, m, d, w)
    for sites, U, cost in gates:
        rho = apply_unitary(rho, U, sites, dims)
        if chans is not None:
            for q in range(n):
                rho = apply_channel(rho, chans[cost], q, dims)
    return control_probs(rho, d, m, w)


def uniform_floor(d: int, r: int) -> float:
    m, _ = shor_config(d, N)
    Dc = d ** m
    return sum(recovered_order(y, Dc, A, N) == r for y in range(Dc)) / Dc


def score(probs, d: int, r: int) -> float:
    m, _ = shor_config(d, N)
    return float(sum(probs[y] for y in range(d ** m)
                     if recovered_order(y, d ** m, A, N) == r))


def one(job):
    d, model, cost, alpha = job
    t0 = time.time()
    probs = run(d, model, S, cost, alpha)
    _, _, gates = build(d, cost, alpha)
    return {"d": d, "model": model, "cost": cost, "alpha": alpha,
            "layers": layer_count(gates),
            "success": score(probs, d, multiplicative_order(A, N)),
            "elapsed_s": round(time.time() - t0, 1)}


def share_1q():
    """Fraction of serial layers spent on single-qudit gates, per base."""
    out = {}
    for d in BASES:
        m, w, gates = build(d, "uniform", 0.0)
        one_q = sum(c for s, _, c in gates if len(s) == 1)
        out[d] = {"m": m, "w": w, "layers_1q": one_q,
                  "layers_total": layer_count(gates),
                  "share": one_q / layer_count(gates)}
    return out


def main():
    os.makedirs(RESULTS, exist_ok=True)
    r = multiplicative_order(A, N)
    floors = {d: uniform_floor(d, r) for d in BASES}

    print("--- single-qudit share of the serial schedule ---")
    shares = share_1q()
    for d in BASES:
        v = shares[d]
        print(f"  d={d}: {v['layers_1q']:.0f} of {v['layers_total']:.0f} "
              f"layers are single-qudit ({100 * v['share']:.0f}%)")
    print("  -> the charge falls hardest on the largest base\n")

    jobs = [(d, model, cost, a) for model in MODELS for cost in COSTS
            for a in ALPHAS for d in BASES]
    print(f"{len(jobs)} exact-DM runs", flush=True)
    t0 = time.time()
    with ProcessPoolExecutor(max_workers=4) as ex:
        runs = list(ex.map(one, jobs))
    print(f"done in {time.time() - t0:.0f} s\n", flush=True)

    # noiseless baselines are unitary, hence independent of every cost
    base = {d: float(shor_run(d, a=A, N=N)["success"]) for d in BASES}

    def sig(x):
        return (x["success"] - floors[x["d"]]) / (base[x["d"]] - floors[x["d"]])

    lookup = {(x["d"], x["model"], x["cost"], x["alpha"]): sig(x)
              for x in runs}

    out = {"N": N, "a": A, "r": r, "strength": S, "alphas": ALPHAS,
           "calibrated": {str(k): v for k, v in CALIBRATED.items()},
           "floors": floors, "share_1q": shares, "runs": runs, "cells": []}

    for model in MODELS:
        print(f"=== {model} at s={S}: qudit-minus-qubit signal margin "
              f"vs single-qudit cost exponent ===")
        print(f"{'cost':>9} {'alpha':>6} " +
              "".join(f"{'d=' + str(d):>9}" for d in BASES) + "   verdict")
        for cost in COSTS:
            crit = {}
            prev = None
            for a in ALPHAS:
                row = {d: lookup[(d, model, cost, a)] for d in BASES}
                best = max((d for d in BASES if d != 2), key=lambda d: row[d])
                margin = row[best] - row[2]
                verdict = "qudit" if margin > 0 else "QUBIT"
                tag = ""
                if a in CALIBRATED:
                    tag = f"  <- {CALIBRATED[a]}"
                print(f"{cost:>9} {a:6.2f} " +
                      "".join(f"{row[d]:9.3f}" for d in BASES) +
                      f"   {verdict} (d={best}), margin {margin:+.3f}{tag}")
                if prev is not None and prev[1] > 0 >= margin:
                    # linear interpolation of the margin crossing in alpha
                    t = prev[1] / (prev[1] - margin)
                    crit["alpha_star"] = prev[0] + t * (a - prev[0])
                prev = (a, margin)
            m0 = lookup[(max((d for d in BASES if d != 2),
                             key=lambda d: lookup[(d, model, cost, 0.0)]),
                         model, cost, 0.0)] - lookup[(2, model, cost, 0.0)]
            cell = {"model": model, "cost": cost, "margin_at_alpha0": m0,
                    **crit}
            for a in CALIBRATED:
                row = {d: lookup[(d, model, cost, a)] for d in BASES}
                best = max((d for d in BASES if d != 2), key=lambda d: row[d])
                cell[f"margin_at_{a}"] = row[best] - row[2]
                cell[f"verdict_at_{a}"] = ("qudit" if row[best] > row[2]
                                           else "qubit")
            out["cells"].append(cell)
            star = crit.get("alpha_star")
            print(f"{'':>9} -> critical alpha* = "
                  f"{f'{star:.2f}' if star else 'none in swept range'}"
                  f" (measured range 2.15-3.15)\n")

    print("=== summary ===")
    survive = [c for c in out["cells"] if c["verdict_at_3.15"] == "qudit"]
    print(f"  at the steepest measured charge (alpha=3.15), "
          f"{len(survive)} of {len(out['cells'])} cells still favour a qudit")
    for c in out["cells"]:
        star = c.get("alpha_star")
        print(f"  {c['model']:>13}/{c['cost']:<9} margin "
              f"{c['margin_at_alpha0']:+.3f} (a=0) -> "
              f"{c['margin_at_2.15']:+.3f} (a=2.15) -> "
              f"{c['margin_at_3.15']:+.3f} (a=3.15)"
              f"   alpha* = {f'{star:.2f}' if star else '--'}")

    path = os.path.join(RESULTS, "single_qudit_cost.json")
    with open(path, "w") as f:
        json.dump(out, f, indent=1)
    print(f"\nwrote {path}")


if __name__ == "__main__":
    main()
