# From Agent Telemetry to Portable Operation Evidence: A Minimal Adapter from OpenTelemetry Agent Spans to EEOAP Evidence Objects

## 1. Abstract

Runtime telemetry improves observability, but it does not automatically
produce portable operation evidence. An OpenTelemetry-style trace can describe
span timing, attributes, parent links, and errors, yet those fields do not by
themselves define an accountability statement that can be transferred and
validated by another party. This paper presents a bounded software engineering
method for transforming OpenTelemetry-style agent telemetry into Execution
Evidence and Operation Accountability Profile (EEOAP) compatible operation
accountability statements.

The method is implemented as a minimal local adapter. The adapter reads a trace
JSON file, identifies the accountable agent operation span, preserves trace and
span provenance, resolves tool execution spans, checks parent-child span
relationships, emits an EEOAP-compatible statement, and routes the output into
the existing EEOAP validator without modifying the EEOAP schema. The evaluation
uses two controlled valid trace contexts and four controlled invalid traces.
Both valid generated statements pass the existing validator with `ok=true` and
`issue_count=0` across the `schema`, `references`, `consistency`, and
`integrity` stages. The invalid traces expose bounded diagnostics for missing
agent spans, unresolved tool spans, broken parent-span relations, and missing
operation names.

The contribution is intentionally narrow. The paper does not claim legal
accountability, full runtime reconstruction, production readiness,
cross-framework generality, agent-output correctness, a new EEOAP profile, or
broad OpenTelemetry implementation compatibility.

## 2. Introduction

Agent systems increasingly emit runtime telemetry. Traces can show which
operation ran, when spans started and ended, which tool spans were involved,
and how spans were connected. This information is valuable for observability,
debugging, and operational analysis. It is not, however, automatically a
portable evidence object. A raw trace usually lacks the profile-aware structure,
evidence references, integrity fields, and validation path expected from an
operation accountability statement.

This paper studies the narrower problem of telemetry-to-evidence
transformation. The question is not whether OpenTelemetry replaces evidence
profiles, and not whether EEOAP should be redefined. The question is whether an
OpenTelemetry-style agent trace can be transformed into an EEOAP-compatible
operation accountability statement using a bounded adapter and the existing
validator path.

The paper's thesis is that this transformation can be implemented as a small
software engineering method. The adapter interprets selected telemetry fields,
checks structural preconditions, preserves provenance links, emits a target
evidence object, and submits the result to the existing EEOAP validator. The
scope is local and reproducible: fixtures, generated outputs, adapter reports,
tests, and frozen-package materials are all kept in the repository.

The paper makes exactly four contributions:

C1. A bounded telemetry-to-evidence mapping model.

C2. A minimal adapter implementation from OpenTelemetry-style agent spans to
EEOAP-compatible statements.

C3. A controlled evaluation with two valid trace contexts and four invalid
diagnostic contexts.

C4. A reproducibility package with generated statements, adapter reports,
scoped tests, checksum verification, clean-clone verification, and external
review notes.

The current draft is a submission candidate for external pre-review and
journal-route preparation. It is not venue-formatted and has not been formally
submitted.

## 3. Problem: Telemetry Is Not Portable Operation Evidence

Telemetry and operation evidence have related but different responsibilities.
Telemetry records runtime signals. It can capture spans, attributes, parent
links, timestamps, errors, and tool calls. These records are useful because they
preserve operational detail close to execution time. A trace is therefore a
strong candidate source for evidence construction.

Portable operation evidence requires an additional layer. Another party needs
to know which operation is being asserted, which actor and subject are
identified, which evidence artifacts support the assertion, how provenance is
preserved, and whether the object passes a known validation path. Raw telemetry
does not automatically answer those questions. It may be incomplete, may
contain spans that are unrelated to the accountable operation, or may contain
tool spans whose parentage is inconsistent with the selected agent operation.

The adapter therefore treats telemetry as a source representation, not as
evidence by definition. Valid telemetry is converted into an EEOAP-compatible
statement only after the adapter identifies an agent operation span, verifies
parent closure, resolves tool spans under that operation, preserves trace and
span locators, and constructs the target evidence object. Invalid telemetry
does not produce an operation accountability statement; it produces an adapter
report with a bounded diagnostic.

