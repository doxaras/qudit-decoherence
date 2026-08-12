"""Exact continued-fraction acceptance set vs register size and order.

Tests the decoder-tolerance account of paper Sec. VI C directly, instead
of leaving it at a back-of-envelope. The account says: continued-fraction
recovery accepts any outcome y whose phase y/D lies within 1/(2r^2) of
some s/r, so the acceptance window around each of the r-1 peaks holds
~D/(2r^2) outcomes while the noiseless peak stays ~1 outcome wide. Two
falsifiable predictions follow:

  (a) at fixed order r, the acceptance set grows linearly in D
      -- this is the redundancy that outruns the added exposure;
  (b) at fixed D, the per-peak window shrinks as 1/r^2
      -- so a larger order is decoded far less tolerantly.

Note on the constant: the convergent guarantee gives a half-width of
1/(2r^2) on each side of s/r, hence a full window of 1/r^2 in phase and
D/r^2 outcomes. The paper's Sec. VI C quotes D/(2r^2), which is the
half-window; the measurements below use the full window D/r^2.

Prediction (b) is only meaningful where the window is wider than one
outcome, i.e. D >> r^2 -- below that the continuum picture cannot apply,
and the r = 10 instances at demo size sit exactly there (D = 64 < 100).
Part (c) therefore sweeps the register size for the fixed-modulus pairs.

Both are measured here exactly, by running the project's own decoder
(qudit_shor.recovered_order) over every outcome y in [0, D). No
simulation and no sampling is involved: this is the classical
post-processing layer alone, so it costs seconds.

Prediction (b) needs r varied at fixed register, which is what the
within-modulus pairs of docs/GRID_ALIGNMENT.md provide (N = 33 and
N = 55 each host r = 5 and r = 10 on identical registers).

Writes results/decoder_scaling.json. Run: python3 decoder_scaling.py
"""

import json
import os

import numpy as np

from qudit_shor import multiplicative_order, recovered_order, shor_config

RESULTS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results")

# Register-size sweep of paper Fig. 3, on the unbiased benchmark instance.
SWEEP = {2: [6, 8, 10, 12], 3: [4, 5, 6, 7], 5: [3, 4, 5]}
SCALING_INSTANCE = (21, 2)

# Within-modulus pairs: identical registers, different order.
FIXED_D_PAIRS = [(33, 4), (33, 2), (55, 16), (55, 4)]


def acceptance(D: int, a: int, N: int, r: int) -> int:
    """Number of outcomes in [0, D) that decode to the true order r."""
    return sum(1 for y in range(D) if recovered_order(y, D, a, N) == r)


def loglog_slope(x, y):
    x, y = np.log(np.asarray(x, float)), np.log(np.asarray(y, float))
    n = len(x)
    A = np.vstack([x, np.ones(n)]).T
    coef, *_ = np.linalg.lstsq(A, y, rcond=None)
    resid = y - A @ coef
    ss_res, ss_tot = np.sum(resid ** 2), np.sum((y - y.mean()) ** 2)
    r2 = 1 - ss_res / ss_tot if ss_tot > 0 else float("nan")
    dof = n - 2
    cov = (ss_res / dof) * np.linalg.inv(A.T @ A) if dof > 0 else None
    sig = float(np.sqrt(cov[0, 0])) if cov is not None else float("nan")
    return float(coef[0]), sig, float(r2)


