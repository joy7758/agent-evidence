# Journal Claim Boundary

## Allowed Claims

- Telemetry-to-evidence transformation can be implemented as a bounded
  adapter.
- OpenTelemetry-style agent spans can be mapped into EEOAP-compatible
  operation accountability statements under controlled fixtures.
- The existing EEOAP validator can check generated statements without schema
  changes.
- Controlled invalid traces expose meaningful diagnostic surfaces.
- Clean-clone verification supports artifact reproducibility.

## Disallowed Claims

- legal accountability proof
- full runtime reconstruction
- general OpenTelemetry implementation compatibility
- cross-framework generality
- agent-output correctness
- production readiness
- new EEOAP profile
- complete agent governance framework
- regulatory compliance

## Claim Upgrade Rule

No claim may be upgraded unless there is a corresponding committed fixture,
test, generated output, and validation result.

For example, a second valid trace may support a claim of a second controlled
operation context only after the fixture, generated statement, adapter report,
test coverage, and validator result are committed. It must not be used to
claim broad runtime, framework, or OpenTelemetry implementation compatibility.
