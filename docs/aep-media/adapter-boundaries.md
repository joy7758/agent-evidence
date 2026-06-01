# AEP-Media Adapter Boundaries

This document explains the boundary of AEP-Media adapter-only ingestion.

## Purpose

Adapters normalize local fixture data into AEP-Media reports. They help users
exercise validation workflows with LinuxPTP-style traces, FFmpeg PRFT-style
metadata, and C2PA-like manifests without requiring external tools in routine
tests.

Adapters are fixture-based local validation helpers. They do not independently
verify external authenticity, clock synchronization, media container internals,
or signatures.

## Summary Table

| Adapter | Required fields | Optional fields | Unknown-field behavior | Missing-field behavior | Non-claims |
| --- | --- | --- | --- | --- | --- |
| LinuxPTP-style | log lines or fixture records with parseable timing samples | extra log text, source labels, role hints | ignored unless needed for declared output | empty or unparseable input reports explicit adapter issues | no real PTP proof, no trusted timestamping |
| FFmpeg PRFT-style | fixture JSON/text with declared PRFT-like timing metadata when present | stream/container metadata, side data summaries | ignored unless mapped into the local report | missing PRFT-like data is reported, not hidden | no full MP4 PRFT parser, no proof of media authenticity |
| C2PA-like manifest | manifest-like JSON fields declared in fixtures | generator, signature status, assertion summaries | ignored unless mapped into the local report | missing/invalid signature-status-like fields are reported | no real C2PA signature verification |

## LinuxPTP-Style Trace Ingestion

Command:

```bash
agent-evidence ingest-linuxptp-trace --help
```

Example fixtures:

- `examples/media/adapters/linuxptp/ptp4l-sample.log`
- `examples/media/adapters/linuxptp/phc2sys-sample.log`
- `examples/media/adapters/linuxptp/invalid-empty.log`

Supported surface:

- local fixture parsing;
- basic timing samples and summaries;
- explicit report output for unsupported or empty input.

Boundary:

- no claim that a real clock was synchronized;
- no claim that a timing source is trusted;
- no replacement for LinuxPTP operational logs or system-level verification.

## FFmpeg PRFT-Style Metadata Ingestion

Command:

```bash
agent-evidence ingest-ffmpeg-prft --help
```

Example fixtures:

- `examples/media/adapters/ffmpeg/ffprobe-prft-sample.json`
- `examples/media/adapters/ffmpeg/ffprobe-no-prft-sample.json`

Supported surface:

- local ffprobe-style fixture parsing;
- PRFT-like metadata reporting when fixture fields are present;
- explicit reporting when PRFT-like data is missing.

Boundary:

- no full MP4 parser;
- no binary media validation;
- no claim that FFmpeg was run on the original file unless an external report is
  separately documented.

## C2PA-Like Manifest Ingestion

Command:

```bash
agent-evidence ingest-c2pa-manifest --help
```

Example fixtures:

- `examples/media/adapters/c2pa/c2pa-manifest-valid-like.json`
- `examples/media/adapters/c2pa/c2pa-manifest-invalid-signature-like.json`

Supported surface:

- local manifest-like fixture parsing;
- declared generator and signature-status-like fields;
- explicit local reports for valid-like and invalid-signature-like fixtures.

Boundary:

- no real C2PA CLI verification;
- no cryptographic signature verification;
- no external authenticity claim.

## Future Fixture Families

Useful future maintenance tasks include:

- additional LinuxPTP log variants;
- missing PRFT-like metadata cases;
- C2PA-like sidecar variants with unknown fields;
- malformed fixture cases with explicit issue-code expectations.
