"""Re-tabulate the proposed ion QPE experiment (paper Table `tab:prediction`)
at PER-BASE noise strengths taken from measured gate fidelities, instead of
one shared strength (referee requirement 2, Innsbruck-style report).

The original table charges qubit and ququint registers the same
per-carrier-layer strength s. Measured hardware does not: the only
published native qudit entangling gate (Hrmo et al., Nat. Commun. 14,
2242 (2023)) has infidelity 0.004 at d=2 and 0.063 at d=5 on the same
apparatus. Under the paper's exposure convention (a two-qudit gate of
relative layer cost L deposits 2 L s (1 - 1/d^2)), the implied strengths
under the `ion` cost model (L = 1 at d=2, d-1 = 4 at d=5) are

    s_2 = eps_2 / (2 * 1 * 3/4)      s_5 = eps_5 / (2 * 4 * 24/25)

Two qubit scenarios: (a) Hrmo's own d=2 gate (same apparatus,
apples-to-apples) and (b) an IonQ-Forte-class 0.7% two-qubit gate.

Writes results/qpe_measured_strengths.json. Run:
python3 qpe_measured_strengths.py
"""

import json
import os
import time

from qpe_generic import PHI_TARGET, _prepare, good_phase_mask, qpe_run_exact

RESULTS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results")
COST = "ion"

EPS = {"hrmo_d2": 0.004, "forte_d2": 0.007, "hrmo_d5": 0.063}


def implied_s(eps: float, d: int) -> float:
    L = 1.0 if d == 2 else float(d - 1)
    return eps / (2.0 * L * (1.0 - 1.0 / d ** 2))

S_QUBIT = {"hrmo": implied_s(EPS["hrmo_d2"], 2),
           "forte": implied_s(EPS["forte_d2"], 2)}
S_QUQUINT = implied_s(EPS["hrmo_d5"], 5)

PAIRS = [  # (bits, qudit config, qubit config)
    (4, (5, 2), (2, 5)),
    (5, (5, 3), (2, 7)),
]


def run_cell(d, m, bits, s):
    D = d ** m
    good = good_phase_mask(D, PHI_TARGET, bits)
    floor = float(good.mean())
    base = qpe_run_exact(d, m, cost_model=COST)
    noiseless = float(base["probs"][good].sum())
    res = qpe_run_exact(d, m, "depolarizing", s, cost_model=COST)
    p = float(res["probs"][good].sum())
    return {"d": d, "m": m, "bits": bits, "s": s, "floor": floor,
            "noiseless": noiseless, "success": p,
            "signal": (p - floor) / (noiseless - floor)}


def main():
    print(f"implied strengths: qubit(hrmo)={S_QUBIT['hrmo']:.5f}, "
          f"qubit(forte)={S_QUBIT['forte']:.5f}, ququint={S_QUQUINT:.5f} "
          f"(x{S_QUQUINT / S_QUBIT['hrmo']:.1f} / x{S_QUBIT['forte'] and S_QUQUINT / S_QUBIT['forte']:.1f})",
          flush=True)
    rows = []
    for bits, (dq, mq), (d2, m2) in PAIRS:
        t0 = time.time()
        qudit = run_cell(dq, mq, bits, S_QUQUINT)
        cells = {"ququint_hrmo": qudit}
        for tag, s2 in S_QUBIT.items():
            cells[f"qubit_{tag}"] = run_cell(d2, m2, bits, s2)
        for tag in S_QUBIT:
            qb = cells[f"qubit_{tag}"]
            winner = "ququint" if qudit["success"] > qb["success"] else "qubit"
            print(f"bits={bits}: d=5,m={mq} success={qudit['success']:.3f} "
                  f"vs d=2,m={m2} ({tag}) {qb['success']:.3f} -> {winner} "
                  f"({time.time() - t0:.0f}s)", flush=True)
            cells[f"winner_vs_{tag}"] = winner
        rows.append({"bits": bits, **cells})

    os.makedirs(RESULTS, exist_ok=True)
    with open(os.path.join(RESULTS, "qpe_measured_strengths.json"), "w") as f:
        json.dump({"cost_model": COST, "noise_model": "depolarizing",
                   "eps": EPS, "s_qubit": S_QUBIT, "s_ququint": S_QUQUINT,
                   "phi": PHI_TARGET, "rows": rows}, f, indent=1)
    print("\nwrote results/qpe_measured_strengths.json")


if __name__ == "__main__":
    main()
