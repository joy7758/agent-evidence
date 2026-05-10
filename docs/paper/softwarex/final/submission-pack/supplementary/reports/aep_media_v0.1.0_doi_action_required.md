# AEP-Media v0.1.0 DOI Action Required

Date: 2026-05-10

## Status

No AEP-Media-specific DOI was created during Mission 019.

Reason: `AEP_MEDIA_PUBLISH_RELEASE` was not set to `1`, so no tag was pushed and no GitHub release was created.

## Release Command Preview

Run only after human approval and a final working-tree scope check:

```bash
git tag -a aep-media-v0.1.0 -m "AEP-Media v0.1.0"
git push origin aep-media-v0.1.0
gh release create aep-media-v0.1.0 \
  --repo joy7758/agent-evidence \
  --title "AEP-Media v0.1.0: Offline Validation of Time-Aware Media Evidence Bundles" \
  --notes-file docs/paper/softwarex/final/release/notes/aep-media-v0.1.0-release-notes.md
```

## Zenodo Steps

1. Open Zenodo.
2. Ensure the GitHub account is linked.
3. Enable the `joy7758/agent-evidence` repository in the Zenodo GitHub integration.
4. Create or reprocess GitHub release `aep-media-v0.1.0`.
5. Wait for Zenodo to create the archive record.
6. Copy the generated DOI.
7. Update `CITATION.cff`, `.zenodo.json` if appropriate, README, SoftwareX manuscript, SoftwareX metadata, release notes, and the final submission pack.
8. Regenerate the SoftwareX final pack.

## Important

Do not invent a DOI. SoftwareX readiness remains NEAR READY until the AEP-Media-specific archive DOI is confirmed.
