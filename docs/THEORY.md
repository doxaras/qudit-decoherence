# Prime-dimensional qudits, decoherence, and Shor's algorithm

This document is the physics background for the simulator in this repo. It
answers three questions:

1. What physical systems can store quantum information in a prime base
   (qutrit, d = 3; ququint, d = 5) rather than a qubit (d = 2)?
2. Why do *prime* dimensions matter mathematically?
3. How does moving to higher d change the decoherence budget of an
   algorithm — concretely, of Shor's order finding?

---

## 1. Physical platforms for prime-d qudits

A qudit is any quantum system with d well-controlled, individually
addressable levels. The realistic candidates:

**Trapped ions.** The current state of the art for universal qudit
computing. Ringbauer et al. (*A universal qudit quantum processor with
trapped ions*, Nature Physics 18, 2022) ran a ⁴⁰Ca⁺ processor with up to
d = 7 levels per ion, using Zeeman/optical sublevels. Crucially, the
levels are spectroscopically resolved but *energetically similar*: no level
is intrinsically much noisier than another, so decoherence is paid roughly
**per ion and per unit time, not per level**. This is the platform our
"depolarizing" noise model represents, and it is the regime where qudits
win.

**Superconducting transmons.** A transmon is a weakly anharmonic
oscillator; levels |2⟩, |3⟩, |4⟩ exist above the qubit subspace and qutrit
processors have been demonstrated (e.g. Blok et al., PRX 2021; Google's
qutrit work). But the ladder structure fixes the noise: multi-photon decay
gives level |k⟩ a relaxation rate ≈ k·γ₁ (T₁ of |4⟩ is ~4× worse than
|1⟩), and frequency noise dephases coherences between levels j, k at a rate
growing like (j−k)². Higher levels are strictly worse. This is our
"transmon" noise model.

**NV centers and spin-1 defects.** The nitrogen-vacancy ground state is a
native spin-1 (S = 1) system — a *natural qutrit* with |m = −1, 0, +1⟩,
room-temperature coherence, and no "borrowed" levels. Molecular spin qudits
(e.g. TbPc₂ single-molecule magnets with a d = 4 nuclear-spin register,
and engineered molecular d = 5 spins) are an active chemistry-driven route.

**Photonics.** Orbital angular momentum, time-bin, and path encodings make
high d natural (d > 100 demonstrated for entanglement). Decoherence is
dominated by loss, which is level-independent for time bins — another
"per-particle" noise platform — but two-qudit gates are the hard part.

**Rydberg atoms and bosonic cavity modes** round out the list; cavity
qudits (Fock encodings) share the transmon's ladder problem (loss rate ∝
photon number).

**Recommendation for a physical build.** For a first prime-d system aimed
at algorithm experiments: a *trapped-ion qudit* (following the Innsbruck
architecture) if you want d = 3 and d = 5 in the same hardware with
per-particle noise; an *NV center* if you want a cheap, room-temperature
native qutrit for storage/metrology experiments rather than multi-qudit
algorithms.

---

## 2. Why prime d is special

For prime d the integers mod d form a field, 𝔽_d, and a surprising amount
of quantum information machinery only works cleanly in that case:

- **Generalized Paulis.** X|j⟩ = |j+1 mod d⟩, Z|j⟩ = ω^j |j⟩ with
  ω = e^{2πi/d}. These generate the qudit Pauli group; for prime d its
  quotient is the vector space 𝔽_d², and symplectic structure over a field
  gives the whole stabilizer formalism (Gottesman 1999) essentially for
  free.
- **Mutually unbiased bases.** A d-level system admits at most d + 1
  mutually unbiased bases, and the maximal set is *known to exist exactly
  when d is a prime power*, with the prime case cleanest. MUBs are the
  backbone of optimal state tomography and robust qudit QKD.
- **Discrete Wigner functions.** For odd prime d there is a unique
  covariant discrete Wigner function (Gross 2006); negativity of it is the
  resource for quantum speedup, which makes odd-prime qudits the natural
  home of the "magic" resource theory.
- **Magic-state distillation.** Qutrit codes give distillation routines
  with exceptionally clean structure and, in some constructions, better
  thresholds/overhead than qubit codes (Campbell, Anwar & Browne, PRX
  2012; Campbell 2014).
