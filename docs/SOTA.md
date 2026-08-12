# State of the art: prime-d qudits, decoherence, and quantum algorithms

Synthesis of a deep read of the 21 papers in `papers/` (see `papers/INDEX.md`),
organized around the question this project answers: *does a prime-base
encoding buy decoherence resilience in phase-critical quantum algorithms,
and on which hardware?* Sections marked (pending) will be filled as the
remaining reader reports arrive.

---

## 1. Theory & fault tolerance

**Structure: odd prime d is cleaner than d = 2, not merely tolerable.**
Gottesman (1998) proves universal fault-tolerant computation for any
prime-d stabilizer code — primality makes n−k stabilizer generators encode
exactly k qudits, and the whole Clifford construction close. Gross (2006)
adds the phase-space side: in odd dimension, pure states have non-negative
Wigner functions iff they are stabilizer states, and Cliffords are exactly
the positivity-preserving unitaries. The qubit case is the structural
anomaly (extra factors of i, order-8 non-Cliffords).

**Magic-state distillation is where qudits demonstrably win — on paper.**
Campbell–Anwar–Browne (PRX 2012): the 4-ququint QRM₅(1) code has
depolarizing distillation threshold **0.363 vs 0.141** for the 15-qubit
Bravyi–Kitaev protocol (2.6×), with yield exponent γ* = 2 vs 2.32 (best
qubit) — the mechanism being that for prime d ≥ 5, diagonal non-Clifford
gates of period d exist, which simply do not exist for qubits. Campbell
(PRL 2014) removes the decline past d = 5 with higher-degree QRM codes
(distance ⌊(d+1)/3⌋ grows linearly in d): thresholds *increase*
monotonically with d, exceeding 0.5 by d = 11, and γ → 1. Headline quote:
"performance is always enhanced by increasing d."

**Topological memory thresholds rise with d — under abstract noise.**
Marks et al. (2017): qudit surface-code thresholds 0.093 (d=2) → 0.155
(plateau, large d); color codes 0.056 → 0.119 (+112%), under code-capacity
bit-flip noise.

**But the one circuit-level comparison mildly favors qubits.** Keppens et
al. (arXiv:2502.05992, 2025) — the closest prior work to this project —
simulate the 5-qudit perfect code for q = 2, 3, 5 under circuit-level
depolarizing noise: thresholds with flag qudits 4.95×10⁻⁴ (qubit) /
3.24×10⁻⁴ (qutrit) / 2.32×10⁻⁴ (ququint). Critically, their noise
convention lets the total error probability grow with dimension as
(q²−1)/q² at fixed parameter p — a *combinatorial* d-dependence (more
Pauli error types), not a *physical* one (higher levels individually
worse). Any comparison of our results to theirs must reconcile this
normalization difference explicitly.

**The recognized open question — exactly ours.** Campbell 2014: "in
physical systems one may also see noise rise with d. Such features depend
subtly on the details of the underlying physics" — flagged, never
quantified. Marks 2017 closes by noting qudit experiments will be
"hampered by the increased dimensionality... increased degrees of freedom
that can be coupled to the environment," and leaves it "an interesting
question for experimental implementations." **Nobody in this literature
(a) simulates algorithms (rather than codes) across d, or (b) uses a
hardware-derived level-dependent noise model.** The control–work
entanglement mechanism we found (which flips the qudit advantage between
Shor and eigenstate QPE) is invisible to code-level metrics by
construction — codes have no control register.

## 2. Hardware platforms: trapped ions & superconducting

**Demonstrated state of the art.**

| | best d | best single-qudit | best two-qudit | coherence |
|---|---|---|---|---|
| Trapped ions | 13 (SPAM, Ba⁺); 7 (universal, Ca⁺) | 2×10⁻³ err/Clifford (d=3); 1×10⁻² (d=5) | Cex 97.5%, Cinc 93.8% (Ringbauer) | T1 1.1–35 s; T2 ~100 ms shielded |
| Superconducting | 3 (gates); 8–20 (bosonic) | 98.89%/Clifford (qutrit RB) | CZ† 97.3% (Goss) | T1⁰¹ 45–125 µs, T1¹² 28–63 µs |

Nobody has run Shor or QPE on qudit hardware. Largest executed qudit
algorithm: Blok's 5-qutrit teleportation/scrambling (F = 0.568 vs 0.5
classical). A d=32 photonic time-bin experiment factored 15 (Weng & Chuu
2024, via Kiktenko review).

**Measured noise structure vs our models — the key calibration data:**

- **T1 ladder: confirmed, exponent < 1.** Across 9 transmons (Goss,
  Blok): Γ¹²/Γ⁰¹ mean ≈ 1.7 (spread 1.1–2.1), vs 2.0 in our ∝k model.
  Tripathi's d=4 data (T1 = 53/34/24 µs) fits Γ_k ∝ k^0.68.
