"""Decoder-convention and modulus-robustness study (round-5 referees).

Two stress tests of the Table II demo grid (N = 21, a = 2, r = 6,
s = 0.005, channels transmon_cal + depolarizing, cost models uniform /
ion / pavlidis):

  Part 1 (exact density matrices, N = 21): re-score the same outcome
  distributions under three continued-fraction decoder conventions --
  the paper's non-lifting decoder (a convergent denominator must be a
  multiple of r), and two textbook Odlyzko-lift variants that recover
  r~ = r/gcd(s,r) and lift over multiples kq <= N (all convergents /
  best convergent only). Referee 2 (round 5) reports that the d=5 vs
  d=3 ordering in two cells reverses under a lifting decoder; this
  script tests that claim on the committed machinery.

  Part 2 (Monte Carlo trajectories, N = 29, a = 2, r = 28): the same
  grid on a second alignment-neutral modulus, both decoders scored on
  the same trajectories. Referee 2's Eq.-(16) arithmetic predicts the
  ladder/ion qutrit cell flips to the qubit at N = 29 (register
  granularity: N = 21 wastes 14% of the qubit work register and only
  5.6% of the ququint's; N = 29 flips the sign).

Run: python3 decoder_convention_study.py [part1|part2|all] [n_traj]
Writes results/decoder_convention_study.json (part1 key) and merges the
part2 key into the same file.
"""

import json
import os
import sys
import time
import zlib
from concurrent.futures import ProcessPoolExecutor

import numpy as np

from qudit_shor import (apply_cost_model, apply_unitary_vec,
                        build_shor_gates, convergents, multiplicative_order,
                        recovered_order, shor_config, shor_run)
from trajectories import _kraus_sets, _sample_kraus

STRENGTH = 0.005
MODELS = ["transmon_cal", "depolarizing"]
COSTS = ["uniform", "ion", "pavlidis"]
BASES = [2, 3, 5]


# ---------------------------------------------------------------------------
# Decoder conventions
# ---------------------------------------------------------------------------


def _minimize(q: int, a: int, N: int):
    for r in range(1, q + 1):
        if q % r == 0 and pow(a, r, N) == 1:
            return r
    return None


def decode_paper(y: int, D: int, a: int, N: int):
    return recovered_order(y, D, a, N)


def decode_lift_small(y: int, D: int, a: int, N: int, kmax: int = 4):
    """Every convergent denominator q <= N (p != 0), lifted over small
    multiples kq <= N with k <= kmax (Shor's 'try small multiples')."""
    if y == 0:
        return None
    for p, q in convergents(y, D):
        if q > N:
            break
        if p == 0:
            continue
        for k in range(1, kmax + 1):
            if k * q > N:
                break
            if pow(a, k * q, N) == 1:
                return _minimize(k * q, a, N)
    return None


def decode_lift_best(y: int, D: int, a: int, N: int):
    """Odlyzko lift on the best (largest-denominator) convergent <= N."""
    if y == 0:
        return None
    best = None
    for p, q in convergents(y, D):
        if q > N:
            break
        if p != 0:
            best = q
    if best is None:
        return None
    k = 1
    while k * best <= N:
        if pow(a, k * best, N) == 1:
            return _minimize(k * best, a, N)
        k += 1
    return None


DECODERS = {"paper": decode_paper, "lift_small": decode_lift_small,
            "lift_best": decode_lift_best}


def masks_for(d: int, m: int, a: int, N: int) -> dict:
    D = d ** m
    r_true = multiplicative_order(a, N)
    return {name: np.array([fn(y, D, a, N) == r_true for y in range(D)])
            for name, fn in DECODERS.items()}


# ---------------------------------------------------------------------------
# Part 1: exact density matrices at N = 21, re-scored per decoder
# ---------------------------------------------------------------------------


def part1_cell(args):
    d, model, cost, N, a = args
    t0 = time.time()
    res = shor_run(d, model, STRENGTH, a=a, N=N, cost_model=cost)
    probs = np.asarray(res["probs"])
    m = res["m"]
    out = {"d": d, "model": model, "cost": cost, "n_layers": res["n_layers"],
           "elapsed_s": round(time.time() - t0, 1)}
    for name, mask in masks_for(d, m, a, N).items():
        out[name] = float(probs[mask].sum())
    return out


