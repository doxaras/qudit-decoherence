"""Rescore the fidelity collapse in LOG fidelity.

The paper's collapse table fits F = A*exp(-k*x) in linear fidelity
(fidelity_collapse.py), where the shared fit reaches R^2 = 0.97/0.99.
Linear R^2 barely weights the deep tail, so the paper also quotes the
same fit rescored in log fidelity -- the metric that does -- and the
log-domain refit. This script computes both numbers.

Run: python3 logfid_rescore.py
Writes results/logfid_rescore.json.
"""

import json

import numpy as np

from exposure_collapse import ent_fidelity, fit_exp

REGIMES = [("transmon_cal", "ladder"), ("depolarizing", "depol")]
OUT = "results/logfid_rescore.json"


def r_squared(y, yhat):
    y, yhat = np.asarray(y, float), np.asarray(yhat, float)
    return 1 - np.sum((y - yhat) ** 2) / np.sum((y - y.mean()) ** 2)


def main():
    points = json.load(open("results/fidelity_collapse.json"))["points"]
    out = {}
    for model, tag in REGIMES:
        sub = [p for p in points if p["model"] == model]
        x = np.array([p["n_qudits"] * p["n_layers"]
                      * (1 - ent_fidelity(p["d"], model, p["strength"]))
                      for p in sub])
        y = np.array([p["fidelity"] for p in sub])
        lin = fit_exp(x, y)
        ly = np.log(np.maximum(y, 1e-12))
        # the linear-domain fit, rescored in log fidelity
        r2_rescore = r_squared(ly, np.log(lin["A"]) - lin["k"] * x)
        # refit in log domain
        slope, icpt = np.polyfit(x, ly, 1)
        r2_refit = r_squared(ly, icpt + slope * x)
        out[tag] = {"n_points": len(sub),
                    "linear_fit": {"A": lin["A"], "k": lin["k"],
                                   "r2_linear": lin["r2"]},
                    "r2_log_rescored": r2_rescore,
                    "r2_log_refit": r2_refit,
                    "log_refit": {"A": float(np.exp(icpt)),
                                  "k": float(-slope)}}
        print(f"{tag:8s} linear R^2 = {lin['r2']:.3f}  "
              f"log-rescored R^2 = {r2_rescore:.3f}  "
              f"log-refit R^2 = {r2_refit:.3f}")
    with open(OUT, "w") as f:
        json.dump(out, f, indent=1)
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
