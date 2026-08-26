# Hardware-calibrated transmon noise model

> **Status: ⚠️ partially superseded.** The channel construction (§1–3)
> is current and is what the paper uses. Two later results overtake the
> results sections:
> - **§4 uses the confounded N = 15 instance.** Superseded by
>   `GRID_ALIGNMENT.md`.
> - **§6's scaling slopes are retired.** Six qutrit sizes (to 14.3 bits,
>   Hilbert dimension 5.3 × 10⁵) give −0.045 ± 0.003/bit (d = 2),
>   −0.021 ± 0.005/bit (d = 3), −0.040 ± 0.004/bit (d = 5) under the
>   calibrated ladder, and the qutrit family is **plateau-then-fall,
>   not flat**.
>
> For the fitted channel derived from first principles, including the
> Euclidean-embedding construction, see `TEXTBOOK.md` §15–16. For the
> manuscript's current numbers see `PAPER.md`.

Pre-publication hardening task #1. The idealized ladder model used in the
first study assumed textbook scalings; published per-level coherence
measurements say both of its exponents are wrong, in opposite directions
and *both* in the direction of over-penalizing qudits. This documents the
calibrated replacement, its verification, and what it does to the
conclusions.

> ⚠️ **The calibrated channel below is current and used by every result in
> the project. Its *Shor* conclusions are not.** All Shor runs here used
> N = 15, whose only orders are powers of two — a confound discovered
> later (`docs/MECHANISM.md`) and controlled for in
> `docs/GRID_ALIGNMENT.md`. On unbiased instances the qubit Shor advantage
> does not exist at any register size, and d = 3 is the most size-robust
> base rather than the loser. The QPE conclusions here are unaffected.

## 1. What the measurements say

| quantity | idealized model | measured | sources |
|---|---|---|---|
| relaxation ladder Γ₂/Γ₁ | 2.0 (∝ k) | **1.7** (∝ k^0.68) | Goss 2022 + Blok 2020 (9 transmons); Tripathi 2024 (T1 = 53/33.7/24.3 µs for levels 1/2/3) |
| dephasing Γφ 01 : 12 : 02 | 1 : 1 : 4 ((Δlevel)²) | **1 : 2.0 : 2.3** | echo data, T1 contribution subtracted, median of 9 devices |
| decay pathway | sequential | sequential, confirmed to level 4 | Peterer 2015 |

The dephasing shape is the important correction. A (Δlevel)² law says
coherence loss depends only on the *separation* of the two levels; the
data says it depends on the *highest* level involved — because the charge
dispersion of |2⟩ is ≥10× that of |1⟩ (Blok: 12 kHz vs 261 Hz at
E_J/E_C = 73), an independent noise channel rather than a steeper ladder.
Note that 1 : 2.0 : 2.3 is *not* reproducible by any "linear frequency
ladder + independent level-2 channel" decomposition (that forces
Γφ₀₂ ≥ Γφ₁₂ + 3Γφ₀₁ = 5, vs 2.3 measured), so the max-level law is
adopted as the empirical summary.

## 2. The calibrated channel

`transmon_calibrated_superop` in `qudit_shor.py`:

- **Relaxation**: jump operator with |⟨k−1|a|k⟩|² = k^0.7, so level k
  decays at k^0.7·γ.
- **Dephasing**: target matrix Γφ(j,k) = ½·γ·ratio·scale·max(j,k)^1.1,
  realized exactly by diagonal jump operators obtained through classical
  **multidimensional scaling**. (With diagonal jumps, Γφ(j,k) = ½‖v_j −
  v_k‖², so realizing a target matrix *is* a Euclidean embedding problem;
  MDS on D² = 2Γφ returns the coordinates. Any target whose square root
  obeys the triangle inequality is exactly realizable — verified below.)
- **`dephase_scale` / `dephase_ratio` knob**: interpolates to the
  high-E_J/E_C regime of Wang et al. 2024 (12 levels on one transmon,
  T2-echo approaching the T1 limit). Setting it to 0 switches off
  charge-noise dephasing and leaves only the relaxation ladder — the
  "engineered" transmon.

