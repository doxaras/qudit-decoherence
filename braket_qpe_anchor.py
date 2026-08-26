"""Braket anchor run: the qubit branch of the paper's prediction table.

Builds the COMPILED eigenstate-QPE circuits for d = 2, m = 5 and m = 7:
one work qubit prepared in the eigenstate |1>, m controlled-phase
kickback gates (angle 2*pi*frac(phi*2^i) on control i, mirroring the
simulator's little-endian exponent wiring), and the no-swap inverse QFT
(mirror of qudit_shor.build_qft_gates, reversed and conjugated), so
outcomes read in natural big-endian order exactly as control_probs
does. Entangling-gate count: m kickbacks + m(m-1)/2 QFT phases = 15
(m=5, 6 qubits) and 28 (m=7, 8 qubits).

Modes (default: validate) -- only `submit` costs money, and it is
double-guarded:

  validate  free local check: exact LocalSimulator probabilities vs the
            analytic Fejer kernel and the paper's noiseless successes.
  predict   exact density-matrix predictions for THIS compiled circuit
            under per-qubit depolarizing noise, two exposure
            conventions: (a) paper convention, every gate one full
            noise layer; (b) time-proportional, 1Q gates cost 130/970
            of a ZZ layer (IonQ Forte timing). Hardware should land
            between them, near (b).
  sv1       same check on the SV1 cloud simulator (~$1).
  submit    submit to an IonQ QPU. Requires --shots and
            --yes-spend-money. Prints the exact cost and asks nothing
            else -- do NOT run without the flag.

Run:  .venv-braket/bin/python braket_qpe_anchor.py [--mode ...]
"""

import argparse
import json
import math
import os

os.environ.setdefault("AWS_DEFAULT_REGION", "us-east-1")

import numpy as np

PHI = 0.6180339887498949          # golden-ratio conjugate (paper target)
CONFIGS = [(5, 4), (7, 5)]        # (m control qubits, success bits b)
ONEQ_LAYER = 130.0 / 970.0        # 1Q vs ZZ gate time on IonQ Forte
FORTE_ARN = "arn:aws:braket:us-east-1::device/qpu/ionq/Forte-1"
PER_SHOT, PER_TASK = 0.08, 0.30
RESULTS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results")


# --------------------------------------------------------------------------
# The compiled circuit, as an abstract gate list shared by every backend
# --------------------------------------------------------------------------

def compiled_gates(m: int, aqft_cutoff: int | None = None):
    """[(kind, qubits, angle)] with qubits 0..m-1 controls, m the work.

    aqft_cutoff drops inverse-QFT phases with denominator power above
    the cutoff (approximate QFT): the smallest-angle entangling gates,
    which cost the most coherent error on hardware for the least
    interference (cf. Pavlidis & Floratos on truncation robustness)."""
    gates = [("x", (m,), None)]
    for i in range(m):
        gates.append(("h", (i,), None))
    for i in range(m):
        theta = 2 * math.pi * ((PHI * (1 << i)) % 1.0)
        gates.append(("cphase", (i, m), theta))
    fwd = []                       # mirror of build_qft_gates(2, m)
    for i in range(m):
        fwd.append(("h", (i,), None))
        for j in range(i + 1, m):
            if aqft_cutoff is not None and (j - i + 1) > aqft_cutoff:
                continue
            fwd.append(("cphase", (i, j), 2 * math.pi / 2 ** (j - i + 1)))
    for kind, q, a in reversed(fwd):
        gates.append((kind, q, None if a is None else -a))
    return gates


def entangling_count(m: int) -> int:
    return sum(1 for k, q, _ in compiled_gates(m) if len(q) == 2)


def success_mask(D: int, bits: int) -> np.ndarray:
    y = np.arange(D)
    dist = np.abs(y / D - PHI)
    dist = np.minimum(dist, 1 - dist)
    return dist <= 2.0 ** -(bits + 1)


