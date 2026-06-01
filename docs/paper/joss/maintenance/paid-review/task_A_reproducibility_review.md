# Task A: Reproducibility Review

## Goal

Evaluate whether a new technical user can clone the repository and reproduce
the AEP-Media README and mobile-video walkthrough without private assistance.

## Reviewer Profile

The reviewer should be comfortable with Python command-line tools, Git, and
pytest. Domain expertise is helpful but not required.

## Required Scope

From a fresh clone, run:

```bash
python -m venv .venv
.venv/bin/python -m pip install -e ".[dev]"
.venv/bin/agent-evidence --help
.venv/bin/agent-evidence validate-media-profile examples/media/use_cases/mobile_video_network_timing/mobile-video-operation-evidence.json
.venv/bin/agent-evidence build-media-bundle examples/media/use_cases/mobile_video_network_timing/mobile-video-operation-evidence.json --out /tmp/aep-media-task-a-bundle
.venv/bin/agent-evidence verify-media-bundle /tmp/aep-media-task-a-bundle
.venv/bin/agent-evidence verify-media-bundle /tmp/aep-media-task-a-bundle --strict-time
.venv/bin/python -m pytest tests/test_media_mobile_video_fixture.py -q
```

If the reviewer uses a different Python executable or shell, they should record
the exact replacement commands.

## Deliverable

Open one GitHub issue with:

- operating system and version;
- Python version;
- install command used;
- commands run;
- command outputs or failure summaries;
- unclear documentation points;
- mismatches between README, walkthrough, and observed behavior;
- suggested fixes.

Screenshots are optional and must not contain private data.

## Acceptance Criteria

The issue is accepted if it is:

- specific and actionable;
- reproducible by maintainers;
- tied to exact commands or file paths;
- critical where criticism is warranted;
- not a generic praise-only comment.

## Boundaries

The reviewer must not upload private media, real evidence files, or large
artifacts. The review must not expand AEP-Media claims beyond local validation
and fixture-based adapter ingestion.
