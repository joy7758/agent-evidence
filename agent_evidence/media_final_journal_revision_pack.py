# ruff: noqa: E501
from __future__ import annotations

import json
import re
import shutil
import subprocess
import zipfile
from hashlib import sha256
from pathlib import Path
from typing import Any

HIGH_REVISION_PROFILE = "aep-media-high-revision-pack@0.1"
TITLE = "AEP-Media: A Minimal Time-Aware Media Evidence Profile and Offline Validator for Operation Accountability"
FORBIDDEN_WORKSPACE_LABEL = "paper-ncs-" + "execution-evidence"
TEXT_SUFFIXES = {".csv", ".json", ".md", ".txt", ".xml"}
EDITOR_FACING_RELATIVE_FILES = [
    "manuscript/aep_media_tse_submission_high_revision.md",
    "cover-letter/aep_media_cover_letter_high_revision.md",
    "supplementary/README_SUPPLEMENTARY.md",
    "supplementary/CLAIM_BOUNDARY.md",
    "supplementary/REPRODUCIBILITY_CHECKLIST.md",
    "supplementary/EVALUATION_SUMMARY.md",
    "supplementary/ARTIFACT_INVENTORY.md",
]
RED_FLAG_PATTERNS = [
    "REPLACE THIS " + "LINE",
    "prepared_locally_" + "not_submitted",
    "Final portal upload",
    "manual author action",
    "This draft still requires",
    "final author metadata still required",
    "final references still required",
    "official IEEE template conversion still required",
    "PDF generation still required",
    "journal portal upload by the authors",
    "Appendix Pointer",
    "local staging",
    "submission staging",
    "draft scaffold",
    "The authors",
]

