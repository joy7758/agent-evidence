# External Action Sequence

1. Run local gate checks.
2. Inspect `external_submission_v1/publish_gate/RELEASE_DECISION_RECORD.md`.
3. Replace real public URLs only after public artifacts exist.
4. Approve or reject release in the decision record.
5. Only after approval, manually perform selected GitHub release, discussion, outreach, or arXiv actions.

Repository scripts do not perform external actions without explicit approval variables.
