"""Deep-tail fidelity points at 16x the trajectory count.

Round-4 referee point (R3-4): the fidelity-collapse tail is scored on
points with 40-48% relative statistical error -- Shor d = 2, m = 12
(100 trajectories) and m = 10 depolarizing (200) -- and the claim "the
law holds within a factor of two" is not a test at that resolution (a
+-44% bar alone spans nearly a factor of two at 2 sigma).

This re-measures the three flagged points at n_traj = 1600 (fresh
seeds, chunked across workers), then re-scores the collapse fits of
fidelity_collapse.py / logfid_rescore.py with the deep values
substituted: shared linear-fidelity R^2, the log-fidelity rescore and
refit, and the factor-of-X deviation of each endpoint from the shared
law.

Writes results/collapse_tail_deep.json.
Run: python3 collapse_tail_deep.py           (~2 h, 6 workers)
     python3 collapse_tail_deep.py analyze   (re-analyze existing JSON)
"""

import json
import os
import sys
import time
import zlib
from concurrent.futures import ProcessPoolExecutor

import numpy as np

from exposure_collapse import ent_fidelity, fit_exp, r_squared
from qudit_shor import (apply_cost_model, apply_unitary_vec,
                        build_shor_gates, shor_config)
from trajectories import _kraus_sets, _sample_kraus

N_SHOR, A_SHOR = 21, 2
POINTS = [(2, 10, "depolarizing", 0.005),
          (2, 12, "depolarizing", 0.005),
          (2, 12, "transmon_cal", 0.003)]
N_TRAJ = 1600
CHUNK = 100
OUT = "results/collapse_tail_deep.json"


def chunk_fids(args):
    """One chunk of trajectories; returns the raw per-trajectory fidelities."""
    d, m, model, strength, chunk = args
    _, w = shor_config(d, N_SHOR)
    dims = [d] * (m + w)
    n = len(dims)
    gates = apply_cost_model(build_shor_gates(d, m, w, A_SHOR, N_SHOR), d,
                             "uniform")
    psi0 = np.zeros(d ** n, complex)
    psi0[1] = 1.0
    psi0 = psi0.reshape(dims)

    ideal = psi0
    for sites, U, _ in gates:
        ideal = apply_unitary_vec(ideal, U, sites, dims)
    ideal_flat = ideal.reshape(-1).conj()

    costs = {cost for _, _, cost in gates}
    kraus_sets = _kraus_sets(d, model, strength, costs)
    seed = zlib.crc32(
        f"deeptail,{d},{m},{model},{int(strength * 1e6)},{chunk}".encode())
    rng = np.random.default_rng(seed)
    t0 = time.time()
    fids = np.empty(CHUNK)
    for k in range(CHUNK):
        t = psi0
        for sites, U, cost in gates:
            t = apply_unitary_vec(t, U, sites, dims)
            for q in range(n):
                t = _sample_kraus(t, q, n, kraus_sets[cost], rng, dims)
        fids[k] = np.abs(ideal_flat @ t.reshape(-1)) ** 2
    return (d, m, model, strength, chunk, fids.tolist(),
            round(time.time() - t0, 1))