- **Error correction.** Qudit surface codes over 𝔽_d have higher error
  thresholds against depolarizing noise as d grows, and qudit stabilizer
  codes need fields, i.e. prime(-power) d.

Composite d (say d = 4 or 6) breaks the field structure: Z_6 has zero
divisors, the symplectic formalism degrades, and maximal MUB sets are not
even known to exist for d = 6. That is why the interesting qudit program is
run at d = 3, 5, 7, …

---

## 3. Shor's algorithm in base d

Order finding is base-agnostic: the control register is any group Z_D, the
QFT is over Z_D, and D = d^m just needs to be large enough. Moving from
qubits to qudits changes only the *resource accounting*:

- **Register size.** You need m = ⌈log_d D⌉ control qudits instead of
  log₂ D qubits: a factor log₂ d fewer particles (≈ 1.58× for qutrits,
  2.32× for ququints).
- **QFT depth.** The no-swap QFT circuit is m single-qudit Fourier gates
  plus m(m−1)/2 two-qudit controlled phases — quadratic in m, so the gate
  count falls by ≈ (log₂ d)² (≈ 2.5× for d = 3, ≈ 5.4× for d = 5).
- **Modular exponentiation.** Controlled multipliers act on a work
  register of w = ⌈log_d N⌉ qudits; both the number of controlled stages
  (m) and the width of each stage (w) shrink.

For the N = 15, a = 7 instance simulated here (control dim ≥ 64, work
dim ≥ 15):

| base | control × work qudits | gates | serial time-layers |
|------|----------------------|-------|--------------------|
| d = 2 | 6 + 4 = 10 | 33 | 51 |
| d = 3 | 4 + 3 = 7  | 18 | 26 |
| d = 5 | 3 + 2 = 5  | 12 | 15 |

Fewer particles, fewer entangling gates, and a ~3.4× shorter serial
schedule at d = 5. **If noise were purely per-particle-per-time, this would
be a pure win.** The question is what the extra levels cost.

---

## 4. The decoherence tradeoff

> **SUPERSEDED (Aug 2026):** The Shor-specific findings in this section —
> the demo-scale transmon-vs-per-particle comparison, the "honest
> conclusions" below (in particular conclusion 2, "on ladder platforms
> ... prime-d encodings are a clear loss"), and the scaling study that
> follows it — were all measured on a single instance, N = 15, a = 7. Its
> multiplicative group is ℤ₂ × ℤ₄, so every possible order is a power of
> two; the control register therefore always lands on exact QFT grid
> points in base 2 and never in base 3 or 5, a structural bias with
> nothing to do with decoherence. The confound was discovered in
> `docs/MECHANISM.md` and controlled for by re-running every Shor study
> on unbiased instances in `docs/GRID_ALIGNMENT.md`. **On unbiased
> instances, qudits beat qubits at Shor under every noise model tested
> (transmon idealized, transmon calibrated, depolarizing), at every noise
> strength and every register size — the opposite ordering from
> conclusion 2 below.** The text is kept for its historical role — it is
> what motivated the calibrated noise model and the later discoveries —
> but every Shor-specific number, ranking, and "law" derived from it in
> this section should be read as retracted and replaced by
> `docs/GRID_ALIGNMENT.md`. (QPE-only material below is unaffected — the
> golden-ratio target phase was chosen to be alignment-free from the
> start.)

Write the per-qudit information content as log₂ d "qubits' worth". The
tradeoff has a clean back-of-envelope form:

- **Ladder platforms (transmon-like).** The average relaxation rate over
  the d levels grows like ⟨k⟩γ₁ ≈ (d−1)/2 · γ₁, and worst-case dephasing
  between the extreme levels grows like (d−1)²·γ_φ. Information capacity
  grows only like log₂ d. So per stored qubit-equivalent, raw idle
  decoherence gets *worse* roughly linearly (relaxation) to quadratically
  (dephasing) in d. Qudits can still come out ahead only if the *circuit
  compression* (fewer gates, shorter schedule, fewer particles) outpaces
  this — which the simulation tests quantitatively.
