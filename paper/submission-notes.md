# EEOAP Submission Notes

## 1. Positioning

Position the work as a short technical artifact/profile paper. EEOAP (Execution Evidence and Operation Accountability Profile, 执行证据与操作问责配置文件) should be described as a minimal execution evidence profile for one AI (Artificial Intelligence, 人工智能) agent operation, supported by a validator path and a reproducible `paper_case` artifact.

The strongest result is narrow: `make paper-demo` shows a valid evidence bundle passing and a tampered-output case failing with `references_digest_mismatch`. The paper should emphasize independently checkable operation evidence, not broad governance, production deployment, legal sufficiency, or new cryptographic proof systems.

After the current text-risk pass, the paper can be treated as workshop-submission ready. It should not be treated as a formal-submission candidate until bibliography completion, venue formatting, citation cleanup, and final artifact-availability wording are completed.

## 2. Best-fit venue types

Good fits:

- Artifact paper venues that value a runnable evidence bundle and verifier path.
- Short technical paper tracks focused on AI (Artificial Intelligence, 人工智能) engineering infrastructure, software accountability, or validation.
- Standards-facing workshops where execution evidence, provenance, object identity, and conformance profiles are in scope.
- Data-space / FDO (FAIR Digital Object, 公平数字对象) discussion venues where an operation-evidence object can be reviewed as an adjacent artifact, not as official FDO adoption.
- Software engineering validation venues that accept compact profile-plus-validator contributions.

Weak fits:

- Pure AI (Artificial Intelligence, 人工智能) model performance venues that expect accuracy, benchmark, or model-comparison results.
- Broad governance policy venues that expect legal, institutional, or regulatory frameworks rather than a small technical artifact.
- Cryptography venues requiring new proof systems; ZKP (Zero-Knowledge Proof, 零知识证明) belongs only in future work for this line.

## 3. Why this is artifact/profile work

The paper is not primarily a theory paper, systems-performance paper, or governance manifesto. Its contribution is a small profile boundary and a concrete validator-backed artifact. The profile packages actor, action, subject, policy, output, provenance, evidence references, and integrity binding into one evidence object. The validator checks structure, references, policy/evidence linkage, and integrity binding. The artifact demonstrates the boundary with one valid case and one intentional tampered-output case.

## 4. Claims to preserve

- EEOAP (Execution Evidence and Operation Accountability Profile, 执行证据与操作问责配置文件) is a minimal operation-level evidence profile.
- The artifact provides a local validator path and a reproducible `paper_case`.
- Valid evidence passes with `PASS valid evidence bundle`.
- Tampered output fails with `FAIL tampered output hash mismatch`.
- The expected tampered primary error code is `references_digest_mismatch`.
- The FDO (FAIR Digital Object, 公平数字对象) / data-space mapping is for discussion, not official standard adoption.
- Targeted EEOAP tests previously passed, specifically `tests/test_paper_case.py` and `tests/test_operation_accountability_profile.py`.

## 5. Claims to avoid

- Do not claim semantic correctness of AI (Artificial Intelligence, 人工智能) outputs.
- Do not claim production readiness.
- Do not claim full repository pytest success.
- Do not claim legal compliance or legal sufficiency of the policy.
- Do not claim official FDO (FAIR Digital Object, 公平数字对象) adoption, certification, conformance, or endorsement.
- Do not claim a full cryptographic trust fabric, secure timestamping system, trusted execution attestation, or uncompromised signer identity.
- Do not claim ZKP (Zero-Knowledge Proof, 零知识证明) implementation.
- Do not treat AEP (Agent Evidence Profile, 智能体证据配置文件), AEP-Media (Agent Evidence Profile Media, 智能体证据配置文件媒体扩展), AI Act (Artificial Intelligence Act, 人工智能法案), or unrelated prior papers as interchangeable evidence for this EEOAP scope.
- Do not present the local artifact tag as a public release.

## 6. What to add before formal submission

- Bibliography completion with verified citation metadata.
- Venue-specific formatting, length control, and reference style.
- Citation cleanup across the manuscript, notes, and related-work scaffolding.
- Related work references backed by actual sources rather than placeholders or generic category labels.
- A short artifact appendix listing exact commands, expected output, environment assumptions, and known limitations.
- A table mapping claims to evidence files and validation outputs.
- A final author review of terminology around FDO (FAIR Digital Object, 公平数字对象), JSON (JavaScript Object Notation, JavaScript 对象表示法), CLI (Command Line Interface, 命令行界面), and ZKP (Zero-Knowledge Proof, 零知识证明).
- Final artifact availability wording based on the real release state: whether `eeoap-v0.1-paper` has been publicly pushed or remains a sealed local tag, whether a public GitHub Release exists, and whether a DOI (Digital Object Identifier, 数字对象标识符) has actually been issued.
- A formal release or archive plan only after the paper text and artifact boundary are reviewed.

## 7. What not to add before formal submission

- Do not add code, schema, validator behavior, examples, tests, scripts, Makefile changes, or README changes solely to make the paper sound larger.
- Do not add ZKP (Zero-Knowledge Proof, 零知识证明) mechanisms unless a later project explicitly opens that implementation scope.
- Do not import broad AEP (Agent Evidence Profile, 智能体证据配置文件), AEP-Media (Agent Evidence Profile Media, 智能体证据配置文件媒体扩展), AI Act (Artificial Intelligence Act, 人工智能法案), or unrelated manuscript claims.
- Do not add public release, DOI (Digital Object Identifier, 数字对象标识符), acceptance, endorsement, or standard-adoption language before those facts exist.
- Do not turn the paper into a general AI governance framework or marketing document.

## 8. Reviewer-risk checklist

- Does the draft clearly say this is a scoped artifact/profile contribution?
- Does the related-work section avoid saying that nobody has done logs, provenance, attestation, or tamper-evident records before?
- Does the evaluation avoid claiming full repository pytest success?
- Does the artifact availability section say local-only unless published later?
- Does the text keep workshop-submission ready separate from formal-submission candidate?
- Does every FDO (FAIR Digital Object, 公平数字对象) mention avoid implying official standard adoption?
- Does every ZKP (Zero-Knowledge Proof, 零知识证明) mention keep it as future work only?
- Are production readiness, legal compliance, semantic correctness, and broad cross-framework validation explicitly out of scope?
- Are the expected demo lines and `references_digest_mismatch` code preserved exactly?
