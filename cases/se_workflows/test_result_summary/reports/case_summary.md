# Test-result summarization operation

| Variant | Expected | Observed | Primary code | Match |
|---|---|---|---|---|
| valid_test_summary | True | True | None | True |
| digest_mismatch | False | False | statement_digest_mismatch | True |
| missing_failed_test | False | False | test_summary_count_mismatch | True |
| policy_threshold_violation | False | False | test_summary_count_mismatch | True |
| unresolved_test_artifact_ref | False | False | unresolved_input_ref | True |
| wrong_count | False | False | test_summary_count_mismatch | True |
