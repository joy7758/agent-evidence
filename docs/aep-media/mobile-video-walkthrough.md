# Mobile-Video Fixture Walkthrough

This walkthrough shows how to validate the fixture-only mobile-video-style
example with local AEP-Media commands.

## Purpose

The fixture demonstrates how one declared mobile-video-style operation can be
packaged with media, timing, metadata, provenance, hashes, and validation
reports.

## What The Fixture Represents

The example models a small inspection-video workflow. The media file is a tiny
placeholder artifact. The package also includes:

- a declared capture window;
- a network timing trace fixture;
- ffprobe-style metadata;
- a C2PA-like provenance sidecar;
- local hashes and validation expectations.

## What It Does Not Represent

The fixture is not a real mobile deployment. It does not prove external
authenticity, legal admissibility, non-repudiation, chain of custody, trusted
timestamping, real PTP synchronization, full MP4 PRFT parsing, real C2PA
signature verification, or production deployment.

## File Inventory

- `mobile-video-operation-evidence.json`: valid AEP-Media statement.
- `artifacts/mobile_video_placeholder.bin`: tiny placeholder media artifact.
- `artifacts/network_timing_log.json`: declared timing trace fixture.
- `artifacts/ffprobe_metadata.json`: ffprobe-style metadata fixture.
- `artifacts/provenance_sidecar.json`: C2PA-like sidecar fixture.
- `expected/expected-validation-summary.json`: expected high-level outcomes.
- `invalid/invalid-mobile-video-broken-hash.json`: broken media hash case.
- `invalid/invalid-mobile-video-missing-timing-ref.json`: missing clock trace ref case.
- `invalid/invalid-mobile-video-unresolved-provenance-ref.json`: unresolved actor ref case.

## Install

```bash
python -m pip install -e .
```

For local development and tests:

```bash
python -m pip install -e ".[dev]"
```

## Validate The Statement

```bash
agent-evidence validate-media-profile examples/media/use_cases/mobile_video_network_timing/mobile-video-operation-evidence.json
```

Expected outcome:

- `ok` is `true`
- `issue_count` is `0`
- summary is `PASS aep-media-evidence-profile@0.1`

## Build A Bundle

```bash
agent-evidence build-media-bundle examples/media/use_cases/mobile_video_network_timing/mobile-video-operation-evidence.json --out /tmp/aep-media-mobile-video-bundle
```

Expected outcome:

- command prints `PASS aep-media-bundle@0.1 build`
- output directory contains `bundle.json`, `statement.json`, `checksums.txt`,
  `validation-report.json`, `summary.json`, and copied artifacts

If the output directory already exists, remove it first or choose a new path:

```bash
rm -rf /tmp/aep-media-mobile-video-bundle
```

## Verify The Bundle

```bash
agent-evidence verify-media-bundle /tmp/aep-media-mobile-video-bundle
```

Expected outcome:

- `ok` is `true`
- `bundle_checksum_ok` is `true`
- `media_profile_ok` is `true`
- summary is `PASS aep-media-bundle@0.1`

## Verify Strict Declared Time

```bash
agent-evidence verify-media-bundle /tmp/aep-media-mobile-video-bundle --strict-time
```

Expected outcome:

- `ok` is `true`
- `strict_time` is `true`
- `time_profile_ok` is `true`
- nested time profile summary is `PASS aep-media-time-evidence@0.1`

## Controlled Negative Cases

Run profile validation on the broken hash case:

```bash
agent-evidence validate-media-profile examples/media/use_cases/mobile_video_network_timing/invalid/invalid-mobile-video-broken-hash.json
```

Expected issue code:

- `media_hash_mismatch`

Run strict-time validation on the missing clock-trace case after bundling it:

```bash
agent-evidence build-media-bundle examples/media/use_cases/mobile_video_network_timing/invalid/invalid-mobile-video-missing-timing-ref.json --out /tmp/aep-media-mobile-video-missing-clock
agent-evidence verify-media-bundle /tmp/aep-media-mobile-video-missing-clock --strict-time
```

Expected issue code:

- `missing_clock_trace_ref`

Run profile validation on the unresolved actor case:

```bash
agent-evidence validate-media-profile examples/media/use_cases/mobile_video_network_timing/invalid/invalid-mobile-video-unresolved-provenance-ref.json
```

Expected issue code:

- `unresolved_actor_ref`

## Troubleshooting

`agent-evidence: command not found`

: Install the package in the active environment with `python -m pip install -e .`
  or run commands through `./.venv/bin/agent-evidence`.

Fixture path errors

: Run commands from the repository root so the relative fixture paths resolve.

Optional tools not installed

: This walkthrough does not require LinuxPTP, FFmpeg, or C2PA binaries. Adapter
  commands work on local fixtures.

Output directory already exists

: Remove the directory or choose a new `--out` path.
