# Evaluation Table

Affected clauses: EEOAP-001, EEOAP-002, EEOAP-003, EEOAP-004, EEOAP-005.

| Experiment | Source | Span count | Validator ok | Issue count | Output |
| --- | --- | ---: | --- | ---: | --- |
| exp1_synthetic | synthetic_fixture | 2 | True | 0 | `experiments/results/exp1_synthetic_evidence.json` |
| exp2_real_trace | public_opentelemetry_proto_example | 1 | True | 0 | `data/eeoap/real_trace_evidence.json` |
| exp3_noisy_recovery | public_opentelemetry_proto_example_with_non_semantic_noise | 1 | True | 0 | `experiments/results/exp3_noisy_recovery_evidence.json` |
| exp4_determinism_oracle | determinism_oracle | 1 | True | 0 | `data/eeoap/real_trace_evidence.json` |

Boundary: these are local experiment receipts. They do not claim external
validation, certification, production deployment, publication status, or
legal non-repudiation.