- **Dephasing (Δlevel)²: half wrong.** Extracted pure-dephasing ratios:
  Γφ⁰²/Γφ⁰¹ ≈ 2.3 measured (model predicts 4); Γφ¹²/Γφ⁰¹ ≈ 2.0 measured
  (model predicts 1). Cause: the charge dispersion of |2⟩ is ≥10× that of
  |1⟩ — reality is closer to "any coherence involving level ≥2 dephases
  ~2× faster" (a max(i,j) law) than to (Δlevel)². **Our model
  over-penalizes qudits on the (Δlevel)² axis and under-penalizes the
  |2⟩-specific channel; the transmon conclusions need a calibrated
  re-run.**
- **Ions ≈ per-particle uniform: confirmed.** Ringbauer: all 8 levels
  metastable, all transitions ~100 ms coherence, sensitivities within 5×;
  d=3→5 physical pulse error grows only 1.6× (Clifford error 5× — a
  compilation-depth effect, not level degradation). Low (d=13): per-level
  SPAM errors span 3–34% but track magnetic sensitivity κ²τ², *not* level
  index; with optimal level choice, fidelity is flat with d up to 13 —
  the strongest experimental support for large-d scaling.
- **Real per-gate noise strengths (rate × gate time):** transmon
  single-qutrit ~5×10⁻⁴; transmon two-qutrit 7×10⁻³–3×10⁻² (dephasing-
  dominated); ion two-qudit ~10⁻³ (T2-limited). The platforms are within
  one order of magnitude per gate: the ions' 10³× coherence advantage is
  mostly eaten by 10³× slower gates. Our sweeps (0.002–0.05 demo,
  0.003–0.005 scaling) bracket the realistic operating points.
- **What we don't model:** coherent errors (cross-Kerr α ≈ 0.1–0.7 MHz —
  kills an unprotected qutrit Bell state in ~1 µs; drive-induced level
  shifts ∝ Ω²), d-dependent readout error (|2⟩ reads out 3–7% worse than
  |0⟩), d-dependent entangling cost (ion Cinc = 2(d−1) MS gates).

## 3. Spin platforms & noise suppression

- **NV centers (Gardill 2020):** the spin-1 rate matrix at field
  B_z > 60 G is per-particle-like (all pairwise rates within ~5×, no
  level-index ordering). At low field a Δm=2 "skip" channel driven by
  1/f² electric-field noise dominates (γ up to 240 kHz vs Ω ≈ 1 kHz) and
  scales as 1/Δ² — a d-dependent penalty *invisible to both our models*,
  since packing more levels shrinks splittings.
- **Molecular qudits (Chiesa 2024):** Lindblad Eq. (38) *microscopically
  derives* our (Δm)² dephasing for single giant spins — and shows
  competing-antiferromagnetic-exchange clusters flatten it to nearly
  level-independent. **The noise model is a chemically tunable axis, not
  a fixed hardware property.**
- **Executed QFT on a molecular qutrit (Rubín-Osanz, Dec 2025):**
  173Yb(trensal), d=3 of 12 available levels, T2 > 0.1 ms, F = 0.98 with
  refocusing embedded in the algorithm vs 0.85 without — the unrefocused
  run selectively lost the two-quanta coherence, the cleanest
  experimental signature of a Δlevel-type penalty, *and refocusing
  removed it*.
- **Qudit dynamical decoupling (Tripathi 2024):** Heisenberg–Weyl DD
  works on transmon qutrits/ququarts and helps *more* at higher d
  (because free evolution is worse); rescues a qutrit Bell state from
  ~1 µs death to >50% at 10 µs. But pulse cost grows as 2(d−1) per cycle
  and DD cannot touch amplitude damping — the residual is the k^0.68 T1
  ladder. Suppression is preferential for exactly the noise component
  that our ladder model says kills qudits.

## 4. Qudit algorithms

**No one has simulated a qudit algorithm under noise.** The field treats
"qudits and noise" in exactly three ways, none a simulation: count
entangling gates and assume fewer means better (Nikolaeva 2021, Kiktenko
2023 — gate count as an explicit noise *proxy*); bound coherent
gate-approximation error analytically (Bocharov 2016, Props. 16–18 —
worst-case unitary distance, no channel); or import the qualitative
"fewer carriers under local noise" argument from quantum communication
(Wang 2020 §6.1).

**Bocharov–Roetteler–Svore 2016** (Microsoft QuArC) is the closest Shor
work: exhaustive resource counts for ternary Shor on generic and
metaplectic architectures (headline: factoring with n+7 logical qutrits;
low-width modular exponentiation 48n³ non-Clifford depth for
emulated-binary encoding vs ~76n³ for native ternary). Notable
counter-intuitive finding: *emulated binary encoding beats native ternary
arithmetic* for ripple-carry adders (12n vs 19n P9 gates) — so a qutrit
advantage cannot be attributed to encoding density alone. d = 3 only, no
d = 5, no decoherence of any kind.

