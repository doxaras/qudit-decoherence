# Gate-cost sensitivity: the strongest objection, tested

Pre-publication hardening task #2. Our default cost model charges every
gate one time-layer regardless of dimension — the assumption most
favourable to qudits, and the obvious reviewer attack, because real
hardware charges more per entangling gate as d grows. This tests three
published cost structures and finds that **the qudit advantage is
conditional on the entangling-gate cost growing no faster than linearly
in d**, and that it exists for phase estimation but not for Shor.

> ⚠️ **The cost models and the linear-in-d condition below are current.
> The "but not for Shor" clause is retracted.** The Shor half of this
> study used N = 15, whose only orders are powers of two — a confound
> discovered later (`docs/MECHANISM.md`). Re-run on an unbiased instance
> (`cost_fair.py`, `docs/GRID_ALIGNMENT.md` §5), Shor obeys exactly the
> same condition as phase estimation. The two algorithms are governed by
> one rule, which makes this document's central finding stronger, not
> weaker.

## 1. The three cost models

| model | multiplier | source | physical situation |
|---|---|---|---|
| `uniform` | 1 | our original assumption | a **native** fully-entangling qudit gate whose count does not grow with d — e.g. Goss 2022's cross-Kerr CZ, one gate spanning the full 9-dimensional two-qutrit space |
| `ion` | d−1 on entangling gates | Ringbauer 2022: Cinc costs 2(d−1) Mølmer–Sørensen gates (normalized to 1 at d = 2) | current trapped-ion qudit hardware |
| `pavlidis` | d²/4 on all gates | Pavlidis & Floratos 2017: qudit QFT-domain arithmetic has depth 8d²q | **no** native qudit entangler — everything decomposed into two-level rotations |

Total Shor circuit cost (time-layers, N = 15) — this is the whole story
in one table:

| cost model | d = 2 | d = 3 | d = 5 | |
|---|---:|---:|---:|---|
| `uniform` | 51.0 | 26.0 | 15.0 | qudits 3.4× cheaper |
| `ion` | 51.0 | 44.0 | 42.0 | advantage nearly gone |
| `pavlidis` | 51.0 | 58.5 | 93.8 | **advantage reversed** |

The width-and-depth compression that drives every qudit win in this
project is exactly what the costlier models eat.

## 2. Results

Floor-corrected signal, exact density-matrix simulation, demo size,
strength 0.005/layer. Entries are **signal(d=5) − signal(d=2)**;
positive means ququints win. Full grid in
`results/cost_sensitivity.json`, figure `results/cost_sensitivity.png`.

| | | `uniform` | `ion` | `pavlidis` |
|---|---|---:|---:|---:|
| **Shor** | ions / per-particle | −0.02 | −0.30 | −0.61 |
| | transmon / calibrated | −0.25 | −0.65 | −0.90 |
| **QPE** | ions / per-particle | **+0.42** | **+0.20** | −0.09 |
| | transmon / calibrated | **+0.30** | +0.00 | −0.27 |

Three conclusions, in decreasing order of comfort:

1. **Shor never wins for qudits under any cost model.** The earlier
   "erodes to a dead heat at scale" result was measured under `uniform`,
   the most generous assumption; charging realistic gate costs removes
   it. Shor is simply not the algorithm for qudits.
2. **QPE's qudit advantage survives linear-in-d gate costs but not
   quadratic.** It is large under `uniform` (+0.42 / +0.30), survives
   `ion` on per-particle hardware (+0.20), reaches exact parity on
   transmon noise (+0.00), and inverts under `pavlidis`.
3. **The crossover condition is sharp and physically meaningful**: qudits
   win iff entangling cost grows no faster than ~linearly in d. That is
   a concrete hardware requirement, not a modelling artifact.

## 3. The physically matched pairings

Cost model and noise model are not independent — each describes a
platform, and only some combinations describe a *real* machine:

