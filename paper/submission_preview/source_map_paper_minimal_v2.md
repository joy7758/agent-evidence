# Paper-Minimal v2 Source Map

## Source And Outputs

| role | path |
| --- | --- |
| full v2 source | `paper/drafts/operation_accountability_boundary_full_v2.md` |
| final consistency audit | `paper/drafts/operation_accountability_boundary_full_v2_audit.md` |
| abstract output | `paper/submission_preview/main_abstract_paper_minimal_v2.tex` |
| body output | `paper/submission_preview/main_body_paper_minimal_v2.md` |
| wrapper output | `paper/submission_preview/main_wrapper_paper_minimal_v2.tex` |
| temporary TeX body | `paper/submission_preview/build/main_body_paper_minimal_v2.tex` |
| citation keys | `paper/submission_preview/citation_keys_paper_minimal_v2.txt` |
| preview references path | `paper/submission_preview/references_paper_minimal_v2.bib` |
| missing references report | `paper/submission_preview/MISSING_REFERENCES_PAPER_MINIMAL_V2.md` |
| build audit | `paper/submission_preview/BUILD_PREVIEW_AUDIT.md` |
| reference restoration audit | `paper/submission_preview/REFERENCE_RESTORATION_AUDIT.md` |
| bibliography completion audit | `paper/submission_preview/BIBLIOGRAPHY_COMPLETION_AUDIT.md` |
| layout patch audit | `paper/submission_preview/LAYOUT_PATCH_AUDIT.md` |

The body preview removes the source title and abstract, then promotes the
remaining Markdown headings one level so pandoc can emit normal LaTeX section
commands. This is a formatting conversion only; it does not change the
paper-minimal claim boundary.

## Commands

Build the isolated preview:

```bash
bash paper/submission_preview/build_preview.sh
```

Run the paper-minimal rerun:

```bash
bash scripts/reproduce_paper_minimal.sh
```

Generate the review package:

```bash
agent-evidence review-pack create --paper-minimal --out /tmp/review-pack-paper-minimal.zip
```

## Non-Claims

The paper-minimal path does not claim:

- no registry design
- no multi-agent orchestration
- no full FDO interoperability
- no full cryptographic trust fabric
- no legal non-repudiation
- no production deployment
- no broad platform governance
- no broad runtime integration coverage
- no compliance approval

## Active Evidence Set

The preview preserves the active evidence set:

- 1 valid example: `examples/minimal-valid-evidence.json`
- 3 controlled invalid examples:
  - `examples/invalid-missing-required.json`
  - `examples/invalid-unclosed-reference.json`
  - `examples/invalid-policy-link-broken.json`
- 1 metadata-enrichment demo: `demo/run_operation_accountability_demo.py`
- 1 rerun command: `bash scripts/reproduce_paper_minimal.sh`
- 1 review package command: `agent-evidence review-pack create --paper-minimal --out /tmp/review-pack-paper-minimal.zip`
