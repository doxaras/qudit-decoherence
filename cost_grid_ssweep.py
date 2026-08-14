"""Noise-strength robustness of the central cost table.

Referee objection (Gottesman-style report, major comment 2): the paper's
title claim rests on Table `tab:cost` -- six cells on one instance at a
single common strength (s = 0.005), with no uncertainties and no sweep.
Some winning margins there are small (the ladder/`ion`/d=5 cell loses by
0.026), so the question is whether the verdicts are a property of the
cost model or of the strength it was evaluated at.

Note on "error bars": those cells are exact density-matrix evolution,
so they carry NO statistical uncertainty -- the numbers are exact for
the stated channel, instance and cost model. The uncertainty that
matters is systematic, and the axis the paper never swept is s. This
script sweeps it across the full demo range for every cell of the
table, reports the winner at each strength, and flags cells whose
verdict is not constant in s.

Grid: both channels x three cost models x d = 2, 3, 5 x seven
strengths, exact density matrices, demo instance (N = 21, a = 2, r = 6).

Writes results/cost_grid_ssweep.json. Run: python3 cost_grid_ssweep.py
"""

import json
import os
import sys
import time
from concurrent.futures import ProcessPoolExecutor

from qudit_shor import (multiplicative_order, recovered_order, shor_config,
                        shor_run)

N, A = 21, 2

# A "winner" is only meaningful while the metric still has dynamic range.
# Once every base has been driven to the random floor the ranking is
# decided by third-decimal noise around zero, so cells whose best signal
# falls below this are reported as collapsed rather than won.
LIVE = 0.10
MODELS = ["depolarizing", "transmon_cal"]
COSTS = ["uniform", "ion", "pavlidis"]
DIMS = [2, 3, 5]
STRENGTHS = [0.001, 0.002, 0.003, 0.005, 0.01, 0.02, 0.05]
TABLE_S = 0.005                     # the strength the paper tabulates

RESULTS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results")


def uniform_floor(d: int, r: int) -> float:
    m, _ = shor_config(d, N)
    D = d ** m
    return sum(recovered_order(y, D, A, N) == r for y in range(D)) / D


def one(args):
    d, model, s, cost = args
    t0 = time.time()
    res = (shor_run(d, model, s, a=A, N=N, cost_model=cost) if model
           else shor_run(d, a=A, N=N, cost_model=cost))
    return {"d": d, "model": model, "strength": s, "cost": cost,
            "success": float(res["success"]),
            "elapsed_s": round(time.time() - t0, 1)}


def main():
    os.makedirs(RESULTS, exist_ok=True)
    path = os.path.join(RESULTS, "cost_grid_ssweep.json")

    # `--analyze` re-reports from the saved runs without re-simulating.
    if len(sys.argv) > 1 and sys.argv[1] == "--analyze":
        saved = json.load(open(path))
        floors = {int(k): v for k, v in saved["floors"].items()}
        base = {(x["d"], x["cost"]): x["success"]
                for x in saved["runs"] if x["model"] is None}

        def sig_at(d, model, cost, s):
            v = next(x["success"] for x in saved["runs"]
                     if x["d"] == d and x["model"] == model
                     and x["cost"] == cost
                     and abs(x["strength"] - s) < 1e-12)
            return (v - floors[d]) / (base[(d, cost)] - floors[d])

        saved["cells"] = []
        saved["live_cutoff"] = LIVE
        analyze(saved, sig_at)
        with open(path, "w") as f:
            json.dump(saved, f, indent=1)
        print(f"\nrewrote {path}")
        return

    r = multiplicative_order(A, N)
    floors = {d: uniform_floor(d, r) for d in DIMS}

    jobs = [(d, None, 0.0, cost) for cost in COSTS for d in DIMS]
    jobs += [(d, model, s, cost)
             for model in MODELS for cost in COSTS
             for s in STRENGTHS for d in DIMS]
    print(f"{len(jobs)} exact-DM runs", flush=True)

    t0 = time.time()
    with ProcessPoolExecutor(max_workers=4) as ex:
        runs = list(ex.map(one, jobs))
    print(f"done in {time.time() - t0:.0f} s\n", flush=True)

    base = {(x["d"], x["cost"]): x["success"]
            for x in runs if x["model"] is None}

    def signal(d, cost, succ):
        return (succ - floors[d]) / (base[(d, cost)] - floors[d])

    def sig_at(d, model, cost, s):
        v = next(x["success"] for x in runs
                 if x["d"] == d and x["model"] == model
                 and x["cost"] == cost and abs(x["strength"] - s) < 1e-12)
        return signal(d, cost, v)

    out = {"N": N, "a": A, "r": r, "strengths": STRENGTHS, "live_cutoff": LIVE,
           "floors": floors, "runs": runs, "cells": []}
    analyze(out, sig_at)

    path = os.path.join(RESULTS, "cost_grid_ssweep.json")
    with open(path, "w") as f:
        json.dump(out, f, indent=1)
    print(f"\nwrote {path}")


