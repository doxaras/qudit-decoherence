# Physical experiments to verify our claims

Each of the paper's load-bearing claims maps to a measurable quantity on
real hardware. Ordered by feasibility — from things doable with cloud
access this month to full collaborations. Access routes verified by live
search, Aug 2026.

## Access reality check (verified)

- **IBM: closed.** Pulse-level control was removed from ALL IBM QPUs on
  2025-02-03 (`qiskit.pulse` deleted in Qiskit 2.0). Every published
  IBM-qutrit experiment predates this; none is reproducible there today.
- **Rigetti: the live cloud route.** Quil-T (QCS) and Amazon Braket
  Pulse expose pulse-level control on Cepheus-1-108Q (GA Apr 2026;
  99.1% median 2Q); Rigetti documented a qutrit `RX_12` gate set and
  |2⟩-adapted readout in 2021, and arXiv:2303.04261 (PR Applied 2024)
  demonstrated qutrit pulse compilation using Rigetti hardware and
  calibration data. **Open question to close first: whether f₁₂ frames
  survived the Aspen→Ankaa→Cepheus transitions** — a support ticket
  gates the plan.
- **IQM Pulla**: true pulse-level access, on-prem (DE/FI/FR) today,
  slated for the Resonance cloud — inquiry-worthy.
- **IQCC** (Israeli QC Center): remote research-grade superconducting
  lab with Quantum Machines OPX + QUA — everything needed to build an
  f₁₂ drive ourselves; quote-based. Possibly the least-constrained
  option.
- **AQT cloud is qubit-only**: the Innsbruck d=7 qudit processor
  (Ringbauer) is NOT the commercial product on Braket. E4 therefore
  requires an academic collaboration with Innsbruck, not a credit card.
- **Quantinuum/IonQ**: no physical qudit access (Quantinuum "qudits"
  are encoded in multiple qubits — useless for physical noise models).
- **NV kits: real and affordable.** Pulsed-capable options: spinEDU
  (Spinflex/Technion; 2–4 GHz 30 W pulsed bridge with AWG — T1/T2/
  tomography/DD) and qutools quEDU+quADD-NV (pulse streamer, 3-axis
  field coils) — both quote-only; a published full pulsed research
  build costs ~$18.6k (APL Materials 2024); a CW-only DIY ODMR rig is
  <€250 (Eur. J. Phys. 2023). Note qutools' older quNV is discontinued
  and CW-only — avoid.
- **Benchtop NMR: dead end.** SpinQ devices use spin-½ nuclei only; no
  commercial benchtop exposes a controllable spin-1 (deuterium) qutrit.
  NMR qutrits (oriented CDCl₃) need a university high-field facility.

## Claim → experiment map

| # | Claim of ours | Verifying measurement | Hardware | Feasibility |
|---|---------------|----------------------|----------|-------------|
| E1 | Transmon noise follows a sublinear T1 ladder (Γ_k ∝ k^0.7) and a max-level dephasing law (~2× for any \|2⟩-involving coherence), not (Δlevel)² | Per-level T1 (prepare \|k⟩, watch cascade) and pairwise Ramsey/echo T2 on 0↔1, 1↔2, 0↔2 | Rigetti Cepheus via Quil-T / Braket Pulse (pending f₁₂-frame confirmation); fallbacks IQCC (QUA/OPX), IQM Pulla | Days of work once access confirmed |
| E2 | Spin-1 (NV) noise is per-particle-like at B > 60 G; a 1/Δ² skip channel dominates at low field | Full 3×3 rate matrix (Ω₊, Ω₋, γ) vs magnetic field via selective ODMR on both \|0⟩→\|±1⟩ transitions | Pulsed NV kit: spinEDU or qutools quEDU+quADD-NV (quotes); DIY pulsed build ~$18.6k | Benchtop; ~weeks incl. setup |
| E3 | Base-d QFT accumulates less noise than the equivalent qubit QFT at matched precision | d=3 QFT (9 pulses) vs 2-qubit QFT on the same device; process fidelity comparison | Cloud transmon with pulse access, or molecular-qudit collaboration (Rubín-Osanz-style) | Medium |
| E4 | Eigenstate QPE at d=5 beats the qubit version at matched precision on per-particle hardware | Our qpe_generic circuit at m=2, d=5 (~8 two-qudit gates) vs d=2, m=5 equivalent | Ringbauer-class ion qudit processor (AQT/Innsbruck) — collaboration | The flagship; proposal-ready |
| E5 | DD/refocusing moves a transmon from ladder-model to per-particle-model behavior (qudits start winning) | Repeat E1/E3 with CPMG or qudit DD (Tripathi sequences) interleaved | Same as E1 | Small increment over E1 |
| E6 | Readout error grows with level and taxes qudit QPE | Per-level SPAM matrix (prepare \|k⟩, measure) | Any qutrit-capable backend | Trivial add-on |