- **Per-particle platforms (ion-like).** If each particle decoheres at a
  d-independent rate, then packing log₂ d qubits into it *divides* the
  error per logical unit of information, and the shorter circuit
  multiplies the win. Here qudits are favored on both axes.

Shor's algorithm is a good stress test for this because it is
*phase-critical*: success depends on interference across the whole control
register, so dephasing anywhere in the schedule directly erodes the
measured peak structure — it probes exactly the quantity (global phase
coherence over time × particles) that the tradeoff is about.

The simulation in `qudit_shor.py` makes both models concrete: identical
circuits, identical scoring (probability that continued fractions recover
the exact order r = 4), full density-matrix evolution, noise applied to
every qudit for every serial time-layer.

### What the simulation finds

A subtlety first: at this demo size, continued fractions "recover" the
order from a *uniformly random* outcome ~28–30% of the time, so the raw
success probability has a high floor. All quantitative statements below use
the floor-corrected signal (success − floor)/(noiseless − floor), which is
1 for the perfect run and 0 for a fully mixed register.

**Transmon-ladder noise: qubits win decisively.** At per-layer strength
0.01 the surviving signal is 0.68 (d = 2) vs 0.36 (d = 3) vs 0.17 (d = 5);
by 0.02 the qutrit and ququint are at or below the random floor while the
qubit machine still retains half its signal. The (d−1)² dephasing penalty
and k·γ relaxation overwhelm the 2–3.4× circuit compression. The slightly
*negative* values are real, not noise: amplitude damping drags the control
register toward |0…0⟩, actively biasing outcomes away from the good set.

**Per-particle depolarizing: nearly a wash, with a slight ququint edge.**
At strength 0.02 the signal is 0.33 (d = 2), 0.16 (d = 3), 0.37 (d = 5);
d = 5 stays marginally ahead of d = 2 across the range and d = 3 lags.
Naive accounting (qudit-layers × bits per qudit: 510p vs 288p vs 174p of
exposure) predicts a ~3× ququint advantage — most of it is eaten by two
effects: a depolarizing *event* on a big qudit destroys a whole particle's
worth (log₂ d qubit-equivalents) of the register at once, and small-
register artifacts (D = 64 is exactly divisible by r = 4, giving d = 2
maximally concentrated, robust peaks; the d = 3 work register carries the
largest fraction of unused leakage states, 12 of 27).

The honest conclusions:

1. **The noise structure of the hardware, not the algorithm, decides the
   question.** The same circuits under two noise models give opposite
   orderings.
2. **On ladder platforms (transmons, cavity Fock encodings), prime-d
   encodings are a clear loss** for phase-critical circuits like Shor.
3. **On per-particle platforms (trapped ions, NV, time-bin photonics),
   qudits break even at this scale** — you get the 2× particle and 3.4×
   depth savings for free, but no *additional* decoherence resilience at
   demo size. The exposure argument (fewer particles × fewer layers)
   scales with problem size while the per-event-damage penalty is a
   constant factor ~log₂ d, so the qudit advantage should grow for larger
   factoring instances — a concrete, testable prediction, tested below.

### The scaling study (prediction confirmed)

Using the quantum-trajectory engine (`trajectories.py`, validated against
the exact simulator to within 1σ), we swept the phase-estimation precision
from 6 to ~11.6 bits (control dimension D = 64 → 4096; registers up to 16
qubits / Hilbert dimension 78 125) at fixed noise strength
(`scaling_experiment.py`, `results/scaling.png`).

**Per-particle depolarizing (0.005/layer): the qudit advantage grows with
problem size, with a crossover.** The ququint's floor-corrected signal
falls at ≈ 0.022 per precision bit against ≈ 0.053/bit for qubits — the
d = 5 line overtakes d = 2 at ~7–8 bits and leads by ~0.16 (0.64 vs 0.48,
well outside error bars) at 12 bits. Extrapolated, a cryptographically
interesting instance (thousands of bits) would amplify this into a
decisive advantage. The qutrit narrows its gap to d = 2 with size but has
not crossed by 11 bits — the small-register artifacts that hurt d = 3
fade only slowly.

