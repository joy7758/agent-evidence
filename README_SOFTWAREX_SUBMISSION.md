# SoftwareX Submission Artifact

This repository contains the software artifact for the manuscript:

**A Software Artifact for Deterministic Conversion of OpenTelemetry Traces into
Structured Execution Evidence**

## Artifact Scope

The artifact implements a deterministic transformation from OpenTelemetry OTLP
JSON traces into structured EEOAP evidence records.

It is limited to:

- local trace transformation;
- schema-bound validation;
- provenance-preserving evidence generation;
- reproducible package-level evaluation.

It does not claim:

- a new telemetry standard;
- a replacement for OpenTelemetry;
- production deployment proof;
- external certification;
- legal non-repudiation.

## Reproduction

From a clean unpacked archive, prepare the local test environment with:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -e ".[test]"
```

Run:

```bash
scripts/reproduce_paper.sh
```

Expected result:

```text
DONE: Reproducibility pipeline complete
```

## Main Files

- `paper/softwarex_v2_revised.pdf`
- `paper/cover_letter.md`
- `paper/highlights.txt`
- `paper/data_availability_statement.md`
- `paper/ai_use_declaration.md`
- `LICENSE`
- `pyproject.toml`
- `agent_evidence/`
- `examples/minimal-valid-evidence.json`
- `tests/test_cli.py`
- `tests/test_aep_profile.py`
- `release/softwarex_v2_EDITORIAL_LOCKED_FINAL_manifest.json`

## Validation

Run:

```bash
python3 scripts/validate_softwarex_package.py \
  --input /path/to/softwarex_v2_EDITORIAL_LOCKED_FINAL.zip
```

Expected result:

```text
ok: true
```

## Data Availability

The final public repository or archival URL must be inserted into:

```text
paper/data_availability_statement.md
```

before external submission.
