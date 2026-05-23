# OpenTelemetry-to-EEOAP Adapter: Transforming Agent Telemetry into Portable Operation Evidence

## Software Metadata Table Placeholder

| Field | Value |
|---|---|
| Current software version | TODO: assign release version before external submission. Internal placeholder: `otel-eeoap-adapter-v0.1.0-rc`. |
| Permanent link to reproducible capsule | TODO: create public release, archive, DOI, or immutable public commit reference before submission. |
| Legal software license | Apache-2.0, via repository root `LICENSE`. TODO: verify whether final SoftwareX package requires `LICENSE.txt`. |
| Code repository | TODO: set public repository release URL before external submission. Current local worktree: `/tmp/agent-evidence-softwarex-otel-eeoap-rc`. |
| Software code languages, tools, and services used | Python; local JSON fixtures; existing `agent-evidence` validator path; no external OpenTelemetry service. |
| Compilation requirements, operating environments, and dependencies | Python 3.11+; `click>=8.1`; `jsonschema>=4.23`; `pydantic>=2.7`; `pytest>=8.0` for scoped tests. TODO: confirm final operating-system statement. |
| Link to developer documentation/manual | TODO: add public link after release. Local docs are under `papers/opentelemetry-to-eeoap/`. |
| Support email for questions | TODO: confirm public support contact before submission. |

## Highlights

- Minimal adapter from OpenTelemetry-style agent traces to EEOAP-compatible operation accountability statements.
- Two valid trace contexts and four invalid diagnostic contexts exercise success and failure behavior.
- Generated statements pass the existing EEOAP validator with `ok=true` and `issue_count=0`.
- Reproducibility package includes tests, generated reports, clean-clone verification, checksums, and local metadata drafts.
- The package is research software, not a legal accountability system or broad OpenTelemetry compatibility claim.

## Abstract

Runtime telemetry improves observability, but it does not automatically produce portable operation evidence. A trace can record spans, attributes, timings, errors, and parent-child links, yet those records do not by themselves become an accountability statement that another party can validate. This article presents the OpenTelemetry-to-EEOAP Adapter, a small research-software package that transforms controlled OpenTelemetry-style agent traces into Execution Evidence and Operation Accountability Profile (EEOAP) compatible operation accountability statements.

The adapter reads a local trace JSON file, identifies the accountable agent operation span, extracts agent identity and operation metadata, resolves tool execution spans, checks span parentage, preserves trace/span provenance, emits an EEOAP-compatible statement, and routes the result into the existing EEOAP validator. The evaluation uses two valid trace contexts and four controlled invalid traces. Both valid generated statements pass the existing EEOAP validator with `ok=true` and `issue_count=0`; invalid traces expose diagnostics for missing agent span, unresolved tool span, broken parent relation, and missing operation name. The contribution is bounded: it does not claim legal accountability, production readiness, agent-output correctness, broad OpenTelemetry implementation compatibility, or a new EEOAP profile.

## Keywords

OpenTelemetry; EEOAP; agent telemetry; operation accountability; execution evidence; validation; reproducibility

## Motivation and Significance

Modern agent systems increasingly emit telemetry. Logs and traces can show which operation ran, which spans were involved, when execution occurred, and whether tool calls or errors appeared. This information is useful for debugging and observability, but it is not automatically portable operation evidence. A reviewer still needs a structured statement that identifies the accountable operation, preserves provenance, identifies evidence artifacts, and follows a known validation path.

EEOAP supplies a target evidence-object structure and validator for operation accountability statements. The key software problem is therefore not to replace OpenTelemetry or create a new EEOAP profile. The problem is to bridge selected telemetry signals into an existing evidence-object path without moving the target schema. If a trace can enter that path through a small adapter, then telemetry becomes a source for evidence construction rather than being treated as evidence by assertion.

The OpenTelemetry-to-EEOAP Adapter addresses that bridge. It treats an OpenTelemetry-style trace as input, checks whether the trace contains enough structure to support an accountable operation, and emits an EEOAP-compatible statement only when those checks pass. When the trace lacks a required accountable span, operation name, parent relation, or connected tool span, the adapter returns a bounded diagnostic instead of silently producing an evidence object.

This matters for software engineering artifact review because evidence-layer claims should be inspectable and reproducible. The package includes local fixtures, generated statements, adapter reports, scoped tests, checksum materials, clean-clone verification, and local metadata drafts. It gives researchers and reviewers a concrete baseline for discussing telemetry-to-evidence transformation. It also separates a narrow software contribution from broader claims about governance, legal accountability, or production deployment.

