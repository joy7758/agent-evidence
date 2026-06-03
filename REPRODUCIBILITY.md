# Reproducibility

## Setup

```bash
python3 -m venv .venv
.venv/bin/python -m pip install --upgrade pip
.venv/bin/python -m pip install -e .
.venv/bin/python -m pip install pytest ruff jsonschema
```

## Case Execution

```bash
.venv/bin/python scripts/run_all_se_cases.py --bootstrap-fixtures
.venv/bin/python scripts/run_case_issue_pr_metadata.py --all
.venv/bin/python scripts/run_case_doc_data_transform.py --all
.venv/bin/python scripts/run_case_test_result_summary.py --all
```

## Verification

```bash
.venv/bin/python -m pytest tests/test_se_workflow_cases.py
.venv/bin/python -m ruff check .
```

## Expected Metrics

- total rows: 18
- valid rows: 3
- invalid rows: 15
- diagnostic match: 18/18
- schema-only missed invalid: 15
- log-only missed invalid: 15
- policy-only missed invalid: 13
- selected pytest suite: use the observed count from this rc3 candidate; do not cite earlier rc2/Phase 30 counts unless reproduced

## Interpretation

Baseline results are partial-capability comparisons. They show which controlled invalid cases are missed by schema-only, log-only, or policy-only checks; they do not establish general benchmark superiority.
