# Security Policy

`agent-evidence` is a narrow local package for runtime evidence export,
operation-accountability profile validation, offline bundle verification,
verification receipts, signed export metadata, and reviewer-facing review
packs.

## Supported Versions

Security review covers:

- the current `main` branch
- the `v0.6.x` release line

Older release lines may be useful for historical reproducibility, but they are
not the active security-support target.

## Security Scope

In-scope security areas are:

- local evidence packaging
- profile validation
- offline bundle verification
- signed export metadata
- verification receipts
- reviewer-facing review packs

Out-of-scope areas include hosted verification services, remote attestation,
legal non-repudiation, compliance certification, and production forensic
timestamping.

## Reporting Vulnerabilities

Report suspected vulnerabilities through GitHub security advisories when
available, or open a GitHub issue with a minimal non-sensitive reproduction.

Do not include private keys, tokens, credentials, production secrets, sensitive
runtime evidence, or private customer data in reports, issues, pull requests,
logs, or test fixtures.

Useful reports include:

- affected command, file, or package surface
- expected and actual behavior
- minimal redacted input needed to reproduce the issue
- whether the issue affects validation, export, bundle verification, signed
  metadata, or review-pack generation

## Key Handling

Maintainers and contributors must not commit:

- private keys
- tokens
- credentials
- production secrets
- sensitive runtime evidence
- unredacted private logs or review packs

Signed export tests and examples should use test fixtures only. Do not reuse
production signing material in this repository.

## Maintainer Security Review Areas

Security-sensitive pull requests should be reviewed for:

- signed export metadata
- manifest and hash verification
- bundle path traversal risks
- untrusted input validation
- JSON, CSV, and XML export safety
- offline verification receipts
- dependency updates
- GitHub Actions workflow permissions

## Claim Boundaries

This project does not claim:

- legal non-repudiation
- court-grade audit proof
- regulatory certification
- AI Act approval
- production forensic timestamping
- official FDO standard status
- hosted verification service
- default sandboxing or access control