The significance is practical as well as conceptual. Many agent projects already produce some form of trace, callback log, span tree, or tool-call record. Those records are often useful to the original developer but hard to cite, transfer, or validate as a portable evidence object. The adapter package shows one conservative path: keep the telemetry source intact, derive a bounded operation statement, preserve links back to trace and span identifiers, and then submit the result to an existing evidence validator. This gives later integrations a concrete pattern to test rather than a broad governance claim to interpret.

The package also helps clarify what should remain outside a minimal software artifact. It does not attempt to reconstruct the full runtime, prove that an agent answer is correct, or certify that every OpenTelemetry implementation can be processed. Those goals would require additional runtime capture, policy, security, and empirical evaluation. The present software instead answers a smaller question: can a trace-like source be mapped into an evidence-object target in a way that is inspectable, reproducible, and validator-checked?

## Software Description

The software input is a local OpenTelemetry-style JSON trace fixture. The current fixture set lives under `examples/opentelemetry/` and includes two valid traces plus four invalid traces. The valid traces are synthetic and controlled. They are not production telemetry and do not claim broad OpenTelemetry implementation coverage. This bounded input design keeps the package reproducible while exposing the adapter behavior clearly.

The main implementation path is `tools/opentelemetry_to_eeoap_adapter.py`. For each input trace, the adapter parses spans and locates one accountable agent span. The selected span must expose agent identity and operation information, including fields aligned with `gen_ai.agent.id`, `gen_ai.agent.name`, `gen_ai.agent.version`, and `gen_ai.operation.name`. Missing agent context produces `missing_agent_span`; a missing operation name produces `missing_operation_name`.

After selecting the operation span, the adapter checks parent-child span relations. Any span that declares a parent must reference an existing parent span. Broken ancestry produces `broken_parent_span_relation`. The adapter then resolves tool execution spans. Tool spans are accepted as operation evidence only when they are reachable from the selected agent span through the parent chain. A tool span outside that operation ancestry produces `unresolved_tool_span`.

For successful inputs, the adapter preserves trace/span provenance and emits two generated artifacts under `generated/`: an EEOAP-compatible operation accountability statement and an adapter report. The statement records the operation, actor, telemetry subject, evidence entries, tool-span links, provenance locators, and integrity material required by the existing EEOAP path. The adapter report records extraction and validation context for review.

The adapter does more than copy fields. It selects the accountable operation, checks parent closure, resolves tool evidence by ancestry, preserves source locators, emits a target evidence object, and relies on the existing validator rather than an adapter-specific schema. The generated statements are validated through the existing EEOAP validator path, so success means the output entered the current profile-aware validation surface without changing the EEOAP schema.

Tests are located at `tests/test_opentelemetry_to_eeoap_adapter.py`. They cover conversion of both valid traces, validator acceptance when callable, and the four invalid diagnostic cases. The package does not require an external OpenTelemetry service, OpenTelemetry Collector, LangChain runtime, or network call.

The adapter outputs are intentionally file-based. This is useful for SoftwareX-style review because the source trace, generated statement, and adapter report can be inspected without a running service. The generated statement is the portable evidence-object candidate. The adapter report is the transformation record: it makes visible which input was processed, which operation span was selected, which tool spans were mapped, and whether validation succeeded. Keeping both artifacts makes the package easier to review and easier to extend.

The software is organized around the existing `agent-evidence` package rather than a separate service. The command-line validation path remains the existing EEOAP validator. This design keeps the adapter small and avoids creating a second validator that could drift from the profile. It also preserves the central claim boundary: OpenTelemetry-style telemetry is the source representation, EEOAP is the target representation, and the adapter is the transformation layer between them.

The fixture design is part of the software description. The two valid fixtures exercise successful statement generation, while the invalid fixtures define the failure vocabulary. This makes the test suite a compact executable specification for the adapter: positive cases must produce validator-ready statements; negative cases must fail at the expected diagnostic surface. That behavior is more important for the current package than throughput, distributed deployment, or runtime instrumentation breadth.

## Illustrative Example

The first valid fixture, `valid-agent-trace`, represents a `research.answer` operation. It contains a root agent span and two direct child tool spans. Running the adapter generates `generated/valid-agent-trace-eeoap-statement.json` and `generated/valid-agent-trace-adapter-report.json`. The generated statement passes the existing validator with `ok=true` and `issue_count=0`.

The second valid fixture, `valid-agent-workflow-trace`, represents a different operation pattern. Its root operation is `workflow.execute`. The trace contains a root agent span, one workflow invocation span, and two tool spans that are children of the workflow invocation rather than direct children of the agent span. This deeper parent-child pattern exercises tool-span resolution through an intermediate span. The generated statement, `generated/valid-agent-workflow-trace-eeoap-statement.json`, also passes the validator with `ok=true` and `issue_count=0`.

