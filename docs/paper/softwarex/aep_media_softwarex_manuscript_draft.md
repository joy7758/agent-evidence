# AEP-Media: Reusable Research Software for Offline Validation of Time-Aware Media Evidence Bundles

## Authors

Bin Zhang

## Abstract

AEP-Media is reusable research software for representing a media-bearing operation as a locally checkable evidence bundle. It provides a minimal media evidence profile, JSON schemas, controlled examples, profile-aware validators, an offline bundle builder and verifier, strict declared time-trace validation, adapter-only ingestion interfaces, demos, tests, and release/evaluation reports. The software targets researchers who need reproducible validation artifacts for operation accountability, media evidence packaging, provenance boundaries, and time-aware evidence review. AEP-Media recomputes media hashes, checks required fields, enforces reference closure across operation, policy, provenance, media, evidence, and validation objects, rejects unsafe bundle paths, validates declared clock-trace artifacts, and reports machine-readable failure codes. Its evaluation package covers valid, invalid, and tamper cases with expected pass/fail behavior, including default, adapter-inclusive, optional-tool reporting, and combined evaluation matrices. The current claim is local validation and fixture-based adapter ingestion. AEP-Media does not claim legal admissibility, non-repudiation, trusted timestamping, real PTP proof, a full MP4 PRFT parser, real C2PA signature verification, chain of custody, or production deployment.

## Keywords

media evidence; operation accountability; research software; provenance; offline validation; evidence bundle; time trace; reproducibility; artifact evaluation

## Software Availability

- Software name: AEP-Media, implemented within `agent-evidence`.
- Repository: https://github.com/joy7758/agent-evidence
- Primary package: `agent_evidence`
- Programming language: Python.
- License: Apache-2.0.
- Repository DOI: `10.5281/zenodo.19334062`.
- AEP-Media-specific archive DOI: action required before SoftwareX submission unless the repository DOI is explicitly used for this release.

## Statement of Need

Researchers studying media-bearing operation accountability often work with disconnected artifacts: media files, logs, policy references, provenance declarations, timing metadata, and validation notes. These artifacts are difficult to inspect consistently when they are not bound into a single evidence object with explicit validation semantics. AEP-Media provides a small reusable software layer for turning those materials into locally checkable evidence bundles with diagnosable failure codes.

The software is useful when the research question is not whether a media event is legally admissible or externally trusted, but whether a declared local evidence package is internally consistent, portable, reproducible, and reviewable. This makes AEP-Media appropriate for research on operation accountability, evidence packaging, provenance boundaries, and validation-oriented artifact design.

## Software Description

AEP-Media extends the `agent-evidence` package with a media-focused profile and validation path. The core profile binds an actor, subject, operation, policy, constraints, time context, media artifacts, provenance references, evidence notes, and validation expectations into one statement. The validator checks profile identity, required fields, reference closure, media hash recomputation, declared time context completeness, and primary media time binding.

The offline bundle layer copies artifacts into a bundle-local structure, rewrites artifact paths, recomputes sizes and hashes, generates checksums, and verifies the package without relying on the original runtime environment. The bundle verifier rejects unsafe paths, path traversal, missing artifacts, checksum mismatches, and profile validation failures.

The strict-time layer adds declared clock-trace validation. It checks clock-trace references, clock-trace artifact hashes, trace profile identity, collection window coverage, sample validity, summary recomputation, offset thresholds, jitter thresholds, and primary media binding to the declared time context.

The adapter layer is intentionally ingestion-only. It normalizes LinuxPTP-style logs, FFmpeg PRFT-style metadata, and C2PA-like manifest metadata from fixtures or optional external-tool outputs. Adapter reports distinguish ingestion from external verification and preserve the local-validation claim boundary.

## Architecture and Main Components

Component | Role
--- | ---
`agent_evidence/media_profile.py` | Media profile validation and machine-readable issue reporting.
`agent_evidence/media_bundle.py` | Offline bundle build and verify functions.
`agent_evidence/media_time.py` | Strict declared time-trace validation.
`agent_evidence/adapters/linuxptp.py` | LinuxPTP-style log ingestion into AEP-Media time traces.
`agent_evidence/adapters/ffmpeg_prft.py` | ffprobe/PRFT-style timing metadata ingestion.
`agent_evidence/adapters/c2pa_manifest.py` | C2PA-like manifest metadata ingestion.
`agent_evidence/media_evaluation.py` | Evaluation matrix generation for default profile, bundle, and time cases.
`agent_evidence/media_adapter_evaluation.py` | Adapter-inclusive evaluation cases.
`agent_evidence/media_optional_tools.py` | Optional external-tool availability and reporting path.
`agent_evidence/media_release_pack.py` | Release pack assembly for research artifact review.
`spec/` and `schema/` | Profile, bundle, time trace, and adapter report specifications.
`examples/media/` | Valid, invalid, fixture, adapter, and strict-time examples.
`demo/` | Executable demonstrations for profile, bundle, time, adapter, evaluation, and release paths.

