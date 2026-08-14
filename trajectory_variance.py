"""Is the trajectory error bar real? Characterise it, then re-derive every
sigma and chi^2 claim from the measurement.

Referee objection (Gottesman-style report, major comment on statistics):
the paper offers chi^2/dof = 0.01 on the first three ladder sizes as
support for a plateau, reading it as "the trajectory error bars are
conservative for these points". With 2 dof that sits in the ~1%
OVER-fitting tail: it says the bars are too large, the points are
correlated, or a low fluctuation happened -- it is not evidence for the
plateau. The very next sentences then spend those same bars on a
"4.1 sigma" drop and a "1.9 sigma" drop. The error model cannot be
simultaneously too conservative and correctly calibrated. The estimator
is moreover advertised as non-Bernoulli ("statistical error is well
below Bernoulli") and its variance is never characterised.

The referee is right that this cannot be argued from the armchair, so
this script measures it. The estimator under test is exactly the one the
paper ran: `trajectories.shor_trajectories` returns the sample mean of
S_k = sum over decoded outcomes of that trajectory's own outcome
distribution, and quotes sd(S_k)/sqrt(M) as the standard error.

Three things are measured, all through the public entry point so that
what is tested is what was run:

  1. Bias. At (d, m) small enough for an exact density matrix, the
     pooled trajectory mean is compared against `shor_run`.
  2. Calibration. R independent replicas of M trajectories give an
     empirical standard error (the spread of the replica means) to set
     against the mean quoted standard error. Their ratio is the number
     the referee is actually asking for; a Bartlett-style chi^2 on the
     replica spread says whether any departure is significant.
  3. Shape. Skewness and excess kurtosis of the replica means, plus the
     realised coverage of the nominal 1- and 2-sigma intervals -- because
     sigma-counting at 4.1 sigma needs the tail, not just the width.

The sub-Bernoulli claim is quantified as var(S_k) / [p(1-p)], the factor
by which averaging a whole outcome distribution per trajectory beats
sampling one outcome from it.

Finally, every chi^2 and sigma claim in the size-scaling passage is
recomputed from the stored run files under the calibration measured
here, so the paper's numbers are checked rather than restated.

Writes results/trajectory_variance.json.
Run: python3 trajectory_variance.py
"""

import json
import math
import os
import time
from concurrent.futures import ProcessPoolExecutor

import numpy as np

from qudit_shor import shor_run
from trajectories import shor_trajectories

N, A = 21, 2
M_TRAJ = 1000          # the paper's per-point trajectory count
REPLICAS = 24          # independent seeds per point

# (d, m, model, strength) -- the points the sigma claims are built on,
# plus a second base and a second regime as controls.
POINTS = [
    (3, 4, "transmon_cal", 0.003),
    (3, 6, "transmon_cal", 0.003),
    (3, 6, "depolarizing", 0.005),
    (2, 8, "transmon_cal", 0.003),
    (5, 3, "transmon_cal", 0.003),
]

RESULTS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results")


def one(job):
    d, m, model, s, rep = job
    t0 = time.time()
    # Deterministic, process-independent seeds. NOTE: the production
    # scripts seed with hash((label, d, m)), and Python randomises str
    # hashing per process unless PYTHONHASHSEED is pinned -- so those
    # seeds are not reproducible across runs. Flagged in the report.
    seed = (rep + 1) * 1_000_003 + d * 10_007 + m * 101 + len(model)
    r = shor_trajectories(d, m, model, s, n_traj=M_TRAJ, seed=seed,
                          a=A, N=N)
    return {"d": d, "m": m, "model": model, "strength": s, "replica": rep,
            "success": r["success"], "stderr": r["stderr"],
            "floor": r["floor"], "elapsed_s": round(time.time() - t0, 1)}


