# OpenTelemetry to EEOAP Claim Boundary

This adapter demonstrates a bounded transformation from one local
OpenTelemetry-style GenAI trace JSON file into one EEOAP v0.1 operation
accountability statement.

It does not define a new EEOAP profile, does not rename EEOAP, and does not
change the existing EEOAP schema.

## Non-Claims

- This adapter does not prove legal accountability.
- This adapter does not reconstruct the full runtime environment.
- This adapter does not claim all OpenTelemetry implementations are compatible.
- This adapter does not prove agent output correctness.
- This adapter only demonstrates a bounded transformation from agent telemetry to portable operation evidence.

## Local Scope

The adapter is local-only:

- no network calls
- no external OpenTelemetry collector
- no hosted service
- no runtime attestation
- no legal non-repudiation claim

The validator checks that the generated EEOAP statement is structurally
complete, internally consistent, and integrity-linked under the current
repository schema.
