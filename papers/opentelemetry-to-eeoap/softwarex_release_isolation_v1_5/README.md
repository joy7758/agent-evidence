# SoftwareX Release Isolation v1.5

This directory records the isolated release-candidate worktree created for the
OpenTelemetry-to-EEOAP SoftwareX route.

Purpose:

- Isolate SoftwareX release preparation away from the current dirty repository
  worktree.
- Verify that the OpenTelemetry-to-EEOAP package can be inspected and tested
  from a clean branch rooted at the v1.4 route-analysis commit.
- Prepare the next gate before any public tag push, DOI, GitHub Release,
  venue formatting, or formal submission.

Source commit:

`eda35b047041baee2eb6b578ba1cdd603fd06939`

Release-candidate branch:

`softwarex-otel-eeoap-release-candidate`

Clean worktree path:

`/tmp/agent-evidence-softwarex-otel-eeoap-rc`

This is analysis/isolation only. No runtime code, tests, fixtures, generated
JSON outputs, EEOAP schema, DOI, GitHub Release, tag push, venue formatting, or
submission was performed.