**Normalization**: rates are scaled so the 0↔1 subspace is *identical* to
the idealized model. The d = 2 channel is therefore bit-for-bit unchanged
(verified to 0.0e+00), so every difference between the two models is
purely a higher-level effect. This is what makes the comparison
apples-to-apples.

## 3. Verification (all in `test_qudit_shor.py`)

| check | result |
|---|---|
| max-level law exactly realizable, d = 2…7 | MDS residual ≤ 3×10⁻¹⁷ |
| relaxation ratio Γ₂/Γ₁ | **1.62** (measured 1.7; idealized 2.00) |
| dephasing ratios 01 : 12 : 02 | **1 : 2.14 : 2.14** (measured 1 : 2.0 : 2.3; idealized 1 : 1 : 4) |
| d = 2 unchanged | max deviation 0.0e+00 |
| trace preservation / complete positivity, d = 2,3,5 | trace 1.0000000000, min Choi eigenvalue > −1×10⁻¹⁷ |
| dephase_ratio = 0 leaves ladder intact | Γφ ≡ 0, Γ₄ = 4^0.7 ✓ |

The max-level law cannot distinguish Γφ₁₂ from Γφ₀₂ (both have max = 2),
so it fits their mean, 2.14, against measured 2.0 and 2.3 — a ~7%
approximation. Device-to-device spread in the source data is far larger
(Goss devices reach 6.2), so this is well inside the experimental
scatter; a sensitivity sweep over the exponent belongs in the paper.

## 4. Results — Shor at demo size (N = 15)

Floor-corrected signal, 1 = noiseless, 0 = random guessing:

| strength | d=2 | d=3 idealized → calibrated | d=5 idealized → calibrated |
|---:|---:|---|---|
| 0.002 | 0.922 | 0.839 → **0.854** | 0.737 → **0.805** |
| 0.005 | 0.819 | 0.629 → **0.657** | 0.454 → **0.571** |
| 0.01 | 0.683 | 0.359 → **0.392** | 0.169 → **0.301** |
| 0.02 | 0.516 | 0.037 → **0.058** | −0.069 → **+0.026** |
| 0.05 | 0.374 | −0.269 → −0.253 | −0.145 → −0.109 |

**The headline survives: qubits still win Shor on transmon-like hardware
at every noise strength.** But the penalty was substantially overstated —
the ququint gains up to 78% signal (0.169 → 0.301 at s = 0.01) and stops
falling below the random-guessing floor at realistic noise. The
conclusion is now robust rather than an artifact of model severity, which
is exactly what the re-run was for.

## 5. Results — the high-E_J/E_C ("engineered transmon") regime

With charge-noise dephasing switched off, leaving only the relaxation
ladder — the regime Wang et al. demonstrated at d = 12:

**Shor** — qubits still win, but the margin nearly vanishes at low noise
(0.925 / 0.914 / 0.915 for d = 2/3/5 at s = 0.002; 0.697 / 0.592 / 0.620
at s = 0.01). Note d = 5 overtakes d = 3 here.

**Eigenstate QPE** — the ordering is **decisively reversed**:

| strength | d=2 | d=3 | d=5 |
|---:|---:|---:|---:|
| 0.002 | 0.786 | 0.885 | **0.953** |
| 0.005 | 0.554 | 0.737 | **0.887** |
| 0.01 | 0.322 | 0.543 | **0.785** |
| 0.02 | 0.130 | 0.294 | **0.615** |
| 0.05 | 0.033 | 0.037 | **0.293** |

d = 5 > d = 3 > d = 2 at every strength, by a factor of 2.4× at s = 0.01
and ~9× at s = 0.05. On an engineered transmon running a
chemistry-style phase-estimation workload, ququints are not marginally
better — they are the difference between a usable and an unusable
answer.

## 6. Results — register-size scaling (the decisive test)

