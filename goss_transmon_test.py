"""The inflation threshold at the measured Goss cross-Kerr qutrit gates.

The Discussion recommends the native-entangler transmon route, but the
measured transmon qutrit gates of Goss et al., Nat. Commun. 13, 7481
(2022) -- CZ+ process fidelity 97.3(1)%, CZ 95.2(3)% -- were never run
against the paper's own threshold. This script closes that gap on the
physically matched pairing (calibrated ladder, uniform cost, d = 3).

Goss et al. report no qubit-subspace two-qubit gate on the same
apparatus, so unlike the Hrmo analysis the inflation factor cannot be a
same-device ratio. Instead the qubit anchor is the paper's transmon
operating point s2 = 0.003 -- equivalent to assuming a same-class
transmon two-qubit gate at eps2 = 2 L (1 - 1/4) s2 = 0.0045, i.e.
99.55% fidelity, representative of the platform -- and the qutrit's
implied per-carrier-layer strength is s3 = eps3 / (2 L (1 - 1/9)) with
L = 1 (single-application cross-Kerr, uniform accounting). Both
inflation scopes are run: global (every carrier-layer at f s2) and
gate-only (participants of each entangling gate at f s2).

Writes results/goss_transmon_test.json. Run: python3 goss_transmon_test.py
"""

import json
import os
import time
from concurrent.futures import ProcessPoolExecutor

from hrmo_reanalysis import uniform_floor, N, A, RESULTS
from qudit_shor import multiplicative_order, shor_run

S2 = 0.003                     # calibrated-ladder transmon operating point
CHANNEL = "transmon_cal"
EPS2_EQUIV = 2 * 1 * (1 - 1 / 4) * S2   # qubit-gate infidelity the anchor implies

# Goss et al. 2022: process infidelity and 1-sigma by gate.
GOSS_EPS = {"CZ+": (0.027, 0.001), "CZ": (0.048, 0.003)}

F_STAR_GLOBAL = 2.05           # ladder/uniform d=3, from noise_inflation.json


def goss_f(eps, sig):
    """Inflation factor f = s3/s2 implied by a measured qutrit infidelity."""
    s3 = eps / (2 * 1 * (1 - 1 / 9))
    f = s3 / S2
    return f, f * (sig / eps)


def one(args):
    d, s, scope, gate_s = args
    t0 = time.time()
    if s == 0.0:
        res = shor_run(d, a=A, N=N, cost_model="uniform")
    elif scope == "gate":
        res = shor_run(d, CHANNEL, s, a=A, N=N, cost_model="uniform",
                       gate_strength=gate_s)
    else:
        res = shor_run(d, CHANNEL, s, a=A, N=N, cost_model="uniform")
    return {"d": d, "strength": s, "scope": scope, "gate_strength": gate_s,
            "success": float(res["success"]),
            "elapsed_s": round(time.time() - t0, 1)}


