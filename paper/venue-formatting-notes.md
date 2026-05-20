# EEOAP Venue Formatting Notes

## 1. Current status

The EEOAP (Execution Evidence and Operation Accountability Profile, 执行证据与操作问责配置文件) paper is workshop-submission ready. It becomes a formal-submission candidate only after bibliography completion, citation cleanup, and venue formatting.

This note is venue-neutral. It does not claim formal submission readiness, acceptance, public release, Zenodo DOI (Digital Object Identifier, 数字对象标识符), production readiness, official FDO (FAIR Digital Object, 公平数字对象) standard status, or ZKP (Zero-Knowledge Proof, 零知识证明) implementation.

## 2. Best-fit formats

- Short technical paper
- Artifact paper
- Standards-facing workshop paper
- Data-space / FDO discussion paper
- Software engineering validation workshop paper

## 3. Weak-fit formats

- Pure AI (Artificial Intelligence, 人工智能) model-performance venue
- Cryptography venue requiring new proof systems
- Broad governance policy venue
- Production systems venue requiring deployment evidence

## 4. Formatting tasks by venue type

### IEEE (Institute of Electrical and Electronics Engineers，电气与电子工程师协会)-style paper

- Convert markdown headings into the venue's section hierarchy.
- Keep the abstract within the venue word limit.
- Add verified references in the required IEEE reference style.
- Make related work citation-dense enough to support category claims.
- Keep artifact results as internal evidence, not bibliography claims.
- Add an artifact availability paragraph only after confirming the real release state.
- Verify whether AI (Artificial Intelligence, 人工智能)-assisted writing disclosure is required.

### ACM (Association for Computing Machinery，计算机协会)-style paper

- Map the current sections into ACM-style introduction, method, artifact, evaluation, related work, limitations, and artifact availability sections.
- Add CCS concepts and keywords only after venue selection.
- Convert candidate references into venue-compliant BibTeX only after source verification.
- Keep the contribution framed as a profile-plus-validator artifact, not a full platform.
- Preserve the boundary that full repository pytest, public release, DOI, production readiness, and official FDO adoption are not claimed.
- Verify whether artifact appendix, artifact badge, or availability statement rules apply.

### Workshop-style markdown / proceedings paper

- Keep the paper compact and emphasize the reproducible `make paper-demo` path.
- Add a short related-work paragraph with verified sources for each main category.
- Keep tables simple and text-first.
- Preserve exact expected output lines: `PASS valid evidence bundle` and `FAIL tampered output hash mismatch`.
- Preserve the expected tampered failure code: `references_digest_mismatch`.
- Avoid adding formal release or DOI wording unless that state changes later.

### Standards-facing white paper

- Lead with the operation evidence boundary and the FDO/data-space discussion fit.
- Keep the mapping language discussion-oriented.
- Separate data-object identity from operation-evidence validation.
- Avoid conformance, certification, adoption, endorsement, or compliance language.
- Add verified FDO, DOIP, and data-space references before circulation outside the project.
- Include non-claims prominently so the white paper cannot be read as an implementation standard.

## 5. Figure and table needs

- Text-level formatting is enough for the next stage.
- Do not request new diagrams unless the current text already has one that a selected venue requires.
- Existing material can support a compact table for claims, evidence, and non-claims.
- Existing material can support a compact table for valid bundle PASS, tampered output FAIL, error code, targeted tests, and full repository pytest non-claim.
- If a figure is required later, it should describe the existing evidence-object and validator flow rather than add new technical claims.

## 6. Artifact statement wording

Preserve these points:

- The local sealed tag `eeoap-v0.1-paper` exists as the artifact anchor.
- Public release is not claimed.
- DOI (Digital Object Identifier, 数字对象标识符) is not claimed.
- The artifact boundary is scoped to the EEOAP paper case, local validator path, valid evidence bundle, tampered-output negative case, and targeted EEOAP tests.
- Full repository pytest success, production readiness, official FDO standard adoption, legal compliance, and ZKP implementation are not claimed.

Suggested neutral wording for later adaptation:

> The artifact is currently a scoped local paper artifact anchored by the sealed local tag `eeoap-v0.1-paper`. This text does not claim a public GitHub Release, Zenodo DOI, production deployment, official FDO standard adoption, legal compliance result, or ZKP implementation.

## 7. AI-assisted writing disclosure

Some venues may require disclosure of AI (Artificial Intelligence, 人工智能)-assisted drafting, coding, editing, or checking. If required, the disclosure should be careful and factual: the author remains responsible for all claims, code, artifacts, citations, validation results, release statements, and conclusions.

Do not add an AI-assisted writing disclosure to the manuscript automatically. Add it only after the selected venue's policy is reviewed.
