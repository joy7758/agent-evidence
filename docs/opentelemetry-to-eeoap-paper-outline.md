# OpenTelemetry to EEOAP Paper Outline

This is an outline only. The implementation target is the adapter prototype,
fixtures, and validator path.

## Working Claim

OpenTelemetry traces are telemetry, not evidence by themselves. A bounded
adapter can transform selected GenAI agent spans and tool-call spans into a
portable EEOAP operation evidence statement that can be validated offline.

## Outline

1. Problem statement
   - Agent runtimes increasingly emit structured telemetry.
   - Telemetry is runtime-observability material, not automatically portable
     operation evidence.

2. Boundary
   - Reuse EEOAP v0.1.
   - Do not introduce a new profile.
   - Keep conversion local and reproducible.

3. Adapter method
   - Locate one GenAI agent span.
   - Require `gen_ai.operation.name`.
   - Resolve `execute_tool` spans through parent span links.
   - Preserve trace and span provenance through EEOAP references and artifacts.

4. Validation
   - Run the generated statement through `agent-evidence validate-profile`.
   - Report adapter diagnostics separately from EEOAP validator diagnostics.

5. Evaluation fixtures
   - valid agent trace
   - missing agent span
   - unresolved tool span
   - broken parent span relation
   - missing operation name

6. Non-claims
   - No legal accountability proof.
   - No full runtime reconstruction.
   - No universal OpenTelemetry compatibility claim.
   - No output correctness proof.

7. Next work
   - Add more runtime fixture variants.
   - Compare OpenTelemetry exporter shapes.
   - Keep schema changes out unless a concrete incompatibility is proven.
