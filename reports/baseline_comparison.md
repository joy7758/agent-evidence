# Baseline Comparison

| Baseline | Detects | Misses | Missed invalid variants | Safe claim |
|---|---|---|---|---|
| schema-only | JSON structural violations. | Relation, policy/evidence, provenance/output, validation/provenance, digest, and case-semantic failures. | 15 | Schema-only validation is insufficient for relation-level operation-accountability review. |
| log-only | Presence of a fixture operation event. | Policy/evidence linkage, output/provenance closure, validation closure, and integrity. | 15 | Logs are useful event evidence but do not close the accountability boundary. |
| policy-only | Local policy rule mismatches represented in the policy file. | Evidence, provenance, output closure, and digest failures. | 13 | Policy-only review is partial and does not prove operation evidence closure. |
