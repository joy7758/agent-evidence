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
CITATION_KEYS="$PREVIEW_DIR/citation_keys_paper_minimal_v2.txt"
BIB="$PREVIEW_DIR/references_paper_minimal_v2.bib"
CURRENT_KEYS="$BUILD_DIR/citation_keys_current.txt"
RECORDED_KEYS="$BUILD_DIR/citation_keys_recorded.txt"
BIB_KEYS="$BUILD_DIR/bibliography_keys_current.txt"
MISSING_KEYS="$BUILD_DIR/missing_citation_keys.txt"

if ! command -v pandoc >/dev/null 2>&1; then
  echo "ERROR: pandoc is required to generate $BODY_TEX." >&2
  exit 2
fi

mkdir -p "$BUILD_DIR"

perl -nE 'while (/(?<![\w@])@([A-Za-z0-9_:-]+)/g) { say $1 }' "$BODY_MD" \
  | sort -u >"$CURRENT_KEYS"

if [ -f "$CITATION_KEYS" ]; then
  awk 'NF && $1 !~ /^#/ { print }' "$CITATION_KEYS" | sort -u >"$RECORDED_KEYS"
  if ! cmp -s "$CURRENT_KEYS" "$RECORDED_KEYS"; then
    echo "WARNING: $CITATION_KEYS differs from current body citation scan." >&2
  fi
else
  echo "WARNING: $CITATION_KEYS was not found." >&2
fi

if [ -s "$BIB" ]; then
  perl -ne 'print "$1\n" if /^\s*@[A-Za-z]+\s*\{\s*([^,\s]+)\s*,/' "$BIB" \
    | sort -u >"$BIB_KEYS"
else
  : >"$BIB_KEYS"
fi

comm -23 "$CURRENT_KEYS" "$BIB_KEYS" >"$MISSING_KEYS"

KEY_COUNT="$(awk 'NF { count++ } END { print count + 0 }' "$CURRENT_KEYS")"
MATCHED_COUNT="$(comm -12 "$CURRENT_KEYS" "$BIB_KEYS" | awk 'NF { count++ } END { print count + 0 }')"
MISSING_COUNT="$(awk 'NF { count++ } END { print count + 0 }' "$MISSING_KEYS")"

pandoc "$BODY_MD" \
  --from=markdown+citations \
  --to=latex \
  --natbib \
  --syntax-highlighting=none \
  --top-level-division=section \
  --output="$BODY_TEX"

perl -0pi -e 's/\\citep\{([^}]+)\}/\\cite{$1}/g; s/\\citet\{([^}]+)\}/\\cite{$1}/g; s/^\{\\def\\LTcaptype\{none\} % do not increment counter\n//mg; s/^\\begin\{longtable\}\[\]\{(.+)\}$/\\begin{table*}[t]\n\\centering\\scriptsize\n\\resizebox{\\textwidth}{!}{%\n\\begin{tabular}{$1}/mg; s/^\\endhead\n//mg; s/^\\bottomrule\\noalign\{\}\n//mg; s/^\\endlastfoot\n//mg; s/^\\end\{longtable\}\n\}$/\\end{tabular}%\n}\n\\end{table*}/mg' "$BODY_TEX"

echo "generated: $BODY_TEX"
echo "citation_key_count: $KEY_COUNT"
echo "matched_bibliography_entry_count: $MATCHED_COUNT"
echo "missing_bibliography_key_count: $MISSING_COUNT"

if [ "$MISSING_COUNT" -gt 0 ]; then
  echo "WARNING: bibliography incomplete; PDF generation skipped." >&2
  echo "missing keys written to: $MISSING_KEYS" >&2
  exit 0
fi

if [ "$KEY_COUNT" -eq 0 ]; then
  if command -v pdflatex >/dev/null 2>&1; then
    pdflatex -interaction=nonstopmode -halt-on-error \
      -output-directory="$BUILD_DIR" \
      "$WRAPPER"
    pdflatex -interaction=nonstopmode -halt-on-error \
      -output-directory="$BUILD_DIR" \
      "$WRAPPER"
    echo "generated: $BUILD_DIR/main_wrapper_paper_minimal_v2.pdf"
    exit 0
  fi
  echo "WARNING: pdflatex was not found; generated TeX only." >&2
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
  if [ "$KEY_COUNT" -gt 0 ] && command -v bibtex >/dev/null 2>&1; then
    bibtex "$BUILD_DIR/main_wrapper_paper_minimal_v2" || true
  elif [ "$KEY_COUNT" -gt 0 ]; then
    echo "WARNING: bibtex was not found; generated TeX only." >&2
    exit 0
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
