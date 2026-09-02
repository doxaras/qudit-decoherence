# Revision status — 3-referee review response (started 2026-08-31)

Referee reports: see review REVIEW.md (delivered in session). Panel: major revision.

**Round 5 (2026-08-31, contrarian panel, `reviews/round5/`)**: second
independent 3-referee pass (experimentalist / theorist / citation-integrity)
grounded in `docs/REFERENCE_DEPTH_AUDIT.md`. Composite: major revision. Many
findings duplicate items already fixed above (Garnet rescue, secular form,
transmon both-scope failure, N=29 Sec-III reversal, Jankovic reframe,
conditional d>=5 labels). See `reviews/round5/SYNTHESIS.md` for the
deduplicated fix list. Round-5-specific work is tracked in the section
"Round-5 additions" at the bottom of this file.

## Done

- [x] **Secular relaxation form** (`qudit_shor.py`): per-transition jump operators
  now default for both ladder channels (`relaxation="secular"`; collective kept
  as option). Validated: d=2 bit-identical, populations and damage identity
  unchanged, CPTP exact, 20/20 tests pass. `cost_fair.json` regenerated —
  matches Referee 1's predicted secular values to 4 decimals.
- [x] Table II ladder rows updated (0.517/0.544, 0.302/0.167, 0.260/0.073);
  ladder/pavlidis bold moved to d=2. Abstract, intro quote, and cost-section
  prose updated for the flipped cell.
- [x] Methods/Setup: channel description now states the secular form explicitly.
- [x] **Garnet finding rewritten** (paper Sec. IX, TEXTBOOK.md, HARDWARE.md):
  single inverted control qubit ($10, most-routed, 35 CZs) — popcount rules out
  bit-order bugs; corrected m=5 success 0.377 vs 0.353 predicted (in band,
  TV=0.09); m=7 control register floor-pinned/uninformative. "3–4× coherent
  excess" withdrawn.
- [x] **Pre-registration language removed** (main.tex:246, :2382 area;
  AQFT band disclosed as post-hoc; dangling commit hash in
  trajectory_variance.json note replaced with hash-free pointer).
- [x] Table VII: per-device scoring conventions stated (IonQ reversed, Garnet
  plain); caption's accounting description corrected; m=7 error bar ±0.002.
- [x] Implied-strength claim corrected (paper + README + TEXTBOOK): 0.0065
  layer-counted / 0.0104 timed; vendor 0.7% between conventions, inside neither CI.
- [x] m=7 relabeling significance claim inverted (0.15 is ~99σ above null;
  real argument = far below prediction + shifted peak y=84 vs 79). Paper + HARDWARE.md.
- [x] **crossing_bootstrap.py written** (was missing); reproduces committed
  medians/CIs to 2 decimals; seeded; added to Makefile. Paper now says
  "error-weighted fits" and carries the plateau-not-line caveat + matched-precision
  3.5σ variant of the deep-size gap.
- [x] Appendix A proof gap: r∤(q−q′) disjointness sentence added.
- [x] Eq. (6) validity domain added (overlap growth at small orders, N=15 r=2
  +12%/+14%; law scoped to scorable instances).
- [x] Jankovic reframed: not independent; bar under paper's own channel
  1.23/1.63/1.98 → 5/6 agreement; "errs conservative" attribution split
  dephasing-structure vs relaxation.
- [x] Winner tally scoped as non-inferential (paper).
- [x] README: 6 of 6→5 of 6, 1.6×→1.1×, strength range. GRID_ALIGNMENT.md,
  PUBLICATION_PLAN.md same. COST_SENSITIVITY.md: pavlidis convention fixed
  (two-qudit-only), layer table 48.5/62.25 with historical note.
- [x] Small fixes: Fig. 1 caption 5.3e5→2.0e6; 2.82s→2.83s; R²=1.00→0.997;
  "oracle count fixed" → at matched M (interpolated); grover.py docstring
  (iteration count not exact optimum, cancels across bases);
  trajectory_variance.py stale seeding docstring.

## In progress

