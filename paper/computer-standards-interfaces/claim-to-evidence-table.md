# Claim-to-Evidence Table

Status: submission-preparation table, not final journal formatting.

| Claim | Evidence in artifact | Boundary / non-claim |
| --- | --- | --- |
| Minimal profile claim | EEOAP evidence object in `examples/paper_case/evidence-valid.json`; profile discussion in the manuscript draft. | Minimal operation-level profile only; not a full governance platform or universal agent registry. |
| Validator path claim | Local `make paper-demo` path and validator-backed checks over the paper case. | No hosted API, OpenAPI, MCP, browser UI, production service, or external verifier is claimed. |
| Valid evidence PASS claim | Expected output includes `PASS valid evidence bundle`. | Applies to the scoped `paper_case`; not a claim about all possible evidence objects. |
| Tampered output FAIL claim | Expected output includes `FAIL tampered output hash mismatch`. | Demonstrates one altered-output-reference case; not a complete adversarial security proof. |
| `references_digest_mismatch` claim | Demo summary exposes `tampered_primary_error_code=references_digest_mismatch`. | Error code is claimed for this tampered paper case only. |
| Targeted tests claim | `tests/test_paper_case.py` and `tests/test_operation_accountability_profile.py` previously reported `19 passed, 1 warning`. | Full repository pytest success is not claimed. |
| FDO-style mapping claim | `examples/paper_case/fdo-dataset.json` and manuscript mapping section. | Discussion mapping only; no official FDO adoption, conformance, certification, or endorsement. |
| Artifact anchor claim | Local sealed tag `eeoap-v0.1-paper`; sealed artifact commit `96f444b7ed39b39fe9f47e428af835952e843cb0`. | Tag is not claimed as publicly pushed; no public GitHub Release or Zenodo DOI is claimed. |
| Non-claims boundary | README, manuscript limitations, artifact availability, and declarations. | No production readiness, legal compliance, semantic correctness of AI output, ZKP implementation, or full cryptographic trust fabric is claimed. |
