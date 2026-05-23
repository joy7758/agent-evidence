# Paper Skeleton

## Title

From Agent Telemetry to Portable Operation Evidence: A Minimal Adapter from
OpenTelemetry Agent Spans to EEOAP Evidence Objects

## Abstract

- State the distinction between runtime telemetry and portable operation
  evidence.
- Present the adapter as a bounded OpenTelemetry-to-EEOAP transformation path.
- Mention that the prototype emits an EEOAP-compatible statement and reuses the
  existing validator.
- Summarize the evaluation: one valid trace, four invalid traces, and full test
  suite execution.
- State the non-claims: no legal proof, no full runtime reconstruction, and no
  general compatibility claim.

## 1. Introduction

- Motivate why agent runtimes increasingly produce telemetry but still need
  portable evidence objects.
- Explain why a trace should not be treated as accountability evidence by
  default.
- Position EEOAP as the target operation accountability statement format.
- Introduce the adapter contribution and its deliberately narrow scope.
- Preview the artifact-first evaluation evidence.

## 2. Problem: Telemetry Is Not Portable Operation Evidence

- Define telemetry as operational observation material.
- Explain the gap between observability traces and reviewable evidence objects.
- Identify the missing pieces: reference closure, statement integrity, and
  validator-checkable structure.
- Use agent spans and tool spans as the concrete problem surface.
- State why simply logging more fields does not solve portability.

## 3. Background: OpenTelemetry Agent Spans and EEOAP Evidence Objects

- Summarize the OpenTelemetry-style GenAI agent span fields used by the
  prototype.
- Identify the fields consumed by the adapter: trace id, span id, parent span
  id, agent attributes, operation name, tool spans, timestamps, and error type.
- Summarize EEOAP v0.1 as a statement profile with actor, subject, operation,
  policy, provenance, evidence, and validation sections.
- Explain the existing validator stages: schema, references, consistency, and
  integrity.
- Keep this section descriptive and avoid claiming a new profile.

## 4. Mapping Model

- Map the trace id to the EEOAP subject and trace input reference.
- Map the agent span to actor, operation, provenance, and agent-span artifact.
- Map resolved `execute_tool` spans into evidence artifact entries.
- Preserve trace/span provenance through `otel://trace/.../span/...` locators.
- Treat `error.type` as a signal for operation result status, not output
  correctness.
- State the failure conditions used by the adapter.

## 5. Adapter Implementation

- Describe the local script path:
  `tools/opentelemetry_to_eeoap_adapter.py`.
- Explain the supported input shape: local OpenTelemetry-style JSON with
  `resourceSpans` or a top-level `spans` list.
- Describe the required agent span and `gen_ai.operation.name` checks.
- Explain parent-span closure and tool-span descendant checks.
- Explain the generated outputs under `generated/`.
- Emphasize that the EEOAP schema is unchanged.

## 6. Evaluation

- Report the valid fixture and generated EEOAP statement.
- Report the existing validator result: `ok=true`, `issue_count=0`.
- Present the invalid trace table and diagnostic codes.
- Report scoped pytest: `6 passed`.
- Report full pytest: `164 passed, 1 skipped, 15 warnings`.
- Disclose that full-repository ruff is blocked by unrelated pre-existing
  lint debt outside the adapter commit.

## 7. Threats to Validity

- The fixtures are local and minimal, not a broad OpenTelemetry implementation
  survey.
- The adapter checks structural and mapping conditions, not legal
  accountability.
- The generated EEOAP statement does not reconstruct the full runtime
  environment.
- The validator checks statement structure, references, consistency, and
  integrity, not agent output correctness.
- Cross-framework generality is not evaluated.

## 8. Related Work

- Discuss OpenTelemetry as an observability standard and source of runtime
  traces.
- Discuss EEOAP as the operation accountability evidence-object target.
- Distinguish this adapter from AEP and earlier EEOAP work.
- Discuss telemetry-to-evidence conversion as the specific contribution.
- Keep framework comparisons out of scope unless future artifacts are added.

## 9. Conclusion

- Restate that telemetry is not evidence by default.
- Summarize the minimal path from OpenTelemetry-style trace to EEOAP statement.
- Emphasize validator compatibility without schema changes.
- Summarize the valid and invalid fixture evidence.
- State the next step: expand fixtures only after preserving the narrow claim
  boundary.