def fejer(D: int) -> np.ndarray:
    """Analytic noiseless control distribution P(y)."""
    y = np.arange(D)
    delta = PHI - y / D
    num = np.sin(np.pi * D * delta) ** 2
    den = np.sin(np.pi * delta) ** 2
    return np.where(den < 1e-300, 1.0, num / np.maximum(den, 1e-300)) / D ** 2


# --------------------------------------------------------------------------
# Backends
# --------------------------------------------------------------------------

def braket_circuit(m: int, device_gates: bool = False,
                   aqft_cutoff: int | None = None):
    """device_gates=True replaces cphaseshift (unsupported on IonQ
    Forte) by the equivalent rz(t/2) rz(t/2) zz(-t/2), equal up to
    global phase; both variants are checked against the analytic
    distribution in `validate`."""
    from braket.circuits import Circuit
    circ = Circuit()
    for kind, q, a in compiled_gates(m, aqft_cutoff):
        if kind == "x":
            circ.x(q[0])
        elif kind == "h":
            circ.h(q[0])
        elif device_gates:
            ra, rb, t = a / 2, a / 2, _wrap(-a / 2)
            if abs(t) > math.pi / 2:      # IonQ ZZ limit: |angle| <= pi/2
                ra, rb = ra + math.pi, rb + math.pi
                t -= math.copysign(math.pi, t)
            circ.rz(q[0], _wrap(ra)).rz(q[1], _wrap(rb))
            circ.zz(q[0], q[1], t)
        else:
            circ.cphaseshift(q[0], q[1], a)
    return circ


def _wrap(t: float) -> float:
    """Reduce an angle to (-pi, pi] (gates are 2*pi-periodic up to
    global phase)."""
    t = math.fmod(t, 2 * math.pi)
    if t > math.pi:
        t -= 2 * math.pi
    elif t <= -math.pi:
        t += 2 * math.pi
    return t


def control_distribution_local(m: int, device_gates: bool = False) \
        -> np.ndarray:
    """Exact control-register distribution from the local simulator."""
    from braket.devices import LocalSimulator
    circ = braket_circuit(m, device_gates)
    circ.probability(target=list(range(m)))
    res = LocalSimulator().run(circ, shots=0).result()
    return np.asarray(res.values[0])


def predict_exact_dm(m: int, bits: int, strength: float,
                     convention: str,
                     aqft_cutoff: int | None = None) -> float:
    """Exact DM success of the compiled circuit under depolarizing noise."""
    from qudit_shor import channels_by_cost, control_probs, run_circuit
    H = np.array([[1, 1], [1, -1]]) / np.sqrt(2)
    X = np.array([[0, 1], [1, 0]], dtype=complex)

    def unitary(kind, a):
        if kind == "x":
            return X
        if kind == "h":
            return H.astype(complex)
        return np.diag([1, 1, 1, np.exp(1j * a)])

    cost_1q = 1.0 if convention == "paper" else ONEQ_LAYER
    gates = [(q, unitary(k, a), 1.0 if len(q) == 2 else cost_1q)
             for k, q, a in compiled_gates(m, aqft_cutoff)]
    dims = [2] * (m + 1)
    D = 1 << m
    psi = np.zeros(2 ** (m + 1))
    psi[0] = 1.0
    rho = np.outer(psi, psi).astype(complex).reshape(dims + dims)
    E = channels_by_cost(2, gates, "depolarizing", strength)
    rho = run_circuit(dims, gates, rho, E)
    probs = control_probs(rho, 2, m, 1)
    return float(probs[success_mask(D, bits)].sum())


# --------------------------------------------------------------------------
# Modes
# --------------------------------------------------------------------------

def mode_validate() -> bool:
    ok = True
    for m, bits in CONFIGS:
        D = 1 << m
        ref = fejer(D)
        for dg in (False, True):
            p = control_distribution_local(m, dg)
            dev = float(np.abs(p - ref).max())
            succ = float(p[success_mask(D, bits)].sum())
            label = "device-gate" if dg else "cphaseshift"
            print(f"m={m} [{label}]: entangling gates = "
                  f"{entangling_count(m)}, max |P - Fejer| = {dev:.2e}, "
                  f"noiseless success(b={bits}) = {succ:.4f}")
            ok &= dev < 1e-9
    print("VALIDATION", "PASSED" if ok else "FAILED")
    return ok


