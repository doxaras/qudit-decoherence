"""The measured d = 4 point of the Hrmo native-gate series (round-3 referees).

Referee request (round-3, referees 1/2 minor): the paper's
measured-fidelity analysis uses the Hrmo et al. native light-shift gate
at d = 2/3/5 (99.6(1)/98.7(2)/93.7(3)%), skipping the same paper's
d = 4 point (97.0(2)%). Adding it tests the monotonicity assumption the
whole inflation analysis rests on: the inflation factor should
interpolate between d = 3 and d = 5, and the d = 4 verdict should track
the d = 3 one (composite dimension is immaterial here -- the bare
dynamics carries no trace of primality, Sec. VIII).

Conversions follow the channel-consistent rebuild (transmon_rebuild.py):
the ladder converts through its own damage identity s = eps/(2 L Delta(d))
with Delta(d) measured from the channel; the depolarizing rows through
the exact identity s = eps/(2 L (1 - 1/d^2)). L = 1 under uniform
accounting, L = d - 1 under ion. f is measured gate vs measured gate
(Hrmo's own d = 2 gate as reference). f* at d = 4 is swept, per channel
x cost, exactly as in noise_inflation.py.

Demo instance (N = 21, a = 2, r = 6): d = 4 runs m = 3, w = 3 (D = 64,
4^6 = 4096 dims), exact density-matrix evolution throughout -- the same
configuration as d4_control.py.

Writes results/hrmo_d4.json. Run: python3 hrmo_d4.py
"""

import json
import math
import os
import time
from concurrent.futures import ProcessPoolExecutor

import numpy as np

from qudit_shor import (multiplicative_order, noise_superop, recovered_order,
                        shor_config, shor_run)

N, A = 21, 2
S2 = {"transmon_cal": 0.003, "depolarizing": 0.005}
COSTS = ["uniform", "ion"]
FACTORS = [1.0, 1.25, 1.5, 1.75, 2.0, 2.5, 3.0, 4.0]
HRMO_EPS = {2: (0.004, 0.001), 4: (0.030, 0.002)}   # 99.6(1)% / 97.0(2)%

RESULTS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results")


def ladder_damage(d: int) -> float:
    """Per-carrier-layer entanglement infidelity per unit strength."""
    s = 1e-6
    E = noise_superop(d, "transmon_cal", s)
    return (1.0 - float(np.real(np.trace(E))) / d ** 2) / s


def uniform_floor(d: int, r: int) -> float:
    m, _ = shor_config(d, N)
    D = d ** m
    return sum(recovered_order(y, D, A, N) == r for y in range(D)) / D


def one(args):
    d, model, s, cost, gate_s = args
    t0 = time.time()
    if model is None:
        res = shor_run(d, a=A, N=N, cost_model="uniform")
    elif gate_s is not None:
        res = shor_run(d, model, s, a=A, N=N, cost_model=cost,
                       gate_strength=gate_s)
    else:
        res = shor_run(d, model, s, a=A, N=N, cost_model=cost)
    return {"d": d, "model": model, "strength": s, "cost": cost,
            "gate_strength": gate_s, "success": float(res["success"]),
            "elapsed_s": round(time.time() - t0, 1)}


