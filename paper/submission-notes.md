# EEOAP Submission Notes

## Best-fit Venue Types

- Research software venues that value a runnable artifact, validator, schema, and reproducibility path.
- Short technical report tracks focused on trustworthy AI engineering, software accountability, or AI agent infrastructure.
- Data-space, FAIR Digital Object, or provenance workshops where FDO-style mapping can be discussed without claiming official standard adoption.
- Artifact evaluation or systems-demonstration venues where the central contribution is a minimal profile plus a replayable validation case.

## Positioning

Position the work as artifact/profile work: EEOAP is a minimal execution evidence and operation accountability profile for verifiable AI agent operations. The claim should be that the repository provides a schema, validator, valid case, tampered case, boundary documents, and `make paper-demo` reproducibility path.

The strongest result is the negative case: the tampered output is rejected with `references_digest_mismatch`. This shows integrity-bound execution evidence rather than a passive log or only a JSON formatting exercise.

## Needed Before Formal Submission

- Add a complete related-work section with citations.
- Decide venue and adapt paper length, formatting, references, and artifact packaging to that venue.
- Freeze a paper artifact release after review of the current dirty worktree and unrelated manuscript files.
- Add a stable release tag and DOI only after the paper draft and artifact boundary are reviewed.
- Add a concise artifact appendix that lists exact commands, expected output, Python version, and known warnings.
- Review terminology for FDO-style mapping so the paper never implies official FDO standard adoption.

## Claims Not To Make

- Do not claim semantic correctness of AI outputs.
- Do not claim legal sufficiency of the policy.
- Do not claim perfect runtime security or uncompromised signer identity.
- Do not claim official FDO adoption, certification, or conformance.
- Do not claim ZKP implementation in this version.
- Do not claim production deployment, multi-tenant governance readiness, or complete policy-engine enforcement.
- Do not claim that EEOAP replaces observability, provenance, supply-chain attestation, or data-space policy systems.
