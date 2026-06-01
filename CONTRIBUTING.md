# Contributing to agent-evidence

Thank you for considering a contribution. This repository focuses on structured
evidence objects for AI agent and service operations, including the AEP-Media
research-software path for local validation of media evidence bundles.

## Project Scope

Contributions should preserve the current evidence-validation boundary:

- local profile validation;
- offline bundle building and verification;
- command-line workflows;
- examples, tests, schemas, specs, and reproducibility documentation;
- fixture-based adapter ingestion for media/time/provenance metadata.

Do not add claims or implementation shortcuts that turn this project into a
legal proof system, production forensic platform, trusted timestamping service,
full C2PA verifier, full MP4 PRFT parser, or chain-of-custody system without
explicit evidence and review.

## Development Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
```

If you only need the package without development tooling:

```bash
python -m pip install -e .
```

## Running Tests

Run the full test suite:

```bash
python -m pytest -q
```

Run targeted AEP-Media checks:

```bash
python -m pytest \
  tests/test_media_profile.py \
  tests/test_media_bundle.py \
  tests/test_media_time.py \
  tests/test_media_adapters.py \
  tests/test_media_evaluation.py \
  tests/test_media_cli_registration.py \
  -q
```

Run core AEP-Media CLI examples:

```bash
agent-evidence validate-media-profile examples/media/minimal-valid-media-evidence.json
agent-evidence validate-media-time-profile examples/media/time/minimal-valid-time-aware-media-evidence.json
agent-evidence run-media-evaluation --out /tmp/aep-media-evaluation
```

Run style checks:

```bash
ruff check agent_evidence tests
```

## Reporting Issues

Please use GitHub issues for bug reports, documentation problems, and feature
requests. Include:

- the command you ran;
- expected behavior;
- actual behavior;
- Python version;
- package version or commit;
- a minimal redacted fixture if possible.

Do not upload private media, personal evidence records, credentials, tokens, or
sensitive logs. Use synthetic or redacted fixtures.

## Pull Requests

Pull requests should:

- describe the user-facing and agent-facing change;
- include tests or explain why tests are not applicable;
- update docs/examples when behavior changes;
- avoid committing large binary artifacts;
- avoid private evidence or non-redacted media;
- preserve the claim boundary below.

If you used substantial AI assistance for code, tests, documentation, or paper
wording, disclose that in the pull request notes and describe what was reviewed
or validated by a human contributor.

## Claim Boundary

Contributors must not add unsupported claims of:

- legal admissibility;
- non-repudiation;
- chain of custody;
- trusted timestamping;
- real PTP proof;
- full MP4 PRFT parsing;
- real C2PA signature verification;
- production deployment;
- broad forensic sufficiency.

Those terms may appear only as explicit limitations or non-claims unless a
future contribution adds and documents the required evidence.
