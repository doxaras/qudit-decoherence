"""Is the partial exposure collapse a physics failure or a units failure?

docs/GROVER.md section 5 reports that signal = A*exp(-k*exposure*strength)
does not collapse Grover and Shor onto one curve: R^2 = 0.72 (ladder),
0.44 (per-particle). But exposure*strength counts noise *events*, not
*damage*: one depolarizing event costs a pure state p*(1-1/d) fidelity --
0.5p for a qubit, 0.8p for a ququint -- and one ladder layer's damage
depends on d through the level-dependent decay rates. A d-dependent
per-event damage inside an exponential is exactly the kind of thing that
scatters bases off a shared curve without any new physics.

This script re-fits the existing points (results/grover.json and
results/scaling_fair.json -- no new simulation) with the abscissa in
damage units, computed exactly from the noise superoperator:

  F_e(d, model, s) = tr(S)/d^2        entanglement fidelity per carrier-layer
  X0 = carriers * layers * s          (original, event units)
  X1 = carriers * layers * (1 - F_e)  (per-event entanglement infidelity)
  X2 = carriers * layers * d/(d+1)*(1-F_e)   (average-fidelity infidelity)
  X3 = carriers * layers * (-ln F_e)  (semigroup rate, composition-exact)

plus two diagnostics that classify whatever residual remains:
  * per-(algorithm, d) log-linear fits -- if families are straight lines
    with different slopes, the failure is a rate factor (units); if the
    lines are curved, the single-exponential ansatz itself is wrong;
  * nested fits (shared vs per-algorithm A and k) -- locates any remaining
    algorithm split in the prefactor or the decay rate.

Writes results/exposure_collapse.json. Run: python3 exposure_collapse.py
"""

import json
import os
import sys

# Optional results directory, so the same fit can be run against an
# archived tree (e.g. results_prehash/) to check what a re-run moved.
RES = sys.argv[1] if len(sys.argv) > 1 else "results"


def _scaling_fair_path():
    p = os.path.join(RES, "scaling_fair_1000.json")
    return p if os.path.exists(p) else os.path.join(RES, "scaling_fair.json")


import numpy as np
from scipy.optimize import curve_fit

from qudit_shor import noise_superop

REGIMES = [("transmon_cal", 0.003), ("depolarizing", 0.005)]


# ----------------------------------------------------------------------
# data: pool Grover scaling points with Shor fair-scaling points
# ----------------------------------------------------------------------

def load_points():
    pts = []
    g = json.load(open(os.path.join(RES, "grover.json")))
    for r in g["scaling"]:
        pts.append(dict(alg="grover", d=r["d"], bits=r["bits"],
                        model=r["noise_model"], strength=r["strength"],
                        exposure=r["n_qudits"] * r["n_layers"],
                        signal=r["signal"]))
    s = json.load(open(_scaling_fair_path()))
    for r in s["runs"]:
        if r["regime"] not in ("transmon_cal", "depolarizing"):
            continue
        pts.append(dict(alg="shor", d=r["d"], bits=r["m"] * np.log2(r["d"]),
                        model=r["noise_model"], strength=r["strength"],
                        exposure=r["n_qudits"] * r["n_layers"],
                        signal=r["signal"]))
    return pts


# ----------------------------------------------------------------------
# damage units from the actual channel
# ----------------------------------------------------------------------

def ent_fidelity(d: int, model: str, strength: float) -> float:
    """F_e = tr(S)/d^2 = sum_k |tr K_k|^2 / d^2, exact for any Kraus rep."""
    S = noise_superop(d, model, strength)
    return float(np.trace(S).real) / d**2


def abscissas(p):
    Fe = ent_fidelity(p["d"], p["model"], p["strength"])
    d = p["d"]
    return {
        "X0_event": p["exposure"] * p["strength"],
        "X1_ent_infid": p["exposure"] * (1.0 - Fe),
        "X2_avg_infid": p["exposure"] * (d / (d + 1)) * (1.0 - Fe),
        "X3_rate": p["exposure"] * (-np.log(Fe)),
    }


# ----------------------------------------------------------------------
# fits
# ----------------------------------------------------------------------

def r_squared(y, yhat):
    y, yhat = np.asarray(y), np.asarray(yhat)
    return 1.0 - np.sum((y - yhat) ** 2) / np.sum((y - np.mean(y)) ** 2)


def fit_exp(x, y):
    """signal = A*exp(-k*x), linear-domain least squares (as the original)."""
    x, y = np.asarray(x, float), np.asarray(y, float)
    pos = y > 0
    k0 = 0.3
    if pos.sum() >= 2:
        slope = np.polyfit(x[pos], np.log(y[pos]), 1)[0]
        k0 = max(-slope, 1e-6)
    (A, k), _ = curve_fit(lambda x, A, k: A * np.exp(-k * x), x, y,
                          p0=(max(y.max(), 1e-3), k0), maxfev=20000)
    yhat = A * np.exp(-k * x)
    return dict(A=A, k=k, r2=r_squared(y, yhat), resid=y - yhat)