def analyze(out, sig_at):
    """Report the two questions the table actually makes claims about:
    does the best qudit beat the qubit, and which qudit is best -- each
    judged only where the metric still has dynamic range."""
    unstable, ties = [], []
    for model in MODELS:
        print(f"=== {model} (floor-corrected signal) ===")
        print(f"{'cost':>9} {'d':>2} " +
              "".join(f"{s:>8}" for s in STRENGTHS))
        for cost in COSTS:
            for d in DIMS:
                print(f"{cost:>9} {d:>2} " +
                      "".join(f"{sig_at(d, model, cost, s):8.3f}"
                              for s in STRENGTHS))
            live, verdicts, best, margins = [], [], [], []
            for s in STRENGTHS:
                sigs = {d: sig_at(d, model, cost, s) for d in DIMS}
                top = max(DIMS, key=lambda d: sigs[d])
                alive = sigs[top] > LIVE
                live.append(alive)
                if alive:
                    bq = max(d for d in DIMS if d != 2)  # placeholder
                    best_qudit = max((d for d in DIMS if d != 2),
                                     key=lambda d: sigs[d])
                    verdicts.append("qudit" if sigs[best_qudit] > sigs[2]
                                    else "qubit")
                    best.append(best_qudit)
                    margins.append(sigs[best_qudit] - sigs[2])
            tab = {d: sig_at(d, model, cost, TABLE_S) for d in DIMS}
            tab_best = max((d for d in DIMS if d != 2), key=lambda d: tab[d])
            tab_verdict = "qudit" if tab[tab_best] > tab[2] else "qubit"
            n_live = sum(live)
            v_stable = len(set(verdicts)) <= 1
            b_stable = len(set(best)) <= 1
            # near-tie between the two qudits at the tabulated strength
            others = sorted((d for d in DIMS if d != 2),
                            key=lambda d: -tab[d])
            tie = (len(others) > 1
                   and abs(tab[others[0]] - tab[others[1]]) < 0.01)
            out["cells"].append({
                "model": model, "cost": cost,
                "tabulated_winner": tab_best,
                "tabulated_verdict": tab_verdict,
                "live_strengths": [s for s, a in zip(STRENGTHS, live) if a],
                "verdict_by_live_strength": verdicts,
                "best_qudit_by_live_strength": best,
                "qudit_margin_by_live_strength": margins,
                "verdict_stable": v_stable, "best_qudit_stable": b_stable,
                "qudit_near_tie_at_table_s": tie,
            })
            msg = (f"{tab_verdict} wins at s={TABLE_S} (best qudit d={tab_best}); "
                   f"over {n_live} live strengths: verdict "
                   f"{'STABLE' if v_stable else 'FLIPS ' + str(verdicts)}, "
                   f"best qudit "
                   f"{'stable d=' + str(best[0]) if b_stable else 'varies ' + str(best)}")
            if tie:
                msg += f"  [d={others[0]} vs d={others[1]} within 0.01 -- a tie]"
                ties.append((model, cost, others[0], others[1]))
            if not v_stable:
                unstable.append((model, cost, verdicts))
            print(f"{'':>9} -> {msg}\n")

    print("=== summary ===")
    print(f"  cells judged only where best signal > {LIVE} "
          f"(beyond that every base sits at the random floor)")
    if unstable:
        for model, cost, v in unstable:
            print(f"  VERDICT FLIPS: {model}/{cost} -> {v}")
    else:
        print("  qudit-vs-qubit verdict is stable in s in every cell")
    for model, cost, a, b in ties:
        print(f"  NEAR-TIE at s={TABLE_S}: {model}/{cost} d={a} vs d={b}")


if __name__ == "__main__":
    main()
