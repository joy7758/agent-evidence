# GitHub build attestation (minimal)

## What this workflow does

The `Build + Attest` workflow builds Python distribution artifacts under `dist/*` with `python -m build`, uploads those files as the GitHub Actions workflow artifact named `python-dist`, and asks GitHub to issue artifact attestations for those exact built files.

This is upstream build provenance only. It gives this repository one minimal GitHub-native proof path for built distribution artifacts.

## What this workflow does not do

- It does not change the AEP schema.
- It does not change `bundle`, `receipt`, or `summary` semantics.
- It does not change CLI behavior, runtime behavior, export logic, or offline verifier semantics.
- It does not add Cosign, OPA, Conftest, container image signing, or a release asset redesign.
- It does not attach built files to GitHub Releases.

## When it runs

- Manually through `workflow_dispatch`
- Automatically when a GitHub release is published

## How to verify a downloaded artifact

Download one built file first, then run:

```bash
gh attestation verify dist/<artifact-file> -R joy7758/agent-evidence
```

`<artifact-file>` should be the local file you want to check, such as a wheel or source distribution downloaded from the `python-dist` workflow artifact or another byte-identical distribution source. This workflow does not publish release assets, so the example assumes you already have the exact built file locally.

## Why this repo uses `actions/attest@v4`

This repository uses `actions/attest@v4` directly because it is the current low-level action for GitHub artifact attestations, and `actions/attest-build-provenance` is now only a thin wrapper around it in v4. Using `actions/attest@v4` keeps the workflow smaller and makes the attested subject path explicit with `subject-path: "dist/*"`.

## GitHub plan limitation

GitHub artifact attestations are supported for public repositories on current GitHub plans. For private or internal repositories, GitHub Enterprise Cloud is required.

## Scope boundary

This workflow is intentionally narrow. It adds upstream build provenance for Python distribution artifacts only. It does not redefine the repository as a broader supply-chain system, and it does not alter the existing AEP, `bundle`, `receipt`, `summary`, CLI, or runtime/export surfaces.
