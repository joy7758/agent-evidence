## Purpose

This issue is a public call for one or two external reproducibility reviewers
to test whether AEP-Media can be installed and run from a fresh clone using the
README and mobile-video walkthrough.

The goal is real feedback, not praise. Failed reproduction, unclear
documentation, confusing command output, or actionable criticism are useful
outcomes.

## Who This Is For

This task is suitable for:

- Python command-line users;
- open-source documentation or testing contributors;
- students or researchers interested in media evidence, provenance, or
  reproducibility workflows.

No private media, real incident data, or domain-specific confidential evidence
is needed.

## Task Summary

Please start from a fresh clone and run the AEP-Media mobile-video walkthrough.
Then report what worked, what failed, and what was unclear.

Primary reference task:

- `docs/paper/joss/maintenance/paid-review/task_A_reproducibility_review.md`

## Commands to Run

```bash
git clone https://github.com/joy7758/agent-evidence
cd agent-evidence
python -m pip install -e .
agent-evidence --help
agent-evidence validate-media-profile examples/media/use_cases/mobile_video_network_timing/mobile-video-operation-evidence.json
agent-evidence build-media-bundle examples/media/use_cases/mobile_video_network_timing/mobile-video-operation-evidence.json --out /tmp/aep-media-mobile-video-bundle
agent-evidence verify-media-bundle /tmp/aep-media-mobile-video-bundle
agent-evidence verify-media-bundle /tmp/aep-media-mobile-video-bundle --strict-time
python -m pytest tests/test_media_cli_registration.py tests/test_media_evaluation.py -q
```

If you need a virtual environment or a different Python command, please record
the exact commands you used.

## Deliverable

Please add one comment on this issue, or open a small PR, with:

- operating system and version;
- Python version;
- install command used;
- exact commands run;
- output summary;
- errors or failures;
- unclear documentation;
- actionable suggestions.

## Compensation and Disclosure

If this is performed as a paid external review, payment is for time spent
testing and reporting. Payment does not buy positive feedback, endorsement,
stars, citations, authorship, or a publication outcome.

Paid-review status should be disclosed in the issue comment or PR where
relevant.

## What Not To Do

- Do not upload private media.
- Do not upload large binaries.
- Do not use confidential evidence or private logs.
- Do not submit generic praise-only feedback.
- Do not broaden AEP-Media's claim boundary.

## Claim Boundary

AEP-Media supports local validation and fixture-based adapter ingestion. It does
not claim legal admissibility, chain of custody, real PTP proof, real C2PA
verification, or production deployment.
