# Mission 036G Agent Discoverability Audit Report

Date: 2026-06-02

## 1. Mission Summary

Mission 036G audited and improved the AEP-Media agent-readable discovery path
from the GitHub README into `llms.txt`, `docs/aep-media/agent-index.md`, the
mobile-video walkthrough, and external review task materials.

The audit found that README and agent-facing files referenced several
discoverability target files that were still untracked locally. The scoped
commit therefore includes the linked AEP-Media docs, mobile-video fixture,
adapter README, JOSS paper draft, contribution/support docs, and mobile fixture
regression test needed to avoid broken GitHub links.

No implementation code was changed. No validator, schema, adapter, or
evaluation semantics were changed. No JOSS submission was performed. No GitHub
issue was created.

## 2. Baseline

- Branch: `opentelemetry-to-eeoap-adapter`
- Mission-start commit: `6a83721 Record agent-readable recruitment commit status`
- README dirty status at start: dirty, with AEP-Media entry-point links from
  prior local work.
- README linked `llms.txt` at start: no.
- README linked `docs/aep-media/agent-index.md` at start: no.
- README linked mobile-video walkthrough at start: yes, but the target file was
  not yet tracked.
- README linked contribution/review tasks at start: contribution/support links
  were present; external review task body was not linked from README.

## 3. README Links Added

Yes.

Added a short `Agent-readable project entry points` section and direct links to:

- `llms.txt`
- `docs/aep-media/agent-index.md`
- `docs/aep-media/mobile-video-walkthrough.md`
- `docs/aep-media/adapter-boundaries.md`
- `paper/paper.md`

## 3A. Discoverability Dependencies Included

Yes.

Included to avoid broken links from README, `llms.txt`, and
`docs/aep-media/agent-index.md`:

- `docs/aep-media/README.md`
- `docs/aep-media/mobile-video-walkthrough.md`
- `docs/aep-media/adapter-boundaries.md`
- `examples/media/use_cases/mobile_video_network_timing/`
- `examples/media/adapters/README.md`
- `tests/test_media_mobile_video_fixture.py`
- `paper/paper.md`
- `paper/paper.bib`
- `CONTRIBUTING.md`
- `SUPPORT.md`

## 4. Agent Index Reachable

Yes.

The path is:

`README.md -> llms.txt -> docs/aep-media/agent-index.md`

## 5. Mobile Walkthrough Reachable

Yes.

The path is:

`README.md -> docs/aep-media/mobile-video-walkthrough.md`

The walkthrough file is included in the scoped discoverability commit to avoid
publishing a broken link.

## 6. Recruitment Issue Body Reachable

Yes.

The path is:

`docs/aep-media/README.md -> docs/paper/joss/maintenance/recruitment/github_recruitment_issue_body.md`

and

`docs/aep-media/README.md -> docs/paper/joss/maintenance/issues/task_A_github_issue_body.md`

## 7. Red-Line Scan

PASS.

Scan result:

- no invented DOI;
- no local absolute path in repository docs;
- no excluded workspace reference;
- no rejected-route history text in the Mission 036G files;
- no venue publication promise;
- no requirement for positive review;
- no positive legal, chain-of-custody, or production-deployment claim.

Restricted claim-boundary terms appear only in explicit non-claim contexts.

## 7A. Checks

- `git diff --check`: PASS.
- `python -m pytest tests/test_media_mobile_video_fixture.py -q`: `6 passed`.

## 8. Commit Hash

- Discoverability commit: `a794d57 Link agent-readable AEP-Media entry points`
- Push status: pushed to `origin/opentelemetry-to-eeoap-adapter`

## 9. Readiness

- JOSS technical readiness: READY.
- JOSS submission readiness: WAITING FOR PUBLIC HISTORY.
- Earliest honest JOSS submission date: 2026-09-16 or later.

## 10. Next Action

Open one recruitment or Task A issue only after a real reviewer is ready or
after explicit authorization is set. Do not create public activity merely to
manufacture history.
