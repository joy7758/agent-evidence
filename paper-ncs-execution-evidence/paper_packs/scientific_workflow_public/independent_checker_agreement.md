# Independent checker agreement table

Pack: `paper-ncs-execution-evidence/paper_packs/scientific_workflow_public`

| Case | Description | Expected class | Expected code | Repository code | Independent class | Independent code | Agreement |
|---|---|---|---:|---:|---|---:|---:|
| scientific_workflow_public | Pack satisfies profile and verification checks. | PASS | 0 | 0 | PASS | 0 | True |
| failures/tampered_input | Recomputed content digest differs from the declared digest. | CONTENT_OR_DIGEST_MISMATCH | 2 | 2 | CONTENT_OR_DIGEST_MISMATCH | 2 | True |
| failures/tampered_output | Recomputed content digest differs from the declared digest. | CONTENT_OR_DIGEST_MISMATCH | 2 | 2 | CONTENT_OR_DIGEST_MISMATCH | 2 | True |
| failures/missing_policy | Policy reference or policy digest linkage is broken. | POLICY_LINKAGE_FAILURE | 5 | 5 | POLICY_LINKAGE_FAILURE | 5 | True |
| failures/broken_evidence_link | Referenced evidence artifact cannot be resolved inside the pack. | REFERENCE_RESOLUTION_FAILURE | 11 | 11 | REFERENCE_RESOLUTION_FAILURE | 11 | True |
| failures/version_mismatch | Pack declares an unsupported profile version. | VERSION_OR_PROFILE_MISMATCH | 4 | 4 | VERSION_OR_PROFILE_MISMATCH | 4 | True |
| failures/temporal_inconsistency | Execution and validation timestamps violate required ordering. | TEMPORAL_INCONSISTENCY | 6 | 6 | TEMPORAL_INCONSISTENCY | 6 | True |
| failures/outcome_unverifiable | Claimed outcome cannot be linked to digest-backed primary output evidence. | OUTCOME_UNVERIFIABLE | 7 | 7 | OUTCOME_UNVERIFIABLE | 7 | True |
