"""Rescore the collapse in average-gate-infidelity (F_avg) units.

Round-4 referee point (R1-M7): the damage unit 1 - F_e tends to
1 - 1/d^2 for a fully depolarizing channel, i.e. it grows with d by
construction. The d-normalized alternative is the average gate
infidelity 1 - F_avg = [d/(d+1)](1 - F_e), which changes the abscissa
scale by 20-25% between d = 2 and d = 5 -- and since the collapse's
headline is precisely a shrinking cross-d spread, part of that
improvement could be metric convention.

exposure_collapse.py already computes the signal fits in both units
(X1 = ent. infidelity, X2 = avg. infidelity); this script extracts the
comparison and adds what was missing: the FIDELITY collapse (the
tab:collapse headline row) refit in X2 units, from the
fidelity_collapse.json points (with the deep-tail re-measurements of
collapse_tail_deep.json substituted when present).

Writes results/favg_rescore.json. Run: python3 favg_rescore.py
"""

import json
import os

import numpy as np

from exposure_collapse import ent_fidelity, fit_exp, r_squared

OUT = "results/favg_rescore.json"


def load_fidelity_points():
    base = json.load(open("results/fidelity_collapse.json"))["points"]
    deep_path = "results/collapse_tail_deep.json"
    if os.path.exists(deep_path):
        deep = json.load(open(deep_path))["points"]
        by_key = {(p["alg"], p["d"], p["size"], p["model"]): p for p in deep}
        base = [by_key.get((p["alg"], p["d"], p["size"], p["model"]), p)
                for p in base]
        print(f"substituted {len(by_key)} deep-tail points")
    return base


def fidelity_fit(points, model, unit):
    sub = [p for p in points if p["model"] == model]
    scale = {p["d"]: (p["d"] / (p["d"] + 1) if unit == "X2" else 1.0)
             for p in sub}
    x = np.array([p["n_qudits"] * p["n_layers"] * scale[p["d"]]
                  * (1 - ent_fidelity(p["d"], model, p["strength"]))
                  for p in sub])
    y = np.array([p["fidelity"] for p in sub])
    lin = fit_exp(x, y)
    # per-algorithm rate split, as the paper's nested check
    out = {"r2": float(lin["r2"]), "A": float(lin["A"]), "k": float(lin["k"])}
    for alg in ("grover", "shor"):
        m = [p["alg"] == alg for p in sub]
        f = fit_exp(x[m], y[np.array(m)])
        out[f"{alg}_k"] = float(f["k"])
    return out


def main():
    exp = json.load(open("results/exposure_collapse.json"))
    out = {"damage_units": {}, "signal": {}, "fidelity": {}}

    for d in (2, 3, 5):
        fe = 1 - ent_fidelity(d, "transmon_cal", 1e-6)
        out["damage_units"][f"ladder_d{d}"] = {
            "ent_infid_per_s": fe / 1e-6,
            "avg_infid_per_s": (d / (d + 1)) * fe / 1e-6}
    print("ladder damage per unit strength, 1-F_e vs 1-F_avg:")
    for k, v in out["damage_units"].items():
        print(f"  {k}: {v['ent_infid_per_s']:.4f} vs "
              f"{v['avg_infid_per_s']:.4f}")

    for ch in ("transmon_cal", "depolarizing"):
        e = exp["fits"][ch]["abscissa"]
        entry = {}
        for unit in ("X1_ent_infid", "X2_avg_infid"):
            fams = {f["family"]: f["k"] for f in e[unit]["families"]
                    if f["family"].startswith("grover")}
            ks = list(fams.values())
            entry[unit] = {"shared_r2": e[unit]["r2"],
                           "grover_family_k": fams,
                           "grover_spread": max(ks) / min(ks)}
        out["signal"][ch] = entry
        print(f"\n{ch} signal: shared R^2 "
              f"{entry['X1_ent_infid']['shared_r2']:.3f} (1-F_e) -> "
              f"{entry['X2_avg_infid']['shared_r2']:.3f} (1-F_avg); "
              f"grover spread {entry['X1_ent_infid']['grover_spread']:.2f}x "
              f"-> {entry['X2_avg_infid']['grover_spread']:.2f}x")

    points = load_fidelity_points()
    for ch in ("transmon_cal", "depolarizing"):
        entry = {unit: fidelity_fit(points, ch, unit)
                 for unit in ("X1", "X2")}
        out["fidelity"][ch] = entry
        print(f"{ch} fidelity: shared R^2 {entry['X1']['r2']:.4f} (1-F_e) "
              f"-> {entry['X2']['r2']:.4f} (1-F_avg); "
              f"alg rates {entry['X2']['grover_k']:.3f}/"
              f"{entry['X2']['shor_k']:.3f} in F_avg units")

    with open(OUT, "w") as f:
        json.dump(out, f, indent=1)
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
