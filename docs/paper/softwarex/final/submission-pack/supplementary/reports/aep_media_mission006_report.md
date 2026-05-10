# AEP-Media Mission 006 Report

## Goal

Mission 006 adds optional external-tool support on top of the Mission 005 adapter-only path. The fixture path remains reproducible and mandatory; real tool probes are optional and environment-dependent.

## Local Tool Probe Results

tool | command | local result
--- | --- | ---
LinuxPTP `ptp4l` | `ptp4l -v` | not installed / not in PATH
LinuxPTP `phc2sys` | `phc2sys -v` | not installed / not in PATH
FFmpeg | `ffmpeg -version` | not installed / not in PATH
ffprobe | `ffprobe -version` | not installed / not in PATH
C2PA CLI | `c2pa --version` | not installed / not in PATH

## Implementation

- Added `agent_evidence/media_optional_tools.py` for optional tool availability probes.
- Extended `agent-evidence run-media-evaluation` with `--include-optional-tools`.
- Kept default `run-media-evaluation` behavior unchanged.
- Kept Mission 005 fixture adapters as the reproducible path.
- Extended FFmpeg and C2PA adapters so explicit external-tool modes can record external probe or verification attempts when tools are available.

## Safety Boundary

`ptp4l -i eth0 -m` and `phc2sys -s /dev/ptp0 -w -m` were not executed on this machine. They can require Linux-specific interfaces, PTP hardware clocks, privileges, and may affect clock discipline. Mission 006 records availability and keeps ingestion through captured logs.

## Verification Results

- `agent-evidence run-media-evaluation --out /tmp/aep-media-evaluation-with-tools --include-optional-tools`
  - `PASS aep-media-evaluation@0.1 cases=23 unexpected=0 optional_tools=included`
- Optional tool summary:
  - `available_count: 0`
  - `skipped_count: 5`
  - `failed_count: 0`
  - `external_verification_performed: false`

## Non-claims

Mission 006 does not prove real PTP synchronization, hardware clock discipline, complete MP4 PRFT parsing, real FFmpeg PRFT proof, real C2PA signature verification, trusted timestamping, external anchoring, non-repudiation, or legal admissibility.

## Minimal Fixes for Real Tool Runs

- Install linuxptp on a Linux host with a real network interface and PTP hardware clock, then capture `ptp4l` or `phc2sys` logs for ingestion.
- Install FFmpeg/ffprobe and provide a real media file containing PRFT metadata.
- Install the C2PA CLI and provide a real C2PA manifest or signed asset for verification.
