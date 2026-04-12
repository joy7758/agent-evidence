<!-- language-switch:start -->
[English](./README.md) | [中文](./README.zh-CN.md)
<!-- language-switch:end -->

# Agent Evidence

Concrete execution-evidence entry for verifiable AI agent runs with offline
verification.

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.19334062.svg)](https://doi.org/10.5281/zenodo.19334062)
[![CI](https://github.com/joy7758/agent-evidence/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/joy7758/agent-evidence/actions/workflows/ci.yml)
![Python 3.11+](https://img.shields.io/badge/python-3.11%2B-blue)
![Semantic Events](https://img.shields.io/badge/semantic%20events-v2.0.0-1f6feb)
![Status](https://img.shields.io/badge/status-experimental-orange)

Agent Evidence is the concrete execution-evidence entry point for the Digital
Biosphere Architecture.

It packages agent/runtime execution into verifiable evidence bundles for offline
verification. It is not the full architecture hub, not the audit control plane,
and not just tracing or logging. For system context, start with
[digital-biosphere-architecture](https://github.com/joy7758/digital-biosphere-architecture);
for the shortest walkthrough, see
[verifiable-agent-demo](https://github.com/joy7758/verifiable-agent-demo); for
post-execution review, see
[aro-audit](https://github.com/joy7758/aro-audit).

## Role

`agent-evidence` is the concrete execution-evidence entry point for packaging
agent/runtime execution into portable bundles that another party can verify
offline.

## Not this repo

- not the full architecture hub
- not the audit control plane
- not just tracing or logging
- not the walkthrough demo
- not the execution-integrity kernel

## Start here

- architecture context -> [digital-biosphere-architecture](https://github.com/joy7758/digital-biosphere-architecture)
- current primary package -> `spec/execution-evidence-operation-accountability-profile-v0.1.md`, `schema/execution-evidence-operation-accountability-profile-v0.1.schema.json`
- current runnable surfaces -> [examples/README.md](examples/README.md), [demo/README.md](demo/README.md), `agent-evidence validate-profile <file>`
- historical lineage -> [docs/lineage.md](docs/lineage.md)
- walkthrough -> [verifiable-agent-demo](https://github.com/joy7758/verifiable-agent-demo)
- post-execution review -> [aro-audit](https://github.com/joy7758/aro-audit)

## EDC / Dataspace augmentation

EDC is a scenario augmentation layer for `agent-evidence`, not a new mainline or a replacement surface.

- boundary -> [docs/edc/EDC_AUGMENTATION_BOUNDARY.md](docs/edc/EDC_AUGMENTATION_BOUNDARY.md)
- minimal profile draft -> [docs/edc/edc_minimal_evidence_profile_draft.md](docs/edc/edc_minimal_evidence_profile_draft.md)
- minimal demo path -> [docs/edc/edc_demo_minimal_path.md](docs/edc/edc_demo_minimal_path.md)
- control-plane event sketch -> [docs/edc/edc_control_plane_event_extension_sketch.md](docs/edc/edc_control_plane_event_extension_sketch.md)
- event mapping -> [docs/edc/edc_event_to_evidence_mapping.md](docs/edc/edc_event_to_evidence_mapping.md)
- extension structure -> [docs/edc/edc_extension_minimal_structure.md](docs/edc/edc_extension_minimal_structure.md)

## Current v0.1 package

The current primary package surface is
`Execution Evidence and Operation Accountability Profile v0.1`.

It is frozen in GitHub Release `v0.2.0`.

Current package DOI: https://doi.org/10.5281/zenodo.19334062

The package version inside that release remains `v0.1`.

Start here for the current v0.1 path:

- Spec: `spec/execution-evidence-operation-accountability-profile-v0.1.md`
- Schema: `schema/execution-evidence-operation-accountability-profile-v0.1.schema.json`
- Validator CLI: `agent-evidence validate-profile <file>`
- Examples: [examples/README.md](examples/README.md)
- Demo: [demo/README.md](demo/README.md)
- Status and acceptance: `docs/STATUS.md`, `docs/ACCEPTANCE-CHECKLIST.md`
- Submission handoff: `submission/package-manifest.md`, `submission/final-handoff.md`

Implementation note: JSONL, SQLite, and PostgreSQL backends remain available,
but they are subordinate to the evidence-entry role of this repository.

![Storage](https://img.shields.io/badge/storage-JSONL%20%7C%20SQLite%20%7C%20Postgres-0a7b83)

### Minimal v0.1 walkthrough

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

The commands below assume the active environment exposes `agent-evidence` on
`PATH`. If you are using the repository virtualenv directly, run
`.venv/bin/agent-evidence ...` instead.

Validate the minimal valid and invalid examples:

```bash
agent-evidence validate-profile examples/minimal-valid-evidence.json
agent-evidence validate-profile examples/valid-trust-binding-evidence.json
agent-evidence validate-profile examples/invalid-missing-required.json
agent-evidence validate-profile examples/invalid-unclosed-reference.json
agent-evidence validate-profile examples/invalid-policy-link-broken.json
agent-evidence validate-profile examples/invalid-trust-binding-digest-mismatch.json
```

Run the minimal demo:

```bash
python3 demo/run_operation_accountability_demo.py
```

Expected result:

- the valid example returns JSON with `"ok": true`
- each invalid example returns JSON with `"ok": false` and one primary error code
- the demo writes artifacts under `demo/artifacts/` and ends with one `PASS` summary line

Known environment note:

- the repository `.venv` may show one `langchain_core` warning under Python 3.14 during broader test runs; it does not affect the minimal profile, validator, or demo path

## Historical lineage

Historical `Execution Evidence Object`, older `Agent Evidence Profile` wording,
legacy FDO mapping language, and conference-specimen notes
remain in this repository, but they are no longer the primary entry surface.
Use [docs/lineage.md](docs/lineage.md) for the historical map and retained
paths.

The historical specimen track still keeps its original DOI:
https://doi.org/10.5281/zenodo.19055948

## Fastest proof

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev,langchain,sql]"
python integrations/langchain/export_evidence.py
agent-evidence verify-bundle --bundle-dir integrations/langchain/langchain-evidence-bundle
```

This runs the documented LangChain exporter and verifies the emitted bundle
offline.

For a smaller callback/export recipe aimed at external readers, see
`docs/cookbooks/langchain_minimal_evidence.md`.

## Why this is not just tracing

Tracing and logs help operators inspect a run. Agent Evidence packages runtime
events into portable artifacts that another party can verify later, including
offline.

Evidence path:

`runtime events -> evidence bundle -> signed manifest -> detached anchor (when present) -> offline verify`

This repository implements the bundle, manifest, signatures, and offline
verification steps. External anchoring is out of scope for AEP v0.1 and is not
enabled by default.

Optional trust bindings are a different concept from manifest signatures. In
the current profile they appear as `validation.trust_bindings[]`, which only
points to an external verification source. They do not replace local signing,
and the validator only checks that the local target and digest are consistent.

The toolkit now supports two storage modes:

- append-only local JSONL files
- SQLAlchemy-backed SQLite/PostgreSQL databases

The current model treats each record as a semantic event envelope:

- `event.event_type` is framework-neutral, such as `chain.start` or `tool.end`
- `event.context.source_event_type` preserves the raw framework event name
- `hashes.previous_event_hash` links to the prior event
- `hashes.chain_hash` provides a cumulative chain tip for integrity checks

### Secure Serialization

The evidence serialization layer implements:

- default redaction of sensitive fields
- maximum recursion depth
- circular reference protection
- object size limits

These protections prevent evidence bundles from leaking secrets or causing
serialization-based denial-of-service conditions.

## Why this shape

The project is organized so evidence capture stays modular:

- `agent_evidence`: core models and recorder logic
- `agent_evidence/crypto`: canonical hashing and chain helpers
- `agent_evidence/storage`: append-only local storage backends
- `agent_evidence/integrations`: adapters for external agent frameworks
- `agent_evidence/cli`: command-line entrypoints
- `agent_evidence/schema`: JSON schema for persisted envelopes
- `examples`: executable usage examples
- `tests`: baseline regression coverage

## Quick start

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev,langchain,sql]"
agent-evidence schema
```

## Agent Evidence Profile v0.1 MVP

The current MVP path is an integrity-verifiable evidence bundle with offline
verification. It is implemented as an Agent Evidence Profile that keeps one
LangChain-first integration path and leaves room for later OpenInference /
OpenTelemetry compatibility mappings.

AEP v0.1 is an integrity-verifiable evidence profile, not a non-repudiation
system.

AEP is an integrity-verifiable evidence profile for autonomous agent runs, with
offline verification and runtime provenance capture.

Generate the first bundle:

```bash
python integrations/langchain/export_evidence.py
agent-evidence verify-bundle --bundle-dir integrations/langchain/langchain-evidence-bundle
```

Run the gate against one valid and one tampered fixture:

```bash
python scripts/run_profile_gate.py
```

## Automaton Sidecar Exporter

The next read-only path is a Conway-neutral Automaton sidecar/exporter. It
reads `state.db`, git history, and persisted on-chain references, then emits an
AEP bundle plus `fdo-stub.json` and `erc8004-validation-stub.json`.

```bash
agent-evidence export automaton \
  --state-db /path/to/state.db \
  --repo /path/to/state/repo \
  --runtime-root /path/to/automaton-checkout \
  --out ./automaton-aep-bundle
```

`agent-evidence export automaton` has been validated against a live isolated-home
Automaton run and remains marked experimental while the live data contract is
still settling.

When `--runtime-root` is provided, the exporter attempts to resolve
`source_runtime_version`, `source_runtime_commit`, and `source_runtime_dirty`
from the Automaton checkout without changing the export path.

## Controlled Release Surface

The controlled specimen release at [v0.1-live-chain](/Users/zhangbin/GitHub/agent-evidence/release/v0.1-live-chain/README.md)
is a historical lineage surface, not the current primary entry.

The historical specimen archive for that track remains on Zenodo with DOI:
https://doi.org/10.5281/zenodo.19055948

It freezes:

- AEP schema
- verify CLI
- LangChain exporter
- Automaton exporter
- live runbook
- public live/tampered fixtures
- AEP boundary statement

See [docs/lineage.md](docs/lineage.md) for how this historical surface relates
to the current Agent Evidence / AEP v0.1 package path.

The formal specimen release note is [RELEASE_NOTE.md](/Users/zhangbin/GitHub/agent-evidence/release/v0.1-live-chain/RELEASE_NOTE.md).

## CLI examples

```bash
agent-evidence record \
  --store ./data/evidence.jsonl \
  --actor planner \
  --event-type tool.call \
  --input '{"task":"summarize"}' \
  --output '{"status":"ok"}' \
  --context '{"source":"cli","component":"tool"}'

agent-evidence list --store ./data/evidence.jsonl
agent-evidence show --store ./data/evidence.jsonl --index 0
agent-evidence verify --store ./data/evidence.jsonl
```

SQL stores use a SQLAlchemy URL instead of a file path:

```bash
agent-evidence record \
  --store sqlite+pysqlite:///./data/evidence.db \
  --actor planner \
  --event-type tool.call \
  --context '{"source":"cli","component":"tool"}'

agent-evidence query \
  --store sqlite+pysqlite:///./data/evidence.db \
  --event-type tool.call \
  --source cli

agent-evidence query \
  --store sqlite+pysqlite:///./data/evidence.db \
  --span-id tool-1 \
  --parent-span-id root \
  --offset 0 \
  --limit 50

agent-evidence query \
  --store sqlite+pysqlite:///./data/evidence.db \
  --previous-event-hash <event-hash> \
  --event-hash-from <lower-bound-hash> \
  --event-hash-to <upper-bound-hash>

agent-evidence export \
  --store ./data/evidence.jsonl \
  --format json \
  --output ./exports/evidence.bundle.json

agent-evidence export \
  --store ./data/evidence.jsonl \
  --format csv \
  --output ./exports/evidence.csv \
  --manifest-output ./exports/evidence.csv.manifest.json \
  --private-key ./keys/manifest-private.pem \
  --key-id evidence-demo

agent-evidence export \
  --store ./data/evidence.jsonl \
  --format xml \
  --output ./exports/evidence.xml \
  --manifest-output ./exports/evidence.xml.manifest.json \
  --private-key ./keys/manifest-private.pem \
  --key-id evidence-demo

agent-evidence export \
  --store ./data/evidence.jsonl \
  --format json \
  --archive-format tar.gz \
  --output ./exports/evidence-package.tgz \
  --private-key ./keys/manifest-private.pem \
  --key-id evidence-demo

agent-evidence export \
  --store ./data/evidence.jsonl \
  --format json \
  --output ./exports/evidence.multisig.json \
  --required-signatures 2 \
  --required-signature-role approver=1 \
  --required-signature-role attestor=1 \
  --signer-config ./keys/operations-q2.signer.json \
  --signer-config ./keys/compliance-q1.signer.json

agent-evidence verify-export \
  --bundle ./exports/evidence.bundle.json \
  --public-key ./keys/manifest-public.pem

agent-evidence verify-export \
  --bundle ./exports/evidence.multisig.json \
  --keyring ./keys/manifest-keyring.json

agent-evidence verify-export \
  --bundle ./exports/evidence.multisig.json \
  --keyring ./keys/manifest-keyring.json \
  --required-signature-role approver=1

agent-evidence verify-export \
  --xml ./exports/evidence.xml \
  --manifest ./exports/evidence.xml.manifest.json \
  --public-key ./keys/manifest-public.pem

agent-evidence verify-export \
  --archive ./exports/evidence-package.tgz \
  --public-key ./keys/manifest-public.pem
```

## Development

```bash
make install
make test
make lint
make hooks
```

The repository includes a `.pre-commit-config.yaml` with baseline whitespace,
JSON, and Ruff checks.

For PostgreSQL support, install the extra driver dependencies:

```bash
pip install -e ".[dev,postgres]"
```

## Semantic event model

Each persisted record follows this shape:

```json
{
  "schema_version": "2.0.0",
  "event": {
    "event_id": "...",
    "timestamp": "2026-03-16T00:00:00+00:00",
    "event_type": "tool.end",
    "actor": "search-tool",
    "inputs": {},
    "outputs": {},
    "context": {
      "source": "langchain",
      "component": "tool",
      "source_event_type": "on_tool_end",
      "span_id": "...",
      "parent_span_id": null,
      "ancestor_span_ids": [],
      "name": "search-tool",
      "tags": ["langchain", "tool"],
      "attributes": {}
    },
    "metadata": {}
  },
  "hashes": {
    "event_hash": "...",
    "previous_event_hash": "...",
    "chain_hash": "..."
  }
}
```

`event_type` is the stable semantic layer. `source_event_type` keeps the
original callback or trace event for lossless debugging.

## LangChain integration

Agent Evidence supports two integration paths for current LangChain runtimes:

- callback handlers for live capture during execution
- stream event adapters for `Runnable.astream_events(..., version="v2")`

Example callback usage:

```python
from agent_evidence import EvidenceRecorder, LocalEvidenceStore
from agent_evidence.integrations import EvidenceCallbackHandler
from langchain_core.runnables import RunnableLambda

store = LocalEvidenceStore("data/evidence.jsonl")
recorder = EvidenceRecorder(store)
handler = EvidenceCallbackHandler(recorder)

chain = RunnableLambda(lambda text: text.upper()).with_config({"run_name": "uppercase"})
result = chain.invoke(
    "hello",
    config={"callbacks": [handler], "metadata": {"session_id": "demo"}},
)
```

Example stream event capture:

```python
import asyncio

from agent_evidence import EvidenceRecorder, LocalEvidenceStore
from agent_evidence.integrations import record_langchain_event
from langchain_core.runnables import RunnableLambda

async def main() -> None:
    store = LocalEvidenceStore("data/evidence.jsonl")
    recorder = EvidenceRecorder(store)
    chain = RunnableLambda(lambda text: text[::-1]).with_config({"run_name": "reverse"})

    async for event in chain.astream_events("hello", version="v2"):
        record_langchain_event(recorder, event)

asyncio.run(main())
```

Both integration paths normalize LangChain callback names such as
`on_chain_start` and `on_tool_end` into semantic event types such as
`chain.start` and `tool.end`.

## OpenAI Agents SDK integration

OpenAI Agents SDK already exposes tracing extension points through custom trace
processors, so Agent Evidence can mirror trace and span lifecycle events into
the same semantic evidence model without patching the runtime.

Install the optional dependency:

```bash
pip install -e ".[openai-agents]"
```

Example trace processor usage:

```python
from agents import trace
from agents.tracing import custom_span

from agent_evidence import EvidenceRecorder, LocalEvidenceStore, export_json_bundle
from agent_evidence.integrations import install_openai_agents_processor

store = LocalEvidenceStore("data/openai-agents.evidence.jsonl")
recorder = EvidenceRecorder(store)
install_openai_agents_processor(recorder)

with trace(
    "support-workflow",
    group_id="session-001",
    metadata={"session_id": "session-001"},
):
    with custom_span("collect_context", {"channel": "chat"}):
        pass

export_json_bundle(
    store.query(source="openai_agents"),
    "exports/openai-agents.bundle.json",
)
```

By default `install_openai_agents_processor()` adds Agent Evidence alongside
the SDK's active processors. Pass `replace=True` if you want the SDK to emit
only into Agent Evidence for that process.

See [`examples/openai_agents/basic_export.py`](examples/openai_agents/basic_export.py)
for a complete local example.

## Verification

Use the CLI to validate the chain after capture:

```bash
agent-evidence verify --store ./data/evidence.jsonl
```

This recomputes each `event_hash`, checks `previous_event_hash`, and validates
the cumulative `chain_hash`.

## SQL storage

`SqlEvidenceStore` persists the semantic event envelope into a relational table
while keeping indexed columns for efficient filtering:

- `event_type`
- `actor`
- `timestamp`
- `source`
- `component`
- `span_id`
- `parent_span_id`
- `previous_event_hash`
- `event_hash`
- `chain_hash`

The query interface supports:

- semantic filters such as `event_type`, `actor`, `source`, and `component`
- chain traversal via `previous_event_hash`
- span-scoped inspection with `span_id` and `parent_span_id`
- time windows via `since` and `until`
- lexicographic hash windows via `event_hash_from/to` and `chain_hash_from/to`
- pagination via `offset` and `limit`

Hash window filters operate on fixed-width lowercase SHA-256 hex digests, so
lexicographic ranges map cleanly to digest ordering for indexed lookups.

The store accepts standard SQLAlchemy URLs, for example:

- `sqlite+pysqlite:///./data/evidence.db`
- `postgresql+psycopg://user:password@localhost:5432/agent_evidence`

## Migration

You can migrate existing JSONL evidence into SQLite or PostgreSQL:

```bash
agent-evidence migrate \
  --source ./data/evidence.jsonl \
  --target sqlite+pysqlite:///./data/evidence.db
```

The `query` command works across both local and SQL stores, although SQL stores
are preferable once record volume grows beyond simple local inspection.

## Bundle export

Agent Evidence supports three export shapes:

- JSON bundles containing `records`, `manifest`, and one or more detached signatures
- CSV artifacts plus a JSON sidecar manifest
- XML artifacts plus a JSON sidecar manifest

Exports can also be packaged as a single `.zip` or `.tar.gz` archive via
`--archive-format`. Packaged exports include:

- the exported artifact
- the sidecar manifest
- a small `package-manifest.json` used to locate those files during verification

Both formats include a manifest with:

- `artifact_digest` for the exported bytes
- ordered event-hash and chain-hash list digests
- first/last event hashes and latest chain hash
- export filters used to produce the artifact

Each signature can also carry:

- `key_id` and `key_version` for key rotation
- `signer` and `role` for audit attribution
- `signed_at` and arbitrary JSON metadata

Manifests can also carry threshold policies:

- `signature_policy.minimum_valid_signatures` for `N-of-M`
- `signature_policy.minimum_valid_signatures_by_role` for role thresholds such
  as `{"approver": 1, "attestor": 1}`

If neither is present, verification defaults to requiring every signature in
the artifact to validate. If only role thresholds are present, the effective
total threshold defaults to the sum of those role requirements.

If a bundle carries signatures, verification is fail-closed: you must provide
`--public-key` or `--keyring`, otherwise verification returns `ok=false`.

Manifest signatures are the repository's built-in verification mechanism.
Optional trust bindings or trust anchors are separate external proof pointers.
They may be attached at the profile layer with `validation.trust_bindings[]`,
but they are not required for `export`, `verify-export`, or
`validate-profile`.

Manifest signing uses Ed25519 PEM keys. To enable signing outside the dev
environment:

```bash
pip install -e ".[signing]"
```

Example key generation with OpenSSL:

```bash
openssl genpkey -algorithm Ed25519 -out ./keys/manifest-private.pem
openssl pkey -in ./keys/manifest-private.pem -pubout -out ./keys/manifest-public.pem
```

Signer config files let you attach multiple signatures during export. Example
`operations-q2.signer.json`:

```json
{
  "private_key": "./operations-q2-private.pem",
  "key_id": "operations",
  "key_version": "2026-q2",
  "signer": "Operations Bot",
  "role": "approver",
  "metadata": {
    "environment": "prod"
  }
}
```

To embed signature policy in the exported manifest, pass:

- `--required-signatures N` for a global `N-of-M` rule
- `--required-signature-role <role>=<count>` one or more times for role rules

`verify-export` will honor the manifest policy by default, or you can override
the global threshold and role thresholds at verification time with the same
flags.

Keyrings let `verify-export` resolve rotated keys by `key_id` and
`key_version`. Example `manifest-keyring.json`:

```json
{
  "keys": [
    {
      "key_id": "operations",
      "key_version": "2026-q1",
      "public_key": "./operations-q1-public.pem"
    },
    {
      "key_id": "operations",
      "key_version": "2026-q2",
      "public_key": "./operations-q2-public.pem"
    }
  ]
}
```

When you export CSV, Agent Evidence writes the CSV artifact and a manifest
sidecar such as `evidence.csv.manifest.json`. Spreadsheet-facing CSV exports
sanitize cells that begin with formula prefixes such as `=`, `+`, `-`, or `@`
to reduce formula injection risk during human review. `verify-export`
validates the manifest summary, exported artifact digest, and every signature
from a provided public key or keyring.

Archive verification also enforces unpacking limits for member count, per-file
size, and total unpacked size so untrusted `.zip` and `.tar.gz` bundles fail
closed before full extraction.

## PostgreSQL integration validation

For a repeatable real-database validation path, use the bundled Docker-backed
integration script:

```bash
make install-postgres
make test-postgres
```

This starts a temporary PostgreSQL container, exports
`AGENT_EVIDENCE_POSTGRES_URL`, and runs `tests/test_postgres_integration.py`
against the live database.
