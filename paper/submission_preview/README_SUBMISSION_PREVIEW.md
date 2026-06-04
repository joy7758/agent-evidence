# Paper-Minimal Submission Source Preview

This directory contains an isolated preview of submission-source files for the
paper-minimal operation-accountability manuscript.

Status: isolated preview only; not a formal submission source. This preview
does not overwrite `main_body.md`, `main_wrapper.tex`, or any file under
`submission/`. It is also explicitly: 不覆盖正式投稿源.

## Source

The preview is generated from:

```text
paper/drafts/operation_accountability_boundary_full_v2.md
```

The current paper-facing boundary is the paper-minimal path:

```text
one operation accountability statement
Execution Evidence and Operation Accountability Profile v0.1
one profile-aware validator path
one valid example
three controlled invalid examples
one metadata-enrichment demo
one reproducible rerun surface
one paper-minimal review package
```

This preview does not broaden the claim into registry design, multi-agent
orchestration, complete object interoperability, legal assurance, deployment,
broad platform governance, broad runtime coverage, or compliance approval.

## Files

```text
paper/submission_preview/main_abstract_paper_minimal_v2.tex
paper/submission_preview/main_body_paper_minimal_v2.md
paper/submission_preview/main_wrapper_paper_minimal_v2.tex
paper/submission_preview/source_map_paper_minimal_v2.md
paper/submission_preview/build_preview.sh
paper/submission_preview/SUBMISSION_PREVIEW_AUDIT.md
```

`paper/submission_preview/build/` is generated output from the preview build
script and should not be committed.

## Build Preview

Run from the repository root:

```bash
bash paper/submission_preview/build_preview.sh
```

The script converts the preview body Markdown into temporary TeX under:

```text
paper/submission_preview/build/main_body_paper_minimal_v2.tex
```

If `pandoc` is unavailable, the script exits nonzero with a clear error. If a
LaTeX compiler or the configured bibliography file is unavailable, the script
keeps the generated TeX preview and reports why PDF generation was skipped.
Preview PDF compilation requires a local preview bibliography at
`paper/submission_preview/references_paper_minimal_v2.bib`. If bibliography
entries are incomplete, the build script generates TeX and skips PDF
compilation.

## Mainline Rerun

Run the paper-minimal rerun from the repository root:

```bash
bash scripts/reproduce_paper_minimal.sh
```

## Review Package

Generate the paper-minimal review package with:

```bash
agent-evidence review-pack create --paper-minimal --out /tmp/review-pack-paper-minimal.zip
```
