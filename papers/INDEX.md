# Reference library — prime-base qudits, decoherence, and Shor/QPE

**51 papers**, all downloaded successfully from arXiv. Every arXiv ID below was
verified against the arXiv API before download; titles and author lists are as
returned by the API.

The library grew in passes as the paper was written: the first 21 answered the
core question, then a second pass added the closest prior work to cite and
differentiate (§2A–2C), and a third referee pass added the exact
success-probability analyses of order finding (§ "Referee pass"). Section 1–5
below are the original organisation; everything after "Download status" is a
later pass. `docs/SOTA.md` synthesises the first 21; the later additions are
annotated in place.

Organised by the question each group answers for this repo: *does a prime-base
(d = 3, 5) encoding buy resilience against decoherence in the phase-critical
core of Shor's algorithm?*

---

## 1. Why prime dimensions are mathematically special

These underpin the repo's claim that *prime* d is not an arbitrary choice.

| # | Paper | Authors | Year | arXiv | File |
|---|---|---|---|---|---|
| 1 | Fault-Tolerant Quantum Computation with Higher-Dimensional Systems | Daniel Gottesman | 1998 | [quant-ph/9802007](https://arxiv.org/abs/quant-ph/9802007) | `gottesman-1998-ft-higher-dimensional-systems.pdf` |

The foundational result: the stabilizer formalism, Clifford group and
fault-tolerant gate constructions generalise cleanly to d-level systems when d
is prime (Z_d is then a field). This is the origin of "prime d is special".

| # | Paper | Authors | Year | arXiv | File |
|---|---|---|---|---|---|
| 2 | Hudson's Theorem for finite-dimensional quantum systems | D. Gross | 2006 | [quant-ph/0602001](https://arxiv.org/abs/quant-ph/0602001) | `gross-2006-hudson-theorem-wigner-functions.pdf` |

Discrete Wigner functions for odd prime d, and the theorem that non-negative
Wigner functions are exactly the stabilizer states. The standard tool for
separating classically simulable from magic resources in odd prime dimensions —
relevant if this project ever asks *which* qudit states carry the interference
that decoherence destroys. (Task brief cited this as "…and non-negative Wigner
functions"; the arXiv title is the shorter form above.)

| # | Paper | Authors | Year | arXiv | File |
|---|---|---|---|---|---|
| 3 | Magic state distillation in all prime dimensions using quantum Reed-Muller codes | Earl T. Campbell, Hussain Anwar, Dan E. Browne | 2012 | [1205.3104](https://arxiv.org/abs/1205.3104) | `campbell-2012-magic-state-distillation-prime-dims.pdf` |

Distillation protocols that exist for *every* prime d, with distillation
thresholds that improve with d. Direct evidence for a prime-d advantage on the
resource-overhead axis, complementary to this repo's decoherence axis.

| # | Paper | Authors | Year | arXiv | File |
|---|---|---|---|---|---|
| 4 | Enhanced fault-tolerant quantum computing in d-level systems | Earl T. Campbell | 2014 | [1406.3055](https://arxiv.org/abs/1406.3055) | `campbell-2014-enhanced-ft-d-level-systems.pdf` |

Shows magic-state distillation overhead falling with increasing prime d,
approaching the theoretical minimum. The strongest "higher prime d is better"
argument in the literature — a useful counterweight to this repo's finding that
ladder-noise hardware reverses the ordering.

---

## 2. Shor's algorithm, QFT and arithmetic on qudit registers

The algorithmic layer this repo actually simulates.

| # | Paper | Authors | Year | arXiv | File |
|---|---|---|---|---|---|
| 5 | Factoring with Qutrits: Shor's Algorithm on Ternary and Metaplectic Quantum Architectures | Alex Bocharov, Martin Roetteler, Krysta M. Svore | 2016 | [1605.02756](https://arxiv.org/abs/1605.02756) | `bocharov-2016-factoring-with-qutrits-shor.pdf` |

The closest prior work to this repo's benchmark: a full ternary implementation
of Shor, with qutrit modular-arithmetic circuits and depth/width counts. The
reference point for the resource-scaling claims (particle count and time-layer
depth for d = 3 vs d = 2).

| # | Paper | Authors | Year | arXiv | File |
|---|---|---|---|---|---|
| 6 | Arithmetic Circuits for Multilevel Qudits Based on Quantum Fourier Transform | Archimedes Pavlidis, Emmanuel Floratos | 2017 | [1707.08834](https://arxiv.org/abs/1707.08834) | `pavlidis-2017-qudit-arithmetic-circuits-qft.pdf` |

QFT-based adders and controlled modular multipliers over Z_{d^m} — exactly the
primitives behind `qudit_shor.py`'s controlled |x⟩ → |a^c x mod 15⟩ and the
no-swap inverse QFT. Use for gate-count and depth cross-checks. **Source of the
`pavlidis` cost model**: the controlled rotations decompose into 4(d−1)²
elementary two-level gates, i.e. (d−1)² per gate after d = 2 normalization —
which our d²/4 charge rounds *down*, making the decomposition verdicts
conservative. Also the source of the truncation-robustness conjecture for
qudits that the paper's AQFT hardware run touches on.

| # | Paper | Authors | Year | arXiv | File |
|---|---|---|---|---|---|
| 6b | Finite Fractional Fourier Transform on Qudits | Emmanuel Floratos, Archimedes Pavlidis | 2024 | [2409.05759](https://arxiv.org/abs/2409.05759) | `floratos-pavlidis-2024-fractional-qft-qudits.pdf` |

Follow-up by the same authors, and the reason `pavlidis` is charged as a
**uniform layer multiplier** rather than a gate-count multiplier: it reports the
same d² scaling in **depth**, not merely in gate count, for a full QFT-based
in-place modular multiplier under a 1D-local-neighbour architecture. Cited in
the paper's gate-cost subsection as `floratos2024`. (Its `refs.bib` entry needs
a `journal` field or the LaTeX build fails.)

| # | Paper | Authors | Year | arXiv | File |
|---|---|---|---|---|---|
| 7 | Efficient realization of quantum algorithms with qudits | Anastasiia S. Nikolaeva, Evgeniy O. Kiktenko, Aleksey K. Fedorov | 2021 | [2111.04384](https://arxiv.org/abs/2111.04384) | `nikolaeva-2021-efficient-algorithms-with-qudits.pdf` |

Embedding qubit algorithms into qudit registers to trade particle count against
per-particle error rate. The formal version of the tradeoff this repo measures
empirically: fewer, noisier carriers vs more, cleaner ones.

| # | Paper | Authors | Year | arXiv | File |
|---|---|---|---|---|---|
| 8 | Qudits for decomposing multiqubit gates and realizing quantum algorithms | Evgeniy O. Kiktenko, Anastasiia S. Nikolaeva, Aleksey K. Fedorov | 2023 | [2311.12003](https://arxiv.org/abs/2311.12003) | `kiktenko-2023-qudits-decomposing-gates-algorithms.pdf` |

Review-style follow-up covering qudit-assisted decomposition of multi-controlled
gates without ancillas — the mechanism behind the shorter serial schedules
(15 vs 51 time-layers) this repo reports for d = 5.

---

## 3. Decoherence in real qutrits — the noise models under test

Empirical grounding for the repo's two competing noise models.

| # | Paper | Authors | Year | arXiv | File |
|---|---|---|---|---|---|
| 9 | A universal qudit quantum processor with trapped ions | Martin Ringbauer, Michael Meth, Lukas Postler, Roman Stricker, Rainer Blatt, Philipp Schindler, Thomas Monz | 2021 | [2109.06903](https://arxiv.org/abs/2109.06903) | `ringbauer-2021-universal-qudit-ion-processor.pdf` |

The canonical trapped-ion qudit processor. Its error behaviour — roughly
per-particle, per-unit-time, largely dimension-independent — is the physical
justification for the repo's uniform depolarizing model, the regime where
d = 5 breaks even and then wins.

| # | Paper | Authors | Year | arXiv | File |
|---|---|---|---|---|---|
| 10 | Quantum Information Scrambling in a Superconducting Qutrit Processor | M. S. Blok, V. V. Ramasesh, T. Schuster, K. O'Brien, J. M. Kreikebaum, D. Dahlen, A. Morvan, B. Yoshida, N. Y. Yao, I. Siddiqi | 2020 | [2003.03307](https://arxiv.org/abs/2003.03307) | `blok-2020-scrambling-superconducting-qutrit.pdf` |

Full qutrit control on transmons with characterisation of the |2⟩ level:
shorter T1 and faster dephasing than |1⟩. The measured asymmetry the repo
encodes as amplitude damping with level-k rate ∝ k plus (Δlevel)² dephasing.

| # | Paper | Authors | Year | arXiv | File |
|---|---|---|---|---|---|
| 11 | Characterization of Control in a Superconducting Qutrit Using Randomized Benchmarking | M. Kononenko, M. A. Yurtalan, S. Ren, J. Shi, et al. | 2020 | [2009.00599](https://arxiv.org/abs/2009.00599) | `kononenko-2020-superconducting-qutrit-rb.pdf` |

Qutrit randomized benchmarking: per-gate error rates for the full SU(3) gate
set. Gives concrete numbers for calibrating the transmon-model γ and γ_φ
instead of using arbitrary units.

| # | Paper | Authors | Year | arXiv | File |
|---|---|---|---|---|---|
| 12 | High-Fidelity Qutrit Entangling Gates for Superconducting Circuits | Noah Goss, Alexis Morvan, Brian Marinelli, Bradley K. Mitchell, et al. | 2022 | [2206.07216](https://arxiv.org/abs/2206.07216) | `goss-2022-high-fidelity-qutrit-entangling-gates.pdf` |

Two-qutrit entangling gates on transmons with measured fidelities and durations.
Supplies realistic two-qudit gate times, which set the number of idling
time-layers each qudit accumulates in this repo's noise accounting.

| # | Paper | Authors | Year | arXiv | File |
|---|---|---|---|---|---|
| 13 | Fast relaxation on qutrit transitions of nitrogen-vacancy centers in nanodiamonds | Aedan Gardill, Matthew C. Cambria, Shimon Kolkowitz | 2019 | [1910.10813](https://arxiv.org/abs/1910.10813) | `gardill-2019-nv-qutrit-fast-relaxation.pdf` |

NV spin-1 relaxation measured on the individual qutrit transitions. The repo
lists NV spin-1 as a per-particle-noise platform; this paper is the check on
whether that assumption holds or whether NV centers are closer to ladder-like.

| # | Paper | Authors | Year | arXiv | File |
|---|---|---|---|---|---|
| 14 | Control and Readout of a 13-level Trapped Ion Qudit | Pei Jiang Low, Brendan White, Crystal Senko | 2023 | [2306.03340](https://arxiv.org/abs/2306.03340) | `low-2023-13-level-trapped-ion-qudit.pdf` |

How coherence and readout fidelity actually scale as d grows to 13 in a single
ion. The empirical test of whether "noise per particle, independent of d" stays
true well beyond d = 5, which is what the repo's scaling extrapolation assumes.

| # | Paper | Authors | Year | arXiv | File |
|---|---|---|---|---|---|
| 15 | Qudit Dynamical Decoupling on a Superconducting Quantum Processor | Vinay Tripathi, Noah Goss, Arian Vezvaee, Long B. Nguyen, et al. | 2024 | [2407.04893](https://arxiv.org/abs/2407.04893) | `tripathi-2024-qudit-dynamical-decoupling.pdf` |

Dynamical decoupling sequences generalised to qudits, suppressing exactly the
idling dephasing this repo applies after every gate layer. The natural
mitigation to test against the ladder-noise result — it could soften the
qubit advantage the repo finds on transmons.

| # | Paper | Authors | Year | arXiv | File |
|---|---|---|---|---|---|
| 16 | Near-term Application Engineering Challenges in Emerging Superconducting Qudit Processors | Davide Venturelli, Erik Gustafson, Doga Kurkcuoglu, Silvia Zorzetti | 2025 | [2506.05608](https://arxiv.org/abs/2506.05608) | `venturelli-2025-superconducting-qudit-processors.pdf` |

Recent survey of where superconducting qudits actually pay off and where the
higher-level decoherence penalty dominates. Closest published statement of this
repo's central caveat; useful for positioning the ladder-vs-per-particle result.

---

## 4. Error correction and thresholds in higher dimensions

What happens once encoded qudits, not bare ones, carry the computation.

| # | Paper | Authors | Year | arXiv | File |
|---|---|---|---|---|---|
| 17 | Comparison of memory thresholds for planar qudit geometries | Jacob Marks, Tomas Jochym-O'Connor, Vlad Gheorghiu | 2017 | [1701.02335](https://arxiv.org/abs/1701.02335) | `marks-2017-memory-thresholds-planar-qudit.pdf` |

Surface-code memory thresholds as a function of d for planar layouts. Shows
thresholds rising with d under depolarizing noise — the encoded-level analogue
of this repo's per-particle-noise result.

| # | Paper | Authors | Year | arXiv | File |
|---|---|---|---|---|---|
| 18 | Qudit vs. Qubit: Simulated performance of error correction codes in higher dimensions | James Keppens, Quinten Eggerickx, Vukan Levajac, George Simion, et al. | 2025 | [2502.05992](https://arxiv.org/abs/2502.05992) | `keppens-2025-qudit-vs-qubit-error-correction.pdf` |

Recent head-to-head simulation study framed the same way as this repo, but at
the error-correction layer rather than the bare-algorithm layer. The most direct
methodological comparison available; worth checking whether its noise
parameterisation also decides the ordering.

---

## 5. Reviews and alternative platforms

| # | Paper | Authors | Year | arXiv | File |
|---|---|---|---|---|---|
| 19 | Qudits and high-dimensional quantum computing | Yuchen Wang, Zixuan Hu, Barry C. Sanders, Sabre Kais | 2020 | [2008.00959](https://arxiv.org/abs/2008.00959) | `wang-2020-qudits-high-dimensional-qc-review.pdf` |

The standard qudit review: platforms, gate sets, algorithms, error correction.
General orientation and a source of citations for `docs/THEORY.md`.

| # | Paper | Authors | Year | arXiv | File |
|---|---|---|---|---|---|
| 20 | Quantum Information Processing with Molecular Nanomagnets: an introduction | Alessandro Chiesa, Emilio Macaluso, Stefano Carretta | 2024 | [2405.21000](https://arxiv.org/abs/2405.21000) | `chiesa-2024-molecular-nanomagnets-intro.pdf` |

Molecular spin qudits, where large d comes free from a single nuclear/electronic
spin. A fourth candidate platform for the repo's physical-systems discussion,
with a noise structure that is neither purely ladder nor purely per-particle.

| # | Paper | Authors | Year | arXiv | File |
|---|---|---|---|---|---|
| 21 | Implementation of the Quantum Fourier Transform on a molecular qudit with full refocusing and state tomography | Marcos Rubín-Osanz, Laura Bersani, Simone Chicco, Giuseppe Allodi, et al. | 2025 | [2512.15611](https://arxiv.org/abs/2512.15611) | `rubinosanz-2025-qft-molecular-qudit.pdf` |

An experimental qudit QFT with refocusing and tomography — the single circuit
element this repo's success metric depends on most. Direct hardware evidence on
how much of the QFT's interference survives decoherence in practice.

---

## Download status

All 21 PDFs verified: each begins with `%PDF` and exceeds 130 KB. No failures,
no retries needed, no papers skipped.


---

# Second pass (targeted)

Added 2026-08-10 by a scoop-check + targeted-reference sweep against the arXiv
API (~46 distinct queries, ~250 unique abstracts triaged). This pass had two
jobs: (a) establish whether anyone has already published the paper's core
claim, and (b) retrieve the specific references the draft has to engage.

**Scoop verdict: LOW risk.** No paper found does a quantitative simulated
comparison of Shor order-finding *and* eigenstate phase-estimation success
probability across qudit dimensions d = 2, 3, 5 under two contrasting physically
motivated noise models, with register-size scaling. The five PARTIAL papers
below each own one axis of that claim and must be cited and differentiated;
everything else is ADJACENT.

---

## 2A. Closest prior work (PARTIAL overlap — cite and differentiate)

| # | Paper | Authors | Year | arXiv | File |
|---|---|---|---|---|---|
| 22 | Noisy Qudit vs Multiple Qubits: Conditions on Gate Efficiency for Enhancing Fidelity | Denis Janković, Jean-Gabriel Hartmann, Mario Ruben, Paul-Antoine Hervieux | 2023 | [2302.04543](https://arxiv.org/abs/2302.04543) | `jankovic-2023-noisy-qudit-vs-multiple-qubits.pdf` |

**The nearest theoretical competitor.** Asks the same question this repo asks —
does one qudit beat n qubits of equal Hilbert-space dimension under noise? —
and answers it analytically, via first-order Average Gate Infidelity in the
Lindblad formalism. Derives a critical curve `O(d²/log₂ d)` in the ratio of gate
times measured in decoherence-time units, separating the regime where the qudit
wins from where the qubit register wins. Differentiators for this repo: Janković
works at the *gate* level with a gate-independent AGI, not algorithm success
probability; there is no Shor, no QPE, no register-size scaling, and no
contrast between ladder-structured and per-particle noise. Their critical curve
is, however, a quantitative analytic prediction this repo's numerics can be
checked against — the single most useful cross-validation in the library.

| # | Paper | Authors | Year | arXiv | File |
|---|---|---|---|---|---|
| 23 | Asymptotic Improvements to Quantum Circuits via Qutrits | Pranav Gokhale, Jonathan M. Baker, Casey Duckering, Natalie C. Brown, Kenneth R. Brown, Frederic T. Chong | 2019 | [1905.10481](https://arxiv.org/abs/1905.10481) | `gokhale-2019-asymptotic-improvements-via-qutrits.pdf` |

**The nearest methodological competitor.** Builds an open-source qutrit circuit
simulator with realistic near-term noise models that charge for the cost of
operating qutrits, then reports simulated fidelity for a qutrit construction
against a qubit-only baseline (>90% vs <30% for the ancilla-free Generalized
Toffoli). That is structurally the experiment this repo runs. Differentiators:
d = 3 only with no scaling in d, the target is gate decomposition depth rather
than Shor/QPE success probability, and the noise model is single, not a
contrast between two physically distinct families.

| # | Paper | Authors | Year | arXiv | File |
|---|---|---|---|---|---|
| 24 | Noise Improvements in Quantum Simulations of sQED using Qutrits | Erik Gustafson | 2022 | [2201.04546](https://arxiv.org/abs/2201.04546) | `gustafson-2022-noise-improvements-sqed-qutrits.pdf` |

**The source of the "10–100× higher tolerable gate error" claim.** Measures the
mass gap of (1+1)d scalar QED via an out-of-time correlator as a function of
noise, for both qubit and qutrit encodings, under *two* channels — amplitude
damping and a generalized Pauli decoherence channel. For equal error in the
extracted mass, the qutrit simulation tolerates 10–100× larger gate noise.
Closest published match to this repo's two-noise-model design, and the strongest
existing "qudits win under decoherence" result. Differentiators: a
lattice-field-theory observable rather than an algorithmic success probability,
d = 3 only, and no register-size scaling.

| # | Paper | Authors | Year | arXiv | File |
|---|---|---|---|---|---|
| 25 | Tradeoff between noise and banding in a quantum adder with qudits | Gaurang Agrawal, Tanoy Kanti Konar, Leela Ganesh Chandra Lakkaraju, Aditi Sen De | 2023 | [2310.11514](https://arxiv.org/abs/2310.11514) | `agrawal-2023-noise-banding-qudit-adder.pdf` |

QFT-based addition in *arbitrary* dimension under local noise on individual
qudits, with an explicit link established between quantum coherence and output
fidelity, plus the result that under noise a banded (constant-depth,
approximate) circuit beats a fuller one. Overlaps this repo's QFT-under-noise
sub-question and its coherence-based mechanism story. Differentiators: an
arithmetic primitive rather than Shor or QPE end-to-end, no hardware-grounded
ladder noise, and no success-probability comparison across d.

Paper #18 in the first pass (Keppens et al. 2025, `2502.05992`) is the fifth
PARTIAL: same qudit-vs-qubit simulated-comparison framing, but at the
error-correction layer rather than the bare-algorithm layer.

---

## 2B. References the draft must engage

| # | Paper | Authors | Year | arXiv | File |
|---|---|---|---|---|---|
| 26 | Quantum Phase Estimation Using Multivalued Logic (ISMVL 2011 **talk slides**) | Vamsi Parasa, Marek Perkowski | 2011 | not on arXiv | `parasa-2011-qpe-multivalued-logic-SLIDES.pdf` |

**The source of the "QPE error decreases exponentially with d" claim the draft
must engage.** The published paper is IEEE-only (Proc. 41st IEEE Int. Symp. on
Multiple-Valued Logic, pp. 224–229, [DOI 10.1109/ISMVL.2011.47](https://doi.org/10.1109/ISMVL.2011.47));
it is *not* on arXiv, and the PDXScholar author's-version link
(`pdxscholar.library.pdx.edu/ece_fac/202/`) returns an empty body. What is
retrievable is the authors' own conference slide deck, hosted at Portland State
(`web.cecs.pdx.edu/~mperkows/CLASS_FUTURE/Good-2011/`), saved here — it carries
the claims but is not the peer-reviewed text. The paper's abstract states a QPE
circuit of `O(n log n)` single-qudit operations and asserts the multivalued
version is "more robust", needing fewer qudits with "drastic improvement in the
precision and success probability". **Action for the draft: obtain the IEEE PDF
before quoting any specific numerical claim from this work.** Note that
`0906.1033` (S. V. Parasa & K. Eswaran, quantum pseudo-fractional Fourier
transform applied to QPE) surfaced in the author search but is a *different*
Parasa and a different result — not a substitute.

| # | Paper | Authors | Year | arXiv | File |
|---|---|---|---|---|---|
| 27 | Noise Thresholds for Higher Dimensional Systems using the Discrete Wigner Function | Wim van Dam, Mark Howard | 2010 | [1011.2497](https://arxiv.org/abs/1011.2497) | `vandam-2010-noise-thresholds-discrete-wigner.pdf` |

Published as PRA 83, 032310 (2011). Finds the depolarizing rate at which
non-stabilizer states and non-Clifford gates become Gottesman-Knill simulable in
dimension d, using the discrete Wigner function and facets of the qudit Clifford
polytope. Critical noise rate for robust gates approaches the theoretical 100%
optimum as d grows — a clean "higher d is more noise-robust" result on the
resource axis, pairing with Gross (#2) and Campbell (#3, #4).

| # | Paper | Authors | Year | arXiv | File |
|---|---|---|---|---|---|
| 28 | Prospects for Simulating a Qudit Based Model of (1+1)d Scalar QED | Erik Gustafson | 2021 | [2104.10136](https://arxiv.org/abs/2104.10136) | `gustafson-2021-qudit-scalar-qed.pdf` |

The companion to #24: the gauge-invariant qudit digitization and Trotter
construction whose cost savings (qutrit spin-1 vs qubit encoding) the noise
paper then evaluates. Read alongside #24 for the full argument.

| # | Paper | Authors | Year | arXiv | File |
|---|---|---|---|---|---|
| 29 | Generalized Toffoli gate decomposition using ququints: Towards realizing Grover's algorithm with qudits | Anastasiia S. Nikolaeva, Evgeniy O. Kiktenko, Aleksey K. Fedorov | 2022 | [2212.12505](https://arxiv.org/abs/2212.12505) | `nikolaeva-2022-ququint-toffoli-grover.pdf` |

**The d = 5 Grover paper.** Uses a ququint's space as two qubits plus a joint
ancillary state, giving an `O(N)`-depth ancilla-free N-qubit Toffoli, then
claims sizable Grover advantage from it. The direct precedent for this repo's
choice of d = 5 as a distinguished dimension and for the entangling-gate-count
reduction mechanism.

| # | Paper | Authors | Year | arXiv | File |
|---|---|---|---|---|---|
| 30 | Scalable improvement of the generalized Toffoli gate realization using trapped-ion-based qutrits | Anastasiia S. Nikolaeva, Ilia V. Zalivako, Alexander S. Borisenko, Nikita V. Semenin, et al. | 2024 | [2407.07758](https://arxiv.org/abs/2407.07758) | `nikolaeva-2024-trapped-ion-qutrit-toffoli.pdf` |

The experimental follow-up to #29 on ¹⁷¹Yb⁺ optical-metastable-ground qutrits up
to N = 10, including a three-qubit Grover run with *leakage out of the qubit
subspace monitored* during the qutrit Toffoli. That leakage measurement is
directly relevant to this repo's ladder-noise accounting.

| # | Paper | Authors | Year | arXiv | File |
|---|---|---|---|---|---|
| 31 | Coherence and Decay of Higher Energy Levels of a Superconducting Transmon Qubit | Michael J. Peterer, Samuel J. Bader, Xiaoyue Jin, Fei Yan, Archana Kamal, Ted Gudmundsen, Peter J. Leek, Terry P. Orlando, William D. Oliver, Simon Gustavsson | 2014 | [1409.6031](https://arxiv.org/abs/1409.6031) | `peterer-2014-higher-levels-transmon-coherence.pdf` |

**The systematic higher-level transmon coherence measurement the repo needed.**
Drives a transmon up to its *fourth* excited level with consecutive π-pulses and
characterises decay and coherence of each state, finding decay proceeds mainly
*sequentially* — i.e. ladder-structured, |k⟩ → |k−1⟩ — with T1 > 20 µs for all
transitions, plus a direct charge-dispersion measurement per level. This is the
empirical foundation for the repo's transmon model (level-k damping rate ∝ k
with (Δlevel)² dephasing), and it predates and outranks Goss 2022 / Blok 2020 /
Tripathi 2024 for this specific purpose. Cite this for the ladder structure
itself, not just the level-2 asymmetry.

| # | Paper | Authors | Year | arXiv | File |
|---|---|---|---|---|---|
| 32 | Characterization of multi-level dynamics and decoherence in a high-anharmonicity capacitively shunted flux circuit | M. A. Yurtalan, J. Shi, G. J. K. Flatt, A. Lupascu | 2020 | [2008.00593](https://arxiv.org/abs/2008.00593) | `yurtalan-2020-multilevel-decoherence-flux-qutrit.pdf` |

Second independent multi-level relaxation and dephasing dataset, on a
high-anharmonicity capacitively shunted flux circuit used as a qutrit, with the
decoherence sources discussed. The cross-check on whether the ladder scaling in
#31 is transmon-specific or generic to superconducting qudits.

| # | Paper | Authors | Year | arXiv | File |
|---|---|---|---|---|---|
| 33 | Experimental high-dimensional Greenberger-Horne-Zeilinger entanglement with superconducting transmon qutrits | Alba Cervera-Lierta, Mario Krenn, Alán Aspuru-Guzik, Alexey Galda | 2021 | [2104.05627](https://arxiv.org/abs/2104.05627) | `cerveralierta-2021-high-dimensional-ghz-transmon-qutrits.pdf` |

The three-qutrit GHZ state on a cloud-accessed superconducting processor, 76±1%
fidelity, certified genuinely three-partite *and* three-dimensional. The paper
referenced in Kiktenko's review, and the hardware datapoint for how much
high-dimensional entanglement survives on transmons — the resource at the centre
of this repo's control-work-entanglement mechanism.

| # | Paper | Authors | Year | arXiv | File |
|---|---|---|---|---|---|
| 34 | Implementation of Shor's Algorithm with a Single Photon in 32 Dimensions | Hao-Cheng Weng, Chih-Sung Chuu | 2024 | [2408.08138](https://arxiv.org/abs/2408.08138) | `weng-2024-shor-single-photon-32-dimensions.pdf` |

Published as Phys. Rev. Applied (2024). Encodes 32 time bins in a single
temporally long photon — the largest reported time-bin dimension — and runs a
compiled Shor factoring 15 on it. The high-water mark for experimental
qudit-based Shor, and the natural "how far has hardware actually got" anchor for
the repo's introduction. It reports a single dimension with no comparison across
d and no decoherence study, so it does not compete with the repo's claim.

| # | Paper | Authors | Year | arXiv | File |
|---|---|---|---|---|---|
| 42 | Systematic study of High $E_J/E_C$ transmon qudits up to $d = 12$ | Z. Wang, R. W. Parker, E. Champion, M. S. Blok | 2024 | [2407.17407](https://arxiv.org/abs/2407.17407) | `wang-2024-high-ej-ec-transmon-qudits-d12.pdf` |

**The primary calibration source for the transmon ladder-noise model.**
Published as Phys. Rev. Applied 23, 034046 (2025). Engineers $E_J/E_C$ ratios up
to 325 to resolve **12 levels on a single transmon** and then characterises them
level by level: process infidelities $e_f < 3\times10^{-3}$ for qubit-like
operations in every adjacent-level subspace across the lowest 10 levels, and a
10-state readout assignment fidelity of 93.8% using deep-neural-network
classification of a multi-tone dispersive measurement.

Two results bear directly on this repo's noise model. First, the Hahn echo time
$T_{2E}$ for the higher levels sits close to the $T_1$ limit and is **primarily
limited by bosonic enhancement** — that is the physical mechanism behind the
level-$k$ decay rate $\propto k$ ladder assumption, measured rather than
posited, and it is the strongest available justification for the transmon model.
Second, they verify the Josephson harmonics model as giving better predictions
for transition frequencies and charge dispersion than the standard transmon
Hamiltonian, which matters if the repo ever derives its rates from circuit
parameters. They also report strong $ZZ$-like coupling between higher levels in
a two-transmon system, relevant to two-qudit gate error at $d>2$.

This extends Peterer 2014 (#31, four levels) by a factor of three in $d$ and
comes from the same group as Blok 2020 (#10). Together, #31, #32, #10 and #42
give the repo four independent superconducting datasets on per-level coherence,
spanning $d = 3$ to $d = 12$ — enough to state the ladder scaling as an
empirical fact rather than a modelling choice.

---

## 2C. Adjacent context (retrieved, lower priority)

| # | Paper | Authors | Year | arXiv | File |
|---|---|---|---|---|---|
| 35 | Quantum Phase Estimation with Time-Frequency Qudits in a Single Photon | Hsuan-Hao Lu, Zixuan Hu, Mohammed S. Alshaykh, Alexandria J. Moore, Yuchen Wang, Poolad Imany, Andrew M. Weiner, Sabre Kais | 2019 | [1906.11401](https://arxiv.org/abs/1906.11401) | `lu-2019-qpe-time-frequency-qudits.pdf` |

The *first* qudit-based phase-estimation experiment on any platform, using time
and frequency degrees of freedom in one photon so the controlled-unitaries are
deterministic. Retrieves an arbitrary phase to one ternary digit. Establishes
priority for "qudit QPE has been done"; contains no noise-vs-d study.

| # | Paper | Authors | Year | arXiv | File |
|---|---|---|---|---|---|
| 36 | Efficient Implementation of a Quantum Algorithm with a Trapped Ion Qudit | Xiaoyang Shi, Jasmine Sinanan-Singh, Timothy J. Burke, John Chiaverini, Isaac L. Chuang | 2025 | [2506.09371](https://arxiv.org/abs/2506.09371) | `shi-2025-grover-trapped-ion-qudit.pdf` |

First Grover on a single trapped-ion qudit at d = 5 and d = 8, with `O(d)`
single-qudit gates and *no* entangling gates — 96.8(3)% and 69(6)% operation
fidelity. The measured d = 5 datapoint, and a clean illustration of the
entangling-gate-elimination half of the repo's mechanism.

| # | Paper | Authors | Year | arXiv | File |
|---|---|---|---|---|---|
| 37 | Realization of two-qutrit quantum algorithms on a programmable superconducting processor | Tanay Roy, Ziqian Li, Eliot Kapit, David I. Schuster | 2022 | [2211.06523](https://arxiv.org/abs/2211.06523) | `roy-2022-two-qutrit-algorithms-superconducting.pdf` |

Deutsch-Jozsa, Bernstein-Vazirani and Grover run on two transmon qutrits with
ancilla-free protocols. The transmon-side counterpart to #36.

| # | Paper | Authors | Year | arXiv | File |
|---|---|---|---|---|---|
| 38 | Extending the Computational Reach of a Superconducting Qutrit Processor | Noah Goss, Samuele Ferracin, Akel Hashim, Arnaud Carignan-Dugas, John Mark Kreikebaum, Ravi K. Naik, David I. Santiago, Irfan Siddiqi | 2023 | [2305.16507](https://arxiv.org/abs/2305.16507) | `goss-2023-extending-reach-qutrit-processor.pdf` |

First error-mitigation experiment on qutrits: noise tailoring for arbitrary
Markovian noise on a transmon qutrit processor, up to 3× improvement. Together
with Tripathi 2024 (#15) this is the mitigation the repo's ladder-noise
pessimism has to be stated against.

| # | Paper | Authors | Year | arXiv | File |
|---|---|---|---|---|---|
| 39 | QuantumSkynet: A High-Dimensional Quantum Computing Simulator | Andres Giraldo-Carvajal, Daniel A. Duque-Ramirez, Jose A. Jaramillo-Villegas | 2021 | [2106.15833](https://arxiv.org/abs/2106.15833) | `giraldocarvajal-2021-quantumskynet-simulator.pdf` |

A prior qudit simulator that explicitly demonstrates qudit Deutsch-Jozsa *and*
qudit phase estimation. Relevant as related tooling and for the
"less vulnerable to decoherence" claim in its abstract, which it asserts rather
than measures — a gap this repo fills.

| # | Paper | Authors | Year | arXiv | File |
|---|---|---|---|---|---|
| 40 | Qudit Noisy Stabilizer Formalism | Paul Aigner, Maria Flors Mor-Ruiz, Wolfgang Dür | 2025 | [2505.03889](https://arxiv.org/abs/2505.03889) | `aigner-2025-qudit-noisy-stabilizer-formalism.pdf` |

Efficient simulation of noisy qudit stabilizer states in prime-power dimensions
under generalized Pauli-diagonal noise. Methodological alternative for scaling
this repo's simulations past exact density-matrix limits, with the caveat that
it is restricted to stabilizer dynamics.

| # | Paper | Authors | Year | arXiv | File |
|---|---|---|---|---|---|
| 41 | Synthesis of Single Qutrit Circuits from Clifford+R | Erik J. Gustafson, Henry Lamm, Diyi Liu, Edison M. Murairi, Shuchen Zhu | 2025 | [2503.20203](https://arxiv.org/abs/2503.20203) | `gustafson-2025-single-qutrit-clifford-r-synthesis.pdf` |

Qutrit gate synthesis costs, reporting 35% and 69% *more* non-Clifford gates
than synthesizing the same unitary on two qubits. A concrete counterweight on
the compilation axis to the resource savings claimed elsewhere.

---

## Scoop-check evidence and coverage

Queried the arXiv API across ~46 distinct searches covering: Shor/order-finding/
factoring × qudit/qutrit/higher-dimensional/d-level; qudit and qutrit phase
estimation; qudit decoherence, depolarizing, amplitude damping, leakage and
noise-model simulation; qudit-vs-qubit comparison and advantage under noise;
success probability, fidelity scaling and resource estimation in dimension;
transmon qudit coherence; and the specific author and title strings for every
requested reference. Roughly 250 unique abstracts were triaged.

**Nothing does all of: (i) Shor order-finding *and* eigenstate QPE, (ii) success
probability as the metric, (iii) across d = 2, 3, 5, (iv) under two contrasting
physically motivated noise models, (v) with register-size scaling, (vi)
attributing the crossover to a control-work-vs-entanglement mechanism.** The
mechanism claim in particular — that the qudit advantage *flips sign* between
Shor and eigenstate QPE — has no precedent in anything retrieved. Scoop risk is
low; the exposure is not priority but insufficient differentiation from #22
(Janković), #23 (Gokhale) and #24 (Gustafson), each of which should be
addressed explicitly in the related-work section.

## Not found / not on arXiv

- **Parasa & Perkowski, "Quantum Phase Estimation Using Multivalued Logic"
  (ISMVL 2011)** — not on arXiv; IEEE Xplore only (DOI 10.1109/ISMVL.2011.47).
  The PDXScholar author's version link returns an empty response. Saved the
  authors' conference **slide deck** instead (`parasa-2011-qpe-multivalued-logic-SLIDES.pdf`,
  verified `%PDF`, 4.2 MB). Obtain the IEEE PDF before quoting numbers from it.
- No other requested item was missing: van Dam & Howard, Gustafson, Nikolaeva
  et al., Peterer et al., Cervera-Lierta et al. and Weng & Chuu were all located
  on arXiv and downloaded.

## Download status (second pass)

21 new files, 20 from arXiv plus 1 conference slide deck. All verified: each
begins with `%PDF` and exceeds 40 KB. No failures after retry. Library now holds
42 PDFs.

## Referee pass (third pass): exact success-probability analyses & QFT robustness

Added 2026-08-12, following the Floratos-style referee review of the paper's
decoder law (Sec. VII) and cost-model attribution. All IDs verified against
the arXiv API before download; all files begin with `%PDF`. These are the
works the decoder tolerance law must be positioned against — every one of
them analyses tolerance *windows* (the sufficient convergent guarantee) on
base-2 registers; none characterizes the exact continued-fraction acceptance
set, and none treats d > 2.

| # | Paper | Authors | Year | arXiv | File |
|---|---|---|---|---|---|
| 43 | On the success probability of quantum order finding | Martin Ekerå | 2022 (ACM ToQC 5(2):11, 2024) | [2201.07791](https://arxiv.org/abs/2201.07791) | `ekera-2022-success-probability-order-finding.pdf` |
| 44 | Tight Success Probabilities for Quantum Period Finding and Phase Estimation | Malik Magdon-Ismail, Khai Dong | 2025 | [2506.20527](https://arxiv.org/abs/2506.20527) | `magdon-2025-tight-success-probabilities-period-finding.pdf` |
| 45 | Sharp probability estimates for Shor's order-finding algorithm | P. S. Bourdon, H. T. Williams | 2006 (QIC 7(5–6):522, 2007) | [quant-ph/0607148](https://arxiv.org/abs/quant-ph/0607148) | `bourdon-2006-sharp-probability-estimates-shor.pdf` |
| 46 | Continued Fractions and Probability Estimations in the Shor Algorithm | Johanna Barzen, Frank Leymann | 2022 (AppliedMath 2(3):393) | [2205.01925](https://arxiv.org/abs/2205.01925) | `barzen-2022-continued-fractions-shor-treatise.pdf` |
| 47 | Shor's Factoring Algorithm and Modern Cryptography | Edward Gerjuoy | 2004 (Am. J. Phys. 73:521, 2005) | [quant-ph/0411184](https://arxiv.org/abs/quant-ph/0411184) | `gerjuoy-2004-shor-factoring-modern-cryptography.pdf` |
| 48 | A Precise Error Bound for Quantum Phase Estimation | Chappell, Lohe, von Smekal, Iqbal, Abbott | 2011 (PLoS ONE 6(5):e19663) | [1102.0108](https://arxiv.org/abs/1102.0108) | `chappell-2011-precise-error-bound-qpe.pdf` |
| 49 | Approximate Quantum Fourier Transform and Decoherence | Barenco, Ekert, Suominen, Törmä | 1996 (PRA 54:139) | [quant-ph/9601018](https://arxiv.org/abs/quant-ph/9601018) | `barenco-1996-approximate-qft-decoherence.pdf` |
| 50 | Scaling laws for Shor's algorithm with a banded quantum Fourier transform | Y. S. Nam, R. Blümel | 2013 | [1302.5844](https://arxiv.org/abs/1302.5844) | `nam-2013-scaling-laws-banded-qft.pdf` |

Notes: the bib entry `nam2012` (PRA 86, 044303) is the 2012 companion Pavlidis
& Floratos cite; it is not on arXiv, so the library carries the 2013 scaling
follow-up (#50). Khinchin's *Continued Fractions* (book, cited for the
mediant-interval measure) has no electronic copy here. All eight are also
registered in the ai-arxiv database (`../ai-arxiv/data/arxiv.db`), together
with Pavlidis & Floratos 1707.08834, which was in the library but not the db.

Library now holds 50 PDFs.
