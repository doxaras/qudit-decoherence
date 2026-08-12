# Hardware anchor: the qubit branch on real devices

Paper Sec. "Hardware anchor". The qubit rows of the paper's prediction
table compile at face-value gate counts on cloud hardware: one work
qubit prepared in the eigenstate, each controlled-U^(2^i) a single
controlled-phase, the no-swap inverse QFT adding m(m−1)/2 more — 15
entangling gates at m = 5 (6 qubits), 28 at m = 7 (8 qubits). All runs
went through AWS Braket in August 2026 with `braket_qpe_anchor.py`
(modes: `validate` / `predict` / `sv1` / `probe` / `submit` / `main` /
`fetch`; QPU submission is double-guarded behind `--yes-spend-money`).

## Predictions (compiled circuits, exact density matrix)

Per-qubit depolarizing at per-gate strength s; two exposure
conventions bracket the hardware (*paper*: every gate a full noise
layer; *timed*: 1Q gates charged their 130/970 duration ratio).
`results/braket_anchor_predictions.json`.

| Circuit | b | s=0.005 | s=0.007 | s=0.010 |
|---|---|---|---|---|
| m=5 (paper/timed) | 4 | 0.673 / 0.754 | **0.599 / 0.699** | 0.505 / 0.625 |
| m=7 (paper/timed) | 5 | 0.531 / 0.640 | **0.422 / 0.542** | 0.306 / 0.428 |
| m=7 AQFT (paper/timed) | 5 | 0.549 / 0.662 | **0.443 / 0.570** | 0.327 / 0.460 |

## Results

| Device | Circuit | Shots | Predicted (s=0.007) | Measured | Work qubit |
|---|---|---|---|---|---|
| IonQ Forte-1 | m=5 pilot (raw) | 1,000 | 0.60–0.70 | 0.608 ± 0.015 | 0.97 |
| IonQ Forte-1 | m=4 probe (raw) | 500 | ~0.8 | 0.108 (peak 1 LSB off) | 0.95 |
| IonQ Forte-1 | m=5 main (debiased) | 5,000 | 0.60–0.70 | **0.617 ± 0.007 — in band** | 0.99 |
| IonQ Forte-1 | m=7 main (debiased) | 5,000 | 0.42–0.54 | 0.011 (below floor 0.031) | 0.99 |
| IonQ Forte-1 | m=7 AQFT (debiased) | 5,000 | 0.44–0.57 | 0.066 | 0.99 |
| IQM Garnet | m=5 | 5,000 | — | 0.080 (floor 0.063) | 0.81 |
| IQM Garnet | m=7 | 5,000 | — | 0.032 (floor 0.031) | 0.66 |

Success scored as the phase correct to b bits, in the digit-reversed
reading (below). `results/braket_pilot_results.json` and
`results/braket_task_*.json` hold per-task records.

## Findings

1. **The shallow ion circuit validates the paper's noise convention
   quantitatively.** 0.617 ± 0.007 against the predicted 0.60–0.70;
   the steep success-vs-strength map pins the device's effective
   per-gate depolarizing strength at 0.007–0.009, bracketing IonQ's
   vendor-reported 0.7% two-qubit infidelity.
2. **The deep ion circuit fails coherently, not by decoherence.** The
   work qubit stays at 0.99 while the interference peak is destroyed;
   no relabeling of outcome bits recovers it (best of 10,080
   reinterpretations: 0.21). The m=4 probe caught the mechanism: a
   nearly pure output (71% of shots on one outcome) whose phase is
   wrong by one least-significant digit — a popcount argument
   ('1101' has three 1s, the ideal '1010' two) rules out any qubit
   relabeling. Debiasing does not repair it; dropping the three
   smallest inverse-QFT angles (AQFT) recovers only ~6×. Past a depth
   threshold, decoded-success benchmarks on this hardware measure
   coherent calibration error, not decoherence.
3. **The superconducting lattice fails by plain decoherence.** Both
   circuits at the random floor with the work qubit visibly decayed
   (0.81 / 0.66): SWAP-routing the all-to-all kickback pattern through
   fixed connectivity, against a T2 four to five orders shorter than
   the ions'. The hardware face of the paper's `pavlidis` lesson.

## Device conventions worth knowing (cost us three failed submissions)

- IonQ Forte rejects `cphaseshift`; compile as
  Rz(θ/2) ⊗ Rz(θ/2) · ZZ(−θ/2) (equal up to global phase).
- IonQ ZZ accepts only |θ| ≤ π/2; fold the excess into paired Rz(π)
  rotations (ZZ(t±π) ≅ Rz(π)⊗Rz(π)·ZZ(t)).
- IonQ returns the control register **digit-reversed** relative to the
  Braket local simulator (the m=5 peak sits exactly on the
  bit-reversed ideal outcome; scoring uses that pre-registered
  reading). The work qubit position is unaffected.
- SV1 rejects probability result types at shots=0; sample instead.
- IQM Garnet supports `cphaseshift` natively; Rigetti Ankaa-3 is
  retired despite appearing in the pricing catalog.
- Every compiled variant was validated against the analytic Fejér
  distribution to 1e-15 on the local simulator before submission.

## Cost

SV1 ~$1; pilot $160.60; probe $40.30; Garnet $15.10; debiased main
batch $1,200.90 — **total ≈ $1,418** at $0.08/shot + $0.30/task
(Forte-1) and $0.00145/shot (Garnet). Two validation-failed
submissions and one queued-then-cancelled batch incurred no charge.
