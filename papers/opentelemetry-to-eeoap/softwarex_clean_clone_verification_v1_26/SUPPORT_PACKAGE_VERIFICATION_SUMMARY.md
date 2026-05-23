# Support Package Verification Summary

| Verification item | Expected result | Observed result | Pass/fail | Notes |
|---|---|---|---|---|
| Checked-out commit | `a03f6455d87bcf67987c7ba1e4297a224de70976` | `a03f6455d87bcf67987c7ba1e4297a224de70976` | pass | Detached HEAD checkout. |
| Clean git status before verification | Empty `git status --short` | Empty output | pass | No untracked files before verification. |
| Support package directory exists | Directory present | Present | pass | `softwarex_release_candidate_package_v1_25/`. |
| Key files exist | All requested key files present | All present | pass | 35 package files observed. |
| Checksum verification | 34 listed files OK | 34 listed files OK | pass | `sha256sum -c CHECKSUMS.sha256`. |
| CodeMeta JSON validation | JSON parses | Passed | pass | Output written to `/tmp`. |
| CFF YAML validation | Pass or documented skip | Skipped: `No module named 'yaml'` | partial | No PyYAML installed; dependency not installed by design. |
| Scoped pytest | Tests pass | `8 passed in 1.94s` | pass | Clean verification checkout. |
| Repository generated statement validator: valid-agent-trace | `ok=true`, `issue_count=0` | `ok=true`, `issue_count=0` | pass | Existing Pydantic warning only. |
| Repository generated statement validator: valid-agent-workflow-trace | `ok=true`, `issue_count=0` | `ok=true`, `issue_count=0` | pass | Existing Pydantic warning only. |
| Support package copied statement validator: valid-agent-trace | `ok=true`, `issue_count=0` | `ok=true`, `issue_count=0` | pass | Existing Pydantic warning only. |
| Support package copied statement validator: valid-agent-workflow-trace | `ok=true`, `issue_count=0` | `ok=true`, `issue_count=0` | pass | Existing Pydantic warning only. |
| Privacy check | No private phone number or home address | Generic matches were synthetic trace IDs, timestamps, and SHA-256 hashes only | pass | No private personal data found. |
| Clean git status after verification | Empty `git status --short` | Empty output | pass | Temporary outputs written under `/tmp`. |
