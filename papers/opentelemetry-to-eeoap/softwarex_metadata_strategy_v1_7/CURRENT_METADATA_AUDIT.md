# Current Metadata Audit

## Root `CITATION.cff` Status

- Exists? yes
- Current scope: AEP-Media software release.
- Current title: `AEP-Media: Reusable Research Software for Offline Validation
  of Time-Aware Media Evidence Bundles`
- Current version: `aep-media-v0.1.0`
- Current DOI: `10.5281/zenodo.20107097`
- Problem for OpenTelemetry-to-EEOAP route: it identifies the AEP-Media
  software object, not the OpenTelemetry-to-EEOAP adapter package.
- Safe action: do not overwrite root `CITATION.cff` until the release scope is
  decided. Prepare OpenTelemetry-to-EEOAP-specific metadata separately first.

## Root `codemeta.json` Status

- Exists? yes
- Current scope: AEP-Media software source code.
- Current software name: `AEP-Media`
- Current identifier: `https://doi.org/10.5281/zenodo.20107097`
- Current release URL: AEP-Media GitHub release.
- Problem for OpenTelemetry-to-EEOAP route: it would misidentify
  OpenTelemetry-to-EEOAP as AEP-Media if reused for the SoftwareX route.
- Safe action: do not overwrite root `codemeta.json` in this strategy step.
  Prepare a focused OpenTelemetry-to-EEOAP codemeta draft under the paper
  package first.

## `pyproject.toml` Status

- Exists? yes
- Current scope: Python package metadata for `agent-evidence`.
- Current project name: `agent-evidence`
- Current version: `0.2.0`
- Helpful for OpenTelemetry-to-EEOAP? partial.
- Problem for OpenTelemetry-to-EEOAP route: it provides package-level
  installation and dependency information, but it does not define
  OpenTelemetry-to-EEOAP as a release-level software object.
- Safe action: use `pyproject.toml` as supporting package metadata only. Do not
  treat it as the SoftwareX-specific metadata record.

## `README.md` Status

- Exists? yes
- Current scope: broad `agent-evidence` repository overview, EEOAP demo, and
  AEP-Media release information.
- Problem for OpenTelemetry-to-EEOAP route: the root README currently does not
  clearly point to the OpenTelemetry-to-EEOAP adapter path or SoftwareX package
  materials.
- Safe action: do not edit README in this task. Later, after release scope is
  fixed, add a small pointer to the OpenTelemetry-to-EEOAP adapter and package
  materials if needed.

## `LICENSE` Status

- Exists? yes
- Current scope: repository-level Apache-2.0 license.
- Problem for OpenTelemetry-to-EEOAP route: no direct problem. SoftwareX may
  expect a clearly discoverable license, and some earlier route notes mentioned
  `LICENSE.txt`; the repository currently uses `LICENSE`.
- Safe action: cite the repository-level Apache-2.0 license in future
  OpenTelemetry-to-EEOAP metadata. Do not duplicate or rename the license in
  this task.

## Local Tag Metadata Status

- `eeoap-v0.1-artifact`
  - Exists locally? yes
  - Tag object: `f4270a575517f987dcd45d8ef80a7d30d808f39f`
  - Target commit: `96f444b7ed39b39fe9f47e428af835952e843cb0`
  - Pushed? no
- `aep-v0.1-artifact`
  - Exists locally? yes
  - Tag object: `a58aa33501252b26acde085fed3dfa0104e255a0`
  - Target commit: `af2b90c14587718a8ed6982131ba9c98e3274054`
  - Pushed? no

Problem for OpenTelemetry-to-EEOAP route: these tags are useful local anchors
for EEOAP and AEP references, but they are not public release identifiers until
pushed or archived.

Safe action: keep them local for now. Do not push tags until release scope and
metadata are aligned.

## SoftwareX Metadata Implication

The current repository contains valid metadata, but it is not valid metadata for
the OpenTelemetry-to-EEOAP SoftwareX object. Reusing it would confuse the paper
route by naming AEP-Media as the cited software. The safest next step is to keep
root metadata unchanged and create OpenTelemetry-to-EEOAP-specific metadata
drafts under `papers/opentelemetry-to-eeoap/`.
