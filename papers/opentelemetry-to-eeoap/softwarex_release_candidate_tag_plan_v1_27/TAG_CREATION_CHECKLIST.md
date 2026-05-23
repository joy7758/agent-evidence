# Tag Creation Checklist

Purpose: define checks required before creating a local annotated RC tag.

- [ ] `git status --short` is clean.
- [ ] Current branch is `softwarex-otel-eeoap-release-candidate`.
- [ ] Target commit is selected and recorded.
- [ ] Proposed tag does not already exist locally.
- [ ] Version 1.25 support package exists.
- [ ] Version 1.26 clean-clone verification passed.
- [ ] SHA-256 checksum passed for 34 listed support-package files.
- [ ] CodeMeta JSON validation passed.
- [ ] CFF YAML validation status is documented.
- [ ] Scoped pytest passed.
- [ ] Validator checks passed for repository generated statements.
- [ ] Validator checks passed for support package copied statements.
- [ ] Privacy check passed.
- [ ] Root metadata strategy is documented.
- [ ] Remaining release fields still TODO are documented.
- [ ] No DOI or GitHub Release claim is made.
- [ ] No tag push is planned during local tag creation.

The checklist is ready for local tag creation planning. It does not authorize a
tag push.
