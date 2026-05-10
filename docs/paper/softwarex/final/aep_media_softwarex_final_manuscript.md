# AEP-Media: Reusable Research Software for Offline Validation of Time-Aware Media Evidence Bundles

## Authors

Bin Zhang

## Abstract

AEP-Media is reusable research software for representing a media-bearing operation as a locally checkable evidence bundle. It provides a minimal time-aware media evidence profile, JSON schemas, controlled examples, validators, command-line tools, offline bundle build and verification, strict declared time-trace validation, adapter-only ingestion interfaces, evaluation matrices, and release packaging reports. The software is intended for researchers studying operation accountability, media evidence packaging, provenance boundaries, and reproducible validation artifacts. AEP-Media checks profile identity, required fields, reference closure, artifact hashes, path safety, bundle checksums, declared clock-trace coverage, clock-trace summaries, and offset/jitter thresholds. Its evaluation materials exercise valid, invalid, tamper, adapter-ingestion, and optional-tool reporting cases with expected pass/fail behavior. The current claim is local validation and fixture-based adapter ingestion. AEP-Media does not claim legal admissibility, non-repudiation, trusted timestamping, real PTP proof, full MP4 PRFT parsing, real C2PA signature verification, chain of custody, or production deployment.

## Keywords

media evidence; operation accountability; research software; provenance; offline validation; evidence bundle; time trace

## Software Availability

- Software name: AEP-Media, within `agent-evidence`
- Repository: `https://github.com/joy7758/agent-evidence`
- License: Apache-2.0
- Primary package: `agent_evidence`
- Programming language: Python
- Documentation: `spec/`, `schema/`, `examples/media/`, `demo/`, and `docs/reports/`
- Tests: media profile, bundle, strict-time, adapter, evaluation, and release-pack tests under `tests/`
- Archive: AEP-Media-specific archive DOI pending release archive; action required before final submission

## Statement of Need

Researchers working with media-bearing operations often need to review several disconnected artifacts: media files, logs, provenance declarations, timing metadata, policy references, and validation reports. These objects are difficult to inspect consistently when they are not bound into a local evidence object with explicit validation semantics. AEP-Media addresses this gap by providing a reusable software layer for turning such materials into locally checkable evidence bundles with machine-readable failure codes.

The problem is deliberately bounded. AEP-Media is not a legal evidence platform and does not attempt to prove external authenticity. Its purpose is to make the local validation boundary explicit: which fields must be present, which references must close, which files must match declared hashes, which time traces cover a declared window, and which failures are reported when a controlled rule is broken. This local conformance layer is useful before stronger external assurance mechanisms such as signing, trusted timestamping, or deployed capture pipelines are added.

## Software Description

AEP-Media extends the `agent-evidence` package with a media-focused profile and validation path. A media evidence statement binds an actor, subject, operation, policy, constraints, time context, media artifacts, provenance references, evidence notes, and validation expectations into one object. The profile validator checks that the statement is structurally complete and locally consistent.

The offline bundle layer packages a statement and its artifacts into a portable directory. The builder copies artifacts, rewrites paths to bundle-local locations, recomputes hashes and sizes, writes checksums, and emits validation reports. The verifier rejects unsafe paths, missing artifacts, checksum mismatches, and media profile failures. This allows review without relying on the original runtime layout.

The strict-time layer validates declared clock-trace artifacts. It checks trace references, artifact roles, trace hashes, trace profile identity, collection window coverage, sample validity, summary recomputation, offset thresholds, jitter thresholds, and media binding to the declared time context.

The adapter layer is ingestion-only. LinuxPTP-style logs, FFmpeg PRFT-style timing metadata, and C2PA-like manifest metadata can be normalized into AEP-Media reports. Adapter reports distinguish fixture ingestion from optional external-tool reporting and do not imply external verification unless a future environment-specific run records it.

## Architecture and Functionality

The main modules are:

- `agent_evidence/media_profile.py`: media profile validation
- `agent_evidence/media_bundle.py`: offline bundle build and verification
- `agent_evidence/media_time.py`: strict declared time-trace validation
- `agent_evidence/adapters/linuxptp.py`: LinuxPTP-style trace ingestion
- `agent_evidence/adapters/ffmpeg_prft.py`: FFmpeg PRFT-style metadata ingestion
- `agent_evidence/adapters/c2pa_manifest.py`: C2PA-like manifest ingestion
- `agent_evidence/media_evaluation.py`: default evaluation matrix
- `agent_evidence/media_adapter_evaluation.py`: adapter-inclusive evaluation
- `agent_evidence/media_optional_tools.py`: optional external-tool reporting
- `agent_evidence/media_release_pack.py`: release pack assembly

