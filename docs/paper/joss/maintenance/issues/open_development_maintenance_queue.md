# Open Development Maintenance Queue

Date: 2026-06-01

This queue is for meaningful public maintenance during the JOSS waiting period.
It should not be treated as an optics exercise. Do not create fake issues or
busywork.

## A. Documentation

- Completed locally in Mission 036: improve the AEP-Media quickstart with the mobile-video-style fixture.
- Completed locally in Mission 036: add a walkthrough for validate/build/verify/strict-time commands.
- Add FAQ: what AEP-Media does and does not prove.
- Completed locally in Mission 036: add adapter boundary documentation.
- Add an examples index for `examples/media/`.

## B. Tests

- Completed locally in Mission 036: add a regression test for the mobile-video-style fixture.
- Add CLI smoke tests for adapter ingestion commands.
- Add checksum/path-safety regression cases if not already covered.
- Add benchmark-script dry-run testing if feasible without large artifacts.

## C. Examples

- Add one tiny synthetic fixture variant with missing PRFT-like metadata.
- Add one LinuxPTP-like log variant.
- Add one C2PA-like sidecar variant.
- Keep all fixtures small, synthetic, and privacy-safe.

## D. CI / Packaging

- Confirm GitHub Actions passes on pull requests.
- Add or refresh badges only after workflows pass.
- Check package metadata for JOSS expectations.

## E. Release Hygiene

- Prepare `aep-media-v0.1.1` after meaningful fixes land.
- Update `CHANGELOG.md`.
- Archive the release if Zenodo integration is configured.

## F. Community / Issue Workflow

- Open meaningful self-issues for real improvements.
- Link commits and PRs to issues.
- Close issues with explanation and test evidence.
- Do not create fake discussion or imply external adoption without evidence.

## G. Paid External Review Protocol

- Completed locally in Mission 036A: create a paid external review protocol for
  real reproduction review, adapter-boundary review, and small mobile-fixture
  regression PRs.
- Use only narrowly scoped paid tasks with public GitHub issue or PR
  deliverables.
- Disclose paid review or paid contribution where relevant.
- Do not pay for stars, praise-only comments, fake issues, fake PRs, citation,
  authorship, or publication outcomes.
- Recommended first paid task: Task A reproducibility review from a fresh clone.

## Mission 036 Local Completion

Issue drafts 001, 002, and 003 were implemented locally without opening GitHub
issues because `AEP_MEDIA_OPEN_MAINTENANCE_ISSUES` was not set to `1`.

Next useful maintenance candidates:

- identify one external reviewer and open a real Task A reproduction issue only
  after the reviewer agrees to perform the work;
- add an examples index for `examples/media/`;
- add CLI smoke tests for adapter ingestion commands;
- add one tiny adapter fixture variant per adapter family;
- prepare a real `aep-media-v0.1.1` maintenance release after meaningful public
  changes land.
