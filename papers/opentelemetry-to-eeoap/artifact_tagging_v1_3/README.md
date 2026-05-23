# OpenTelemetry-to-EEOAP Artifact Tagging v1.3

This directory records the local immutable artifact-tagging step requested after
the v1.2 strict red-team review of the OpenTelemetry-to-EEOAP paper package.

The v1.2 review route decision was:

- Primary route: SoftwareX-style software paper.
- Fallback route: workshop or artifact track.
- Immediate blocker to reduce: stabilize the EEOAP and AEP artifact references.

This step created local annotated Git tags only. It did not create a DOI, did
not create a GitHub Release, did not push tags to any remote, did not venue
format the manuscript, and did not submit anything externally.

No runtime code, tests, fixtures, generated JSON outputs, adapter features, or
EEOAP schema files were changed by this step. Existing out-of-scope worktree
changes under SoftwareX/AEP-Media, `pd-oap`, `tmp`, and other unrelated paths
were not modified or staged.

Files in this packet:

- `TAGGING_DECISION.md`: target analysis and final tag decisions.
- `TAG_RECORDS.md`: tag object hashes, target commits, messages, and push
  status.
- `SUBMISSION_BLOCKER_UPDATE.md`: blocker status after local immutable tags.
- `NEXT_ROUTE_RECOMMENDATION.md`: next route action based on tag status.
- `COMMAND_LOG.md`: commands, validation, worktree boundaries, and plugin
  selection report.
