# Scientific workflow failure matrix

| Case | Modification | Expected class | Expected exit code | Reference validator | Independent checker |
|---|---|---|---:|---:|---:|
| untouched | none | PASS | 0 | PASS 0 | TODO |
| tampered_input | modify one input byte after receipt generation | CONTENT_OR_DIGEST_MISMATCH | 2 | FAIL 2 | TODO |
| tampered_output | modify output artifact after receipt generation | CONTENT_OR_DIGEST_MISMATCH | 2 | FAIL 2 | TODO |
| missing_policy | remove policy reference or policy object | POLICY_LINKAGE_FAILURE | 5 | FAIL 5 | TODO |
| broken_evidence_link | point evidence reference to missing artifact | REFERENCE_RESOLUTION_FAILURE | 11 | FAIL 11 | TODO |
| version_mismatch | change profile version to unsupported version | VERSION_OR_PROFILE_MISMATCH | 4 | FAIL 4 | TODO |
| temporal_inconsistency | validation timestamp before execution timestamp | TEMPORAL_INCONSISTENCY | 6 | FAIL 6 | TODO |
| outcome_unverifiable | remove output digest while retaining success claim | OUTCOME_UNVERIFIABLE | 7 | FAIL 7 | TODO |