**Pavlidis & Floratos 2017**: d-parametric cost formulas for QFT-domain
arithmetic — QFT depth 8d²q, MAC depth 4d²q, MMAC depth 21d³q². These
d²/d³ factors are the honest price of higher-d gates that layer-based
cost models (including ours) do not charge; the paper explicitly states
qudit noise robustness is "expected" but requires "further
investigation."

**Nikolaeva/Kiktenko/Fedorov line** (2021 transpiler; 2023 RMP
colloquium): qudit hardware running qubit circuits — N-qubit Toffoli in
2N−3 entangling gates with one ancilla level vs 6N+const for qubits;
claimed thousandfold entangling-gate reduction for Grover ≥ 8 qubits
using ququints. Collected experimental fidelities (calibration data for
us): single-qudit 99.936% (d=2) / 99.909% (d=3) / 99.78% (d=4); qutrit
CZ 97.3%; trapped-ion two-qutrit 97.5%; d=32 photonic time-bin factored
15. Their open problem #2 verbatim: "the investigation of the impact of
noise within the discussed schemes."

**Wang et al. 2020 review**: states both halves of our per-particle
result *qualitatively* — "noise sources act locally on every system,
increasing the dimension d will reduce the number of systems and thus
reduce the effect of noise" (§6.1, for entangled states/QKD), and quotes
Parasa & Perkowski (ISMVL 2011) that qudit-PEA "error rate decreases
exponentially as the qudit dimension increases" — a one-line secondhand
claim with no model, no simulation, no d-sweep. Both must be cited and
engaged.

## 5. Gap analysis & positioning

