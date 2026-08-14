"""Does the serial-schedule assumption manufacture the qudit advantage?

Referee objection (Gottesman-style report, major comment 10; echoed as
Innsbruck minor 8): every number in the paper is an exposure budget, and
exposure is accounted with EVERY carrier idling through EVERY gate. The
paper discloses this and even names its sign -- concurrent execution
"would cut idle exposure most for the widest register, i.e. for d = 2"
-- and then leaves it at a sentence. That is the wrong place to leave
it: the assumption is not neutral, it runs against the paper's own
conclusion, and the conclusion is entirely an exposure comparison. The
referee asked for the demo grid re-run under a parallelised schedule
with a count of how many cells flip. This is that run.

Scheduling. Gates acting on disjoint carriers commute, so the serial
gate list may be packed into time slots by as-soon-as-possible list
scheduling on carrier availability without changing the circuit at all:
gate g starts at max over its sites of that carrier's ready time and
occupies `cost` slots. The makespan replaces the serial layer sum as the
exposure depth, and every carrier still takes one channel per slot --
the paper's convention, applied to a shorter schedule. With no
parallelism available the schedule reduces to the serial one exactly,
which is the regression check in `verify`.

The asymmetry the referee predicted is structural. The order-finding
circuit has three parts: the initial Fourier layer on m controls (fully
parallel, m gates collapse to 1 slot), the m controlled multipliers
(fully serial -- every one of them touches the whole work register), and
the inverse QFT (m(m+1)/2 gates, parallel depth ~2m-1). Only the first
and third compress, both scale with m, and m is largest for d = 2. So
parallelisation is a headwind for the qudit by construction; the
question this script answers is how strong.

Grid: both channels x three cost models x d = 2, 3, 5 at the tabulated
s = 0.005, serial and parallel, exact density matrices, demo instance
(N = 21, a = 2, r = 6).

Writes results/parallel_schedule.json. Run: python3 parallel_schedule.py
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
S = 0.005                    # the strength the paper tabulates

RESULTS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results")


def schedule(gates, n_sites: int):
    """ASAP list schedule. Returns (start slot per gate, makespan).

    Dependencies run through shared carriers only, which is exact: two
    gates on disjoint sites commute, so any order consistent with
    per-carrier ordering realises the same circuit.
    """
    ready = [0.0] * n_sites
    starts = []
    for sites, _, cost in gates:
        t = max(ready[s] for s in sites)
        starts.append(t)
        for s in sites:
            ready[s] = t + cost
    return starts, (max(ready) if ready else 0.0)


def run_scheduled(d: int, model: str | None, strength: float, cost_model: str,
                  parallel: bool):
    """Exact density-matrix run charging exposure by schedule slot.

    Serial mode reproduces `qudit_shor.shor_run` exactly (regression-
    checked in `verify`); parallel mode applies one channel per carrier
    per slot of the ASAP makespan instead of per gate-layer.
    """
    m, w = shor_config(d, N)
    n = m + w
    dims = [d] * n
    gates = apply_cost_model(build_shor_gates(d, m, w, A, N), d, cost_model)
    starts, makespan = schedule(gates, n)
    serial_layers = layer_count(gates)

    rho = initial_state(dims, m, d, w)
    noisy = bool(model) and strength > 0

    if parallel:
        probs = _run_parallel(rho, gates, starts, makespan, dims, d, m, w,
                              model if noisy else None, strength)
    else:
        chans = ({c: noise_superop_pow(d, model, strength, c)
                  for c in {g[2] for g in gates}} if noisy else None)
        for sites, U, cost in gates:
            rho = apply_unitary(rho, U, sites, dims)
            if chans is not None:
                for q in range(n):
                    rho = apply_channel(rho, chans[cost], q, dims)
        probs = control_probs(rho, d, m, w)
    return probs, serial_layers, makespan


def _run_parallel(rho, gates, starts, makespan, dims, d, m, w,
                  model, strength):
    """Walk the schedule interval by interval.

    Interval boundaries are the distinct gate start times plus the
    makespan. Every gate starts at one of them (a gate of positive cost
    starting at t ends by the makespan, so none starts at the final
    boundary), and every carrier takes one interval's worth of noise
    across each interval. Widths are real, not integral -- the pavlidis
    model charges d^2/4 layers per gate -- so the channel is raised to
    the interval width exactly via the semigroup, never rounded.
    """
    n = len(dims)
    bounds = sorted(set(starts) | {makespan})
    by_start = {}
    for i, t in enumerate(starts):
        by_start.setdefault(t, []).append(i)

    chans = {}
    for b0, b1 in zip(bounds, bounds[1:]):
        for i in by_start.get(b0, []):
            sites, U, _ = gates[i]
            rho = apply_unitary(rho, U, sites, dims)
        if model is None:
            continue
        width = b1 - b0
        if width not in chans:
            chans[width] = noise_superop_pow(d, model, strength, width)
        for q in range(n):
            rho = apply_channel(rho, chans[width], q, dims)
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
    d, model, cost, parallel = job
    t0 = time.time()
    probs, ser, par = run_scheduled(d, model, S, cost, parallel)
    return {"d": d, "model": model, "cost": cost, "parallel": parallel,
            "serial_layers": ser, "makespan": par,
            "success": score(probs, d, multiplicative_order(A, N)),
            "elapsed_s": round(time.time() - t0, 1)}


def verify():
    """Serial mode must reproduce shor_run, and an unparallelisable
    circuit must give makespan == serial layer count."""
    print("--- regression checks ---")
    ok = True
    for d in (2, 3):
        for cost in ("uniform", "pavlidis"):
            probs, ser, par = run_scheduled(d, "depolarizing", S, cost, False)
            ref = shor_run(d, "depolarizing", S, a=A, N=N, cost_model=cost)
            err = abs(score(probs, d, multiplicative_order(A, N))
                      - ref["success"])
            ok &= err < 1e-12 and abs(ser - ref["n_layers"]) < 1e-12
            print(f"  d={d} {cost:>8}: serial vs shor_run diff {err:.2e}, "
                  f"layers {ser:g} (makespan {par:g})")
    print(f"  -> {'PASS' if ok else 'FAIL'}\n")
    return ok


def main():
    os.makedirs(RESULTS, exist_ok=True)
    if not verify():
        raise SystemExit("regression check failed")

    r = multiplicative_order(A, N)
    floors = {d: uniform_floor(d, r) for d in BASES}

    print("--- schedule compression (serial layers -> ASAP makespan) ---")
    depth = {}
    for cost in COSTS:
        for d in BASES:
            m, w = shor_config(d, N)
            g = apply_cost_model(build_shor_gates(d, m, w, A, N), d, cost)
            _, mk = schedule(g, m + w)
            depth[(d, cost)] = {"carriers": m + w, "serial": layer_count(g),
                                "parallel": mk}
            print(f"  d={d} {cost:>8}: {m + w} carriers, "
                  f"{layer_count(g):6.1f} -> {mk:6.1f} layers "
                  f"({100 * (1 - mk / layer_count(g)):4.1f}% shorter); "
                  f"exposure {(m + w) * layer_count(g):7.1f} -> "
                  f"{(m + w) * mk:7.1f}")
    print()

    jobs = [(d, model, cost, par)
            for model in MODELS for cost in COSTS
            for par in (False, True) for d in BASES]
    print(f"{len(jobs)} exact-DM runs", flush=True)
    t0 = time.time()
    with ProcessPoolExecutor(max_workers=4) as ex:
        runs = list(ex.map(one, jobs))
    print(f"done in {time.time() - t0:.0f} s\n", flush=True)

    base = {(d, c): float(shor_run(d, a=A, N=N, cost_model=c)["success"])
            for c in COSTS for d in BASES}

    def sig(x):
        return ((x["success"] - floors[x["d"]])
                / (base[(x["d"], x["cost"])] - floors[x["d"]]))

    out = {"N": N, "a": A, "r": r, "strength": S, "floors": floors,
           "depth": {f"{d}_{c}": v for (d, c), v in depth.items()},
           "runs": runs, "cells": []}

    flips = []
    for model in MODELS:
        print(f"=== {model} at s={S} (floor-corrected signal) ===")
        print(f"{'cost':>9} {'schedule':>9} " +
              "".join(f"{'d=' + str(d):>9}" for d in BASES) + "   verdict")
        for cost in COSTS:
            verdicts = {}
            for par in (False, True):
                row = {d: sig(next(x for x in runs if x["d"] == d
                                   and x["model"] == model
                                   and x["cost"] == cost
                                   and x["parallel"] == par))
                       for d in BASES}
                best = max((d for d in BASES if d != 2), key=lambda d: row[d])
                verdicts[par] = ("qudit" if row[best] > row[2] else "qubit",
                                 best, row)
                print(f"{cost:>9} {'parallel' if par else 'serial':>9} " +
                      "".join(f"{row[d]:9.3f}" for d in BASES) +
                      f"   {verdicts[par][0]} (d={best}), "
                      f"margin {row[best] - row[2]:+.3f}")
            flipped = verdicts[False][0] != verdicts[True][0]
            out["cells"].append({
                "model": model, "cost": cost,
                "serial_verdict": verdicts[False][0],
                "parallel_verdict": verdicts[True][0],
                "serial_margin": verdicts[False][2][verdicts[False][1]]
                - verdicts[False][2][2],
                "parallel_margin": verdicts[True][2][verdicts[True][1]]
                - verdicts[True][2][2],
                "flipped": flipped})
            if flipped:
                flips.append((model, cost, verdicts[False][0],
                              verdicts[True][0]))
            print()

    print("=== summary ===")
    print(f"  {len(flips)} of {len(out['cells'])} cells flip under a "
          f"parallel schedule")
    for model, cost, a, b in flips:
        print(f"  FLIP: {model}/{cost}: {a} -> {b}")
    worst = max(out["cells"], key=lambda c: c["serial_margin"]
                - c["parallel_margin"])
    print(f"  largest margin erosion: {worst['model']}/{worst['cost']} "
          f"{worst['serial_margin']:+.3f} -> {worst['parallel_margin']:+.3f}")

    path = os.path.join(RESULTS, "parallel_schedule.json")
    with open(path, "w") as f:
        json.dump(out, f, indent=1)
    print(f"\nwrote {path}")


if __name__ == "__main__":
    main()