def part1(N=21, a=2):
    jobs = [(d, model, cost, N, a) for d in BASES for model in MODELS
            for cost in COSTS if not (d == 2 and cost != "uniform")]
    base = {}
    for d in BASES:
        m, w = shor_config(d, N)
        D = d ** m
        masks = masks_for(d, m, a, N)
        res = shor_run(d, a=a, N=N)
        probs = np.asarray(res["probs"])
        base[d] = {"m": m, "w": w, "D": D}
        for name, mask in masks.items():
            base[d][f"floor_{name}"] = float(mask.mean())
            base[d][f"noiseless_{name}"] = float(probs[mask].sum())
        print(f"[part1] d={d} noiseless paper/lift_small/lift_best = "
              f"{base[d]['noiseless_paper']:.4f}/"
              f"{base[d]['noiseless_lift_small']:.4f}/"
              f"{base[d]['noiseless_lift_best']:.4f}  floors = "
              f"{base[d]['floor_paper']:.4f}/{base[d]['floor_lift_small']:.4f}/"
              f"{base[d]['floor_lift_best']:.4f}", flush=True)

    cells = []
    with ProcessPoolExecutor(max_workers=6) as ex:
        for out in ex.map(part1_cell, jobs):
            d = out["d"]
            for name in DECODERS:
                lo = base[d][f"floor_{name}"]
                hi = base[d][f"noiseless_{name}"]
                out[f"signal_{name}"] = (out[name] - lo) / (hi - lo)
            cells.append(out)
            print(f"[part1] d={out['d']} {out['model']:13s} "
                  f"{out['cost']:8s} signal paper={out['signal_paper']:.3f} "
                  f"lift_small={out['signal_lift_small']:.3f} "
                  f"lift_best={out['signal_lift_best']:.3f} "
                  f"({out['elapsed_s']}s)", flush=True)
    return {"N": N, "a": a, "r": multiplicative_order(a, N),
            "strength": STRENGTH, "base": base, "cells": cells}


# ---------------------------------------------------------------------------
# Part 2: trajectories at N = 29, both decoders on the same trajectories
# ---------------------------------------------------------------------------


def traj_cell(args):
    d, model, cost, N, a, n_traj = args
    t0 = time.time()
    m, w = shor_config(d, N)
    dims = [d] * (m + w)
    n = len(dims)
    gates = apply_cost_model(build_shor_gates(d, m, w, a, N), d, cost)
    Dc, Dw = d ** m, d ** w
    masks = masks_for(d, m, a, N)

    psi0 = np.zeros(Dc * Dw, complex)
    psi0[1] = 1.0
    psi0 = psi0.reshape(dims)

    costs = {c for _, _, c in gates}
    kraus_sets = _kraus_sets(d, model, STRENGTH, costs, 1.0)
    seed = zlib.crc32(f"decoder_study,{d},{model},{cost},{N}".encode())
    rng = np.random.default_rng(seed % (2 ** 32))

    succ = {name: np.empty(n_traj) for name in DECODERS}
    for k in range(n_traj):
        t = psi0
        for sites, U, c in gates:
            t = apply_unitary_vec(t, U, sites, dims)
            for q in range(n):
                t = _sample_kraus(t, q, n, kraus_sets[c], rng, dims)
        y = (np.abs(t.reshape(Dc, Dw)) ** 2).sum(axis=1)
        for name, mask in masks.items():
            succ[name][k] = y[mask].sum()
        if (k + 1) % 100 == 0:
            print(f"[part2] d={d} {model} {cost}: {k + 1}/{n_traj} traj "
                  f"({time.time() - t0:.0f}s)", flush=True)

    out = {"d": d, "model": model, "cost": cost, "m": m, "w": w,
           "n_layers": sum(c for _, _, c in gates), "n_traj": n_traj,
           "seed": seed % (2 ** 32),
           "elapsed_s": round(time.time() - t0, 1)}
    for name in DECODERS:
        out[name] = float(succ[name].mean())
        out[f"{name}_err"] = float(succ[name].std(ddof=1) / np.sqrt(n_traj))
    return out