def mode_predict(strengths):
    rows = []
    print(f"{'m':>2} {'b':>2} {'conv':>6} " +
          " ".join(f"s={s:<7g}" for s in strengths))
    # (m, bits, aqft_cutoff): the two full circuits, plus the truncated
    # 25-entangling-gate AQFT variant actually submitted (cutoff 5, see
    # results/braket_task_main_m7aqft.json).
    for m, bits, aqft in [(m, b, None) for m, b in CONFIGS] + [(7, 5, 5)]:
        for conv in ("paper", "timed"):
            succ = [predict_exact_dm(m, bits, s, conv, aqft)
                    for s in strengths]
            rows.append({"m": m, "bits": bits, "convention": conv,
                         "aqft_cutoff": aqft,
                         "strengths": list(strengths), "success": succ})
            print(f"{m:>2} {bits:>2} {conv:>6} aqft={str(aqft):>4} " +
                  " ".join(f"{x:<9.4f}" for x in succ))
    os.makedirs(RESULTS, exist_ok=True)
    with open(os.path.join(RESULTS, "braket_anchor_predictions.json"),
              "w") as f:
        json.dump({"phi": PHI, "oneq_layer": ONEQ_LAYER, "rows": rows},
                  f, indent=1)
    print("wrote results/braket_anchor_predictions.json")


def mode_sv1(shots: int = 10000):
    """SV1 requires shots >= 1 for the probability result type, so this
    is a sampled check: agreement within a few sigma_bin of the analytic
    value validates the cloud submission path end to end."""
    from braket.aws import AwsDevice
    dev = AwsDevice("arn:aws:braket:::device/quantum-simulator/amazon/sv1")
    for m, bits in CONFIGS:
        circ = braket_circuit(m)
        circ.probability(target=list(range(m)))
        res = dev.run(circ, shots=shots).result()
        p = np.asarray(res.values[0])
        succ = float(p[success_mask(1 << m, bits)].sum())
        ref = float(fejer(1 << m)[success_mask(1 << m, bits)].sum())
        sig = math.sqrt(ref * (1 - ref) / shots)
        print(f"SV1 m={m}: success = {succ:.4f} "
              f"(analytic {ref:.4f}, {abs(succ - ref) / sig:.1f} sigma, "
              f"{shots} shots)")


def _submit_batch(jobs, confirmed: bool):
    """jobs: [(label, m, bits, shots, aqft_cutoff, debias)]."""
    cost = sum(PER_TASK + PER_SHOT * j[3] for j in jobs)
    names = ", ".join(j[0] for j in jobs)
    print(f"Would submit {len(jobs)} tasks [{names}] to Forte-1 "
          f"-> ${cost:.2f}")
    if not confirmed:
        print("Refusing: pass --yes-spend-money to actually submit.")
        return
    from braket.aws import AwsDevice
    from braket.error_mitigation import Debias
    dev = AwsDevice(FORTE_ARN)
    for label, m, bits, shots, aqft, debias in jobs:
        kw = ({"device_parameters": {"errorMitigation": Debias()}}
              if debias else {})
        circ = braket_circuit(m, device_gates=True, aqft_cutoff=aqft)
        task = dev.run(circ, shots=shots, **kw)
        print(f"submitted {label}: {task.id}")
        with open(os.path.join(RESULTS, f"braket_task_{label}.json"),
                  "w") as f:
            json.dump({"label": label, "m": m, "bits": bits,
                       "shots": shots, "aqft_cutoff": aqft,
                       "debias": debias, "task_arn": task.id}, f, indent=1)


def mode_submit(shots: int, confirmed: bool):
    _submit_batch([(f"m{m}", m, bits, shots, None, False)
                   for m, bits in CONFIGS], confirmed)


