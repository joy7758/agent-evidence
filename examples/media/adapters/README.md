# AEP-Media Adapter Fixtures

These fixtures support adapter-only ingestion tests and examples for AEP-Media.

## Adapter Families

- LinuxPTP-style logs: `linuxptp/`
- FFmpeg PRFT-style metadata: `ffmpeg/`
- C2PA-like manifest metadata: `c2pa/`

For the detailed boundary, see
[docs/aep-media/adapter-boundaries.md](../../../docs/aep-media/adapter-boundaries.md).

## Commands

```bash
agent-evidence ingest-linuxptp-trace --help
agent-evidence ingest-ffmpeg-prft --help
agent-evidence ingest-c2pa-manifest --help
```

## Boundary

The adapters parse local fixtures into AEP-Media reports. They do not claim real
PTP proof, full MP4 PRFT parsing, real C2PA signature verification, legal
admissibility, chain of custody, or production deployment.