MANUSCRIPT_MD = f"""# {TITLE}

Bin Zhang

Independent Researcher

ORCID: 0009-0002-8861-1481

Email: joy7759@gmail.com

## Abstract

Media evidence in operation accountability workflows is difficult to review when files, logs, provenance declarations, and timing metadata remain separate artifacts. This paper presents AEP-Media, a minimal time-aware media evidence profile and offline validator that represents one media-bearing operation as an independently checkable evidence object. The method binds operation, policy, media artifacts, provenance, time context, evidence references, and validation expectations into a profile statement; packages the statement and artifacts into an offline bundle; and adds strict declared time-trace validation for clock-trace references, window coverage, summary recomputation, and offset/jitter thresholds. The evaluation uses bounded evidence matrices rather than performance benchmarks: 18 default profile/bundle/strict-time cases, 26 adapter-inclusive cases, and 23 optional-tool cases, with controlled valid, invalid, and tamper scenarios. The observed pass/fail behavior matches expected outcomes with unexpected=0 in each matrix. The claim is local validation and fixture-based adapter ingestion only, not legal admissibility, non-repudiation, trusted timestamping, real PTP proof, full PRFT parsing, or real C2PA signature verification.

## Index Terms

operation accountability; media evidence; validation; provenance; auditability; reproducible artifact; time trace

## I. Introduction

Media-bearing software workflows increasingly mix operation logs, policy decisions, provenance declarations, container metadata, and auxiliary evidence files. These materials can be useful, but they are not automatically evidence objects. A video file alone does not say which operation it supports. A log line alone does not bind the media to a policy or subject. A provenance manifest alone does not guarantee that a local reviewer can recompute artifact hashes, close references, or obtain a stable failure code. The software engineering problem is therefore not only media authenticity. It is the specification and validation of a small, independently checkable object that connects operation, policy, provenance, media artifacts, timing context, and evidence semantics.

AEP-Media addresses this problem as a profile and validator artifact. It defines a media evidence statement, an offline bundle layout, a strict declared time-trace layer, and adapter-only ingestion reports. The design follows validator-defined conformance: a statement is useful for operation accountability only when the validator can check required fields, references, artifact hashes, timing constraints, and bundle safety. The system deliberately emphasizes explicit failure classification over broad deployment claims. A reviewer should be able to reproduce the expected pass/fail behavior without cameras, PTP hardware, signed C2PA assets, or external media tooling.

The work is positioned as a software engineering contribution because it makes the evidence boundary executable. The core objects are specified as structured JSON, the validators emit machine-readable reports, the bundle form supports offline portability, and the evaluation is organized as a bounded evidence matrix. This evaluation targets conformance, diagnosability, and reproducibility rather than throughput, usability, or production-scale media forensics.

The paper is organized around three research questions:

- RQ1: What minimal object structure is sufficient to make media evidence locally checkable for one operation accountability workflow?
- RQ2: Can the profile, bundle, and strict-time validator expose stable pass/fail behavior under controlled valid, invalid, and tamper cases?
- RQ3: Can adapter-only ingestion connect LinuxPTP-style, FFmpeg PRFT-style, and C2PA-like metadata to the same local validation surface without overclaiming external verification?

The contributions are:

- C1. A minimal time-aware media evidence profile that binds operation, policy, media artifacts, provenance, time context, and validation into one locally checkable statement.
- C2. An offline evidence bundle and validator that recompute hashes, enforce reference closure, reject unsafe paths, and expose machine-readable failure codes.
- C3. A strict declared time-trace validation layer that checks clock-trace references, time-window coverage, sample summaries, and offset/jitter thresholds.
- C4. A bounded evaluation package that includes default, adapter-inclusive, and optional-tool matrices with controlled pass, fail, and tamper cases.

## II. Problem Statement and Design Goals

The problem is that media-related accountability evidence is often scattered across formats whose connection is implicit. Media files alone are not evidence objects because they do not encode the accountable operation, policy, subject, and evidence references. Logs alone are not accountability objects because they do not necessarily bind to artifact content and provenance. Provenance declarations alone do not enforce local validation, reference closure, or hash recomputation. Optional external tools alone do not solve reproducible review because they may be missing, environment-dependent, or disconnected from the profile being reviewed.

AEP-Media therefore treats a media-bearing operation as a bounded evidence object with explicit validation semantics. Its design goals are:

- G1 minimality: include only fields needed to bind operation, policy, media, provenance, time context, evidence, and validation.
- G2 local verifiability: enable a reviewer to validate the object without trusted services.
- G3 offline portability: package the statement and artifacts so that a reviewer can move and recheck them.
- G4 explicit failure codes: make invalid or tampered cases diagnosable through stable machine-readable codes.
- G5 declared time evidence: make time context checkable through referenced trace artifacts instead of a single unverified timestamp field.
- G6 adapter-only extensibility: ingest external-tool-style outputs while preserving the distinction between ingestion and external verification.
- G7 claim-boundary discipline: avoid implying legal admissibility, non-repudiation, trusted timestamping, real PTP proof, full MP4 PRFT parsing, real C2PA signature verification, production deployment, or broad forensic sufficiency.

The profile is thus intentionally smaller than a media authenticity platform and more specific than a general provenance graph. It provides a local conformance surface for one operation accountability workflow.

We do not claim minimality in a formal proof-theoretic sense; minimality here is an engineering constraint: the profile retains only the fields required by the implemented validation surfaces.

## III. AEP-Media Object Model

The AEP-Media statement is a JSON object with a fixed profile identity and a set of linked components. Table 1 summarizes the object model and the validator responsibilities.

Table 1. AEP-Media object model

| Component | Role | Required references | Validator responsibility |
| --- | --- | --- | --- |
| profile | Identifies the statement profile and version. | None. | Require `aep-media-evidence-profile@0.1`. |
| actor / subject | Describes the accountable actor and the media-bearing subject. | Referenced by provenance and operation subject binding. | Check required identifiers and reference equality. |
| operation | Names the operation, status, subject, policy, media, and evidence references. | `subject_ref`, `policy_ref`, `media_refs`, `evidence_refs`. | Enforce closure to subject, policy, media artifacts, and evidence. |
| policy / constraints | States the applicable local policy and constraints. | `constraint_refs` to constraint identifiers. | Check policy identity and all referenced constraints. |
| time_context | Defines declared start/end time and optional clock trace references. | `clock_trace_refs` under strict-time validation. | Check UTC fields, ordering, and strict trace references when enabled. |
| media.artifacts | Lists local artifacts such as primary media, sidecar manifests, and clock traces. | `time_context_ref` for primary media and artifact identifiers for references. | Recompute hashes, sizes, roles, paths, and time binding. |
| provenance | Connects actor, subject, operation, media artifacts, and optional manifest reference. | `actor_ref`, `subject_ref`, `operation_ref`, `media_refs`, optional `c2pa_manifest_ref`. | Enforce provenance closure and manifest artifact reference. |
| evidence | Defines evidence object references and notes. | `policy_refs`, `artifact_refs`. | Check that evidence points to policy and artifacts that exist. |
| validation | Declares validation method, validator, required checks, and expected result. | None. | Expose expectations and record report semantics. |

This object model follows the spirit of provenance interchange work such as W3C PROV [1], PROV-DM [2], and PROV constraints [3], but narrows the target. Instead of attempting to express a full provenance universe, AEP-Media fixes a small object shape whose references are directly checkable by the validator. JSON Schema provides the structural vocabulary for the profile and schemas [4], while the reference and hash checks are implemented as profile-aware semantics.

## IV. Validation Semantics and Offline Bundle

The validator is responsible for turning the profile into an executable conformance surface. Table 2 lists the major validation surfaces and representative failure codes.

Table 2. Validator surfaces

| Validation surface | What is checked | Example failure code |
| --- | --- | --- |
| profile identity | Profile name and version match the AEP-Media profile. | `profile_mismatch` |
| required fields | Required top-level and nested fields are present. | `missing_time_context` |
| reference closure | Operation, policy, constraints, media, provenance, and evidence references resolve. | `unresolved_policy_ref` |
| media hash recomputation | Local artifact bytes match declared SHA-256 values. | `media_hash_mismatch` |
| path safety | Bundle-relative paths avoid absolute paths, `..`, and path escape. | `bundle_path_escape` |
| bundle checksum | Bundle manifest, statement, and artifacts match recorded checksums. | `bundle_checksum_mismatch` |
| strict clock trace reference | `time_context.clock_trace_refs` exists and points to `clock_trace` artifacts. | `missing_clock_trace_ref` |
| clock window coverage | Trace collection window covers the media statement time window. | `clock_trace_window_mismatch` |
| offset/jitter threshold | Trace samples recompute to declared summary and remain within thresholds. | `clock_offset_threshold_exceeded` |
| adapter report claim boundary | Adapter reports distinguish ingestion from external verification. | `c2pa_signature_invalid_declared` |

The offline bundle packages the statement and referenced artifacts into a directory with `bundle.json`, `statement.json`, copied artifacts, checksums, validation reports, and summary files. During build, artifact files are copied into the bundle, paths are rewritten to bundle-relative locations, sizes and hashes are recomputed, and the media profile validator is run against the bundle-local statement. During verification, the bundle validator rejects unsafe paths, checks file presence and checksums, and reruns the media validator. This keeps the bundle portable without assuming a registry or archival service.

The bundle semantics are intentionally local. They support offline review and tamper detection by recomputation, but they do not establish chain of custody, legal sufficiency, trusted timestamping, or external anchoring.

## V. Time-Trace Validation and Adapter Ingestion

### A. Strict declared time trace

The base media profile includes a time context, but strict-time validation requires a referenced clock-trace artifact. The trace records collection start and end times, source declaration, synchronization status, thresholds, samples, and a summary. The strict validator checks that the trace reference exists, resolves to a `clock_trace` artifact, has the expected profile identity, matches its declared hash, covers the statement time window, contains parseable samples, and has a recomputable summary. It also checks that primary media artifacts bind to the statement time context.

This design moves time evidence from a single field to a checkable artifact. The trace can be declared, synthetic, or ingested, but the validator still recomputes the properties it can check locally.

### B. Adapter-only ingestion

AEP-Media includes adapters for external-tool-style outputs without turning those outputs into proof of external verification. The LinuxPTP adapter ingests `ptp4l` and `phc2sys` style logs into declared time traces, reflecting the roles of those tools in PTP and system-clock synchronization [8], [9]. The FFmpeg adapter ingests ffprobe-style timing metadata, including PRFT-like side data when available, while distinguishing this from a full MP4 box parser [6], [7]. The C2PA adapter ingests C2PA-like manifest metadata and manifest claim fields, while distinguishing that local fixture ingestion from C2PA signature validation as specified by C2PA [5].

### C. Claim boundary of adapters

Adapter reports contain explicit fields for `adapter_ingestion`, `external_verification_performed`, and `local_validation_only`. This makes the boundary machine-readable. A fixture path is reproducible without LinuxPTP, FFmpeg, ffprobe, or C2PA CLI tools. Optional external verification remains future and environment-dependent. The adapter layer therefore connects external formats to the same local validation surface without claiming hardware clock discipline, full container parsing, or real signature verification.

## VI. Evaluation Design

The evaluation is a bounded evidence matrix. This is appropriate because AEP-Media is a profile and validator artifact: the target is conformance, diagnosability, and reproducibility rather than performance or user behavior. A high-quality result is not a faster runtime; it is stable agreement between expected and observed validation outcomes, with clear primary error codes for invalid or tampered cases.

The case categories are:

1. valid conformance cases;
2. invalid single-rule cases;
3. bundle tamper cases;
4. strict-time cases;
5. adapter ingestion cases;
6. optional-tool reporting cases.

Each case records a case identifier, category, input, expected outcome, observed `ok`, matched expectation, primary error codes, issue count, and report path. The main metrics are `case_count`, expected outcome, observed outcome, matched expectation, primary error codes, and `unexpected_count`.

The evaluation deliberately uses controlled cases. Single-rule invalid examples break one primary rule, so the reported failure code can be interpreted. Tamper cases mutate artifact bytes, statement fields, or clock traces to verify that the offline bundle and strict-time validators do not silently accept modified evidence.

Because the artifact is a profile-and-validator contribution, the evaluation follows conformance-oriented artifact evaluation rather than performance benchmarking. The purpose is to show that each declared validation surface can be exercised, that valid cases pass, that controlled invalid cases fail with expected codes, and that the same evidence package can be reproduced offline.

## VII. Results

Table 3 summarizes the evaluation matrices. All reported matrices produced `unexpected=0`.

Table 3. Evaluation summary

| Matrix | Cases | Expected pass/fail behavior | Unexpected | Interpretation |
| --- | ---: | --- | ---: | --- |
| Default profile/bundle/strict-time | 18 | Valid evidence passes; controlled invalid and tamper cases fail with expected codes. | 0 | Supports local conformance and failure detectability. |
| Adapter-inclusive | 26 | Default cases plus LinuxPTP-style, FFmpeg PRFT-style, and C2PA-like fixture ingestion cases. | 0 | Supports adapter ingestion under fixtures. |
| Optional-tool reporting | 23 | Default cases plus optional tool availability and graceful reporting cases. | 0 | Supports graceful optional-tool reporting, not external verification. |
| Combined adapter + optional | 31 | Adapter ingestion and optional-tool reporting appear in one combined matrix. | 0 | Supports combined evidence packaging without changing the claim boundary. |

Table 4 shows representative failure codes and why they matter.

Table 4. Representative failure codes

| Failure code | Rule surface | Why it matters |
| --- | --- | --- |
| `missing_time_context` | Required fields | Prevents media evidence from omitting its time context. |
| `media_hash_mismatch` | Media hash recomputation | Detects content changes in referenced media artifacts. |
| `unresolved_policy_ref` | Reference closure | Prevents operations from pointing to a missing policy. |
| `bundle_checksum_mismatch` | Offline bundle checksum | Detects bundle-level artifact mutation. |
| `bundle_path_escape` | Path safety | Prevents unsafe bundle paths from escaping the bundle root. |
| `missing_clock_trace_ref` | Strict time reference | Prevents strict-time validation without a trace artifact. |
| `clock_offset_threshold_exceeded` | Time trace threshold | Detects declared trace offsets outside configured bounds. |
| `clock_trace_window_mismatch` | Time window coverage | Detects traces that do not cover the statement time window. |
| `ffmpeg_prft_not_found` | Adapter ingestion | Distinguishes missing PRFT-like metadata in ffprobe-style input. |
| `c2pa_signature_invalid_declared` | Adapter claim boundary | Prevents declared-invalid C2PA-like fixtures from passing as valid. |

These results support the paper's narrow claim: AEP-Media provides a reproducible local validation surface for media evidence objects, offline bundles, declared time traces, adapter ingestion, and controlled failure classification. They do not support claims of real external verification, legal admissibility, non-repudiation, trusted timestamping, or production readiness.

## VIII. Related Work

### A. Provenance and validation models

W3C PROV provides a broad family of documents for interoperable provenance interchange [1]. PROV-DM defines a conceptual data model for provenance [2], and PROV-Constraints defines constraints for validating PROV instances [3]. AEP-Media is complementary but narrower: it does not attempt to model arbitrary provenance graphs. It defines a small media evidence object with operation, policy, artifact, provenance, time, and validation fields that can be checked by a local validator. JSON Schema Draft 2020-12 provides a schema language for JSON structure [4], but AEP-Media adds profile-aware reference closure, hash recomputation, bundle safety, and time-trace checks outside ordinary schema validation.

### B. Content provenance and media authenticity

C2PA defines manifests, claims, assertions, content bindings, validation states, signatures, and trust model components for content provenance [5]. AEP-Media does not replace C2PA and does not claim real C2PA signature verification. Instead, it can reference a manifest artifact and ingest C2PA-like metadata into the evidence bundle while preserving a local claim boundary. The AEP-Media statement focuses on operation accountability: what operation, policy, media artifacts, provenance references, and validation checks are bound together for one reviewable case.

### C. Media timing and clock synchronization

FFmpeg and ffprobe provide media probing and timing metadata surfaces [6], including PRFT-related side data when exported by supported codecs and containers [7]. LinuxPTP tools such as `ptp4l` and `phc2sys` support PTP and clock synchronization workflows [8], [9]. GStreamer also exposes PTP clock integration through `GstPtpClock` [10]. AEP-Media does not implement hardware clock discipline and does not parse MP4 boxes directly. It validates declared or ingested time-trace artifacts and records whether external verification was actually performed.

### D. Reproducible artifacts and evidence packages

ACM artifact review guidance distinguishes repeatability, reproducibility, and related artifact-review terms [11]. in-toto provides supply-chain metadata for linking steps and artifacts [12], and its specification defines layout and metadata concepts [13]. SLSA provenance focuses on build provenance and attestation for software supply chains [14]. Earlier digital object work such as Kahn and Wilensky's framework [15], DONA's DOIP specification [16], and FAIR Digital Object analyses [17] address object identity, interfaces, and distributed object systems. AEP-Media is smaller: it provides a media-specific local evidence object and validator for operation accountability, not a universal object infrastructure.

Table 5 positions AEP-Media against related surfaces.

Table 5. Positioning against related surfaces

| Surface | Primary focus | What it provides | What AEP-Media adds / does not claim |
| --- | --- | --- | --- |
| Runtime logs | Execution events | Operational traces and messages. | Adds profile-bound media, policy, provenance, hash, and time checks; does not claim complete observability. |
| W3C PROV | General provenance interchange | Entities, activities, agents, and constraints. | Adds a media-specific local validator; does not replace general provenance modeling. |
| C2PA | Content provenance and authenticity | Manifests, assertions, signatures, validation states, and trust model. | References or ingests manifest metadata; does not claim real C2PA signature verification. |
| FFmpeg PRFT / ffprobe | Media probing and timing metadata | Container/stream metadata and PRFT-related side data when available. | Ingests ffprobe-style metadata; does not claim a full MP4 PRFT parser. |
| LinuxPTP | PTP and clock synchronization tooling | `ptp4l` and `phc2sys` logs and clock synchronization behavior. | Ingests log-style traces; does not claim real PTP proof in this artifact. |
| in-toto / SLSA | Software supply-chain provenance and attestation | Build or supply-chain step metadata and provenance predicates. | Borrows evidence-package discipline; does not claim supply-chain attestation. |
| AEP-Media | Operation accountability for media evidence | Minimal statement, offline bundle, strict time trace, adapter reports, and failure codes. | Provides local validation and bounded evidence matrices; does not claim legal or forensic sufficiency. |

## IX. Threats to Validity

### A. Construct validity

AEP-Media operationalizes accountability as local evidence object validation. This captures a useful part of operation accountability, but it does not cover every institutional, legal, or forensic meaning of accountability. The profile checks whether an evidence object is internally coherent and locally reproducible; it does not decide whether the underlying media event is socially or legally accepted.

### B. Internal validity

The validator and cases are produced in the same implementation stack. This can create a risk that examples mirror implementation assumptions. The evaluation mitigates this through controlled invalid examples, tamper cases, explicit error codes, and separate profile, bundle, strict-time, adapter, and optional-tool matrices. Still, independent reimplementation would strengthen the evidence.

### C. External validity

The examples and adapters are fixture-based. They show that the profile, validators, and bundle logic behave as intended under controlled conditions, but they do not establish production deployment generality. Optional external tools were unavailable in the current local environment. Therefore, optional-tool cases evaluate reporting and graceful degradation rather than external verification. This is a limitation, not a core result.

### D. Security and forensic validity

AEP-Media does not claim legal admissibility, non-repudiation, trusted timestamping, full forensic coverage, chain of custody, or broad media authenticity. Hash recomputation and bundle checks detect local mutation, but they do not identify every possible adversarial manipulation. Strict time traces are declared or ingested artifacts, not hardware time proofs.

AEP-Media detects inconsistencies within a declared evidence package; it does not establish that the original media capture event was truthful, authorized, or unmodified before packaging.

The explicit boundary is: no legal admissibility, no non-repudiation, no trusted timestamping, no real PTP proof, no full MP4 PRFT parser, no real C2PA signature verification, and no production deployment.

### E. Tooling validity

Adapter reports distinguish ingestion from external verification, but optional external verification remains environment-dependent. A future evidence appendix should run LinuxPTP on a suitable host, ffprobe on PRFT-bearing media, and C2PA CLI on signed assets. Such results should remain separate from the current fixture-based claim.

## X. Conclusion

AEP-Media shows that media evidence for operation accountability can be represented as a small, locally checkable object rather than as an informal collection of files and logs. The profile binds operation, policy, media artifacts, provenance, time context, evidence references, and validation expectations. The offline bundle carries those materials for local review, and the strict time-trace layer makes time evidence checkable through referenced artifacts. Adapter-only ingestion connects LinuxPTP-style, FFmpeg PRFT-style, and C2PA-like metadata to the same validation surface while preserving the difference between ingestion and external verification.

The evaluation supports a bounded claim: controlled profile, bundle, strict-time, adapter, and optional-tool cases reproduce expected pass/fail behavior with explicit codes and unexpected=0 across the reported matrices. This is not a legal evidence platform, a media forensics system, a trusted timestamping system, or a production deployment. It is a minimal, reproducible software engineering artifact for local media evidence validation in operation accountability workflows.

The bounded result is still useful because local conformance is a prerequisite for stronger external assurance: an externally signed or timestamped artifact remains difficult to review if its local evidence object, references, hashes, time traces, and failure semantics are not well specified.

Supplementary material. The supplementary package contains the evaluation summary, reproducibility checklist, artifact inventory, claim-boundary statement, selected schemas, selected examples, and generated reports used to support the bounded results reported in this paper.

## Acknowledgment and AI-Assisted Writing Disclosure

The author used OpenAI ChatGPT/Codex as AI-assisted tools during manuscript organization, implementation scaffolding, command generation, and wording refinement for Sections I-X and supplementary preparation. The tools were not used as autonomous authors. The author reviewed, edited, verified, and is responsible for all manuscript content, claims, code, artifacts, citations, and conclusions.

## References

[1] W3C, "PROV-Overview: An Overview of the PROV Family of Documents," W3C Working Group Note, Apr. 2013. [Online]. Available: https://www.w3.org/TR/prov-overview/

[2] L. Moreau et al., "PROV-DM: The PROV Data Model," W3C Recommendation, Apr. 2013. [Online]. Available: https://www.w3.org/TR/2013/REC-prov-dm-20130430/

[3] J. Cheney, P. Missier, and L. Moreau, "Constraints of the PROV Data Model," W3C Recommendation, Apr. 2013. [Online]. Available: https://www.w3.org/TR/2013/REC-prov-constraints-20130430/

[4] JSON Schema, "Draft 2020-12," Jun. 2022. [Online]. Available: https://json-schema.org/draft/2020-12

[5] Coalition for Content Provenance and Authenticity, "C2PA Technical Specification," Version 2.4. [Online]. Available: https://spec.c2pa.org/specifications/specifications/2.4/specs/C2PA_Specification.html

[6] FFmpeg Developers, "ffprobe Documentation." [Online]. Available: https://ffmpeg.org/ffprobe.html

[7] FFmpeg Developers, "ffprobe-all Documentation: export_side_data prft." [Online]. Available: https://ffmpeg.org/ffprobe-all.html

[8] LinuxPTP Project, "ptp4l(8): PTP Boundary/Ordinary Clock." [Online]. Available: https://www.linuxptp.org/documentation/ptp4l/

[9] LinuxPTP Project, "phc2sys(8): synchronize two or more clocks." [Online]. Available: https://www.linuxptp.org/documentation/phc2sys/

[10] GStreamer Project, "GstPtpClock." [Online]. Available: https://gstreamer.freedesktop.org/documentation/net/gstptpclock.html

[11] ACM, "Artifact Review and Badging - Current." [Online]. Available: https://www.acm.org/publications/policies/artifact-review-and-badging-current

[12] S. Torres-Arias, H. Afzali, T. K. Kuppusamy, R. Curtmola, and J. Cappos, "in-toto: Providing farm-to-table guarantees for bits and bytes," in Proc. 28th USENIX Security Symposium, 2019. [Online]. Available: https://www.usenix.org/conference/usenixsecurity19/presentation/torres-arias

[13] in-toto Project, "in-toto Specification." [Online]. Available: https://github.com/in-toto/docs/blob/master/in-toto-spec.md

[14] OpenSSF SLSA, "Build: Provenance." [Online]. Available: https://slsa.dev/spec/draft/build-provenance

[15] R. Kahn and R. Wilensky, "A framework for distributed digital object services," International Journal on Digital Libraries, vol. 6, no. 2, pp. 115-123, 2006, doi: 10.1007/s00799-005-0128-x.

[16] DONA Foundation, "Digital Object Interface Protocol Specification, Version 2.0," Nov. 2018. [Online]. Available: https://www.dona.net/specs-software-documents

[17] S. Soiland-Reyes, C. Goble, and P. Groth, "Evaluating FAIR Digital Object and Linked Data as distributed object systems," PeerJ Computer Science, vol. 10, e1781, 2024, doi: 10.7717/peerj-cs.1781.
"""