Four invalid fixtures define the controlled failure surface. `invalid-missing-agent-span` verifies that an accountable operation span is required. `invalid-unresolved-tool-span` verifies that tool spans must be structurally connected to the selected agent operation. `invalid-broken-parent-span` verifies that broken span ancestry prevents safe mapping. `invalid-missing-operation-name` verifies that an unnamed agent operation cannot become an operation accountability statement.

The main scoped evaluation uses:

```bash
pytest tests/test_opentelemetry_to_eeoap_adapter.py -q
```

The v0.7 evidence expansion recorded `8 passed in 2.48s`. Later maintenance checks in the isolated release-candidate branch continued to pass. This supports the package claim that two valid trace contexts and four invalid diagnostic contexts are reproducible in the repository. It does not support a claim about production traces, real framework integrations, or all OpenTelemetry implementations.

The illustrative workflow is therefore short but complete. A reviewer can start from a fixture, run the adapter, inspect the generated EEOAP statement, inspect the adapter report, and run the existing validator. The successful path demonstrates that telemetry can enter the evidence-object validator without changing the EEOAP schema. The failure path demonstrates that the adapter refuses selected malformed mappings. In SoftwareX terms, this is the key usage pattern: the package is a runnable reference implementation for a bounded telemetry-to-evidence bridge.

The second valid trace is particularly important for avoiding a single-shape demonstration. In the baseline case, both tools are direct children of the agent span. In the workflow case, the tools are descendants through an intermediate invocation span. This does not prove general workflow support, but it does show that the adapter is not hard-coded only to direct children. It can follow a deeper parent chain while preserving the same output target and validator.

## Impact

The package provides a reproducible bridge between observability telemetry and portable operation evidence. It shows how trace data can be treated as source material for a validator-ready evidence object, rather than as evidence by default. That distinction is useful for research on agent observability, provenance, audit trails, and evidence packaging.

For artifact evaluation, the package offers a small but inspectable testbed. Reviewers can inspect the input fixtures, generated statements, adapter reports, and validation results. Future work can replace or extend synthetic fixtures with real runtime traces while keeping the same evidence-object target and validator path. The current package therefore serves as a baseline for later LangChain, OpenTelemetry SDK, or collector-based integrations without claiming those integrations now.

The software is also useful as a design reference. It demonstrates that schema reuse is possible: the adapter did not require an EEOAP schema change. This keeps the evaluation focused on transformation quality and reproducibility rather than on redefining the target profile.

The expected users are researchers and engineers working near agent observability, provenance, evidence packaging, and reproducibility. For those users, the value is not that this adapter is large or production-ready. The value is that it provides an auditable minimal case with known inputs, known outputs, known failure modes, and a known validator. That makes it suitable as a seed artifact for future comparisons: raw trace versus evidence statement, synthetic fixture versus runtime fixture, or local adapter versus runtime-integrated exporter.

The package also supports incremental development. A later integration can add a real framework-derived trace only if it also adds a committed fixture, generated output, test, and validation result. This rule keeps future claims tied to artifacts. It prevents a common failure mode in evidence-tooling work, where broad claims about accountability or provenance outrun the actual validation surface.

## Limitations

The evaluation uses synthetic fixtures. They are useful for reproducibility and diagnostic clarity, but they do not prove behavior on production telemetry. Only two valid trace contexts are included, so the package does not claim broad empirical coverage.

The package does not include real LangChain runtime integration, OpenTelemetry Collector integration, CrewAI or AutoGen integration, or OpenTelemetry SDK-generated trace capture. It does not claim broad OpenTelemetry implementation compatibility. It demonstrates a bounded transformation over local OpenTelemetry-style fixtures.

Validator success is also limited. Passing the EEOAP validator means that generated statements satisfy the current profile-aware checks. It does not prove legal accountability, regulatory compliance, full runtime reconstruction, agent-output correctness, or production readiness. The adapter is not a new EEOAP profile.

Finally, release metadata remains in draft form. Local EEOAP and AEP artifact tags exist, but they have not been pushed or archived. No DOI or GitHub Release has been created for this OpenTelemetry-to-EEOAP package. Root repository metadata currently describes AEP-Media and was intentionally left unchanged.

These limitations are not accidental omissions; they define the current software boundary. The package is positioned as a SoftwareX candidate because it is a reusable, inspectable software artifact with a clear research-enabling purpose. It should not be submitted as evidence of field deployment, legal compliance, or end-to-end agent governance. Before formal submission, the release metadata, CFF validation, public availability statement, and final template formatting must be completed.

