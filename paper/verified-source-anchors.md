# EEOAP Verified Source Anchors

## 1. Purpose

This file records a text-only verified-source anchor layer for EEOAP
(Execution Evidence and Operation Accountability Profile,
执行证据与操作问责配置文件). It supports internal citation planning only. It
does not complete the venue bibliography, does not create final reference
style, and does not claim formal submission readiness.

The anchors below are limited to manually verified metadata provided for this
source-verification pass. Missing metadata remains intentionally absent.

## 2. Verified anchors

### 2.1 W3C PROV-DM

- Source name: PROV-DM: The PROV Data Model.
- Source type: W3C (World Wide Web Consortium, 万维网联盟) Recommendation.
- Verified metadata: organization W3C; title `PROV-DM: The PROV Data Model`;
  status W3C Recommendation; date 30 April 2013.
- EEOAP use: provenance model background for entities, activities, agents,
  and provenance as part of evidence object design.
- Boundary / non-claim: related work only; EEOAP does not implement full PROV
  conformance.
- Suggested citation role: background citation for provenance vocabulary and
  evidence-object design context.

### 2.2 W3C PROV-Constraints

- Source name: Constraints of the PROV Data Model.
- Source type: W3C (World Wide Web Consortium, 万维网联盟) Recommendation.
- Verified metadata: organization W3C; title `Constraints of the PROV Data
  Model`; status W3C Recommendation; date 30 April 2013.
- EEOAP use: validity constraints and consistency checking background.
- Boundary / non-claim: related work only; EEOAP uses a narrower
  operation-level validation boundary.
- Suggested citation role: background citation for validity constraints and
  consistency-checking language.

### 2.3 JSON Schema Draft 2020-12

- Source name: JSON Schema Draft 2020-12.
- Source type: JSON Schema project specification draft.
- Verified metadata: organization JSON Schema project; title `JSON Schema
  Draft 2020-12`; published 16 June 2022; authors listed by source Austin
  Wright, Henry Andrews, Ben Hutton, Greg Dennis.
- EEOAP use: schema and conformance validation background.
- Boundary / non-claim: EEOAP uses JSON (JavaScript Object Notation,
  JavaScript 对象表示法)-style evidence objects and validator-backed structure
  checks; this does not make JSON Schema the whole EEOAP contribution.
- Suggested citation role: background citation for JSON-style schema,
  conformance, and validator-backed structure checks.

### 2.4 ACM Artifact Review and Badging

- Source name: Artifact Review and Badging - Current.
- Source type: ACM (Association for Computing Machinery, 计算机协会) artifact
  review guidance.
- Verified metadata: organization ACM; title `Artifact Review and Badging -
  Current`; version 1.1; date 24 August 2020.
- EEOAP use: artifact reproducibility and reviewability framing.
- Boundary / non-claim: EEOAP does not claim ACM artifact badge or formal
  artifact acceptance.
- Suggested citation role: background citation for artifact reviewability and
  reproducibility framing.

### 2.5 DONA DOIP Version 2.0

- Source name: Digital Object Interface Protocol Specification.
- Source type: DONA Foundation protocol specification.
- Verified metadata: organization DONA Foundation; title `Digital Object
  Interface Protocol Specification`; version 2.0; date 12 November 2018.
- EEOAP use: digital object and object-interface background adjacent to FDO
  (FAIR Digital Object, 公平数字对象) and data-space mapping.
- Boundary / non-claim: EEOAP does not implement DOIP (Digital Object
  Interface Protocol, 数字对象接口协议) and does not claim official DOIP
  conformance.
- Suggested citation role: background citation for digital object interface
  concepts adjacent to EEOAP mapping discussion.

### 2.6 Kahn and Wilensky digital object services paper

- Source name: A framework for distributed digital object services.
- Source type: journal article.
- Verified metadata: authors Robert Kahn and Robert Wilensky; title `A
  framework for distributed digital object services`; venue International
  Journal on Digital Libraries; volume/pages/year 6, 115-123, 2006; DOI
  10.1007/s00799-005-0128-x.
- EEOAP use: digital object architecture background.
- Boundary / non-claim: EEOAP is not a general digital object architecture.
- Suggested citation role: background citation for digital object architecture
  lineage.

### 2.7 SLSA Version 1.2

- Source name: SLSA specification.
- Source type: SLSA (Supply-chain Levels for Software Artifacts,
  软件制品供应链等级) approved specification.
- Verified metadata: organization SLSA; title `SLSA specification`; version
  1.2; status Approved.
- EEOAP use: supply-chain integrity and provenance background.
- Boundary / non-claim: EEOAP does not claim SLSA conformance.
- Suggested citation role: background citation for supply-chain integrity and
  provenance framing.

### 2.8 SLSA Build Provenance

- Source name: Build: Provenance.
- Source type: SLSA (Supply-chain Levels for Software Artifacts,
  软件制品供应链等级) approved provenance specification page.
