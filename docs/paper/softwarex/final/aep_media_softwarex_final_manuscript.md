# AEP-Media: Reusable Research Software for Offline Validation of Time-Aware Media Evidence Bundles

## Authors

Bin Zhang

Independent Researcher

ORCID: 0009-0002-8861-1481

Email: joy7759@gmail.com

## Abstract

AEP-Media is reusable research software for representing a media-bearing operation as a locally checkable evidence bundle. It provides a minimal time-aware media evidence profile, JSON schemas, controlled examples, validators, command-line tools, offline bundle build and verification, strict declared time-trace validation, adapter-only ingestion interfaces, evaluation matrices, and release packaging reports. The software is intended for researchers studying operation accountability, media evidence packaging, provenance boundaries, and reproducible validation artifacts. AEP-Media checks profile identity, required fields, reference closure, artifact hashes, path safety, bundle checksums, declared clock-trace coverage, clock-trace summaries, and offset/jitter thresholds. Its evaluation materials exercise valid, invalid, tamper, adapter-ingestion, and optional-tool reporting cases with expected pass/fail behavior. The current claim is local validation and fixture-based adapter ingestion. AEP-Media does not claim legal admissibility, non-repudiation, trusted timestamping, real PTP proof, full MP4 PRFT parsing, real C2PA signature verification, chain of custody, or production deployment.

## Keywords

media evidence; operation accountability; research software; provenance; offline validation; evidence bundle

## Metadata

| Nr | Code metadata description | Metadata |
| --- | --- | --- |
| C1 | Current code version | `aep-media-v0.1.0` |
| C2 | Permanent link to code/repository used for this code version | `https://github.com/joy7758/agent-evidence` |
| C3 | Legal code license | Apache-2.0 |
| C4 | Code versioning system used | git |
| C5 | Software code languages, tools and services used | Python; JSON Schema; pytest; Click CLI; Pandoc/LaTeX only for manuscript packaging |
| C6 | Compilation requirements, operating environments and dependencies | Python 3.11+; install with `python -m pip install -e .`; optional LinuxPTP, FFmpeg/ffprobe, and C2PA tools are not required for fixture-based validation |
| C7 | If available, link to developer documentation/manual | `https://github.com/joy7758/agent-evidence`; repository documentation under `README.md`, `spec/`, `schema/`, `examples/media/`, `demo/`, and `docs/reports/` |
| C8 | Support email for questions | joy7759@gmail.com |

## 1. Motivation and significance

Researchers working with media-bearing operations often need to review disconnected artifacts: media files, logs, provenance declarations, timing metadata, policy references, and validation reports. These objects are difficult to inspect consistently when they are not bound into a local evidence object with explicit validation semantics. AEP-Media addresses this gap by providing a reusable software layer for turning such materials into locally checkable evidence bundles with machine-readable failure codes.

The problem is deliberately bounded. AEP-Media is not a legal evidence platform and does not attempt to prove external authenticity. Its purpose is to make the local validation boundary explicit: which fields must be present, which references must close, which files must match declared hashes, which time traces cover a declared window, and which failures are reported when a controlled rule is broken. This local conformance layer is useful before stronger external assurance mechanisms such as signing, trusted timestamping, or deployed capture pipelines are added.

AEP-Media is positioned next to provenance, media-authenticity, timing, and artifact-review surfaces rather than as a replacement for them. W3C PROV provides general provenance concepts [1,2]. C2PA focuses on content provenance and manifest-based authenticity [3]. FFmpeg/ffprobe and LinuxPTP expose media timing and clock-synchronization surfaces [4,5], while GStreamer provides a PTP clock interface for media pipelines [6]. JSON Schema supports structured validation [7], and artifact-review practices emphasize inspectable and reproducible software packages [8]. AEP-Media contributes a concrete local validation boundary that binds media artifacts, declared provenance, declared time traces, bundle integrity, and failure codes into one reusable research software artifact.

## 2. Software description

AEP-Media extends the `agent-evidence` package with a media-focused profile and validation path. A media evidence statement binds an actor, subject, operation, policy, constraints, time context, media artifacts, provenance references, evidence notes, and validation expectations into one object. The profile validator checks that the statement is structurally complete and locally consistent.

