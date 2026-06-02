# SE Case Matrix

| Case | Variant | Expected | Profile-aware | Primary code | Schema-only | Log-only | Policy-only | Match |
|---|---|---|---|---|---|---|---|---|
| issue_pr_metadata | valid_label_update | True | True | None | True | True | True | True |
| issue_pr_metadata | invalid_label_transition | False | False | invalid_label_transition | True | True | False | True |
| issue_pr_metadata | missing_policy_ref | False | False | unresolved_evidence_policy_ref | True | True | True | True |
| issue_pr_metadata | provenance_output_mismatch | False | False | provenance_output_refs_mismatch | True | True | True | True |
| issue_pr_metadata | unresolved_issue_input_ref | False | False | unresolved_input_ref | True | True | True | True |
| issue_pr_metadata | validation_provenance_missing | False | False | unresolved_validation_provenance_ref | True | True | True | True |
| doc_data_transform | valid_doc_metadata | True | True | None | True | True | True | True |
| doc_data_transform | digest_mismatch | False | False | statement_digest_mismatch | True | True | True | True |
| doc_data_transform | missing_policy_link | False | False | unresolved_evidence_policy_ref | True | True | True | True |
| doc_data_transform | provenance_mismatch | False | False | provenance_output_refs_mismatch | True | True | True | True |
| doc_data_transform | stale_source_hash | False | False | stale_source_digest | True | True | True | True |
| doc_data_transform | wrong_derived_output_ref | False | False | provenance_output_refs_mismatch | True | True | True | True |
| test_result_summary | valid_test_summary | True | True | None | True | True | True | True |
| test_result_summary | digest_mismatch | False | False | statement_digest_mismatch | True | True | True | True |
| test_result_summary | missing_failed_test | False | False | test_summary_count_mismatch | True | True | True | True |
| test_result_summary | policy_threshold_violation | False | False | test_summary_count_mismatch | True | True | False | True |
| test_result_summary | unresolved_test_artifact_ref | False | False | unresolved_input_ref | True | True | True | True |
| test_result_summary | wrong_count | False | False | test_summary_count_mismatch | True | True | True | True |

These are representative reproducible SE workflow fixtures, not industrial real-world cases.
