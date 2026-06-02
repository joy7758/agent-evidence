# Formal Model Alignment For SE Case Prototype

| Formal item | Fixture field | Statement field | Validator/checker rule | Report evidence |
|---|---|---|---|---|
| operation object | `operation_id`, `operation_type` | `operation` | schema/profile and case runner | per-case report |
| actor | `actor` | `actor` | reference closure through provenance actor ref | profile report |
| subject | `subject`, `payloads.input` | `subject`, `operation.subject_ref` | local reference closure | profile report |
| policy | `policy_payload` | `policy`, `operation.policy_ref` | policy/evidence linkage | baseline and profile report |
| constraint | `policy_payload.description` | `constraints` | schema/profile plus case adapter | report summary |
| input/output refs | `input_refs`, `output_refs` | `operation`, `evidence.references` | local closure and provenance/output consistency | profile report |
| evidence | `evidence_payload` | `evidence` | policy/evidence and integrity checks | profile report |
| provenance relation | `provenance_payload` | `provenance` | provenance/output consistency | profile report |
| validation relation | `validation_refs` | `validation` | validation/provenance closure | profile report |
| integrity material | `integrity_refs` | `evidence.integrity` | digest recomputation | profile report |
| statement | generated statement JSON | whole profile object | core validator | statement and report files |
| report | generated report JSON | output report | runner contract | per-case JSON |
| diagnostic totality | expected primary code | `primary_error_code` | tie-breaking order | diagnostic match field |

Remaining gap: this alignment is an implementation note, not a formal proof.