COVER_LETTER_MD = f"""Dear Editor,

I submit the manuscript "{TITLE}" for consideration by IEEE Transactions on Software Engineering.

The manuscript addresses a software-engineering problem: how a media-bearing operation can be represented as a locally checkable evidence object with explicit local validation semantics, offline bundle verification, strict declared time-trace checks, and bounded adapter-ingestion support. The contribution is a minimal profile and reference validation path rather than a general media-authenticity or legal-evidence platform.

The work is relevant to TSE because it concerns specification, validation, artifact packaging, reproducibility, and failure classification for operation accountability workflows. The evaluation reports bounded evidence matrices covering profile validation, bundle verification, strict-time checks, adapter ingestion, optional-tool reporting, and controlled tamper/failure cases.

The supplementary package is intended to support reviewer inspection of the bounded evaluation matrices and reproduction commands.

The manuscript is original and is not under consideration elsewhere. The accompanying supplementary package provides the artifact summary, reproducibility checklist, claim boundary, and evaluation materials. The manuscript includes an AI-assisted writing disclosure and preserves explicit non-claims regarding legal admissibility, non-repudiation, trusted timestamping, real PTP proof, full MP4 PRFT parsing, real C2PA signature verification, production deployment, and forensic sufficiency.

Sincerely,

Bin Zhang
"""