**Transmon-ladder noise (0.003/layer): the qubit advantage *widens* with
problem size.** The d = 2 signal is nearly flat beyond 10 bits (0.92 →
0.74) while d = 5 falls steadily (0.65 → 0.37); the ordering is monotone
in d at every size, exactly as the level-k decay structure predicts. No
crossover is coming: deeper circuits spend longer holding coherence on
levels that decay faster.

So the final refinement of conclusion 3: on per-particle-noise hardware,
prime-d encodings are not merely free — **their decoherence advantage
compounds with problem size**, which is precisely the regime that matters
for factoring.

### Beyond Shor: generic phase estimation

Shor is one member of the phase-estimation family (quantum chemistry
energy estimation, HHL, amplitude estimation share the same skeleton). To
test whether the conclusions are Shor-specific, `qpe_generic.py` swaps the
modular multipliers for controlled powers of an *arbitrary* 16-dim unitary
(random eigenbasis; target eigenphase pinned to the golden-ratio conjugate
so it is far from every fraction with a small base-2/3/5 denominator), the
work register starts in the target eigenvector, and success = "phase
correct to 5 bits" (random floor ≈ 2⁻⁵ — far cleaner than the
continued-fraction floor). Same registers, cost model, noise machinery,
and scaling grid (`qpe_scaling_experiment.py`, `results/qpe_scaling.png`).

Floor-corrected signal at ~7 / ~9.5 / ~11.6 bits of precision:

| noise | d = 2 | d = 3 | d = 5 |
|-------|-------|-------|-------|
| depolarizing 0.005 | 0.40 / 0.22 / 0.15 | 0.66 / 0.51 / 0.45 | 0.82 / 0.76 / 0.65 |
| transmon 0.003 | 0.56 / 0.30 / 0.26 | 0.70 / 0.54 / 0.51 | 0.74 / 0.67 / 0.60 |

Two findings:

1. **Under per-particle noise the qudit advantage generalizes and
   strengthens: d = 5 > d = 3 > d = 2 at every size, no crossover
   needed.** With a base-fair phase and metric, the qutrit also falls
   into its natural place between qubit and ququint — confirming that
   d = 3's poor showing in the Shor study was an artifact of that
   instance (D = 64 divisible by r = 4 gave d = 2 perfectly aligned
   peaks that continued fractions loves, and the d = 3 work register
   carried the largest leakage fraction).

2. **Under transmon-ladder noise the ordering FLIPS relative to Shor:
   qudits win here too.** This is the surprise, and the mechanism is
   instructive. In Shor the work register is *entangled* with the control
   (|c⟩|aᶜ mod N⟩): every amplitude-damping event on a work qudit carries
   which-path information and directly dephases the control register —
   and the base-2 work register only ever occupies its slow-decaying
   levels 0/1, while the base-5 work register lives on fast-decaying
   high levels. In eigenstate QPE the two registers remain in a product
   state under ideal evolution, so work-register noise carries no
   which-path information; it only hurts by leaking population out of
   the eigenvector. With that channel neutralized, the exposure
   advantage (fewer qudits × fewer layers) beats the ladder penalty on
   the control register at these strengths.

> **SUPERSEDED (Aug 2026):** The which-path-entanglement explanation in
> finding 2 above, and the "refined general law" it motivates immediately
> below, were falsified by a direct test. `docs/MECHANISM.md` interpolates
> smoothly between eigenstate QPE and Shor (K = 1 → 4 eigenstates in
> superposition, i.e. control–work entanglement 0 → log₂4 bits) and
> measures the ququint advantage at each step. If the hypothesis were
> right, the advantage should collapse to Shor's (negative) value by
> K = 4; instead it stays positive (+0.281) while actual Shor under
> identical noise and cost gives −0.248 — entanglement's measured effect
> is only ≈ −0.025 signal per bit, an order of magnitude too small to
> explain the Shor/QPE gap. The real cause, found by chasing that failed
> experiment, is the same N = 15 grid-alignment confound flagged at the
> top of this section: it structurally favored base 2 in the Shor
> comparison, and once removed (`docs/GRID_ALIGNMENT.md`), Shor obeys the
> same rule as QPE — qudits win with a native two-qudit gate, on both
> ladder and per-particle noise, with no work-register caveat needed. The
> "law" below is kept only as the record of the (wrong) hypothesis that
> the interpolation test was built to check.

