#!/usr/bin/env bash
set -euo pipefail

if [ ! -f "pyproject.toml" ] || [ ! -d "agent_evidence" ]; then
  echo "ERROR: run this script from the repository root." >&2
  exit 2
fi

PREVIEW_DIR="paper/submission_preview"
BUILD_DIR="$PREVIEW_DIR/build"
BODY_MD="$PREVIEW_DIR/main_body_paper_minimal_v2.md"
BODY_TEX="$BUILD_DIR/main_body_paper_minimal_v2.tex"
WRAPPER="$PREVIEW_DIR/main_wrapper_paper_minimal_v2.tex"
BIB="submission/58_references_tse.bib"

if ! command -v pandoc >/dev/null 2>&1; then
  echo "ERROR: pandoc is required to generate $BODY_TEX." >&2
  exit 2
fi

mkdir -p "$BUILD_DIR"

pandoc "$BODY_MD" \
  --from=gfm \
  --to=latex \
  --top-level-division=section \
  --output="$BODY_TEX"

echo "generated: $BODY_TEX"

if [ ! -f "$BIB" ]; then
  echo "WARNING: bibliography file $BIB was not found; PDF generation skipped." >&2
  exit 0
fi

if command -v latexmk >/dev/null 2>&1; then
  latexmk -pdf -interaction=nonstopmode -halt-on-error \
    -output-directory="$BUILD_DIR" \
    "$WRAPPER"
  echo "generated: $BUILD_DIR/main_wrapper_paper_minimal_v2.pdf"
  exit 0
fi

if command -v pdflatex >/dev/null 2>&1; then
  pdflatex -interaction=nonstopmode -halt-on-error \
    -output-directory="$BUILD_DIR" \
    "$WRAPPER"
  if command -v bibtex >/dev/null 2>&1; then
    bibtex "$BUILD_DIR/main_wrapper_paper_minimal_v2" || true
  fi
  pdflatex -interaction=nonstopmode -halt-on-error \
    -output-directory="$BUILD_DIR" \
    "$WRAPPER"
  pdflatex -interaction=nonstopmode -halt-on-error \
    -output-directory="$BUILD_DIR" \
    "$WRAPPER"
  echo "generated: $BUILD_DIR/main_wrapper_paper_minimal_v2.pdf"
  exit 0
fi

echo "WARNING: latexmk or pdflatex was not found; generated TeX only." >&2