## Functionality

The main command-line entry points are:

```bash
agent-evidence validate-media-profile examples/media/minimal-valid-media-evidence.json
agent-evidence build-media-bundle examples/media/minimal-valid-media-evidence.json --out /tmp/aep-media-bundle-check
agent-evidence verify-media-bundle /tmp/aep-media-bundle-check
agent-evidence validate-media-time-profile examples/media/time/minimal-valid-time-aware-media-evidence.json
agent-evidence verify-media-bundle /tmp/aep-media-time-bundle-check --strict-time
agent-evidence run-media-evaluation --out demo/output/media_evaluation_demo
agent-evidence run-media-evaluation --out demo/output/media_evaluation_with_adapters --include-adapters
agent-evidence run-media-evaluation --out demo/output/media_evaluation_with_tools --include-optional-tools
```

The software also includes demos for evidence statement generation, bundle construction, strict-time validation, adapter-backed statements, evaluation packs, and release packs. The examples include controlled invalid cases that intentionally break one rule at a time, such as missing time context, broken media hash, unresolved policy reference, missing clock trace reference, exceeded clock offset threshold, and clock window mismatch.

## Reproducibility and Evaluation

AEP-Media is evaluated as a profile-and-validator research artifact. The evaluation target is conformance, diagnosability, and reproducibility rather than performance benchmarking or field deployment. Existing reports record:

- default evaluation: 18 cases, `unexpected=0`;
- adapter-inclusive evaluation: 26 cases, `unexpected=0`;
- optional-tool reporting evaluation: 23 cases, `unexpected=0`;
- combined adapter and optional-tool evaluation: 31 cases, `unexpected=0` from prior release materials and should be rerun before submission.

The evaluation includes valid cases, controlled invalid examples, bundle tamper cases, strict-time failures, adapter ingestion failures, and optional-tool reporting cases. The fixture path does not require LinuxPTP, FFmpeg, ffprobe, or C2PA tools to be installed.

## Impact

AEP-Media provides a reusable validation boundary for researchers who need to package and inspect media-bearing operation evidence. It can support:

- reproducible evidence-package experiments;
- media provenance boundary studies;
- operation-accountability prototypes;
- local validation of declared evidence bundles;
- controlled tamper and failure-code studies;
- integration experiments with external-tool-style metadata without requiring those tools for baseline reproduction.

The main impact is not that AEP-Media proves external authenticity. Its value is that it makes the local evidence object explicit, portable, and reproducibly checkable before stronger external assurance mechanisms are added.

## Limitations and Claim Boundary

AEP-Media detects inconsistencies within a declared evidence package. It does not establish that the original media capture event was truthful, authorized, or unmodified before packaging. It does not provide legal admissibility, non-repudiation, trusted timestamping, real PTP proof, a full MP4 PRFT parser, real C2PA signature verification, chain of custody, production deployment, or broad forensic sufficiency.

Optional external-tool paths are reporting and smoke-integration paths. The reproducible baseline remains local validation and fixture-based adapter ingestion.

## Future Work

Future work should keep the local profile semantics stable while adding environment-specific appendices:

- LinuxPTP log collection on a Linux host with appropriate PTP hardware;
- ffprobe runs on PRFT-bearing media assets;
- C2PA CLI verification on real signed assets;
- archived AEP-Media-specific release DOI;
- independent reproduction of the evaluation matrix.

## Acknowledgment and AI-assisted Writing Disclosure

The author used OpenAI ChatGPT/Codex as AI-assisted tools for manuscript organization, implementation scaffolding, command generation, and wording refinement. The tools were not used as autonomous authors. The author reviewed, edited, verified, and is responsible for all manuscript content, claims, code, artifacts, citations, and conclusions.

## References

1. AEP-Media specifications and release reports in the `agent-evidence` repository.
2. SoftwareX Guide for Authors, Elsevier.
3. Journal of Open Source Software submission documentation.
4. Forensic Science International: Digital Investigation aims and scope.
