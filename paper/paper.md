---
title: "AEP-Media: Local Validation of Time-Aware Media Evidence Bundles"
tags:
  - Python
  - digital evidence
  - media provenance
  - validation
  - reproducible research
authors:
  - name: Bin Zhang
    orcid: 0009-0002-8861-1481
    affiliation: 1
affiliations:
  - name: Independent Researcher, China
    index: 1
date: 2026-06-01
bibliography: paper.bib
---

# Summary

AEP-Media is an open-source Python software path within `agent-evidence` for
local validation of time-aware media evidence bundles. It provides JSON schemas,
command-line validators, examples, mobile-video-style fixtures, offline bundle
build and verification, strict declared time-trace validation, adapter-only
ingestion, tests, reproducibility reports, and a release archive
[@aepmedia_zenodo_2026].

A media evidence bundle is a review package for one media-related operation. It
contains a media artifact or media reference, operation and policy context,
provenance references, declared timing evidence, file hashes, bundle checksums,
adapter reports, and validation output. AEP-Media helps researchers and
reviewers check local package consistency. It does not prove that a real-world
capture event was truthful, authorized, or externally authenticated.

# Statement of need

Researchers studying media evidence packaging, provenance boundaries, and
operation accountability need a small reproducible baseline for checking whether
a declared media evidence package is internally complete. AEP-Media targets the
stage before external assurance layers are introduced: it checks whether the
local package is referenced, hash-consistent, time-bounded, and diagnosable.

# State of the field

Existing adjacent tools and standards cover different layers. JSON Schema
defines structural validation vocabulary [@jsonschema_core_2022;
@jsonschema_validation_2022], PROV describes provenance relationships
[@prov_overview_2013], C2PA defines a content provenance ecosystem
[@c2pa_spec], FFmpeg/ffprobe exposes media metadata [@ffprobe_docs], and
LinuxPTP exposes clock-synchronization log surfaces [@linuxptp_docs]. Forensic
containers such as AFF4 and EWF/E01 focus on forensic acquisition and storage
objects [@loc_aff4; @loc_ewf].

AEP-Media does not replace these tools. It provides a local validation layer
that binds media references, policy, provenance, declared timing, hashes,
adapter reports, bundle safety, and explicit failure codes into a reusable
research-software artifact.

# Software design

AEP-Media is designed as a small command-line workflow rather than a hosted
service. Validators, bundle builders, adapter ingesters, examples, and tests are
kept in the same repository so reviewers can run the full local path without
external accounts or specialized media tools. The adapter layer is intentionally
fixture-based: it normalizes declared LinuxPTP-style, ffprobe/PRFT-style, and
C2PA-like metadata into local reports while preserving the boundary that those
external systems have not been independently verified by AEP-Media.

The main design trade-off is explicitness over automation. AEP-Media requires
statements to declare artifacts, references, hashes, time context, and expected
validation behavior instead of inferring them from a live capture system. This
makes the examples small enough for review, keeps failure modes inspectable, and
lets downstream users replace fixtures with stronger external evidence layers
without changing the local validation contract.

# Functionality

The current callable surface includes:

- `validate-media-profile` for validating AEP-Media statements;
- `build-media-bundle` and `verify-media-bundle` for offline bundle creation and
  verification;
- `validate-media-time-profile` for strict declared time-trace validation;
- `ingest-linuxptp-trace`, `ingest-ffmpeg-prft`, and `ingest-c2pa-manifest` for
  fixture-based/local adapter ingestion;
- `run-media-evaluation` for bounded evaluation matrices;
- `build-aep-media-release-pack` for release evidence packaging.

The repository includes a mobile-video-style fixture with network timing logs,
ffprobe-style metadata, and a provenance sidecar. The fixture is intentionally
small and reproducible; it is not a real mobile deployment or production
forensic corpus.

The repository also includes a mobile-video-style walkthrough and
adapter-boundary documentation to support reviewer reproduction.

This combination is intended to support repeatable review tasks: check that a
media artifact hash matches the statement, verify that referenced sidecars are
present, confirm that declared time traces cover the media window, and observe
controlled failures for common package errors. The result is a reusable
validation harness rather than a single-purpose analysis script.

# Availability and reproducibility

The software is available under Apache-2.0 at
<https://github.com/joy7758/agent-evidence>. The AEP-Media v0.1.0 release is
archived with DOI <https://doi.org/10.5281/zenodo.20107097>.

Typical local commands are:

```bash
python -m pip install -e ".[dev]"
agent-evidence validate-media-profile examples/media/minimal-valid-media-evidence.json
agent-evidence validate-media-time-profile examples/media/time/minimal-valid-time-aware-media-evidence.json
agent-evidence run-media-evaluation --out /tmp/aep-media-evaluation
python -m pytest tests/test_media_profile.py tests/test_media_bundle.py tests/test_media_time.py tests/test_media_adapters.py tests/test_media_evaluation.py -q
```

# Research impact statement

AEP-Media provides a citable, reusable baseline for researchers who need to
construct or review media evidence package fixtures with explicit timing,
provenance, and integrity fields. Its near-term significance is the
reproducible reference material: schemas, examples, mobile-video-style fixtures,
negative cases, tests, evaluation matrices, and a DOI-archived release that can
be rerun by reviewers.

The software is also useful as a comparison point for future work that evaluates
real capture systems, independently documented external assurance components, or
forensic-container integrations. Those layers can be assessed against a stable
local consistency baseline instead of being mixed directly into a larger, less
auditable workflow.

# Claim boundary

AEP-Media supports local validation and fixture-based adapter ingestion. It does
not claim legal admissibility, non-repudiation, chain of custody, trusted
timestamping, real PTP proof, full MP4 PRFT parsing, real C2PA signature
verification, production deployment, or broad forensic sufficiency.

# AI usage disclosure

The author used OpenAI ChatGPT/Codex for manuscript organization, command
generation, implementation-facing drafting support, and wording refinement. The
author reviewed, edited, validated, and is responsible for all content, code,
artifacts, and claims.

# Acknowledgements

No specific funding was received for this work.

# References
