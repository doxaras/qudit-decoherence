# arXiv publication plan

Working plan for a paper based on this repo's results, grounded in the
SOTA analysis (`docs/SOTA.md`) of the 21-paper library.

## Working title

*"When do prime-dimensional qudits help? Algorithm-level decoherence
comparison of Shor's algorithm and phase estimation on qubit, qutrit and
ququint registers under hardware-calibrated noise and realistic gate
costs"*

(shorter alt: *"Native gates or nothing: the condition for a qudit
advantage in phase-critical quantum algorithms"*)

**Revised one-line thesis** (after hardening tasks #1, #2, #4, #4b and #5 —
this supersedes three earlier versions):

> *Prime-dimensional qudits help phase-critical algorithms — both Shor
> order finding and eigenstate phase estimation — under one condition:
> the two-qudit entangling gate must be native at the device's operating
> dephasing level, i.e. its cost must grow no faster than linearly in d.
> The apparent exception for Shor reported in earlier drafts was a
> number-theoretic artifact of the N = 15 instance, not physics.*

The "at the device's operating dephasing level" clause is not hedging: it
is measured. Refocusing (`docs/ROBUSTNESS.md` §3) is worth roughly one
cost model's headroom — under linear-in-d gate cost the ququint loses Shor
without echo and wins with it.

Two supporting results, both novel and both methodological:

1. **Grid alignment is a confound in every cross-dimension algorithm
   comparison.** Phase estimation is sharpest when the target phase is
   exactly representable in the base being used. N = 15 admits only
   power-of-two orders, silently handing qubits perfect grid alignment.
   Measured over one instance per alignment class (r = 3, 4, 5, 6, 7) in
   two noise models, **the base that divides r wins in all 6 biased runs**
   (3 aligned instances × 2 noise models), while both unbiased instances
   give d = 5 > d = 3 > d = 2 in all 4 runs;
   a within-modulus control (N = 33 and N = 55, each carrying r = 5 and
   r = 10 on identical registers) isolates the effect from register width
   and prices it at ≈ 0.2 signal, against a residual physical qudit lead
   of 0.38–0.57. Controlling for it reverses the Shor conclusion. The
   literature does not discuss this, because it is invisible at fixed d.
2. **Compression is the mechanism, and the advantage responds at least
   proportionally to it.** Grover holds the oracle count fixed, halving the
   exposure compression (5.7× vs Shor's 10.9× at matched size; the split
   into width and depth is partial — see `docs/GROVER.md` §3). The qudit
   advantage survives at every size in both noise models but shrinks to
   0.33–0.50 of Shor's (1000-trajectory Shor statistics; see
   `docs/GROVER.md`), and obeys the same native-gate cost condition —
   so the condition is now tested on two genuinely different algorithms
   (amplitude-critical and phase-critical), not one family. See
   `docs/GROVER.md`. The exposure mechanism itself sharpens into a law
   with a stated boundary: in damage units (per-event channel
   infidelity, 1 − tr(S)/d²) exposure governs *state decay* across
   algorithms and bases (Grover collapses onto one exponential,
   R² ≥ 0.996 per family), and the residual algorithm dependence is the
   decoder transfer — continued-fraction recovery gains error tolerance
   with register size, decoding correct orders from states nearly
   orthogonal to the ideal one (`exposure_collapse.py`,
   `fidelity_collapse.py`).
3. **Control–work entanglement is a real but secondary effect**
   (≈ −0.025 signal per bit), measured by interpolating QPE from 0 to 2
   bits of entanglement. It does *not* explain the Shor/QPE difference —
   a falsified hypothesis we report as such.

Target: arXiv quant-ph; journal target PRX Quantum or Quantum (both
publish algorithm+noise simulation studies of this type; PRA as
fallback).

## Novelty claim (validated against the literature)

> Prior work compares qudit algorithms across dimensions by noiseless
> resource counts and treats decoherence as a compilation budget or a
> qualitative argument; qudit error-correction studies compare codes,
> which have no control register and therefore cannot exhibit
> algorithm-level mechanisms. We give the first quantitative, simulated
> comparison of Shor order-finding and phase-estimation success
> probability across d = 2, 3, 5 under decoherence channels calibrated
> to published per-level coherence measurements, with scaling in
> register size, and identify the single condition that governs both
> algorithms: the qudit advantage survives iff the two-qudit entangling
> gate is native, i.e. its cost grows no faster than linearly in d. We
> further identify a confound that invalidates naive cross-dimension
> comparisons — the exact representability of the target phase s/r in
> base d — show that it predicts the winner in all 6 biased runs
> while being invisible at fixed d, and control for it.