The offline bundle layer packages a statement and its artifacts into a portable directory. The builder copies artifacts, rewrites paths to bundle-local locations, recomputes hashes and sizes, writes checksums, and emits validation reports. The verifier rejects unsafe paths, missing artifacts, checksum mismatches, and media profile failures. This allows review without relying on the original runtime layout.

The strict-time layer validates declared clock-trace artifacts. It checks trace references, artifact roles, trace hashes, trace profile identity, collection window coverage, sample validity, summary recomputation, offset thresholds, jitter thresholds, and media binding to the declared time context.

The adapter layer is ingestion-only. LinuxPTP-style logs, FFmpeg PRFT-style timing metadata, and C2PA-like manifest metadata can be normalized into AEP-Media reports. Adapter reports distinguish fixture ingestion from optional external-tool reporting and do not imply external verification unless a future environment-specific run records it. This boundary is important because real clock discipline, PRFT extraction, and C2PA signature verification depend on external tools and environment-specific evidence.

The main modules are:

- `agent_evidence/media_profile.py`: media profile validation.
- `agent_evidence/media_bundle.py`: offline bundle build and verification.
- `agent_evidence/media_time.py`: strict declared time-trace validation.
- `agent_evidence/adapters/linuxptp.py`: LinuxPTP-style trace ingestion.
- `agent_evidence/adapters/ffmpeg_prft.py`: FFmpeg PRFT-style metadata ingestion.
- `agent_evidence/adapters/c2pa_manifest.py`: C2PA-like manifest ingestion.
- `agent_evidence/media_evaluation.py`: default evaluation matrix.
- `agent_evidence/media_adapter_evaluation.py`: adapter-inclusive evaluation.
- `agent_evidence/media_optional_tools.py`: optional external-tool reporting.
- `agent_evidence/media_release_pack.py`: release pack assembly.

## 3. Illustrative examples

A typical profile validation run is:

```bash
agent-evidence validate-media-profile \
  examples/media/minimal-valid-media-evidence.json
```

A minimal offline bundle workflow is:

```bash
agent-evidence build-media-bundle \
  examples/media/minimal-valid-media-evidence.json \
  --out /tmp/aep-media-bundle-check

agent-evidence verify-media-bundle \
  /tmp/aep-media-bundle-check
```

A strict-time validation run is:

```bash
agent-evidence validate-media-time-profile \
  examples/media/time/minimal-valid-time-aware-media-evidence.json
```

The evaluation matrix can be reproduced with:

```bash
agent-evidence run-media-evaluation \
  --out /tmp/aep-media-evaluation
```

The repository includes valid examples, controlled invalid examples, strict-time fixtures, adapter fixtures, and tamper cases. These allow researchers to reproduce the intended pass/fail behavior without installing LinuxPTP, FFmpeg, ffprobe, or C2PA. The archived software release is available from Zenodo as version `aep-media-v0.1.0` [9].

## 4. Impact

AEP-Media supports research on operation accountability, media evidence packaging, provenance boundaries, and reproducible validation artifacts. It gives researchers a concrete software artifact for asking whether a declared media evidence package is internally consistent and portable. This is useful for experiments that need a stable evidence-object representation rather than ad hoc media files and logs.

The evaluation is conformance-oriented. Prior release reports record 18 default cases, 26 adapter-inclusive cases, 23 optional-tool reporting cases, and 31 combined adapter/optional-tool cases, all with `unexpected=0`. The case categories include valid conformance cases, invalid single-rule cases, bundle tamper cases, strict-time failures, adapter-ingestion cases, and optional-tool reporting cases. Expected failures include missing time context, media hash mismatch, unresolved policy reference, bundle checksum mismatch, path escape, missing clock-trace reference, clock offset threshold exceedance, clock window mismatch, missing PRFT metadata, and declared invalid C2PA-like signature status.

