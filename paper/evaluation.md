# EEOAP Paper Evaluation Notes

Keywords: EEOAP (Execution Evidence and Operation Accountability Profile, 执行证据与操作问责配置文件), execution evidence, operation accountability, validator, FDO (FAIR Digital Object, 公平数字对象)-style mapping, paper_case.

| Scenario | Expected result | Artifact or check |
| --- | --- | --- |
| paper demo command | PASS | `make paper-demo` completes in the scoped paper artifact path |
| valid evidence bundle | PASS | `examples/paper_case/evidence-valid.json` via `make paper-demo` |
| missing required field | FAIL | Covered by existing `examples/invalid-missing-required.json`; not duplicated inside paper_case |
| tampered output | FAIL as expected | `examples/paper_case/evidence-invalid-tampered-output.json` via output hash mismatch and stale integrity binding |
| tampered primary error code | `references_digest_mismatch` | `tampered_primary_error_code=references_digest_mismatch` in the demo summary |
| targeted EEOAP tests | 19 passed, 1 warning | Targeted tests only; full repository pytest success is not claimed |
| offline verification | PASS | `scripts/reproduce_paper_demo.sh` does not install dependencies and assumes the repository's existing Python dependencies are already available |
| FDO-style mapping | discussion-ready | `examples/paper_case/fdo-dataset.json` and `docs/paper-demo-boundary.md` |

The paper_case tests are low-risk additions and use the existing repository test style. No new dependency is introduced by the `paper_case` artifact. Reproduction assumes an environment with the repository's existing Python dependencies available; the demo script itself does not install dependencies. No schema change, package metadata change, or network access is required.
