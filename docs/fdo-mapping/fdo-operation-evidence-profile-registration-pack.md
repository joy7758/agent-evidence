# FDO Operation Evidence Profile Registration Pack

This note turns the current repository package into one FDO-facing registration
pack without creating a second implementation surface.

## 1. Naming Boundary

Use the following names consistently:

| Purpose | Value |
| --- | --- |
| Repository canonical package name | `Execution Evidence and Operation Accountability Profile v0.1` |
| Repository machine-readable profile id | `execution-evidence-operation-accountability-profile@0.1` |
| Proposed FDO-facing object name | `FDO_OPERATION_EVIDENCE_PROFILE_V0_1` |
| Proposed FDO-facing object type | `Profile` |

The FDO-facing name is an external registration label. It should point to the
current canonical package already implemented in this repository. It should not
trigger a rename of the existing schema, validator, examples, or demo.

## 1.1 Relationship To `ARO_AUDIT_PROFILE_V1`

Use the following external naming relationship:

| Object | Role |
| --- | --- |
| `FDO_OPERATION_EVIDENCE_PROFILE_V0_1` | operation-level evidence and validation profile for one agent or service operation |
| `ARO_AUDIT_PROFILE_V1` | audit-facing sibling profile used to declare audit-ready object support and audit pointers |

They are related but not interchangeable:

- `FDO_OPERATION_EVIDENCE_PROFILE_V0_1` focuses on one bounded operation
  accountability statement.
- `ARO_AUDIT_PROFILE_V1` focuses on audit-ready object declaration and audit
  trace support.
- The new FDO-facing object should be presented as complementary to
  `ARO_AUDIT_PROFILE_V1`, not as a rename or replacement.

## 2. Current Repository Assets To Link

The current repository already contains the minimum package needed for an
FDO-facing registration:

| Purpose | File |
| --- | --- |
| Spec | `spec/execution-evidence-operation-accountability-profile-v0.1.md` |
| Schema | `schema/execution-evidence-operation-accountability-profile-v0.1.schema.json` |
| Valid example | `examples/minimal-valid-evidence.json` |
| Invalid examples | `examples/invalid-missing-required.json`, `examples/invalid-unclosed-reference.json`, `examples/invalid-policy-link-broken.json` |
| Validator implementation | `agent_evidence/oap.py` |
| Validator CLI entry | `agent_evidence/cli/main.py` |
| Demo | `demo/run_operation_accountability_demo.py` |
| Demo guide | `demo/README.md` |
| Repo overview | `README.md` |

If a dedicated GitHub repository is created later, these files are the minimal
subset to copy first.

## 3. Mapping From Flat Outreach Terms To Canonical Fields

The flat example often used in outreach is narrower than the canonical
statement shape. The mapping below keeps the external explanation short while
preserving the actual implemented structure.

| Flat outreach term | Canonical field path |
| --- | --- |
| `operation_id` | `operation.id` |
| `agent_id` | `actor.id` |
| `input_hash` | `evidence.references[]` entry with `role = "input"` -> `digest` |
| `output_hash` | `evidence.references[]` entry with `role = "output"` -> `digest` |
| `operation_type` | `operation.type` |
| `policy_reference` | `policy.id` and `operation.policy_ref` |
| `provenance_chain` | `provenance.*` links plus `evidence.artifacts[]` |
| `signature` | not a core v0.1 field; use local integrity digests and optional `validation.trust_bindings[]` |
| `verification_result` | `validation.status` plus validator report `ok` |

## 4. Suggested FDO Testbed Registration Text

Recommended object name:

`FDO_OPERATION_EVIDENCE_PROFILE_V0_1`

Recommended description:

`A minimal profile for recording and validating one policy-constrained agent operation with explicit policy, provenance, evidence, and validation links.`

Recommended type:

`Profile`

Recommended GitHub landing surface:

- repository root `README.md`
- spec document
- schema file
- valid example
- validator entry
- demo guide

## 5. Manual External Steps Still Required

The repository can prepare the registration pack, but these actions still
require manual completion outside the local workspace:

1. Create or choose the GitHub repository that will host the public package.
2. Log into the FDO Testbed Type Registry.
3. Submit the new object entry and paste the public GitHub links.
4. Share the resulting registry URL in the outreach email and proposal note.

Until those actions are completed, treat this pack as submission-ready draft
material rather than an already registered object.
