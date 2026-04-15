# Third-Party Checker Handoff

This directory is a third-party-checker handoff surface for the B1 line.

Its purpose is narrow: let an external checker implementation or an external reviewer
reuse the current canonical B1 package surface and the current supplementary surfaces
for independent re-checking.

There is still no external third-party checker result included.

Canonical B1 remains:

- `Execution Evidence and Operation Accountability Profile v0.1`
- `1 valid / 3 invalid / 1 demo`

Supplementary surfaces remain supplementary:

- `../external_context/`
- `../second_checker/`

They support reviewer-facing inspection and future re-checking, but they do not rewrite
canonical B1 counts.

This handoff surface points to:

- `checker_input_manifest.json` for canonical and supplementary inputs
- `checker_contract.md` for the minimum expected re-checking contract

This directory does not contain an external checker implementation result. It is a
handoff surface for future independent re-checking only.
