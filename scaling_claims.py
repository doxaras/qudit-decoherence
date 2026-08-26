"""Recompute every size-scaling number the paper quotes, from the runs.

The slopes, R^2 values, plateau chi^2 and sigma gaps in
Sec.~\\ref{sec:scaling} were originally produced by ad-hoc analysis
rather than a committed script, which made them impossible to
regenerate after the seeding fix re-rolled every Monte Carlo stream.
This script is that missing step: it merges the sweeps exactly as
plots_scaling_fair.py does (override on (d, m, regime), so a
re-measurement replaces rather than double-counts), fits the signal
against precision in bits, and prints the results in the form the
manuscript quotes them.

Pass a directory to score a different tree, e.g.

    python3 scaling_claims.py results_prehash

which is how the fit convention below was pinned: unweighted least
squares reproduces the published slopes, weighted does not, so
unweighted is what the paper means and what is reported first. Both are
printed, because the two disagree by more than their error bars
wherever the error bars vary strongly across sizes.

Run: python3 scaling_claims.py [results_dir]
Writes <results_dir>/scaling_claims.json
"""

import glob
import json
import math
import os
import sys

import numpy as np

ROOT = os.path.dirname(os.path.abspath(__file__))
REGIMES = ["depolarizing", "transmon", "transmon_cal",
           "transmon_cal_lowcharge"]


def load(resdir):
    """Merge the main sweep with any deeper single-point measurements."""
    main = os.path.join(resdir, "scaling_fair_1000.json")
    if not os.path.exists(main):
        main = os.path.join(resdir, "scaling_fair.json")
    with open(main) as f:
        data = json.load(f)
    runs, bl = list(data["runs"]), dict(data["baselines"])

    extra = [os.path.join(resdir, "scaling_fair_m8.json")]
    extra += sorted(glob.glob(os.path.join(resdir, "scaling_fair_d*_m*.json")))
    for path in extra:
        if not os.path.exists(path):
            continue
        with open(path) as f:
            sup = json.load(f)
        bl[f"{sup['d']},{sup['m']}"] = sup["baseline"]
        gone = {(r["d"], r["m"], r["regime"]) for r in sup["runs"]}
        runs = [r for r in runs if (r["d"], r["m"], r["regime"]) not in gone]
        runs += sup["runs"]
    return runs, bl


def series(runs, bl, regime, d):
    out = []
    for r in runs:
        if r["regime"] != regime or r["d"] != d:
            continue
        span = bl[f"{r['d']},{r['m']}"]["success"] - r["floor"]
        out.append({"m": r["m"], "bits": r["m"] * math.log2(d),
                    "signal": (r["success"] - r["floor"]) / span,
                    "err": r["stderr"] / span})
    return sorted(out, key=lambda p: p["m"])


def fit(pts, weighted):
    """Least-squares line, with the slope standard error and R^2."""
    x = np.array([p["bits"] for p in pts])
    y = np.array([p["signal"] for p in pts])
    w = (1.0 / np.array([p["err"] for p in pts]) ** 2 if weighted
         else np.ones(len(pts)))
    S, Sx, Sy = w.sum(), (w * x).sum(), (w * y).sum()
    Sxx, Sxy = (w * x * x).sum(), (w * x * y).sum()
    det = S * Sxx - Sx ** 2
    b = (S * Sxy - Sx * Sy) / det
    a = (Sxx * Sy - Sx * Sxy) / det
    resid = y - (a + b * x)
    if weighted:
        se = math.sqrt(S / det)
    else:
        # unweighted: scale by the residual variance, the usual OLS bar
        dof = max(len(pts) - 2, 1)
        se = math.sqrt((w * resid ** 2).sum() / dof * S / det)
    ybar = Sy / S
    ss_res, ss_tot = (w * resid ** 2).sum(), (w * (y - ybar) ** 2).sum()
    return {"slope": float(b), "slope_se": float(se), "intercept": float(a),
            "r2": float(1 - ss_res / ss_tot), "n": len(pts)}


def plateau_chi2(pts):
    y = np.array([p["signal"] for p in pts])
    e = np.array([p["err"] for p in pts])
    w = 1 / e ** 2
    ybar = (w * y).sum() / w.sum()
    c2 = float((w * (y - ybar) ** 2).sum())
    dof = len(pts) - 1
    from scipy.stats import chi2
    return {"chi2": c2, "dof": dof, "chi2_per_dof": c2 / dof,
            "p_low_tail": float(chi2.cdf(c2, dof)),
            "spread": float(y.max() - y.min()),
            "range": [float(y.min()), float(y.max())]}


