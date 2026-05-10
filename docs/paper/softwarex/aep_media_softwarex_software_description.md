# AEP-Media Software Description

## Overview

AEP-Media is implemented inside the `agent-evidence` Python package. It adds a media-evidence validation path on top of the repository's broader operation-accountability work.

## Profile Validator

The profile validator checks a media evidence statement for:

- profile identity;
- required fields;
- operation, policy, provenance, media, evidence, and validation reference closure;
- media artifact hash recomputation;
- declared time-context completeness;
- primary media time-context binding;
- machine-readable issue reporting.

Example:

```bash
agent-evidence validate-media-profile examples/media/minimal-valid-media-evidence.json
```

## Bundle Builder and Verifier

The bundle builder copies referenced artifacts into a bundle-local structure, rewrites artifact paths, recomputes hashes and sizes, writes checksums, and emits validation reports. The verifier checks path safety, checksums, artifact presence, and profile validity.

Examples:

```bash
agent-evidence build-media-bundle examples/media/minimal-valid-media-evidence.json --out /tmp/aep-media-bundle-check
agent-evidence verify-media-bundle /tmp/aep-media-bundle-check
```

## Strict-time Trace Validator

The strict-time validator adds required declared clock-trace checks. It verifies clock-trace references, artifact role, trace profile, hash, collection window coverage, sample validity, summary recomputation, offset thresholds, jitter thresholds, and media time-context binding.

Example:

```bash
agent-evidence validate-media-time-profile examples/media/time/minimal-valid-time-aware-media-evidence.json
```

## Adapter-only Ingestion

AEP-Media includes ingestion adapters for external-tool-style outputs:

- LinuxPTP-style `ptp4l` and `phc2sys` logs;
- FFmpeg/ffprobe PRFT-style timing metadata;
- C2PA-like manifest metadata.

These adapters normalize input fixtures or optional tool outputs into AEP-Media metadata. They do not claim real external verification by default.

Examples:

```bash
agent-evidence ingest-linuxptp-trace examples/media/adapters/linuxptp/ptp4l-sample.log --out /tmp/aep-linuxptp-clock-trace.json
agent-evidence ingest-ffmpeg-prft examples/media/adapters/ffmpeg/ffprobe-prft-sample.json --out /tmp/aep-ffmpeg-prft-metadata.json
agent-evidence ingest-c2pa-manifest examples/media/adapters/c2pa/c2pa-manifest-valid-like.json --out /tmp/aep-c2pa-manifest-metadata.json
```

## Evaluation Runner

The evaluation runner generates matrices for default, adapter-inclusive, and optional-tool cases.

Examples:

```bash
agent-evidence run-media-evaluation --out demo/output/media_evaluation_demo
agent-evidence run-media-evaluation --out demo/output/media_evaluation_with_adapters --include-adapters
agent-evidence run-media-evaluation --out demo/output/media_evaluation_with_tools --include-optional-tools
```

## Release and Submission Pack Builders

The release and submission pack builders assemble reproducibility materials, claim boundaries, artifact inventories, evaluation summaries, checksums, and paper scaffolds. For SoftwareX, these builders should be treated as packaging aids rather than the core scientific claim.

## Examples and Fixtures

The repository includes:

- a valid minimal media evidence statement;
- invalid examples for missing time context, broken media hash, and unresolved policy reference;
- strict-time valid and invalid examples;
- bundle tamper cases;
- LinuxPTP-style, ffprobe-style, and C2PA-like adapter fixtures.

## Controlled Tamper Matrix

The tamper matrix demonstrates that offline bundle verification and strict-time checks fail with explicit codes when artifacts, statements, policy references, clock traces, or time windows are intentionally altered.
