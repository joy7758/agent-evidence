# Title

OpenTelemetry-to-EEOAP Adapter: Transforming Agent Telemetry into Portable Operation Evidence

# Authors

Bin Zhang

ORCID: `https://orcid.org/0009-0002-8861-1481`

Affiliation: TODO: confirm public affiliation before external submission.

Email: TODO: confirm support/contact email before external submission.

# Software metadata table

| Field | Value |
|---|---|
| Current software version | TODO: assign release version before external submission. Draft label: `otel-eeoap-adapter-v0.1.0-rc`. |
| Permanent link to reproducible capsule | TODO: create public release, archive, DOI, or immutable public commit reference before formal submission. |
| Legal software license | Apache-2.0 via root `LICENSE`. TODO: confirm whether final SoftwareX package needs `LICENSE.txt`. |
| Code repository | TODO: set public release URL. Current readiness work is local to the release-candidate branch. |
| Software code languages, tools, and services used | Python; JSON fixtures; local `agent-evidence` CLI validator path; no external OpenTelemetry service. |
| Compilation requirements, operating environments, and dependencies | Python 3.11+; `click`, `jsonschema`, `pydantic`; `pytest` for scoped tests. TODO: confirm final operating-system statement. |
| If available, link to developer documentation/manual | Local docs under `papers/opentelemetry-to-eeoap/`; TODO: add public link after release. |
| Support email for questions | TODO: confirm public support contact before submission. |

Local OpenTelemetry-to-EEOAP metadata drafts exist under
`papers/opentelemetry-to-eeoap/softwarex_metadata_drafts_v1_8/`. They are draft
support only. Final public release metadata is pending. The root `CITATION.cff`
and root `codemeta.json` currently describe AEP-Media and are not used as final
OpenTelemetry-to-EEOAP release metadata.

# Highlights

- Converts OpenTelemetry-style agent trace fixtures into EEOAP-compatible operation accountability statements.
- Provides two valid trace contexts, four invalid diagnostics, generated reports, and scoped tests.
- Valid generated statements pass the existing EEOAP validator without changing the EEOAP schema.
- Documents release-readiness boundaries, including draft metadata, local tags, and public-release TODOs.

# Abstract

Runtime telemetry helps developers observe agent execution, but trace records do not automatically become portable operation evidence. The OpenTelemetry-to-EEOAP Adapter is a small research-software package that converts controlled OpenTelemetry-style agent trace fixtures into Execution Evidence and Operation Accountability Profile (EEOAP) compatible operation accountability statements. The package includes adapter code, valid and invalid fixtures, generated statements, adapter reports, scoped tests, metadata drafts, and SoftwareX preparation documentation.

The adapter reads one trace JSON file, selects the accountable agent span, extracts agent and operation metadata, resolves tool execution spans, checks parent-child span relations, preserves trace/span provenance, emits an EEOAP-compatible statement, and routes the output to the existing EEOAP validator. The evaluation includes two valid trace contexts and four invalid diagnostic contexts. Both valid generated statements pass the existing validator with `ok=true` and `issue_count=0`. Invalid fixtures expose bounded diagnostics for missing agent span, unresolved tool span, broken parent relation, and missing operation name. The package does not claim legal accountability, production readiness, real runtime integration, broad OpenTelemetry compatibility, agent-output correctness, or a new EEOAP profile. Public release identifiers, DOI, GitHub Release, and pushed tags remain TODO before formal submission.

# Keywords

OpenTelemetry; EEOAP; agent telemetry; operation accountability; execution evidence; validation; reproducibility

# 1. Motivation and significance

Agent applications often produce traces, callback logs, span trees, or tool-call records. These records are useful to developers, but they are not automatically portable evidence objects. A reviewer needs more than a trace viewer: they need a structured operation statement, evidence entries, provenance links, integrity material, and a validator path.

This package provides a small executable bridge between those layers. It treats OpenTelemetry-style telemetry as the source representation and EEOAP as the target evidence representation. The adapter does not define a new profile or move the validator target. It shows how a bounded trace fixture can be mapped into an existing EEOAP-compatible statement and then checked by the existing validator.

The software contribution is practical. A reviewer can inspect a fixture, run the adapter, inspect the generated EEOAP statement and adapter report, and rerun the scoped tests. The package is useful as a reference artifact for researchers working on agent observability, provenance, evidence packaging, and reproducible audit trails. It also gives future integrations a baseline: any real runtime fixture can be added later only if it brings committed input, generated output, tests, and validation results.

# 2. Software description

The main adapter is `tools/opentelemetry_to_eeoap_adapter.py`. Broader package code and validator support live under `agent_evidence/`. The adapter consumes local OpenTelemetry-style JSON trace fixtures and writes two review artifacts for successful inputs: an EEOAP-compatible statement and an adapter report under `generated/`. The statement is the portable evidence-object candidate. The report records what the adapter selected, extracted, mapped, and validated.

