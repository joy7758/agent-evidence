# References Draft - Verified Metadata, Not Final Upload Style

Status: verified reference draft for author review. This file is closer to a
Computer Standards & Interfaces reference list than the earlier candidate
inventory, but it is still not the final upload bibliography.

Verification date: 21 May 2026.

Rules preserved:

- Use only source anchors already selected for EEOAP (Execution Evidence and
  Operation Accountability Profile, 执行证据与操作问责配置文件).
- Do not invent DOI (Digital Object Identifier, 数字对象标识符) values, author
  names, versions, publication status, public release status, or endorsements.
- Include DOI values only where verified.
- Keep public GitHub Release and Zenodo DOI citations out unless those
  artifacts actually exist later.
- Re-check every entry against the live source before actual journal upload.

## Draft Numbered References

[1] W3C (World Wide Web Consortium). PROV-DM: The PROV Data Model. W3C
Recommendation, 30 April 2013. Editors: Luc Moreau and Paolo Missier.
Available at: https://www.w3.org/TR/prov-dm/. Accessed 21 May 2026.

[2] W3C (World Wide Web Consortium). Constraints of the PROV Data Model. W3C
Recommendation, 30 April 2013. Editors: James Cheney, Paolo Missier, and Luc
Moreau; author: Tom De Nies. Available at:
https://www.w3.org/TR/prov-constraints/. Accessed 21 May 2026.

[3] Austin Wright, Henry Andrews, Ben Hutton, and Greg Dennis. JSON Schema Draft
2020-12. JSON Schema project, published 16 June 2022. Available at:
https://json-schema.org/draft/2020-12. Accessed 21 May 2026.

[4] ACM (Association for Computing Machinery). Artifact Review and Badging -
Current. Artifact Review and Badging Version 1.1, 24 August 2020. Available
at: https://www.acm.org/publications/policies/artifact-review-and-badging-current.
Accessed 21 May 2026.

[5] DONA Foundation. Digital Object Interface Protocol Specification. Version
2.0, 12 November 2018. Available at:
https://www.dona.net/sites/default/files/2018-11/DOIPv2Spec_1.pdf. Accessed
21 May 2026.

[6] Robert Kahn and Robert Wilensky. A framework for distributed digital object
services. International Journal on Digital Libraries, 6, 115-123, 2006.
https://doi.org/10.1007/s00799-005-0128-x.

[7] SLSA (Supply-chain Levels for Software Artifacts). SLSA specification.
Version 1.2, status: Approved. Available at: https://slsa.dev/spec/v1.2/.
Accessed 21 May 2026.

[8] SLSA (Supply-chain Levels for Software Artifacts). Build: Provenance.
Status: Approved. Predicate type: https://slsa.dev/provenance/v1. Available
at: https://slsa.dev/spec/v1.2/build-provenance. Accessed 21 May 2026.

[9] in-toto. Specifications: in-toto Stable (v1.0). Status from source:
thoroughly reviewed specification. Available at: https://in-toto.io/docs/specs/.
Accessed 21 May 2026.

[10] OpenTelemetry. OpenTelemetry semantic conventions 1.41.0. Available at:
https://opentelemetry.io/docs/specs/semconv/. Accessed 21 May 2026.

[11] OpenTelemetry. Semantic conventions for generative AI systems. OpenTelemetry
semantic conventions 1.41.0, status: Development. Available at:
https://opentelemetry.io/docs/specs/semconv/gen-ai/. Accessed 21 May 2026.

## Verification Notes

- [1] and [2] are W3C Recommendations, used as provenance and validity
  background only. EEOAP does not claim PROV conformance.
- [3] is used for JSON (JavaScript Object Notation, JavaScript 对象表示法)
  schema and conformance-validation background. EEOAP does not claim that JSON
  Schema is the whole contribution.
- [4] is used for artifact reproducibility and reviewability framing. EEOAP
  does not claim an ACM artifact badge or formal artifact acceptance.
- [5] and [6] are used for digital object and object-interface background.
  EEOAP does not implement DOIP (Digital Object Interface Protocol,
  数字对象接口协议) and is not a general digital object architecture.
- [7], [8], and [9] are used for supply-chain provenance and attestation
  background. EEOAP does not claim SLSA conformance, does not define a SLSA
  build provenance predicate, and does not implement in-toto verification.
- [10] and [11] are used for observability and telemetry background. The
  generative-AI conventions remain Development status and should be cited
  cautiously.

## Do Not Use Until Verified

- Any public GitHub Release citation for `eeoap-v0.1-paper`.
- Any Zenodo DOI citation for the EEOAP artifact.
- Any official FDO (FAIR Digital Object, 公平数字对象) adoption, conformance,
  certification, or endorsement source for EEOAP.
- Any ZKP (Zero-Knowledge Proof, 零知识证明) source framed as implemented EEOAP
  functionality.
- Any legal compliance, regulatory certification, or court-grade audit source
  framed as an EEOAP guarantee.
- Any AEP (Agent Evidence Profile, 智能体证据配置文件), AEP-Media (Agent Evidence
  Profile Media, 智能体证据配置文件媒体扩展), AI Act (Artificial Intelligence Act,
  人工智能法案), or unrelated prior-paper source as evidence for this EEOAP scope.
- Any access date, URL, DOI, author list, venue, standard status, or
  publication status not directly checked against the source used for final
  upload.
