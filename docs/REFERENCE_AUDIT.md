# Reference audit — 2026-08-28

Run against `paper/refs.bib` (54 entries) and `paper/main.tex` ahead of arXiv
submission. Motivated by arXiv's May 2026 enforcement policy, under which the
ban trigger is **unverified AI output** — hallucinated references, leftover
model prompts, fabricated tables — not disclosed AI assistance. This audit
tests for exactly those failure modes.

Script: `verify_refs.py` (scratchpad). Sources of truth: arXiv API,
Crossref REST, DBLP.

## Result

| Check | Outcome |
|---|---|
| Entries in `refs.bib` | 54 |
| arXiv IDs that resolve | **45 / 45** |
| First author matches arXiv record | **45 / 45** |
| Hallucinated / non-existent references | **0** |
| Wrong volume / page / year after adjudication | **0** |
| Cited keys missing from bib | 0 |
| Bib entries never cited | 0 |
| Undefined citations or references in the build | 0 |
| `??` (unresolved refs) in the rendered PDF | 0 |
| LLM artifacts in `main.tex` (prompts, placeholders, "as an AI", TODO/FIXME) | 0 |

**Every reference is real and correctly cited.**

## Adjudication of the 15 automated flags

All fifteen were artifacts of automated matching, not citation errors.

*Crossref matched a different edition of the same work:*

- `shor1997` — flagged vol 41, pp. 303–332, 1999. That is the 1999 *SIAM
  Review* reprint. The bib cites SIAM J. Comput. **26**, 1484 (1997),
  confirmed correct via DOI `10.1137/S0097539795293172` (26, 1484–1509, 1997).
- `gottesman1999` — flagged pp. 302–313. That is the Springer LNCS conference
  version. The bib cites Chaos, Solitons & Fractals **10**, 1749, confirmed
  via DOI `10.1016/S0960-0779(98)00218-5` (10, 1749–1758, 1999).
- `khinchin1964` — matched an unrelated CUP chapter. The Chicago 1964 edition
  is correct.

*Preprint title differs from published title; bib correctly uses the
published one:*

- `pavlidis2021` — confirmed Phys. Rev. A **103**, 032417 (2021).
- `blok2021` — confirmed Phys. Rev. X **11**, 021010 (2021).
- `meth2025` — confirmed Nat. Phys. **21**, 570 (2025).
- `kiktenko2025` — confirmed Rev. Mod. Phys. **97**, 021003 (2025); the
  "Colloquium:" prefix is part of the published title.

*Crossref metadata defective or journal not indexed:*

- `campbell2014` — confirmed Phys. Rev. Lett. **113**, 230501 (2014) by DOI.
  PRL uses article numbers, so Crossref carries no page field.
- `chiesa2024` — Crossref reports vol 64 / 2023, which cannot be right for a
  paper posted in May 2024. arXiv's author-supplied journal_ref and the DOI
  both say Contemporary Physics, 2024. Bib is correct.
- `bourdon2007` — absent from Crossref (Rinton Press coverage). **DBLP
  confirms** Quantum Inf. Comput. **7**(5–6), 522–550 (2007), DOI
  `10.26421/QIC7.5-6-7`.
- `ekera2024` — flagged pp. 1–40 against bib `pages = 11`. 11 is the ACM
  article number; both describe the same record.
- `lu2020` — Crossref issue date 2019 is the online-first date; the journal
  issue is vol 3 (2020), as cited.

*Preprints cited as `@misc` that have since been published — see below.*

- `low2023`, `shi2025`, `sutherland2023`.

## Optional improvements (not errors)

Three entries are cited as arXiv preprints and now have published versions.
All three were confirmed to be the same paper (title and authors match):

| Key | Currently | Published as |
|---|---|---|
| `sutherland2023` | arXiv:2312.09399 | Phys. Rev. A **109**, 022620 (2024), `10.1103/PhysRevA.109.022620` |
| `low2023` | arXiv:2306.03340 | npj Quantum Inf. **11** (2025), `10.1038/s41534-025-01031-y` |
| `shi2025` | arXiv:2506.09371 | Nat. Commun. **17** (2026), `10.1038/s41467-026-68746-0` |

`shi2025` is worth upgrading on substance as well as form: a trapped-ion
qudit algorithm implementation published in Nature Communications in January
2026 is a stronger citation than a preprint, and a referee will know it has
appeared.

`bourdon2007` could also gain `doi = {10.26421/QIC7.5-6-7}`.