def main():
    out = {}

    # --- (a) fixed r, growing D -------------------------------------------
    N, a = SCALING_INSTANCE
    r = multiplicative_order(a, N)
    print(f"(a) Acceptance vs register size: N = {N}, a = {a}, r = {r}")
    print(f"{'d':>2} {'m':>3} {'D':>6} {'|A|':>6} {'|A|/D':>8} "
          f"{'per peak':>9} {'D/r^2':>8} {'ratio':>6}")
    rows = []
    for d, ms in SWEEP.items():
        for m in ms:
            D = d ** m
            A = acceptance(D, a, N, r)
            per_peak, pred = A / (r - 1), D / r ** 2
            rows.append({"d": d, "m": m, "D": D, "accepted": A,
                         "fraction": A / D, "per_peak": per_peak,
                         "predicted_per_peak": pred,
                         "measured_over_predicted": per_peak / pred})
            print(f"{d:>2} {m:>3} {D:>6} {A:>6} {A / D:>8.4f} "
                  f"{per_peak:>9.1f} {pred:>8.1f} {per_peak / pred:>6.2f}")
    slope, sig, r2 = loglog_slope([x["D"] for x in rows],
                                  [x["accepted"] for x in rows])
    print(f"\n  log-log slope of |A| vs D: {slope:.3f} +/- {sig:.3f} "
          f"(R^2 = {r2:.4f});  prediction: 1.0")
    out["vs_size"] = {"N": N, "a": a, "r": r, "rows": rows,
                      "loglog_slope": slope, "loglog_slope_err": sig,
                      "loglog_r2": r2, "predicted_slope": 1.0}

    # --- (b) fixed D and register, varying r ------------------------------
    print("\n(b) Acceptance vs order at FIXED register:")
    print(f"{'N':>3} {'a':>3} {'r':>3} {'d':>2} {'m':>3} {'D':>6} "
          f"{'|A|':>6} {'per peak':>9} {'D/(2r^2)':>9}")
    pair_rows = []
    for N2, a2 in FIXED_D_PAIRS:
        r2_ord = multiplicative_order(a2, N2)
        for d in (2, 3, 5):
            m, w = shor_config(d, N2)
            D = d ** m
            A = acceptance(D, a2, N2, r2_ord)
            pair_rows.append({"N": N2, "a": a2, "r": r2_ord, "d": d, "m": m,
                              "D": D, "accepted": A,
                              "per_peak": A / (r2_ord - 1),
                              "predicted_per_peak": D / (2 * r2_ord ** 2)})
            print(f"{N2:>3} {a2:>3} {r2_ord:>3} {d:>2} {m:>3} {D:>6} "
                  f"{A:>6} {A / (r2_ord - 1):>9.2f} "
                  f"{D / (2 * r2_ord ** 2):>9.2f}")

    print("\n  r = 5 vs r = 10 at identical register "
          "(prediction: per-peak ratio = 4.0):")
    ratios = []
    for N2 in (33, 55):
        for d in (2, 3, 5):
            lo = [x for x in pair_rows if x["N"] == N2 and x["d"] == d
                  and x["r"] == 5][0]
            hi = [x for x in pair_rows if x["N"] == N2 and x["d"] == d
                  and x["r"] == 10][0]
            ratio = lo["per_peak"] / hi["per_peak"]
            ratios.append(ratio)
            print(f"    N = {N2}, d = {d}, D = {lo['D']}: "
                  f"{lo['per_peak']:.2f} vs {hi['per_peak']:.2f} "
                  f"-> {ratio:.2f}x")
    print(f"    mean ratio {np.mean(ratios):.2f}x "
          f"(range {min(ratios):.2f}-{max(ratios):.2f})")
    print("    NOTE: at D = 64-125 the r = 10 window is narrower than one "
          "outcome\n          (D < r^2), so the continuum picture cannot "
          "apply here -- see (c).")
    out["vs_order"] = {"rows": pair_rows, "per_peak_ratios": ratios,
                       "mean_ratio": float(np.mean(ratios)),
                       "predicted_ratio": 4.0,
                       "caveat": "demo size sits at D < r^2 for r = 10"}

    # --- (c) the same ratio as the register grows into D >> r^2 -----------
    print("\n(c) Per-peak window ratio r=5 : r=10 as the register grows")
    print(f"{'d':>2} {'m':>3} {'D':>6} {'D/r^2 (r=10)':>13} "
          f"{'peak r=5':>9} {'peak r=10':>10} {'ratio':>6}")
    conv_rows = []
    for d, ms in SWEEP.items():
        for m in ms:
            D = d ** m
            lo = acceptance(D, 4, 33, 5) / 4      # N = 33, a = 4  -> r = 5
            hi = acceptance(D, 2, 33, 10) / 9     # N = 33, a = 2  -> r = 10
            ratio = lo / hi if hi > 0 else float("nan")
            conv_rows.append({"d": d, "m": m, "D": D, "peak_r5": lo,
                              "peak_r10": hi, "ratio": ratio,
                              "window_r10": D / 100})
            print(f"{d:>2} {m:>3} {D:>6} {D / 100:>13.2f} "
                  f"{lo:>9.2f} {hi:>10.2f} {ratio:>6.2f}")
    deep = [x for x in conv_rows if x["window_r10"] >= 5]
    if deep:
        vals = [x["ratio"] for x in deep]
        print(f"\n  restricted to D >= 5 r^2 (n = {len(deep)}): "
              f"mean ratio {np.mean(vals):.2f}x "
              f"(range {min(vals):.2f}-{max(vals):.2f}); prediction 4.0")
    out["vs_order_converged"] = {
        "rows": conv_rows,
        "deep_mean_ratio": float(np.mean([x["ratio"] for x in deep]))
        if deep else None,
        "deep_n": len(deep), "predicted_ratio": 4.0}

    # --- (d) where the 1/r^2 form goes wrong ------------------------------
    # Continued fractions accept any convergent denominator q that is a
    # multiple of r with q <= N (then reduce to the true order), so the
    # count of admissible denominators, floor(N/r), carries its own
    # r-dependence that the single-peak estimate omits.
    print("\n(d) Deviation from (r-1) D / r^2 vs the number of admissible")
    print("    convergent denominators floor(N/r), at D = 4096:")
    print(f"{'N':>3} {'a':>3} {'r':>3} {'floor(N/r)':>10} {'|A|/D':>8} "
          f"{'(r-1)/r^2':>10} {'ratio':>6}")
    D = 4096
    diag = []
    for N2, a2 in [(21, 2), (33, 4), (33, 2), (55, 16), (55, 4), (29, 16)]:
        r2_ord = multiplicative_order(a2, N2)
        frac = acceptance(D, a2, N2, r2_ord) / D
        simple = (r2_ord - 1) / r2_ord ** 2
        diag.append({"N": N2, "a": a2, "r": r2_ord,
                     "n_denominators": N2 // r2_ord, "fraction": frac,
                     "simple_prediction": simple, "ratio": frac / simple})
        print(f"{N2:>3} {a2:>3} {r2_ord:>3} {N2 // r2_ord:>10} {frac:>8.4f} "
              f"{simple:>10.4f} {frac / simple:>6.2f}")
    cc = np.corrcoef([x["n_denominators"] for x in diag],
                     [x["ratio"] for x in diag])[0, 1]
    print(f"\n  correlation(floor(N/r), deviation) = {cc:.3f}")
    out["denominator_diagnostic"] = {"D": D, "rows": diag,
                                     "correlation": float(cc)}

    path = os.path.join(RESULTS, "decoder_scaling.json")
    with open(path, "w") as f:
        json.dump(out, f, indent=1)
    print(f"\nwrote {path}")


if __name__ == "__main__":
    main()
