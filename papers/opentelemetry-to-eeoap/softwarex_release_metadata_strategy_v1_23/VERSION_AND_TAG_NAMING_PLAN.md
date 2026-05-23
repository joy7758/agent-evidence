# Version And Tag Naming Plan

## Existing Local Artifact Tags

- `eeoap-v0.1-artifact`
- `aep-v0.1-artifact`

Existing status: local only, not pushed.

These tags identify related EEOAP and AEP artifact targets. They are not final
public release tags for the OpenTelemetry-to-EEOAP SoftwareX package.

## Proposed OpenTelemetry-to-EEOAP Release Candidate Tag

Primary candidate:

- `opentelemetry-to-eeoap-softwarex-rc-v1.0`

## Alternative Names

- `otel-eeoap-softwarex-rc-v1.0`
- `opentelemetry-eeoap-adapter-v1.0-rc`

## Naming Criteria

- Clear OpenTelemetry-to-EEOAP scope.
- Not confused with EEOAP/AEP artifact tags.
- SoftwareX route visible.
- Release-candidate status clear.
- Compatible with later GitHub Release and archive naming.

## Recommendation

Use `opentelemetry-to-eeoap-softwarex-rc-v1.0` as the provisional release
candidate tag name. Keep the internal software version provisional until the
final release package is verified.

## Checks Required Before Tag Creation

1. Package-local CFF and CodeMeta drafts updated.
2. Final support issue URL decided.
3. Final release-candidate support package built.
4. SHA-256 checksums regenerated and verified.
5. Scoped pytest passes.
6. Validator passes for repository generated statements.
7. Validator passes for support package copied statements.
8. CodeMeta JSON parses.
9. CFF YAML validation passes or the skip reason is explicitly accepted.
10. Clean-clone verification passes at the candidate commit.
11. Manuscript references and artifact availability wording match the planned
    tag/release identifiers.

No tag is created or pushed in this task.