This distinction is the central claim boundary. The paper does not argue that
OpenTelemetry traces are inadequate or that provenance records are unnecessary.
Logs, traces, provenance records, and evidence objects each hold partial
capabilities. The contribution is the adapter path that makes the transition
from telemetry to profile-aware operation evidence explicit and testable.

## 4. Background

### 4.1 OpenTelemetry Agent Spans

OpenTelemetry provides a broadly used observability model for traces, metrics,
and logs. Its Generative AI semantic conventions include an agent and framework
span area [OpenTelemetry-GenAI]. The agent-span documentation records
attributes relevant to this adapter's mapping surface, including agent
identity, operation name, timestamps, span identifiers, parent span
relationships, and error attributes [OpenTelemetry-Agent-Spans].

This paper uses OpenTelemetry-style local JSON fixtures. The fixtures are not
claimed to be production telemetry and are not claimed to represent all
OpenTelemetry implementations. They are controlled trace contexts used to test
a bounded mapping from selected agent-span information to an EEOAP-compatible
statement.

The OpenTelemetry references are official but evolving. The v0.9 citation
verification records the GenAI semantic convention material as verified against
official OpenTelemetry documentation, while also marking it as time-sensitive
because the semantic conventions can change before final submission.

### 4.2 EEOAP Evidence Objects

EEOAP supplies the target evidence object and validation path
[EEOAP-Artifact]. In this repository, an EEOAP-compatible operation
accountability statement contains structured sections for actor, subject,
operation, policy, constraints, evidence artifacts, provenance, integrity, and
validation metadata. The existing validator checks schema conformance,
reference closure, consistency, and integrity.

The adapter does not create a new EEOAP profile. It does not modify the EEOAP
schema. That design choice is important because validator success is meaningful
only if the adapter enters the existing evidence-object path rather than moving
the target.

JSON Schema provides the general structured-validation context for JSON objects
such as EEOAP statements [JSON-Schema-2020-12]. W3C PROV is relevant as an
adjacent provenance standard family for agents, activities, entities, and
relationships [W3C-PROV]. AEP-related repository materials provide broader
local context for runtime evidence bundles and integrity-verifiable packaging
[AEP-Artifact]. This paper is narrower than those lines: it studies
span-to-operation-evidence transformation.

## 5. Method: Telemetry-to-Evidence Mapping

The method maps one OpenTelemetry-style trace JSON file into one
EEOAP-compatible operation accountability statement when the input satisfies
the adapter preconditions. The mapping has seven steps.

First, the adapter parses span records from the input trace. The fixture format
uses OpenTelemetry-style span fields such as `trace_id`, `span_id`,
`parent_span_id`, names, attributes, timestamps, and optional error attributes.

Second, the adapter identifies the accountable agent span. The selected span
must carry the expected agent semantic attributes, including
`gen_ai.agent.id`, `gen_ai.agent.name`, `gen_ai.agent.version`, and
`gen_ai.operation.name`. If no agent span is found, the adapter reports
`missing_agent_span`. If the agent span lacks an operation name, it reports
`missing_operation_name`.

Third, the adapter checks parent-child span consistency. Every span in the
selected trace context that declares a parent must reference an existing parent
span. A missing parent produces `broken_parent_span_relation`. This check
prevents a trace with broken ancestry from being treated as a coherent
operation evidence source.

Fourth, the adapter resolves tool execution spans. Spans with tool-execution
semantics must be reachable from the selected agent span through the parent
chain. If a tool span is present but not under the selected agent operation,
the adapter reports `unresolved_tool_span`. This step distinguishes the
adapter from a field-copying script: tool evidence is included only when its
span ancestry supports the operation mapping.

Fifth, the adapter preserves provenance. The generated statement records trace
and span locators, span identifiers, tool-span identifiers, timestamps, and
artifact locators. These links allow a reviewer to connect the EEOAP statement
back to the telemetry source.

Sixth, the adapter emits the EEOAP-compatible statement. The target statement
records the agent as the actor, the trace as the subject, the selected
operation as the operation, and each resolved tool span as an evidence artifact.
The statement also includes integrity fields computed through existing helper
paths.

Seventh, the adapter routes the result into the existing EEOAP validator. A
successful adapter output is not accepted solely because the adapter wrote JSON;
it must satisfy the existing profile-aware validation path.

## 6. Adapter Implementation

