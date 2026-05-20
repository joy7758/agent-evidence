# EEOAP Citation Audit

## 1. Purpose

This audit maps EEOAP (Execution Evidence and Operation Accountability Profile, 执行证据与操作问责配置文件) paper claims to citation needs, internal artifact evidence, and non-claim boundaries. It is a preparation document for later formal submission work. It is not a completed bibliography and does not assert formal submission readiness.

## 2. Claims that need citations

- Logs, traces, spans, transcripts, and observability systems help reconstruct runtime behavior but do not automatically define a bounded operation evidence object.
- Agent frameworks may expose tool calls, intermediate messages, execution spans, or traces.
- Provenance models describe derivation, process contribution, and data lineage.
- Profile, schema, and conformance validators are common mechanisms for narrowing broad data models into checkable subsets.
- JSON (JavaScript Object Notation, JavaScript 对象表示法) Schema and related validation practices are relevant to the paper's profile-and-validator framing.
- Supply-chain provenance, signed metadata, transparency logs, attestations, and integrity manifests are related background for binding artifacts to process claims.
- FDO (FAIR Digital Object, 公平数字对象), DOIP (Digital Object Interface Protocol，数字对象接口协议), and data-space systems provide relevant background on object identity, metadata, policy references, provenance, and exchange concepts.
- Agent governance literature discusses monitoring, control, approval, auditability, policy compliance, and organizational accountability.
- Artifact evaluation and reproducibility guidance supports the paper's positioning as an artifact/profile contribution.

## 3. Claims already supported by artifact results

- `make paper-demo` is an internal artifact fact, not an external literature citation.
- The valid evidence bundle result, `PASS valid evidence bundle`, is an internal artifact result.
- The tampered-output result, `FAIL tampered output hash mismatch`, is an internal artifact result.
- `references_digest_mismatch` is an internal validator result.
- `tampered_primary_error_code=references_digest_mismatch` is an internal demo summary field.
- Targeted EEOAP tests `19 passed, 1 warning` are internal verification results for the targeted scope only.
- The local sealed artifact tag `eeoap-v0.1-paper` and sealed artifact commit are artifact-state facts, not external literature.
- The current text-polish base commit is a repository-state fact, not an external citation.

## 4. Claims that should remain uncited internal artifact facts

- The exact `make paper-demo` command and expected PASS/FAIL lines.
- The valid and tampered `examples/paper_case/` behavior.
- The `references_digest_mismatch` failure code.
- The targeted EEOAP test result, while preserving that full repository pytest is not claimed.
- The scoped local artifact boundary.
- The absence of a claimed public GitHub Release or Zenodo DOI (Digital Object Identifier, 数字对象标识符).
- The absence of production readiness, official FDO adoption, legal compliance, or ZKP (Zero-Knowledge Proof, 零知识证明) implementation claims.

## 5. Claims that must be weakened if no source is added

- Replace broad claims such as "many existing systems" with narrower phrasing if no source is added.
- Avoid saying logs, traces, or observability systems never provide accountability evidence. The safer claim is that they do not automatically package the specific EEOAP operation boundary.
- Avoid claiming general novelty over all provenance, attestation, or governance systems. The safer claim is that EEOAP composes selected elements into a minimal validator-backed operation object.
- Avoid saying FDO or data-space communities require EEOAP. The safer claim is that EEOAP is relevant to discussion because those communities often discuss object identity, metadata, policy, provenance, and integrity.
- Avoid saying agent governance work lacks evidence objects. The safer claim is that EEOAP contributes one narrow artifact and validation boundary inside a broader space.

## 6. Related work citation gaps

- Logs, traces, observability, and runtime telemetry need verified background sources.
- Provenance and workflow validity constraints need verified background sources.
- JSON Schema and conformance validation need verified standard or specification sources.
- Attestation, signed metadata, supply-chain provenance, and transparency-log background need verified sources.
- FDO, DOIP, and data-space object-system discussion needs verified standards-facing sources.
- Agent governance and execution evidence needs verified technical sources, not broad policy-only references.
- Artifact evaluation and reproducibility positioning needs venue-appropriate sources or guidelines.

## 7. Artifact availability citation boundary

- Public GitHub Release and Zenodo DOI are not claimed.
- A public release URL, archive URL, DOI, badge, or external artifact citation must not be added until it exists.
- The sealed local tag `eeoap-v0.1-paper` can be described as a local artifact anchor, but not as a public release.
- Artifact evidence should remain scoped to the local repository files, `make paper-demo`, the valid evidence bundle, the tampered-output failure, and targeted EEOAP tests.
- FDO-style mapping is discussion-oriented, not official adoption, certification, endorsement, or conformance.

## 8. Formal submission citation checklist

- Verify every external reference before adding author names, years, DOI values, standard versions, or official titles.
- Add citations for the broad related-work categories before formal submission.
- Confirm that internal artifact facts are not formatted as external literature citations.
- Preserve the no-claim boundary for public release, Zenodo DOI, production readiness, official FDO status, legal compliance, full cryptographic trust, and ZKP implementation.
- Recheck all FDO and DOIP language after citations are inserted.
- Recheck all claims about logs, traces, provenance, observability, attestation, and governance after citations are inserted.
- Confirm the final venue's reference style only after the venue is selected.
- Keep this audit as preparation material unless a later formal submission pass explicitly integrates it into the manuscript package.
