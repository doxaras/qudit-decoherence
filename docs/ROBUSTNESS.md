# Robustness: independent validation, readout error, and echo

> **Status: ⚠️ incomplete.** Everything in this file is current, but the
> paper's robustness section (Sec. VIII) has since grown three more
> controls that are **not** documented here:
> - **Noise-inflation threshold** (`noise_inflation.py`) — the qudit
>   advantage survives a qudit-to-qubit per-gate noise ratio up to
>   f* = 1.2–4.5 depending on the cost/channel pairing.
> - **Zeeman-structured dephasing** (`collective_zeeman.py`,
>   `ion_zeeman_*.py`) — the sharpest failure mode found: it **reverses
>   the verdict outright**, and the qudit ordering returns only at
>   ε* = 0.58–0.79 under native-gate cost, 0.09–0.15 under MS cost.
> - **Composite dimension** (`d4_control.py`, `composite_control.py`) —
>   d = 4 and d = 6 both land inside the qudit band; the bare dynamics
>   carries no trace of primality.
>
> All three are written up in `TEXTBOOK.md` §17, §19.3 and §21.4.

Pre-publication hardening tasks **#1b**, **#5** and **#6**. Three separate
attacks on the result, grouped because each asks the same question: does
the qudit advantage survive something we had not charged for?

Summary: yes to all three, and the echo result is the most useful thing in
this document — it says *where* qudits should be benchmarked.

## 1. Cross-validation against an independent analytic result (#1b)

Everything else in this repo is our machinery checked against itself
(CPTP, exact-vs-trajectory agreement, dense-QFT comparison). This checks it
against a result derived by other people with entirely different methods:
Janković et al. 2023 (arXiv:2302.04543) compute the first-order response of
the *average gate infidelity* to Lindblad noise using linear response and
Weingarten calculus over the Haar measure, for one qudit of dimension d
versus n = log₂d qubits spanning the same Hilbert space, under pure
dephasing (L = J_z).

`jankovic_check.py` reproduces their three central equations from our own
superoperator code — the same `_dissipator` and matrix-exponential path the
main study uses — with no analytics of our own.

| quantity | their result | our simulation | worst rel. error |
|---|---|---|---|
| qudit process infidelity (Eq. 30) | (γt/12)(d²−1) | reproduced, d = 2…64 | 4.1 × 10⁻⁴ |
| n-qubit process infidelity (Eq. 31) | (γt/4)·n | reproduced, n = 1…6 | 8.8 × 10⁻⁷ |
| **critical curve** (Eq. 22) | **(d²−1)/(3 log₂ d)** | reproduced, d = 2…64 | 4.1 × 10⁻⁴ |

The residual is not numerical error — it is the O((γt)²) term their
first-order expansion drops. It tracks the infidelity itself (at d = 64 the
process infidelity is 3.4 × 10⁻⁴ and the relative deviation is 4.1 × 10⁻⁴),
which is exactly the signature expected if our simulation is right and
their expansion is truncated. Two supporting checks: the tensor-product
multiplicativity of entanglement fidelity used for the n-qubit case is
verified directly against explicitly constructed 2- and 3-qubit channels
(agreement to 10⁻⁹), and their L = J_z differs from our number operator n̂
by a multiple of the identity, under which the Lindblad dissipator is
exactly invariant — so this exercises the identical code path as
`transmon_superop`, not a special case written for the test.

### 1.1 Their criterion, applied to our circuits

Their curve is also usable as an independent prediction. It says a
d-dimensional carrier must beat the multiqubit gate-time-per-decoherence-
time by (d²−1)/(3 log₂ d) to break even. Two things follow.

**The bar is much lower than folklore at small d.** The often-quoted
O(d²/log₂d) gives 5.68 at d = 3 and 10.77 at d = 5; the exact curve gives
**1.68 and 3.45**. Prime-dimensional qudits need to be only ~1.7× (qutrit)
or ~3.4× (ququint) more time-efficient than a qubit register, not 6–11×.
This is the strongest external support for our thesis that we have found,
and it belongs in the introduction.

**It predicts our own results.** Our circuits buy efficiency by using fewer
layers rather than faster ones, so we read the layer-count ratio as the
gate-efficiency ratio and ask whether it clears the curve. Because their
(d²−1) comes from J_z dephasing — the physics of our ladder channel, not of
our per-particle depolarizing channel — the criterion should apply to the
transmon results only, and that is where we test it:

| cost model | d | layers ratio | critical curve | predicted | observed | |
|---|---:|---:|---:|---|---|---|
| uniform | 3 | 2.19 | 1.68 | qutrit | qutrit | ✓ |
| uniform | 5 | 3.80 | 3.45 | ququint | ququint | ✓ |
| ion | 3 | 1.30 | 1.68 | qubit | *qutrit* | ✗ |
| ion | 5 | 1.36 | 3.45 | qubit | qubit | ✓ |
| pavlidis | 3 | 0.97 | 1.68 | qubit | qubit | ✓ |
| pavlidis | 5 | 0.61 | 3.45 | qubit | qubit | ✓ |

**5 of 6**, including the genuinely tight case (d = 5 under uniform cost
clears the curve by only 3.80 vs 3.45, and wins). An analytic gate-level
criterion derived for a single Haar-averaged gate has no obligation to
predict the success probability of a 57-layer algorithm, so the level of
agreement is a meaningful check on both.

The one miss is instructive rather than embarrassing: at `ion` cost the
qutrit wins where the criterion says it should lose. Our ladder channel is
not their pure-dephasing channel — it also carries amplitude damping with
Γ_k ∝ k^0.7, which is *gentler* than the J_z dephasing that produces the
(d²−1). The criterion is therefore conservative for us, and the direction
of the miss is the direction that conservatism predicts.

