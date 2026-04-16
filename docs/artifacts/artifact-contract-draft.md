# Artifact Contract Draft

Scope: `agent-evidence` only.

Grounding surfaces used for this draft:

- `docs/reports/repo-map-audit.md`
- `README.md`
- `docs/quickstart.md`
- `examples/langchain_minimal_evidence.py`
- `spec/execution-evidence-operation-accountability-profile-v0.1.md`
- `schema/execution-evidence-operation-accountability-profile-v0.1.schema.json`
- `agent_evidence/oap.py`
- one current generated output set from the LangChain quickstart path:
  - `bundle`: `/tmp/agent-evidence-quickstart/langchain-evidence.bundle.json`
  - `receipt`: `/tmp/agent-evidence-quickstart/receipt.json`
  - `summary`: `/tmp/agent-evidence-quickstart/summary.json`

This draft is product-facing. It does not define a new schema. It records the minimum artifact contract already visible in current repo surfaces.

## 1. Primary Outputs vs Supporting Files

| Type | Current normalized name | Current examples | Contract status |
| --- | --- | --- | --- |
| Primary output | `bundle` | `langchain-evidence.bundle.json` | Primary product output |
| Primary output | `receipt` | `receipt.json`, `validate-profile` JSON, `validation-report.json` | Primary product output |
| Primary output | `summary` | `summary.json`, demo PASS/FAIL review lines | Primary product output |
| Supporting file | manifest sidecar | `langchain-evidence.manifest.json` | Supporting export material, not a primary output name |
| Supporting file | verification key | `manifest-public.pem` | Supporting verification material |
| Supporting file | signing key | `manifest-private.pem` | Supporting local demo material only |
| Supporting file | runtime capture | `runtime-events.jsonl` | Supporting runtime/export material |

Working rule:

- product-facing language should normalize to `bundle`, `receipt`, and `summary`
- supporting files may exist around those outputs, but they are not additional primary artifact types

## 2. Bundle Minimum Contract

Current bundle carrier in the quickstart path is one JSON document with three top-level fields:

- `manifest`
- `records`
- `signatures`

### Minimum required fields

At minimum, a current JSON `bundle` should preserve:

- `manifest.export_format`
- `manifest.generated_at`
- `manifest.record_count`
- `manifest.artifact_digest`
- `manifest.event_hash_list_digest`
- `manifest.chain_hash_list_digest`
- `manifest.signature_policy`
- `records[]`
- for each record:
  - `schema_version`
  - `event`
  - `hashes`
- for each `event`:
  - `event_id`
  - `timestamp`
  - `event_type`
  - `actor`
  - `context`
  - `inputs`
  - `outputs`
  - `metadata`
- for each `hashes` object:
  - `event_hash`
  - `chain_hash`
  - `previous_event_hash`
- `signatures[]`
  - when signatures are present, each signature must preserve:
    - `algorithm`
    - `signature`
    - `signed_at`
    - any available signer metadata such as `key_id`, `key_version`, `signer`, `role`, `metadata`

### What makes a bundle portable/reviewable

A current `bundle` is portable and reviewable when it keeps all of the following together:

- the exported evidence records themselves
- the manifest digests and counts needed to re-check integrity
- the chain-hash progression needed to reason about event order and continuity
- any signatures that let another party verify the manifest later

The sidecar manifest file is useful support material, but the bundle itself already carries the manifest and signatures. Portability should not depend on a second naming layer.

### Which fields are canonical evidence fields

In the current bundle surface, the canonical evidence-bearing fields are:

- `records[].event.*`
- `records[].hashes.*`
- `manifest.*`
- `signatures[]` when present

Local paths, temp directories, shell commands, and review notes are not bundle fields and must not be treated as canonical evidence.

## 3. Receipt Minimum Contract

Current receipts are command-specific JSON verification results. The repo currently emits them from at least these surfaces:

- `agent-evidence verify-export`
- `agent-evidence verify-bundle`
- `agent-evidence validate-profile`

They do not yet share one explicit schema, so the contract here is the minimum common product-facing surface.

### Minimum required fields

Every `receipt` should preserve at least:

- `ok`
- machine-readable issue or failure material
  - `issues[]` when the verifier emits flat issues
  - or staged issue lists when the verifier emits `stages[]`
- verification scope
  - `format` for export verification receipts
  - or `profile` plus `source` for profile-validation receipts
- at least one scale/count field
  - `record_count`
  - or `issue_count`

When signature verification is in scope, the receipt should also preserve:

- `signature_present`
- `signature_count`
- `required_signature_count`
- `signature_verified`
- `signature_results[]`

When chain integrity is in scope, the receipt should preserve:

- `latest_chain_hash`

### What must be preserved from verification results

The receipt is the machine-readable verification result. It must preserve:

