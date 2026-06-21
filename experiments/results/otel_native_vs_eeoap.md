# OpenTelemetry Native vs EEOAP Baseline Comparison

Affected clauses: EEOAP-001, EEOAP-002, EEOAP-003, EEOAP-004, EEOAP-005.

Feature-coverage comparison across identical input traces.
The comparison is local and descriptive, not an external benchmark.

Fairness constraints:

- All comparisons use the identical input trace:
  `data/otel/raw_demo_trace.json`.
- No preprocessing differences are allowed before comparison.
- Only the output representation differs across rows.

| System | Preserves trace identity | Binds policy/constraints | Binds provenance | Includes evidence references | Validator-readable output | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| Baseline A: raw OpenTelemetry trace storage | yes | no | no | no | no | Preserves OTLP trace payload but does not bind policy, provenance, evidence references, or local validator output. |
| Baseline B: OpenTelemetry trace plus JSON export only | yes | no | no | no | no | Portable JSON improves transport but remains observability-oriented rather than operation-accountability-oriented. |
| System: OpenTelemetry to EEOAP conversion | yes | yes | yes | yes | yes | Adds operation, policy, provenance, evidence references, integrity digests, and local validator-readable output. |

Boundary: the comparison identifies local review surfaces. It does not
claim legal sufficiency, external certification, deployment robustness,
official standard adoption, or publication status.