The refined general law, replacing the simple noise-structure dichotomy:

> Prime-d encodings win whenever noise is paid per particle, and they
> win under ladder noise too *unless* the algorithm entangles the
> phase-carrying register with a work register whose computational basis
> states occupy high, fast-decaying levels — which Shor's modular
> arithmetic does maximally, and eigenstate phase estimation (the
> quantum-chemistry workhorse) does not at all.

Caveats: one noise strength per model; the d = 2 noiseless baseline is
lower (0.82 vs 0.95–1.0) because D = 64 happens to place its nearest grid
point 0.007 from the target phase — the floor-corrected normalization
absorbs this, and the orderings sit far outside the error bars.

### The exposure law, quantified — and where it ends

The "fewer particles × fewer layers" argument above can be pushed to a
quantitative law, with one unit conversion and one boundary
(`exposure_collapse.py`, full narrative in `docs/GROVER.md` §5):

1. **Exposure must be counted in damage, not events.** One noise layer
   does d-dependent harm: the per-carrier-layer entanglement infidelity
   1 − F_e = 1 − tr(S)/d² of the calibrated ladder channel is
   0.75s / 1.46s / 2.82s for d = 2/3/5 — a ququint takes ~4× a qubit's
   damage per event. With the abscissa exposure × (1 − F_e), Grover's
   three bases collapse onto a single exponential (decay rates
   0.44/0.49/0.43, each family log-linear with R² ≥ 0.996), where event
   units scatter them by 3.6×. This is the quantitative content of the
   "per-event-damage penalty ~log₂ d" hand-wave above.
2. **The law describes state decay, not measured signal.** Pooling Shor
   and Grover, one shared amplitude with a per-*algorithm* decay rate
   reaches R² = 0.93–0.94; the split that remains is the
   decoder, not the noise. Grover's signal *is* state survival, and
   behaves as a pure exponential in damage. Shor's signal passes through
   continued-fraction order recovery, whose error tolerance grows with
   register size — its d = 3 family holds ~0.72 signal while exposure
   triples. That tolerance is now derived exactly rather than only
   inferred from the flat signal: the acceptance set obeys
   |A|/D → 2 ln 2 · Σ_{k=1}^{⌊N/r⌋} φ(kr)/(kr)² (φ Euler's totient),
   with an exact finite-D Stern–Brocot form that reproduces the
   enumerated |A| outcome-for-outcome on every instance and size tested
   (`decoder_formula.py`, superseding the correlation account of
   `decoder_scaling.py`; full account in `docs/GROVER.md` §5). The direct check (`fidelity_collapse.py`) measures end-state
   fidelity instead of decoded signal, and *fidelity* obeys the one-curve
   law that signal does not: one shared exponential in damage units fits
   both algorithms, all bases and sizes, at R² = 0.97 (ladder) / 0.99
   (per-particle) with amplitude ≈ 1. Grover's fidelity equals its
   signal to a few parts in a thousand, while Shor decodes the right
   order from states nearly orthogonal to the ideal one (at d = 2,
   m = 12, depolarizing: fidelity 0.0003, signal 0.09).

So the exposure argument is a genuine law at the level of physics
(accumulated channel damage), and the algorithm enters only through how
much decoding redundancy stands between the state and the score.

---

## 5. Pointers

- M. Ringbauer et al., "A universal qudit quantum processor with trapped
  ions", Nat. Phys. 18, 1053 (2022).
- Y. Wang, Z. Hu, B. C. Sanders, S. Kais, "Qudits and high-dimensional
  quantum computing", Front. Phys. 8, 589504 (2020) — broad review.
- D. Gottesman, "Fault-tolerant quantum computation with higher-dimensional
  systems", (1999) — qudit stabilizer codes.
- D. Gross, "Hudson's theorem for finite-dimensional quantum systems",
  J. Math. Phys. 47, 122107 (2006) — odd-prime discrete Wigner functions.
- E. T. Campbell, H. Anwar, D. E. Browne, "Magic-state distillation in all
  prime dimensions using quantum Reed-Muller codes", PRX 2, 041021 (2012).
- M. S. Blok et al., "Quantum information scrambling on a superconducting
  qutrit processor", PRX 11, 021010 (2021).
