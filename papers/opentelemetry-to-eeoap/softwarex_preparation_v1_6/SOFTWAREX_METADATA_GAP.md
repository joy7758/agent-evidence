# SoftwareX Metadata Gap

## Root `CITATION.cff` Status

Root `CITATION.cff` exists.

Current content describes:

- `AEP-Media: Reusable Research Software for Offline Validation of Time-Aware
  Media Evidence Bundles`
- version `aep-media-v0.1.0`
- DOI `10.5281/zenodo.20107097`
- URL `https://github.com/joy7758/agent-evidence/releases/tag/aep-media-v0.1.0`

It does not describe the OpenTelemetry-to-EEOAP adapter package.

## Root `codemeta.json` Status

Root `codemeta.json` exists.

Current content describes:

- software name `AEP-Media`
- version `aep-media-v0.1.0`
- identifier `https://doi.org/10.5281/zenodo.20107097`
- release notes and download URL for AEP-Media

It does not describe the OpenTelemetry-to-EEOAP adapter package.

## Required Metadata for OpenTelemetry-to-EEOAP

A SoftwareX-ready OpenTelemetry-to-EEOAP package needs metadata that identifies:

- software name;
- version or release tag;
- authorship;
- repository URL;
- license;
- programming language;
- software requirements;
- adapter path;
- fixture and generated output paths;
- availability URL or DOI once public;
- relationship to EEOAP and AEP artifact tags;
- bounded non-claim scope.

## Safe Options

### Option A: Separate Citation Note Under `papers/opentelemetry-to-eeoap/`

Create a paper-local citation and metadata note that describes the package
without changing root metadata. This is safest while route and release scope are
still not final.

### Option B: Update Root Metadata Only After Release Scope Is Decided

Root metadata should not be changed until the repository owner decides whether
the whole repository, AEP-Media, or OpenTelemetry-to-EEOAP is the primary
software object for the next public release.

### Option C: Create Subpackage Metadata If Repository Policy Allows

Create OpenTelemetry-to-EEOAP-specific metadata inside a subdirectory or release
package. This can avoid overwriting AEP-Media metadata, but it should match the
final release structure.

## Recommendation

Resolve metadata strategy before drafting the SoftwareX article. The safest next
step is to prepare a metadata strategy note that chooses between a paper-local
citation note, root metadata update after release-scope decision, or subpackage
metadata. Do not edit root `CITATION.cff` or `codemeta.json` until the software
object and release strategy are fixed.
