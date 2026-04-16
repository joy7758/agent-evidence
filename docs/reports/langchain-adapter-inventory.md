# LangChain Adapter Inventory

Scope: `agent-evidence` only.

Method: local inventory of current LangChain / LangGraph-related code, docs, examples, CLI references, and tests. This document distinguishes between current working surfaces and a proposed future adapter API. It does not change code, schema, tests, or directory structure.

## 1. Current LangChain / LangGraph Touchpoints

### Current LangChain touchpoints

| Path | Surface type | Current role | Notes |
| --- | --- | --- | --- |
| `pyproject.toml` | packaging | declares `langchain` extra | Current install surface is `pip install -e ".[langchain,signing]"`; no `langgraph` extra exists. |
| `README.md` | product entry | names LangChain / LangGraph as the first integration priority | Product-facing priority statement only. |
| `docs/quickstart.md` | active product doc | current first-run path | Uses `examples/langchain_minimal_evidence.py` plus `agent-evidence verify-export`. |
| `docs/cookbooks/langchain_minimal_evidence.md` | active how-to doc | detailed LangChain-first recipe | Explicitly says the path stays outside LangGraph persistence and checkpointer internals. |
| `examples/langchain_minimal_evidence.py` | runnable example | current de facto product path | Callback capture -> local JSONL -> JSON `bundle` -> in-process verify -> `summary`. |
| `agent_evidence/integrations/langchain.py` | integration module | current LangChain capture primitives | Exposes stream-event normalization helpers and `EvidenceCallbackHandler`. |
| `agent_evidence/integrations/__init__.py` | public integration exports | re-exports LangChain helpers | Makes LangChain surfaces available from `agent_evidence.integrations`. |
| `agent_evidence/__init__.py` | public package exports | exposes generic record/export/verify primitives | Current example path imports generic primitives from here, not from a LangChain-specific adapter entry. |
| `integrations/langchain/export_evidence.py` | runnable integration helper | alternate LangChain path via `EvidenceBundleBuilder` | Produces an AEP bundle directory, not the current JSON `bundle` quickstart surface. |
| `integrations/langchain/README.md` | helper doc | documents the AEP bundle path | Uses `verify-bundle`; this is parallel to, not the same as, the quickstart path. |
| `agent_evidence/cli/main.py` | CLI | generic verify/export commands used by LangChain paths | No LangChain-specific CLI subcommand exists. |
| `tests/test_langchain_integration.py` | test | lower-level LangChain coverage | Covers callback capture, stream event normalization, AEP bundle builder path, and example smoke. |
| `tests/test_quickstart_smoke.py` | test | current first-run smoke gate | Covers the docs quickstart path only. |
| `tests/test_aep_profile.py` and `tests/fixtures/agent_evidence_profile/*` | test / fixtures | supporting AEP bundle verification path | LangChain-labeled payloads exist here, but this is not the current quickstart product path. |

### Current LangGraph touchpoints

Actual LangGraph-specific implementation surfaces are absent.

Current LangGraph-related references are limited to:

- `README.md`
  - priority statement: `LangChain / LangGraph` first
- `docs/cookbooks/langchain_minimal_evidence.md`
  - explicit boundary: the current path stays outside LangGraph persistence and checkpointer internals
  - explicit non-goal: this is not a LangGraph persistence or checkpointer integration

There is currently:

- no `langgraph` dependency in `pyproject.toml`
- no `agent_evidence/integrations/langgraph.py`
- no LangGraph example
- no LangGraph-specific test
- no LangGraph-specific CLI surface

## 2. Current Responsibilities by Surface

| Surface | Capture | Export | Verify | Summary / review | Supporting materials |
| --- | --- | --- | --- | --- | --- |
| `agent_evidence/integrations/langchain.py` | Yes | Indirectly, via `bundle_builder` branch in callback handler | No direct CLI-level verify | No | tags, event mapping, span metadata, redaction flags |
| `examples/langchain_minimal_evidence.py` | Yes, via `EvidenceCallbackHandler(recorder=...)` | Yes, via `export_json_bundle` | Yes, via `verify_json_bundle` and later `verify-export` command | Yes, writes `summary.json` | key generation, manifest sidecar, runtime JSONL |
| `docs/quickstart.md` | Documents current path | Documents current path | Documents explicit `verify-export` step | Documents review step | names manifest, key, runtime capture as supporting files |
| `docs/cookbooks/langchain_minimal_evidence.md` | Documents callback capture | Documents signed JSON bundle export | Documents offline verify | Documents reviewer-oriented output artifacts | installation notes, artifact locations, boundary notes |
| `integrations/langchain/export_evidence.py` | Yes, via `EvidenceCallbackHandler(bundle_builder=...)` | Yes, via `EvidenceBundleBuilder.write_bundle()` | Yes, via `verify_bundle` | No normalized `summary` output | AEP bundle directory contents |
| `integrations/langchain/README.md` | Documents AEP callback path | Documents AEP bundle write | Documents `verify-bundle` | No | points to fixture gate |
| `agent_evidence/cli/main.py` | No LangChain-specific capture | Generic export of stored records | Generic `verify-export` and `verify-bundle` | JSON verification result only | keyring, signer config, archive packaging |
| `tests/test_langchain_integration.py` | Yes | Yes | Yes | Partial | validates callback/event surfaces and example behavior |
| `tests/test_quickstart_smoke.py` | Yes, by executing the example | Yes, by asserting `bundle` exists | Yes, via `verify-export` | Yes, by asserting `summary` exists | subprocess and temp output directory |