- pass/fail state
- exact machine-readable issue data as emitted by the verifier
- enough context to know what was verified
- counts and signature results needed to interpret the outcome

### Which fields are canonical versus presentation-only

Canonical receipt facts:

- `ok`
- `issues[]` or stage issue payloads
- `profile`, `source`, or `format`
- `record_count` / `issue_count`
- `latest_chain_hash` when present
- signature policy and signature verification results when present

Presentation-only receipt fields:

- any human summary lines such as `summary[]`
- CLI stderr wording
- local output filenames chosen by one example or shell command

Important note:

- the current OAP validator includes `summary[]` inside its JSON report
- that convenience rendering is useful, but it should still be treated as presentation-layer material rather than a canonical schema obligation for every receipt type

## 4. Summary Minimum Contract

Current `summary` is reviewer-facing output. In the LangChain quickstart path it is a JSON file that combines high-level run context with an embedded verification result.

### Minimum required fields

To function as a reviewer-facing `summary`, the current surface should preserve at least:

- overall outcome: `ok`
- pointer to the produced `bundle`
  - for example `bundle_path`
- enough run context to orient a reviewer
  - for example `record_count`
  - and `signature_count`
- a way to re-run or inspect verification
  - `verify_command`
  - and/or an embedded or linked receipt such as `verify_result`

### What makes a summary reviewer-facing rather than evidence-canonical

A `summary` is for orientation and review, not for canonical evidence closure. Its job is to answer:

- what was produced
- whether the current run passed
- where the reviewer should look next

### Distinguish summary content from verification facts

Verification facts belong in the `receipt`.

Summary-only or review-only content includes:

- `output_dir`
- `bundle_path`
- `manifest_path`
- `store_path`
- `private_key_path`
- `public_key_path`
- `verify_command`
- `anchor_note`

The current `summary` may embed `verify_result`, but that embedded copy is convenience content. The authoritative verification facts still belong to the `receipt` surface.

## 5. Evidence-Origin Fields vs Review/Presentation Fields

### Evidence-origin fields

Fields that come from core evidence or verification logic:

- bundle record payloads: `records[].event.*`
- bundle hash-chain payloads: `records[].hashes.*`
- manifest digests, counts, filters, timestamps, signature policy
- manifest signatures and signature metadata
- OAP statement fields defined by the current spec/schema:
  - `actor`
  - `subject`
  - `operation`
  - `policy`
  - `constraints`
  - `provenance`
  - `evidence`
  - `validation`
- machine-readable verification facts emitted by validators and verifiers

### Review/presentation fields

Fields that belong only to review, rendering, or local operator convenience:

- `summary[]` text lines
- `verify_command`
- `output_dir`
- local file paths
- shell snippets
- explanatory notes such as `anchor_note`
- smoke-check wording
- any future reviewer annotations or pack-level commentary

### What must NOT back-propagate into canonical schema

The following should not be pushed back into the canonical profile schema just because they are helpful in product docs or summary files:

- `receipt.json` and `summary.json` filenames
- local path fields such as `bundle_path` or `output_dir`
- `verify_command`
- reviewer notes
- review-pack layout fields
- presentation-only summary lines

## 6. Implementation-Specific Filenames vs Canonical Artifact Names

| Canonical product name | Current implementation-level names | Contract stance |
| --- | --- | --- |
| `bundle` | `langchain-evidence.bundle.json`, bundle directories used by `verify-bundle` | Normalize product language to `bundle`; do not promote path-specific filenames to canonical names |
| `receipt` | `receipt.json`, JSON from `validate-profile`, demo `validation-report.json` | Normalize product language to `receipt`; `validation-report.json` is an implementation filename, not a fourth artifact type |
| `summary` | `summary.json`, demo PASS/FAIL summary lines | Normalize product language to `summary`; keep filename choices implementation-level |

Supporting filenames that remain supporting only:

- `langchain-evidence.manifest.json`
- `manifest-public.pem`
- `manifest-private.pem`
- `runtime-events.jsonl`

## 7. Open Questions Deferred to Later Review Pack Work

- Should `summary` always embed the full `receipt`, or should it only point to it?
- Should the repo later define one normalized receipt schema across `validate-profile`, `verify-export`, and `verify-bundle`?
- Should reviewer-facing summaries have one stable minimal template across quickstart, demo, and future review-pack flows?
- Should implementation filenames become more uniform across examples, or remain path-specific while the product language stays normalized?
- Should the sidecar manifest remain a visible supporting file in developer paths, or become an internal implementation detail later?

These are deferred questions. They should not be solved here by inventing a new schema or adding a new artifact type.

## 8. Non-Goals

- no schema change
- no exporter expansion
- no cross-repo changes
- no EDC expansion
- no audit-plane expansion
- no new primary artifact type beyond `bundle`, `receipt`, and `summary`
