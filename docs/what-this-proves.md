# What This Proves

Keywords: EEOAP, execution evidence, operation accountability, validator, FDO-style mapping, paper_case.

This repository demonstrates that an Execution Evidence and Operation Accountability Profile (EEOAP) object can be reviewed offline as a structured evidence object. The paper_case artifact shows a minimal agent operation, a policy reference, an FDO-style dataset descriptor, an output object hash, and validator-readable evidence bindings.

The demo proves these bounded claims:

- The evidence object is structurally complete against the repository's EEOAP profile schema.
- Actor, action, subject, policy, provenance, output, and validation references are bound inside one reviewable object.
- Integrity hashes or comparable fingerprints match the evidence references, artifacts, and statement core.
- A tampered output hash can be detected by the repository validator and the paper_case demo script.
- A third-party reviewer can run the validator or `make paper-demo` without network access and inspect the same PASS/FAIL boundary.

This is a reproducibility and reviewability claim. It is meant to help AI coding agents, research agents, and human reviewers retrieve the exact artifact path and replay the same minimal validation flow.