def main():
    os.makedirs(RESULTS, exist_ok=True)
    r = multiplicative_order(A, N)
    d4 = 4
    delta2, delta4 = ladder_damage(2), ladder_damage(d4)
    dep2, dep4 = 0.75, 1.0 - 1.0 / d4 ** 2
    print(f"Delta(2) = {delta2:.5f}  Delta(4) = {delta4:.5f}")
    print(f"depol damage: d=2 {dep2}, d=4 {dep4:.5f}")

    def conv(d_chan, eps, L):
        return eps / (2 * L * d_chan)

    # measured inflation factors, both channel identities x both accountings
    eps2, sig2e = HRMO_EPS[2]
    eps4, sig4e = HRMO_EPS[4]
    fs = {}
    for chan, d2, d4v in (("transmon_cal", delta2, delta4),
                          ("depolarizing", dep2, dep4)):
        for cost in COSTS:
            L1, L4 = 1.0, (1.0 if cost == "uniform" else float(d4 - 1))
            s2m = conv(d2, eps2, L1)
            s4m = conv(d4v, eps4, L4)
            f = s4m / s2m
            rel = math.sqrt((sig4e / eps4) ** 2 + (sig2e / eps2) ** 2)
            fs[(chan, cost)] = (f, f * rel, s4m, s2m)
            print(f"{chan:>13} {cost:>7}: s4 {s4m:.5f} vs s2 {s2m:.5f} "
                  f"-> f = {f:.2f} +/- {f * rel:.2f}")

    floors = {2: uniform_floor(2, r), 4: uniform_floor(d4, r)}

    # --- job list ---------------------------------------------------------
    jobs = [(2, None, 0.0, "uniform", None), (4, None, 0.0, "uniform", None)]
    for chan, s2 in S2.items():
        jobs.append((2, chan, s2, "uniform", None))          # qubit anchor
        for cost in COSTS:
            for fct in FACTORS:                              # f* sweep
                jobs.append((4, chan, s2 * fct, cost, None))
            for scope in ("global", "gate"):                 # measured f
                f, fsig, _, _ = fs[(chan, cost)]
                for ff in (max(f - fsig, 0.0), f, f + fsig):
                    jobs.append((4, chan, s2 * ff, cost, None)
                                if scope == "global" else
                                (4, chan, s2, cost, s2 * ff))
    jobs = list(dict.fromkeys(jobs))
    print(f"{len(jobs)} exact-DM runs", flush=True)
    t0 = time.time()
    with ProcessPoolExecutor(max_workers=4) as ex:
        runs = list(ex.map(one, jobs))
    print(f"grid done in {time.time() - t0:.0f} s", flush=True)
    res = {tuple(j): x["success"] for j, x in zip(jobs, runs)}

    base = {d: res[(d, None, 0.0, "uniform", None)] for d in (2, 4)}

    def signal(d, succ):
        return (succ - floors[d]) / (base[d] - floors[d])

    rows, fstars = [], {}
    for chan, s2 in S2.items():
        sig2 = signal(2, res[(2, chan, s2, "uniform", None)])
        for cost in COSTS:
            fsig = [signal(4, res[(4, chan, s2 * fct, cost, None)])
                    for fct in FACTORS]
            diff = np.asarray(fsig) - sig2
            fstar = None
            for i in range(1, len(FACTORS)):
                if diff[i - 1] >= 0 > diff[i]:
                    t = diff[i - 1] / (diff[i - 1] - diff[i])
                    fstar = FACTORS[i - 1] + t * (FACTORS[i] - FACTORS[i - 1])
                    break
            fstars[f"{chan}/{cost}"] = fstar
            f, fs_1s, s4m, s2m = fs[(chan, cost)]
            for scope in ("global", "gate"):
                sigs = {}
                for lab, ff in (("lo", max(f - fs_1s, 0.0)), ("central", f),
                                ("hi", f + fs_1s)):
                    job = ((4, chan, s2 * ff, cost, None) if scope == "global"
                           else (4, chan, s2, cost, s2 * ff))
                    sigs[lab] = signal(4, res[job])
                verdict = ("LOST (even at -1 sigma)"
                           if sigs["lo"] < sig2 and sigs["central"] < sig2
                           else "lost (survives at -1 sigma)"
                           if sigs["central"] < sig2 else "SURVIVES")
                rows.append({"channel": chan, "cost": cost, "scope": scope,
                             "f_central": f, "f_sigma": fs_1s,
                             "f_star": fstar, "qubit_signal": sig2,
                             "qudit_signal": sigs, "verdict": verdict})
                print(f"{chan:>13} {cost:>7} {scope:>6}: f {f:.2f}+/-{fs_1s:.2f} "
                      f"f* {fstar if fstar else '>4'}  "
                      f"sig {sigs['lo']:.3f}/{sigs['central']:.3f}/"
                      f"{sigs['hi']:.3f} vs {sig2:.3f}  {verdict}")

    out = {"N": N, "a": A, "r": r, "d": d4,
           "hrmo_eps": {str(k): v for k, v in HRMO_EPS.items()},
           "delta2": delta2, "delta4": delta4, "floors": floors,
           "noiseless": base, "s2": S2, "factors": FACTORS,
           "f_stars": fstars, "rows": rows, "runs": runs}
    path = os.path.join(RESULTS, "hrmo_d4.json")
    with open(path, "w") as fh:
        json.dump(out, fh, indent=1)
    print(f"\nwrote {path}")


if __name__ == "__main__":
    main()
