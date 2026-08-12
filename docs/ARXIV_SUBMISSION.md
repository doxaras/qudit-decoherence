# arXiv submission — field-by-field

Everything needed to submit `paper/main.tex` to arXiv. Rebuild the package
with `./paper/make_arxiv.sh`; it refuses to write the tarball unless a
standalone pdflatex-only build of exactly the shipped files is clean.

**Upload file:** `paper/arxiv-submission.tar.gz` (853 KB)
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
Native gates or nothing: the condition for a qudit advantage in uncorrected quantum algorithms under decoherence
```

**Authors** — exactly this format, arXiv parses comma-separated:

```
John Doxaras
```

**Abstract** — plain text, LaTeX macros already stripped (see below).

**Comments:**

```
18 pages, 6 figures, 5 tables, 47 references. Code, data, and hardware records: https://github.com/doxaras/qudit-decoherence (v1.0 archived at https://doi.org/10.5281/zenodo.21901534)
```

**Leave these three empty:**

| Field | Why |
|---|---|
| Journal reference | Only for already-published work |
| DOI | **This field is for the published journal DOI, not the Zenodo code DOI.** Putting the Zenodo DOI here tells arXiv the paper is published in a journal, which it isn't. It belongs in Comments, where it is above. |
| Report number | Institutional preprint series only |

`ACM/MSC class` is optional and safely skipped.

## Page 6 — Upload files

Upload `paper/arxiv-submission.tar.gz`. arXiv unpacks and compiles it
server-side; the build takes a minute or two.

Expect exactly one benign warning class in the log: an underfull/overfull
`\hbox` or two, and possibly `A float is stuck`. Both are cosmetic — the
local build produces them too and all six floats place correctly.

If it errors on a missing `.bbl`, the tarball is stale: re-run
`./paper/make_arxiv.sh`.

## Page 7 — Preview

Download the generated PDF and check, in this order:

1. **18 pages** — a shorter PDF means a float or the bibliography was dropped
2. **All five figure PNGs render** — they land on pages 5, 7, 8, 10, and 11 — not grey boxes
3. **The TikZ pipeline diagram (Fig. 1, page 3)** draws: it is vector, not a
   PNG, so it is the one element sensitive to a TeX Live version gap
4. **No `[?]` citation marks** anywhere — those mean the `.bbl` did not load
5. Bibliography lists **47 entries**

## Page 8 — Review and submit

Confirm the metadata, then submit. Announcement is 20:00 US Eastern on
business days; papers submitted after that cutoff announce the next cycle.
Until announcement you can `Unsubmit` and fix anything.

After announcement, add the arXiv ID to the Zenodo record's "Related
identifiers" (`is supplemented by` / `is documented by`) so the code and
paper cross-link in both directions.

---

## Abstract as plain text

Paste verbatim:

```
Whether qudits buy resilience against decoherence is a recognized open question: prior work compares algorithms by noiseless resource counts, or error-correcting codes, which have no problem instance to compress. We simulate Shor order finding, eigenstate phase estimation, and Grover search as bare, uncorrected circuits - the regime of near-term demonstrations - on qubit, qutrit, and ququint registers (with a demo-size d=7 check) under two decoherence channels - a ladder channel calibrated to published per-level transmon coherence data and a depolarizing channel representative of trapped-ion qudits - three entangling-gate cost models, and registers to 3.9x10^5 Hilbert dimensions (18.6 qubit-equivalents). One condition governs all three algorithms: qudits outperform qubits only with a native two-qudit entangling gate whose cost grows no faster than linearly in d. Gates compiled by two-level decomposition forfeit the advantage in every case tested but one - Shor at d=3 under per-particle noise, where width compression alone survives the depth surcharge; whether linear cost suffices is set by the level and structure of the operating dephasing - the advantage holds on per-particle and refocused-ladder hardware, free-evolution ladder dephasing splits the linear-cost cells, and unmitigated Zeeman-structured dephasing reverses the verdict outright. Along the way we identify a number-theoretic confound - grid alignment of the phases s/r - that reverses naive cross-dimension Shor comparisons and predicts the winner in every biased instance tested (three instances x two noise models), and we reduce the mechanism to a quantitative law: accumulated channel damage fixes end-state fidelity on a single exponential across algorithms and bases, with amplitude ~1 and R^2=0.97-0.99 (the first-order expectation; in log fidelity the law holds within a factor of two until states approach their 1/dim floor); the algorithm enters only through its decoder's error tolerance, which we reduce to an exact number-theoretic law verified outcome-for-outcome against the decoder. The qubit branch of our predictions is anchored on hardware: the shallow compiled circuit reproduces its predicted success band on a commercial trapped-ion processor (0.617 +/- 0.007 vs 0.60-0.70), pinning the device's effective depolarizing strength at its measured per-gate infidelity.
```

Written ASCII-only on purpose. arXiv accepts UTF-8, but ASCII removes any
chance of an em dash or `±` mangling in the mail announcement and the many
downstream services that scrape abstracts.
