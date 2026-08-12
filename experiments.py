"""Sweep noise strength for d in {2,3,5} under both noise models.

Writes results/results.json. Run: python3 experiments.py
"""

import json
import os
import time

from qudit_shor import shor_run

STRENGTHS = [0.002, 0.005, 0.01, 0.02, 0.035, 0.05]
MODELS = ["transmon", "depolarizing"]
BASES = [2, 3, 5]


def main():
    os.makedirs("results", exist_ok=True)
    out = {"strengths": STRENGTHS, "models": MODELS, "bases": BASES, "runs": []}

    for d in BASES:
        t0 = time.time()
        base = shor_run(d)
        base["probs"] = base["probs"].tolist()
        base["elapsed_s"] = round(time.time() - t0, 2)
        out["runs"].append(base)
        print(f"d={d} noiseless: success={base['success']:.4f} "
              f"qudits={base['n_qudits']} layers={base['n_layers']} "
              f"({base['elapsed_s']}s)", flush=True)
        for model in MODELS:
            for s in STRENGTHS:
                t0 = time.time()
                res = shor_run(d, model, s)
                res["probs"] = res["probs"].tolist()
                res["elapsed_s"] = round(time.time() - t0, 2)
                out["runs"].append(res)
                print(f"d={d} {model:13s} s={s:<6g} success={res['success']:.4f} "
                      f"rel={res['success']/base['success']:.3f} "
                      f"({res['elapsed_s']}s)", flush=True)

    with open("results/results.json", "w") as f:
        json.dump(out, f, indent=1)
    print("\nwrote results/results.json")


if __name__ == "__main__":
    main()
