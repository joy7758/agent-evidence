# Tag Push Checklist

Purpose: define checks required before pushing any tag.

- [ ] Final public release scope is confirmed.
- [ ] Root metadata strategy is confirmed.
- [ ] Package-local metadata is confirmed.
- [ ] Support package is current.
- [ ] Local RC tag exists and points to the selected commit.
- [ ] Final clean-clone verification after tag creation passes.
- [ ] Final checksum verification after tag creation passes.
- [ ] Final references are updated if a public URL exists.
- [ ] GitHub remote is checked.
- [ ] Author approves tag push.
- [ ] No private personal data is present.
- [ ] Decision is made on whether the tag should be pushed before or after
  GitHub Release creation.
- [ ] Push is explicitly approved.

No tag should be pushed until these checks are complete and approval is
explicit.
