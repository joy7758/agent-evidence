# Claim-to-Evidence Table for Submission

| Claim | Evidence in submission package | Artifact evidence | Boundary / non-claim |
| --- | --- | --- | --- |
| Minimal profile | Manuscript Sections 1-3. | `evidence-valid.json` and paper_case descriptors. | Minimal operation-level profile only; not a full governance platform. |
| Validator path | Manuscript Section 4 and reproducibility summary. | `make paper-demo` and local validator path. | No hosted API, OpenAPI, MCP, browser UI, or external verifier is claimed. |
| Valid evidence PASS | Manuscript Sections 4 and 6. | `PASS valid evidence bundle`. | Applies to scoped paper_case, not every possible evidence object. |
| Tampered output FAIL | Manuscript Sections 4 and 6. | `FAIL tampered output hash mismatch`. | Demonstrates one altered-output-reference case, not all attacks. |
| references_digest_mismatch | Manuscript Sections 4, 6, and 7. | `tampered_primary_error_code=references_digest_mismatch`. | Claimed for this tampered paper case only. |
| Targeted tests | Manuscript Sections 6, 7, and reviewer summary. | `tests/test_paper_case.py`; `tests/test_operation_accountability_profile.py`; `19 passed, 1 warning`. | Full repository pytest success is not claimed. |
| FDO-style mapping | Manuscript Section 5. | `fdo-dataset.json` and mapping discussion. | Discussion mapping only; no official FDO adoption, conformance, certification, or endorsement. |
| Local-only artifact | Artifact availability statement and README. | Local tag `eeoap-v0.1-paper`; commit `96f444b7ed39b39fe9f47e428af835952e843cb0`. | Tag is not claimed as publicly pushed; no public GitHub Release or Zenodo DOI. |
| Non-claims | Non-claims checklist, declarations, and limitations. | Local artifact boundary only. | No production readiness, legal compliance, semantic correctness, ZKP implementation, artifact badge, or external endorsement. |
