# Checker Contract

This file defines a minimal checker contract for the third-party-checker handoff.

It is a handoff contract only. There is still no external third-party checker result included.

## Minimum coverage

An external checker implementation should be able to cover at least:

- schema validity against `schema/execution-evidence-operation-accountability-profile-v0.1.schema.json`
- unresolved output refs
- broken evidence-policy refs

## Minimum expected outcomes

The handoff expects the following minimum outcomes:

- canonical valid specimen -> PASS
- canonical invalid unclosed-reference specimen -> FAIL
- supplementary external-context valid specimen -> PASS, if the external checker chooses to include supplementary checking

## Boundary note

This contract does not require a full reproduction of the current repository validator path.
It only defines the smallest re-checking floor needed for independent review of the B1
line.

## Scope note

This handoff does not change canonical B1 counts. Canonical B1 remains `1 valid / 3 invalid / 1 demo`.
Supplementary surfaces remain supplementary.