def part2(N=29, a=16, n_traj=1000):
    # a=16 has order r=7 mod 29: alignment-neutral (7 divides no power of
    # 2, 3, 5) and scorable in every base under every decoder convention.
    # a=2 (r=28) is UNSCORABLE at d=2 under the paper decoder (noiseless
    # success = floor = 0.0000 at D=64): no convergent denominator <= N
    # of any y/64 is a multiple of 28.
    base = {}
    for d in BASES:
        m, w = shor_config(d, N)
        masks = masks_for(d, m, a, N)
        # noiseless exact run for ceilings
        res = traj_noiseless(d, m, w, a, N)
        base[d] = {"m": m, "w": w, "D": d ** m}
        for name, mask in masks.items():
            base[d][f"floor_{name}"] = float(mask.mean())
            base[d][f"noiseless_{name}"] = float(res[mask].sum())
        print(f"[part2] d={d} m={m} w={w} noiseless paper/lift_small = "
              f"{base[d]['noiseless_paper']:.4f}/"
              f"{base[d]['noiseless_lift_small']:.4f}  floors = "
              f"{base[d]['floor_paper']:.4f}/{base[d]['floor_lift_small']:.4f}",
              flush=True)

    jobs = [(d, model, cost, N, a, n_traj) for d in BASES for model in MODELS
            for cost in COSTS if not (d == 2 and cost != "uniform")]
    cells = []
    with ProcessPoolExecutor(max_workers=6) as ex:
        for out in ex.map(traj_cell, jobs):
            d = out["d"]
            for name in DECODERS:
                lo = base[d][f"floor_{name}"]
                hi = base[d][f"noiseless_{name}"]
                span = hi - lo
                if span < 0.05:
                    out[f"signal_{name}"] = None
                    out[f"signal_{name}_err"] = None
                    continue
                out[f"signal_{name}"] = (out[name] - lo) / span
                out[f"signal_{name}_err"] = out[f"{name}_err"] / span
            cells.append(out)
            fmt = lambda v: "n/a" if v is None else f"{v:.3f}"
            print(f"[part2] DONE d={out['d']} {out['model']:13s} "
                  f"{out['cost']:8s} signal paper="
                  f"{fmt(out['signal_paper'])}±{fmt(out['signal_paper_err'])} "
                  f"lift_best={fmt(out['signal_lift_best'])}"
                  f"±{fmt(out['signal_lift_best_err'])} "
                  f"({out['elapsed_s']}s)", flush=True)
    return {"N": N, "a": a, "r": multiplicative_order(a, N),
            "strength": STRENGTH, "n_traj": n_traj, "base": base,
            "cells": cells}


def traj_noiseless(d, m, w, a, N):
    dims = [d] * (m + w)
    gates = apply_cost_model(build_shor_gates(d, m, w, a, N), d, "uniform")
    Dc, Dw = d ** m, d ** w
    psi0 = np.zeros(Dc * Dw, complex)
    psi0[1] = 1.0
    t = psi0.reshape(dims)
    for sites, U, _ in gates:
        t = apply_unitary_vec(t, U, sites, dims)
    return (np.abs(t.reshape(Dc, Dw)) ** 2).sum(axis=1)


def main():
    which = sys.argv[1] if len(sys.argv) > 1 else "all"
    n_traj = int(sys.argv[2]) if len(sys.argv) > 2 else 1000
    os.makedirs("results", exist_ok=True)
    path = "results/decoder_convention_study.json"
    data = {}
    if os.path.exists(path):
        with open(path) as f:
            data = json.load(f)
    if which in ("part1", "all"):
        data["part1"] = part1()
        with open(path, "w") as f:
            json.dump(data, f, indent=1)
        print(f"wrote {path} (part1)", flush=True)
    if which in ("part2", "all"):
        data["part2"] = part2(n_traj=n_traj)
        with open(path, "w") as f:
            json.dump(data, f, indent=1)
        print(f"wrote {path} (part2)", flush=True)


if __name__ == "__main__":
    main()
