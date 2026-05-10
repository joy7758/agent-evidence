# AEP-Media Final Artifact Inventory

The release pack writes a machine-readable `artifact-inventory.json` with SHA-256 and size metadata for the v0.1 research artifact.

Category | Included surfaces
--- | ---
profiles/specs | media profile, bundle, time trace, adapter specs
schemas | media profile, bundle, time trace, adapter report schemas
examples | valid, invalid, time-aware, bundle, adapter, and optional-tool fixtures
fixtures | demo media, C2PA placeholders, time traces, LinuxPTP-style logs, ffprobe-style JSON, C2PA-like manifests
validators | media profile, bundle, strict time, evaluation, optional tools, release pack modules
adapters | LinuxPTP-style, FFmpeg PRFT-style, C2PA-like ingestion modules and adapter evaluation
demos | media, bundle, strict time, evaluation, adapter, and release pack demos
tests | media profile, bundle, strict time, evaluation, adapters, and release pack tests
reports | mission reports, final claim boundary, reproducibility checklist, evaluation summary
paper scaffold | abstract, methods, evaluation, threats, related-work notes, manuscript draft

The release pack excludes the unrelated paper workspace, virtual environments, `.git`, bytecode caches, and historical demo output directories.
