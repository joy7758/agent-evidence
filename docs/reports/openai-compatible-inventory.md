# OpenAI-Compatible Inventory

Scope: `agent-evidence` only.

Method: local inventory of current OpenAI / provider-related code, docs, examples, CLI references, and tests. This document distinguishes between current working helper surfaces and a proposed future OpenAI-compatible adapter API. It does not change code, schema, tests, or directory structure.

## 1. Current OpenAI / Provider-Related Touchpoints

### Product and packaging surfaces

| Path | Surface type | Current role | Notes |
| --- | --- | --- | --- |
| `README.md` | product entry | names OpenAI-compatible runtimes as the second integration priority | Priority statement only. It does not point to a current runnable OpenAI-compatible path. |
| `pyproject.toml` | packaging | declares `openai-agents` extra | There is no `openai` SDK extra and no `openai-compatible` extra today. |
| `agent_evidence/integrations/__init__.py` | public integration exports | re-exports `openai_agents` helper surfaces | Makes the SDK-specific tracing processor visible from `agent_evidence.integrations`. |

### Current OpenAI-related implementation surfaces

| Path | Surface type | Current role | Notes |
| --- | --- | --- | --- |
| `agent_evidence/integrations/openai_agents.py` | integration module | OpenAI Agents SDK tracing processor | Converts OpenAI Agents traces/spans into evidence records through `EvidenceRecorder`. This is SDK-specific, not provider-agnostic. |
| `examples/openai_agents/basic_export.py` | runnable helper example | minimal local export path using the OpenAI Agents SDK | Exports a JSON `bundle` and prints verification output, but does not write a normalized `receipt` file or `summary`. |
| `tests/test_openai_agents_integration.py` | test | coverage for the OpenAI Agents tracing processor | Covers trace/span recording, exported summaries, and SDK registration. |

### Current helper / prototype / legacy surfaces

| Path | Surface type | Current role | Notes |
| --- | --- | --- | --- |
| `integrations/openai-agents/README.md` | helper doc | older prototype doc for OpenAI Agents export | Explicitly describes a legacy `Execution Evidence Object` wording surface. |
| `integrations/openai-agents/export_evidence.py` | prototype script | converts a mocked OpenAI Agents runtime trace into an older object-model export | Does not use the current `bundle / receipt / summary` product language. |
| `examples/openai-agent-run.json` | sample data | mocked OpenAI Agents runtime trace | Historical/example payload only. |
| `examples/evidence-object-openai-run.json` | sample data | mocked `execution-evidence-object` export | Historical/example payload only. |
| `demo/run_operation_accountability_demo.py` | demo | includes `"runtime": "openai-agents"` in one statement | This is a scenario label inside the profile demo, not an actual provider integration path. |

### CLI surfaces

Current CLI surfaces are generic only:

- `agent-evidence verify-export`
- `agent-evidence verify-bundle`
- `agent-evidence validate-profile`

There is currently:

- no `agent-evidence openai ...` subcommand
- no `agent-evidence provider ...` subcommand
- no provider-specific export or capture CLI entry point

## 2. What Already Exists vs What Is Absent

### What already exists

- one SDK-specific tracing helper for the OpenAI Agents SDK:
  - `AgentEvidenceTracingProcessor`
  - `install_openai_agents_processor(...)`
- generic evidence building blocks already used by other paths:
  - `EvidenceRecorder`
  - `LocalEvidenceStore`
  - `export_json_bundle(...)`
  - `verify_json_bundle(...)`
- JSON-safe serialization helpers:
  - `to_jsonable(...)`
  - `ensure_json_object(...)`
- redaction behavior for sensitive fields in `agent_evidence/serialization.py`
  - currently includes `api_key`, `authorization`, `token`, and `prompt`
- one OpenAI Agents example and one OpenAI Agents integration test module

### What is absent

- no provider-agnostic module such as `agent_evidence/integrations/openai_compatible/`
- no `openai` SDK dependency in `pyproject.toml`
- no provider/client abstraction for:
  - `api_key`
  - `base_url`
  - `model`
  - `provider_label`