Inputs are stored under `examples/opentelemetry/`. The current set contains two valid fixtures and four invalid fixtures. The valid fixtures are `valid-agent-trace.json` and `valid-agent-workflow-trace.json`. The invalid fixtures cover missing agent span, unresolved tool span, broken parent span relation, and missing operation name.

The adapter behavior has six core steps. First, it parses trace spans and selects one accountable agent span. Second, it extracts agent identity and operation metadata, including agent id, agent name, agent version, and operation name. Third, it checks parent-child span consistency so that referenced parent spans exist. Fourth, it resolves tool execution spans only when they are reachable from the selected agent operation. Fifth, it preserves source provenance through trace ids, span ids, timestamps, and artifact locators. Sixth, it emits an EEOAP-compatible statement and uses the existing EEOAP validator path.

The failure behavior is also part of the software interface. If no accountable agent span is available, the adapter reports `missing_agent_span`. If a tool span is outside the selected operation ancestry, it reports `unresolved_tool_span`. If a span references a missing parent, it reports `broken_parent_span_relation`. If the selected agent span lacks an operation name, it reports `missing_operation_name`. The adapter does not silently convert these traces into evidence statements.

The tests are in `tests/test_opentelemetry_to_eeoap_adapter.py`. They check both valid conversions, validator acceptance when the validator is callable, and all four invalid diagnostics. The adapter does not require network calls, a remote OpenTelemetry service, OpenTelemetry Collector, or LangChain runtime integration.

The file layout is explicit but not yet SoftwareX-final. The adapter source is under `tools/`, broader package source is under `agent_evidence/`, examples are under `examples/opentelemetry/`, generated review artifacts are under `generated/`, and scoped tests are under `tests/`. There is no `repo/src` layout in this draft. That absence is a known packaging issue, not a runtime test failure. No source layout rewrite is performed here.

The adapter does not modify the EEOAP schema. It relies on the existing EEOAP validator to check generated statements through the profile-aware path.

# 3. Illustrative example

The baseline valid fixture, `valid-agent-trace`, represents a `research.answer` operation with one root agent span and two direct child tool spans. Running the adapter produces `generated/valid-agent-trace-eeoap-statement.json` and `generated/valid-agent-trace-adapter-report.json`. The generated statement passes the existing EEOAP validator with `ok=true` and `issue_count=0`.

The second valid fixture, `valid-agent-workflow-trace`, represents `workflow.execute`. It contains a root agent span, an intermediate workflow invocation span, and two tool spans below that invocation. This tests a deeper parent-child pattern than the baseline fixture. Its generated statement also passes the validator with `ok=true` and `issue_count=0`.

The review workflow is:

```bash
python tools/opentelemetry_to_eeoap_adapter.py examples/opentelemetry/valid-agent-trace.json
agent-evidence validate-profile generated/valid-agent-trace-eeoap-statement.json
python tools/opentelemetry_to_eeoap_adapter.py examples/opentelemetry/valid-agent-workflow-trace.json
agent-evidence validate-profile generated/valid-agent-workflow-trace-eeoap-statement.json
pytest tests/test_opentelemetry_to_eeoap_adapter.py -q
```

The committed evaluation records two validator-passing valid statements and four diagnostic-preserving invalid fixtures. The invalid diagnostics are `missing_agent_span`, `unresolved_tool_span`, `broken_parent_span_relation`, and `missing_operation_name`. The version 0.7 evidence expansion recorded `8 passed in 2.48s`; later release-candidate maintenance checks continued to pass. This supports the package's bounded software claim. It does not support claims about production traces, all OpenTelemetry implementations, or real framework integrations.

# 4. Impact

The adapter makes a narrow but reusable contribution: it shows how trace-like telemetry can become a validator-ready evidence object through a small, inspectable transformation package. That is useful for artifact evaluation because reviewers can inspect the source traces, generated statements, reports, and tests without depending on a live telemetry service.

The package gives future work a concrete baseline. A later LangChain-derived fixture, OpenTelemetry SDK fixture, or collector-based integration can be compared against the same target: EEOAP-compatible statements checked by the existing validator. This keeps future claims tied to committed artifacts rather than to broad accountability language.

For evidence-layer research, the package clarifies what EEOAP adds beyond raw telemetry: a structured operation statement, evidence entries, provenance links, integrity material, and a profile-aware validation result. For software engineers, it provides a minimal reference for building adapters that preserve provenance and fail clearly when telemetry cannot support an evidence claim.

# 5. Limitations

The fixtures are synthetic. They make the package reproducible and easy to inspect, but they do not prove behavior on production telemetry. Only two valid trace contexts are included, so the evaluation remains intentionally small.

The package does not include real LangChain runtime integration, OpenTelemetry Collector integration, OpenTelemetry SDK-generated trace capture, CrewAI integration, or AutoGen integration. It does not claim broad OpenTelemetry implementation compatibility.

Validator success is limited to EEOAP profile checks. It does not prove legal accountability, regulatory compliance, full runtime reconstruction, production readiness, or agent-output correctness. The adapter is not a new EEOAP profile and does not change the EEOAP schema.