def characterise(runs, d, m, model, s):
    """Empirical vs quoted standard error for one point."""
    sel = [x for x in runs if x["d"] == d and x["m"] == m
           and x["model"] == model and x["strength"] == s]
    means = np.array([x["success"] for x in sel])
    quoted = np.array([x["stderr"] for x in sel])
    R = len(means)

    emp = float(means.std(ddof=1))          # truth: spread of replica means
    quo = float(quoted.mean())              # what the paper prints
    ratio = emp / quo

    # Is the departure significant? (R-1) * emp^2 / quo^2 ~ chi^2_{R-1}
    stat = (R - 1) * (emp / quo) ** 2
    # two-sided p-value from the chi^2_{R-1} tail
    from scipy.stats import chi2, norm
    p = 2 * min(chi2.cdf(stat, R - 1), 1 - chi2.cdf(stat, R - 1))

    z = (means - means.mean()) / quoted
    pooled = float(means.mean())
    var_Sk = quo ** 2 * M_TRAJ              # per-trajectory variance
    bern = pooled * (1 - pooled)

    return {
        "d": d, "m": m, "model": model, "strength": s, "replicas": R,
        "pooled_mean": pooled,
        "empirical_stderr": emp, "quoted_stderr": quo,
        "calibration_ratio": ratio,
        "bartlett_chi2": float(stat), "bartlett_dof": R - 1,
        "bartlett_p": float(p),
        "var_per_traj": float(var_Sk), "bernoulli_var": float(bern),
        "sub_bernoulli_factor": float(bern / var_Sk),
        "skew": float(((z - z.mean()) ** 3).mean() / z.std() ** 3),
        "excess_kurtosis": float(((z - z.mean()) ** 4).mean()
                                 / z.std() ** 4 - 3.0),
        "coverage_1sigma": float(np.mean(np.abs(z) <= 1.0)),
        "coverage_2sigma": float(np.mean(np.abs(z) <= 2.0)),
        "nominal_1sigma": float(2 * norm.cdf(1) - 1),
        "nominal_2sigma": float(2 * norm.cdf(2) - 1),
    }


# --- re-derivation of the paper's size-scaling statistics ------------------

def load_series(regime_index: int = 2):
    """d = 3 signal series over m = 4..9, assembled as the paper assembles
    it: sizes 4-7 from the main sweep, 8 and 9 from their own runs.

    regime order in the stored files is
    [depolarizing, transmon, transmon_cal, transmon_cal_lowcharge].
    """
    main = json.load(open(os.path.join(RESULTS, "scaling_fair_1000.json")))
    base = {k: v["success"] for k, v in main["baselines"].items()}
    series = {}
    for label, idx in (("transmon_cal", 2), ("depolarizing", 0)):
        pts = []
        for x in main["runs"]:
            if x["d"] != 3:
                continue
            if x["regime"] != main["regimes"][idx][0]:
                continue
            # two entries share the transmon_cal model name; the paper's
            # calibrated ladder is the dephase_ratio = 1 one, which is the
            # first of the pair in file order.
            pts.append(x)
        seen, keep = set(), []
        for x in pts:
            if x["m"] in seen:
                continue
            seen.add(x["m"])
            keep.append(x)
        rows = []
        for x in sorted(keep, key=lambda y: y["m"]):
            span = base[f"3,{x['m']}"] - x["floor"]
            rows.append({"m": x["m"], "bits": x["m"] * math.log2(3),
                         "signal": (x["success"] - x["floor"]) / span,
                         "sig_err": x["stderr"] / span})
        for fname in ("scaling_fair_m8.json", "scaling_fair_d3_m9.json"):
            j = json.load(open(os.path.join(RESULTS, fname)))
            for x in j["runs"]:
                if x["d"] != 3 or x["regime"] != main["regimes"][idx][0]:
                    continue
                if any(rr["m"] == x["m"] for rr in rows):
                    continue
                span = (x["success"] - x["floor"]) / x["signal"]
                rows.append({"m": x["m"], "bits": x["m"] * math.log2(3),
                             "signal": x["signal"],
                             "sig_err": x["stderr"] / span})
        series[label] = sorted(rows, key=lambda r: r["m"])
    return series


def rederive(series, inflate: float):
    """Recompute the plateau chi^2 and every sigma gap, scaling the quoted
    bars by the measured calibration ratio."""
    from scipy.stats import chi2
    out = {"calibration_applied": inflate, "claims": []}

    lad = series["transmon_cal"]
    first3 = lad[:3]
    y = np.array([r["signal"] for r in first3])
    e = np.array([r["sig_err"] for r in first3]) * inflate
    w = 1.0 / e ** 2
    ybar = float((w * y).sum() / w.sum())
    c2 = float((w * (y - ybar) ** 2).sum())
    dof = len(y) - 1
    out["claims"].append({
        "claim": "plateau over the first three ladder sizes",
        "paper": "chi^2/dof = 0.01, read as 'error bars are conservative'",
        "signals": y.tolist(), "errors": e.tolist(),
        "chi2": c2, "dof": dof, "chi2_per_dof": c2 / dof,
        "p_low_tail": float(chi2.cdf(c2, dof)),
        "raw_spread": float(y.max() - y.min()),
    })

    def gap(rows, m_hi, m_lo, label, paper):
        a = next(r for r in rows if r["m"] == m_lo)
        b = next(r for r in rows if r["m"] == m_hi)
        delta = a["signal"] - b["signal"]
        sd = math.hypot(a["sig_err"] * inflate, b["sig_err"] * inflate)
        out["claims"].append({
            "claim": label, "paper": paper,
            "from_bits": a["bits"], "to_bits": b["bits"],
            "delta": delta, "sigma": sd, "n_sigma": delta / sd})

    gap(lad, 9, 6, "ladder drop, 9.5 -> 14.3 bits", "4.1 sigma")
    gap(series["depolarizing"], 9, 6,
        "depolarizing drop, 9.5 -> 14.3 bits", "1.9 sigma")
    return out


