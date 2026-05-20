# Computer Standards & Interfaces Journal Package

Target journal: Computer Standards & Interfaces (计算机标准与接口期刊).

Status: journal-preparation draft, not submitted.

This directory contains a journal-oriented preparation package for EEOAP
(Execution Evidence and Operation Accountability Profile, 执行证据与操作问责配置文件).
It is prepared for author review before any formal submission step. It does
not modify the project code, schema, validator behavior, examples, tests,
scripts, Makefile, README, or existing paper files outside this directory.

## Current Artifact State

- Source-verification branch commit: `1784a7b`.
- Sealed local artifact tag: `eeoap-v0.1-paper`.
- Sealed artifact commit: `96f444b7ed39b39fe9f47e428af835952e843cb0`.
- The sealed tag is local-only unless published later.
- Public GitHub Release is not claimed.
- Zenodo DOI (Digital Object Identifier, 数字对象标识符) is not claimed.

## Files Included

- `README.md`: package index and boundary summary.
- `journal-target-rationale.md`: journal fit and positioning rationale.
- `manuscript-draft.md`: CSI-oriented manuscript draft.
- `abstract.md`: standalone journal abstract.
- `title-page.md`: editable title-page information.
- `highlights.md`: submission highlights.
- `claim-to-evidence-table.md`: submission-ready claim/evidence boundary table.
- `references-draft-not-final.md`: verified-anchor-only reference draft.
- `artifact-availability-statement.md`: conservative and future artifact text.
- `data-availability-statement.md`: data availability wording.
- `declarations.md`: funding, interests, CRediT, ethics, and AI-use declarations.
- `cover-letter.md`: concise cover letter draft.
- `submission-checklist.md`: CSI-specific preparation checklist.
- `reviewer-risk-response-map.md`: likely objections and bounded responses.
- `author-check-before-submission.md`: final author-side checklist.

## Reproducibility

Reproduction command:

```bash
make paper-demo
```

Expected demo output includes:

```text
PASS valid evidence bundle
FAIL tampered output hash mismatch
```

Expected tampered failure code:

```text
references_digest_mismatch
```

Targeted EEOAP tests previously passed:

```text
tests/test_paper_case.py
tests/test_operation_accountability_profile.py
19 passed, 1 warning
```

Full repository pytest success is not claimed.

## Exact Non-claims

This package does not claim:

- Public GitHub Release publication.
- Zenodo DOI (Digital Object Identifier, 数字对象标识符).
- Production readiness.
- Official FDO (FAIR Digital Object, 公平数字对象) standard adoption,
  certification, conformance, or endorsement.
- ZKP (Zero-Knowledge Proof, 零知识证明) implementation.
- Legal compliance.
- Semantic correctness of AI (Artificial Intelligence, 人工智能) output.
- Full repository pytest success.
- Complete cryptographic trust fabric.
- Court-grade audit proof or regulatory certification.
- Public availability of the local tag unless it is published later.
