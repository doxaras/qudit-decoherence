"""Predicted success probabilities for the proposed ion-trap QPE experiment.

Paper Sec. "Discussion" proposes the cheapest decisive test of the native
-gate condition: eigenstate QPE at d = 5, m = 2-3 on a Ringbauer-class
trapped-ion processor, and promises the predicted success probabilities.
This script computes them: per-particle depolarizing noise (the measured
ion structure), `ion` gate-cost model (the 2(d-1) Molmer-Sorensen
construction), exact density-matrix evolution (no sampling error), with
the noise strength bracketing the measured ion per-gate figure ~1e-3.

Qubit references are matched in control dimension, not digit count:
d=5, m=2 (D=25) vs d=2, m=5 (D=32) scored at 4 bits, and
d=5, m=3 (D=125) vs d=2, m=7 (D=128) scored at 5 bits
(at 5 bits the D=25 grid has no outcome within the success window, so
the 4-bit criterion is the finest both D~25-32 registers can express).

Writes results/ion_qpe_prediction.json. Run: python3 ion_qpe_prediction.py
"""

import json
import os
import time

from qpe_generic import PHI_TARGET, _prepare, good_phase_mask, qpe_run_exact

RESULTS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results")

PAIRS = [  # (bits, [(d, m), ...])
    (4, [(5, 2), (2, 5)]),
    (5, [(5, 3), (2, 7)]),
]
# 0.0005-0.002 brackets the projected ion memory/single-qudit figure;
# 0.005-0.02 is the band of DEMONSTRATED two-qudit entangling gates
# (two-qutrit MS fidelities ~95-98%, nothing published above d=3).
STRENGTHS = [0.0005, 0.001, 0.002, 0.005, 0.01, 0.02]
COST = "ion"


def gate_budget(d: int, m: int) -> dict:
    """Entangling-gate count and total layer cost of the compiled circuit."""
    dims, gates, *_ = _prepare(d, m, seed=42, cost_model=COST)
    ent = [(sites, cost) for sites, _, cost in gates if len(sites) > 1]
    return {"entangling_gates": len(ent),
            "entangling_layers": float(sum(c for _, c in ent)),
            "total_layers": float(sum(c for *_, c in gates))}


def main():
    rows = []
    for bits, configs in PAIRS:
        for d, m in configs:
            D = d ** m
            budget = gate_budget(d, m)
            base = qpe_run_exact(d, m, cost_model=COST)
            good = good_phase_mask(D, PHI_TARGET, bits)
            floor = float(good.mean())
            noiseless = float(base["probs"][good].sum())
            row = {"d": d, "m": m, "D": D, "bits": bits, **budget,
                   "floor": floor, "noiseless": noiseless, "success": {}}
            for s in STRENGTHS:
                t0 = time.time()
                res = qpe_run_exact(d, m, "depolarizing", s, cost_model=COST)
                p = float(res["probs"][good].sum())
                row["success"][str(s)] = {
                    "raw": p, "signal": (p - floor) / (noiseless - floor)}
                print(f"d={d} m={m} bits={bits} s={s:<7g} "
                      f"success={p:.4f} signal={(p - floor) / (noiseless - floor):.3f} "
                      f"({time.time() - t0:.0f}s)", flush=True)
            rows.append(row)
            print(f"  d={d} m={m}: {budget['entangling_gates']} entangling "
                  f"gates, {budget['entangling_layers']:.0f} MS-equivalent "
                  f"layers, noiseless={noiseless:.4f}, floor={floor:.4f}",
                  flush=True)

    os.makedirs(RESULTS, exist_ok=True)
    with open(os.path.join(RESULTS, "ion_qpe_prediction.json"), "w") as f:
        json.dump({"cost_model": COST, "noise_model": "depolarizing",
                   "strengths": STRENGTHS, "phi": PHI_TARGET, "rows": rows},
                  f, indent=1)
    print("\nwrote results/ion_qpe_prediction.json")


if __name__ == "__main__":
    main()
