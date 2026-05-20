# EEOAP Paper Reproducible Release Checklist

## 1. Scope

This checklist is for a scoped paper reproducible artifact release of EEOAP (Execution Evidence and Operation Accountability Profile, 执行证据与操作问责配置文件). It is not a full repository release, and it is not a production governance release, production policy engine, runtime security platform, or legal-compliance product.

The intended release boundary is a small, reviewable package that shows a validator-backed execution evidence profile, a reproducible `paper_case`, and a tampered-output failure case. Tagging, GitHub release creation, DOI registration, and external announcement remain manual future steps.

## 2. Required Artifact Files

Before an `eeoap-v0.1-paper` release is considered, confirm that these files and directories are present and reviewable:

- `examples/paper_case/`
- `scripts/reproduce_paper_demo.sh`
- `Makefile` `paper-demo` target
- `docs/what-this-proves.md`
- `docs/what-this-does-not-prove.md`
- `docs/paper-demo-boundary.md`
- `paper/outline.md`
- `paper/evaluation.md`
- `paper/figures/execution-evidence-pipeline.md`
- `paper/abstract.md`
- `paper/draft.md`
- `paper/submission-notes.md`
- `tests/test_paper_case.py`

## 3. Required Commands

### A. Required Scoped EEOAP Release Checks

Run these checks before a scoped EEOAP paper artifact release:

```bash
git status --short
```

```bash
git diff --check
```

```bash
make paper-demo
```

```bash
python -m pytest tests/test_paper_case.py tests/test_operation_accountability_profile.py
```

Use `git status --short` to confirm that no unintended files are staged or committed. Local unrelated dirty files may exist in another worktree, but they must not be part of the scoped EEOAP release commit or artifact.

### B. Optional Full Repository Health Check

```bash
python -m pytest
```

This optional full repository health check is useful, but it is not the release gate for the scoped EEOAP paper artifact. If the optional full repository health check fails only because of unrelated artifacts outside the EEOAP `paper_case` scope, the release may still proceed as a scoped EEOAP paper artifact. In that case, release notes must not claim full repository pytest success.

## 4. Expected Paper Demo Output

The `make paper-demo` output must include exactly these expected lines:

```text
PASS valid evidence bundle
FAIL tampered output hash mismatch
```

The expected tampered failure code is:

```text
references_digest_mismatch
```

This failure code is the core evidence that the tampered output/reference digest mismatch is detected by the validator-backed path.

## 5. Claims Allowed

The release may claim:

- Minimal execution evidence profile.
- Validator-backed reproducibility.
- Tamper detection for output/reference digest mismatch.
- Offline review path.
- FDO-style mapping for discussion.
- Scoped EEOAP verification passed.
- Targeted EEOAP tests passed.

## 6. Claims Not Allowed

The release must not claim:

- Official FDO (FAIR Digital Object, 公平数字对象) standard status.
- Proof that the AI (Artificial Intelligence, 人工智能) answer is semantically correct.
- Proof that the runtime was fully secure.
- Legal compliance by itself.
- Implemented ZKP (Zero-Knowledge Proof, 零知识证明).
- Production readiness.
- Full repository pytest success, unless it actually passes in a clean worktree.
- Repository-wide production readiness.

## 7. Versioning Suggestion

Preferred future scoped tag name:

```text
eeoap-v0.1-paper
```

This scoped tag name is clearer than a generic `v0.1-paper` tag because it indicates that the release covers the EEOAP paper reproducible artifact, not the full repository. Tagging and release creation are manual future steps and must not be treated as completed by this checklist.

## 8. Pre-release Manual Review

Before any tag or release is created, manually confirm:

- [ ] No unrelated dirty files are included.
- [ ] No local Codex summary logs are included.
- [ ] README paper demo section is present.
- [ ] `paper/draft.md` matches actual `make paper-demo` behavior.
- [ ] FDO wording remains "FDO-style mapping" and discussion-oriented.
- [ ] ZKP remains future work only.
- [ ] Unrelated dirty or untracked files from other research lines are not included.
- [ ] Any unrelated full pytest failures are documented separately and are not represented as EEOAP failures.

## 9. Artifact Statement

This release packages a minimal reproducible artifact for EEOAP: an execution evidence and operation accountability profile, a validator-backed `paper_case`, a valid evidence object, a tampered output/reference mismatch case, boundary documentation, tests, and a paper draft. It demonstrates that valid evidence can pass offline review and that a tampered output reference can fail with `references_digest_mismatch`, while avoiding claims of production readiness, official FDO standard status, legal compliance, semantic correctness, or implemented ZKP.