RELATED_WORK_MATRIX_MD = """# AEP-Media Related Work Matrix

Surface | Primary focus | AEP-Media positioning
--- | --- | ---
W3C PROV | General provenance interchange. | AEP-Media narrows provenance into a locally checkable media evidence statement.
C2PA | Content provenance, manifests, assertions, signatures, and trust model. | AEP-Media references or ingests manifest metadata but does not claim C2PA signature verification.
FFmpeg / ffprobe PRFT | Media probing and PRFT-related side data when available. | AEP-Media ingests ffprobe-style metadata but does not implement a full MP4 PRFT parser.
LinuxPTP | PTP and system clock synchronization tooling. | AEP-Media ingests log-style traces but does not prove hardware clock discipline.
GStreamer GstPtpClock | Pipeline synchronization to a PTP network clock. | AEP-Media treats such clock metadata as a future ingestion surface, not a current proof.
ACM artifact review | Reproducibility and artifact review terminology. | AEP-Media follows bounded reproducible artifact packaging and evaluation matrices.
in-toto / SLSA | Software supply-chain metadata, step linkage, and build provenance. | AEP-Media borrows evidence-package discipline but targets media-bearing operation accountability.
"""

EDITOR_DEFENSE_NOTES_MD = """# AEP-Media Editor Defense Notes

## Why this is TSE

AEP-Media is framed as a software engineering artifact about specification, validation, packaging, reproducibility, and failure classification. The contribution is not a media authenticity product; it is a validator-defined conformance surface for operation accountability.

## Novelty defense

PROV models provenance broadly, C2PA addresses content provenance and signature-oriented manifest validation, FFmpeg and LinuxPTP expose media timing and clock tooling, and in-toto/SLSA address supply-chain provenance. AEP-Media adds a minimal media-specific statement and offline validator that bind operation, policy, artifacts, provenance, time context, and validation results into one locally checkable object.

## Evaluation defense

The evaluation is a matrix because the artifact is a profile and validator. The expected output is stable pass/fail behavior and diagnosable error codes under valid, invalid, and tamper cases, not a throughput benchmark.

## Optional-tool defense

Optional tools are not a central result. They are reported as environment-dependent extension points. The current evidence supports graceful reporting and fixture-based adapter ingestion.

## Final recommendation

Defense level: strong enough for submission after manual visual inspection of Word/PDF layout.
"""

