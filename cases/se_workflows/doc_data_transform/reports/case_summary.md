# Documentation / data transformation operation

| Variant | Expected | Observed | Primary code | Match |
|---|---|---|---|---|
| valid_doc_metadata | True | True | None | True |
| digest_mismatch | False | False | statement_digest_mismatch | True |
| missing_policy_link | False | False | unresolved_evidence_policy_ref | True |
| provenance_mismatch | False | False | provenance_output_refs_mismatch | True |
| stale_source_hash | False | False | stale_source_digest | True |
| wrong_derived_output_ref | False | False | provenance_output_refs_mismatch | True |
