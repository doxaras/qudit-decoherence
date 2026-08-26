"""f* under the harsher 2d ion-cost count (round-3 referee 3, minor 4).

The paper's `ion` cost model charges each entangling gate d - 1 layers:
the supplement of Ringbauer et al. 2022 decomposes the d-dimensional
controlled-increment into 2(d-1) pairwise fully entangling (two-pulse MS)
gates, normalized to 1 at d = 2. The same reference's main text quotes
2d MS gates for the Cinc. This script prices the difference: a variant
cost model charging d layers per entangling gate (the qubit's
controlled-phase is a single two-pulse MS gate and stays at 1), and

  (a) re-bisects the critical inflation factor f* for the pairings the
      paper quotes -- the marginal depolarizing/ion d = 3 cell and its
      d = 5 sibling, plus the ladder cells;
  (b) recomputes the measured Hrmo inflation factor under the same
      accounting (the native gate charged L = d layers, not d - 1):
      f moves down because the heavier charge absorbs more of the
      measured infidelity.

The referee question is which moves faster. Demo instance (N = 21, a = 2,
r = 6), exact density matrices.

Writes results/ion_2d_fstar.json. Run: python3 ion_2d_fstar.py
"""

import json
import math
import os
import time
from concurrent.futures import ProcessPoolExecutor

import numpy as np

import qudit_shor
from hrmo_reanalysis import uniform_floor, N, A
from qudit_shor import multiplicative_order, noise_superop, shor_run

qudit_shor.GATE_COST_MODELS["ion2d"] = (
    lambda d: 1.0, lambda d: (1.0 if d == 2 else float(d)))

S2 = {"transmon_cal": 0.003, "depolarizing": 0.005}
QUDITS = [3, 5]
FACTORS = [0.5, 0.75, 1.0, 1.25, 1.5, 1.75, 2.0, 2.5, 3.0]
HRMO_EPS = {2: (0.004, 0.001), 3: (0.013, 0.002), 5: (0.063, 0.003)}

RESULTS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results")


def ladder_damage(d: int) -> float:
    s = 1e-6
    E = noise_superop(d, "transmon_cal", s)
    return (1.0 - float(np.real(np.trace(E))) / d ** 2) / s


def one(args):
    d, model, s, cost = args
    t0 = time.time()
    res = (shor_run(d, a=A, N=N, cost_model="uniform") if model is None
           else shor_run(d, model, s, a=A, N=N, cost_model=cost))
    return {"d": d, "model": model, "strength": s, "cost": cost,
            "success": float(res["success"]),
            "elapsed_s": round(time.time() - t0, 1)}


def main():
    os.makedirs(RESULTS, exist_ok=True)
    r = multiplicative_order(A, N)
    delta = {d: ladder_damage(d) for d in (2, 3, 5)}

    # measured f under the 2d accounting: qudit gate charged L = d layers,
    # the d = 2 gate L = 1 (one two-pulse MS gate)
    f_meas = {}
    for chan, dam in (("transmon_cal", delta), ("depolarizing", None)):
        for d in QUDITS:
            dam2 = delta[2] if chan == "transmon_cal" else 0.75
            damd = delta[d] if chan == "transmon_cal" else 1 - 1 / d ** 2
            eps_d, sig_d = HRMO_EPS[d]
            eps_2, sig_2 = HRMO_EPS[2]
            f = (eps_d / (2 * d * damd)) / (eps_2 / (2 * 1 * dam2))
            rel = math.sqrt((sig_d / eps_d) ** 2 + (sig_2 / eps_2) ** 2)
            f_meas[f"{chan}/d{d}"] = (f, f * rel)
            print(f"measured f under 2d, {chan} d={d}: "
                  f"{f:.2f} +/- {f * rel:.2f}")

    floors = {d: uniform_floor(d, r) for d in (2, 3, 5)}
    jobs = [(2, None, 0.0, "uniform"), (3, None, 0.0, "uniform"),
            (5, None, 0.0, "uniform")]
    for chan, s2 in S2.items():
        jobs.append((2, chan, s2, "ion"))     # qubit anchor (d=2 unchanged)
        for d in QUDITS:
            for fct in FACTORS:
                jobs.append((d, chan, s2 * fct, "ion2d"))
    jobs = list(dict.fromkeys(jobs))
    print(f"{len(jobs)} exact-DM runs", flush=True)
    t0 = time.time()
    with ProcessPoolExecutor(max_workers=4) as ex:
        runs = list(ex.map(one, jobs))
    print(f"grid done in {time.time() - t0:.0f} s", flush=True)
    res = {tuple(j): x["success"] for j, x in zip(jobs, runs)}
    base = {d: res[(d, None, 0.0, "uniform")] for d in (2, 3, 5)}

    def signal(d, succ):
        return (succ - floors[d]) / (base[d] - floors[d])

    rows = []
    for chan, s2 in S2.items():
        sig2 = signal(2, res[(2, chan, s2, "ion")])
        for d in QUDITS:
            sigs = [signal(d, res[(d, chan, s2 * fct, "ion2d")])
                    for fct in FACTORS]
            diff = np.asarray(sigs) - sig2
            fstar = None
            for i in range(1, len(FACTORS)):
                if diff[i - 1] >= 0 > diff[i]:
                    t = diff[i - 1] / (diff[i - 1] - diff[i])
                    fstar = FACTORS[i - 1] + t * (FACTORS[i] - FACTORS[i - 1])
                    break
            f, fs = f_meas[f"{chan}/d{d}"]
            f_lo = max(f - fs, 0.0)
            i_near = min(range(len(FACTORS)),
                         key=lambda i: abs(FACTORS[i] - f))
            sig_at_f = sigs[i_near]
            verdict = ("SURVIVES" if f <= (fstar or 99) else "LOST")
            rows.append({"channel": chan, "d": d, "qubit_signal": sig2,
                         "f_star_2d": fstar, "f_measured_2d": f,
                         "f_measured_sigma": fs,
                         "f_measured_1d": None,
                         "signal_at_nearest_f": sig_at_f,
                         "nearest_factor": FACTORS[i_near],
                         "sweep": dict(zip([str(x) for x in FACTORS], sigs)),
                         "verdict": verdict})
            print(f"{chan} d={d}: f* {fstar if fstar else '>3'}  "
                  f"f_meas {f:.2f}+/-{fs:.2f}  -> {verdict} "
                  f"(signal at f={FACTORS[i_near]}: {sig_at_f:.3f} "
                  f"vs {sig2:.3f})")

    out = {"N": N, "a": A, "r": r, "s2": S2, "factors": FACTORS,
           "delta": {str(k): v for k, v in delta.items()},
           "floors": {str(k): v for k, v in floors.items()},
           "noiseless": {str(k): v for k, v in base.items()},
           "note": "ion2d charges the qudit entangler d layers; the "
                   "qubit entangler stays at 1 (single two-pulse MS gate)",
           "rows": rows, "runs": runs}
    path = os.path.join(RESULTS, "ion_2d_fstar.json")
    with open(path, "w") as fh:
        json.dump(out, fh, indent=1)
    print(f"\nwrote {path}")


if __name__ == "__main__":
    main()