def mode_probe(confirmed: bool):
    """Endianness probe: m=4, raw (no debiasing -- debiasing symmetrizes
    qubit assignments and would mask the mapping). Ideal peak y=10
    ('1010'); digit reversal would show it at y=5 ('0101')."""
    _submit_batch([("probe_m4", 4, 3, 500, None, False)], confirmed)


def mode_main(confirmed: bool):
    """The debiased main run: full m=5 and m=7, plus the AQFT-truncated
    m=7 (cutoff 5 drops the three smallest inverse-QFT angles)."""
    _submit_batch([("main_m5", 5, 4, 5000, None, True),
                   ("main_m7", 7, 5, 5000, None, True),
                   ("main_m7aqft", 7, 5, 5000, 5, True)], confirmed)


def mode_fetch():
    """Retrieve completed QPU tasks and score them against predictions."""
    import glob
    from braket.aws import AwsQuantumTask
    out = []
    for path in sorted(glob.glob(os.path.join(RESULTS,
                                              "braket_task_*.json"))):
        with open(path) as f:
            rec = json.load(f)
        m, bits = rec["m"], rec["bits"]
        task = AwsQuantumTask(rec["task_arn"])
        if task.state() != "COMPLETED":
            print(f"{rec.get('label', f'm{m}')}: {task.state()}, skipping")
            continue
        counts = task.result().measurement_counts
        D = 1 << m
        mask = success_mask(D, bits)
        shots = sum(counts.values())
        succ = work_ok = 0
        for bstr, n in counts.items():
            y = int(bstr[:m], 2)          # qubit 0 = MSB (validated)
            if mask[y]:
                succ += n
            if bstr[m] == "1":
                work_ok += n
        p = succ / shots
        err = math.sqrt(p * (1 - p) / shots)
        # IonQ returns the control register digit-reversed relative to
        # the local simulator (empirically: the m=5 peak sits exactly on
        # the bit-reversed ideal outcome); score both readings.
        succ_rev = sum(n for b, n in counts.items()
                       if mask[int(b[:m][::-1], 2)])
        p_rev = succ_rev / shots
        noiseless = float(fejer(D)[mask].sum())
        floor = float(mask.mean())
        row = {"label": rec.get("label", f"m{m}"), "m": m, "bits": bits,
               "aqft_cutoff": rec.get("aqft_cutoff"),
               "debias": rec.get("debias", False),
               "shots": shots, "success": p,
               "stderr": err, "success_bitreversed": p_rev,
               "stderr_bitreversed": math.sqrt(p_rev * (1 - p_rev) / shots),
               "work_qubit_one": work_ok / shots,
               "noiseless": noiseless, "floor": floor,
               "signal": (p - floor) / (noiseless - floor),
               "signal_bitreversed": (p_rev - floor) / (noiseless - floor),
               "task_arn": rec["task_arn"]}
        out.append(row)
        print(f"{row['label']}: success = {p:.4f} ± {err:.4f}  "
              f"bit-reversed = {p_rev:.4f}  "
              f"work-qubit |1> = {row['work_qubit_one']:.4f}  "
              f"({shots} shots)")
    with open(os.path.join(RESULTS, "braket_pilot_results.json"), "w") as f:
        json.dump(out, f, indent=1)
    print("wrote results/braket_pilot_results.json")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", default="validate",
                    choices=["validate", "predict", "sv1", "submit",
                             "fetch", "probe", "main"])
    ap.add_argument("--shots", type=int, default=1000)
    ap.add_argument("--strengths", type=float, nargs="+",
                    default=[0.005, 0.007, 0.010])
    ap.add_argument("--yes-spend-money", action="store_true")
    args = ap.parse_args()
    if args.mode == "validate":
        raise SystemExit(0 if mode_validate() else 1)
    if args.mode == "predict":
        mode_predict(args.strengths)
    elif args.mode == "sv1":
        mode_sv1()
    elif args.mode == "fetch":
        mode_fetch()
    elif args.mode == "probe":
        mode_probe(args.yes_spend_money)
    elif args.mode == "main":
        mode_main(args.yes_spend_money)
    else:
        mode_submit(args.shots, args.yes_spend_money)


if __name__ == "__main__":
    main()
