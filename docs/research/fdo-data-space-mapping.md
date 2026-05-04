# FDO / Data-Space Mapping

This document frames how `agent-evidence` can be discussed in relation to FDO
and data-space concepts without claiming official standard status.

## Why the mapping is relevant

`agent-evidence` produces artifacts that have object-like properties:

- an evidence bundle can be treated as a portable digital object
- a manifest can describe object metadata and integrity information
- a receipt can describe verification state
- a Review Pack can package verified artifacts for local review
- citation metadata can support attribution and reproducibility

These properties make FDO and data-space language useful for research
discussion.

## Possible mapping

| agent-evidence artifact | FDO / data-space interpretation |
| --- | --- |
| Evidence bundle | Portable digital object containing operation evidence. |
| Manifest | Object metadata, inventory, and integrity context. |
| Public key | Verification material associated with the exported object. |
| Receipt | Local verification state for a supplied bundle. |
| Review Pack | Reviewer-facing package assembled after verification. |
| Citation metadata | Attribution and release-level reference layer. |

This mapping is conceptual. It helps explain how evidence artifacts might move
through review workflows, not how to operate a complete data-space connector.

## Boundaries

The mapping does not claim:

- official FDO profile status
- official FDO standard status
- a complete data-space connector
- a policy enforcement system
- compliance certification
- AI Act approval
- legal non-repudiation
- a remote registry
- hosted review infrastructure

`agent-evidence` remains local-first. FDO and data-space mapping should be used
as a research bridge, not as a deployment claim.

## Role of Review Pack V0.3

Review Pack V0.3 provides a concrete local artifact that can be discussed in
data-space terms:

- it is produced from a verified signed export bundle
- it records artifact inventory
- it includes reviewer-facing summary material
- it preserves public verification material
- it states non-claims and limitations

It does not create remote registration, policy enforcement, access control, or
cross-organization exchange by itself.

## Future work

Future work can explore:

- profile formalization
- validator alignment
- metadata interoperability
- controlled sharing of review artifacts
- privacy-preserving evidence packaging
- data-space connector experiments after the local evidence boundary is stable

Those topics should remain separate from the current v0.6.0 implementation.
