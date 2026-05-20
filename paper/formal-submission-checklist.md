# EEOAP Formal Submission Checklist

## 1. Preconditions

- Confirm the target venue and paper type.
- Confirm that this is a formal submission pass, not only workshop-submission preparation.
- Confirm the sealed artifact tag `eeoap-v0.1-paper` remains anchored and is not moved.
- Confirm the current text-polish base and any later edits are recorded in ordinary repository history only if a later commit is explicitly authorized.
- Confirm no code, schema, validator behavior, examples, tests, scripts, Makefile, README, or unrelated docs are changed for bibliography or formatting work.

## 2. Bibliography completion

- Verify all sources in `paper/references.md`.
- Add exact author names, titles, venues, years, versions, DOI (Digital Object Identifier, 数字对象标识符) values, URLs, and access dates only after source verification.
- Choose the final reference style only after venue selection.
- Do not invent bibliographic metadata.
- Do not add public release, archive, DOI, acceptance, endorsement, or standard-adoption references unless they exist.

## 3. Citation cleanup

- Use `paper/citation-audit.md` to map claims to citations or internal artifact facts.
- Cite logs, traces, observability, provenance, JSON (JavaScript Object Notation, JavaScript 对象表示法) Schema, attestation, FDO (FAIR Digital Object, 公平数字对象), DOIP (Digital Object Interface Protocol，数字对象接口协议), data-space systems, agent governance, and artifact reproducibility claims where needed.
- Keep `make paper-demo` as an internal artifact fact, not an external literature citation.
- Keep `references_digest_mismatch` as an internal validator result.
- Keep targeted EEOAP tests as an internal verification result.
- Weaken broad related-work language if verified sources are not added.

## 4. Venue formatting

- Apply the selected venue's section order, heading style, reference style, figure/table rules, page limit, and artifact statement rules.
- For IEEE (Institute of Electrical and Electronics Engineers，电气与电子工程师协会)-style papers, verify reference and abstract formatting.
- For ACM (Association for Computing Machinery，计算机协会)-style papers, verify CCS, keywords, artifact appendix, and BibTeX formatting.
- For workshop markdown or proceedings papers, preserve compact artifact-first framing.
- For standards-facing white papers, keep mapping language discussion-oriented and non-claim boundaries visible.

## 5. Artifact availability wording

- State that the local sealed tag `eeoap-v0.1-paper` exists only if that remains true.
- Do not claim public GitHub Release unless actually created later.
- Do not claim Zenodo DOI unless actually issued later.
- Do not claim external endorsement or artifact acceptance unless actually received later.
- Preserve the scoped artifact boundary: local validator path, `paper_case`, valid evidence PASS, tampered output FAIL, and targeted EEOAP tests.

## 6. Non-claims review

- No full repository pytest claim.
- No production readiness claim.
- No official FDO standard claim.
- No official FDO adoption, certification, conformance, or endorsement claim.
- No ZKP (Zero-Knowledge Proof, 零知识证明) implementation claim.
- No legal compliance, court-grade audit, or regulatory certification claim.
- No semantic correctness claim for AI (Artificial Intelligence, 人工智能) output.
- No public release / DOI claim unless actually created later.
- No movement of `eeoap-v0.1-paper` tag.

## 7. Reproducibility checks

- Run `make paper-demo`.
- Confirm `PASS valid evidence bundle`.
- Confirm `FAIL tampered output hash mismatch`.
- Confirm `tampered_primary_error_code=references_digest_mismatch`.
- Run targeted EEOAP tests only when explicitly in scope.
- Record targeted EEOAP tests as targeted scope only, for example `19 passed, 1 warning` if that is the current verified result.
- Do not claim full repository pytest unless it is actually run and passes in a later authorized pass.
- Do not install dependencies during a text-only submission-preparation pass.

## 8. Final author review

- Confirm all citations are real and accurately represented.
- Confirm all artifact statements match the actual release state.
- Confirm all FDO, DOIP, data-space, JSON Schema, CLI (Command Line Interface, 命令行界面), AI, and ZKP terminology is expanded consistently where needed.
- Confirm the author accepts responsibility for all claims, code, artifacts, citations, validation results, and conclusions.
- Check whether the venue requires AI-assisted writing or coding disclosure.

## 9. Submission package

- Final formatted manuscript.
- Verified reference list or BibTeX file.
- Artifact availability statement.
- Reproducibility command summary.
- Claim-to-evidence checklist.
- Non-claims checklist.
- Optional artifact appendix only if the venue permits or requires it.

## 10. Do not proceed if

- Bibliography metadata is unverified.
- Citation gaps remain for broad related-work claims.
- Venue formatting has not been applied.
- Artifact availability wording implies a public release or DOI that does not exist.
- The paper implies production readiness, official FDO standard status, legal compliance, full cryptographic trust, or ZKP implementation.
- Full repository pytest is implied without being run and verified.
- The `eeoap-v0.1-paper` tag would need to be moved.
- Any required author, venue, artifact, or AI-assisted writing disclosure review remains incomplete.