## 3. Which Surfaces Are Active, Helper, or Confusing

### Active product surface

- `README.md`
  - current product entry and priority statement
- `docs/quickstart.md`
  - current first-run path
- `docs/cookbooks/langchain_minimal_evidence.md`
  - current detailed LangChain-first recipe
- `examples/langchain_minimal_evidence.py`
  - current runnable example for `bundle / receipt / summary`
- `agent_evidence/integrations/langchain.py`
  - current capture primitive
- `tests/test_quickstart_smoke.py`
  - current smoke gate for the first-run path

### Helper / example surface

- `tests/test_langchain_integration.py`
  - low-level coverage and API characterization
- `agent_evidence/integrations/__init__.py`
  - public re-export layer
- `agent_evidence/__init__.py`
  - generic primitives that the example currently composes manually
- `pyproject.toml`
  - install-time support surface

### Legacy / duplicated / confusing surface

- `integrations/langchain/export_evidence.py`
  - alternate LangChain path that writes an AEP bundle directory
- `integrations/langchain/README.md`
  - documents the alternate AEP bundle path, not the quickstart path
- `agent_evidence.aep.EvidenceBundleBuilder`
  - still active in tests and the integration helper, but not aligned with the current `bundle / receipt / summary` quickstart language
- `verify-bundle`
  - valid command, but it verifies the alternate AEP bundle line rather than the current quickstart JSON `bundle`
- `README.md` and docs using `LangChain / LangGraph` together
  - currently overstates parity because only LangChain has real implementation surfaces
- `examples/README.md`
  - current primary example index does not mention `examples/langchain_minimal_evidence.py`, which makes the actual first-run path harder to discover

## 4. Current De Facto Integration Path

### What a developer must actually do today

The current first-run path is:

1. install the LangChain + signing extras
2. import generic primitives from `agent_evidence`
3. import `EvidenceCallbackHandler` from `agent_evidence.integrations`
4. attach the handler to LangChain callbacks
5. run the LangChain workflow
6. export a JSON `bundle`
7. verify that `bundle`
8. write a `summary`

In code, that means the current de facto path is composed from multiple surfaces:

```python
from agent_evidence import (
    EvidenceRecorder,
    LocalEvidenceStore,
    export_json_bundle,
    verify_json_bundle,
)
from agent_evidence.integrations import EvidenceCallbackHandler
```

Then the example itself is still responsible for:

- output directory creation
- signing key generation
- manifest sidecar path selection
- receipt generation or re-verification command construction
- summary file construction

### Where that path is fragmented

- The active capture primitive is LangChain-specific, but export and verify primitives are generic top-level functions.
- There is no single adapter object that owns the whole LangChain path.
- The repo exposes two parallel LangChain output lines:
  - quickstart line: JSON `bundle` + `verify-export`
  - AEP line: bundle directory + `verify-bundle`
- There is no dedicated LangChain CLI entry such as `agent-evidence langchain ...`.
- Discovery is split across `README.md`, `docs/quickstart.md`, `docs/cookbooks/langchain_minimal_evidence.md`, and `integrations/langchain/README.md`.
- `examples/README.md` does not surface the current LangChain example at all.

## 5. Missing or Weak Integration Points

### API gaps

- No single LangChain adapter entry point wraps capture, export, verify, and summary generation.
- No reusable summary helper exists for the current LangChain-first path; `examples/langchain_minimal_evidence.py` assembles the summary inline.
- No reusable quickstart-oriented signer/output configuration helper exists; the example owns key generation and output naming.
- Stream-event normalization and callback capture are exposed as separate helper surfaces without one recommended primary API.

### Naming gaps

- `bundle` means two different implementation shapes today:
  - JSON export artifact in the quickstart path
  - AEP bundle directory in the older path
