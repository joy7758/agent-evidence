# Reviewer Risk Response Map

Status: preparation aid for author review, not text to submit unchanged.

| Reviewer concern | Correct response | Manuscript section that should address it | Code work needed? |
| --- | --- | --- | --- |
| Too small / only one case | Agree on scope. The paper claims a minimal reproducible profile artifact, not broad empirical generality. More cases are future work. | 2, 6, 9 | No new code needed for journal-preparation draft. |
| Not official FDO standard | Correct. The paper says FDO-style mapping for discussion only, with no adoption, conformance, certification, or endorsement claim. | 5, 7, 9, 12 | No new code needed. |
| Not production-ready | Correct. The artifact is a scoped paper case and validator path, not a production service or deployment package. | 2, 9, 12 | No new code needed. |
| Not semantic correctness | Correct. The validator checks structure, references, policy/evidence linkage, and integrity binding, not truth of the AI output. | 2, 6, 9 | No new code needed. |
| Not full cryptographic trust fabric | Correct. Current artifact uses inspectable JSON evidence and integrity bindings; signatures, timestamps, and transparency are future layers. | 4, 8, 9, 10 | No new code needed. |
| Not ZKP implementation | Correct. ZKP (Zero-Knowledge Proof, 零知识证明) is explicitly a non-claim and possible future privacy layer. | 2, 9, 12 | No new code needed. |
| Not legal compliance | Correct. A policy reference in an evidence object is not a legal opinion, regulatory certification, or compliance proof. | 2, 7, 9, 12 | No new code needed. |
| Not full repository pytest | Correct. The draft reports `make paper-demo` and targeted EEOAP tests only; full repository pytest success is not claimed. | 6, 7, 12 | No new code needed. |
| Artifact local-only | Correct. The local sealed tag is an anchor, not a public release. Public release and DOI wording must wait until those artifacts exist. | 7, 12 | No new code needed unless author chooses a later release step. |
