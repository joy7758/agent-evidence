# Validation Before Submission Plan

## Required Validation Checks

1. Scoped pytest:

   ```bash
   /Users/zhangbin/GitHub/agent-evidence/.venv/bin/python -m pytest tests/test_opentelemetry_to_eeoap_adapter.py -q
   ```

2. Validator checks for repository generated statements:

   ```bash
   /Users/zhangbin/GitHub/agent-evidence/.venv/bin/agent-evidence validate-profile generated/valid-agent-trace-eeoap-statement.json
   /Users/zhangbin/GitHub/agent-evidence/.venv/bin/agent-evidence validate-profile generated/valid-agent-workflow-trace-eeoap-statement.json
   ```

3. Validator checks for support package copied statements:

   ```bash
   /Users/zhangbin/GitHub/agent-evidence/.venv/bin/agent-evidence validate-profile papers/opentelemetry-to-eeoap/softwarex_release_candidate_package_v1_15/EVIDENCE/generated/valid-agent-trace-eeoap-statement.json
   /Users/zhangbin/GitHub/agent-evidence/.venv/bin/agent-evidence validate-profile papers/opentelemetry-to-eeoap/softwarex_release_candidate_package_v1_15/EVIDENCE/generated/valid-agent-workflow-trace-eeoap-statement.json
   ```

4. CodeMeta JSON validation:

   ```bash
   python -m json.tool <final-codemeta-json>
   ```

5. CFF YAML validation:

   Run when PyYAML or an equivalent YAML parser is available. The v1.16 result
   was skipped because `yaml` was not installed.

6. Checksum regeneration:

   Regenerate SHA-256 checksums for the final support package after all release
   metadata changes.

7. Final support package checksum verification:

   ```bash
   sha256sum -c CHECKSUMS.sha256
   ```

8. Clean-clone verification:

   Run after the final release metadata/support package changes and before tag
   push, DOI creation, GitHub Release, or formal submission.

9. Git status check:

   ```bash
   git status --short
   ```

10. Generated artifact hygiene:

    Confirm no untracked generated artifacts appear after tests, validators,
    template build, or clean-clone checks.

## Validation Principle

Any release metadata change can invalidate previous checksum and clean-clone
evidence. Final validation must run after the final artifact set is assembled,
not before.