def gap(pts, m_lo, m_hi):
    a = next(p for p in pts if p["m"] == m_lo)
    b = next(p for p in pts if p["m"] == m_hi)
    delta = a["signal"] - b["signal"]
    sd = math.hypot(a["err"], b["err"])
    return {"from_bits": a["bits"], "to_bits": b["bits"], "delta": delta,
            "sigma": sd, "n_sigma": delta / sd,
            "hi_value": b["signal"], "hi_err": b["err"]}


def main():
    resdir = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "results")
    if not os.path.isabs(resdir):
        resdir = os.path.join(ROOT, resdir)
    runs, bl = load(resdir)
    out = {"results_dir": resdir, "slopes": {}, "plateau": {}, "gaps": {}}

    print(f"=== size-scaling claims from {os.path.basename(resdir)} ===\n")
    for regime in REGIMES:
        rows = []
        for d in (2, 3, 5):
            pts = series(runs, bl, regime, d)
            if len(pts) < 3:
                continue
            u, w = fit(pts, False), fit(pts, True)
            out["slopes"][f"{regime}_{d}"] = {"unweighted": u, "weighted": w,
                                              "points": pts}
            rows.append((d, u, w, pts))
        if not rows:
            continue
        print(f"-- {regime} --")
        for d, u, w, pts in rows:
            print(f"   d={d}: slope {u['slope']:+.3f}+-{u['slope_se']:.3f}/bit "
                  f"(R^2={u['r2']:.2f}, n={u['n']})   "
                  f"[weighted {w['slope']:+.3f}+-{w['slope_se']:.3f}, "
                  f"R^2={w['r2']:.2f}]")
            print("        " + "  ".join(
                f"{p['bits']:.1f}b {p['signal']:.3f}+-{p['err']:.3f}"
                for p in pts))
        print()

    out["crossings"] = {}
    for regime in REGIMES:
        k3, k5 = f"{regime}_3", f"{regime}_5"
        if k3 not in out["slopes"] or k5 not in out["slopes"]:
            continue
        entry = {}
        for conv in ("unweighted", "weighted"):
            f3 = out["slopes"][k3][conv]
            f5 = out["slopes"][k5][conv]
            if f3["slope"] == f5["slope"]:
                continue
            x = (f5["intercept"] - f3["intercept"]) / (f3["slope"] - f5["slope"])
            entry[conv] = x
        bits5 = [p["bits"] for p in out["slopes"][k5]["points"]]
        entry["ququint_max_bits"] = max(bits5)
        out["crossings"][regime] = entry
        print(f"-- {regime}, d=3/d=5 fitted-line crossing --")
        for conv in ("unweighted", "weighted"):
            if conv in entry:
                tag = (" (extrapolated past ququint data)"
                       if entry[conv] > entry["ququint_max_bits"] else "")
                print(f"   {conv}: {entry[conv]:.2f} bits{tag}")
        print()

    for regime in ("transmon_cal", "depolarizing"):
        pts = series(runs, bl, regime, 3)
        if len(pts) < 3:
            continue
        pl = plateau_chi2(pts[:3])
        out["plateau"][regime] = pl
        print(f"-- {regime}, d=3 plateau (first three sizes) --")
        print(f"   {pl['range'][0]:.3f}-{pl['range'][1]:.3f}, spread "
              f"{pl['spread']:.4f}; chi^2/dof = {pl['chi2_per_dof']:.4f} "
              f"({pl['dof']} dof), lower-tail p = {pl['p_low_tail']:.4f}")
        have = {p["m"] for p in pts}
        for lo, hi in ((6, 9), (6, 8)):
            if {lo, hi} <= have:
                g = gap(pts, lo, hi)
                out["gaps"][f"{regime}_{lo}_{hi}"] = g
                print(f"   drop {g['from_bits']:.1f} -> {g['to_bits']:.1f} "
                      f"bits: {g['delta']:.4f} +- {g['sigma']:.4f} = "
                      f"{g['n_sigma']:.2f} sigma "
                      f"(endpoint {g['hi_value']:.3f}+-{g['hi_err']:.3f})")
        print()

    path = os.path.join(resdir, "scaling_claims.json")
    with open(path, "w") as f:
        json.dump(out, f, indent=1)
    print(f"wrote {path}")


if __name__ == "__main__":
    main()