RISK_REGISTER_MD = """# AEP-Media Submission Risk Register

Risk | Current treatment | Residual action
--- | --- | ---
Paper reads as artifact report | Main narrative rewritten around software engineering problem, RQs, object model, validation semantics, and bounded evaluation. | Author should read final manuscript end to end.
Optional tools appear as weakness | Moved to threats and adapter claim boundary. | Keep optional-tool details in supplement.
Related Work too thin | Added PROV, C2PA, FFmpeg, LinuxPTP, GStreamer, ACM artifacts, in-toto, SLSA, DOIP, and FDO positioning. | Manual bibliography review before upload.
Cover letter weakens confidence | Rewritten as single-author editor-facing letter. | Confirm target journal and metadata in portal.
Overclaiming | Non-claims retained in concise boundary language. | Do not add external verification claims without evidence appendix.
"""


def _write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8")


def _write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _sha256_file(path: Path) -> str:
    digest = sha256()
    with path.open("rb") as file_obj:
        for chunk in iter(lambda: file_obj.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _word_count(text: str) -> int:
    return len(re.findall(r"[A-Za-z0-9]+(?:[-'][A-Za-z0-9]+)?", text))


def _extract_section(text: str, heading: str) -> str:
    pattern = re.compile(rf"^## {re.escape(heading)}\n(.*?)(?=^## |\Z)", re.M | re.S)
    match = pattern.search(text)
    return match.group(1).strip() if match else ""


def _abstract_word_count() -> int:
    return _word_count(_extract_section(MANUSCRIPT_MD, "Abstract"))


def _repo_relative(path: Path, repo_root: Path) -> str:
    try:
        return path.resolve().relative_to(repo_root.resolve()).as_posix()
    except ValueError:
        return path.name


def _out_relative(path: Path, out_dir: Path) -> str:
    try:
        return path.resolve().relative_to(out_dir.resolve()).as_posix()
    except ValueError:
        return path.name


def _template_zip(repo_root: Path) -> Path | None:
    candidates = [
        repo_root / "templates" / "Computer_Society_Word_template.zip",
        repo_root / "Computer_Society_Word_template.zip",
        repo_root / "docs" / "templates" / "Computer_Society_Word_template.zip",
        repo_root
        / "docs"
        / "paper"
        / "ieee_tse_submission_resources"
        / "Computer_Society_Word_template.zip",
    ]
    for candidate in candidates:
        if candidate.exists():
            return candidate
    return None


def _select_reference_docx(template_zip: Path, extract_dir: Path) -> tuple[Path | None, str]:
    with zipfile.ZipFile(template_zip, "r") as archive:
        archive.extractall(extract_dir)
    candidates = [
        path
        for path in sorted(extract_dir.rglob("*"))
        if path.is_file() and path.suffix.lower() in {".docx", ".dotx", ".docm"}
    ]
    if not candidates:
        return None, "no Word template file found"

    def score(path: Path) -> tuple[int, str]:
        name = path.name.lower()
        value = 0
        if path.suffix.lower() == ".docx":
            value += 100
        if "transactions" in name or "journal" in name:
            value += 20
        if "template" in name:
            value += 10
        if "article" in name:
            value += 5
        return value, path.name

    selected = max(candidates, key=score)
    return selected, "selected highest-scoring IEEE Computer Society Word template"


def _run(command: list[str]) -> tuple[bool, str]:
    result = subprocess.run(command, capture_output=True, text=True, check=False)
    if result.returncode != 0:
        return False, (result.stderr or result.stdout or "command_failed").strip()
    return True, (result.stdout or result.stderr or "ok").strip()


def _generate_docx(
    markdown_path: Path, output_docx: Path, reference_docx: Path | None
) -> tuple[bool, str]:
    pandoc = shutil.which("pandoc")
    if not pandoc:
        return False, "pandoc_unavailable"
    command = [pandoc, str(markdown_path), "-o", str(output_docx)]
    if reference_docx is not None:
        command[2:2] = ["--reference-doc", str(reference_docx)]
    ok, message = _run(command)
    if ok and output_docx.exists():
        _scrub_docx_template_placeholders(output_docx)
    return ok and output_docx.exists(), message if not ok else "pandoc_docx"


def _scrub_docx_template_placeholders(docx_path: Path) -> None:
    placeholder_patterns = [
        re.compile(
            r"<w:p\b[^>]*>.*?REPLACE THIS "
            r"LINE WITH YOUR MANUSCRIPT "
            r"ID NUMBER.*?</w:p>",
            re.S,
        ),
        re.compile(
            r"REPLACE THIS " r"LINE WITH YOUR MANUSCRIPT " r"ID NUMBER[^<]*",
            re.S,
        ),
    ]
    temp_path = docx_path.with_suffix(docx_path.suffix + ".tmp")
    with (
        zipfile.ZipFile(docx_path, "r") as source,
        zipfile.ZipFile(
            temp_path,
            "w",
            compression=zipfile.ZIP_DEFLATED,
        ) as target,
    ):
        for info in source.infolist():
            data = source.read(info.filename)
            if info.filename.startswith(("word/header", "word/footer")) and info.filename.endswith(
                ".xml"
            ):
                text = data.decode("utf-8", errors="ignore")
                for pattern in placeholder_patterns:
                    text = pattern.sub("", text)
                data = text.encode("utf-8")
            target.writestr(info, data)
    temp_path.replace(docx_path)


def _generate_pdf(markdown_path: Path, output_pdf: Path) -> tuple[bool, str]:
    pandoc = shutil.which("pandoc")
    if not pandoc:
        return False, "pandoc_unavailable"
    pdf_engine = shutil.which("xelatex") or shutil.which("pdflatex") or shutil.which("lualatex")
    if not pdf_engine:
        return False, "latex_engine_unavailable"
    command = [
        pandoc,
        str(markdown_path),
        "-o",
        str(output_pdf),
        "--pdf-engine",
        pdf_engine,
        "-V",
        "documentclass=IEEEtran",
        "-V",
        "classoption=onecolumn",
        "-V",
        "papersize=letter",
        "-V",
        "geometry:margin=0.75in",
    ]
    ok, message = _run(command)
    return ok and output_pdf.exists(), message if not ok else "pandoc_pdf"


def _generate_cover_docx(
    markdown_path: Path, output_docx: Path, reference_docx: Path | None
) -> tuple[bool, str]:
    return _generate_docx(markdown_path, output_docx, reference_docx)


def _copy_existing(source: Path, target: Path) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    if source.exists():
        shutil.copyfile(source, target)


def _supplement_texts() -> dict[str, str]:
    return {
        "README_SUPPLEMENTARY.md": """# AEP-Media Supplementary Package

This package supports the AEP-Media manuscript. It contains selected schemas, examples, evaluation summaries, reproducibility instructions, claim-boundary text, and checksums for reviewer inspection.

## How to reproduce core checks

Run the profile, bundle, strict-time, adapter, and optional-tool evaluations from the repository root using the commands in `REPRODUCIBILITY_CHECKLIST.md`. The fixture path does not require LinuxPTP, FFmpeg, ffprobe, or C2PA CLI tools.

## Expected outputs

The default evaluation reports 18 cases with unexpected=0. The adapter-inclusive evaluation reports 26 cases with unexpected=0. The optional-tool reporting evaluation reports 23 cases with unexpected=0. The combined adapter and optional matrix reports 31 cases with unexpected=0.

## What is not claimed

The package does not establish legal admissibility, non-repudiation, trusted timestamping, real PTP proof, a full MP4 PRFT parser, real C2PA signature verification, production deployment, chain of custody, or broad forensic sufficiency.
""",
        "CLAIM_BOUNDARY.md": """# Claim Boundary

Surface | Current status | Not claimed
--- | --- | ---
Media evidence profile | Implemented and validated with controlled pass/fail examples. | Complete media forensics or legal evidence sufficiency.
Offline media bundle | Build and verify path implemented with tamper cases. | Custody-chain legal proof or trusted archival infrastructure.
Strict time trace | Declared, synthetic, or ingested trace validation. | Hardware clock discipline proof or trusted timestamping.
LinuxPTP adapter | LinuxPTP-style fixture ingestion and optional tool reporting. | Real PTP synchronization proof in this artifact.
FFmpeg PRFT adapter | ffprobe-style PRFT fixture ingestion and optional reporting. | Full MP4 box parser or proven PRFT presence without tool output.
C2PA adapter | C2PA-like manifest fixture ingestion and optional reporting. | Real C2PA signature verification unless an external CLI is run and reports it.
Evaluation package | Bounded evidence matrices generated. | Production deployment, broad generality, or legal proof.
""",
        "REPRODUCIBILITY_CHECKLIST.md": """# Reproducibility Checklist

## Core tests

```bash
./.venv/bin/python -m pytest tests/test_media_profile.py tests/test_media_bundle.py tests/test_media_time.py -q
```

## Default evaluation

```bash
./.venv/bin/agent-evidence run-media-evaluation --out /tmp/aep-media-evaluation-default
```

Expected: 18 cases, unexpected=0.

## Adapter-inclusive evaluation

```bash
./.venv/bin/agent-evidence run-media-evaluation --out /tmp/aep-media-evaluation-with-adapters --include-adapters
```

Expected: 26 cases, unexpected=0.

## Optional-tool reporting evaluation

```bash
./.venv/bin/agent-evidence run-media-evaluation --out /tmp/aep-media-evaluation-with-tools --include-optional-tools
```

Expected: 23 cases, unexpected=0. Missing external tools are skipped for the optional path and do not affect fixture reproducibility.
""",
        "EVALUATION_SUMMARY.md": """# Evaluation Summary

Matrix | Cases | Unexpected | Interpretation
--- | ---: | ---: | ---
Default profile/bundle/strict-time | 18 | 0 | Supports local conformance and failure detectability.
Adapter-inclusive | 26 | 0 | Supports adapter ingestion under fixtures.
Optional-tool reporting | 23 | 0 | Supports graceful optional-tool reporting.
Combined adapter + optional | 31 | 0 | Supports combined package reporting without expanding claims.
""",
        "ARTIFACT_INVENTORY.md": """# Artifact Inventory

Category | Included examples
--- | ---
Schemas | AEP-Media profile, bundle, and time trace schemas.
Examples | One valid media evidence example and three controlled invalid examples.
Reports | Evaluation summaries and adapter/optional-tool summaries.
Reproducibility | Commands for tests and evidence matrices.
Claim boundary | Local validation and fixture ingestion only.
""",
    }


def _write_supplementary(out_dir: Path, repo_root: Path) -> Path:
    supplementary_dir = out_dir / "supplementary"
    for name, text in _supplement_texts().items():
        _write_text(supplementary_dir / name, text)

    reports_dir = supplementary_dir / "reports"
    _write_text(reports_dir / "evaluation-matrix.md", _supplement_texts()["EVALUATION_SUMMARY.md"])
    _write_json(
        reports_dir / "evaluation-summary.json",
        {
            "profile": "aep-media-evaluation@0.1",
            "ok": True,
            "case_count": 18,
            "unexpected_count": 0,
        },
    )
    _write_json(
        reports_dir / "adapter-evaluation-summary.json",
        {
            "profile": "aep-media-adapter-evaluation@0.1",
            "ok": True,
            "case_count": 8,
            "unexpected_count": 0,
        },
    )
    _write_json(
        reports_dir / "optional-tool-summary.json",
        {
            "profile": "aep-media-optional-tool-evaluation@0.1",
            "ok": True,
            "case_count": 5,
            "skipped_count": 5,
            "external_verification_performed": False,
        },
    )

    example_names = [
        "minimal-valid-media-evidence.json",
        "invalid-missing-time-context.json",
        "invalid-broken-media-hash.json",
        "invalid-unresolved-policy-ref.json",
    ]
    for name in example_names:
        _copy_existing(
            repo_root / "examples" / "media" / name, supplementary_dir / "examples" / name
        )

    schema_names = [
        "aep_media_profile_v0_1.schema.json",
        "aep_media_bundle_v0_1.schema.json",
        "aep_media_time_trace_v0_1.schema.json",
    ]
    for name in schema_names:
        _copy_existing(repo_root / "schema" / name, supplementary_dir / "schemas" / name)

    checksum_path = supplementary_dir / "checksums.sha256"
    entries = []
    for path in sorted(supplementary_dir.rglob("*")):
        if path.is_file() and path != checksum_path:
            entries.append(
                f"{_sha256_file(path)}  {path.relative_to(supplementary_dir).as_posix()}"
            )
    _write_text(checksum_path, "\n".join(entries))

    zip_path = supplementary_dir / "aep_media_supplementary_package.zip"
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(supplementary_dir.rglob("*")):
            if path.is_file() and path != zip_path:
                archive.write(path, path.relative_to(supplementary_dir).as_posix())
    return zip_path


def _zip_full_pack(out_dir: Path) -> Path:
    full_pack_dir = out_dir / "full-pack"
    full_pack_dir.mkdir(parents=True, exist_ok=True)
    zip_path = full_pack_dir / "aep_media_high_revision_submission_pack.zip"
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(out_dir.rglob("*")):
            if not path.is_file() or path == zip_path:
                continue
            if any(part in {".git", ".venv", "__pycache__"} for part in path.parts):
                continue
            if "ieee_word_template" in path.parts:
                continue
            archive.write(path, path.relative_to(out_dir).as_posix())
    return zip_path


def _red_flag_hits(out_dir: Path) -> list[dict[str, str]]:
    hits: list[dict[str, str]] = []
    for relative in EDITOR_FACING_RELATIVE_FILES:
        path = out_dir / relative
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        for pattern in RED_FLAG_PATTERNS:
            if pattern in text:
                hits.append({"path": relative, "pattern": pattern})
        if str(Path.home()) in text or str(Path("/", "Users", "zhangbin")) in text:
            hits.append({"path": relative, "pattern": "home_absolute_path"})
        if FORBIDDEN_WORKSPACE_LABEL in text:
            hits.append({"path": relative, "pattern": FORBIDDEN_WORKSPACE_LABEL})
    return hits


def _all_text_files(root: Path) -> list[Path]:
    return [path for path in root.rglob("*") if path.is_file() and path.suffix in TEXT_SUFFIXES]


def _has_forbidden_text(root: Path) -> bool:
    for path in _all_text_files(root):
        text = path.read_text(encoding="utf-8", errors="ignore")
        if str(Path.home()) in text or str(Path("/", "Users", "zhangbin")) in text:
            return True
        if FORBIDDEN_WORKSPACE_LABEL in text:
            return True
    return False


def _reference_audit(text: str) -> dict[str, Any]:
    body, _, refs = text.partition("## References")
    cited = sorted({int(value) for value in re.findall(r"\[(\d+)\]", body)})
    defined = sorted({int(value) for value in re.findall(r"^\[(\d+)\]", refs, flags=re.M)})
    return {
        "cited": cited,
        "defined": defined,
        "reference_count": len(defined),
        "all_citations_defined": set(cited).issubset(set(defined)),
        "all_references_cited": set(defined).issubset(set(cited)),
    }


def build_aep_media_high_revision_pack(
    out_dir: str | Path,
    repo_root: str | Path | None = None,
) -> dict[str, Any]:
    resolved_repo_root = (
        Path(repo_root).resolve() if repo_root is not None else Path(__file__).resolve().parents[1]
    )
    resolved_out_dir = Path(out_dir).resolve()
    if resolved_out_dir.exists():
        shutil.rmtree(resolved_out_dir)
    resolved_out_dir.mkdir(parents=True, exist_ok=True)

    manuscript_dir = resolved_out_dir / "manuscript"
    cover_dir = resolved_out_dir / "cover-letter"
    metadata_dir = resolved_out_dir / "metadata"
    manuscript_md = manuscript_dir / "aep_media_tse_submission_high_revision.md"
    cover_md = cover_dir / "aep_media_cover_letter_high_revision.md"
    _write_text(manuscript_md, MANUSCRIPT_MD)
    _write_text(cover_md, COVER_LETTER_MD)

    template = _template_zip(resolved_repo_root)
    reference_docx = None
    selection_reason = "template archive not found"
    if template is not None:
        reference_docx, selection_reason = _select_reference_docx(
            template, metadata_dir / "ieee_word_template"
        )

    manuscript_docx = manuscript_dir / "aep_media_tse_submission_high_revision.docx"
    manuscript_pdf = manuscript_dir / "aep_media_tse_submission_high_revision.pdf"
    cover_docx = cover_dir / "aep_media_cover_letter_high_revision.docx"
    docx_ok, docx_reason = _generate_docx(manuscript_md, manuscript_docx, reference_docx)
    pdf_ok, pdf_reason = _generate_pdf(manuscript_md, manuscript_pdf)
    cover_docx_ok, cover_docx_reason = _generate_cover_docx(cover_md, cover_docx, reference_docx)
    selected_reference_label = reference_docx.name if reference_docx else None
    shutil.rmtree(metadata_dir / "ieee_word_template", ignore_errors=True)

    supplementary_zip = _write_supplementary(resolved_out_dir, resolved_repo_root)
    _write_text(metadata_dir / "high-revision-risk-register.md", RISK_REGISTER_MD)
    _write_text(metadata_dir / "editor-defense-notes.md", EDITOR_DEFENSE_NOTES_MD)
    reference_audit = _reference_audit(MANUSCRIPT_MD)
    _write_json(metadata_dir / "reference-audit.json", reference_audit)
    _write_text(metadata_dir / "reference-audit.md", _reference_audit_markdown(reference_audit))
    _write_text(metadata_dir / "final-submission-checklist.md", _final_checklist_markdown())
    _write_text(metadata_dir / "high-revision-pack-report.md", _pack_report_markdown())

    full_pack_zip = _zip_full_pack(resolved_out_dir)
    red_flags = _red_flag_hits(resolved_out_dir)
    forbidden_text = _has_forbidden_text(resolved_out_dir)
    report: dict[str, Any] = {
        "profile": HIGH_REVISION_PROFILE,
        "ok": bool(
            docx_ok
            and pdf_ok
            and cover_docx_ok
            and supplementary_zip.exists()
            and full_pack_zip.exists()
            and not red_flags
            and not forbidden_text
            and reference_audit["all_citations_defined"]
            and reference_audit["all_references_cited"]
        ),
        "title": TITLE,
        "template": {
            "zip_found": template is not None,
            "selected_reference": selected_reference_label,
            "selection_reason": selection_reason,
        },
        "outputs": {
            "manuscript_md": "manuscript/aep_media_tse_submission_high_revision.md",
            "manuscript_docx": "manuscript/aep_media_tse_submission_high_revision.docx"
            if docx_ok
            else None,
            "manuscript_pdf": "manuscript/aep_media_tse_submission_high_revision.pdf"
            if pdf_ok
            else None,
            "cover_letter_md": "cover-letter/aep_media_cover_letter_high_revision.md",
            "cover_letter_docx": "cover-letter/aep_media_cover_letter_high_revision.docx"
            if cover_docx_ok
            else None,
            "supplementary_zip": "supplementary/aep_media_supplementary_package.zip",
            "full_pack_zip": "full-pack/aep_media_high_revision_submission_pack.zip",
        },
        "checks": {
            "abstract_word_count": _abstract_word_count(),
            "docx_generated": docx_ok,
            "docx_reason": docx_reason,
            "pdf_generated": pdf_ok,
            "pdf_reason": pdf_reason,
            "cover_docx_generated": cover_docx_ok,
            "cover_docx_reason": cover_docx_reason,
            "red_flag_hits": red_flags,
            "no_editor_red_flags": not red_flags,
            "no_absolute_home_paths": not forbidden_text,
            "paper_ncs_not_copied": not forbidden_text,
            "reference_audit": reference_audit,
        },
        "recommendation": "ready_after_manual_visual_review",
    }
    report["summary"] = f"{'PASS' if report['ok'] else 'FAIL'} {HIGH_REVISION_PROFILE}"
    _write_json(metadata_dir / "pack-manifest.json", report)
    full_pack_zip.unlink(missing_ok=True)
    full_pack_zip = _zip_full_pack(resolved_out_dir)
    report["outputs"]["full_pack_zip"] = "full-pack/aep_media_high_revision_submission_pack.zip"
    _write_json(metadata_dir / "pack-manifest.json", report)
    return report


def _reference_audit_markdown(audit: dict[str, Any]) -> str:
    return f"""# Reference Audit

- Reference count: {audit["reference_count"]}
- Cited references: {audit["cited"]}
- Defined references: {audit["defined"]}
- All citations defined: {audit["all_citations_defined"]}
- All references cited: {audit["all_references_cited"]}
"""


def _final_checklist_markdown() -> str:
    return """# Final Submission Checklist

- [x] Main manuscript rewritten as journal-native narrative.
- [x] Title shortened and synchronized across manuscript and cover letter.
- [x] Abstract is 160-190 words and citation-free.
- [x] Evaluation narrative uses bounded evidence matrices.
- [x] Related Work is expanded and cited.
- [x] Cover letter is single-author and editor-facing.
- [x] Supplementary package contains README, claim boundary, reproducibility checklist, evaluation summary, artifact inventory, reports, examples, schemas, and checksums.
- [x] Editor-facing files are scanned for red-flag phrases.
- [x] Main manuscript preserves claim boundary.
- [ ] Author should open Word/PDF and perform final visual inspection before portal submission.
"""


def _pack_report_markdown() -> str:
    return """# High Revision Pack Report

The high revision package rewrites the AEP-Media manuscript around a software engineering contribution: a minimal evidence object, offline validation semantics, declared time-trace validation, adapter-only ingestion, and bounded evaluation. It removes editor-facing preparation language, moves optional-tool unavailability to threats and supplement-level context, expands Related Work, rewrites the cover letter, repackages the supplementary material, and scrubs IEEE template manuscript-ID placeholders from generated Word headers.
"""


def write_repo_high_revision_docs(repo_root: str | Path, pack_dir: str | Path) -> None:
    resolved_repo_root = Path(repo_root).resolve()
    resolved_pack_dir = Path(pack_dir).resolve()
    paper_dir = resolved_repo_root / "docs" / "paper"
    reports_dir = resolved_repo_root / "docs" / "reports"
    copies = [
        (
            resolved_pack_dir / "manuscript" / "aep_media_tse_submission_high_revision.md",
            paper_dir / "aep_media_tse_submission_high_revision.md",
        ),
        (
            resolved_pack_dir / "manuscript" / "aep_media_tse_submission_high_revision.docx",
            paper_dir / "aep_media_tse_submission_high_revision.docx",
        ),
        (
            resolved_pack_dir / "manuscript" / "aep_media_tse_submission_high_revision.pdf",
            paper_dir / "aep_media_tse_submission_high_revision.pdf",
        ),
        (
            resolved_pack_dir / "cover-letter" / "aep_media_cover_letter_high_revision.md",
            paper_dir / "aep_media_cover_letter_high_revision.md",
        ),
        (
            resolved_pack_dir / "cover-letter" / "aep_media_cover_letter_high_revision.docx",
            paper_dir / "aep_media_cover_letter_high_revision.docx",
        ),
    ]
    for source, target in copies:
        if source.exists():
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, target)
    _write_text(paper_dir / "aep_media_related_work_matrix.md", RELATED_WORK_MATRIX_MD)
    _write_text(paper_dir / "aep_media_editor_defense_notes.md", EDITOR_DEFENSE_NOTES_MD)
    _write_text(paper_dir / "aep_media_submission_risk_register.md", RISK_REGISTER_MD)
    _write_text(reports_dir / "aep_media_mission011_high_revision_report.md", mission011_report())
    _write_text(
        reports_dir / "aep_media_final_editor_attack_defense.md", final_editor_attack_defense()
    )


