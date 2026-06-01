# AEP-Media Agent Index

Date: 2026-06-01

## Project Purpose

AEP-Media is a local validation component inside `agent-evidence`. It helps
reviewers and researchers check whether a media evidence bundle is internally
complete, hash-consistent, path-safe, time-bounded, and diagnosable.

The main review fixture is a mobile-video-style package with synthetic media,
network timing, ffprobe-style metadata, and provenance sidecar files.

## Main Commands

```bash
python -m pip install -e .
agent-evidence --help
agent-evidence validate-media-profile examples/media/use_cases/mobile_video_network_timing/mobile-video-operation-evidence.json
agent-evidence build-media-bundle examples/media/use_cases/mobile_video_network_timing/mobile-video-operation-evidence.json --out /tmp/aep-media-mobile-video-bundle
agent-evidence verify-media-bundle /tmp/aep-media-mobile-video-bundle
agent-evidence verify-media-bundle /tmp/aep-media-mobile-video-bundle --strict-time
agent-evidence run-media-evaluation --out /tmp/aep-media-evaluation
```

## Important Paths

- `README.md`: repository overview and installation.
- `llms.txt`: agent-readable project entry point.
- `docs/aep-media/README.md`: AEP-Media documentation index.
- `docs/aep-media/mobile-video-walkthrough.md`: mobile-video fixture
  walkthrough.
- `docs/aep-media/adapter-boundaries.md`: adapter ingestion boundaries.
- `paper/paper.md`: JOSS-style paper draft.
- `docs/paper/joss/maintenance/recruitment/`: external reviewer recruitment
  templates.
- `docs/paper/joss/maintenance/paid-review/`: paid external review protocol.

## Fixture Paths

- Valid statement:
  `examples/media/use_cases/mobile_video_network_timing/mobile-video-operation-evidence.json`
- Fixture README:
  `examples/media/use_cases/mobile_video_network_timing/README.md`
- Synthetic media placeholder:
  `examples/media/use_cases/mobile_video_network_timing/artifacts/mobile_video_placeholder.bin`
- Network timing fixture:
  `examples/media/use_cases/mobile_video_network_timing/artifacts/network_timing_log.json`
- FFprobe-style fixture:
  `examples/media/use_cases/mobile_video_network_timing/artifacts/ffprobe_metadata.json`
- Provenance sidecar:
  `examples/media/use_cases/mobile_video_network_timing/artifacts/provenance_sidecar.json`

## Test Paths

- `tests/test_media_mobile_video_fixture.py`
- `tests/test_media_cli_registration.py`
- `tests/test_media_evaluation.py`

Recommended targeted test:

```bash
python -m pytest tests/test_media_cli_registration.py tests/test_media_evaluation.py -q
```

## Expected Issue Codes

The mobile-video fixture regression tests use these expected issue codes:

- `media_hash_mismatch`
- `missing_clock_trace_ref`
- `unresolved_actor_ref`

These codes describe local validation failures. They are not external
authenticity, legal, or chain-of-custody findings.

## Non-Claims

AEP-Media does not claim:

- legal admissibility;
- chain of custody;
- non-repudiation;
- trusted timestamping;
- real PTP proof;
- full MP4 PRFT parsing;
- real C2PA signature verification;
- production deployment;
- proof that the underlying event is truthful.

## Reviewer Task

External reviewers should reproduce the mobile-video-style fixture from a fresh
clone and report:

- operating system;
- Python version;
- shell;
- install command;
- exact commands run;
- output summary;
- first failure, if any;
- confusing terminology;
- missing expected output;
- suggested fix.

Useful task files:

- `docs/paper/joss/maintenance/recruitment/github_recruitment_issue_body.md`
- `docs/paper/joss/maintenance/issues/task_A_github_issue_body.md`
- `docs/paper/joss/maintenance/paid-review/task_A_reproducibility_review.md`
