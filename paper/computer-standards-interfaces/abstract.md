# Abstract

EEOAP (Execution Evidence and Operation Accountability Profile, 执行证据与操作问责配置文件)
defines a minimal operation-level evidence profile for one AI (Artificial
Intelligence, 人工智能) agent operation in FDO (FAIR Digital Object, 公平数字对象)-
style data spaces. The profile packages actor, action, subject, policy,
output, provenance, evidence references, integrity binding, and validation
metadata into a structured object that can be reviewed outside the original
runtime. The accompanying artifact provides a local validator path and a
reproducible `paper_case` example. Running `make paper-demo` reports a valid
PASS for the evidence bundle and an expected tampered FAIL for an altered
output reference. The tampered case exposes `references_digest_mismatch`,
showing that a stale integrity binding is not silently accepted. Targeted
EEOAP tests for the paper case and operation-accountability profile previously
reported 19 passed / 1 warning. The contribution is intentionally bounded:
it does not claim full repository pytest success, public GitHub Release
publication, Zenodo DOI issuance, production readiness, official FDO standard
adoption, legal compliance, semantic correctness of AI output, or ZKP
(Zero-Knowledge Proof, 零知识证明) implementation. The result is a standards-
facing research artifact that makes selected operation evidence claims
inspectable, replayable, and falsifiable offline. It supports profile and
interface review rather than model benchmarking.
