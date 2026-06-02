# Case Protocol

## Run Commands

```bash
python scripts/run_case_issue_pr_metadata.py --all
python scripts/run_case_doc_data_transform.py --all
python scripts/run_case_test_result_summary.py --all
python scripts/run_all_se_cases.py
```

## Meaning Of Outputs

- `reports/se_case_matrix.json`: cross-case machine-readable result matrix.
- `reports/se_case_matrix.md`: human-readable case matrix.
- `reports/baseline_comparison.*`: baseline capability and limitation summary.
- `reports/failure_code_coverage.*`: diagnostic coverage by invalid variant.
- `cases/se_workflows/*/reports/*.profile-aware.json`: per-fixture reports.

## Baseline Meaning

Baselines are partial capability holders:

- schema-only checks structure;
- log-only checks event presence;
- policy-only checks local policy fields.

They are not strawmen and are not claimed to be complete alternatives.

## Allowed Claims

- The prototype provides representative reproducible SE workflow fixtures.
- Some invalid variants pass partial baselines but fail profile-aware or case-adapter checks.
- The result supports bounded operation-level reviewability for selected fixtures.

## Forbidden Claims

- industrial real-world evaluation;
- broad empirical generalization;
- deployment robustness;
- legal or compliance sufficiency;
- full FDO interoperability;
- general provenance model;
- TSE v3 readiness.
