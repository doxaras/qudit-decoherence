# Hardware anchor: the qubit branch on real devices

> **Status: ✅ current.** This is the paper's Sec. IX. Raw shot
> histograms are committed to `results/braket_raw_counts.json`, so
> `braket_raw_analysis.py` reproduces every number below **without
> re-running hardware** (and without cost). The reinterpretation-search
> figure in Finding 2 was recomputed from those histograms and is
> **0.15**, superseding an earlier 0.21.

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
   reinterpretations: 0.15 — recomputed from the committed raw shot
   histograms by `braket_raw_analysis.py`; an earlier pass reported
   0.21, which is superseded. Either way it is not significant over so
   large a hypothesis set — in fact it is ~99σ above the
   multiplicity-corrected null of ≈0.04, so the output is structured,
   just structured *wrong*: far below the 0.42–0.54 prediction, with
   the scored peak shifted to y=84 against the ideal 79, a cyclic
   phase-offset signature no relabeling represents). The m=4 probe caught the mechanism: a
   nearly pure output (71% of shots on one outcome) whose phase is
   wrong by one least-significant digit — a popcount argument
   ('1101' has three 1s, the ideal '1010' two) rules out any qubit
   relabeling. Debiasing does not repair it; dropping the three
   smallest inverse-QFT angles (AQFT) recovers only ~6×. Past a depth
   threshold, decoded-success benchmarks on this hardware measure
   coherent calibration error, not decoherence.
3. **The superconducting lattice fails by routed decoherence plus one
   anomalous qubit.** SWAP-routing the all-to-all kickback pattern
   through fixed connectivity inflates 15/28 entangling gates to
   47/104 native CZs; exact-DM depolarizing over the routed circuits
   predicts the work-qubit decay (0.81 / 0.66 measured vs 0.79 / 0.66
   predicted at s ≈ 0.004; at the best-fit s ≈ 0.0035 the m=5 pair is
   0.814 / 0.808). At m=5 the control register's apparent
   deficit is a single *inverted* control qubit — the most heavily
   routed one (35 CZs); with that bit corrected, routed decoherence
   reproduces success (0.377 vs 0.353, inside the 0.18–0.42 band) and
   the full histogram (TV = 0.09). The m=7 control register sits on
   the random floor and carries no information. The hardware face of
   the paper's `pavlidis` lesson. (Follow-up DONE: the S3 result
   objects were re-fetched — `braket_fetch_s3_metadata.py`, stored as
   `results/braket_s3_garnet_m*.json`. They confirm the bit order and
   the counts exactly, and localize the inversion to the *end* of the
   qubit's sequence: a terminal flip fits at TV 0.09 against 0.24+ for
   any insertion before its last two CZs (sampling noise 0.027). A π
   accumulated through the routed sequence is excluded; a static
   qubit-local readout mis-assignment is excluded model-independently
   — the two tasks ran in overlapping execution windows and disagree
   about the same qubit, whose predicted P(c0=1) exceeds 1/2 at every
   depolarizing strength while the m=5 measurement gives 0.332. What
   remains: a coherent π in the closing rotations, or a readout
   inversion that depends on the differing multiplexed readout sets.
   Note for re-fetchers: `taskMetadata.deviceParameters` carries a
   simulator schema name — a Braket envelope quirk, not a simulator
   run; `deviceId` and `iqmMetadata` settle it.)

   **Deciding experiments run 2026-09-02** (~$9 on-device; task ARNs in
   `results/braket_cal_q10_tasks.json`, `braket_m5_rerun_task.json`):

   1. *Configuration-matched calibration* (same six qubits, same
      measure map, 3 × 1000 shots): $10 discriminates correctly today —
      P(1|0)=0.007, P(1|1)=0.988, and 0.96–0.98 even with all six
      qubits excited (`results/braket_s3_cal_*`). A persistent
      multiplexed-readout inversion is out.
   2. *Byte-identical program re-run* (sha256-matched compiled program,
      1000 shots, `results/braket_s3_garnet_m5_rerun_results.json`):
      reproduces the phenomenon on a **different qubit** — $10 normal
      (0.730 vs 0.693 predicted), $15 fully inverted (0.360 vs 0.637;
      prediction >½ at every strength). Work qubit 0.802 → s ≈ 0.0037,
      consistent with August. So the inversion is stochastic per run,
      not qubit-specific and not a deterministic artifact of the
      compiled sequence — which rules out the coherent-π-as-compilation-
      artifact reading and leaves a device-side stochastic fault,
      readout or control, that three clean single-gate calibration
      circuits do not exclude. **Caveat:** the bit2-corrected re-run
      fits the model materially worse than August's bit0-corrected data
      (TV 0.21 vs 0.09, against sampling noise 0.058 vs 0.027; success
      0.245 vs 0.297 predicted, 3.8σ low where August was 3.6σ high).
      Terminality was established for August only — at 1000 shots the
      X-injection scan cannot localize the $15 flip (interior and
      terminal positions all within 0.213–0.256).
   3. *Third run* (2026-09-02, 5000 shots,
      `results/braket_s3_garnet_m5_rerun5k_results.json`): **no
      inversion** — all five control bits normal, every single-bit
      flip worsens the fit (TV 0.39–0.49 vs 0.12), ideal peak dominant
      at P(y=20)=0.226. Noisier epoch — work ⟨1⟩ = 0.717 → s ≈ 0.006,
      vs 0.0035 (Aug) and 0.0037 (Sep 2 early). The run still does
      not fit: misfit 0.117 against sampling noise 0.028, with $16
      high by 9.5σ at s_work and 16σ at s_hist, and no single
      strength reconciling the work qubit (s ≈ 0.006), the histogram
      (0.0045) and $16 (0.0097).

   **Tally over three deep runs of the identical program:** $10
   inverted / $15 inverted / none — plus 0 of 3 shallow calibration
   runs. Fisher one-sided p = 0.20 for the deep-vs-shallow contrast,
   and the per-run rate 2/3 has a 95% CI of [0.09, 0.99]. Real and
   recurring, but the rate and the trigger are uncharacterized, and
   the deep/shallow comparison is confounded (depth, duration, gate
   count and entanglement all differ). **The practical lesson for
   single-shot hardware anchors: on this device the m=5 output varied
   run to run by more than its counting statistics, so quantitative
   agreement from one execution should not be read as a measurement
   of the channel.**

## Device conventions worth knowing (cost us three failed submissions)

- IonQ Forte rejects `cphaseshift`; compile as
  Rz(θ/2) ⊗ Rz(θ/2) · ZZ(−θ/2) (equal up to global phase).
- IonQ ZZ accepts only |θ| ≤ π/2; fold the excess into paired Rz(π)
  rotations (ZZ(t±π) ≅ Rz(π)⊗Rz(π)·ZZ(t)).
- IonQ returns the control register **digit-reversed** relative to the
  Braket local simulator (the m=5 peak sits exactly on the
  bit-reversed ideal outcome; IonQ scoring uses that reading, IQM
  the plain one — fixed per platform by the noiseless-parse check).
  The work qubit position is unaffected.
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
