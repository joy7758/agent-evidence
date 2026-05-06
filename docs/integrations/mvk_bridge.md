# MVK Execution Integrity Bridge

`fdo-kernel-mvk` is the execution-integrity layer. It proves deterministic
execution, replay validation, checksum/checkpoint integrity, tamper detection,
rollback behavior, and runtime integrity.

`agent-evidence` is the evidence packaging and handoff layer. It provides
evidence validation, signed manifest/export paths, offline verification, and
reviewer-facing handoff packs.

## Handoff Path

In `fdo-kernel-mvk`:

```bash
make demo
make verify-demo
make export-aep
make verify-aep
```

In `agent-evidence`:

```bash
agent-evidence verify-bundle --bundle-dir ../fdo-kernel-mvk/mvk-aep-bundle
```

The MVK bridge bundle is unsigned and local. It is intended as a minimal
AEP-compatible handoff shape from MVK `audit_bundle.json`, not as a replacement
for this repository.

Signed exports, signature verification, portable receipts, and reviewer packs
remain in `agent-evidence`.

## Non-Claim Boundary

This bridge is not legal non-repudiation, not compliance certification, and not
official FDO standard adoption.
