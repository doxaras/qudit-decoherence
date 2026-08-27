# arXiv submission — field-by-field

> **Status 2026-08-16: fields below are current.** Rebuilt after the
> referee-driven revision, the four robustness simulations, the seed
> reproducibility fix and the full sweep re-run. Paper is **28 pages,
> 5 figures, 10 tables, 54 references**; tarball rebuilt from the
> current source. The abstract was shortened to 1913 characters so it
> fits arXiv's 1920-character metadata field verbatim -- the block
> below is a copy of the paper's abstract, not a separate summary.

Everything needed to submit `paper/main.tex` to arXiv. Rebuild the package
with `./paper/make_arxiv.sh`; it refuses to write the tarball unless a
standalone pdflatex-only build of exactly the shipped files is clean.

**Upload file:** `paper/arxiv-submission.tar.gz` (874 KB)
Contents: `main.tex`, `main.bbl`, and the five figure PNGs, flat, no
subdirectories. No `.aux`/`.log`/`.pdf`/`.bib` — arXiv rejects or ignores
those, and a stray `main.pdf` can make it skip compilation entirely.

---

## Before you start: endorsement

arXiv requires an **endorsement** for a first-time submitter's first paper in
a category. If this is your first `quant-ph` submission from this account,
you cannot submit until an established `quant-ph` author endorses you — arXiv
shows an endorsement code and a request link once you start. Registering an
[ORCID](https://orcid.org) on your account first is worth the two minutes;
it survives affiliation changes and disambiguates you permanently.

---

## Page 1 — Start submission

| Field | Value |
|---|---|
| Submission type | **New submission** (not Replacement / Cross-list / Journal ref) |

## Page 2 — License

| Field | Value |
|---|---|
| License | **CC BY 4.0** |

Matches the CC-BY-4.0 already on the Zenodo record, so the paper and its
artifact carry one license. arXiv's default "minimal rights" license is more
restrictive and cannot be loosened after announcement without emailing
support — pick CC BY here, not later.

## Page 3 — Authorship

| Field | Value |
|---|---|
| Authorship | **I am an author of this paper** |
| Agreement | Accept arXiv's submission policies |

## Page 4 — Categories

| Field | Value |
|---|---|
| Primary | **quant-ph** (Quantum Physics) |
| Cross-list | none required |

`cs.ET` (Emerging Technologies) is a defensible cross-list given the
gate-cost and hardware-anchor material, but `quant-ph` alone is the norm for
algorithm-under-noise work and cross-lists can be added after announcement.

## Page 5 — Metadata

**Title** — one line, no `\\` linebreak:

```
Native gates are necessary but not sufficient: the conditions for a qudit advantage in uncorrected quantum algorithms under decoherence
```

**Authors** — exactly this format, arXiv parses comma-separated:

```
John Doxaras
```

**Abstract** — plain text, LaTeX macros already stripped (see below).

**Comments:**

```
28 pages, 5 figures, 10 tables, 54 references. Code, data, and hardware records: https://github.com/doxaras/qudit-decoherence
```

**Leave these three empty:**

| Field | Why |
|---|---|
| Journal reference | Only for already-published work |
| DOI | **This field is for the published journal DOI, not the Zenodo code DOI.** Putting the Zenodo DOI here tells arXiv the paper is published in a journal, which it isn't. The Zenodo DOI is also absent from Comments on purpose: `10.5281/zenodo.21901533` is a *version* DOI for v1.0, which carries the superseded title and none of the revision. Cut a v1.1 release and put its concept DOI in Comments, or leave the repo link to stand alone as it does now. |
| Report number | Institutional preprint series only |

`ACM/MSC class` is optional and safely skipped.

## Page 6 — Upload files

Upload `paper/arxiv-submission.tar.gz`. arXiv unpacks and compiles it
server-side; the build takes a minute or two.

Expect exactly one benign warning class in the log: an underfull/overfull
`\hbox` or two, and possibly `A float is stuck`. Both are cosmetic — the
local build produces them too, and all fifteen floats (5 figures, 10
tables) place correctly.

If it errors on a missing `.bbl`, the tarball is stale: re-run
`./paper/make_arxiv.sh`.

## Page 7 — Preview

Download the generated PDF and check, in this order:

1. **28 pages** — a shorter PDF means a float or the bibliography was dropped
2. **All five figure PNGs render** — Figs. 2-6 — not grey boxes
3. **The TikZ pipeline diagram (Fig. 1, page 3)** draws: it is vector, not a
   PNG, so it is the one element sensitive to a TeX Live version gap
4. **No `[?]` citation marks** anywhere — those mean the `.bbl` did not load
5. Bibliography lists **54 entries**

## Page 8 — Review and submit

Confirm the metadata, then submit. Announcement is 20:00 US Eastern on
business days; papers submitted after that cutoff announce the next cycle.
Until announcement you can `Unsubmit` and fix anything.

After announcement, add the arXiv ID to the Zenodo record's "Related
identifiers" (`is supplemented by` / `is documented by`) so the code and
paper cross-link in both directions.

---

## Abstract as plain text

arXiv's abstract field accepts at most 1920 characters. The paper's
abstract is 1913, so this is the paper's abstract verbatim, with LaTeX
stripped -- the PDF and the metadata say the same thing. Paste it as is:

```
Whether qudits buy resilience against decoherence in full algorithms is open: prior noisy comparisons stop at gate-level criteria, arithmetic primitives, or a fixed dimension, and error-correcting codes have no instance to compress. We simulate Shor order finding, eigenstate phase estimation, and Grover search as bare, uncorrected circuits on qubit, qutrit, and ququint registers, under transmon-calibrated ladder and trapped-ion depolarizing channels, three entangling-gate cost models, and registers to Hilbert-space dimension 2.0x10^6. Two conditions organize all three. A qudit advantage needs an entangling gate whose cost grows at most linearly in d: two-level-decomposed gates forfeit it at d>=5 on the ladder and at d=7 everywhere, and the decomposed qutrit's residual advantage survives realistic accounting only under per-particle noise. And it survives only while the gate's own infidelity growth with d stays below a critical inflation factor we compute: converted through each channel's damage identity, the only native gate characterized across d=2/3/5 (99.6/98.7/93.7%) fails at d=5 in seven of eight readings, while its qutrit gate passes seven of eight; the transmon qutrit gate passes only when charged solely on the entangler, and loses once its 580-ns duration is charged as exposure. Further tightenings independently leave only d=3. Accumulated channel damage fixes end-state fidelity on one exponential across algorithms and bases; what the algorithm adds is its decoder, for which we derive an exact finite-size mediant-interval acceptance law, verified outcome-for-outcome, base-independent at matched control dimension: the quantum state carries the whole cross-base difference. A number-theoretic confound, grid alignment, reverses naive cross-dimension comparisons. A shallow trapped-ion anchor fixes the channel's scale; deeper anchors fail coherently, bounding the validated depth.
```

Written ASCII-only on purpose. arXiv accepts UTF-8, but ASCII removes any
chance of an em dash or `±` mangling in the mail announcement and the many
downstream services that scrape abstracts.
