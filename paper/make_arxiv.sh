#!/bin/sh
# Build paper/arxiv-submission.tar.gz: the source package arXiv compiles.
#
# arXiv does NOT run BibTeX, so main.bbl ships in the tarball and must be
# current — this script rebuilds it from refs.bib rather than trusting the
# copy on disk (which .gitignore keeps out of the repo anyway).
#
# Figures live in ../results/ in the repo but must sit beside main.tex in
# the tarball; main.tex's \graphicspath lists {./} first so one source
# builds in both layouts with no edit.
set -e
HERE="$(cd "$(dirname "$0")" && pwd)"
OUT="$HERE/arxiv-submission.tar.gz"
STAGE="$(mktemp -d)"
trap 'rm -rf "$STAGE"' EXIT

FIGS="grid_alignment.png fair_demo.png scaling_fair.png grover.png mechanism.png"

cd "$HERE"
latexmk -pdf -interaction=nonstopmode main.tex >/dev/null
[ -f main.bbl ] || { echo "ABORT: main.bbl was not produced" >&2; exit 1; }

cp main.tex main.bbl "$STAGE/"
for f in $FIGS; do cp "$HERE/../results/$f" "$STAGE/"; done

# Verify the package standalone, exactly as arXiv sees it: pdflatex only,
# no bibtex, nothing but the shipped files present.
VERIFY="$STAGE/.verify"
mkdir "$VERIFY"
cp "$STAGE"/*.tex "$STAGE"/*.bbl "$STAGE"/*.png "$VERIFY/"
cd "$VERIFY"
for _ in 1 2 3; do pdflatex -interaction=nonstopmode main.tex >/dev/null 2>&1 || true; done
if grep -qE "^!|Undefined control sequence|LaTeX Error" main.log; then
  echo "ABORT: standalone build failed — see $VERIFY/main.log" >&2
  grep -E "^!|Undefined control sequence|LaTeX Error" main.log | head >&2
  exit 1
fi
if grep -qE "Warning.*undefined" main.log; then
  echo "ABORT: undefined references or citations in the standalone build" >&2
  grep -E "Warning.*undefined" main.log | head >&2
  exit 1
fi
rm -rf "$VERIFY"

cd "$STAGE"
COPYFILE_DISABLE=1 tar --no-xattrs -czf "$OUT" main.tex main.bbl $FIGS
echo "wrote $OUT"
tar -tzf "$OUT"
