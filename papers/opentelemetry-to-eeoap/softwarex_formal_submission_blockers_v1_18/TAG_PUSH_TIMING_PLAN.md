# Tag Push Timing Plan

## Current Local Tags

- `eeoap-v0.1-artifact`
  - Status: local only, not pushed
- `aep-v0.1-artifact`
  - Status: local only, not pushed

These tags support related artifact history. They are not public release
references for the OpenTelemetry-to-EEOAP SoftwareX submission yet.

## Why Tags Should Not Be Pushed Yet

Tags should not be pushed before release metadata is decided because:

- the final OpenTelemetry-to-EEOAP release scope is not fixed;
- DOI/GitHub Release strategy is unresolved;
- root metadata still describes AEP-Media;
- final references need public release identifiers;
- pushing an incorrect tag creates a public immutability and correction burden.

## Proposed Future Tags

Candidate names for discussion only:

- `opentelemetry-to-eeoap-softwarex-rc-v1.0`
- `otel-eeoap-adapter-softwarex-rc-v1.0`
- `softwarex-otel-eeoap-v1.0-rc1`

No tag is created in this task.

## Required Checks Before Any Tag Push

1. Confirm release metadata strategy.
2. Confirm final author/support metadata.
3. Finalize support package contents.
4. Regenerate and verify SHA-256 checksums.
5. Run scoped pytest.
6. Run validator on repository generated statements.
7. Run validator on support package copied statements.
8. Validate CodeMeta JSON.
9. Validate CFF YAML.
10. Run clean-clone verification from the tag candidate.
11. Confirm git status is clean.
12. Confirm manuscript references and artifact availability wording match the
    tag/release identifiers.

## Rollback Risk

Pushed tags are public immutability signals. Moving or deleting them later can
damage the evidence trail. A tag push should happen only after the exact release
candidate commit and metadata scope are stable.

## Final Recommendation

Do not push any tag now. Decide release metadata and final support package first,
then create and push one focused OpenTelemetry-to-EEOAP release candidate tag
only after validation passes.