**The open gap, cross-confirmed by all four reading groups:** no
published work simulates any quantum *algorithm* across qudit dimensions
under a physically motivated noise model. The fault-tolerance literature
evaluates codes (which have no control register, so our entanglement-flip
mechanism is invisible to their metrics); the algorithms literature
counts noiseless resources and defers noise explicitly (Pavlidis:
"further investigation to be carried"; Kiktenko open problem #2: "the
investigation of the impact of noise within the discussed schemes";
Campbell 2014: noise rising with d "depend[s] subtly on the details of
the underlying physics"; Marks 2017: "an interesting question for
experimental implementations"). The hardware literature characterizes
gates, never algorithms.

**Prior fragments to engage honestly:**
1. *Wang 2020 §6.1* states the per-particle argument qualitatively;
   *Parasa & Perkowski 2011* (secondhand via Wang) claim qudit-PEA error
   "decreases exponentially" with d. Neither has a model or simulation.
   We quantify, name the channels, and find the claim is
   noise-structure-dependent.
2. *Keppens 2025* (5-qudit code, q = 2/3/5, circuit-level depolarizing,
   qudits slightly worse): **same channel convention as ours** (fixed p,
   error probability grows as (q²−1)/q²) — the opposite conclusion is
   structural, not a normalization artifact. Their circuit is fixed-width
   in physical qudits for all q (a code has no problem to compress);
   ours shrinks with d (the entire source of the qudit win). This is the
   cleanest possible illustration that code-level and algorithm-level
   comparisons answer different questions.
3. *Bocharov 2016*: ternary Shor resource counts, analytic coherent
   error bounds only; also shows emulated-binary encoding can beat
   native ternary arithmetic — so qudit advantage claims must not rest
   on encoding density alone.
4. *Pavlidis 2017*: QFT-arithmetic depth carries explicit d²/d³ factors.
   Our layer-based cost model does not charge these — a sensitivity
   analysis with d-dependent gate costs is required pre-publication.

**Scoop check (second-pass targeted search, ~46 queries / ~250
abstracts, Aug 2026): LOW RISK, no direct overlap.** Nothing published
combines Shor + eigenstate QPE, success probability across d = 2/3/5,
two contrasting physical noise models, and register-size scaling; the
sign-flip mechanism has no precedent. Three PARTIAL competitors own one
axis each and must be explicitly differentiated in related work:

1. *Janković et al. 2023* (arXiv:2302.04543) — one qudit vs n qubits
   under Lindblad noise, analytic average-gate-infidelity criterion with
   a critical curve O(d²/log₂ d) in gate-time ratios. Gate-level, no
   algorithms, no scaling. **Doubles as our best cross-validation
   target**: our numerics should reproduce their critical curve in the
   appropriate limit.
2. *Gokhale et al. 2019* (arXiv:1905.10481) — qutrit circuit simulator
   with realistic noise charging for qutrit operation, fidelity vs qubit
   baseline for Generalized Toffoli. d = 3 only, gate decomposition
   target, one noise model.
3. *Gustafson 2022* (arXiv:2201.04546) — qutrit vs qubit encodings of
   scalar-QED simulation under amplitude damping + generalized Pauli
   noise; source of the "10–100× higher tolerable gate error" claim.
   Field-theory observable, d = 3 only, no size scaling.

Also new to the library: Peterer 2015 (arXiv:1409.6031 — sequential
|k⟩→|k−1⟩ decay measured up to the 4th transmon level: the primary
citation for the ladder *structure*), Wang/Blok 2024 (d = 12 transmon,
T2E at the T1 limit — the dephasing penalty is a design parameter),
Shi/Chuang 2025 (Grover on d = 5/8 ion qudits), Lu 2019 (first qudit QPE
experiment, single ternary digit), and the Parasa & Perkowski ISMVL 2011
slides (paper is IEEE-only — obtain before quoting specific numbers).
Four independent superconducting per-level coherence datasets now span
d = 3 to d = 12 (Peterer, Yurtalan, Blok, Wang).

**Model-calibration issues surfaced by the experimental data (must fix
before submitting):**
- Ladder T1 exponent: measured ≈ k^0.7, we use k¹ (over-severe).
- Ladder dephasing: measured ≈ 2× penalty for any |2⟩-involving
  coherence (max-level law), we use (Δlevel)² (wrong shape; over-severe
  at Δ=2, under-severe at 1↔2).
- Net direction of both errors: our model overstates the qudit penalty on
  transmons — the "qubits win Shor under ladder noise" headline might
  soften or flip under calibrated noise. Re-run required.
- Missing channels with d-dependence: cross-Kerr coherent errors,
  d-dependent readout error, 2(d−1) entangling-gate cost on ions, NV
  1/Δ² skip channel.

---

## 6. Reconciliations, written for the related-work section

Task #8. Draft prose for the two prior results that appear to contradict
us, plus a status note on the calibration issues listed above.

### 6.1 Keppens et al. 2025 — why a code-level study orders the dimensions
the other way

> Keppens et al. compare the five-qudit code across q = 2, 3, 5 under
> circuit-level depolarizing noise and report that qudits perform slightly
> *worse* as q grows, which appears to contradict the ordering we find.
> The two results are compatible, and the difference is instructive. We
> adopt the same noise convention they do — a fixed per-gate parameter p
> whose realized error probability grows as (q²−1)/q², so a qudit gate is
> already charged more than a qubit gate — hence the disagreement is not a
> normalization artifact. It is structural. A quantum code has no problem
> instance to compress: the five-qudit code is five physical carriers and
> a fixed gate list at every q, so raising q buys no reduction in width or
> depth while strictly increasing each carrier's exposure. An algorithm
> does compress: at matched precision, order finding on base-d qudits
> needs m = ⌈log_d D⌉ control carriers and a proportionally shorter serial
> schedule, and that compression is the entire source of the advantage we
> measure. Code-level and algorithm-level comparisons therefore answer
> different questions, and both answers are correct. The practical reading
> is that a qudit advantage must be argued at the level of a *compressible
> workload*; it does not transfer automatically to the error-correction
> layer that would protect that workload.

### 6.2 Bocharov et al. 2016 — the encoding caveat

> Bocharov et al. give ternary resource counts for Shor's algorithm and
> show that binary arithmetic *emulated* on ternary carriers can beat
> native ternary arithmetic. We take this as a constraint on how a qudit
> advantage may be claimed rather than as a counter-result: it shows that
> encoding density alone — more Hilbert space per carrier — is not a
> mechanism. Our registers use native base-d arithmetic throughout, and we
> attribute the advantage specifically to width-and-depth compression at
> matched problem size under a per-carrier noise budget, not to the
> dimension of the carrier as such. Where the entangling gate is not
> native, that compression is bought back by the compiler and the
> advantage disappears — which is precisely the condition our cost
> sensitivity analysis isolates, and it is consistent with their finding.

### 6.3 Status of the calibration issues listed in §5

| issue | status |
|---|---|
| ladder T1 exponent (k¹ → k^0.7) | **fixed** — `docs/CALIBRATION.md` |
| ladder dephasing shape ((Δlevel)² → max-level) | **fixed** — realized exactly via MDS embedding |
| "qubits win Shor under ladder noise" | **retracted** — it was an N = 15 grid-alignment artifact, not a calibration artifact (`docs/GRID_ALIGNMENT.md`) |
| d-dependent gate cost (Pavlidis d², ion 2(d−1)) | **charged** — `docs/COST_SENSITIVITY.md`; it is now the paper's central condition |
| d-dependent readout error | **charged** — `spam_study.py` |
| dynamical decoupling / refocused operation | **swept** — `dd_study.py` |
| cross-Kerr coherent errors | **open** — stated as a limitation |
| NV 1/Δ² skip channel | **open** — proposed as follow-up work (direction E) |
