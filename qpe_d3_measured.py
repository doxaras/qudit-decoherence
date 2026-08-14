"""Qutrit QPE predictions at per-base measured gate fidelities.

The measured-fidelity analysis of `hrmo_reanalysis.py` leaves exactly one
surviving pairing: d = 3 under per-particle depolarizing noise with the
`ion` cost model, where the inflation factor implied by the measured
native gates (Hrmo et al., Nat. Commun. 14, 2242 (2023): 99.6% at d = 2,
98.7% at d = 3) is f = 1.37, below the critical f* = 1.56. This script
turns that cell into an experimental proposal: eigenstate QPE at d = 3
against qubit registers, each base charged the per-carrier-layer strength
its own measured gate implies,

    s = eps / (2 L (1 - 1/d^2)),   L = 1 (d=2), d-1 (ion cost, d>2).

Two qubit pairings are reported at 5 bits, because the choice is not
neutral: m = 7 (D = 128) matches the qutrit's D = 81 in the paper's
"approximately matched control dimension" convention, while m = 6
(D = 64) is the closer register but cannot express the 5-bit criterion
(noiseless ceiling 0.816 vs 0.995). The qutrit's raw-success advantage
survives both; its floor-corrected signal advantage does not.

Writes results/qpe_d3_measured.json. Run: python3 qpe_d3_measured.py
"""

import json
import os
import time

from qpe_generic import PHI_TARGET, _prepare, good_phase_mask, qpe_run_exact

RESULTS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results")
COST = "ion"

# Hrmo et al. 2023, measured native two-qudit gate infidelities.
EPS = {2: 0.004, 3: 0.013}


def implied_s(eps: float, d: int) -> float:
    L = 1.0 if d == 2 else float(d - 1)
    return eps / (2.0 * L * (1.0 - 1.0 / d ** 2))


S = {d: implied_s(e, d) for d, e in EPS.items()}

# (bits, qutrit config, [qubit configs])
PAIRS = [
    (4, (3, 3), [(2, 5)]),
    (5, (3, 4), [(2, 7), (2, 6)]),
]


def cell(d: int, m: int, bits: int, s: float) -> dict:
    D = d ** m
    good = good_phase_mask(D, PHI_TARGET, bits)
    floor = float(good.mean())
    noiseless = float(qpe_run_exact(d, m, cost_model=COST)["probs"][good].sum())
    p = float(qpe_run_exact(d, m, "depolarizing", s,
                            cost_model=COST)["probs"][good].sum())
    _, gates, *_ = _prepare(d, m, seed=42, cost_model=COST)
    ent = [c for sites, _, c in gates if len(sites) > 1]
    return {"d": d, "m": m, "D": D, "bits": bits, "s": s,
            "floor": floor, "noiseless": noiseless, "success": p,
            "signal": (p - floor) / (noiseless - floor),
            "entangling_gates": len(ent),
            "entangling_layers": float(sum(ent))}


def main():
    print(f"implied strengths: s2={S[2]:.5f}, s3={S[3]:.5f} "
          f"(inflation f={S[3] / S[2]:.2f}, vs f*=1.56)", flush=True)
    rows = []
    for bits, (dq, mq), qubits in PAIRS:
        t0 = time.time()
        q = cell(dq, mq, bits, S[3])
        print(f"\n{bits} bits | d=3 m={mq} (D={q['D']}, "
              f"{q['entangling_gates']} gates / {q['entangling_layers']:.0f} "
              f"layers): success={q['success']:.3f} signal={q['signal']:.3f}",
              flush=True)
        refs = []
        for d2, m2 in qubits:
            b = cell(d2, m2, bits, S[2])
            refs.append(b)
            print(f"   vs d=2 m={m2} (D={b['D']}, {b['entangling_gates']} "
                  f"gates / {b['entangling_layers']:.0f} layers): "
                  f"success={b['success']:.3f} signal={b['signal']:.3f}"
                  f"  -> raw: {'qutrit' if q['success'] > b['success'] else 'qubit'}"
                  f", signal: {'qutrit' if q['signal'] > b['signal'] else 'qubit'}"
                  f"  ({time.time() - t0:.0f}s)", flush=True)
        rows.append({"bits": bits, "qutrit": q, "qubit_refs": refs})

    os.makedirs(RESULTS, exist_ok=True)
    path = os.path.join(RESULTS, "qpe_d3_measured.json")
    with open(path, "w") as f:
        json.dump({"cost_model": COST, "noise_model": "depolarizing",
                   "eps": {str(k): v for k, v in EPS.items()},
                   "s": {str(k): v for k, v in S.items()},
                   "phi": PHI_TARGET, "rows": rows}, f, indent=1)
    print(f"\nwrote {path}")


if __name__ == "__main__":
    main()
