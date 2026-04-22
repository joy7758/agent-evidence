# Mapping AGT runtime evidence to EEOAP v0.1

This note defines a minimal, non-invasive interoperability path from
Microsoft Agent Governance Toolkit runtime evidence into the Execution Evidence
and Operation Accountability Profile v0.1.

## Scope

This mapping does not modify AGT runtime governance, policy enforcement,
identity, or sandboxing behavior.

It treats AGT as an upstream runtime governance source and EEOAP v0.1 as an
external operation-accountability statement format.

## Pipeline

```text
AGT runtime event / evidence
-> AGT-to-EEOAP adapter
-> EEOAP v0.1 statement
-> agent-evidence validate-profile
-> offline validation result
```

## Non-goals

- No AGT runtime changes
- No AGT policy-engine changes
- No new EEOAP v0.1 fields
- No dependency on AGT internals
- No replacement of `agt verify --evidence`

## Mapping

| AGT concept | EEOAP v0.1 field |
|---|---|
| Agent identity | `actor` |
| Governed action/tool call | `operation` |
| Governed resource/object | `subject` |
| Policy decision | `policy` / `constraints` |
| Runtime audit material | `evidence.artifacts` |
| Input/output material | `evidence.references` |
| Runtime linkage | `provenance` |
| Independent profile validation | `validation` |

## Boundary

AGT verifies governance evidence within its own runtime-governance model.

EEOAP v0.1 verifies whether a single operation-accountability statement is
structurally complete, internally consistent, and independently checkable.

The adapter keeps AGT-specific material out of the EEOAP top level. Runtime
receipts, policy decisions, and synthetic source evidence are represented as
`evidence.artifacts[]` entries or artifact locators.
