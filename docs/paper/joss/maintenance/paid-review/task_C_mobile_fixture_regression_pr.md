# Task C: Mobile Fixture Regression PR

## Goal

Add or improve a small regression test for the mobile-video-style AEP-Media
fixture without changing validator, schema, adapter, or evaluation semantics.

## Required Scope

The contributor should inspect:

- `examples/media/use_cases/mobile_video_network_timing/`
- `tests/test_media_mobile_video_fixture.py`
- existing media profile, bundle, and strict-time test patterns.

Potential improvements include:

- a new negative fixture using an existing failure mode;
- an assertion that a documented report field remains stable;
- a small documentation-linked regression test for a current CLI-visible path.

## Deliverable

Open one GitHub PR with:

- the test or fixture change;
- a short explanation of the covered behavior;
- the exact pytest command and result;
- no large binaries;
- no semantic validator/schema/adapter changes unless separately justified.

Recommended validation:

```bash
.venv/bin/python -m pytest tests/test_media_mobile_video_fixture.py -q
git diff --check
```

## Acceptance Criteria

The PR is accepted if:

- the test passes locally;
- CI passes when available;
- fixtures remain small and synthetic;
- the change is narrowly scoped;
- no unsupported claims are introduced;
- any behavior change is explicitly separated from this task.

## Boundaries

This task is for regression coverage, not feature expansion. Do not change
reported evaluation numbers, validation semantics, schemas, or adapter parsing
logic to make a test pass.