Release readiness is incomplete. Root `CITATION.cff` and `codemeta.json` currently describe AEP-Media, not OpenTelemetry-to-EEOAP. Local metadata drafts exist, but they are not final public release metadata. Local tags exist but are not pushed or archived. No DOI or GitHub Release exists for this package. CFF YAML validation remains TODO. The repository layout also remains unchanged: the adapter lives under `tools/`, not `repo/src`.

# 6. Reproducibility and artifact availability

The release-candidate branch is `softwarex-otel-eeoap-release-candidate`. Generated statements and adapter reports are committed repository artifacts under `generated/`. The valid statement paths are `generated/valid-agent-trace-eeoap-statement.json` and `generated/valid-agent-workflow-trace-eeoap-statement.json`. Adapter reports use matching `-adapter-report.json` names. Scoped tests are run with:

```bash
pytest tests/test_opentelemetry_to_eeoap_adapter.py -q
```

The version 0.5 frozen package under `papers/opentelemetry-to-eeoap/frozen_v0_5/` is a historical internal freeze with clean-clone verification, checksum verification, claim boundaries, reviewer notes, and an external review brief. It predates the version 0.7 second valid trace and should not be presented as the complete final SoftwareX package.

The release-candidate branch contains the second valid trace and later SoftwareX route, metadata, article, and readiness materials. Local metadata drafts are under `papers/opentelemetry-to-eeoap/softwarex_metadata_drafts_v1_8/`. Local EEOAP/AEP artifact tags exist, but they are not pushed or archived. DOI creation, GitHub Release creation, public tag push, final release URL, final artifact availability wording, final checksums, and final clean-clone verification remain TODO before formal submission.

Before submission, the local artifact set must become a public, stable release surface. The likely forward path is a release-candidate support package derived from this branch, not the historical version 0.5 frozen package alone.

# 7. Declarations

## Generative AI and AI-assisted technologies

OpenAI ChatGPT/Codex was used for planning, drafting, code scaffolding, documentation structuring, local command execution support, and review support. The human author remains responsible for the content, code, claims, artifacts, citations, limitations, and conclusions. The AI system is not an author. TODO: adapt this wording to the target venue policy before submission.

## Conflict of interest

TODO: confirm final wording before submission. Draft statement: the author declares no known competing financial interests or personal relationships that could have appeared to influence the work reported in this paper.

## Funding

TODO: confirm final wording before submission. Draft statement: this research received no specific grant from any funding agency in the public, commercial, or not-for-profit sectors.

## Data availability

No human subject data, patient data, private production telemetry, or private operational logs are used. Fixtures are synthetic OpenTelemetry-style trace JSON files under `examples/opentelemetry/`. Generated statements and adapter reports are under `generated/`. TODO: update after public release or archive.

## Artifact availability

Artifacts are currently local to the repository and release-candidate branch. Local EEOAP/AEP tags exist but are not pushed or archived. No DOI or GitHub Release has been created. The version 0.5 frozen package is historical support material, not the final SoftwareX release package. TODO: replace this draft with the final public artifact availability statement before submission.

# References

- [OpenTelemetry-GenAI] OpenTelemetry. `Semantic conventions for generative AI systems`. Official OpenTelemetry semantic conventions documentation. Accessed 2026-05-23. URL: <https://opentelemetry.io/docs/specs/semconv/gen-ai/>. TODO: verify status immediately before submission.

- [OpenTelemetry-Agent-Spans] OpenTelemetry. `Semantic Conventions for GenAI agent and framework spans`. Official OpenTelemetry semantic conventions documentation. Accessed 2026-05-23. URL: <https://opentelemetry.io/docs/specs/semconv/gen-ai/gen-ai-agent-spans/>. TODO: verify field list immediately before submission.

- [JSON-Schema-2020-12] Wright, Austin; Andrews, Henry; Hutton, Ben; Dennis, Greg. `JSON Schema Draft 2020-12`. Published 2022-06-16. URL: <https://json-schema.org/draft/2020-12>. TODO: adapt format to the selected venue.

- [W3C-PROV] Lebo, Timothy; Sahoo, Satya; McGuinness, Deborah. `PROV-O: The PROV Ontology`. W3C Recommendation, 2013-04-30. URL: <https://www.w3.org/TR/prov-o/>. TODO: decide final provenance references.

- [EEOAP-Artifact] `agent-evidence` repository. Execution Evidence and Operation Accountability Profile artifacts and OpenTelemetry-to-EEOAP adapter materials. TODO: replace with immutable release, archive, tag, or DOI before external submission.

- [AEP-Artifact] `agent-evidence` repository. AEP-related evidence artifact materials used for positioning. TODO: identify exact public artifact, commit, release, archive, or DOI before external submission.

- [ACM-Artifact-Badging] Association for Computing Machinery. `Artifact Review and Badging - Current`. ACM Publications Policy. Accessed 2026-05-23. URL: <https://www.acm.org/publications/policies/artifact-review-and-badging-current>. TODO: re-check wording before submission.
