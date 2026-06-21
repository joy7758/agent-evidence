# SoftwareX Environment Boundary

Affected clauses: EEOAP-001, EEOAP-002, EEOAP-003, EEOAP-004, EEOAP-005.

This file records the local execution boundary for the SoftwareX v2 artifact
package.

## Project Metadata

- Project requires Python `>=3.11` in `pyproject.toml`.
- Runtime dependencies are declared in `pyproject.toml`.
- The reproducibility script uses the local `.venv` when available.
- The package contains the local Python source tree and the test targets used
  by `scripts/reproduce_paper.sh`.
- No network access is required when the declared Python dependencies are
  already installed in the local environment.

## Verified Local Environment

The final local package was checked with:

- Python: `3.14.5`
- `agent-evidence`: editable local project, package metadata version `0.1.0rc3`
- `pytest`: `9.0.2`
- `jsonschema`: `4.26.0`
- `pydantic`: `2.12.5`
- `click`: `8.3.1`

## Boundary

The reproducibility claim is scoped to local execution of the bundled
repository snapshot and support material.

It is not a claim of universal byte-identical behavior across arbitrary
operating systems, Python builds, locale settings, or filesystem layouts.

The determinism oracle in `experiments/exp4_determinism_oracle.py` compares
canonicalized evidence content and validator outcome status. It intentionally
excludes environment-specific locator strings from semantic equivalence.
