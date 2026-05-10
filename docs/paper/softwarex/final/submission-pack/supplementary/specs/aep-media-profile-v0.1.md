# AEP-Media Profile v0.1: Time-Aware Media Evidence for Operation Accountability

## 1. Purpose

AEP-Media Profile v0.1 defines a minimal, local, time-aware media evidence object for operation accountability. It records one operation, the media artifacts used as evidence, the declared time context for those artifacts, and the policy, provenance, evidence, and validation references needed for an independent validator to check the object.

The profile is intentionally small. Its first purpose is to make media evidence a verifiable object before adding real media capture, signing, clock synchronization, or external anchoring.

## 2. Scope

The profile covers one media-bearing operation statement with these top-level sections:

- `profile`: fixed profile identity, `aep-media-evidence-profile@0.1`.
- `statement_id` and `timestamp`: statement identity and creation time.
- `actor`: the agent or component responsible for the operation.
- `subject`: the object or event the operation is about.
- `operation`: the operation under audit, including links to policy, media, and evidence.
- `policy` and `constraints`: the local rule references used by the validator.
- `time_context`: declared timing information for the media evidence.
- `media`: one or more local artifacts, including hash, size, role, path, and declared timing metadata.
- `provenance`: links from actor, subject, operation, media, and optional manifest artifact.
- `evidence`: the evidence object and the artifacts/policies it binds.
- `validation`: the expected validator method and required checks.

## 3. Non-claims

- This profile does not prove legal admissibility.
- This profile does not provide non-repudiation.
- This profile does not parse real MP4 PRFT boxes in v0.1.
- This profile does not perform real PTP synchronization in v0.1.
- This profile does not create or verify real C2PA signatures in v0.1.
- It only validates a declared, local, minimal media evidence object.

## 4. Object model

An AEP-Media statement binds operation accountability to media evidence through local references:

- `operation.subject_ref` resolves to `subject.id`.
- `operation.policy_ref` resolves to `policy.id`.
- `operation.media_refs` resolve to `media.artifacts[].id`.
- `operation.evidence_refs` resolve to `evidence.id` or `evidence.artifact_refs`.
- `policy.constraint_refs` resolve to `constraints[].id`.
- `provenance.actor_ref`, `subject_ref`, and `operation_ref` resolve to their top-level objects.
- `provenance.media_refs` resolve to media artifacts.
- `provenance.c2pa_manifest_ref`, when present, resolves to a media artifact.
- `evidence.policy_refs` resolve to `policy.id`.
- `evidence.artifact_refs` resolve to media artifacts.

The `time_context` section is a declared timing context. In v0.1, `source` may be `ptp`, `system_clock`, or `declared_demo`, but the validator only checks field presence, time ordering, and artifact reference closure. A `declared_demo` source is appropriate for the included examples and demo.

## 5. Validation checks

The v0.1 validator performs these checks:

- Profile identity: `profile.name` must be `aep-media-evidence-profile`, and `profile.version` must be `0.1`.
- Required field completeness: all required top-level sections must exist, including `time_context`.
- Schema conformance: object structure and basic field types must match the JSON Schema.
- Reference closure: policy, constraint, media, evidence, provenance, and optional manifest references must resolve locally.
- Media hash recomputation: local artifact files are read relative to the evidence JSON file and checked against `media.artifacts[].sha256`.
- Media size check: local artifact file sizes are checked against `media.artifacts[].size_bytes`.
- Time relation: `time_context.start_utc` and `time_context.end_utc` must exist, and `end_utc` must not be earlier than `start_utc`.
- Primary media timing: every `role=primary_media` artifact must carry a `time_context_ref` equal to `time_context.id`.

## 6. Example commands

```bash
agent-evidence validate-media-profile examples/media/minimal-valid-media-evidence.json
agent-evidence validate-media-profile examples/media/invalid-missing-time-context.json
agent-evidence validate-media-profile examples/media/invalid-broken-media-hash.json
agent-evidence validate-media-profile examples/media/invalid-unresolved-policy-ref.json
python demo/run_media_evidence_demo.py
```

The valid example should pass. The invalid examples are controlled failures: one missing timing context, one broken media hash, and one unresolved policy reference.

## 7. Future integration points

- PTP clock trace collection
- FFmpeg PRFT extraction
- C2PA manifest signing / verification
- pFDO-style bundle packaging
- external anchoring or transparency log