def main():
    os.makedirs(RESULTS, exist_ok=True)
    r = multiplicative_order(A, N)
    floors = {d: uniform_floor(d, r) for d in (2, 3)}

    variants = {}  # (gate, scope) -> [(label, f, args tuple)]
    jobs = [(2, 0.0, None, None), (3, 0.0, None, None),
            (2, S2, "global", None)]
    for gate, (eps, sig) in GOSS_EPS.items():
        f, fs = goss_f(eps, sig)
        for scope in ("global", "gate"):
            vs = []
            for lab, ff in (("lo", f - fs), ("central", f), ("hi", f + fs)):
                if scope == "global":
                    job = (3, S2 * ff, "global", None)
                else:
                    job = (3, S2, "gate", S2 * ff)
                vs.append((lab, ff, job))
                jobs.append(job)
            variants[(gate, scope)] = vs
    print(f"{len(jobs)} exact-DM runs", flush=True)

    t0 = time.time()
    with ProcessPoolExecutor(max_workers=4) as ex:
        runs = list(ex.map(one, jobs))
    print(f"all runs done in {time.time() - t0:.0f} s", flush=True)

    def lookup(job):
        d, s, scope, gate_s = job
        return next(x["success"] for x in runs
                    if x["d"] == d and abs(x["strength"] - (s or 0.0)) < 1e-15
                    and x["scope"] == scope
                    and (x["gate_strength"] is None) == (gate_s is None)
                    and (gate_s is None
                         or abs(x["gate_strength"] - gate_s) < 1e-15))

    base = {d: lookup((d, 0.0, None, None)) for d in (2, 3)}

    def signal(d, succ):
        return (succ - floors[d]) / (base[d] - floors[d])

    sig2 = signal(2, lookup((2, S2, "global", None)))

    out = {"N": N, "a": A, "r": r, "channel": CHANNEL, "s2": S2,
           "eps2_equivalent": EPS2_EQUIV,
           "goss_eps": GOSS_EPS, "f_star_global": F_STAR_GLOBAL,
           "floors": floors, "noiseless": base, "qubit_signal": sig2,
           "runs": runs, "cells": []}

    print(f"\nqubit anchor (ladder, s={S2}): signal {sig2:.3f} "
          f"(implied eps2 = {EPS2_EQUIV:.4f})")
    print(f"{'gate':>5} {'scope':>7} {'f (1s)':>16} "
          f"{'qutrit sig (lo/c/hi)':>22}  verdict")
    for gate, (eps, sig) in GOSS_EPS.items():
        f, fs = goss_f(eps, sig)
        for scope in ("global", "gate"):
            sigs = {lab: signal(3, lookup(job))
                    for lab, _, job in variants[(gate, scope)]}
            lost_c = sigs["central"] < sig2
            lost_lo = sigs["lo"] < sig2
            verdict = ("LOST (even at -1 sigma)" if lost_lo and lost_c
                       else "lost (survives at -1 sigma)" if lost_c
                       else "SURVIVES")
            out["cells"].append({
                "gate": gate, "scope": scope, "eps": eps, "eps_sigma": sig,
                "f_central": f, "f_sigma": fs,
                "qubit_signal": sig2, "qutrit_signal": dict(sigs),
                "verdict": verdict})
            print(f"{gate:>5} {scope:>7} {f:5.2f} +/- {fs:4.2f}  "
                  f"{sigs['lo']:6.3f}/{sigs['central']:6.3f}/"
                  f"{sigs['hi']:6.3f}  {verdict}")

    # Gate-only critical factor by bisection: the f at which the qutrit's
    # gate-only signal meets the qubit anchor (global-scope f* = 2.05 is
    # already committed in results/noise_inflation.json).
    lo, hi = 2.0, 6.0
    for _ in range(9):
        mid = (lo + hi) / 2
        s = signal(3, shor_run(3, CHANNEL, S2, a=A, N=N,
                               cost_model="uniform",
                               gate_strength=S2 * mid)["success"])
        if s > sig2:
            lo = mid
        else:
            hi = mid
    f_star_gate = (lo + hi) / 2
    eps_gate = f_star_gate * S2 * 2 * (1 - 1 / 9)
    eps_glob = F_STAR_GLOBAL * S2 * 2 * (1 - 1 / 9)
    out["f_star_gate_only"] = f_star_gate
    out["eps3_target_gate_only"] = eps_gate
    out["eps3_target_global"] = eps_glob
    print(f"\ngate-only f* = {f_star_gate:.2f} -> eps3 target "
          f"{eps_gate:.4f} ({100 * (1 - eps_gate):.1f}% fidelity); "
          f"global f* = {F_STAR_GLOBAL} -> {eps_glob:.4f} "
          f"({100 * (1 - eps_glob):.1f}%)")

    path = os.path.join(RESULTS, "goss_transmon_test.json")
    with open(path, "w") as fh:
        json.dump(out, fh, indent=1)
    print(f"\nwrote {path}")


if __name__ == "__main__":
    main()