- [ ] **Background rerun** (`revision_rerun.log`): 27 ladder-affected scripts
  under secular form (fair_demo, d7/d11_demo, matched_D, grover, QPE, all
  robustness, collapse, cost sweeps, cost_sensitivity). When done: sweep ALL
  prose numbers in main.tex + docs against the new JSONs. Known pending spots:
  - d=7 demo replication parenthetical (removed from cost prose; re-add with
    new numbers from d7_demo.json)
  - QPE ladder/ion "dead heat" clause (removed; re-add from fair_demo.json)
  - Sec. VIII robustness numbers (dd, α*, concurrency, f* re-readings,
    quasistatic/thermal, composite/d4 controls) — all ladder cells shift
  - jankovic.json tallies; exposure/fidelity collapse R²s and rates
  - COST_SENSITIVITY.md results table (regenerate from new cost_sensitivity.json)
  - figures: rerun plots_* after data lands; then rebuild paper PDF

## Prose sweep vs regenerated data (applied 2026-08-31, referee discrepancy list)

Applied (verdict-level): abstract + intro "seven of eight" -> eight of
eight ququint readings; transmon qutrit now FAILS BOTH scopes
(f*_gate=2.93 < f=3.08; targets 97.4%/98.5% vs 97.3% measured) --
abstract, intro, Sec VIII, Discussion all updated; timed rho*=1.88
(~310 ns, IBM-class point lost); d=4 tally 5/8 -> 4/8; ququint
gate-only ladder pass -> lost centrally; leakage "rescues neither
scope"; dd/refocusing rewritten (no ion-cost reversal at any dephasing
scale; qutrit +0.019->+0.054 the only ion cell moving; headroom "a
fraction of a cost model"); ladder ion f* undefined at s=0.003
(strength-dependent verdict noted); f* 2.0-2.5 -> 1.7-1.9; 2d-MS f*
0.70/0.52; dephase-ratio + quasistatic rewrites (ion qutrit cell sign
flips across grid); composite family 0.44/0.58/0.69/0.64/0.70 (both
composites top the ladder band); Table VII (tab:hrmo) ladder rows +
f* labels; matched-D, d7/d11 demo numbers; Grover ladder d5>d3 leg
now a tie at deepest matched size (caption + text softened); Grover
family rates 0.445/0.553/0.538 (1.24x vs 4.55x event); favg both
channels tighten; log-fid 0.76-0.84 (0.85-0.95 refit) incl. abstract;
Sec VI damage-unit passage replaced with the hardened omega/rate-test
draft (R1-M5 CLOSED); restorations (a) d7 replication and (b) QPE
ion-cost clause; COST_SENSITIVITY.md results tables regenerated.

Deferred -- pending long batch (pre-secular scaling_fair contamination
of pooled fits): Table IV rows 1-2 (0.67/0.84 ladder), nested-fit
R2=0.953 sentence, mechanism figure caption R2 ranges, Shor-d3
plateau level ~0.73. Refresh from final exposure/fidelity_collapse
after the batch, incl. the mechanism.png replot.

PART 2 applied (2026-08-31): Table VI fully regenerated (uniform d3
0.679-0.561 keeps the qutrit conclusion; ion column now belongs to
the qubit at every exponent incl. the published calibration, 0.504
vs 0.506); alpha* updates (ladder/uniform 3.29; ladder/ion 0.61 --
"fails at exactly the measured charge" coincidence gone; ladder/
pavlidis needs no threshold, qubit leads at alpha=0); concurrency
rewrite (the one flip is now ladder/ion +0.020 -> -0.054; ladder/ion
serial win is CREATED by the serial convention; margin inflation
up to 1.7x among surviving cells); ququint tally "two surviving only
at -1sigma" (fresh hrmo_gate_only: depol/uniform/gate 0.290 vs
0.331, -1sigma 0.383; ion/gate 0.248 lost outright) -- abstract,
Sec VIII, Discussion "seven of eight" leftover fixed; hrmo citation
split (ladder rows transmon_rebuild, depol rows hrmo_gate_only);
interpolation slopes -0.003+/-0.013 etc., bound ~0.10; Eq. (10) now
predicts 12/12 verdicts and 5/6 row winners (the collective-form
miss resolved by the secular correction -- verified arithmetically:
7*48.5*1.4623=496 > 11*57*0.75=470 predicts qubit, measured qubit).