- `verify-export` and `verify-bundle` both look like primary verification commands, but they serve different artifact lines.
- `LangChain / LangGraph` is used as one priority label even though only LangChain has implemented surfaces.

### Runtime / config gaps

- No canonical config object exists for output directory, signing, redaction, or summary behavior in the current LangChain path.
- The example assumes local PEM key generation inside the example itself.
- The example uses direct callback method calls for the mocked model step rather than one reusable adapter lifecycle.

### Test gaps

- Quickstart smoke coverage now exists, which is good.
- There is still no test for one unified LangChain adapter API because that API does not exist yet.
- There is no LangGraph-specific test surface.
- There is no regression test asserting that the documented current example index points to the LangChain quickstart path.

### Documentation gaps

- `examples/README.md` omits the current LangChain runnable example.
- `integrations/langchain/README.md` documents a valid but alternate path without clearly marking it as secondary to the quickstart path.
- The repo does not yet have one explicit inventory document separating:
  - active LangChain path
  - alternate AEP LangChain path
  - LangGraph not-yet-implemented scope

## 6. Proposed Minimal Unified Adapter API

This section is a recommendation for B2. It is not a description of current code.

### Recommendation

Use one stateful adapter object in `agent_evidence.integrations.langchain` as the single recommended entry point:

- `LangChainAdapter`
- `LangChainArtifacts`

### Recommended entry points only

```python
from agent_evidence.integrations.langchain import LangChainAdapter

adapter = LangChainAdapter.for_output_dir(
    output_dir="./artifacts/langchain-run",
    digest_only=True,
    omit_request=False,
    omit_response=False,
)

callbacks = [adapter.callback_handler()]

# user runs LangChain / LangGraph workflow with these callbacks

artifacts = adapter.finalize()
```

### Suggested API shape

`LangChainAdapter.for_output_dir(...)`

Inputs:

- `output_dir`
- optional signing material or signer config
- optional redaction flags:
  - `digest_only`
  - `omit_request`
  - `omit_response`
- optional callback behavior:
  - `capture_stream_tokens`
- optional default metadata/tags

Behavior:

- internally creates the current recommended capture path
- owns the local store, export step, verify step, and summary write
- returns one normalized artifact result

`adapter.callback_handler()`

Output:

- one callback handler to place into LangChain or LangGraph callback configuration

`adapter.finalize()`

Output:

- `LangChainArtifacts`

Suggested `LangChainArtifacts` fields:

- `bundle_path`
- `receipt`
- `receipt_path`
- `summary`
- `summary_path`
- `supporting_files`

### How outputs stay normalized

The adapter should normalize outputs to:

- `bundle`
  - exported JSON artifact path
- `receipt`
  - machine-readable verification result
- `summary`
  - reviewer-facing output

Supporting files such as manifest sidecars, keys, and runtime JSONL should remain supporting files, not first-class product outputs.

### Why this is the right minimum

- It matches the current quickstart path instead of inventing a new artifact line.
- It keeps `EvidenceCallbackHandler` as the underlying capture primitive rather than replacing it.
- It gives LangGraph a place to land later without promising a separate API now; if LangGraph continues to use LangChain callback semantics, it can use the same adapter entry point.
- It avoids exposing developers to the current choice between generic record/export primitives and the older `EvidenceBundleBuilder` line.

## 7. Lowest-Risk Implementation Sequence for B2

### Implement first

1. Add the one recommended adapter wrapper in `agent_evidence.integrations.langchain`.
2. Build it on top of the current quickstart path only:
   - callback capture
   - local JSONL store
   - `export_json_bundle`
   - `verify_json_bundle`
   - summary write
3. Update `examples/langchain_minimal_evidence.py` to use that wrapper internally.
4. Add focused tests for the new adapter object while keeping the current quickstart smoke gate.

### Explicitly wait

- any LangGraph persistence / checkpointer integration
- any LangGraph-specific adapter module
- any OpenAI-compatible unification work
- any new CLI surface for LangChain
- any attempt to merge the JSON quickstart path and the AEP bundle directory path in one patch
- any cross-repo demo synchronization

### What should not be changed

- canonical schema
- normalized output language: `bundle / receipt / summary`
- current quickstart smoke semantics
- current generic export/verify functions as underlying building blocks
- current `EvidenceCallbackHandler` event mapping unless a bug is found

## 8. Non-Goals

- no schema changes
- no exporter expansion
- no cross-repo changes
- no OpenAI-compatible work yet
- no demo repo changes yet
- no directory moves
- no attempt to productize LangGraph before the repo has real LangGraph surfaces
