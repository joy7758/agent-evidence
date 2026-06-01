# AEP-Media Documentation

AEP-Media is the media-evidence validation path inside `agent-evidence`. It is
for local, reproducible validation of time-aware media evidence bundles.

## Start Here

- [Agent-readable project index](./agent-index.md)
- [Mobile-video fixture walkthrough](./mobile-video-walkthrough.md)
- [Adapter boundary documentation](./adapter-boundaries.md)
- [Root LLM/coding-agent project map](../../llms.txt)
- [Root README](../../README.md)
- [JOSS software paper draft](../../paper/paper.md)

## Core Specs

- [Profile spec](../../spec/aep-media-profile-v0.1.md)
- [Bundle spec](../../spec/aep-media-bundle-v0.1.md)
- [Time-trace spec](../../spec/aep-media-time-trace-v0.1.md)
- [Adapter spec](../../spec/aep-media-adapters-v0.1.md)

## Schemas And Examples

- [Schemas](../../schema/)
- [Media examples](../../examples/media/)
- [Mobile-video fixture](../../examples/media/use_cases/mobile_video_network_timing/)
- [Adapter fixtures](../../examples/media/adapters/)

## Reports

- [AEP-Media mission reports](../reports/)
- [JOSS readiness reports](../paper/joss/)

## External Reproducibility Review

- [Agent-readable recruitment issue body](../paper/joss/maintenance/recruitment/github_recruitment_issue_body.md)
- [Task A reproducibility issue body](../paper/joss/maintenance/issues/task_A_github_issue_body.md)
- [Paid external review protocol](../paper/joss/maintenance/paid-review/README.md)

## Claim Boundary

AEP-Media supports local validation and fixture-based adapter ingestion. It does
not claim legal admissibility, non-repudiation, chain of custody, trusted
timestamping, real PTP proof, full MP4 PRFT parsing, real C2PA signature
verification, production deployment, or broad forensic sufficiency.