Anchor citations for the gap: Campbell PRL 2014 (noise-vs-d "depends
subtly on the underlying physics"), Marks 2017 (closing paragraph),
Kiktenko RMP 2023 (open problem #2), Pavlidis 2017 ("further
investigation to be carried").

Must-engage prior claims: Wang 2020 §6.1 (qualitative per-particle
argument), Parasa & Perkowski 2011 (secondhand exponential-improvement
claim — IEEE-only, obtain full PDF before quoting), Keppens 2025
(code-level opposite ordering — resolved by the
fixed-width-vs-compressed-circuit distinction, same noise convention),
Bocharov 2016 (encoding caveat), Gustafson 2022 (qutrit sQED encodings
tolerate 10–100× higher gate error — closest to our two-channel design,
supports us).

Must-differentiate (scoop check verdict LOW, these three own one axis
each): **Janković 2023** (arXiv:2302.04543 — analytic gate-level
qudit-vs-qubits noise criterion; also our cross-validation target),
**Gokhale 2019** (arXiv:1905.10481 — noisy qutrit circuit simulation,
gate-decomposition target), **Gustafson 2022** (above). Our unique
combination: algorithm-level success probability, d = 2/3/5, two
contrasting hardware-grounded channels, size scaling, and the
sign-flip mechanism (no precedent found in ~250 abstracts).

## Pre-publication hardening (ordered, with effort)

1. **[DONE — see `docs/CALIBRATION.md`] Calibrated transmon model
   re-run.** Channel fitted to measured per-level data (Γ_k ∝ k^0.7;
   max-level dephasing realized exactly via MDS embedding; d = 2
   bit-for-bit unchanged so the comparison is apples-to-apples).
   Verified against measured ratios (1.62 vs 1.7; 1 : 2.14 : 2.14 vs
   1 : 2.0 : 2.3), CPTP, 13 tests passing. **Outcome: the headline must
   be NARROWED.** The qubit Shor advantage is real but confined to small
   registers — the ququint deficit decays from 1.3σ at 7 bits to **0.1σ
   (dead heat) at 11.6 bits**, and in the high-E_J/E_C regime d = 5
   edges ahead (+0.039, 0.7σ — parity with a positive trend). The
   idealized model's "qubits dominate at every size" was an artifact of
   over-severe exponents. Meanwhile **eigenstate QPE is a qudit win at
   12–17σ in both regimes, widening with problem size** (slope ratio
   4.4×). Also: **d = 3 is the genuine loser in Shor** (0.07–0.12 behind
   at every size) — the story is not monotonic in d.

   > **Superseded by task 4b.** Both Shor findings in this item were
   > measured on the confounded N = 15 instance. On unbiased instances the
   > qubit Shor advantage does not exist at any size, and d = 3 is not the
   > loser but the *most size-robust* base (slope −0.000/bit vs the qubit's
   > −0.054). The calibration work itself — the fitted channel, the MDS
   > dephasing embedding, the two regimes — stands unchanged and is used by
   > every result since. Only its Shor conclusions are withdrawn; the QPE
   > conclusions hold.

   *(original task text)* Replace ∝k damping
   with ∝k^0.7 (Tripathi T1 table) and (Δlevel)² dephasing with a
   max(i,j)-law calibrated to Γφ ratios ≈ 1 : 2 : 2.3 (Goss/Blok echo
   data). Calibration sources now span four independent datasets,
   d = 3–12 (Peterer 1409.6031 — cite for ladder structure; Yurtalan;
   Blok; Wang 2407.17407 — whose T2E ≈ T1-limit finding at high E_J/E_C
   also motivates a "dephasing-scale" knob from 0 to charge-limited).
   Re-run demo + both scaling studies. Determines whether the "qubits
   win Shor on transmons" headline survives, softens, or flips. ~1 day
   of compute, small code change to `transmon_superop`.
1b. **[DONE — see `docs/ROBUSTNESS.md` §1] Janković cross-validation.**
   All three of their central equations reproduced from our superoperator
   code to a worst relative error of 4.1 × 10⁻⁴, with the residual
   identified as their own O((γt)²) truncation rather than our error
   (it tracks the infidelity itself). **Two outcomes beyond the
   credibility anchor.** (a) The exact break-even ratio at the dimensions
   we study is **1.68 (d = 3) and 3.45 (d = 5)**, against 5.68 and 10.77
   for the O(d²/log₂d) folklore — an independent derivation that the bar
   for prime-dimensional qudits is far lower than commonly assumed. This
   is the best external support for our thesis we have found and belongs
   in the introduction. (b) Used as a predictor of our own transmon
   results it agrees in **5 of 6** cost-model/dimension cases, including
   the tight one (d = 5 under uniform cost clears the curve 3.80 vs 3.45
   and wins). The single miss is in the conservative direction, as
   expected: our ladder channel's k^0.7 damping is gentler than their
   pure J_z dephasing.
2. **[DONE — see `docs/COST_SENSITIVITY.md`] Gate-cost sensitivity.**
   Three cost models implemented (`uniform` = native qudit gate;
   `ion` = Ringbauer's 2(d−1) MS gates; `pavlidis` = d² decomposition),
   with exact fractional channel powers so non-integer costs are exact.
   **Outcome: the claims must be narrowed substantially.** (a) *Shor
   never wins for qudits under any cost model* — the earlier
   "dead heat at scale" was an artifact of the most generous cost
   assumption; Shor becomes an honest negative result.
   > **(a) is superseded by task 4b** — it was an N = 15 result. Re-run on
   > the unbiased instance (`cost_fair.py`), Shor tracks QPE exactly:
   > qudits win under `uniform`, survive `ion` cost on per-particle noise,
   > and lose only under `pavlidis`. (b) and (c) below stand.

   (b) *QPE's qudit
   advantage survives linear-in-d cost but not quadratic*: +0.42
   (uniform/ions), +0.20 (ion cost/ions), +0.00 (ion cost/transmon),
   −0.09 to −0.27 (pavlidis). (c) Both **physically matched** pairings
   (ion costs + per-particle noise; native-CZ transmon + calibrated
   ladder) favour ququints for QPE. **The sharp condition — qudits win
   iff entangling cost grows no faster than linearly in d — is now the
   paper's most useful output**, and it explains the field's split
   results (Gokhale's native-ancilla qutrit wins vs Gustafson 2025's
   35–69% synthesis penalty).
3. **[High] Device operating points on every figure.** Mark measured
   per-gate noise strengths (transmon 2-qudit ~10⁻²; ion ~10⁻³) on the
   x-axes so readers see where hardware sits today.
4. **[DONE — see `docs/MECHANISM.md`] Entanglement-interpolation
   experiment.** QPE run on a K-fold eigenstate superposition, sweeping
   control–work entanglement over 0 → 2 bits (verified exactly log₂K).
   **Outcome: hypothesis falsified.** Entanglement costs only ≈ 0.025
   signal per bit — 10% of the effect it was meant to explain. Chasing
   the failure exposed the **grid-alignment confound**, which retracts
   the "qudits lose Shor" result and unifies both algorithms under the
   single gate-cost condition. The most valuable experiment in the
   project so far, precisely because it failed.

4b. **[DONE — see `docs/GRID_ALIGNMENT.md`] Re-run everything on unbiased
   instances.** Demo sweep (`fair_demo.py`), scaling study
   (`scaling_fair.py`) and cost grid (`cost_fair.py`) all repeated on
   N = 21, a = 2 (r = 6); a second unbiased instance (N = 29, a = 16,
   r = 7) added to the alignment series. **Outcome: the retraction is
   confirmed and becomes the stronger claim.** On unbiased instances
   qudits beat qubits at *every* noise strength under *all three* noise
   models — including the idealized ladder (Γ_k ∝ k, (Δlevel)²
   dephasing) that produced the original "qubits win Shor on transmons"
   headline, where the qubit now trails by 0.16–0.52. That headline does
   not survive de-confounding at all; calibration merely softened it.
   Grid alignment now has its own figure and two supporting results:
   **6/6 prediction accuracy** on the biased instances (3 aligned
   instances × 2 noise models — the base dividing r always wins), and a
   **within-modulus
   control** (N = 33 and N = 55, each hosting r = 5 and r = 10 on
   identical registers) that isolates alignment from register width and
   prices it at ≈ 0.2 signal, against a residual physical qudit lead of
   0.38–0.57. Also documented: a base-2-aligned within-N control is
   *impossible* to construct at D ≥ 64, because r = 4's continued-fraction
   floor exceeds its noiseless baseline at every modulus large enough to
   also carry a non-power-of-two order (N = 35, 39, 55, 65 measured).
5. **[DONE — see `docs/ROBUSTNESS.md` §3] DD-on variant.** Dephasing
   scaled from 1 to 0 with pulse cost bracketed by the `uniform` and
   `ion` cost models. **Outcome: echo helps qudits more than qubits,
   monotonically, in all four conditions — and it moves the paper's
   central condition.** Under linear-in-d gate cost the ququint *loses*
   Shor without echo (−0.026) and *wins* with it (+0.191); QPE moves from
   an exact dead heat to +0.196. Mechanism: DD suppresses dephasing,
   which is the part of the ladder channel scaling worst with d
   (max-level law), and leaves the gentler k^0.7 relaxation. The
   condition should be stated as "native gate *at the device's operating
   dephasing level*", with refocusing worth roughly one cost model's
   headroom. Also sharpens direction (C): the DD crossover dimension is
   bracketed but not located — that needs a per-pulse error model.
6. **[DONE — see `docs/ROBUSTNESS.md` §2] d-dependent SPAM.** Readout
   channel with misread rate of |k⟩ growing as (1+k), charged on every
   control qudit of every base, floors and baselines recomputed at each
   ε. **Outcome: the advantage is untouched** — the ququint's lead drifts
   by less than ±0.03 across a 4× range of readout error, and in Shor
   slightly widens. **The reason is a structural cancellation worth
   reporting**: total readout exposure is m × ε(d+1)/2, and at matched
   precision m ≈ log D/log d, giving 9ε / 8ε / 9ε for d = 2/3/5 at
   D ≈ 64. The growth of per-level readout error with d is almost exactly
   cancelled by the reduction in carrier count, so d-dependent SPAM is
   near-neutral between bases by construction.
7. **[Medium] Statistics.** Final figures at ≥1000 trajectories/point
   (batch the trajectory engine or just burn compute).
8. **[DONE — see `docs/SOTA.md` §6] Keppens reconciliation and Bocharov
   encoding note**, both drafted as paper-ready prose, plus a status
   table tracking every calibration issue raised in the SOTA read
   (six fixed or charged, two open and stated as limitations).

## Proposed paper structure

1. Introduction — the recognized open question (4 anchor quotes), our
   answer in one figure.
2. Setup — circuits, cost model (3 variants), noise channels (calibrated
   from published device data — table of sources), success metrics with
   floor correction.
3. Results I — demo-size: noise structure decides the ordering.
4. Results II — scaling: per-particle advantage compounds with size;
   crossover analysis.
5. Results III — beyond Shor: eigenstate QPE, the entanglement
   mechanism, interpolation experiment.
6. Discussion — hardware implications (which platform first), relation
   to code-level results (Keppens), limitations (coherent errors,
   cross-Kerr, SPAM), outlook.
7. Methods — exact + trajectory simulators, validation, reproducibility
   (repo link).

## Innovation directions beyond the paper (ranked)

A. **Hardware proposal: first qudit algorithm demonstration.** Eigenstate
   QPE at d = 5, m = 2–3 on a Ringbauer-class ion processor needs only
   ~8–12 two-qudit gates — inside today's budget (Cinc 93.8% → ~half the
   shots survive 8 gates). A concrete pulse-level proposal (gate list,
   expected success probability from our calibrated simulation) could be
   the paper's closing section or a standalone follow-up with an
   experimental group. Nobody has run *any* algorithm on a qudit
   register above d = 3.
B. **Noise-aware level mapping.** Low 2023 shows per-level error spans
   3–34% at d = 13 but is *unordered* (tracks κ²τ², not level index) and
   optimal level choice keeps fidelity flat with d. A compiler pass that
   permutes logical levels to put high-traffic amplitudes on quiet
   physical levels is unexplored and directly buildable in our
   simulator (per-level rate vectors instead of uniform γ).
C. **DD crossover dimension.** DD gain grows with d but pulse cost grows
   as 2(d−1); the dimension where DD stops paying is cheaply computable
   with our machinery and experimentally testable — a short standalone
   result.
D. **Chemically tunable noise (with a chemistry group).** Chiesa's
   Eq. 38 says exchange topology interpolates between our two noise
   models within one material class; our simulator can predict algorithm
   performance vs exchange parameters — a design rule for molecular
   qudit chemistry.
E. **NV skip-channel model.** Add the 1/Δ² Δm=2 channel and derive the
   optimal d for NV-class hardware as a function of field — small,
   self-contained, experimentally grounded.

## Honesty constraints (from the literature read)

- Do not claim novelty for "fewer carriers ⇒ less local noise" (Wang
  2020 says it); claim the quantification, the channels, the scaling,
  and the mechanism.
- Do not attribute the qudit win to encoding density (Bocharov
  counter-example); attribute it to width+depth compression at matched
  problem size.
- Charge (or bound) the d-dependent gate-cost penalty (Pavlidis d²; ion
  2(d−1)) — a d-independent per-gate cost flatters qudits.
- State clearly that d = 5 two-qudit gates exist only on ions today, and
  our deep-register results are 1–2 hardware generations ahead.
