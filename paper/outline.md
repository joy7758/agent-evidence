# EEOAP Paper Outline

Keywords: EEOAP, execution evidence, operation accountability, validator, FDO-style mapping, paper_case.

This outline targets a compact 6 to 8 page paper about the Execution Evidence and Operation Accountability Profile.

## 1. Introduction

Introduce the accountability gap in AI agent and service operations. Explain why chat logs, traces, and screenshots are not enough for independent review. Present EEOAP as a minimal evidence object profile for turning an operation into a reviewable artifact.

## 2. Problem Statement

Define the problem: a reviewer needs to know who acted, what object was acted on, which policy was referenced, what output was produced, and whether the evidence was tampered with. State the non-goals: semantic correctness, legal sufficiency, runtime security proof, official FDO adoption, and ZKP implementation.

## 3. EEOAP Profile Design

Describe the profile fields: actor, subject, operation, policy, constraints, provenance, evidence references, artifacts, integrity, and validation. Emphasize reference closure and hash binding as the minimal operation accountability mechanism.

## 4. Validator and Evidence Bundle

Explain the repository validator path, schema validation, reference closure, consistency checks, and integrity recomputation. Use `examples/paper_case/evidence-valid.json` and `examples/paper_case/evidence-invalid-tampered-output.json` as the reproducible core.

## 5. FDO/Data-space Mapping

Map the EEOAP evidence object to FDO-style concepts: persistent identity, typed object metadata, policy reference, provenance, and integrity fingerprint. Make the boundary explicit: this is a discussion-ready FDO-style mapping, not official FDO standard adoption.

## 6. Evaluation

Report a small reproducibility matrix: valid evidence passes, tampered output fails, offline verification passes, and FDO-style mapping is discussion-ready. Include `make paper-demo` as the one-command replay path.

## 7. Limitations

State that EEOAP does not prove semantic correctness, legal policy sufficiency, perfect runtime security, uncompromised signer identity, official FDO adoption, or ZKP privacy support. Explain that ZKP can be layered later for selective disclosure.

## 8. Conclusion

Summarize EEOAP as a minimal, inspectable, offline-verifiable operation evidence profile for AI agent and service accountability. Close with future work: broader adapters, signed manifests, multi-party review, data-space integration, and privacy-preserving extensions.