Still deferred -- pending artifacts: ladder_exponent_sensitivity_d7
-> the d=7 exponent-sweep prose (0.682 to 0.075, tied at 1.6,
0.345+/-0.025) NOT regenerated; grid_alignment/same_n_control/
ensemble_a* -> Sec III ladder columns incl. Table I and unbiased
d5>d3>d2 ordering claims (long batch); goss_transmon_test.json;
Grover 0.33-0.50 ratio pending plots_grover recheck. Table VII ion
d=3 ladder f* "<1" from noise_inflation (f_star null at s=0.003).
transmon_rebuild/hrmo_reanalysis/goss_transmon_test re-running with
runtime-computed f_star labels (code fixed).


PART 3 applied (2026-08-31 evening): Sec III unbiased-ordering claims
corrected (ladder N=29 is a 2.0-sigma qutrit-over-ququint REVERSAL:
0.446/0.599/0.525; depolarizing keeps d5>d3>d2 at both moduli) in
figure caption + prose; sigma tiers ">=7 sigma depol / 2.3-4.7 sigma
ladder"; within-modulus prices 0.19-0.26, narrowing 0.17-0.26,
residual 0.33-0.59, "1.5-2x the alignment term", price quoted as
~0.2-0.26 consistently (intro (i), Sec III scoping line, ensembles);
Table I (tab:ensemble) N=33/N=55 rows regenerated (verified vs
ensemble_a_n33/n55.json to 3 decimals); aligned-excess sentence
+0.24/+0.19 and +0.24/+0.18; aligned ququint 1.01/0.98 & 1.01/0.99;
QPE hi-res margins +0.31 (2.3x) measured, +0.32 (1.8x) low-charge
(verified by direct interpolation of qpe_hires_1000.json: 0.311/2.26,
0.318/1.78).

Part 3 item 7 NOT applied (flagged back to referee): the qubit ladder
slope cannot change under the secular form (d=2 channel provably
invariant) and fresh scaling_claims.json weighted fit reproduces the
existing text exactly (-0.0488+/-0.0048, R2=0.974, n=4). The proposed
-0.052+/-0.009 / R2=0.92 appears to be an unweighted or stale-file
fit; paper quotes the weighted variant. Left as is.

Still deferred (Part 3 item 9 list): deep-size claims (n=7/n=5
slopes, 3.3+/-0.7 ratio, plateau-fall numbers, 3.5/5.0 sigma, both
crossings + CIs, 0.568/0.407 pair), Table I N=21 row (ensemble_a
re-running), thermal paragraph (ladder_thermal re-running on fixed
generator), collapse Table IV rows 1-2 + nested R2 + mechanism fig
caption + Shor-plateau level, Grover 0.33-0.50 ratio + matched-size
ordering claim. "Plateau consistent with zero over first five sizes"
CONFIRMED by fresh slopes (-0.011+/-0.010, -0.004+/-0.011), left as
is.


PART 4 applied (2026-09-01): thermal paragraph regenerated on the
fixed secular generator (qubit 0.51->0.45 at nbar=0.05, all three
bases dip comparably there; 0.05/0.61 at nbar=0.4; gaps
+0.17->+0.48 and +0.22->+0.56 "monotonically within errors"; total
losses 0.46/0.15/0.12; note added that the "qubit" is a three-level
ladder in this study); Table I N=21 row 0.52/0.68/0.69 (verified vs
ensemble_a.json); full-ensemble excess -0.006/+0.027/+0.015; the
d5>d3 scorable-class statement scoped to DEPOLARIZING (ladder full
ensemble orders d3>d5, r=6 class a tie 0.69 vs 0.68); d=7 exponent
prose from fresh _d7 file (0.572->0.055; 3.8-sigma below the qubit
already at exponent 1.6 -- the old "tied at 1.6" claim is gone;
6.5 sigma at 2.0; worst draw -2.7 sigma); Sec IV d=7 uniform-cost
win at s=0.003 flagged as a 2-sigma statement (+0.062+/-0.030), with
the trajectory file corroborating the d=5 optimum (0.690 vs 0.572).
All verified against ladder_thermal.json / ensemble_a.json /
ladder_exponent_sensitivity_d7.json before applying.