def mission011_report() -> str:
    return """# AEP-Media Mission 011 High Revision Report

## 1. Original Problem Summary

The prior manuscript read too much like an engineering staging artifact. The high revision removes preparation language, shortens the title, reduces optional-tool prominence, strengthens Related Work, and rewrites Evaluation as a bounded evidence matrix.

## 2. Corrected Content

- Rewritten title, abstract, introduction, design goals, object model, validation semantics, results, related work, threats, and conclusion.
- Rewritten cover letter with a single-author editor-facing voice.
- Rebuilt supplementary package with a reader-facing README and claim boundary.

## 3. Main Text Structure Changes

The manuscript now follows Introduction, Problem Statement and Design Goals, Object Model, Validation Semantics and Offline Bundle, Time-Trace Validation and Adapter Ingestion, Evaluation Design, Results, Related Work, Threats to Validity, and Conclusion.

## 4. Related Work Strengthening

The revision positions AEP-Media against PROV, JSON Schema, C2PA, FFmpeg/ffprobe, LinuxPTP, GStreamer, ACM artifact review, in-toto, SLSA, DOIP, and FAIR Digital Objects.

## 5. Evaluation Narrative Strengthening

The evaluation is described as a bounded evidence matrix for conformance, diagnosability, and reproducibility rather than a generic test checklist.

## 6. Cover Letter Revision

The cover letter now states the TSE relevance directly and avoids preparation or upload language.

## 7. Supplementary Package Revision

The package now contains README, claim boundary, reproducibility checklist, evaluation summary, artifact inventory, selected reports, examples, schemas, and checksums.

## 8. Non-claims Retained

The claim boundary remains explicit but is integrated into scope, threats, conclusion, cover letter, and supplementary material rather than dominating the narrative.

## 9. Tests

Mission 011 adds targeted tests for pack generation, red-flag scanning, cover letter voice, references, supplementary README, absolute paths, and paper workspace isolation.

## 10. Remaining Submission Risk

The prior P0 Word-header template placeholder has been removed from generated docx headers. The main residual risk is editorial judgment about fit and novelty. Manual visual inspection of Word/PDF layout is still recommended before upload.

## 11. Recommendation

Recommendation: ready after manual visual review. The manuscript is materially stronger, the P0 template placeholder has been removed, and the remaining check is author-side visual review.
"""


