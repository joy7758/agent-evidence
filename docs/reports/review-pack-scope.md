# Review Pack Scope

Scope: `agent-evidence` only.

Grounding surfaces used for this draft:

- `docs/artifacts/artifact-contract-draft.md`
- `docs/quickstart.md`
- `README.md`
- `examples/langchain_minimal_evidence.py`
- `agent_evidence/integrations/langchain.py`
- `agent_evidence/integrations/openai_compatible/`
- `tests/test_quickstart_smoke.py`
- `tests/test_openai_compatible_adapter.py`

This draft defines the first commercial Review Pack as a packaging and rendering
layer above the current `bundle` / `receipt` / `summary` contract. It does not
define a new schema or a new canonical artifact type.

## 1. What Review Pack Is

### Product goal

Review Pack is the first commercial layer that turns current machine-facing
artifacts into a reviewer-facing handoff package.

Its job is to:

- package the current primary outputs together
- render verification facts into a readable review surface
- preserve a clear line back to the underlying evidence artifacts

### Target reader

The first target readers are:

- engineering managers
- AI platform engineers
- internal reviewers or audit-adjacent operators

The target reader is someone who needs to decide whether a run is reviewable,
verifiable, and handoff-ready without manually navigating raw artifact files.

### Why it is not just raw artifacts

The current raw artifacts are already correct, but they still require the
reader to do manual correlation:

- open the `summary`
- inspect the `receipt`
- find the right `bundle`
- translate machine-readable failures into a reviewer-facing explanation

Review Pack is the layer that assembles those materials into one bounded
review surface without changing what counts as canonical evidence.

## 2. Review Pack Primary Contents

### Included primary contents

The first Review Pack should include the existing primary outputs only:

- `bundle`
- `receipt`
- `summary`

In addition, it should include one rendered review report derived from those
three sources.

That rendered review report is product-facing, but it is not a new canonical
artifact type. It is a packaging/rendering file inside the Review Pack.

### Optional or supporting contents

Supporting files should remain optional/supporting:

- manifest sidecar
- verification public key
- runtime JSONL capture

Supporting files may help with:

- offline re-verification
- deeper diagnostics
- provenance of how the pack was assembled

They should not become additional primary outputs.

### Explicit exclusions

The local signing private key should not be included in a commercial Review Pack
by default, even if it exists in local demo/example surfaces today.

## 3. Source-of-Truth Mapping

### What comes from `bundle`

`bundle` remains the source of truth for:

- exported evidence records
- event ordering and chain continuity
- manifest digests and counts
- signature material attached to the manifest
- runtime/context fields captured by the adapter path

### What comes from `receipt`

`receipt` remains the source of truth for:

- pass/fail verification outcome
- machine-readable issue lists
- signature verification results
- chain verification result
- record counts and latest chain hash
- verification scope such as export/profile format context

### What comes from `summary`

`summary` remains the source of truth for reviewer orientation only:

- which run/package is being discussed
- where the `bundle` and `receipt` live
- high-level counts such as `record_count`, `signature_count`, or `call_count`
- adapter-facing run context such as `provider_label`, `model`, or `base_url`
- re-run hints such as `verify_command`

### What must never become a new canonical evidence field

The following must remain outside canonical evidence:

- Review Pack folder layout fields
- rendered headings and section labels
- severity labels added for reviewer readability
- report prose or recommended next steps
- checklists, badges, or status decorations
- local file path conventions
- source filename normalization used only by the package

## 4. Failure Taxonomy Surface

### Failure classes to expose to reviewers

The first Review Pack should expose reviewer-facing failure classes such as:

- integrity failure
- chain continuity failure
- signature failure
- signature policy failure
- profile validation failure
- packaging incompleteness warning

### Which are verification facts

Verification facts must come from `receipt` only:

- `ok`
- `issues[]`
- signature verification flags and counts
- chain verification outputs
- profile-validation issue payloads when that receipt type is in scope

### Which are presentation labels

Presentation labels may be introduced by Review Pack, but only as render-time
labels above receipt facts:

- `Integrity failed`
- `Signature missing`
- `Receipt passed with warnings`
- `Review blocked`
- `Optional support material missing`

These labels must be reproducible from existing receipt facts and must not be
written back into canonical schema or evidence records.

## 5. Verification Report Shape

The first rendered review report should include at least these sections:

### 1. Verdict

- overall pass/fail result
- one short reviewer-facing explanation

### 2. What Was Reviewed

- artifact identifiers or normalized artifact names
- adapter/runtime context from `summary`
- high-level counts such as records and signatures

### 3. Verification Findings

- failure classes or warnings
- linked machine-readable issues from `receipt`
- signature and chain status

### 4. Evidence References

- pointer to the included `bundle`
- pointer to the included `receipt`
- pointer to the included `summary`
- optional pointer to supporting materials when present

### 5. Reviewer-Facing Explanation

- a short explanation of why the package passed or failed
- next review step guidance such as:
  - inspect the bundle
  - rerun verification
  - escalate signature failure

This explanatory text is presentation-only. It must not replace receipt facts.

## 6. Packaging/Layout Proposal

### Minimal folder/file layout

The first Review Pack should normalize its root layout to reviewer-facing names:

```text
review-pack/
  bundle.json
  receipt.json
  summary.json
  review-report.md
  supporting/
    manifest.json
    manifest-public.pem
    runtime-events.jsonl
```

### Naming rules

Product-facing names inside the pack root should stay normalized:

- `bundle.json`
- `receipt.json`
- `summary.json`
- `review-report.md`

Implementation-specific source filenames such as
`langchain-evidence.bundle.json` should be treated as source-path details, not
as the product-facing naming layer of the pack.

### Product-facing vs implementation-facing

Product-facing:

- normalized root artifact names
- rendered report layout
- reviewer headings and summaries

Implementation-facing:

- source output filenames from examples/adapters
- local output directories
- private adapter temp paths
- pack assembly internals

## 7. Lowest-Risk Implementation Sequence

### Implement first

1. Define one adapter-agnostic pack assembler that consumes current
   `bundle` / `receipt` / `summary` without requiring schema changes.
2. Generate one rendered review report from existing receipt + summary fields.
3. Package normalized root files plus optional supporting materials.

### Implement second

1. Add fixture-based tests that prove both current adapter lines can assemble
   the same Review Pack shape:
   - LangChain path
   - OpenAI-compatible path
2. Verify that rendered failure classes are derived from receipt facts rather
   than invented independently.

### What should explicitly wait

- any new canonical artifact type
- any CLI surface for Review Pack
- any live-provider hardening work
- any hosted delivery or sharing workflow
- any review annotations or collaboration workflow
- any cross-repo review-pack integration

### What must not be changed

- canonical schema
- current `bundle` / `receipt` / `summary` contract
- adapter-specific artifact generation logic
- existing quickstart semantics
- supporting-files-as-supporting rule

## 8. Non-Goals

- no schema changes
- no exporter expansion
- no CLI changes
- no cross-repo work
- no live-provider hardening work
- no new canonical artifact types
- no attempt to push Review Pack labels back into core evidence fields