Remaining deferrals after Part 4: collapse Table IV rows 1-2 +
nested R2 + mechanism fig caption + Shor-plateau level (final
exposure/fidelity_collapse), deep-size claims + crossings + 3.3
ratio (final scaling_claims pass), Grover 0.33-0.50 ratio +
matched-size ordering (plots_grover), figure regeneration (plots_*).
Part 3 item 7 RESOLVED: referee withdrew it -- existing text
(-0.049+/-0.005, weighted, 1000-traj) kept; the 400-vs-1000
provenance issue is addressed by regenerating scaling_fair_1000.json.


PART 5 applied (2026-09-01): final collapse numbers -- Table IV rows
0.59/0.77 and 0.82/0.77 (verified vs final exposure_collapse.json:
X0 ladder 0.5941, X1 0.8223); prose R2=0.59/0.77; nested-fit
sentence restored to the spanning phrasing with final range
0.81-0.94 ladder / 0.93-0.94 depol (both abscissae now stored);
mechanism caption 0.77-0.83 and 0.93-0.94; Shor d=3 flat level
~0.65 (rate 0.047/0.002, flatness claim kept); log-fid 0.76-0.84
(0.85-0.95 refit) and omega-passage k/A values confirmed against
final logfid_rescore.json (k=0.6891/0.8066) -- no change needed.
THE GROVER BAND REPLACED in all three locations (intro clause, fig
caption, body): 0.33-0.50 no longer exists; now 0.43-0.57 of Shor's
under depolarizing / 0.12-0.19 ladder at the shallowest matched
size, falling toward zero with depth (no decoder reprieve); ordering
claim finalized (d5>d3>d2 at shallowest size both channels, tie by
~7 bits on ladder, unresolvable at the 1/M floor at depth); the
"Halving costs one-half to two-thirds" sentence adjusted to "at
least half ... more than proportionally". All deferred collapse/
Grover items from Parts 1-4 are now CLOSED.

Remaining after Part 5: deep-size claims + crossings + 3.3 ratio
(final scaling_claims pass -- note crossing_bootstrap.py should be
re-run after any scaling_claims regeneration), figure regeneration
(plots_*), COST_SENSITIVITY doc final check, Part 3 item 7
disagreement (qubit ladder slope) awaiting referee reconciliation,
final referee re-verification pass, rebuild arXiv tarball.


PART 6 applied (2026-09-01, FINAL data pass): Sec V slopes (d3 ladder
R2 0.69; d5 ladder -0.044+/-0.003, R2 0.994 incl. crossing passage;
ratio 3.2+/-0.7 -- all verified vs fresh scaling_claims.json);
plateau spread 0.043 (0.644-0.687), chi2/dof=1.20 (p=0.70), the
earlier-release chi2=0.015 defense sentence CUT (approved); ladder
fall 4.25 sigma at 14.3 bits, 15.8-bit point 0.525+/-0.032 (4.1
sigma); crossings 7.7 [7.0-8.3] and 14.7 [13.1-17.6] (verified vs
fresh crossing_bootstrap.json medians 7.68/14.69); four-regime
sentence corrected (idealized crosses at 2.0 bits below the measured
range -- NOT "never"; low-charge crosses INSIDE the register range
at 9.9); qutrit weighted-R2 caveat 0.38-0.71; deep-size comparison
0.525+/-0.032 vs 0.298+/-0.031 (5.1 sigma; matched-precision
0.529/0.379, 3.5 sigma -- both recomputed independently); N=29
passage parenthetical 8.7->7.7; Methods provenance note added (d2m12
quoted at 1000 traj from the deep file, 0.227 vs 0.200, ~1 sigma).
Figures regenerated (12 pngs, Sep 1 19:55) and picked up by the
build -- PDF is now 31 pages (was 30; figure aspect changes).

FLAG for referee: the N=29 crossing "10.5 bits" (line ~1252) was not
in Part 6's verified set -- confirm it against the regenerated
N=29 fit or supply the fresh value.

ALL data applications complete (Parts 1-6). Remaining: Part 3 item 7
reconciliation, N=29 crossing check above, final referee
re-verification pass, arXiv tarball rebuild, author commit.

## Still to do (from referee reports)

- [x] **R1-M3**: dd_study "echo" claim — restate as E_J/E_C engineering only
  (Markovian dephasing is echo-immune), or redo with Sec. VIII permutation
  machinery + per-pulse charge; fix dd_study.py docstring's "perfect echo"
  and its entangling-cost "bracket" claim.
