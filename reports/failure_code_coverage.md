# Failure Code Coverage

| Diagnostic code | Case | Variant | Expected | Observed | Coverage |
|---|---|---|---|---|---|
| invalid_label_transition | issue_pr_metadata | invalid_label_transition | invalid_label_transition | invalid_label_transition | covered |
| unresolved_evidence_policy_ref | issue_pr_metadata | missing_policy_ref | unresolved_evidence_policy_ref | unresolved_evidence_policy_ref | covered |
| provenance_output_refs_mismatch | issue_pr_metadata | provenance_output_mismatch | provenance_output_refs_mismatch | provenance_output_refs_mismatch | covered |
| unresolved_input_ref | issue_pr_metadata | unresolved_issue_input_ref | unresolved_input_ref | unresolved_input_ref | covered |
| unresolved_validation_provenance_ref | issue_pr_metadata | validation_provenance_missing | unresolved_validation_provenance_ref | unresolved_validation_provenance_ref | covered |
| statement_digest_mismatch | doc_data_transform | digest_mismatch | statement_digest_mismatch | statement_digest_mismatch | covered |
| unresolved_evidence_policy_ref | doc_data_transform | missing_policy_link | unresolved_evidence_policy_ref | unresolved_evidence_policy_ref | covered |
| provenance_output_refs_mismatch | doc_data_transform | provenance_mismatch | provenance_output_refs_mismatch | provenance_output_refs_mismatch | covered |
| stale_source_digest | doc_data_transform | stale_source_hash | stale_source_digest | stale_source_digest | covered |
| provenance_output_refs_mismatch | doc_data_transform | wrong_derived_output_ref | provenance_output_refs_mismatch | provenance_output_refs_mismatch | covered |
| statement_digest_mismatch | test_result_summary | digest_mismatch | statement_digest_mismatch | statement_digest_mismatch | covered |
| test_summary_count_mismatch | test_result_summary | missing_failed_test | test_summary_count_mismatch | test_summary_count_mismatch | covered |
| test_summary_count_mismatch | test_result_summary | policy_threshold_violation | test_summary_count_mismatch | test_summary_count_mismatch | covered |
| unresolved_input_ref | test_result_summary | unresolved_test_artifact_ref | unresolved_input_ref | unresolved_input_ref | covered |
| test_summary_count_mismatch | test_result_summary | wrong_count | test_summary_count_mismatch | test_summary_count_mismatch | covered |
