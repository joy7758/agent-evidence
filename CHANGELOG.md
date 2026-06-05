# Changelog

This project uses a concise Keep a Changelog-style record for notable public
changes. Older release history is available through GitHub releases and git
history.

## Unreleased

### Added

- Mobile-video fixture walkthrough documentation.
- Adapter boundary documentation.
- Mobile-video fixture regression tests.

### Changed

- README links for AEP-Media documentation.

## [aep-media-v0.1.0] - 2026-05-10

### Added

- AEP-Media media evidence profile validator.
- Offline media bundle builder and verifier.
- Strict declared time-trace validation.
- LinuxPTP-style, FFmpeg PRFT-style, and C2PA-like adapter ingestion commands.
- Bounded AEP-Media evaluation matrices.
- Fixture-only mobile-video-style use case.
- AEP-Media Zenodo archive DOI: `10.5281/zenodo.20107097`.
- Documentation, examples, tests, schemas, specs, and release package.

### Known Limitations

- Local validation only.
- No legal admissibility claim.
- No chain-of-custody claim.
- No non-repudiation claim.
- No trusted timestamping claim.
- No real PTP proof.
- No full MP4 PRFT parser.
- No real C2PA signature verification.
- No production deployment claim.

## [v0.6.0] - 2026-05-03

### Added

- Review Pack release surface for broader `agent-evidence` operation-evidence
  workflows.

## [v0.1.0] - 2026-03-15

### Added

- Initial public Agent Evidence release.
- Minimal evidence capture, validation, and local bundle concepts.
