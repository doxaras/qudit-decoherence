# The transmon: physical implementation and state of the art

Why this document: our "ladder" noise model is named after this device.
This explains what a transmon physically is, why its noise has the ladder
structure we simulate, what the field has demonstrated (qubit and qudit
mode), and how the measured numbers calibrate our model.

---

## 1. What a transmon physically is

A transmon is a **superconducting anharmonic oscillator**: an LC circuit
in which the inductor is replaced by a **Josephson junction** — two
aluminum superconductors separated by a ~1 nm aluminum-oxide barrier
through which Cooper pairs tunnel coherently. The junction contributes a
*nonlinear* inductance, so instead of the evenly spaced levels of a
harmonic oscillator, the circuit has levels

E_m ≈ m·ℏω₀₁ − (m(m−1)/2)·E_C,

i.e. each higher transition is shifted down by the **anharmonicity**
α ≈ −E_C ≈ −200 to −340 MHz (our library's devices: −260 to −275 MHz)
relative to ω₀₁/2π ≈ 4–6 GHz. Those unequally spaced levels are what make
it usable as a qubit (|0⟩,|1⟩) — or a qutrit/ququart (|2⟩,|3⟩), since the
higher levels exist for free.

The design parameter is the ratio of Josephson to charging energy,
**E_J/E_C ≈ 50–100** ("transmon regime"). Large E_J/E_C exponentially
suppresses sensitivity to stray charge noise — the reason the transmon
displaced the older charge qubit — at the cost of the small anharmonicity
that limits how fast you can drive one transition without touching its
neighbors.

Operating environment: a **dilution refrigerator at ~10–20 mK** (so that
ℏω ≫ k_BT and the thermal population of |1⟩ is small — though not zero:
one device in our library ran at an effective 44 mK with 25% thermal
population). Control is entirely by **microwave pulses** sent down
attenuated coax lines; readout is **dispersive**: the qubit shifts the
frequency of a coupled readout resonator by a state-dependent amount, and
a weak microwave probe of the resonator reveals the state without
absorbing the qubit's energy.

Gates: single-qubit rotations are resonant microwave pulses (~10–50 ns,
fidelity 99.9%+); two-qubit gates couple neighboring transmons via a bus
resonator or tunable coupler — cross-resonance (fixed-frequency, IBM) or
CZ via flux tuning (Google) — at ~20–300 ns and 99.5–99.9% fidelity on
current hardware.

## 2. Why transmon noise is a "ladder"

Two physical facts create the level-dependent noise structure our model
simulates:

**Relaxation: bosonic enhancement.** The transmon is close to a harmonic
oscillator, so its coupling to the electromagnetic environment goes
through the ladder operator a with matrix elements ⟨m−1|a|m⟩ = √m. Decay
rates therefore grow with level: Γ_{m→m−1} ≈ m·Γ₁. **Measured reality
(9 devices in our library): ratio Γ₂₁/Γ₁₀ ≈ 1.7 mean (spread 1.1–2.1),
and the d = 4 data fits Γ_k ∝ k^0.68** — the ladder is real but
sublinear, because the environment's spectral density differs at the
(lower) 1→2 transition frequency.

**Dephasing: charge dispersion explodes with level index.** The residual
charge sensitivity the transmon design suppresses comes back
exponentially fast in the level index: the charge dispersion of level m
grows roughly as (E_J/E_C)^(m/2) e^(−√(8E_J/E_C)) scaled by a
combinatorial factor — in practice **|2⟩ is ≥10× more charge-sensitive
than |1⟩** (measured: 12 kHz vs 261 Hz at E_J/E_C = 73; 102 kHz vs
<10 kHz at E_J/E_C = 50). Blok et al. deliberately raised E_J/E_C from 50
to 73 specifically to make qutrit gates possible — at 50, the 1–2
coherence died in 5 µs. Measured pure-dephasing ratios: Γφ⁰²/Γφ⁰¹ ≈ 2.3
and Γφ¹²/Γφ⁰¹ ≈ 2.0 — i.e. **"anything involving level 2 dephases ~2×
faster" (a max-level law), not the (Δlevel)² law of a pure
frequency-fluctuation model.** Our simulation's (Δlevel)² model
over-penalizes the 0↔2 coherence and under-penalizes 1↔2; recalibration
is pre-publication task #1.

Additional channels our model omits: **cross-Kerr coupling** between
neighboring qudits (always-on conditional phase shifts, 0.1–0.7 MHz —
enough to take an unprotected two-qutrit Bell state to zero fidelity in
~1 µs; suppressible by dynamical decoupling), drive-induced AC-Stark
shifts of spectator levels (∝Ω², no qubit analogue), leakage during fast
pulses, and readout error growing with level (|0⟩ 0.97–0.99 vs |2⟩
0.92–0.96).

## 3. State of the art — transmon as qubit

(verified by live search, Aug 2026)

- **Scale & coherence**: IBM Nighthawk (120 qubits, 218 tunable
  couplers, square lattice) with **~350 µs median T1** — IBM's highest
  ever; Heron R3 at 156 qubits, T2 ~350 µs. Google Willow: 105 qubits,
  T1 68 µs mean. Lab record: **Princeton tantalum-on-silicon, T1 up to
  1.68 ms**, single-qubit fidelity 99.994% (Nature, Nov 2025).
- **Two-qubit gates**: Google Willow CZ error 0.33% (QEC chip) / 0.14%
  (iswap, RCS chip); IBM Heron-class median ~0.3% with >99.9% on more
  than half of tested pairs (late 2025).
- **Error correction milestones**: Willow's below-threshold surface code
  (Λ = 2.14 per distance step, logical lifetime 2.4× best physical
  qubit); magic-state cultivation at ~0.9999 fidelity (Dec 2025); IBM
  Loon demonstrating qLDPC "bicycle"-code components with <480 ns
  real-time decoding, fault tolerance targeted 2029.
- Gate times: single ~20 ns, two-qubit 30–300 ns; readout ~100–500 ns.

## 4. State of the art — transmon as qudit

From our paper library (see `docs/SOTA.md` §2 for full numbers):

- **d = 3 universal control**: single-qutrit RB 98.9% per Clifford
  (Kononenko, CSFQ variant); qutrit gates in 30 ns (Blok).
- **Best two-qutrit gate**: CZ† at 97.3% process fidelity, 580 ns
  (Goss 2022, cross-Kerr-activated) — a 4× error reduction over the
  previous best; synthesizes any two-qutrit unitary at depth ≤ 6.
- **Largest qudit algorithm on any hardware**: 5-qutrit
  teleportation/scrambling protocol, F = 0.568 vs 0.5 classical (Blok).
- **d = 4**: qudit dynamical decoupling demonstrated (Tripathi 2024);
  T1 = 53/34/24 µs for levels 1/2/3.
- **Bosonic route**: a transmon controlling a 3D microwave cavity gives
  qudits of d ≈ 10–20 photon-number states with T1 up to ~2 s for bare
  cavities; 5-year roadmap projects ~40 cavity modes at d ≈ 10
  (Venturelli 2025). The missing engineering component is a good CSUM
  entangling gate between cavity qudits.
- **Coherence hierarchy (measured, our library)**: T1⁰¹ 45–125 µs,
  T1¹² 28–63 µs, T1²³ 23–26 µs; T2e ratios 84 : 57 : 26 µs for
  01 : 12 : 23 coherences.
- **The frontier result (2025): d = 12 on a single transmon.** Wang,
  Parker, Champion & Blok (PR Applied 23, 034046): pushing E_J/E_C up
  to 325 gives 12 controllable levels, adjacent-subspace gate
  infidelities <3×10⁻³ across the lowest 10 levels, 10-state readout
  93.8% — and crucially **T2E close to the T1 limit for higher levels**.
  High-E_J/E_C design nearly eliminates the charge-dispersion dephasing
  penalty, leaving only the bosonic T1 ladder — i.e. a transmon can be
  *engineered toward* the regime where our simulations say qudits
  compete. This reframes the ladder model's dephasing term as a design
  parameter, not a law.

## 5. What this means for our project

- The transmon is the *hard case* for prime-d encodings: it is the one
  mainstream platform whose noise genuinely worsens with level index.
  Our ladder model captures the right physics but with the wrong
  exponents (k¹ vs measured k^0.7; (Δlevel)² vs measured max-level ≈2×).
  Since both errors overstate the qudit penalty, the calibrated re-run
  can only move our transmon conclusions *toward* qudits.
- Realistic per-gate noise strength on today's transmons: ~5×10⁻⁴
  (single-qutrit) to ~1–3×10⁻² (two-qutrit, dephasing-dominated) — our
  simulated sweeps bracket exactly this range.
- Dynamical decoupling and refocusing preferentially remove the
  dephasing component (and help more at higher d), so "transmon + echo"
  behaves closer to the per-particle model where qudits win — the DD-on
  simulation variant will quantify this.