## 2. d-dependent readout error (#6)

Every result until now assumed noiseless state preparation and
measurement — a real gift to qudits, since a d-level readout must resolve d
pointer states and the higher ones are the hardest (crowded dispersive
shifts, more decay during the measurement window).

`spam_study.py` charges one readout channel at the end of the circuit on
every control qudit, with the misread rate of |k⟩ growing as (1+k) — about
1 : 2 : 3 for a qutrit, matching reported transmon qutrit readout errors
(~1% / 2% / 4%). The qubit's own readout is charged too. Floors and
baselines are recomputed at each ε so the metric never credits a base for
damage it already removed.

Floor-corrected signal, unbiased instance, noise strength as in §5 of
`docs/GRID_ALIGNMENT.md`:

| ε | Shor, ladder | Shor, per-particle | QPE, ladder | QPE, per-particle |
|---|---|---|---|---|
| 0 | +0.253 | +0.452 | +0.232 | +0.424 |
| 0.01 | +0.259 | +0.456 | +0.231 | +0.422 |
| 0.02 | +0.266 | +0.461 | +0.230 | +0.421 |
| 0.04 | +0.281 | +0.474 | +0.227 | +0.417 |

(entries are the ququint's lead over the qubit, d = 5 signal − d = 2 signal)

**The advantage is untouched — it drifts by less than ±0.03 over a 4×
range of readout error**, and in Shor it very slightly *widens*.

The reason is a structural cancellation worth reporting on its own. Total
readout exposure is (number of control carriers) × (mean per-level misread
rate) = m × ε(d+1)/2. At matched precision m ≈ log D / log d, so at D ≈ 64
this is 6 × 1.5ε = 9ε for qubits, 4 × 2ε = 8ε for qutrits, 3 × 3ε = 9ε for
ququints. **The growth of per-level readout error with d is almost exactly
cancelled by the reduction in carrier count.** d-dependent SPAM is close to
neutral between bases by construction, not by luck.

Caveat: the QPE rows drift very slightly *upward* with ε. That is the
floor-corrected metric, not physics — the noiseless baseline degrades a
little faster than the noisy run, nudging the ratio up. Absolute success
falls monotonically in every case, which the test suite pins.

## 3. Dynamical decoupling (#5)

No real transmon runs a long circuit without refocusing, so the honest
question is not whether DD helps — it always does — but **whether it helps
qubits or qudits more**. `dd_study.py` sweeps `dephase_scale` from 1 (free
evolution) to 0 (perfect echo, the T1 limit), which is the same knob that
defines the `transmon_cal_lowcharge` regime — there reached by device
engineering (high E_J/E_C, Wang et al. 2024), here by pulses. DD is not
free, so we bracket its pulse cost with the two cost models already in the
repo rather than inventing a new one.

Ququint lead over the qubit (d = 5 signal − d = 2 signal):

| dephasing left | Shor, uniform | Shor, ion | QPE, uniform | QPE, ion |
|---|---:|---:|---:|---:|
| 1.00 (no DD) | +0.349 | **−0.026** | +0.297 | **+0.000** |
| 0.75 | +0.366 | +0.006 | +0.306 | +0.032 |
| 0.50 | +0.384 | +0.050 | +0.315 | +0.074 |
| 0.25 | +0.402 | +0.110 | +0.324 | +0.127 |
| 0.00 (perfect echo) | +0.423 | **+0.191** | +0.332 | **+0.196** |

**Echo helps qudits more than qubits, monotonically, in all four
conditions.** The mechanism is direct: DD suppresses dephasing, which is
the part of the ladder channel that scales worst with dimension (the
max-level law, ~2.15× at level 2), and leaves relaxation, which scales
only as k^0.7. Refocusing therefore removes the qudit's largest structural
penalty and leaves its width-and-depth advantage intact.

The consequential entry is the `ion` column. Under linear-in-d gate cost —
the realistic charge for a Mølmer–Sørensen-style native gate — the ququint
*loses* Shor without echo (−0.026) and *wins* with it (+0.191); QPE moves
from an exact dead heat to +0.196. **Dynamical decoupling moves the
break-even point of the paper's central condition.** The condition should
therefore be stated as: qudits win iff the entangling gate is native *at
the device's operating dephasing level*, and refocused operation buys
roughly one cost-model's worth of headroom.

This also strengthens direction (C) in `docs/PUBLICATION_PLAN.md`: since DD
gain grows with d while DD pulse count grows as 2(d−1), there is a
crossover dimension where refocusing stops paying. Our numbers bracket it
but do not locate it; doing so needs a per-pulse error model rather than
the two-cost-model bracket used here.

## 4. What these change for the paper

1. **The methods section gains an external anchor.** We reproduce a
   published analytic critical curve to 4 × 10⁻⁴ with the residual
   identified as their truncation, not our error.
2. **The introduction gains its best supporting citation.** The exact
   break-even ratio at the dimensions we study is 1.68 (d = 3) and 3.45
   (d = 5), not the 5.68 and 10.77 of the O(d²/log₂d) folklore — an
   independent derivation that the bar for prime-dimensional qudits is
   low.
3. **Two reviewer objections are pre-empted with data**: SPAM is charged
   and is structurally near-neutral; refocused operation is charged and
   *favours* qudits.
4. **A hardware recommendation follows**: benchmark qudit algorithms on
   refocused devices. It is the regime where the advantage is largest, it
   is how any real device runs, and it is what decides the ion-cost case.
