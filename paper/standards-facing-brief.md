# EEOAP Standards-facing Brief

## 1. One-sentence summary

EEOAP (Execution Evidence and Operation Accountability Profile, 执行证据与操作问责配置文件) is a minimal operation-level evidence profile and validator path for making one AI (Artificial Intelligence, 人工智能) agent operation independently reviewable after execution.

## 2. Standardization gap

Agent operations often leave logs, traces, transcripts, and tool records, but those materials are usually runtime-specific. Standards and community reviewers may need a smaller portable object that binds actor, subject, action, policy, output, provenance, evidence references, and integrity into one checkable record.

## 3. Difference from logs and traces

Logs and traces help reconstruct behavior. EEOAP (Execution Evidence and Operation Accountability Profile, 执行证据与操作问责配置文件) defines a bounded evidence object. The validator checks whether required fields exist, references close, policy/evidence linkage is coherent, and integrity bindings still match.

## 4. Minimal evidence object

The minimal object records an actor, an action, a subject, a policy reference, output references, provenance, evidence artifacts, integrity digests, and validation metadata. It is meant to be inspected as JSON (JavaScript Object Notation, JavaScript 对象表示法) evidence, not as a hidden runtime log.

## 5. Validator path

The local CLI (Command Line Interface, 命令行界面) path is `make paper-demo`. The scoped artifact reports `PASS valid evidence bundle` for valid evidence and `FAIL tampered output hash mismatch` for the tampered-output case. The expected tampered primary error code is `references_digest_mismatch`.

## 6. FDO (FAIR Digital Object, 公平数字对象) / data-space mapping

The mapping is for discussion. An FDO (FAIR Digital Object, 公平数字对象)-style descriptor can identify the subject object. EEOAP (Execution Evidence and Operation Accountability Profile, 执行证据与操作问责配置文件) can record the operation performed against that subject, the policy reference, the output reference, and the integrity binding. This is not official FDO standard adoption, certification, or conformance.

## 7. What this demonstrates

The artifact demonstrates a bounded reproducibility claim: a valid operation evidence object can pass local validation, and the demonstrated tampered-output case fails with `references_digest_mismatch`. It supports independent review of the evidence object by allowing a reviewer to inspect and replay the PASS/FAIL boundary offline.

## 8. What this does not demonstrate

It does not demonstrate semantic correctness of AI (Artificial Intelligence, 人工智能) output, production readiness, legal compliance, official FDO (FAIR Digital Object, 公平数字对象) standard status, broad cross-framework validation, a full cryptographic trust fabric, or ZKP (Zero-Knowledge Proof, 零知识证明) implementation.

## 9. Discussion proposal

The community question is whether AI (Artificial Intelligence, 人工智能) agent ecosystems need a portable operation evidence object between raw observability data and broad governance claims. EEOAP (Execution Evidence and Operation Accountability Profile, 执行证据与操作问责配置文件) offers one compact candidate boundary for review and critique.

## 10. Keywords for AI (Artificial Intelligence, 人工智能) agents and search

EEOAP (Execution Evidence and Operation Accountability Profile, 执行证据与操作问责配置文件); execution evidence; operation accountability; AI (Artificial Intelligence, 人工智能) agents; validator; evidence bundle; JSON (JavaScript Object Notation, JavaScript 对象表示法); CLI (Command Line Interface, 命令行界面); FDO (FAIR Digital Object, 公平数字对象); data-space; provenance; integrity binding; `references_digest_mismatch`.