- no abstraction for raw OpenAI-compatible request/response capture
- no normalized summary writer for the current OpenAI-related example path
- no explicit `receipt.json` writer in the current OpenAI-related example path
- no provider-agnostic compatibility tests
- no active quickstart doc for an OpenAI-compatible first-run path

### Current response-handling assumptions

Current OpenAI-related code assumes one thing only:

- if the OpenAI Agents SDK emits trace/span objects with `.export()` payloads, those payloads can be converted into evidence events

Current code does not assume or provide:

- a Responses API wrapper
- a Chat Completions wrapper
- streaming delta aggregation for OpenAI-compatible clients
- tool-call normalization across providers
- a stable provider-neutral response shape

### Current signing / export / verify reuse points

The Phase C wrapper should reuse the same stable building blocks already used by the LangChain path:

- `EvidenceRecorder`
- `LocalEvidenceStore`
- `export_json_bundle(...)`
- `verify_json_bundle(...)`

Those reuse points already produce the repo’s current product outputs:

- `bundle`
- `receipt`
- `summary`

## 3. Proposed Minimal Adapter API

This section is a recommendation for Phase C. It is not a description of current code.

### Recommendation

Use one provider-agnostic adapter module:

- `agent_evidence/integrations/openai_compatible/`

Use one recommended public entry point:

- `OpenAICompatibleAdapter`

Use one normalized artifact result object:

- `OpenAICompatibleArtifacts`

### Recommended public API

```python
from agent_evidence.integrations.openai_compatible import OpenAICompatibleAdapter

adapter = OpenAICompatibleAdapter.for_output_dir(
    output_dir="./artifacts/openai-compatible-run",
    provider_label="openai",
    model="gpt-4.1-mini",
    api_key=os.environ["OPENAI_API_KEY"],
    base_url="https://api.openai.com/v1",
    digest_only=True,
    omit_request=False,
    omit_response=False,
)

response = adapter.record_call(
    operation="responses.create",
    request={"input": "hello world"},
    invoke=lambda: client.responses.create(model="gpt-4.1-mini", input="hello world"),
)

artifacts = adapter.finalize()
```

### Why this shape is the right minimum

- It gives Phase C one recommended entry point instead of many provider-specific helpers.
- It keeps provider client invocation outside core business logic.
- It can reuse the current local-first artifact path:
  - capture one provider call
  - write a JSON `bundle`
  - verify the exported `bundle`
  - write a `receipt`
  - write a `summary`
- It avoids treating the OpenAI Agents SDK tracing processor as the universal Phase C entry point.

### Suggested API behavior

`OpenAICompatibleAdapter.for_output_dir(...)`

Inputs:

- `output_dir`
- `provider_label`
- `model`
- `api_key`
- `base_url`
- optional redaction flags:
  - `digest_only`
  - `omit_request`
  - `omit_response`
- optional request defaults:
  - `temperature`
  - `top_p`
  - `max_output_tokens`
  - `tool_choice`
  - `timeout`

Behavior:

- stores provider/runtime metadata needed for the evidence context
- records one or more provider calls through a provider-neutral capture method
- keeps the actual provider client object outside core
- owns export, verify, and summary write

`adapter.record_call(...)`

Inputs:

- `operation`
- `request`
- `invoke`
- optional metadata/tags

Behavior:

- records a start/end call boundary using generic evidence events
- normalizes request and response payloads through existing serialization helpers
- redacts or digests sensitive payload fields using the adapter settings
- returns the provider response to the caller

`adapter.finalize()`

Output:

- `OpenAICompatibleArtifacts`

Suggested `OpenAICompatibleArtifacts` fields:

- `bundle_path`
- `receipt`
- `receipt_path`
- `summary`
- `summary_path`
- `supporting_files`

### How outputs remain normalized

The OpenAI-compatible adapter should keep the same product language already used elsewhere in this repo:

- `bundle`
  - exported evidence artifact
- `receipt`
  - machine-readable verification result
- `summary`
  - reviewer-facing output

Supporting files such as manifest sidecars, keys, and runtime JSONL should remain supporting files, not additional primary outputs.

## 4. Configuration Model

### Required configuration

- `api_key`
  - accepted as adapter input
  - must never be persisted raw into evidence artifacts
  - if it appears in captured structures, current redaction should replace it with `[REDACTED]`