## Reproducibility and Artifact Availability

The frozen package path is `papers/opentelemetry-to-eeoap/frozen_v0_5/`. It contains freeze documentation, a manifest, checksum material, claim-boundary notes, evaluation summaries, reviewer positioning notes, clean-clone verification, and an external review brief. The release-candidate branch is `softwarex-otel-eeoap-release-candidate`.

Generated statements and adapter reports are committed under `generated/`. The two valid generated statements passed the existing EEOAP validator with `ok=true` and `issue_count=0`. Scoped tests are run with:

```bash
pytest tests/test_opentelemetry_to_eeoap_adapter.py -q
```

Local metadata drafts are under `papers/opentelemetry-to-eeoap/softwarex_metadata_drafts_v1_8/`. CodeMeta JSON validation passed in v1.8; CFF YAML validation was skipped because PyYAML was unavailable and remains a release-preparation TODO.

This artifact availability statement is draft only. DOI creation, GitHub Release creation, public tag push, final release URL, and final SoftwareX availability wording remain TODO before formal submission.

The current isolated branch exists to avoid contaminating release preparation with unrelated dirty worktree changes. Earlier clean-clone and checksum verification materials are preserved in the paper package. Before any public release, the same checks should be rerun against the final release candidate, and the availability statement should point to public, stable identifiers rather than local worktree paths.

## Declarations

### Generative AI and AI-Assisted Technologies Disclosure

OpenAI ChatGPT/Codex was used for planning, drafting, code scaffolding, documentation structuring, local command execution support, and review support. The human author remains responsible for the content, code, claims, artifacts, citations, limitations, and conclusions. The AI system is not an author. TODO: adapt this wording to the target venue policy before submission.

### Conflict of Interest

TODO: confirm final wording before submission. Draft statement: the author declares no known competing financial interests or personal relationships that could have appeared to influence the work reported in this paper.

### Funding

TODO: confirm final wording before submission. Draft statement: this research received no specific grant from any funding agency in the public, commercial, or not-for-profit sectors.

### Data Availability

No human subject data, patient data, private production telemetry, or private operational logs are used. Fixtures are synthetic OpenTelemetry-style trace JSON files stored in `examples/opentelemetry/`. Generated statements and reports are stored in `generated/`. TODO: update after public release or archive.

### Artifact Availability

Artifacts are currently local to the repository and release-candidate branch. Local EEOAP/AEP tags exist but are not pushed or archived. No DOI or GitHub Release has been created. TODO: replace this draft with the final public artifact availability statement before submission.

## References

- [OpenTelemetry-GenAI] OpenTelemetry. `Semantic conventions for generative AI systems`. Official OpenTelemetry semantic conventions documentation. Accessed 2026-05-23. URL: <https://opentelemetry.io/docs/specs/semconv/gen-ai/>. TODO: verify status immediately before submission.

- [OpenTelemetry-Agent-Spans] OpenTelemetry. `Semantic Conventions for GenAI agent and framework spans`. Official OpenTelemetry semantic conventions documentation. Accessed 2026-05-23. URL: <https://opentelemetry.io/docs/specs/semconv/gen-ai/gen-ai-agent-spans/>. TODO: verify field list immediately before submission.

- [JSON-Schema-2020-12] Wright, Austin; Andrews, Henry; Hutton, Ben; Dennis, Greg. `JSON Schema Draft 2020-12`. Published 2022-06-16. URL: <https://json-schema.org/draft/2020-12>. TODO: adapt format to the selected venue.

- [W3C-PROV] Lebo, Timothy; Sahoo, Satya; McGuinness, Deborah. `PROV-O: The PROV Ontology`. W3C Recommendation, 2013-04-30. URL: <https://www.w3.org/TR/prov-o/>. TODO: decide final provenance references.

- [EEOAP-Artifact] `agent-evidence` repository. Execution Evidence and Operation Accountability Profile artifacts and OpenTelemetry-to-EEOAP adapter materials. TODO: replace with immutable release, archive, tag, or DOI before external submission.

- [AEP-Artifact] `agent-evidence` repository. AEP-related evidence artifact materials used for positioning. TODO: identify exact public artifact, commit, release, archive, or DOI before external submission.

- [ACM-Artifact-Badging] Association for Computing Machinery. `Artifact Review and Badging - Current`. ACM Publications Policy. Accessed 2026-05-23. URL: <https://www.acm.org/publications/policies/artifact-review-and-badging-current>. TODO: re-check wording before submission.