def fit_nested(x, y, groups):
    """Shared/split A and k across algorithm groups, pooled R^2."""
    x, y = np.asarray(x, float), np.asarray(y, float)
    gset = sorted(set(groups))
    gi = np.array([gset.index(g) for g in groups])
    base = fit_exp(x, y)
    out = {"shared_A_shared_k": {"r2": base["r2"], "n_params": 2}}

    def model_splitA(x_, Ag, As, k):
        A = np.where(gi == 0, Ag, As)
        return A * np.exp(-k * x_)

    def model_splitk(x_, A, kg, ks):
        k = np.where(gi == 0, kg, ks)
        return A * np.exp(-k * x_)

    p, _ = curve_fit(model_splitA, x, y, p0=(base["A"], base["A"], base["k"]),
                     maxfev=20000)
    out["per_alg_A_shared_k"] = {"r2": r_squared(y, model_splitA(x, *p)),
                                 "n_params": 3,
                                 "A": dict(zip(gset, p[:2])), "k": p[2]}
    p, _ = curve_fit(model_splitk, x, y, p0=(base["A"], base["k"], base["k"]),
                     maxfev=20000)
    out["shared_A_per_alg_k"] = {"r2": r_squared(y, model_splitk(x, *p)),
                                 "n_params": 3,
                                 "A": p[0], "k": dict(zip(gset, p[1:]))}
    # fully split = independent fits, pooled R^2
    yhat = np.empty_like(y)
    per = {}
    for i, gname in enumerate(gset):
        m = gi == i
        f = fit_exp(x[m], y[m])
        yhat[m] = f["A"] * np.exp(-f["k"] * x[m])
        per[gname] = {"A": f["A"], "k": f["k"], "r2_within": f["r2"]}
    out["per_alg_A_per_alg_k"] = {"r2": r_squared(y, yhat), "n_params": 4,
                                  "per_alg": per}
    return out


def family_diagnostics(x, y, fams):
    """Per-(alg,d) log-linear slope + curvature: rate failure vs shape failure."""
    x, y = np.asarray(x, float), np.asarray(y, float)
    rows = []
    for fam in sorted(set(fams)):
        m = np.array([f == fam for f in fams]) & (y > 0)
        if m.sum() < 3:
            rows.append(dict(family=fam, n=int(m.sum()), note="too few points"))
            continue
        ly = np.log(y[m])
        lin = np.polyfit(x[m], ly, 1)
        r2_lin = r_squared(ly, np.polyval(lin, x[m]))
        quad = np.polyfit(x[m], ly, 2)
        r2_quad = r_squared(ly, np.polyval(quad, x[m]))
        rows.append(dict(family=fam, n=int(m.sum()), k=-lin[0],
                         r2_loglinear=r2_lin, r2_logquad=r2_quad,
                         curvature=quad[0]))
    return rows


# ----------------------------------------------------------------------

def main():
    pts = load_points()
    report = {"n_points": len(pts), "per_event_infidelity": {}, "fits": {}}

    for model, s in REGIMES:
        for d in (2, 3, 5):
            Fe = ent_fidelity(d, model, s)
            report["per_event_infidelity"][f"{model},d={d}"] = {
                "F_e": Fe, "ent_infid": 1 - Fe, "rate": -np.log(Fe),
                "vs_strength": (1 - Fe) / s}

    for model, s in REGIMES:
        sub = [p for p in pts if p["model"] == model]
        y = [p["signal"] for p in sub]
        algs = [p["alg"] for p in sub]
        fams = [f"{p['alg']} d={p['d']}" for p in sub]
        xs = {name: [abscissas(p)[name] for p in sub]
              for name in abscissas(sub[0])}
        entry = {"n_points": len(sub), "abscissa": {}}
        for name, x in xs.items():
            f = fit_exp(x, y)
            med = {a: float(np.median(np.abs(f["resid"][np.array(algs) == a])))
                   for a in ("grover", "shor")}
            entry["abscissa"][name] = {
                "A": f["A"], "k": f["k"], "r2": round(f["r2"], 4),
                "median_abs_resid": med,
                "families": family_diagnostics(x, y, fams),
            }
        # nested fits on the original and the best damage-unit abscissa
        best = max(("X1_ent_infid", "X2_avg_infid", "X3_rate"),
                   key=lambda n: entry["abscissa"][n]["r2"])
        entry["best_damage_abscissa"] = best
        entry["nested"] = {
            "X0_event": fit_nested(xs["X0_event"], y, algs),
            best: fit_nested(xs[best], y, algs),
        }
        report["fits"][model] = entry

    with open(os.path.join(RES, "exposure_collapse.json"), "w") as fh:
        json.dump(report, fh, indent=1, default=float)

    # ------------------------------------------------------------------
    print(f"{report['n_points']} points pooled (grover.json + scaling_fair.json)\n")
    print("per-event damage at run strength (infidelity / strength):")
    for kkey, v in report["per_event_infidelity"].items():
        print(f"  {kkey:22s} 1-F_e = {v['ent_infid']:.5f}   "
              f"ratio to strength = {v['vs_strength']:.2f}")
    for model, entry in report["fits"].items():
        print(f"\n=== {model} ({entry['n_points']} points) ===")
        print(f"{'abscissa':16s} {'R^2':>7s} {'k':>8s} {'medres G':>9s} {'medres S':>9s}")
        for name, f in entry["abscissa"].items():
            print(f"{name:16s} {f['r2']:7.3f} {f['k']:8.4f} "
                  f"{f['median_abs_resid']['grover']:9.3f} "
                  f"{f['median_abs_resid']['shor']:9.3f}")
        print(f"best damage abscissa: {entry['best_damage_abscissa']}")
        for absc, nest in entry["nested"].items():
            print(f"  nested on {absc}:")
            for mname, m in nest.items():
                print(f"    {mname:22s} R^2 = {m['r2']:.3f}  "
                      f"({m['n_params']} params)")
        print("  per-family log-linear slopes (best damage abscissa):")
        for row in entry["abscissa"][entry["best_damage_abscissa"]]["families"]:
            if "note" in row:
                print(f"    {row['family']:12s} {row['note']}")
            else:
                print(f"    {row['family']:12s} k = {row['k']:7.4f}  "
                      f"R^2(log-lin) = {row['r2_loglinear']:.3f}  "
                      f"R^2(log-quad) = {row['r2_logquad']:.3f}")


if __name__ == "__main__":
    main()