- `base_url`
  - optional but first-class
  - required for non-default OpenAI-compatible providers
- `model`
  - required
  - should be preserved in evidence metadata/context
- `provider_label`
  - required
  - should be a stable provider-neutral label such as:
    - `openai`
    - `azure-openai`
    - `vllm`
    - `lm-studio`
    - `openrouter`

### Optional request settings

The adapter should allow provider-neutral pass-through settings such as:

- `temperature`
- `top_p`
- `max_output_tokens`
- `tool_choice`
- `parallel_tool_calls`
- `timeout`

These should remain request metadata, not canonical schema fields.

### What must remain provider-agnostic

The core adapter should not bake in:

- Azure deployment naming rules
- provider-specific auth headers beyond the generic `api_key` input
- Responses API as the only supported operation surface
- Chat Completions as the only supported operation surface
- provider-specific retry or rate-limit policy inside core evidence logic

The core contract should care about:

- one provider call happened
- what request/response boundary was captured
- how that call becomes `bundle`, `receipt`, and `summary`

## 5. Risks / Gaps

### Provider-specific assumptions currently baked into code or docs

- the only real implementation surface is named `openai_agents`, which is SDK-specific rather than provider-agnostic
- `README.md` says “OpenAI-compatible runtimes”, but the repo currently exposes only an OpenAI Agents SDK helper
- `integrations/openai-agents/export_evidence.py` and `examples/evidence-object-openai-run.json` still use the older `execution-evidence-object` wording
- `demo/run_operation_accountability_demo.py` uses `"runtime": "openai-agents"` as a scenario label, which could be misread as an implemented Phase C runtime path

### Test gaps

- no test for a provider-agnostic adapter object
- no test for provider config fields such as `base_url`, `provider_label`, and `model`
- no test for request/response capture across multiple OpenAI-compatible shapes
- no compatibility test for fake OpenAI-compatible clients

### Artifact-structure risks

- the current OpenAI Agents example exports a `bundle` and prints verify output, but does not write a normalized `receipt.json`
- the current OpenAI Agents example does not write a `summary`
- older OpenAI-related prototype files still point toward object-model exports rather than the current `bundle / receipt / summary` contract

### Naming risks

- the repo currently mixes:
  - `openai-agents`
  - `openai_agents`
  - “OpenAI-compatible runtimes”
- that naming mix can blur the difference between:
  - one SDK-specific tracing helper
  - one future provider-agnostic adapter line

### Security / serialization risks

- current serialization redacts `prompt` globally
  - that is safe by default, but it means provider request capture may lose reviewer-facing detail unless the adapter defines a clear digest-only / omit / inline policy
- current code has no explicit boundary yet for which provider config fields are safe to include in `summary`

## 6. Lowest-Risk Implementation Sequence

### C1 wrapper

Implement one provider-agnostic wrapper only:

- module path:
  - `agent_evidence/integrations/openai_compatible/`
- public entry:
  - `OpenAICompatibleAdapter`
- build it on existing stable primitives only:
  - `EvidenceRecorder`
  - `LocalEvidenceStore`
  - `export_json_bundle(...)`
  - `verify_json_bundle(...)`

### C2 provider config examples

Add one or two small example surfaces after the wrapper exists:

- one default OpenAI-compatible example
- one alternate `base_url` example

These examples should demonstrate config only. They should not introduce provider-specific branching into core.

### C3 compatibility tests

Add tests for:

- adapter artifact generation
- request/response redaction behavior
- config propagation for `provider_label`, `model`, and `base_url`
- fake-client compatibility without live network calls

### What should explicitly wait

- any OpenAI-compatible CLI subcommand
- any live-provider integration test
- any cross-repo demo synchronization
- any attempt to merge `openai-agents` tracing and raw client wrapping into one patch
- any schema change

## 7. Non-Goals

- no schema changes
- no exporter expansion
- no LangGraph work
- no cross-repo demo changes
- no provider-specific business logic in core
- no attempt to recast `openai-agents` tracing as the final OpenAI-compatible API
- no attempt to absorb the older `execution-evidence-object` prototype surfaces into the Phase C wrapper patch