44 trajectory runs: 2 algorithms × 2 regimes × 11 register sizes,
strength 0.003/layer, 400 trajectories/point (200 at d = 2, m = 12).
Figure: `results/scaling_calibrated.png`. Because the three bases land on
different precision grids, the table below interpolates the qubit curve
to each qudit's precision and propagates both errors.

**Shor, noise as measured — the qubit advantage erodes to nothing:**

| precision | d = 5 | qubit (interp.) | Δ | significance |
|---:|---:|---:|---:|---|
| 7.0 bits | 0.756 | 0.821 | −0.065 | 1.3σ |
| 9.3 bits | 0.675 | 0.713 | −0.037 | 0.6σ |
| 11.6 bits | 0.583 | 0.593 | **−0.010** | **0.1σ — dead heat** |

Decay slopes per precision bit: d = 2 −0.0494, d = 3 −0.0512,
**d = 5 −0.0376**. The ququint curve is the shallowest, so the qubit
lead shrinks monotonically and is statistically gone by ~11.6 bits. The
qutrit, by contrast, stays 0.07–0.12 behind at every size (1.3–2.7σ) —
a genuine deficit, not an artifact.

**Shor, high-E_J/E_C — parity, trending ququint:** Δ = −0.002 (7 bits),
+0.020 (9.3), +0.039 (11.6), i.e. d = 5 pulls slightly ahead but only at
0.5–0.7σ. Honest reading: **parity with a positive trend**, not a
demonstrated reversal. Slopes: d = 2 −0.0160, d = 5 **−0.0093**.

**Phase estimation — overwhelming qudit win, both regimes:**

*Updated to 1000-trajectory statistics (`results/qpe_hires_1000.json`);
qubit values are linearly interpolated onto each qudit's precision.*

| precision | regime | d = 5 | qubit (interp.) | Δ | significance |
|---:|---|---:|---:|---:|---|
| 7.0 | as measured | 0.803 ± 0.011 | 0.493 ± 0.009 | +0.310 | 21σ |
| 11.6 | as measured | 0.681 ± 0.013 | 0.241 ± 0.012 | **+0.441** | **~25σ** |
| 7.0 | high-E_J/E_C | 0.928 ± 0.007 | 0.618 ± 0.009 | +0.310 | 28σ |
| 11.6 | high-E_J/E_C | 0.878 ± 0.008 | 0.381 ± 0.013 | **+0.497** | **~33σ** |

d = 5 > d = 3 > d = 2 at every size in both regimes, and **the gap widens
with problem size** (slope ratio ~4.9× in the engineered regime: −0.011
for d = 5 vs −0.054 for d = 2). At 11.6 bits the ququint retains 2.83×
the signal of the qubit register as measured, and 2.30× when charge
noise is engineered away — while the qubit curve is heading for the
noise floor.

## 7. What this changes in the paper

1. **The "qubits win Shor on transmons" claim must be narrowed.** It
   holds at small scale under measured noise, but the advantage decays
   with problem size and is statistically gone (0.1σ) by ~11.6 bits of
   precision for ququints. The idealized model's picture — qubits
   dominating at every size — was an artifact of its over-severe
   exponents. Correct statement: *the qubit advantage in Shor is real
   but confined to small registers, and it does not survive scaling.*
2. **The qutrit is the genuine loser in Shor**, consistently 0.07–0.12
   behind at every size in both regimes. Worth stating explicitly: the
   qudit story is not monotonic in d, and d = 3 is the worst of the
   three bases for this algorithm.
3. **Phase estimation is an unambiguous qudit win at 12–17σ**, growing
   with problem size, in both noise regimes. Since eigenstate QPE is
   the quantum-chemistry workhorse, this is the result with the
   clearest practical consequence.
4. **The dephasing half of the ladder is a design parameter** (E_J/E_C),
   and it is the half that punishes qudits most. The transmon platform
   is therefore engineering itself toward the qudit-favorable regime —
   a trajectory claim, testable today on high-E_J/E_C devices, that
   replaces the static "which platform suits qudits" framing.
5. All quantitative statements in the draft must be restated from the
   calibrated numbers; the idealized model stays in the paper only as a
   documented contrast showing how much modelling choices matter.
