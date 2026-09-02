"""Recompute every N=29 instance-robustness number the paper quotes.

The "Instance robustness" paragraph of Sec.~V quotes slopes, matched-range
comparisons, and a d=3/d=5 crossing on the second unbiased instance
(N = 29, a = 16, r = 7) that were produced by ad-hoc analysis of
results/scaling_fair_n29.json rather than a committed script -- the same
provenance gap scaling_claims.py closed for the N = 21 sweep. This script
is that missing step for N = 29. Fit conventions (weighted least squares,
signal = (success - floor) / (baseline - floor), bits = m log2 d) are
imported from scaling_claims.py so the two instances cannot drift apart.

Quantities reproduced (manuscript wording in Sec.~V):
  * full-range weighted slopes per regime and base on N = 29;
  * the d = 3 / d = 5 fitted-line crossing per regime on N = 29
    ("recurs at 9.3 bits"; no crossing under depolarizing);
  * matched-size-range slope pairs against the N = 21 sweep
    (d = 2 full range; d = 3 restricted to m = 4..7; d = 5 to m = 3..5).

Run: python3 n29_claims.py
Writes results/n29_claims.json
"""

import json
import math
import os

from scaling_claims import fit, load, series

ROOT = os.path.dirname(os.path.abspath(__file__))
REGIMES = ["depolarizing", "transmon", "transmon_cal",
           "transmon_cal_lowcharge"]
BASES = [2, 3, 5]
# common m-range between the two instances' sweeps
MATCHED_M = {2: (6, 12), 3: (4, 7), 5: (3, 5)}


def load_n29(resdir):
    with open(os.path.join(resdir, "scaling_fair_n29.json")) as f:
        data = json.load(f)
    return data["runs"], data["baselines"]


def restrict(pts, m_lo, m_hi):
    return [p for p in pts if m_lo <= p["m"] <= m_hi]


def crossing(fit3, fit5):
    if fit3["slope"] == fit5["slope"]:
        return None
    return (fit5["intercept"] - fit3["intercept"]) / (
        fit3["slope"] - fit5["slope"])


def main():
    resdir = os.path.join(ROOT, "results")
    runs29, bl29 = load_n29(resdir)
    runs21, bl21 = load(resdir)

    out = {"N": 29, "a": 16, "r": 7, "regimes": {}}
    for regime in REGIMES:
        block = {"full_range": {}, "matched_range": {}}
        fits29 = {}
        for d in BASES:
            pts29 = series(runs29, bl29, regime, d)
            if not pts29:
                continue
            fits29[d] = fit(pts29, weighted=True)
            block["full_range"][str(d)] = fits29[d]
            m_lo, m_hi = MATCHED_M[d]
            f29 = fit(restrict(pts29, m_lo, m_hi), weighted=True)
            f21 = fit(restrict(series(runs21, bl21, regime, d), m_lo, m_hi),
                      weighted=True)
            block["matched_range"][str(d)] = {
                "m_range": [m_lo, m_hi], "n29": f29, "n21": f21,
                "n_sigma": abs(f29["slope"] - f21["slope"]) / math.hypot(
                    f29["slope_se"], f21["slope_se"])}
        if 3 in fits29 and 5 in fits29:
            x = crossing(fits29[3], fits29[5])
            # a crossing behind the smallest size means the lines diverge
            # over the measured range (d=3 never overtakes d=5, or leads
            # throughout); quote it but flag it
            block["d3_d5_crossing_bits"] = x
            block["crossing_in_range"] = bool(
                x is not None and x >= min(p["bits"] for p in series(
                    runs29, bl29, regime, 5)))
        out["regimes"][regime] = block

        print(f"-- {regime} (N=29) --", flush=True)
        for d in BASES:
            if str(d) not in block["full_range"]:
                continue
            f = block["full_range"][str(d)]
            mr = block["matched_range"][str(d)]
            print(f"   d={d}: slope {f['slope']:+.4f}+-{f['slope_se']:.4f}"
                  f"/bit (R^2={f['r2']:.2f}, n={f['n']})   matched m="
                  f"{mr['m_range']}: N29 {mr['n29']['slope']:+.4f}"
                  f"+-{mr['n29']['slope_se']:.4f} vs N21 "
                  f"{mr['n21']['slope']:+.4f}+-{mr['n21']['slope_se']:.4f} "
                  f"({mr['n_sigma']:.1f} sigma)", flush=True)
        if "d3_d5_crossing_bits" in block:
            x = block["d3_d5_crossing_bits"]
            tag = "" if block["crossing_in_range"] else "  [out of range]"
            print(f"   d3/d5 crossing: {x:.2f} bits{tag}", flush=True)

    path = os.path.join(resdir, "n29_claims.json")
    with open(path, "w") as f:
        json.dump(out, f, indent=1)
    print(f"wrote {path}", flush=True)


if __name__ == "__main__":
    main()