The impact is not that AEP-Media proves authenticity. Its value is that it makes the local evidence object explicit and reproducibly checkable, which is a prerequisite for stronger assurance layers. Researchers can use it as a baseline when comparing provenance models, evidence-package formats, adapter boundaries, or future external-verification appendices. The implementation also complements supply-chain and attestation systems such as in-toto and SLSA by focusing on media-bearing operation evidence rather than build provenance alone [10,11].

## 5. Conclusions

AEP-Media is reusable research software for offline validation of time-aware media evidence bundles. It combines a small profile, schemas, examples, command-line validators, bundle verification, strict declared time-trace validation, adapter-only ingestion, reproducible evaluation matrices, and release packaging material.

The current claim is local validation and fixture-based adapter ingestion. AEP-Media detects inconsistencies inside a declared evidence package, but it does not establish that the original media capture event was truthful, authorized, or unmodified before packaging. It does not provide legal admissibility, non-repudiation, trusted timestamping, real PTP proof, full MP4 PRFT parsing, real C2PA signature verification, chain of custody, production deployment, or broad forensic sufficiency.

Future work should keep the local profile semantics stable while adding environment-specific evidence appendices: LinuxPTP traces captured on equipped Linux hosts, ffprobe output from PRFT-bearing media, C2PA CLI reports for real signed assets, and independent reproduction of the evaluation matrix.

## Data availability

The software, selected examples, schemas, reports, and release materials are available in the public GitHub repository at `https://github.com/joy7758/agent-evidence` and in the Zenodo archive for AEP-Media v0.1.0 at `https://doi.org/10.5281/zenodo.20107097`. The supplementary package accompanying this submission contains selected schemas, examples, reproducibility commands, evaluation summaries, and claim-boundary documentation.

## CRediT authorship contribution statement

Bin Zhang: Conceptualization, Methodology, Software, Validation, Investigation, Data curation, Writing - original draft, Writing - review and editing, Project administration.

## Declaration of competing interest

The author declares no known competing financial interests or personal relationships that could have appeared to influence the work reported in this article.

## Funding

No specific funding was received for this work.

## Declaration of generative AI and AI-assisted technologies in the manuscript preparation process

During the preparation of this work, the author used OpenAI ChatGPT/Codex for manuscript organization, implementation scaffolding, command generation, and wording refinement. After using these tools, the author reviewed and edited the content as needed and takes full responsibility for the content of the submitted article.

## References

[1] W3C. PROV Overview. World Wide Web Consortium. <https://www.w3.org/TR/prov-overview/>; 2013 [accessed 10 May 2026].

[2] W3C. PROV-DM: The PROV Data Model. World Wide Web Consortium. <https://www.w3.org/TR/prov-dm/>; 2013 [accessed 10 May 2026].

[3] Coalition for Content Provenance and Authenticity. C2PA Technical Specification. <https://c2pa.org/specifications/>; 2024 [accessed 10 May 2026].

[4] FFmpeg Project. ffprobe Documentation. <https://ffmpeg.org/ffprobe.html>; 2026 [accessed 10 May 2026].

[5] LinuxPTP Project. ptp4l and phc2sys Documentation. <https://linuxptp.sourceforge.net/>; 2026 [accessed 10 May 2026].

[6] GStreamer Project. GstPtpClock Documentation. <https://gstreamer.freedesktop.org/documentation/net/gstptpclock.html>; 2026 [accessed 10 May 2026].

[7] JSON Schema. JSON Schema Core and Validation Specifications. <https://json-schema.org/specification>; 2026 [accessed 10 May 2026].

[8] Association for Computing Machinery. Artifact Review and Badging. <https://www.acm.org/publications/policies/artifact-review-and-badging-current>; 2026 [accessed 10 May 2026].

[9] Zhang B. AEP-Media v0.1.0: Offline Validation of Time-Aware Media Evidence Bundles [software]. Zenodo; 2026. <https://doi.org/10.5281/zenodo.20107097>.

[10] in-toto Project. in-toto: Providing farm-to-table guarantees for bits and bytes. <https://in-toto.io/>; 2026 [accessed 10 May 2026].

[11] Supply-chain Levels for Software Artifacts. SLSA Provenance. <https://slsa.dev/spec/v1.0/provenance>; 2026 [accessed 10 May 2026].
