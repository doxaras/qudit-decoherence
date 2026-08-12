"""Cross-validation against Jankovic et al. 2023 (arXiv:2302.04543).

Pre-publication hardening task #1b. Everything else in this repo is our own
machinery checked against itself; this checks it against an independent
analytic result derived by other people with other methods (linear response
of the average gate infidelity, Weingarten calculus over the Haar measure).

Their setup is the gate-level limit of ours: one qudit of dimension d
against n = log2(d) qubits spanning the same Hilbert space, both under pure
dephasing with collapse operator L = J_z, compared by the first-order-in-
gamma*t response of the infidelity. They derive (their Eqs. 30, 31, 22):

    E_p(qudit)   = (gamma t / 12) (d^2 - 1)
    E_p(n qubits)= (gamma t / 4) n
    ratio c_d / c_b,n = (d^2 - 1) / (3 log2 d)          <- critical curve

The last one is the paper's headline: a qudit platform must beat the
multiqubit platform's gate-time-per-decoherence-time by exactly this factor
to break even, and it is *less* demanding than the O(d^2/log2 d) folklore
at the small d we care about (d = 3, 5).

We reproduce all three from our own superoperator code -- the same
`_dissipator` and `expm` path the main study uses -- with no analytics.

Two notes on why this is a fair test of our code rather than a tautology:

  * Their L = J_z = diag((d-1)/2, ..., -(d-1)/2); ours is the number
    operator n_hat. For Hermitian L the Lindblad dissipator is invariant
    under L -> L + cI, so D[J_z] = D[n_hat] exactly -- the check exercises
    the identical code path used by `transmon_superop`.
  * The entanglement (process) infidelity is computed from the Choi
    matrix of the numerically exponentiated superoperator, so an error in
    our vec convention, dissipator, or matrix exponential would show up.

Writes results/jankovic.json. Run: python3 jankovic_check.py
"""

import json
import os

import numpy as np
from scipy.linalg import expm

from qudit_shor import _dissipator

GAMMA_T = 1e-6           # deep in the linear-response regime they require
DIMS = [2, 4, 8, 16, 32, 64]


def dephasing_channel(d: int, gamma_t: float) -> np.ndarray:
    """exp(gamma t D[J_z]) as a row-major-vec superoperator."""
    Jz = np.diag(np.arange(d - 1, -d, -2) / 2.0)   # (d-1)/2 ... -(d-1)/2
    return expm(gamma_t * _dissipator(Jz))


def entanglement_fidelity(E: np.ndarray, d: int) -> float:
    """F_e = (1/d^2) sum_ij <i| E(|i><j|) |j>."""
    tot = 0.0 + 0j
    for i in range(d):
        for j in range(d):
            eij = np.zeros((d, d))
            eij[i, j] = 1.0
            tot += (E @ eij.reshape(-1)).reshape(d, d)[i, j]
    return float(np.real(tot)) / d ** 2


