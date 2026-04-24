# Public scientific workflow failure matrix

| Case | Modification | Expected class | Expected exit code | Repository validator | Independent checker |
|---|---|---|---:|---:|---:|
| untouched | none | PASS | 0 | PASS 0 | PASS 0 |
| tampered_input | append bytes to one input FASTQ gzip after receipt generation | CONTENT_OR_DIGEST_MISMATCH | 2 | FAIL 2 | FAIL 2 |
| tampered_output | append a newline to `outputs/qc_metrics.json` after receipt generation | CONTENT_OR_DIGEST_MISMATCH | 2 | FAIL 2 | FAIL 2 |
| missing_policy | remove `policy.json` | POLICY_LINKAGE_FAILURE | 5 | FAIL 5 | FAIL 5 |
| broken_evidence_link | point workflow-script evidence reference to a missing file | REFERENCE_RESOLUTION_FAILURE | 11 | FAIL 11 | FAIL 11 |
| version_mismatch | change profile version to `ncs-v0-broken` | VERSION_OR_PROFILE_MISMATCH | 4 | FAIL 4 | FAIL 4 |
| temporal_inconsistency | set `validation_time` earlier than `execution_start` | TEMPORAL_INCONSISTENCY | 6 | FAIL 6 | FAIL 6 |
| outcome_unverifiable | remove the primary output digest while retaining outcome claims | OUTCOME_UNVERIFIABLE | 7 | FAIL 7 | FAIL 7 |