def main():
    os.makedirs(RESULTS, exist_ok=True)

    print("--- bias check against exact density matrix ---", flush=True)
    bias = []
    for d, m, model, s in [(3, 4, "transmon_cal", 0.003)]:
        exact = shor_run(d, model, s, a=A, N=N)["success"]
        big = shor_trajectories(d, m, model, s, n_traj=8 * M_TRAJ, seed=99,
                                a=A, N=N)
        z = (big["success"] - exact) / big["stderr"]
        bias.append({"d": d, "m": m, "model": model, "exact": float(exact),
                     "traj": big["success"], "stderr": big["stderr"],
                     "n_traj": 8 * M_TRAJ, "z": float(z)})
        print(f"  d={d} m={m} {model}: exact {exact:.6f}  traj "
              f"{big['success']:.6f} +- {big['stderr']:.6f}  ({z:+.2f} sigma)",
              flush=True)

    jobs = [(d, m, mo, s, rep) for (d, m, mo, s) in POINTS
            for rep in range(REPLICAS)]
    print(f"\n{len(jobs)} trajectory batches "
          f"({REPLICAS} replicas x {M_TRAJ} traj at {len(POINTS)} points)",
          flush=True)
    t0 = time.time()
    with ProcessPoolExecutor(max_workers=6) as ex:
        runs = list(ex.map(one, jobs))
    print(f"done in {time.time() - t0:.0f} s\n", flush=True)

    print("--- estimator calibration ---")
    print(f"{'point':>22} {'empirical SE':>13} {'quoted SE':>10} "
          f"{'ratio':>7} {'p':>7} {'sub-Bern':>9} {'skew':>7} {'cov1s':>6}")
    stats = []
    for d, m, model, s in POINTS:
        st = characterise(runs, d, m, model, s)
        stats.append(st)
        print(f"{'d=%d m=%d %s' % (d, m, model):>22} "
              f"{st['empirical_stderr']:13.6f} {st['quoted_stderr']:10.6f} "
              f"{st['calibration_ratio']:7.3f} {st['bartlett_p']:7.3f} "
              f"{st['sub_bernoulli_factor']:9.1f} {st['skew']:7.2f} "
              f"{st['coverage_1sigma']:6.2f}")

    ratios = np.array([x["calibration_ratio"] for x in stats])
    inflate = float(ratios.mean())
    print(f"\n  mean calibration ratio {inflate:.3f} "
          f"(range {ratios.min():.3f}-{ratios.max():.3f}); "
          f"nominal 1-sigma coverage {stats[0]['nominal_1sigma']:.2f}")
    print(f"  a ratio near 1 means the quoted bars are right and the "
          f"chi^2/dof=0.01 was a fluctuation, not conservatism")

    print("\n--- re-derivation of the paper's scaling statistics ---")
    series = load_series()
    for label, rows in series.items():
        print(f"  {label}: " + ", ".join(
            f"{r['bits']:.1f}b {r['signal']:.3f}+-{r['sig_err']:.3f}"
            for r in rows))
    red = rederive(series, inflate)
    for c in red["claims"]:
        if "chi2" in c:
            print(f"\n  [{c['claim']}]\n    paper: {c['paper']}")
            print(f"    recomputed chi^2/dof = {c['chi2_per_dof']:.4f} "
                  f"({c['dof']} dof), lower-tail p = {c['p_low_tail']:.4f}")
            print(f"    raw spread {c['raw_spread']:.4f} vs typical bar "
                  f"{np.mean(c['errors']):.4f}")
        else:
            print(f"\n  [{c['claim']}]\n    paper: {c['paper']}")
            print(f"    recomputed: delta {c['delta']:.4f} +- {c['sigma']:.4f}"
                  f" = {c['n_sigma']:.2f} sigma")

    out = {"m_traj": M_TRAJ, "replicas": REPLICAS, "points": POINTS,
           "bias_check": bias, "stats": stats, "runs": runs,
           "calibration_ratio_mean": inflate,
           "series": series, "rederivation": red}
    path = os.path.join(RESULTS, "trajectory_variance.json")
    with open(path, "w") as f:
        json.dump(out, f, indent=1)
    print(f"\nwrote {path}")


if __name__ == "__main__":
    main()
