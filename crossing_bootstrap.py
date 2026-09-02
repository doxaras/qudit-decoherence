"""Parametric bootstrap for the d=3 / d=5 scaling-crossing estimates.

Regenerates results/crossing_bootstrap.json, the file behind the paper's
"7.7 bits (68% CI 7.0-8.3)" and "14.7 bits (13.1-17.6)" crossing quotes
(Sec. V; secular-channel values -- the pre-revision collective channel
gave 8.7 [8.0-9.2]). Procedure, per noise regime:

  1. Take the per-size points (bits_i, signal_i, err_i) of the d=3 and
     d=5 slope families from results/scaling_claims.json.
  2. Draw signal_i* ~ N(signal_i, err_i) independently for every point.
  3. Refit both lines by 1/err^2-weighted least squares (the "weighted"
     variant of scaling_claims.json -- the variant the paper quotes).
  4. Solve for the crossing in bits; keep draws with a finite crossing.
  5. Repeat N_BOOT times; report median and the 16th/84th percentiles.

The point estimates equal the weighted crossings already recorded in
scaling_claims.json; this file adds only the uncertainty. Caveat carried
from the paper: the d=3 family is a plateau-then-fall, not a line
(weighted R^2 0.38-0.71), so the crossing inherits the linear reading
of that family.
"""

import json
import os

import numpy as np

N_BOOT = 6000
SEED = 20260831
REGIMES = ("transmon_cal", "depolarizing")
RESULTS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results")


def weighted_fit(bits, sig, err):
    w = 1.0 / np.asarray(err) ** 2
    b = np.asarray(bits, dtype=float)
    s = np.asarray(sig, dtype=float)
    W = w.sum()
    xb = (w * b).sum() / W
    sb = (w * s).sum() / W
    cov = (w * (b - xb) * (s - sb)).sum()
    var = (w * (b - xb) ** 2).sum()
    slope = cov / var
    return slope, sb - slope * xb


def crossing(p3, p5, rng=None):
    def draw(pts):
        sig = np.array([p["signal"] for p in pts])
        err = np.array([p["err"] for p in pts])
        if rng is not None:
            sig = rng.normal(sig, err)
        return [p["bits"] for p in pts], sig, err

    a3, b3 = weighted_fit(*draw(p3))
    a5, b5 = weighted_fit(*draw(p5))
    if a3 == a5:
        return np.nan
    return (b3 - b5) / (a5 - a3)


def main():
    claims = json.load(open(os.path.join(RESULTS, "scaling_claims.json")))
    rng = np.random.default_rng(SEED)
    out = {}
    for regime in REGIMES:
        p3 = claims["slopes"][f"{regime}_3"]["points"]
        p5 = claims["slopes"][f"{regime}_5"]["points"]
        point = crossing(p3, p5)
        draws = np.array([crossing(p3, p5, rng) for _ in range(N_BOOT)])
        draws = draws[np.isfinite(draws)]
        out[regime] = {
            "n": N_BOOT,
            "point_weighted": point,
            "median": float(np.median(draws)),
            "lo68": float(np.percentile(draws, 16)),
            "hi68": float(np.percentile(draws, 84)),
        }
        print(f"{regime}: point {point:.2f}, median {out[regime]['median']:.2f} "
              f"[{out[regime]['lo68']:.2f}, {out[regime]['hi68']:.2f}]")
    with open(os.path.join(RESULTS, "crossing_bootstrap.json"), "w") as f:
        json.dump(out, f, indent=1)


if __name__ == "__main__":
    main()
