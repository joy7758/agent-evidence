# Security and Concurrency Boundaries

This note records implementation boundaries for local audit and evidence
packaging surfaces.

## Local API Paths

The local API binds to localhost by default. Request-body paths such as
`profile_path` and `bundle_path` are resolved before use and must stay inside
the allowed local root. By default that root is the current working directory.
Set `AGENT_EVIDENCE_ALLOWED_ROOT` to use a narrower or different root.

Direct symlinks are rejected. Paths outside the allowed root are rejected.
`profile_path` must resolve to a regular file, and `bundle_path` must resolve
to a bundle directory.

## LocalStore Atomicity

`LocalEvidenceStore.append_atomic()` holds a file-level mutex on an adjacent
`.lock` file across the full read-tip, build-envelope, append critical section.
On POSIX platforms this uses `fcntl.flock`. Windows uses `msvcrt.locking` for
the same lock file, but deployments that need strong multi-process guarantees
should still validate behavior on their target filesystem.

The base `EvidenceStore.append_atomic()` method is a best-effort default only.
Concurrent-safe stores must override it with storage-specific locking or
transaction behavior.

## Secret Scans

CSV exports and Review Pack secret checks are best-effort safeguards. They are
not comprehensive DLP, compliance certification, or proof that every sensitive
value was detected.