## E1 in detail — the cheapest decisive experiment

Our publication's most exposed conclusion ("qubits win Shor on
transmon-like hardware") rests on the ladder noise model. The model is
calibrated today from three published devices (Goss, Blok, Tripathi);
measuring it ourselves on one more device would make the calibration
section partly first-party:

1. Calibrate the 1→2 transition frequency (ω₀₁ + α, α ≈ −250 MHz).
2. T1 ladder: prepare |2⟩ via π₀₁ then π₁₂; delay; measure populations
   with a discriminator trained on |0⟩,|1⟩,|2⟩ readout signatures. Fit
   the two-step cascade → Γ₂₁, Γ₁₀. Repeat for |3⟩ if drivable.
3. Dephasing: Ramsey and echo on the 0–1, 1–2, and 0–2 (two-photon or
   composite) coherences → Γφ ratios. Our model predicts 1 : 1 : 4
   (Δlevel² law); measured literature says ≈ 1 : 2 : 2.3 (max-level
   law). One afternoon of shots decides it.
4. Optional: repeat under CPMG (E5) to watch the ratios collapse toward
   uniform.

Analysis pipeline: the fitted (Γ₁ ladder exponent, Γφ vector) drop
directly into `transmon_superop` as a device-twin channel; re-running our
Shor/QPE scaling with the measured channel turns the paper's model
section into a hardware-validated one.

## E2 in detail — NV center rate matrix (benchtop)

The per-particle model's experimental basis for spin systems is
Gardill 2020 (5 NVs, nanodiamonds). A reproduction on a standard NV
ODMR setup measures, vs applied field B_z:

- Ω₊ (|0⟩↔|+1⟩) and Ω₋ (|0⟩↔|−1⟩) relaxation rates (selective π pulses
  on the two hyperfine-split ODMR lines, ~2.87 GHz ± γB),
- γ (|+1⟩↔|−1⟩ double-quantum rate) via the difference between
  single-quantum-prepared and double-quantum-prepared decay.

Verifies: (a) Ω₊ ≈ Ω₋ (no ladder asymmetry — per-particle confirmed);
(b) γ(Δ) ∝ 1/Δ² at small splitting (the skip channel our models omit).
If (b) reproduces, the paper's NV discussion gains a first-party panel,
and the "optimal d vs field" curve (innovation direction E) becomes
publishable with data.

## E4 in detail — the flagship proposal

Eigenstate QPE at d = 5, m = 2 (25-point phase grid, ~4.6 bits):
circuit = 2 F₅ + 2 controlled-U powers + 2 F₅† + 1 CP ≈ **8 entangling
gates + 5 single-qudit gates**. At Ringbauer's measured Cinc fidelity
(93.8%) the whole-circuit survival is ≈ 0.938⁸ ≈ 60% — comfortably above
the ~3% random floor of the 5-bit window metric. The same phase estimated
with qubits needs 5 control qubits + deeper QFT ≈ 2.5–3× the entangling
count at lower per-gate error — the comparison is genuinely competitive,
and **no algorithm has ever been run on any qudit processor above
d = 3.** Deliverable we can produce from the repo today: gate list, cost
table, and predicted success probabilities under the calibrated ion
noise model, as a one-page proposal to an ion-trap group.

## Next actions (all cheap, all binary)

1. Email Rigetti support / QCS: are f₁₂ drive frames and `RX_12`
   calibrations exposed on Cepheus-1-108Q via Quil-T, and are
   custom-frequency frames permitted on Braket Pulse for that device?
2. Email IQM: Pulla-on-Resonance timeline; custom-frequency drive
   frames allowed?
3. Email IQCC: pricing for remote QUA/OPX access; multi-level drive
   permitted?
4. Request quotes: spinEDU (Spinflex) and quEDU+quADD-NV (qutools).
5. Read arXiv:2407.17407 (12-level transmon, PR Applied 2025) before
   finalizing the calibrated noise model — its "T2E ≈ T1 limit at high
   E_J/E_C" finding turns our dephasing term into a design parameter.

## What we cannot verify without a fab

The d-dependence of *cross-Kerr* coherent errors, scaling behavior past
d = 5 on transmons, and anything involving thousands of gates (real
factoring instances). These stay simulation-only and are labeled as such
in the paper.