The prototype adapter is implemented at
`tools/opentelemetry_to_eeoap_adapter.py`. It is local and reproducible. It does
not call an external OpenTelemetry service, does not use OpenTelemetry
Collector, and does not require a remote runtime. Inputs are local fixtures
under `examples/opentelemetry/`. Outputs are generated under `generated/`.

For a valid input, the adapter writes two files:

- one EEOAP-compatible statement, using the suffix
  `-eeoap-statement.json`;
- one adapter report, using the suffix `-adapter-report.json`.

For an invalid input, the adapter writes a report with a diagnostic and does
not produce a successful operation accountability statement. The diagnostic
surface is intentionally small and targeted:

- `missing_agent_span`
- `unresolved_tool_span`
- `broken_parent_span_relation`
- `missing_operation_name`

The implementation also records the intended validator path as
`agent-evidence validate-profile`. The test suite calls the same validation
library path when available in the local repository environment. This keeps the
adapter coupled to the existing EEOAP validation behavior without changing the
EEOAP schema.

## 7. Evaluation

The evaluation asks three questions. First, can OpenTelemetry-style agent
telemetry be transformed into EEOAP-compatible operation accountability
statements without modifying the EEOAP schema? Second, can the adapter support
more than one valid trace context, including a workflow-style parent-child span
pattern? Third, can controlled invalid traces expose meaningful
telemetry-to-evidence diagnostics?

The v0.7 evidence expansion provides the main evaluation result:

```text
pytest tests/test_opentelemetry_to_eeoap_adapter.py -q
8 passed in 2.48s
```

Both valid generated statements pass the existing EEOAP validator with
`ok=true` and `issue_count=0`. For both statements, the validator stages
`schema`, `references`, `consistency`, and `integrity` pass. The later v0.9
maintenance verification also passed with `8 passed in 2.00s`; that result is
recorded as maintenance evidence rather than the main evaluation result.

### Table 1: Valid Trace Contexts

| Case | Operation pattern | Span structure | Generated statement | Validator result | Evaluation meaning |
|---|---|---|---|---|---|
| `valid-agent-trace` | Root agent operation `research.answer` with two tool calls. | Agent span `1111111111111111`; direct child tool spans `2222222222222222` and `3333333333333333`. | `generated/valid-agent-trace-eeoap-statement.json` | PASS; `ok=true`; `issue_count=0`; stages `schema`, `references`, `consistency`, `integrity` pass. | Baseline positive case for telemetry-to-evidence transformation. |
| `valid-agent-workflow-trace` | Root agent operation `workflow.execute` with one workflow invocation and two tool calls. | Agent span `4444444444444444`; workflow invocation span `5555555555555555`; descendant tool spans `6666666666666666` and `7777777777777777`. | `generated/valid-agent-workflow-trace-eeoap-statement.json` | PASS; `ok=true`; `issue_count=0`; stages `schema`, `references`, `consistency`, `integrity` pass. | Shows resolution through a deeper parent-child chain. |

### Table 2: Invalid Diagnostic Cases

| Case | Broken condition | Expected diagnostic | Evaluation meaning |
|---|---|---|---|
| `invalid-missing-agent-span` | No accountable agent span is present. | `missing_agent_span` | The adapter refuses to emit evidence without an accountable operation span. |
| `invalid-unresolved-tool-span` | A tool span is not under the selected agent span. | `unresolved_tool_span` | Tool evidence must be structurally connected to the operation. |
| `invalid-broken-parent-span` | A span references a missing parent span. | `broken_parent_span_relation` | Broken trace ancestry prevents safe mapping. |
| `invalid-missing-operation-name` | The agent span lacks `gen_ai.operation.name`. | `missing_operation_name` | An unnamed operation cannot become an operation accountability statement. |

### Table 3: Telemetry-only vs EEOAP Statement

