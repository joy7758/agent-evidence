# Support Package Verification Summary

| Verification item | Expected result | Observed result | Pass/fail | Notes |
|---|---:|---:|---|---|
| Support package directory exists | Exists | Exists | Pass | `softwarex_release_candidate_package_v1_15/` present |
| Key files exist | All requested key paths present | All requested key paths present | Pass | README, manifest, checksums, article, metadata, evidence, validation summary |
| Checksum verification | All listed files OK | 31 listed files OK | Pass | `sha256sum -c CHECKSUMS.sha256` |
| CodeMeta JSON validation | JSON parses | JSON parses | Pass | `python -m json.tool` |
| CFF YAML validation | YAML parses if parser available | Skipped | Deferred | `No module named 'yaml'`; no dependency installed |
| Scoped pytest | Tests pass | `8 passed in 2.34s` | Pass | Clean verification checkout |
| Repository generated statement validator: valid-agent-trace | `ok=true`, `issue_count=0` | `ok=true`, `issue_count=0` | Pass | Existing validator |
| Repository generated statement validator: valid-agent-workflow-trace | `ok=true`, `issue_count=0` | `ok=true`, `issue_count=0` | Pass | Existing validator |
| Support package copied statement validator: valid-agent-trace | `ok=true`, `issue_count=0` | `ok=true`, `issue_count=0` | Pass | Existing validator |
| Support package copied statement validator: valid-agent-workflow-trace | `ok=true`, `issue_count=0` | `ok=true`, `issue_count=0` | Pass | Existing validator |
| Clean git status after verification | Clean | Clean | Pass | `git status --short` empty |

Overall result: pass, with CFF YAML validation deferred because the local YAML
parser dependency is unavailable.
