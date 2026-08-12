# The mechanism: a falsified hypothesis and a confound

Pre-publication hardening task #4. This was meant to be the paper's
mechanism section — a clean demonstration that control–work entanglement
explains why Shor and phase estimation order oppositely. **The experiment
falsified that hypothesis, and following the failure led to a confound
that overturns the Shor result entirely.** Both are recorded here because
both change what the paper can claim.

> **Follow-up:** this document is the discovery narrative. The work it
> forced — grid alignment measured across one instance per alignment class,
> a within-modulus control isolating it from register width, and every Shor
> study re-run on unbiased instances — is in **`docs/GRID_ALIGNMENT.md`**.
> Every conclusion below survived that re-run and strengthened.

## 1. The hypothesis

Shor entangles the control register with a work register holding
|aᶜ mod N⟩; eigenstate QPE leaves them in a product state. The proposal:
in Shor the work register carries *which-path information* about the
control, so noise on the work register dephases the control even when the
control is untouched — and since qudits pack that work register onto
fewer, higher, noisier levels, they suffer more. Eigenstate QPE has no
such channel, so qudits win there.

Plausible, and it explained the observed sign flip. It is also wrong.

## 2. The test

Shor's work register starts in |x = 1⟩, which is an equal superposition of
the **r eigenstates** of the modular multiplier. Shor *is* phase
estimation on an r-fold eigenstate superposition. So running QPE on a
K-fold superposition sweeps continuously from eigenstate QPE (K = 1) to
the Shor regime (K = 4 = r), with circuit, metric, noise and cost all
held fixed. Verified: control–work entanglement entropy comes out at
exactly log₂K — 0.000, 1.000, 1.585, 2.000 bits — in all three bases.

If the hypothesis is right, the ququint advantage should collapse as K
grows and reach Shor's value at K = 4.

## 3. The result: falsified

Ququint advantage (signal d=5 − signal d=2), 1000 trajectories/point,
strength 0.005:

| entanglement | transmon/uniform | transmon/ion | ions/uniform | ions/ion |
|---|---:|---:|---:|---:|
| 0.00 bits (K=1) | +0.324 | −0.007 | +0.423 | +0.194 |
| 1.00 bits (K=2) | +0.321 | −0.030 | +0.383 | +0.164 |
| 1.58 bits (K=3) | +0.257 | −0.052 | +0.393 | +0.130 |
| 2.00 bits (K=4) | +0.281 | −0.041 | +0.369 | +0.158 |
| slope per bit | −0.029 | −0.020 | −0.024 | −0.024 |

Entanglement does hurt qudits — the slope is negative in all four
conditions, consistently ≈ −0.025 per bit, which is 2–3σ over the full
range. But the effect is **an order of magnitude too small**. At K = 4 the
ququint still leads by +0.281 under transmon/uniform, whereas *actual
Shor* under identical noise and cost gives **−0.248**. Entanglement
accounts for roughly 10% of a 0.53 gap.

So control–work entanglement is a real but minor effect, and it is not
why Shor and QPE differ.

## 4. Following the failure: the grid-alignment confound

If not entanglement, what? The remaining differences between our Shor and
QPE setups are the metric and the target phases. The phases turn out to be
decisive.

Phase estimation concentrates probability on the phases s/r. **If r
divides the control dimension D = dᵐ, those phases sit exactly on grid
points and the interference peaks are perfectly sharp**; otherwise they
smear across neighbouring outcomes and are far more fragile under noise.

For N = 15 the multiplicative group is ℤ₂ × ℤ₄, so **every** order is a
power of two (r ∈ {1, 2, 4}). With D = 2ᵐ, qubits *always* land on exact
grid points; qutrits and ququints *never* do. Our Shor comparison handed
base 2 a structural advantage that has nothing to do with decoherence —
and we chose the golden-ratio conjugate for QPE precisely to avoid this,
which is why the two experiments disagreed.

**Test** (exact density matrix, floor-corrected signal):

| instance | r | exact grid for | d = 2 | d = 3 | d = 5 | winner |
|---|---:|---|---:|---:|---:|---|
| N=15, a=7 | 4 | **d = 2** (D=64) | **0.819** | 0.657 | 0.571 | d = 2 |
| N=21, a=4 | 3 | **d = 3** (D=81) | −0.067 | **1.020** | 0.404 | d = 3 |
| N=21, a=2 | 6 | *none* | 0.282 | 0.578 | **0.631** | d = 5 |

(transmon-calibrated noise, strength 0.005; the depolarizing rows show the
same pattern.)

**The winner tracks which base can represent s/r exactly, not the noise
physics.** At r = 3 the qutrit is essentially immune to noise at this
strength while the qubit collapses to *below* the random floor. And in the
only unbiased instance — r = 6, representable in no base — **qudits win
Shor**, reversing the result this project has reported until now.

## 5. What this changes

1. **The "qudits lose Shor" result is retracted.** It was an artifact of
   N = 15, whose group structure admits only power-of-two orders. On the
   unbiased r = 6 instance (N = 21, a = 2), charged under all three gate
   cost models at strength 0.005:

   | noise | cost | d = 2 | d = 3 | d = 5 |
   |---|---|---:|---:|---:|
   | transmon (calibrated) | `uniform` | 0.282 | 0.578 | **0.631** |
   | | `ion` | 0.282 | **0.374** | 0.256 |
   | | `pavlidis` | **0.282** | 0.255 | 0.039 |
   | ions (per-particle) | `uniform` | 0.331 | 0.667 | **0.782** |
   | | `ion` | 0.331 | 0.497 | **0.502** |
   | | `pavlidis` | **0.331** | 0.394 | 0.215 |

   **Shor now behaves exactly like phase estimation**: qudits win with
   native gates, survive linear-in-d gate costs on per-particle hardware,
   and lose only under quadratic decomposition costs. The two algorithms
   were never governed by different rules — the apparent difference was
   the arithmetic confound.
2. **The entanglement mechanism is demoted** from headline explanation to
   a measured secondary effect (≈ −0.025 signal per bit of control–work
   entanglement). It should still be reported — it is a real, novel,
   quantified effect — but not as the cause of the Shor/QPE difference.
3. **Grid alignment becomes a first-class experimental variable.** Any
   cross-dimension algorithm comparison must either randomize it (as our
   QPE does, via an irrational target phase) or report it explicitly.
   This is a methodological result in its own right, and to our knowledge
   the qudit-algorithms literature does not discuss it — Bocharov 2016
   and the qudit-QPE papers all work at fixed d, where it is invisible.
4. **The QPE results are unaffected**, because the golden-ratio conjugate
   target phase was chosen from the start to be far from any small-
   denominator fraction in every base. That precaution is now the
   experiment's most important design feature and must be foregrounded in
   Methods rather than buried.

## 6. Metric caveat

At r = 3 the d = 3 floor-corrected signal slightly exceeds 1 (1.02). This
is real, not numerical: when r | D the noiseless distribution sits exactly
on r peaks with weight 1/r each, and the y = 0 peak yields no order, so
the noiseless baseline is capped near (r−1)/r. Mild noise spreads a little
of that useless y = 0 weight into outcomes that continued fractions *does*
accept, pushing success slightly above the noiseless value. Worth stating
in the paper; it does not affect any ordering.