| Representation | What it captures | What it misses | Validation path | Role in this paper |
|---|---|---|---|---|
| Raw logs | Event text and runtime messages. | Structured operation accountability, span ancestry, profile-aware evidence sections. | Depends on log tooling and conventions. | Adjacent operational source, not the evaluated input. |
| Raw OpenTelemetry-style trace | Spans, attributes, identifiers, parent links, timestamps, and errors. | EEOAP actor/subject/operation statement, evidence artifacts, integrity fields, and profile validation result. | Telemetry tooling can process traces, but not as EEOAP statements. | Source representation consumed by the adapter. |
| Provenance-only record | Relations among agents, activities, entities, and derivations. | OpenTelemetry-specific span extraction and EEOAP-specific accountability structure. | Depends on the provenance format and validator. | Conceptual neighbor for provenance preservation. |
| EEOAP statement | Actor, subject, operation, constraints, evidence references, provenance, integrity, and validation metadata. | Full raw runtime breadth unless preserved by reference or artifact locator. | Existing EEOAP validator checks schema, references, consistency, and integrity. | Target portable operation evidence object. |
| Adapter path | Selection, mapping, parent closure, tool-span resolution, provenance preservation, statement emission, and validator routing. | Production telemetry support and broad OpenTelemetry compatibility. | Output is checked by the existing EEOAP validator. | Main contribution of the paper. |

### Table 4: Reproducibility Evidence

| Evidence item | Result | Interpretation |
|---|---|---|
| Scoped adapter tests | v0.7 evidence expansion: `8 passed in 2.48s`; v0.9 maintenance verification: `8 passed in 2.00s`. | Focused tests cover valid conversions and invalid diagnostics. |
| Generated statements | Two valid EEOAP-compatible statements are committed under `generated/`. | Positive evaluation has concrete output artifacts. |
| Adapter reports | Reports exist for generated valid outputs. | The transformation records extracted telemetry and validation metadata. |
| Existing EEOAP validator | Both valid statements pass with `ok=true` and `issue_count=0`. | Adapter outputs enter the existing profile-aware validation path. |
| Clean-clone verification | v0.5 frozen package includes clean-clone verification. | The frozen package was reproducible from a clean checkout before v0.7 expansion. |
| Checksum verification | v0.5 frozen package includes checksum verification. | The frozen package had file-level integrity evidence. |
| Repository hygiene note | Full-repository Ruff remains affected by unrelated out-of-scope lint debt. | Scoped adapter evidence is separated from unrelated repository hygiene debt. |

The evaluation remains bounded. It uses two synthetic valid trace contexts and
four synthetic invalid contexts. This is enough to support the paper's bounded
claim that telemetry-to-evidence transformation can be implemented and checked
under controlled trace contexts. It is not enough to claim broad
OpenTelemetry compatibility, cross-framework generality, or production
readiness.

## 8. Discussion

The second workflow-style trace matters because it changes the operation
structure without changing the EEOAP schema. In the first valid trace, tool
spans are direct children of the agent span. In the second valid trace, tool
spans are children of a workflow invocation span, which is itself a child of
the agent span. Passing both cases shows that the adapter is not limited to a
single direct-child pattern. It can resolve tool spans through a deeper
parent-child chain while preserving the same target evidence profile.

The adapter is more than field copying. It identifies the accountable operation
span, rejects traces without required operation context, checks parent closure,
resolves tool spans by ancestry, preserves source provenance links, emits an
EEOAP-compatible statement, recomputes integrity-related fields, and routes the
result into the existing validator. These operations introduce explicit
mapping and validation decisions between telemetry and evidence.

Schema reuse is central. A new schema could make almost any mapping appear to
succeed by redefining the target. This paper instead keeps EEOAP stable and
asks whether telemetry can enter the existing evidence-object path. The
validator result is therefore an important part of the artifact story:
generated statements pass the existing profile-aware checks rather than a
newly created adapter-specific checker.

The work is software engineering research because it studies an interface
between observability infrastructure and evidence-object validation. The
method is about extracting, checking, transforming, and validating operational
data under explicit boundaries. The artifact is small, but the engineering
question is general enough to matter: how can runtime telemetry be made
portable and validator-aware without pretending that telemetry alone proves
accountability?

## 9. Threats to Validity

The first threat is synthetic fixture limitation. Both valid traces are local
and controlled. They support reproducibility and diagnostic clarity, but they
do not prove behavior on production telemetry.

The second threat is evaluation size. Two valid trace contexts and four invalid
diagnostic contexts strengthen the earlier artifact package, but they remain a
small evaluation. The paper should not claim broad empirical coverage.

The third threat is OpenTelemetry evolution. The OpenTelemetry GenAI semantic
conventions are official but evolving [OpenTelemetry-GenAI]. A future version
may revise attribute names, status, or recommended patterns. The adapter claim
therefore stays limited to the controlled OpenTelemetry-style fixtures in this
repository.

