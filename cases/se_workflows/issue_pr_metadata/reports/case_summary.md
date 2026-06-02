# Issue / PR metadata operation

| Variant | Expected | Observed | Primary code | Match |
|---|---|---|---|---|
| valid_label_update | True | True | None | True |
| invalid_label_transition | False | False | invalid_label_transition | True |
| missing_policy_ref | False | False | unresolved_evidence_policy_ref | True |
| provenance_output_mismatch | False | False | provenance_output_refs_mismatch | True |
| unresolved_issue_input_ref | False | False | unresolved_input_ref | True |
| validation_provenance_missing | False | False | unresolved_validation_provenance_ref | True |
