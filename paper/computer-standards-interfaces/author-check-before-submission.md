# Author Check Before Submission

Use this checklist immediately before any actual Computer Standards &
Interfaces submission. It is an author-side gate, not evidence that submission
is already ready.

- [ ] Verify all reference metadata manually.
- [ ] Verify final journal reference style and citation placement.
- [ ] Decide whether to push tag `eeoap-v0.1-paper` or create a public release.
- [ ] Do not move `eeoap-v0.1-paper`.
- [ ] Update artifact availability wording only after actual release state
      changes.
- [ ] Do not claim a public GitHub Release unless it actually exists.
- [ ] Do not claim a Zenodo DOI (Digital Object Identifier, 数字对象标识符)
      unless it has actually been issued.
- [ ] Check the current Computer Standards & Interfaces instructions before
      final upload.
- [ ] Check abstract length against the journal's current limit.
- [ ] Check highlights: 3 to 5 bullets, each 85 characters or fewer.
- [ ] Check AI-assisted writing disclosure wording.
- [ ] Confirm AI tools are not listed as authors.
- [ ] Run `make paper-demo`.
- [ ] Run targeted EEOAP tests:
      `python -m pytest tests/test_paper_case.py tests/test_operation_accountability_profile.py`.
- [ ] Do not run or claim full repository pytest unless it is actually run and
      passed.
- [ ] Preserve no production readiness claim.
- [ ] Preserve no official FDO (FAIR Digital Object, 公平数字对象) standard
      adoption, certification, conformance, or endorsement claim.
- [ ] Preserve no legal compliance claim.
- [ ] Preserve no ZKP (Zero-Knowledge Proof, 零知识证明) implementation claim.
- [ ] Preserve no semantic correctness claim for AI (Artificial Intelligence,
      人工智能) output.
- [ ] Confirm all manuscript and declaration files match the actual artifact
      state at the time of upload.