The fourth threat is lack of real framework integration. No LangChain,
CrewAI, AutoGen, or OpenTelemetry Collector integration is implemented here.
Any claim about those systems would require committed fixtures, generated
outputs, tests, and validator results.

The fifth threat is no legal or regulatory validation. Validator success means
that a generated statement satisfies the current EEOAP profile checks. It does
not prove legal accountability, regulatory compliance, agent-output
correctness, or full runtime reconstruction.

The sixth threat is repository hygiene. Full-repository Ruff is affected by
unrelated out-of-scope lint debt in other directories. This paper relies on
scoped adapter tests, generated outputs, validator results, clean-clone notes,
and checksum evidence while disclosing that broader repository hygiene issue.

The seventh threat is artifact citation status. The v0.9 citation assessment
marks OpenTelemetry, JSON Schema, W3C PROV, and ACM artifact badging sources as
verified against official sources, but `EEOAP-Artifact` and `AEP-Artifact`
remain local artifact references. External submission requires a release,
archive, DOI, or immutable tag for those references.

## 10. Related Work

OpenTelemetry provides the telemetry-side source vocabulary and runtime
observability context [OpenTelemetry-GenAI]. The GenAI agent-span documentation
motivates the adapter's use of agent identity, operation name, span ancestry,
timestamps, and error attributes [OpenTelemetry-Agent-Spans]. This paper does
not evaluate OpenTelemetry instrumentation coverage; it uses controlled
OpenTelemetry-style traces as source artifacts.

EEOAP provides the target operation accountability statement and validator path
[EEOAP-Artifact]. Earlier EEOAP work defines the evidence object and validation
surface. This paper studies how telemetry enters that object through a bounded
adapter.

JSON Schema is relevant because EEOAP statements are structured JSON objects
that require schema-aware validation [JSON-Schema-2020-12]. W3C PROV is
adjacent because it models provenance across agents, activities, and entities
[W3C-PROV]. The adapter preserves provenance links but does not claim to be a
general provenance interchange framework.

AEP-related repository artifacts provide broader context for runtime evidence
bundles and integrity-verifiable evidence packaging [AEP-Artifact]. This paper
is narrower: it focuses on span-to-operation-evidence transformation, not
runtime bundle governance or a new profile. Artifact review and reproducibility
expectations are adjacent to ACM artifact-badging practices
[ACM-Artifact-Badging], but this package has not been formally badged.

## 11. Conclusion

This paper presents a minimal adapter from OpenTelemetry-style agent spans to
EEOAP-compatible operation accountability statements. The adapter keeps the
target profile stable, preserves trace and span provenance, resolves tool
spans, checks parent-child span relationships, emits validator-ready
statements, and uses the existing EEOAP validator.

The evaluation covers two valid trace contexts and four invalid diagnostic
contexts. Both valid generated statements pass the existing EEOAP validator
with `ok=true` and `issue_count=0` across `schema`, `references`,
`consistency`, and `integrity`. The invalid fixtures demonstrate bounded
diagnostics for missing agent span, unresolved tool span, broken parent-span
relation, and missing operation name.

The result is a small but explicit bridge between agent telemetry and portable
operation evidence. It does not prove legal accountability, full runtime
reconstruction, cross-framework generality, production readiness, or broad
OpenTelemetry compatibility. It shows that telemetry-to-evidence
transformation can be made reproducible, profile-aware, and validator-checked
under controlled conditions.

## 12. References

- [OpenTelemetry-GenAI] OpenTelemetry. `Semantic conventions for generative AI
  systems`. Official OpenTelemetry semantic conventions documentation. Accessed
  2026-05-23. URL:
  <https://opentelemetry.io/docs/specs/semconv/gen-ai/>. TODO: verify semantic
  convention version and status immediately before external submission.

- [OpenTelemetry-Agent-Spans] OpenTelemetry. `Semantic Conventions for GenAI
  agent and framework spans`. Official OpenTelemetry semantic conventions
  documentation. Accessed 2026-05-23. URL:
  <https://opentelemetry.io/docs/specs/semconv/gen-ai/gen-ai-agent-spans/>.
  TODO: verify field list and current semantic convention version immediately
  before external submission.