- [x] **R1-M4**: move coherent-vs-incoherent conversion caveat into the
  statement of the second condition; state fidelity conventions
  (Bell-state vs process) for Hrmo/Goss numbers.
- [x] **R1 minor 2**: label d≥5 ladder results conditional (abstract + Table II
  note) on the max(j,k)^1.1 extrapolation; soften charge-dispersion sentence.
- [x] **R1-M5**: DONE — hardened omega/rate-test passage in Sec VI (referee-drafted, applied 2026-08-31).
- [ ] **R1 minor 1**: one readout-exponent sweep row (α ∈ {0, 0.5, 1, 1.5, 2}).
- [x] **R1 minor 3/4**: depolarizing = twirled gate-error model (state it);
  quasistatic σ convention = scale-setting only (ordering convention-free,
  margin not).
- [x] **R3 minor 3**: debiasing-ensemble variance + vendor-fidelity drift
  caveat on the 0.60–0.70 band.
- [x] **R3 minor 4/5**: weighted-fit variants added alongside unweighted
  (fit_exp err param; pooled weighted fit printed; per-family log R²s
  flagged diagnostic-only; n_traj_note header field).
- [x] **R3 minor 10** (numbers to refresh after ladder re-runs): show all four regimes' crossings next to the 8.7-bit figure.
- [x] **R1 minor 7**: completeness guard assertion in trajectories.py.
- [ ] **Long re-runs** (hours; run overnight): scaling_fair.py + scaling_fair_*
  ladder rows, ensemble_a_traj, grid_alignment.py, same_n_control.py,
  qpe_hires under secular; then scaling_claims.py + crossing_bootstrap.py
  (transmon_cal crossing will move); collapse_tail_deep.
- [ ] **Hardware follow-ups** (author, few cents): re-fetch Braket result
  objects (measuredQubits field) or run |0⟩/|1⟩ readout calibration on
  Garnet $10 to resolve the inversion's origin.
- [ ] Rebuild paper/main.pdf (latexmk) after number sweep; regenerate figures.
- [ ] Final referee re-check pass over the revised manuscript.

## Round-5 additions (2026-09-01)

### Applied (citation-repair batch, main.tex + refs.bib; PDF rebuilt clean)

- [x] Lu 2020 miscite fixed: "$d=32$ Shor and qudit QPE" split into
  "$d=32$ Shor [weng2024] and qutrit QPE [lu2020]" (Lu is d=3).
- [x] shi2025 removed from "earlier d=3 circuit work" (single ion, d=5/8,
  zero entangling gates); roy2022 flagged as superconducting.
- [x] Readout fidelities and few-percent readout cites goss2022 -> goss2024
  (goss2022 reports no assignment fidelities).
- [x] Cross-Kerr range 0.1--0.7 -> 0.1--0.6 MHz, cite goss2024 added
  (values are goss2024 Table A1; 0.7 unsourced).
- [x] low2023 removed from the 1e-3--1e-4 single-qudit-error cite
  (SPAM-only paper, 8-13% errors); "13 levels" scoped to
  "state preparation and readout".
- [x] Relaxation-ratio sentence rewritten: "nine devices ~1.7" ->
  "1.6--2.1 across transmon-class devices, channel realizes 1.62 (low
  end)"; yurtalan2020 named as flux-qudit outlier at 4.2, excluded.
- [x] Dephasing anchor 1:2.0:2.3 attributed to Blok five-qutrit RAMSEY
  data explicitly, with upper-composite caveat (echo shallower,
  quasi-static steeper).
- [x] Hrmo maximal-entanglement caveat added in two places: intro
  ("single application up to d=4, d=5 needs repeated applications") and
  uniform cost-model definition (circuit-layer convention; pulse-linear
  reading is the ion model).