Typical commands are:

```bash
agent-evidence validate-media-profile examples/media/minimal-valid-media-evidence.json
agent-evidence build-media-bundle examples/media/minimal-valid-media-evidence.json --out /tmp/aep-media-bundle-check
agent-evidence verify-media-bundle /tmp/aep-media-bundle-check
agent-evidence validate-media-time-profile examples/media/time/minimal-valid-time-aware-media-evidence.json
agent-evidence run-media-evaluation --out demo/output/media_evaluation_demo
```

The repository includes valid examples, controlled invalid examples, strict-time fixtures, adapter fixtures, and tamper cases. These allow researchers to reproduce the intended pass/fail behavior without installing LinuxPTP, FFmpeg, ffprobe, or C2PA.

## Reproducibility and Evaluation

AEP-Media is evaluated as a conformance-oriented software artifact. The evaluation targets reproducibility, diagnosability, and validation coverage rather than throughput or field deployment. Prior release reports record:

- default evaluation: 18 cases, `unexpected=0`;
- adapter-inclusive evaluation: 26 cases, `unexpected=0`;
- optional-tool reporting evaluation: 23 cases, `unexpected=0`;
- combined adapter and optional-tool evaluation: 31 cases, `unexpected=0`.

The case categories include valid conformance cases, invalid single-rule cases, bundle tamper cases, strict-time failures, adapter-ingestion cases, and optional-tool reporting cases. Expected failures include missing time context, media hash mismatch, unresolved policy reference, bundle checksum mismatch, path escape, missing clock-trace reference, clock offset threshold exceedance, clock window mismatch, missing PRFT metadata, and declared invalid C2PA-like signature status.

## Impact

AEP-Media supports research on operation accountability, media evidence packaging, provenance boundaries, and reproducible validation artifacts. It gives researchers a concrete software artifact for asking whether a declared media evidence package is internally consistent and portable. The software may also serve as a baseline for future work that adds real external tool runs, signed manifests, trusted timestamps, or deployed capture pipelines.

The impact is not that AEP-Media proves authenticity. Its value is that it makes the local evidence object explicit and reproducibly checkable, which is a prerequisite for stronger assurance layers.

## Limitations and Claim Boundary

AEP-Media detects inconsistencies inside a declared evidence package. It does not establish that the original media capture event was truthful, authorized, or unmodified before packaging. It does not provide legal admissibility, non-repudiation, trusted timestamping, real PTP proof, full MP4 PRFT parsing, real C2PA signature verification, chain of custody, production deployment, or broad forensic sufficiency.

Optional external-tool paths are reporting paths. The reproducible baseline remains local validation and fixture-based adapter ingestion.

## Future Work

Future work should keep the local profile semantics stable while adding environment-specific evidence appendices: LinuxPTP traces captured on equipped Linux hosts, ffprobe output from PRFT-bearing media, C2PA CLI reports for real signed assets, independent reproduction of the evaluation matrix, and an AEP-Media-specific archived release DOI.

## Declaration of Generative AI and AI-assisted Technologies in the Manuscript Preparation Process

During the preparation of this work, the author used OpenAI ChatGPT/Codex for manuscript organization, implementation scaffolding, command generation, and wording refinement. After using these tools, the author reviewed and edited the content as needed and takes full responsibility for the content of the submitted article.

## References

[1] W3C, "PROV Overview," World Wide Web Consortium.

[2] W3C, "PROV-DM: The PROV Data Model," World Wide Web Consortium.

[3] Coalition for Content Provenance and Authenticity, "C2PA Technical Specification."

[4] FFmpeg Project, "ffprobe Documentation."

[5] LinuxPTP Project, "ptp4l and phc2sys Documentation."

[6] GStreamer Project, "GstPtpClock Documentation."

[7] JSON Schema, "JSON Schema Core and Validation Specifications."

[8] Association for Computing Machinery, "Artifact Review and Badging."

[9] in-toto Project, "in-toto: Providing farm-to-table guarantees for bits and bytes."

[10] Supply-chain Levels for Software Artifacts, "SLSA Provenance."

[11] R. Kahn and R. Wilensky, "A Framework for Distributed Digital Object Services."

[12] DONA Foundation, "Digital Object Interface Protocol Specification."