- [JSON-Schema-2020-12] Wright, Austin; Andrews, Henry; Hutton, Ben; Dennis,
  Greg. `JSON Schema Draft 2020-12`. Published 2022-06-16. URL:
  <https://json-schema.org/draft/2020-12>. TODO: adapt author/editor format to
  the selected venue.

- [W3C-PROV] Lebo, Timothy; Sahoo, Satya; McGuinness, Deborah. `PROV-O: The
  PROV Ontology`. W3C Recommendation, 2013-04-30. URL:
  <https://www.w3.org/TR/prov-o/>. TODO: decide whether to add PROV-DM and
  PROV Overview as separate references.

- [EEOAP-Artifact] `agent-evidence` repository. Execution Evidence and
  Operation Accountability Profile artifacts and OpenTelemetry-to-EEOAP adapter
  materials. Local branch `opentelemetry-to-eeoap-adapter`; v0.8 draft commit
  `d5879f3678ab22896b36d1d81e7a4f18a466ebcf`. TODO: replace with immutable
  release, archive, tag, or DOI before external submission.

- [AEP-Artifact] `agent-evidence` repository. AEP-related evidence artifact
  materials used for positioning. TODO: identify exact public artifact, commit,
  release, archive, or DOI before external submission.

- [ACM-Artifact-Badging] Association for Computing Machinery. `Artifact Review
  and Badging - Current`. ACM Publications Policy. Accessed 2026-05-23. URL:
  <https://www.acm.org/publications/policies/artifact-review-and-badging-current>.
  TODO: re-check policy wording before submission.

## 13. Artifact Availability and Reproducibility Note

The frozen package path is
`papers/opentelemetry-to-eeoap/frozen_v0_5/`. That package includes a README,
manifest, freeze status, checksum file, claim boundary, evaluation summary,
reviewer positioning notes, clean-clone verification, and an external review
brief. Clean-clone verification and checksum verification exist for the v0.5
frozen package.

The repository also contains generated EEOAP statements and adapter reports for
both valid traces:

- `generated/valid-agent-trace-eeoap-statement.json`
- `generated/valid-agent-trace-adapter-report.json`
- `generated/valid-agent-workflow-trace-eeoap-statement.json`
- `generated/valid-agent-workflow-trace-adapter-report.json`

The current status is: submission candidate, not externally archived final
package. EEOAP and AEP external archive, release, DOI, or immutable tag
references are still required before final external submission.

Submission Candidate Status: This draft is intended for external pre-review
and journal-route preparation. It is not yet venue-formatted and not yet
formally submitted.

## 14. Draft Preparation Note

Commands run while preparing this draft:

```text
git branch --show-current
git status --short
git log --oneline -8
rg -n "^#|^##|Table|8 passed|ok=true|issue_count|References|Artifact Availability|Draft Preparation" papers/opentelemetry-to-eeoap/paper_v0_8_journal_draft.md papers/opentelemetry-to-eeoap/journal_v0_9_citation_and_venue/*.md papers/opentelemetry-to-eeoap/journal_v0_7_second_trace/*.md papers/opentelemetry-to-eeoap/frozen_v0_5/*.md
nl -ba /Users/zhangbin/.codex/memories/MEMORY.md | sed -n '746,782p;792,837p;2147,2149p'
/Users/zhangbin/GitHub/agent-evidence/.venv/bin/python -m pytest tests/test_opentelemetry_to_eeoap_adapter.py -q
```

Scoped pytest result:

```text
........                                                                 [100%]
8 passed in 1.91s
```

Change boundary:

- Runtime code changed: no.
- Tests changed: no.
- Fixtures changed: no.
- Generated JSON outputs changed: no.
- EEOAP schema changed: no.
- Out-of-scope worktree items touched: no.

Plugin Selection Report:

- `tool_search` was used first to inspect available plugin/workflow/tool
  support, satisfying the plugin-first instruction.
- `update_plan` was used for task tracking.
- `exec_command` was used for repository inspection, scoped validation,
  staging, and commit commands.
- `apply_patch` was used for the Markdown file edit.
- Web/browser tools were not used in this v1.0 drafting step because v0.9
  already contains the required citation verification and the task explicitly
  avoided broad venue research.
- Canva, Figma, Google Drive, Hugging Face, OpenAI Platform, LegalZoom, and
  Node REPL tools were not used because they are unrelated to this local
  Markdown drafting and test-validation task.
