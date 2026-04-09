# acmart TOSEM Scaffold

This directory contains the current acmart-based anonymous-review scaffold derived from the stable English draft in `paper/tosem_en/` and the curated bibliography scaffold in `paper/submission_tosem/references.bib`.

The goal of this scaffold is submission packaging rather than camera-ready polish. It provides:

- a journal-style `main.tex`
- section-level `.tex` files
- a copied `references.bib`
- an artifact availability note
- integrated figure assets under `figures/`
- integrated table assets under `tables/`
- build and handoff notes for the anonymous review package

The scaffold is intended to compile locally with a standard ACM LaTeX toolchain and to remain safe for anonymous review. Figures and tables are integrated as real assets, the CCS block is populated with a conservative final candidate in `ccs_keywords.tex`, and the current text withholds public repository/release/archive identifiers in the review version.

Suggested local build flow:

```bash
cd paper/submission_tosem/acmart
pdflatex main.tex
bibtex main
pdflatex main.tex
pdflatex main.tex
```
