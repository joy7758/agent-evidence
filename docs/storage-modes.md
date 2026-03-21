# Storage Modes

`agent-evidence` supports two canonical storage modes.

## JSONL

- append-only local event chain
- minimal operational surface
- useful for CLI demos, fixtures, and offline bundle export

## SQLite and PostgreSQL

- SQLAlchemy-backed storage
- query support for event type, source, span, and hash-chain traversal
- suitable when evidence must be inspected or filtered without rewriting bundles

## Shared constraints

- schema compatibility is preserved across storage backends
- serialization defaults include redaction, recursion limits, and object-size limits
- exported bundles should preserve the same semantic envelope regardless of storage backend