| platform | cost model | noise model | QPE result |
|---|---|---|---|
| Trapped-ion qudits (Ringbauer-class) | `ion` (measured: 2(d−1) MS gates) | per-particle depolarizing | **+0.20 ququint win** |
| Transmon with native cross-Kerr CZ (Goss-class) | `uniform` (one native gate) | calibrated ladder | **+0.30 ququint win** |
| Any platform lacking a native qudit entangler | `pavlidis` | either | qubits win |

Both physically matched pairings favour ququints for phase estimation.
The pessimistic cells of the grid are mostly *mismatched* combinations
(ion gate costs charged against transmon noise, or d² decomposition costs
charged to hardware that has native qudit gates). This must be stated
carefully in the paper — presenting only the matched cells would be
cherry-picking, so the full grid goes in, with the pairing argument
made explicitly and the `pavlidis` row given as the genuine failure
mode.

## 4. What this changes in the paper

1. **Drop any claim that qudits help Shor.** Under honest gate costs
   they do not, on any platform, at any noise strength tested. The Shor
   result becomes a *negative* result — valuable, because it isolates
   *why* (the control–work entanglement mechanism) and because Shor is
   the algorithm everyone assumes first.
2. **Restate the QPE claim conditionally**: ququints beat qubits at
   eigenstate phase estimation *provided the entangling-gate cost grows
   no faster than linearly in d* — satisfied by both current ion
   hardware and native-cross-Kerr transmons, violated by
   decomposition-based compilation.
3. **New headline candidate**: the paper's most useful output is the
   *condition*, not a verdict. "Qudits help phase-critical algorithms iff
   your two-qudit gate is native" is an actionable engineering target,
   and it explains the field's existing split results (Gokhale's qutrit
   wins used native ancilla levels; Gustafson's 2025 finding that qutrit
   synthesis costs 35–69% *more* non-Clifford gates is the `pavlidis`
   regime).
4. The `uniform` results stay in the paper as the "native-gate limit"
   upper bound, explicitly labelled as such — never as the default.

## 5. Caveats on the cost models themselves

- The `pavlidis` d² factor is derived for their specific QFT-domain
  arithmetic decomposition; applying it to *all* gates (including
  single-qudit) is deliberately the harshest reading.
- `ion` normalizes Ringbauer's 2(d−1) to (d−1) so that d = 2 costs one
  layer. This makes d = 2 identical across all three models — the same
  apples-to-apples device used for the noise calibration.
- Neither `ion` nor `pavlidis` accounts for the *fidelity* differences
  between subspace and full-space entanglers (Goss: depth 6 vs 9 for a
  Haar-random two-qutrit unitary), which would partly offset the ion
  penalty.
- Gate cost and gate *error* are treated as proportional here (more
  layers = more idle decoherence). A model where longer gates have
  better fidelity per operation would soften the penalty.

## 6. The d = 7 demo point (`d7_demo.py`)

Demo-size run on the unbiased instance (N = 21, a = 2, r = 6; base 7 is
never grid-aligned and has mean residual misalignment 0.300, identical
to bases 3 and 5), 1000 trajectories/point, all four bases × both
channels × all three cost models (`results/d7_demo.json`). Findings:

- **Native-gate direction survives at d = 7**: `uniform` signal 0.53 vs
  qubit 0.27 (calibrated ladder, s = 0.005) and 0.80 vs 0.31
  (depolarizing) — despite the Janković d = 7 bar of 5.70 not being
  cleared (layer ratio 57/15 = 3.80). Second conservative miss of the
  gate-level criterion (with d = 3 `ion`), same direction.
- **No longer monotone in d on the ladder**: uniform-cost ordering is
  0.27 / 0.62 / 0.65 / 0.53 for d = 2/3/5/7 — the optimum sits at
  d = 5. Under depolarizing d = 7 still leads (0.80).
- **`ion` cost fails at d = 7 on the ladder** (0.07 vs 0.30) and keeps
  only +0.07 under depolarizing; `pavlidis` is at/below the floor
  (−0.05 to +0.04). The native-vs-decomposed window narrows with every
  added level.
- Trajectory replication check: the d = 2/3/5 cells reproduce the
  exact-DM Table `tab:cost` signals within ~0.03.
