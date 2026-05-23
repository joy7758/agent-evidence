# Comparison Framework

This comparison frames logs, traces, provenance records, EEOAP statements, and
the adapter path as different capability holders. It does not dismiss logs,
traces, or provenance as useless. Each representation captures part of the
evidence problem.

| Representation | What it captures | What it misses | Whether it is portable | Whether it has validation path | Role in this paper |
|---|---|---|---|---|---|
| Raw logs | Human-readable runtime events, messages, warnings, and errors. | Stable operation boundary, structured provenance, typed evidence references, and profile-aware validation. | Sometimes, but usually depends on local format and context. | Usually no standard profile validation. | Baseline operational record that may support debugging but is not the target evidence object. |
| Raw OpenTelemetry trace | Structured spans, trace ids, span ids, parent links, attributes, timestamps, and error signals. | Explicit EEOAP actor/subject/operation structure, policy references, evidence artifacts, integrity fields, and validator result. | More portable than local logs, but still telemetry-oriented and exporter/semantic-convention dependent. | OpenTelemetry tooling can process traces, but not as an EEOAP operation accountability statement. | Source-side representation used by the adapter. |
| Provenance-only record | Relationships among actors, activities, entities, and derivations. | Telemetry-specific span extraction, EEOAP-specific operation accountability structure, and repository validator integration. | Often portable if expressed with a standard model. | Depends on the provenance format and validator used. | Related conceptual neighbor for explaining why provenance links matter. |
| EEOAP statement | Actor, subject, operation, policy, constraints, provenance, evidence references, artifacts, integrity, and validation metadata. | Raw runtime breadth and all original telemetry context unless included by reference or artifact locator. | Yes, within the EEOAP profile and validator assumptions. | Yes, through existing EEOAP schema/reference/consistency/integrity validation. | Target evidence object produced by the adapter. |
| OpenTelemetry-to-EEOAP adapter path | Transformation from selected spans into an EEOAP-compatible statement, including parent closure, tool-span resolution, provenance locators, artifacts, integrity recomputation, and validator routing. | Broad OpenTelemetry compatibility, full runtime reconstruction, legal accountability, production readiness, and output correctness. | Yes for committed fixtures and generated statements. | Yes, because the output is routed into the existing EEOAP validator. | Main contribution of this package and the proposed journal method. |

The journal version should use this framing to avoid a false competition
between telemetry and evidence. The claim is not that traces are weak or that
EEOAP replaces observability. The claim is that trace data must be transformed
and validated before it becomes portable operation evidence under EEOAP.
