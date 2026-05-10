# AEP-Media Final Pre-Release Validation

Date: 2026-05-10

## CLI Availability

`agent-evidence --help` lists the AEP-Media commands required for the SoftwareX reproducibility path, including:

- `validate-media-profile`
- `build-media-bundle`
- `verify-media-bundle`
- `validate-media-time-profile`
- `run-media-evaluation`
- `build-aep-media-release-pack`

## Tests

Targeted AEP-Media tests:

- Command: targeted media pytest set including `tests/test_media_cli_registration.py`
- Result: `48 passed, 1 warning`

SoftwareX/readiness tests:

- Command: submission/release/readiness pytest set
- Result: `23 passed, 1 warning`

Full test suite:

- Command: `./.venv/bin/python -m pytest -q`
- Result: `155 passed, 1 skipped, 15 warnings`

## Lint and Diff Checks

- `./.venv/bin/ruff check agent_evidence/cli/main.py tests/test_media_cli_registration.py`: `All checks passed!`
- `git diff --check`: passed

## Evaluation CLI

- Default evaluation: `PASS aep-media-evaluation@0.1 cases=18 unexpected=0`
- Adapter-inclusive evaluation: `PASS aep-media-evaluation@0.1 cases=26 unexpected=0 adapters=included`
- Optional-tool reporting evaluation: `PASS aep-media-evaluation@0.1 cases=23 unexpected=0 optional_tools=included`
- Combined adapter and optional-tool evaluation: `PASS aep-media-evaluation@0.1 cases=31 unexpected=0 adapters=included optional_tools=included`

## Release Pack CLI

- `PASS aep-media-release-pack@0.1`

## Result

Pre-release validation result: PASS.

Release publication remains gated because `AEP_MEDIA_PUBLISH_RELEASE` was not set to `1`.