- [x] Jankovic wording corrected ("Haar-random input states,
  gate-independent") + off-lattice flag for 1.68/3.45/5.70 at odd primes.
- [x] goss2024 "3x" restated as GHZ *state* infidelity at ~60x sampling
  overhead; "gap within reach of demonstrated mitigation" -> transfer is
  a conjecture (no post-mitigation gate fidelity reported).
- [x] Ringbauer 100 ms restated as achievability projection (3 spots:
  "Measured devices are engineered" -> "Devices can be engineered";
  "(if realized)" on the factor-two margin; "idle-coherence projection").
- [x] nikolaeva2024toffoli (arXiv:2407.07758, 171Yb+ qutrit Toffoli,
  measured algorithm-level fidelities) added to refs.bib and cited in the
  intro as closest experimental precedent for the Sec-Discussion proposal.

### Done (2026-09-01): decoder_convention_study.py — BOTH R5-R2 claims CONFIRMED

`results/decoder_convention_study.json`, log `decoder_study.log`. Paper-decoder
column reproduces Table II exactly (floors 0.125/0.1235/0.128).

- **R5-R2-M2 CONFIRMED (Part 1, N=21 exact rho, s=0.005).** Under a
  lifting decoder (lift_best = best convergent + Odlyzko lift; lift_small
  = all convergents, k<=4) every d5-over-d3 ordering dissolves:
  ladder/uniform d3 0.517->0.708 vs d5 0.544->0.514 (FLIPS);
  depol/ion 0.497->0.666 vs 0.502->0.494 (FLIPS);
  depol/uniform d5 win -> exact tie (0.781 vs 0.782).
  Qutrit-over-qubit survives everywhere (qubit 0.400/0.369 lift_best).
  Abstract's "d=5 leads on the calibrated ladder" cannot stand.
- **R5-R2-M1 CONFIRMED (Part 2, N=29, a=16, r=7 alignment-neutral,
  1000 traj).** The ladder/ion qutrit cell flips to the QUBIT at N=29:
  d2 0.243+/-0.014 vs d3 0.187+/-0.012 (~3 sigma), where N=21 gave the
  qutrit +0.020. depol/pavlidis d5 drops below the qubit
  (0.187+/-0.014 vs 0.271+/-0.013); depol/uniform ordering d5>d3>d2
  survives; ladder/uniform d5-d3 is a statistical tie (0.435 vs 0.422).
  The "thin" ladder/ion qutrit win is measured instance-dependent.
- Side-finding: N=29/a=2 (r=28) is UNSCORABLE at d=2 under the paper
  decoder (noiseless = floor = 0.000) — new member of the paper's own
  unscorable class; footnote-worthy in Sec. III.
- [x] Paper actions APPLIED (2026-09-02): new "Decoder and modulus
  conventions" paragraph in Sec IV (full study numbers, granularity
  mechanism, r=28 unscorability); Table II caption scopes every
  d5-over-d3 bolding; "matched pairings favor ququints" -> "favor
  qudits" with ordering conditional; ladder/ion thin-win sentence
  carries the modulus reversal; Sec V crossing carries the
  non-lifting-decoder scope. PDF rebuilds clean.
- [x] N=29 provenance closed (2026-09-02): `n29_claims.py` written
  (imports fit/series/load from scaling_claims.py; writes
  results/n29_claims.json); reproduces the 9.3-bit crossing (9.347)
  and every slope. Two stale prose cells corrected against final
  data: ququint matched-range pair -0.058±0.010 vs -0.047±0.007
  (0.9 sigma, was -0.043±0.006 / 1.4 sigma — replication now
  STRONGER); qutrit pair error bar ±0.009 -> ±0.006 (1.6 sigma);
  depol non-replication 3.6 -> 3.7 sigma.

### Still to do (round-5-specific, not covered above)

- [x] ALL FOUR COMPUTE ITEMS CLOSED (2026-09-02,
  roundfive_closures.py + scaling_exponent_sweep.py; results in
  results/roundfive_closures.json + results/scaling_exponent_sweep.json;
  paper edits applied, PDF + tarballs rebuilt):
  * R5-R2-M4 pavlidis d^3: the surviving depol/pavlidis qutrit cell
    ERASES at the MMAC charge (0.326 vs qubit 0.331, dead heat; ladder
    0.119, d=5 0.096/0.004). Cost-section caveat + "survivable only by"
    sentence updated.
  * R5-R1-M2 timed ion: LS-only d/2 charge -- qutrit 0.398/0.576,
    ququint 0.299/0.627 vs qubit 0.282/0.331; with-locals ~d bracketed
    by the ion column. Ion qutrit SURVIVES its own timed convention.
    Wall-clock passage extended.
  * R5-R1-M6 state-prep: (1+k) misprep sweep 0-0.04 flips no ordering,
    qudit leads widen (0.135/0.386/0.389 at 0.04); scope caveat re
    basis-state prep vs low2023 arbitrary-level prep. SPAM passage
    extended. Shelving-readout charge on tab:prediction: every pair
    survives (b=5: 0.747/0.628; b=6: 0.649/0.518 at s=0.001; b=4
    inverts TOWARD the ququint); budget item (ii) + caption updated.
  * R5-R2-M8/R3-M4 exponents: Table VI gains the echo-derived 0.8 row
    (uniform 0.692/0.728, ion qutrit 0.522 above the qubit -- one-sided
    risk statement added); scaling families re-run at 1.6/2.0 (qutrit
    flat +0.004/-0.001 per bit; qubit -0.040/-0.063; ququint
    -0.049/-0.058) -- Sec V exponent-robustness passage added.