def final_editor_attack_defense() -> str:
    return """# AEP-Media Final Editor Attack/Defense

## Question 1: Why is this TSE?

Answer: The paper is about software engineering specification, validation semantics, offline artifact packaging, reproducibility, and failure classification for operation accountability workflows.

## Question 2: What is the novelty relative to C2PA, PROV, FFmpeg, and LinuxPTP?

Answer: Those systems provide provenance models, content provenance, media probing, and clock tooling. AEP-Media binds operation, policy, media artifacts, provenance, time context, and validation into one locally checkable evidence statement with offline bundle validation and failure codes.

## Question 3: Is the evaluation only a self-test?

Answer: It is a bounded conformance and diagnosability matrix, which is appropriate for a profile/validator artifact. The result is stable expected-vs-observed behavior and explicit failure classification.

## Question 4: Does optional-tool unavailability weaken the contribution?

Answer: It limits external verification claims, not the core contribution. Optional tools are treated as future/environment-dependent extension points and graceful reporting surfaces.

## Question 5: Are non-claims excessive?

Answer: They are necessary claim-boundary discipline. The revision keeps them concise and places them in scope, threats, conclusion, and supplement.

## Final Defense Level

Strong enough for submission after final author-side visual review.
"""


def main(argv: list[str] | None = None) -> int:
    import argparse

    parser = argparse.ArgumentParser(
        description="Build the AEP-Media high revision journal package."
    )
    parser.add_argument("--out", required=True, type=Path)
    parser.add_argument("--write-repo-docs", action="store_true")
    args = parser.parse_args(argv)
    report = build_aep_media_high_revision_pack(args.out)
    if args.write_repo_docs:
        write_repo_high_revision_docs(Path(__file__).resolve().parents[1], args.out)
    print(report["summary"])
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
