# EEOAP Paper Evaluation Notes

Keywords: EEOAP, execution evidence, operation accountability, validator, FDO-style mapping, paper_case.

| Scenario | Expected result | Artifact or check |
| --- | --- | --- |
| valid evidence | PASS | `examples/paper_case/evidence-valid.json` via `make paper-demo` |
| missing required field | FAIL | Covered by existing `examples/invalid-missing-required.json`; not duplicated inside paper_case |
| tampered output | FAIL | `examples/paper_case/evidence-invalid-tampered-output.json` via output hash mismatch and stale integrity binding |
| offline verification | PASS | `scripts/reproduce_paper_demo.sh` runs without network access or dependency installation |
| FDO-style mapping | discussion-ready | `examples/paper_case/fdo-dataset.json` and `docs/paper-demo-boundary.md` |

The paper_case tests are low-risk additions and use the existing repository test style. No new dependency, schema change, package metadata change, or network access is required.