- [ ] R5-R2-M7: replace "n of m readings" tallies with
  independent-measurement counts (8 ququint readings = 1 measurement
  through 8 deterministic conversions); FDR/multiplicity statement.
- [x] R5-R3 minor-cite batch APPLIED (2026-09-02): keppens MWPM/flag
  disclosure; bocharov carry-lookahead disclosure; gustafson
  asymptotic/diagonal qualifiers (12-40% at practical precision);
  marks "misleading" caveat; campbell2014 d>=5 exclusion note.
- [x] R5-R2-M7 tally rewrite APPLIED (2026-09-02): abstract/intro/
  Sec VIII/conclusion now read "all eight readings of the accounting";
  Sec VIII carries the independence statement (one measured fidelity
  through deterministic channel/cost/scope conversions; only the
  matched pairings read a real platform).
- [x] Abstract trimmed to fit arXiv metadata cap (2026-09-02): the
  revision rounds had grown it to ~2260 rendered chars vs the 1920
  cap, and docs/ARXIV_SUBMISSION.md still carried the pre-revision
  seven-of-eight text. Both fixed: paper abstract tightened (no claim
  dropped; the codes-have-no-instance clause and the cross-base
  punchline moved to body-only), metadata block re-rendered verbatim
  at 1914 ASCII chars.
- [x] Bib year drift: already fixed in refs.bib (low2023 -> npj QI
  2025, shi2025 -> Nat Commun 2026, sutherland -> PRA 2024).
- [ ] R5-R2-M5/M6: after the overnight scaling batch lands, refit
  collapse in log space as primary (A, k + uncertainties) and crossing
  with model-error term + 95% CIs (plateau-then-fall model for d=3).
- [ ] Bib year drift: low2023 -> npj QI 2025, shi2025 -> Nat Commun 2026
  (verify), nam2012 archived PDF is the 2013 companion.

## FINAL STATE (2026-09-01)

All six referee discrepancy passes applied; final verification round complete:
- Referee 1 (physics/open systems): **ACCEPT** after the N=29 crossing
  correction (10.5 -> 9.4 bits, applied) and the "qubit's fastest decay"
  robustness claim scoped (applied; slope sentence updated to
  -0.024+/-0.008 vs -0.008+/-0.009, 1.3 sigma; depol 3.6 sigma).
  17/17 spot-checks passed; no orphaned pre-secular numbers; figures
  consistent with text.
- Referee 3 (numerics/hardware): **FAITHFUL** — all Sec IX numbers
  verbatim, forbidden language gone, crossing_bootstrap deterministic and
  byte-reproducible. Three cosmetic residuals fixed (script docstring,
  HARDWARE.md predicted value, PUBLICATION_PLAN 6/6 annotations).
- Referee 2 (number theory): M2/M3 **sound as applied**; Jankovic tallies
  updated per their finding (4/6 -> 5/6, re-derived bar 5/6 -> all six,
  miss list trimmed, intro echo fixed — the secular flip fixed a Jankovic
  miss too); "exactly" -> "essentially" softening applied.

Remaining for the author:
- Review the working tree (git diff) and commit.
- Optional hardware follow-up: Braket result-object re-fetch or a
  readout-calibration circuit on Garnet $10 to resolve the inversion.
- Optional: regenerate ladder_exponent_sensitivity_d7's exact-DM variant
  if wanted (trajectory variant is current); arXiv tarball via
  paper/make_arxiv.sh when ready.
