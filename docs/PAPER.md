# The paper: current state, section map, and changelog

Single source of truth for **what the manuscript currently says** and
**which document in `docs/` still matches it.** The other `docs/` files
are lab notebooks written in the order the work happened; several
predate results that superseded them. This file records those
supersessions in one place so no one has to diff a notebook against the
manuscript.

- **Manuscript:** `paper/main.tex` → `paper/main.pdf`
- **Build:** `cd paper && latexmk -pdf main.tex`
- **arXiv package:** `paper/make_arxiv.sh` → `paper/arxiv-submission.tar.gz`
- **Submission walkthrough:** `docs/ARXIV_SUBMISSION.md`
- **Derivations from first principles:** `docs/TEXTBOOK.md`
- **Public repo:** https://github.com/doxaras/qudit-decoherence
- **Archive:** [10.5281/zenodo.21901533](https://doi.org/10.5281/zenodo.21901533) (concept DOI, resolves to current) · v1.0 = [10.5281/zenodo.21901534](https://doi.org/10.5281/zenodo.21901534)

---

## 1. Current metadata

| field | value |
|---|---|
| **Title** | *Native gates or nothing: the condition for a qudit advantage in uncorrected quantum algorithms under decoherence* |
| Author | John Doxaras · AI Employee, Athens, Greece · john@ai-employee.cloud |
| Class | `revtex4-2`, `[aps,prx,reprint,superscriptaddress,nofootinbib,floatfix]` |
| Extent | 19 pages · 6 figures · 7 tables · 48 references |
| Status | content-complete; builds clean; arXiv package built |

### The claim, in the form the paper states it

> Qudits outperform qubits in **bare, uncorrected** circuits **only**
> with a native two-qudit entangling gate whose cost grows no faster
> than linearly in *d*. Whether linear cost *suffices* is set by the
> level and structure of the operating dephasing. Break-even is the
> qudit's layer-count ratio clearing (d²−1)/(3 log₂ d).

Two scope fences the paper draws explicitly, and both matter when
quoting it:

1. It is a statement about **uncorrected** circuits. It does **not**
   transfer to the error-correction layer, where the dimension
   dependence can carry the opposite sign (Keppens *et al.*).
2. The one exception to the decomposition verdict is **Shor at d = 3
   under per-particle noise** — width compression alone surviving the
   depth surcharge.

---

## 2. Section → document → script map

| § | paper section | background doc | primary scripts |
|---|---|---|---|
| I | Introduction | `SOTA.md`, `PUBLICATION_PLAN.md` | — |
| II | Setup (algorithms, channels, cost models, metric) | `TEXTBOOK.md` §3–9, §13–20; `CALIBRATION.md`, `TRANSMON.md` | `qudit_shor.py`, `qpe_generic.py`, `grover.py`, `trajectories.py` |
| III | Grid alignment | `GRID_ALIGNMENT.md`, `MECHANISM.md`; `TEXTBOOK.md` §10 | `grid_alignment.py`, `same_n_control.py`, `ensemble_a{,_traj}.py`, `misalignment_scaling.py`, `fair_demo.py` |
| IV | The cost condition | `COST_SENSITIVITY.md`; `TEXTBOOK.md` §3, §19 | `cost_fair.py`, `d7_demo.py`, `matched_D.py`, `jankovic_check.py` |
| V | Scaling with problem size | `GRID_ALIGNMENT.md` §6; `TEXTBOOK.md` §21.3 | `scaling_fair.py`, `scaling_fair_m8.py`, `scaling_fair_n29.py`, `scaling_fair_point.py` |
| VI | Grover | `GROVER.md`; `TEXTBOOK.md` §9 | `grover_study.py`, `grover_cost.py` |
| VII | Mechanism: damage units and the decoder | `GROVER.md` §5, `MECHANISM.md`; `TEXTBOOK.md` §14, §11–12 | `exposure_collapse.py`, `fidelity_collapse.py`, `logfid_rescore.py`, `decoder_formula.py`, `decoder_scaling.py`, `interpolation_experiment.py` |
| VIII | Robustness | `ROBUSTNESS.md`; `TEXTBOOK.md` §17, §19.3, §20.4 | `spam_study.py`, `dd_study.py`, `noise_inflation.py`, `collective_zeeman.py`, `ion_zeeman_{demo,echo}.py`, `d4_control.py`, `composite_control.py` |
| IX | Hardware anchor | `HARDWARE.md`; `TEXTBOOK.md` §21.5 | `braket_qpe_anchor.py`, `braket_raw_analysis.py` |
| X | Discussion (incl. proposed experiment) | `EXPERIMENTS.md`; `TEXTBOOK.md` §21.6 | `ion_qpe_prediction.py` |
| XI | Methods | `GLOSSARY.md` §3–4 | `test_qudit_shor.py` |
| App. A | Decoder acceptance lemma | `TEXTBOOK.md` §11 | `decoder_formula.py` |

### Figures and tables

| object | source |
|---|---|
| Fig. 1 pipeline | inline TikZ in `main.tex` |
| Fig. 2 `grid_alignment.png` | `plots_grid.py` |
| Fig. 3 `fair_demo.png` | `plots_fair.py` |
| Fig. 4 `scaling_fair.png` | `plots_scaling_fair.py` |
| Fig. 5 `grover.png` | `plots_grover.py` |
| Fig. 6 `mechanism.png` | `plots_mechanism.py` |
| Tab. I ensembles · II cost · III collapse · IV decoder · V Zeeman · VI hardware · VII predictions | see § map above |

---

## 3. Changelog — what changed, and what it superseded

Newest first. Each entry names the documents it invalidated.

### Aug 13, 2026 — Floratos–Pavlidis 2024 read in full, cited three more times
*(uncommitted in the working tree at the time of writing)*

A full read of the 28-page follow-up found three contributions beyond
the depth-scaling claim, now worked into the manuscript:

- **Intro** — odd-prime dimension is not only a fault-tolerance
  requirement: the in-place multipliers, quadratic-phase operators and
  fractional Fourier transforms of that work are built on the odd-prime
  case, where the discrete rotation group is cyclic and every nonzero
  multiplier is invertible.
- **Sec. VIII (composite dimension)** — the prime restriction is
  therefore inherited from the fault-tolerance **and QFT-arithmetic**
  motivations, not one of them.
- **Limitations** — the compiled-arithmetic penalty is confined to
  **depth**. The construction is in-place and ancilla-free (width
  exactly *n*, nearest-neighbour only), so compiled arithmetic inflates
  the *layers* term of the carriers × layers exposure budget but not the
  carrier count, and maps onto a linear ion chain without routing
  overhead.

→ `TEXTBOOK.md` §2 (Consequence 4), §2.1 and §22 updated to match;
`THEORY.md` banner updated.

### Aug 13, 2026 — Floratos–Pavlidis 2024 cited
`floratos2024` (arXiv:2409.05759, *Finite fractional Fourier transform
on qudits*) added to `refs.bib` and cited in the gate-cost subsection.
It reports the same **d² scaling in depth** — not merely in gate count —
for a full QFT-based in-place modular multiplier under 1D-local
connectivity. This is what licenses treating `pavlidis` as a uniform
layer multiplier rather than a gate-count multiplier.
*Note:* the entry needs a `journal` field or the build fails.
→ `papers/INDEX.md` updated (51 PDFs).

### Aug 12, 2026 — sixth qutrit size; the flatness claim retired
`scaling_fair_d3_m9` (d = 3, m = 9 → 14.3 bits, dim ℋ = 5.3 × 10⁵)
plus a d = 2, m = 12 rerun at 1000 trajectories.

**Superseded:** the "qutrit's Shor signal is independent of problem
size" claim. The qutrit family is **plateau-then-fall**, not flat:
calibrated-ladder slope **−0.021 ± 0.005/bit** (R² = 0.80, n = 6), with
the first three sizes agreeing to χ²/dof = 0.01 and the 14.3-bit point
sitting **4.1σ** below the 9.5-bit one. Qubit **−0.045 ± 0.003/bit**
(n = 4); ququint **−0.040 ± 0.004/bit** (n = 3).
→ invalidates `GRID_ALIGNMENT.md` §6's "−0.000/bit" table **and** the
Aug-12 correction block already inside it (which quoted the m = 8 figure
−0.018 ± 0.008). → invalidates `CALIBRATION.md` §6 and `GLOSSARY.md`
§5.3 slopes. All three now carry status banners.

**Honest-reporting note preserved in the paper:** five sizes would have
read as a flat depolarizing family; the sixth resolves the shape.

### Aug 12, 2026 — abstract and intro rebalanced toward the decoder law
The fidelity collapse was downgraded to what it is — the **null
expectation** for first-order composition of incoherent channels — and
the decoder acceptance law promoted to the paper's quantitative
contribution. `logfid_rescore.py` added: rescored in log fidelity the
same fit gives R² = 0.76 (0.85–0.91 if refit there), against 0.97–0.99
in linear fidelity.

### Aug 12, 2026 — raw Braket histograms committed
`results/braket_raw_counts.json` + `braket_raw_analysis.py` make every
hardware number in Sec. IX reproducible from shot data.
**Superseded:** the m = 7 reinterpretation-search maximum is **0.15**
over 10,080 relabelings, not 0.21. → `HARDWARE.md` corrected.

### Aug 12, 2026 — Zeeman-structured dephasing
`collective_zeeman.py`, `ion_zeeman_demo.py`, `ion_zeeman_echo.py`. The
sharpest failure mode in the paper: keeping the ⁴⁰Ca⁺ encoding's full
pair anisotropy (1–25× at d = 3, 1–49× at d = 5) **reverses the verdict
outright** — qubit wins at every strength under both cost models, and
common-mode dephasing preserves the reversal. Echo sweep prices it:
qudit ordering returns at ε* = 0.58–0.79 (`uniform`) but only
0.09–0.15 (`ion`), i.e. ≳ 400–600 vs ≳ 2200–3800 layer times of
0↔1 coherence.
→ new material; no prior doc covers it. See `TEXTBOOK.md` §17.

### Aug 12, 2026 — multiplicative-group ensembles at N = 33 and N = 55
`ensemble_a_traj.py` generalized to any modulus. Scores every unit
a ≠ 1: 11 (N = 21), 19 (N = 33), 39 (N = 55). Alignment theory predicts
the ensemble **class by class**; the ququint's aligned-over-unaligned
excess (+0.18 to +0.19) independently reproduces the ≈ 0.2 price from
the within-modulus control. Every base-2-aligned class is unscorable at
all three moduli.
→ extends `GRID_ALIGNMENT.md` §3.

### Aug 12, 2026 — decoder acceptance law derived, proved, verified
`decoder_formula.py`, `decoder_scaling.py`, and Appendix A.

|A|/D → 2 ln 2 · Σ_{k=1}^{⌊N/r⌋} φ(kr)/(kr)². Verified
outcome-for-outcome on **27** instance/size combinations; the underlying
acceptance lemma on **42**. Settles both scaling directions: exactly
linear in D (measured D^{1.03±0.01}), and replaces the 1/r² envelope in
r (measured per-peak ratios 9.6/8.9 where 1/r² predicts 4.0; the law
gives 9.7/9.3).

**The consequence that matters:** the law depends only on r and N, not
on the base — so at matched control dimension the entire cross-base
difference in decoded success sits in the **quantum state**.
→ `GROVER.md` §5 carries an earlier partial version; `TEXTBOOK.md`
§11–12 is the complete derivation.

### Aug 12, 2026 — three-referee review cycle closed
Floratos pass (literature gaps, decoder appendix, ensemble over *a*),
Gottesman pass (scope fences, null expectation, inflation threshold,
d = 4 control), Innsbruck pass (predictions at *demonstrated* gate
noise, Zeeman channel). Round-2 fixes applied across all three.

### Aug 11–12, 2026 — hardware anchor campaign
IonQ Forte-1 and IQM Garnet via AWS Braket. Shallow ion circuit lands
inside its predicted band (0.617 ± 0.007 vs 0.60–0.70), pinning the
device's effective per-gate depolarizing strength at 0.007–0.009. Deep
circuit fails **coherently** (work qubit still 0.99); Garnet fails by
plain decoherence. Cost: USD 1,200.90.
→ `HARDWARE.md`.

### Aug 11, 2026 — d = 7 demo grid
`d7_demo.py`, 1000 trajectories. Decomposition direction unchanged
(`pavlidis` at/below the floor). Native-gate direction survives, but on
the ladder the ordering is **no longer monotone in d** — the optimum
sits at d = 5, with the seventh level's larger per-event damage pulling
d = 7 back. `ion` cost now fails cleanly on the ladder. **The window
between native and decomposed cost narrows with every added level.**
→ `COST_SENSITIVITY.md` §6.

---

## 4. Document status board

| document | status | note |
|---|---|---|
| `TEXTBOOK.md` | ✅ current | derivations from first principles; written against this manuscript |
| `PAPER.md` | ✅ current | this file |
| `ARXIV_SUBMISSION.md` | ✅ current | field-by-field walkthrough |
| `HARDWARE.md` | ✅ current | reinterpretation figure corrected to 0.15 |
| `COST_SENSITIVITY.md` | ✅ current | includes the d = 7 point |
| `GROVER.md` | ⚠️ partial | §5's decoder account predates the proved law — see `TEXTBOOK.md` §11–12 |
| `GRID_ALIGNMENT.md` | ⚠️ superseded in part | §6 scaling slopes retired by the m = 9 point |
| `CALIBRATION.md` | ⚠️ superseded in part | §6 slopes retired; §4 uses the confounded N = 15 instance |
| `GLOSSARY.md` | ⚠️ superseded in part | §5.3 benchmark slopes retired |
| `MECHANISM.md` | 📓 audit trail | records a falsified hypothesis; kept deliberately |
| `ROBUSTNESS.md` | ⚠️ incomplete | predates Zeeman, noise-inflation, and composite-*d* controls |
| `THEORY.md` | ⚠️ partial | physics background sound; §4 quotes retired slopes |
| `TRANSMON.md` | ✅ current | device background, unaffected |
| `SOTA.md` | ⚠️ incomplete | 21-paper synthesis; library is now 51 |
| `EXPERIMENTS.md` | ✅ current | proposal matches Sec. X |
| `PUBLICATION_PLAN.md` | 📓 historical | the plan that produced the paper; not a live document |
| `papers/INDEX.md` | ✅ current | 51 PDFs |

Legend: ✅ matches the manuscript · ⚠️ partially superseded (banner in
file) · 📓 kept as audit trail, not current results.

---

## 5. Reproducing every paper number

```bash
# correctness first
python3 test_qudit_shor.py         # 20 tests, ~3.5 min

# Sec. III — alignment
python3 grid_alignment.py          # Fig. 2
python3 same_n_control.py          # within-modulus control
python3 ensemble_a_traj.py 33      # Tab. I  (also: 21, 55)
python3 misalignment_scaling.py    # the size-drift objection
python3 fair_demo.py               # Fig. 3

# Sec. IV — the cost condition
python3 cost_fair.py               # Tab. II
python3 d7_demo.py                 # the seventh dimension
python3 matched_D.py               # matched control dimension

# Sec. V — scaling
python3 scaling_fair.py            # Fig. 4  (~1 h)
python3 scaling_fair_point.py      # single deep points (m = 9, m = 12)
python3 scaling_fair_n29.py        # instance robustness

# Sec. VI–VII — Grover, mechanism, decoder
python3 grover_study.py; python3 grover_cost.py
python3 exposure_collapse.py; python3 fidelity_collapse.py
python3 logfid_rescore.py          # the log-fidelity honesty check
python3 decoder_formula.py         # Appendix A lemma, 42 combinations
python3 decoder_scaling.py         # Tab. IV + Eq. (5)

# Sec. VIII — robustness
python3 spam_study.py; python3 dd_study.py; python3 noise_inflation.py
python3 collective_zeeman.py; python3 ion_zeeman_echo.py
python3 d4_control.py; python3 composite_control.py
python3 jankovic_check.py          # independent validation

# Sec. IX–X — hardware and predictions
python3 braket_raw_analysis.py     # from committed shot histograms
python3 ion_qpe_prediction.py      # Tab. VII

# figures, then the paper
python3 plots_grid.py plots_fair.py plots_scaling_fair.py \
        plots_grover.py plots_mechanism.py
cd paper && latexmk -pdf main.tex
```

`braket_qpe_anchor.py` re-submits to AWS Braket and **costs money**;
`braket_raw_analysis.py` reproduces every hardware number in the paper
from the committed histograms at no cost.
