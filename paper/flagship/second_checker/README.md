# Second Checker Surface

This directory contains one repo-local second checker surface for the B1 line.

It is not an external third-party checker.

Its purpose is narrow: add one additional checker path for minimal profile inspection and
basic closure review without changing the canonical validator implementation.

It does not change B1 minimal-frozen `1 valid / 3 invalid / 1 demo`.

Current files:

- Checker script: `check_profile_minimal.py`
- Canonical valid report: `reports/minimal-valid.report.json`
- Canonical invalid report: `reports/invalid-unclosed-reference.report.json`
- Supplementary external-context valid report: `reports/external-context-valid.report.json`

Inputs used:

- `examples/minimal-valid-evidence.json`
- `examples/invalid-unclosed-reference.json`
- `paper/flagship/external_context/data_space_metadata_update.valid.json`

Run commands:

```bash
python3 paper/flagship/second_checker/check_profile_minimal.py \
  examples/minimal-valid-evidence.json \
  > paper/flagship/second_checker/reports/minimal-valid.report.json

python3 paper/flagship/second_checker/check_profile_minimal.py \
  examples/invalid-unclosed-reference.json \
  > paper/flagship/second_checker/reports/invalid-unclosed-reference.report.json

python3 paper/flagship/second_checker/check_profile_minimal.py \
  paper/flagship/external_context/data_space_metadata_update.valid.json \
  > paper/flagship/second_checker/reports/external-context-valid.report.json
```

This surface is supplementary checker evidence only. It is intended to strengthen checker
diversity for B1 while remaining repo-local and reviewable.