def run_points():
    jobs = [(d, m, model, s, c)
            for d, m, model, s in POINTS for c in range(N_TRAJ // CHUNK)]
    fids = {p: [] for p in POINTS}
    done = {p: 0 for p in POINTS}
    with ProcessPoolExecutor(max_workers=6) as ex:
        for d, m, model, s, chunk, f, dt in ex.map(chunk_fids, jobs):
            p = (d, m, model, s)
            fids[p].extend(f)
            done[p] += 1
            print(f"d={d} m={m} {model:13s} chunk {done[p]:2d}/"
                  f"{N_TRAJ // CHUNK} ({dt}s)", flush=True)

    points = []
    for (d, m, model, s), f in fids.items():
        f = np.array(f)
        _, w = shor_config(d, N_SHOR)
        gates = apply_cost_model(build_shor_gates(d, m, w, A_SHOR, N_SHOR),
                                 d, "uniform")
        points.append({
            "alg": "shor", "d": d, "size": m, "bits": m * np.log2(d),
            "n_qudits": m + w,
            "n_layers": sum(c for _, _, c in gates),
            "model": model, "strength": s,
            "fidelity": float(f.mean()),
            "stderr": float(f.std(ddof=1) / np.sqrt(len(f))),
            "n_traj": len(f)})
    return points


def analyze(deep_points):
    base = json.load(open("results/fidelity_collapse.json"))
    deep_by_key = {(p["alg"], p["d"], p["size"], p["model"]): p
                   for p in deep_points}
    merged, replaced = [], []
    for p in base["points"]:
        key = (p["alg"], p["d"], p["size"], p["model"])
        if key in deep_by_key:
            q = deep_by_key[key]
            replaced.append({"key": list(key),
                             "old": {"fidelity": p["fidelity"],
                                     "stderr": p["stderr"],
                                     "n_traj": p["n_traj"]},
                             "new": {"fidelity": q["fidelity"],
                                     "stderr": q["stderr"],
                                     "n_traj": q["n_traj"]}})
            merged.append(q)
        else:
            merged.append(p)

    out = {"replaced": replaced, "fits": {}}
    for model in ("transmon_cal", "depolarizing"):
        sub = [p for p in merged if p["model"] == model]
        x = np.array([p["n_qudits"] * p["n_layers"]
                      * (1 - ent_fidelity(p["d"], model, p["strength"]))
                      for p in sub])
        y = np.array([p["fidelity"] for p in sub])
        lin = fit_exp(x, y)
        ly = np.log(np.maximum(y, 1e-12))
        r2_rescore = r_squared(ly, np.log(lin["A"]) - lin["k"] * x)
        ls, li = np.polyfit(x, ly, 1)
        r2_logfit = r_squared(ly, li + ls * x)
        # factor by which each deep endpoint misses the shared linear fit
        factors = {}
        for p in sub:
            key = (p["alg"], p["d"], p["size"], p["model"])
            if key in deep_by_key:
                xi = (p["n_qudits"] * p["n_layers"]
                      * (1 - ent_fidelity(p["d"], model, p["strength"])))
                pred = lin["A"] * np.exp(-lin["k"] * xi)
                factors[f"d{p['d']}_m{p['size']}"] = {
                    "measured": p["fidelity"],
                    "rel_err": p["stderr"] / p["fidelity"],
                    "predicted": float(pred),
                    "factor": float(max(p["fidelity"] / pred,
                                        pred / p["fidelity"]))}
        out["fits"][model] = {
            "linear_r2": float(lin["r2"]), "A": float(lin["A"]),
            "k": float(lin["k"]),
            "log_rescore_r2": float(r2_rescore),
            "log_refit_r2": float(r2_logfit),
            "endpoint_factors": factors}
        print(f"-- {model} (deep tail substituted) --")
        print(f"   linear R^2 = {lin['r2']:.4f}  "
              f"log rescore = {r2_rescore:.4f}  "
              f"log refit = {r2_logfit:.4f}")
        for k, v in factors.items():
            print(f"   {k}: F = {v['measured']:.3e} "
                  f"(+-{100 * v['rel_err']:.0f}%), fit predicts "
                  f"{v['predicted']:.3e}, factor {v['factor']:.2f}")
    return out


def main():
    os.makedirs("results", exist_ok=True)
    if len(sys.argv) > 1 and sys.argv[1] == "analyze":
        deep_points = json.load(open(OUT))["points"]
    else:
        deep_points = run_points()
    out = analyze(deep_points)
    out["points"] = deep_points
    out["n_traj"] = N_TRAJ
    with open(OUT, "w") as f:
        json.dump(out, f, indent=1)
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