def main():
    os.makedirs("results", exist_ok=True)
    gt = GAMMA_T

    # --- 1. single qudit: E_p should be (gamma t / 12)(d^2 - 1)
    qudit = []
    for d in DIMS:
        ep = 1.0 - entanglement_fidelity(dephasing_channel(d, gt), d)
        pred = gt / 12.0 * (d ** 2 - 1)
        qudit.append({"d": d, "measured": ep, "predicted": pred,
                      "rel_err": abs(ep - pred) / pred})
        print(f"qudit  d={d:3d}  E_p={ep:.6e}  Jankovic Eq30={pred:.6e}  "
              f"rel.err={qudit[-1]['rel_err']:.2e}", flush=True)

    # --- 2. n qubits: E_p should be (gamma t / 4) n.
    # For a tensor-product channel F_e is multiplicative, so the n-qubit
    # entanglement fidelity is F_e(1 qubit)^n. Verified directly against an
    # explicitly built 2- and 3-qubit channel below.
    f1 = entanglement_fidelity(dephasing_channel(2, gt), 2)
    qubits = []
    for d in DIMS:
        n = int(round(np.log2(d)))
        ep = 1.0 - f1 ** n
        pred = gt / 4.0 * n
        qubits.append({"n": n, "measured": ep, "predicted": pred,
                       "rel_err": abs(ep - pred) / pred})
        print(f"qubits n={n:3d}  E_p={ep:.6e}  Jankovic Eq31={pred:.6e}  "
              f"rel.err={qubits[-1]['rel_err']:.2e}", flush=True)

    # multiplicativity is an assumption above -- check it explicitly
    tensor_ok = []
    for n in (2, 3):
        E1 = dephasing_channel(2, gt)
        # build the n-qubit dephasing channel as a genuine 2^n-dim channel
        D = 2 ** n
        Jz1 = np.diag([0.5, -0.5])
        L = np.zeros((D, D))
        for q in range(n):
            op = np.eye(1)
            for k in range(n):
                op = np.kron(op, Jz1 if k == q else np.eye(2))
            L = L + op
        # independent dephasing on each qubit = sum of dissipators
        gen = sum(gt * _dissipator(
            np.kron(np.kron(np.eye(2 ** q), Jz1), np.eye(2 ** (n - q - 1))))
            for q in range(n))
        ep_direct = 1.0 - entanglement_fidelity(expm(gen), D)
        ep_mult = 1.0 - entanglement_fidelity(E1, 2) ** n
        tensor_ok.append({"n": n, "direct": ep_direct, "multiplicative":
                          ep_mult, "rel_err": abs(ep_direct - ep_mult)
                          / ep_direct})
        print(f"tensor check n={n}: direct={ep_direct:.6e} "
              f"multiplicative={ep_mult:.6e} "
              f"rel.err={tensor_ok[-1]['rel_err']:.2e}", flush=True)

    # --- 3. the critical curve itself
    curve = []
    for q, b in zip(qudit, qubits):
        d, n = q["d"], b["n"]
        if n == 0:
            continue
        measured = q["measured"] / b["measured"]
        pred = (d ** 2 - 1) / (3.0 * np.log2(d))
        curve.append({"d": d, "n": n, "measured": measured,
                      "critical_curve": pred,
                      "rel_err": abs(measured - pred) / pred})
        print(f"ratio  d={d:3d}  c_d/c_b,n={measured:9.4f}  "
              f"(d^2-1)/(3log2 d)={pred:9.4f}  "
              f"rel.err={curve[-1]['rel_err']:.2e}", flush=True)

    worst = max(x["rel_err"] for x in qudit + qubits + curve + tensor_ok)
    print(f"\nworst relative error across all checks: {worst:.2e}")

    # --- 4. what the curve says about the dimensions we actually study
    print("\nbreak-even gate-efficiency ratio our bases must beat:")
    for d in (3, 5):
        print(f"  d={d}: (d^2-1)/(3 log2 d) = "
              f"{(d ** 2 - 1) / (3 * np.log2(d)):.3f}  "
              f"(naive d^2/log2 d = {d ** 2 / np.log2(d):.3f})")

    # --- 5. does their gate-level criterion predict our algorithm results?
    # Their (d^2-1) factor comes from the J_z dephasing scaling -- the same
    # physics as our transmon ladder, and NOT as our per-particle
    # depolarizing model, so the criterion should apply to the former only.
    # Our circuits buy their speed-up by using fewer layers rather than
    # faster ones, so we read the layer-count ratio as the gate-efficiency
    # ratio tau_b/tau_d and ask whether it clears the critical curve.
    print("\napplying their criterion to our circuits (transmon ladder):")
    applied = []
    try:
        with open("results/cost_fair.json") as f:
            cf = json.load(f)
    except FileNotFoundError:
        cf = None
    if cf:
        runs = [r for r in cf["runs"]
                if r["noise"] == "transmon_cal" and r["strength"] == 0.005]
        for cm in cf["costs"]:
            by_d = {r["d"]: r for r in runs if r["cost"] == cm}
            for d in (3, 5):
                ratio = by_d[2]["layers"] / by_d[d]["layers"]
                crit = (d ** 2 - 1) / (3.0 * np.log2(d))
                predicted = ratio > crit
                observed = by_d[d]["signal"] > by_d[2]["signal"]
                applied.append({"cost": cm, "d": d, "layer_ratio": ratio,
                                "critical": crit, "predicted_qudit_wins":
                                bool(predicted), "observed_qudit_wins":
                                bool(observed), "agree": bool(predicted == observed)})
                print(f"  {cm:9s} d={d}: layers ratio={ratio:5.2f} vs "
                      f"critical={crit:5.2f} -> predict "
                      f"{'qudit' if predicted else 'qubit':5s}, observed "
                      f"{'qudit' if observed else 'qubit':5s} "
                      f"{'OK' if predicted == observed else 'MISS'}")
        hits = sum(x["agree"] for x in applied)
        print(f"  criterion agrees with our simulation in "
              f"{hits}/{len(applied)} cases")

    with open("results/jankovic.json", "w") as f:
        json.dump({"gamma_t": gt, "qudit": qudit, "qubits": qubits,
                   "tensor_check": tensor_ok, "critical_curve": curve,
                   "worst_rel_err": worst, "applied": applied}, f, indent=1)
    print("\nwrote results/jankovic.json")


if __name__ == "__main__":
    main()
