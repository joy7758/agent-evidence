# Reference Verification Report

Status: author-review support file. This report records the source-checking
performed for the Computer Standards & Interfaces journal-preparation package.
It is not a publication record and not evidence of formal submission.

Verification date: 21 May 2026.

## Scope

This pass verified metadata for the 11 numbered references used by
`manuscript-draft.md`. It did not add new related-work sources, did not create
a public artifact citation, and did not create a Zenodo DOI (Digital Object
Identifier, 数字对象标识符) citation.

## Verified Entries

| Ref | Source | Verified metadata | Use in manuscript | Boundary |
| --- | --- | --- | --- | --- |
| [1] | W3C PROV-DM | W3C Recommendation; 30 April 2013; editors Luc Moreau and Paolo Missier. | Provenance model background. | No PROV conformance claim. |
| [2] | W3C PROV-Constraints | W3C Recommendation; 30 April 2013; editors James Cheney, Paolo Missier, Luc Moreau; author Tom De Nies. | Validity and consistency-checking background. | EEOAP uses a narrower operation-level validation boundary. |
| [3] | JSON Schema Draft 2020-12 | Published 16 June 2022; authors Austin Wright, Henry Andrews, Ben Hutton, Greg Dennis. | JSON-style schema and conformance-validation background. | JSON Schema is not the whole EEOAP contribution. |
| [4] | ACM Artifact Review and Badging | Version 1.1; 24 August 2020. | Artifact reproducibility and reviewability framing. | No ACM badge or artifact acceptance claim. |
| [5] | DONA DOIP Specification | Version 2.0; 12 November 2018; released by DONA Foundation. | Digital object and interface background. | No DOIP implementation or conformance claim. |
| [6] | Kahn and Wilensky | International Journal on Digital Libraries, 6, 115-123, 2006; DOI verified. | Digital object architecture background. | EEOAP is not a general digital object architecture. |
| [7] | SLSA specification | Version 1.2; status Approved. | Supply-chain integrity and provenance background. | No SLSA conformance claim. |
| [8] | SLSA Build Provenance | Status Approved; predicate type `https://slsa.dev/provenance/v1`. | Verifiable build provenance background. | EEOAP does not define a build provenance predicate. |
| [9] | in-toto Stable | Stable v1.0 described as thoroughly reviewed. | Attestation and supply-chain metadata background. | No in-toto layout or verification implementation. |
| [10] | OpenTelemetry semantic conventions | OpenTelemetry semantic conventions 1.41.0. | Logs, traces, spans, metrics, semantic attributes. | EEOAP does not replace telemetry. |
| [11] | OpenTelemetry generative AI conventions | OpenTelemetry semantic conventions 1.41.0; status Development. | Current GenAI telemetry background. | Development status; cite cautiously. |

## Source URLs Checked

- https://www.w3.org/TR/prov-dm/
- https://www.w3.org/TR/prov-constraints/
- https://json-schema.org/draft/2020-12
- https://www.acm.org/publications/policies/artifact-review-and-badging-current
- https://www.dona.net/sites/default/files/2018-11/DOIPv2Spec_1.pdf
- https://link.springer.com/article/10.1007/s00799-005-0128-x
- https://slsa.dev/spec/v1.2/
- https://slsa.dev/spec/v1.2/build-provenance
- https://in-toto.io/docs/specs/
- https://opentelemetry.io/docs/specs/semconv/
- https://opentelemetry.io/docs/specs/semconv/gen-ai/

## Remaining Author-side Checks

- Confirm Computer Standards & Interfaces accepts the chosen reference style at
  upload time.
- Verify each URL and access date again immediately before upload.
- Add artifact release or DOI references only if they actually exist later.
- Ensure every in-text numeric citation still maps to the same numbered entry.
- Keep `make paper-demo`, `references_digest_mismatch`, and `19 passed,
  1 warning` as internal artifact facts, not literature citations.
