# Evidence Integrity Hardening Status

## Status

Evidence integrity hardening phase 1 and phase 2 are complete.

Merged PRs:

- #29: deterministic canonicalization for unordered collections
- #30: resource-bound guard for oversized unordered collections
- #31: store-level atomic append for the default `record()` path

Baseline at the time of this note:

- `1af1af8` Merge pull request #31 from joy7758/feature/evidence-atomic-append

## What Was Fixed

### 1. Hash Determinism For Unordered Collections

PR #29 fixed non-deterministic handling of `set` and `frozenset`
values in both AEP canonicalization and runtime evidence serialization.

Before this fix, unordered collection traversal could produce different
canonical forms for semantically equivalent payloads, which could lead to
unstable evidence hashes.

The implementation now uses deterministic canonical normalization and
sorting for unordered collections. Regression tests cover ordinary unordered
collections and mixed-type JSONable sets such as `{1, "1", None}`.

### 2. Resource-Bound Guard For Oversized Unordered Collections

PR #30 added an early size guard for oversized unordered collections.

Oversized `set` and `frozenset` values now fail closed before normalization
and sorting. This avoids resource overuse and avoids non-deterministic
truncation such as `list(my_set)[:limit]`.

Ordered collections such as `list` and `tuple` retain deterministic slicing
behavior.

### 3. Atomic Append For The Default Recording Path

PR #31 moved the default `EvidenceRecorder.record()` path to a store-level
`append_atomic(...)` operation.

The store now owns the critical section for:

- reading the latest chain tip
- generating chain pointers
- computing the chain hash
- persisting the envelope

`LocalEvidenceStore` protects read-tip + build + append with `RLock` and
writes each JSONL envelope as a single line.

`SqlEvidenceStore` protects read-tip + insert with a store-level lock and
SQLAlchemy transaction.

Concurrent tests cover both Local JSONL storage and SQLite-backed SQL storage.

## Verified Behavior

The current test suite verifies that concurrent `record()` calls in the tested
setting:

- produce the expected number of records
- produce exactly one genesis event
- do not produce duplicate `previous_event_hash` values among non-genesis events
- pass `verify_chain()`
- can be traced from latest head back to genesis

## Current Guarantee Boundary

The current implementation covers the tested single-process,
shared-store-instance, default `record()` path.

It does not yet claim:

- cross-process JSONL write safety
- multiple `LocalEvidenceStore` instances writing the same file
- multiple `SqlEvidenceStore` instances writing the same database
- multi-instance service-level database consistency
- PostgreSQL advisory locking
- database tip-row locking
- distributed append consistency

Those remain future hardening work.

## Compatibility

These changes do not modify:

- public schema
- bundle field semantics
- receipt field semantics
- README narrative

Existing hashes for payloads containing `set` or `frozenset` may differ from
earlier non-deterministic outputs. This is an expected correction.

## Recommended Next Hardening Steps

1. Add dependency audit and supply-chain checks, such as `pip-audit`, SBOM
   generation, and Dependabot.
2. Add cross-process JSONL locking if file-backed multi-process writes become a
   supported use case.
3. Add stronger PostgreSQL concurrency controls if multi-instance database
   writes become a supported use case.
4. Improve validator error aggregation and fail-fast behavior.
5. Keep AGT, Review Pack, poster, and submission materials on separate branches.
