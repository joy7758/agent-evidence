# AEP-Media FSIDI Backup Positioning

## Backup Target

Forensic Science International: Digital Investigation is a possible backup path if AEP-Media is reframed around digital evidence, multimedia, provenance, integrity, and authenticity boundaries.

## Current Fit

AEP-Media already includes several elements that are relevant to digital evidence and media provenance:

- media artifact hash recomputation;
- offline bundle integrity;
- provenance and manifest references;
- declared time context and strict time-trace validation;
- adapter-only ingestion of LinuxPTP-style, FFmpeg PRFT-style, and C2PA-like metadata;
- controlled tamper cases and diagnosable failure codes.

## Required Reframing

An FSIDI-oriented paper should focus less on software package mechanics and more on evidence methodology:

- what a locally checkable media evidence package is;
- how integrity, provenance references, and declared time traces interact;
- how local validation differs from authenticity proof;
- how adapter-only ingestion preserves claim boundaries;
- how tamper cases expose inconsistencies in a declared evidence package.

## Claim Boundary

The claim boundary must be even more explicit for a digital-evidence venue:

- no legal admissibility;
- no non-repudiation;
- no trusted timestamping;
- no real PTP proof;
- no full MP4 PRFT parser;
- no real C2PA signature verification;
- no chain of custody;
- no proof that the original media capture event was truthful, authorized, or unmodified before packaging.

## Current Suitability

FSIDI backup suitability: POSSIBLE.

Reason: the media evidence, bundle integrity, provenance boundary, and strict declared time-trace components are relevant. However, the current strongest package is still a software/artifact submission. An FSIDI version should be rewritten as a digital-evidence methodology paper rather than submitted as-is.