- Verified metadata: organization SLSA; title `Build: Provenance`; status
  Approved; predicate type `https://slsa.dev/provenance/v1`.
- EEOAP use: verifiable provenance and downstream verification background.
- Boundary / non-claim: EEOAP does not define a build provenance predicate.
- Suggested citation role: background citation for build provenance and
  downstream verification concepts.

### 2.9 in-toto Stable v1.0

- Source name: in-toto Stable.
- Source type: in-toto specification.
- Verified metadata: organization/project in-toto; title `in-toto Stable`;
  version v1.0; status from source thoroughly reviewed specification.
- EEOAP use: attestation and verifiable supply-chain metadata background.
- Boundary / non-claim: EEOAP does not implement in-toto layout or in-toto
  verification.
- Suggested citation role: background citation for attestation and verifiable
  supply-chain metadata.

### 2.10 OpenTelemetry Semantic Conventions

- Source name: OpenTelemetry Semantic Conventions.
- Source type: OpenTelemetry (开放遥测) semantic conventions.
- Verified metadata: project OpenTelemetry; title `OpenTelemetry Semantic
  Conventions`.
- EEOAP use: logs, traces, telemetry terminology, and semantic attribute
  background.
- Boundary / non-claim: EEOAP does not replace telemetry; it packages selected
  operation evidence.
- Suggested citation role: background citation for observability and telemetry
  terminology.

### 2.11 OpenTelemetry Semantic conventions for generative AI systems

- Source name: Semantic conventions for generative AI systems.
- Source type: OpenTelemetry (开放遥测) semantic conventions for Generative AI
  (生成式人工智能).
- Verified metadata: project OpenTelemetry; title `Semantic conventions for
  generative AI systems`; status Development.
- EEOAP use: examples of current agent/model spans, metrics, events, and
  telemetry conventions for Generative AI.
- Boundary / non-claim: because status is Development, use cautiously as
  current background only; do not treat as stable standard proof.
- Suggested citation role: cautious current-background citation for
  generative-AI telemetry vocabulary and examples.

## 3. Claim mapping

- Provenance model background: W3C PROV-DM supports discussion of entities,
  activities, agents, and provenance as one part of EEOAP evidence objects.
- Validity and consistency checking background: W3C PROV-Constraints supports
  discussion of constraints, while EEOAP remains narrower and
  operation-level.
- Schema and conformance validation background: JSON Schema Draft 2020-12
  supports validator-backed structure and profile language.
- Artifact review and reproducibility framing: ACM Artifact Review and
  Badging supports the artifact-reviewability framing without implying badge
  status.
- Digital object and object-interface background: DONA DOIP Version 2.0 and
  Kahn and Wilensky support FDO-adjacent and digital-object discussion without
  turning EEOAP into a DOIP implementation or general digital object
  architecture.
- Supply-chain provenance and attestation background: SLSA Version 1.2, SLSA
  Build Provenance, and in-toto Stable v1.0 support integrity, provenance, and
  attestation background without implying conformance.
- Observability and telemetry background: OpenTelemetry Semantic Conventions
  and the OpenTelemetry generative-AI conventions support logs, traces, spans,
  metrics, events, and semantic attribute terminology without replacing the
  EEOAP evidence object.

## 4. Boundaries and non-claims

- This anchor layer does not claim a complete bibliography.
- This anchor layer does not claim formal submission readiness.
- EEOAP does not claim full PROV conformance.
- EEOAP does not claim JSON Schema as the whole contribution.
- EEOAP does not claim ACM artifact badge or formal artifact acceptance.
- EEOAP does not implement DOIP or claim official DOIP conformance.
- EEOAP is not a general digital object architecture.
- EEOAP does not claim SLSA conformance.
- EEOAP does not define a SLSA build provenance predicate.
- EEOAP does not implement in-toto layout or in-toto verification.
- EEOAP does not replace telemetry.
- OpenTelemetry generative-AI conventions are Development status and must not
  be treated as stable standard proof.
- This pass does not claim public GitHub Release, Zenodo DOI (Digital Object
  Identifier, 数字对象标识符), production readiness, official FDO standard status,
  or ZKP (Zero-Knowledge Proof, 零知识证明) implementation.

## 5. Sources still needing verification

No additional source outside the verified anchors above is added in this file.
Any future venue-specific bibliography entry, public artifact citation,
release citation, DOI citation, or additional related-work source must be
verified separately before use.

The current unresolved work is citation integration rather than source
expansion: final venue style, final manuscript citation placement, artifact
availability wording, and any later public release or DOI language remain
outside this text-only anchor layer.

## 6. Not a final bibliography

This file is an internal verified-source anchor layer. It is not a final
bibliography, not a BibTeX file, not a venue-formatted reference list, and not
evidence that the paper is ready for formal submission.
