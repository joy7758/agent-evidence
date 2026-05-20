# EEOAP Candidate Bibliography Inventory

## 1. Purpose

This file is a candidate reference inventory for EEOAP (Execution Evidence and Operation Accountability Profile, 执行证据与操作问责配置文件). It is not a finalized venue bibliography and does not establish final citation metadata, final reference style, DOI (Digital Object Identifier, 数字对象标识符) values, acceptance status, public release status, or external endorsement.

The purpose is to identify source areas that must be verified before a formal submission pass. Exact author names, years, venue names, DOI values, standard versions, and official titles should be added only after manual source verification.

## Verified source anchors added

A separate file, `paper/verified-source-anchors.md`, now records verified
anchors for provenance, JSON (JavaScript Object Notation, JavaScript 对象表示法)
Schema, artifact review, digital objects, DOIP (Digital Object Interface
Protocol，数字对象接口协议), SLSA (Supply-chain Levels for Software Artifacts,
软件制品供应链等级), in-toto, and OpenTelemetry (开放遥测). These anchors support
internal citation planning only; they do not finalize all candidate references.

## 2. Core reference clusters

- Logs, traces, and observability
- Provenance and validity constraints
- JSON (JavaScript Object Notation, JavaScript 对象表示法) Schema and conformance validation
- Verifiable provenance and attestation artifacts
- FDO (FAIR Digital Object, 公平数字对象), DOIP (Digital Object Interface Protocol，数字对象接口协议), and data-space object systems
- Agent governance and execution evidence
- Artifact evaluation and reproducibility

## 3. Candidate references to verify

### Logs, traces, and observability

- Candidate: Observability sources covering logs, metrics, traces, spans, and runtime events.
  - Status: verified-in-paper-text
  - Why it is relevant: The draft contrasts logs and traces with an operation-level evidence object.
  - Verification needed: Select authoritative sources and verify exact title, publisher, version, date, and citation format.
- Candidate: Agent runtime or framework tracing documentation.
  - Status: needs-source-verification
  - Why it is relevant: The draft says agent frameworks may expose tool calls, intermediate messages, execution spans, or traces.
  - Verification needed: Verify whether any specific framework source should be cited, and avoid implying endorsement or broad cross-framework validation.
- Candidate: General logging or tracing background literature.
  - Status: optional-background-only
  - Why it is relevant: It may help frame why ordinary operational records do not by themselves define a bounded evidence object.
  - Verification needed: Use only if the venue expects a deeper related-work baseline.

### Provenance and validity constraints

- Candidate: Provenance model or provenance data model sources.
  - Status: verified-in-paper-text
  - Why it is relevant: The draft uses provenance as one component of the operation evidence object.
  - Verification needed: Verify exact source family, official title, standard status, version, and citation details.
- Candidate: Workflow audit trail and validity-constraint sources.
  - Status: needs-source-verification
  - Why it is relevant: The draft discusses derivation, dependency relationships, policy/evidence linkage, and reference closure.
  - Verification needed: Add only sources that directly support the limited profile-and-validation framing.
- Candidate: Broad data lineage literature.
  - Status: optional-background-only
  - Why it is relevant: It may be useful background but should not displace the narrow EEOAP contribution.
  - Verification needed: Use sparingly to avoid turning the paper into a provenance survey.

### JSON (JavaScript Object Notation, JavaScript 对象表示法) Schema and conformance validation

- Candidate: JSON Schema specification family.
  - Status: verified-in-paper-text
  - Why it is relevant: The draft repeatedly frames the artifact as inspectable JSON evidence with validator-backed structure checks.
  - Verification needed: Verify exact specification names, versions, maintainers, publication dates, and citation style.
- Candidate: Conformance validation and profile validation sources.
  - Status: needs-source-verification
  - Why it is relevant: EEOAP is framed as a profile with a validator path rather than a new runtime platform.
  - Verification needed: Add only sources that support profile narrowing, schema conformance, or validation methodology.
- Candidate: Internal repository validator behavior.
  - Status: verified-in-paper-text
  - Why it is relevant: `make paper-demo` and the EEOAP validator path are internal artifact facts, not external bibliography.
  - Verification needed: Do not cite this as external literature; keep it in artifact and evaluation sections.

### Verifiable provenance and attestation artifacts

- Candidate: Supply-chain provenance sources.
  - Status: verified-in-paper-text
  - Why it is relevant: The draft mentions supply-chain provenance as related background for binding artifacts to process claims.
  - Verification needed: Choose exact sources only after manual verification; do not add specific framework names by guess.
- Candidate: Attestation, signed metadata, transparency log, and integrity manifest sources.
  - Status: needs-source-verification
  - Why it is relevant: The draft distinguishes EEOAP from stronger signing, timestamping, transparency, and trusted-execution layers.
  - Verification needed: Verify the selected source and ensure the citation supports background only, not an EEOAP implementation claim.
- Candidate: Trusted execution, secure timestamping, or key-custody systems.
  - Status: do-not-use-until-verified
  - Why it is relevant: These are tempting because the draft lists them as out of scope.
  - Verification needed: Do not cite unless the final manuscript explicitly discusses them as non-claims or future work with a verified source.

### FDO (FAIR Digital Object, 公平数字对象), DOIP (Digital Object Interface Protocol，数字对象接口协议), and data-space object systems

- Candidate: FDO overview, model, or specification sources.
  - Status: verified-in-paper-text
  - Why it is relevant: The paper uses FDO-style language and a local `fdo-dataset.json` example for discussion.
  - Verification needed: Verify exact FDO source details and avoid claiming official adoption, certification, conformance, or endorsement.
- Candidate: DOIP sources.
  - Status: needs-source-verification
  - Why it is relevant: DOIP may be relevant to object-interface discussions adjacent to FDO and data-space systems.
  - Verification needed: Verify whether DOIP belongs in the final venue bibliography; do not add version, title, authors, or DOI by memory.
- Candidate: Data-space policy, usage-control, or object-exchange sources.
  - Status: needs-source-verification
  - Why it is relevant: The draft frames EEOAP as adjacent to data-space object identity, policy context, and exchange concepts.
  - Verification needed: Select sources that support the discussion boundary without implying compliance or deployment evidence.

### Agent governance and execution evidence

- Candidate: Agent governance, auditability, monitoring, and accountability sources.
  - Status: verified-in-paper-text
  - Why it is relevant: The draft positions EEOAP as a narrow artifact inside broader agent governance concerns.
  - Verification needed: Verify sources that discuss governance or accountability without turning EEOAP into a broad policy framework.
- Candidate: AI (Artificial Intelligence, 人工智能) agent execution evidence or tool-call trace sources.
  - Status: needs-source-verification
  - Why it is relevant: The paper needs citations for claims about agent operations, tool calls, intermediate messages, and review needs.
  - Verification needed: Use sources that directly support execution evidence or auditability, not model-performance claims.
- Candidate: Broad legal, regulatory, or institutional governance sources.
  - Status: optional-background-only
  - Why it is relevant: They may help set context but are outside the core technical contribution.
  - Verification needed: Use only if the venue requires policy context, and keep legal compliance as a non-claim.

### Artifact evaluation and reproducibility

- Candidate: Artifact evaluation guidelines or reproducibility-badge guidance.
  - Status: needs-source-verification
  - Why it is relevant: The paper is strongest as an artifact/profile paper with a replayable `make paper-demo` path.
  - Verification needed: Verify venue-specific artifact guidance before citing it.
- Candidate: Software reproducibility and research artifact packaging sources.
  - Status: needs-source-verification
  - Why it is relevant: The draft emphasizes local replay, expected output, and a bounded paper case.
  - Verification needed: Choose sources that fit a text-only formal submission pass and do not imply a public release or DOI.
- Candidate: Internal `make paper-demo` output and targeted EEOAP test result.
  - Status: verified-in-paper-text
  - Why it is relevant: These are the paper artifact's own verification facts.
  - Verification needed: Keep them as internal artifact facts, not external literature citations.

## 4. Citation risk notes

- The draft currently uses broad category language such as logs, traces, provenance, attestation, transparency logs, FDO, data-space systems, profile validation, and agent governance. Formal submission needs verified sources for those category claims.
- No exact DOI (Digital Object Identifier, 数字对象标识符) values, author names, publication years, standard versions, or official titles should be added from memory.
- FDO and DOIP sources require special care. The final paper may discuss an FDO-style mapping, but it must not imply official FDO adoption, conformance, certification, or endorsement.
- Attestation and cryptographic-evidence sources should be cited as related background only. The current artifact does not implement a full cryptographic trust fabric, trusted execution, secure timestamping, transparency-log inclusion, or ZKP (Zero-Knowledge Proof, 零知识证明).
- Artifact availability should cite the local command and repository files as internal artifact facts. Public GitHub Release, Zenodo DOI, and external archive citations must remain absent unless those artifacts are actually created later.

## 5. Do not cite yet

- Do not cite any public GitHub Release or Zenodo DOI for `eeoap-v0.1-paper` unless it is actually created later.
- Do not cite an official FDO standard adoption, certification, conformance result, or endorsement for EEOAP.
- Do not cite ZKP (Zero-Knowledge Proof, 零知识证明) systems as implemented support; at most, verified sources may later support future-work discussion.
- Do not cite legal compliance, regulatory certification, or court-grade audit sources as if EEOAP provides those guarantees.
- Do not add framework-specific tracing, observability, or agent governance references unless the exact source is manually verified and the paper text is adjusted to the same narrow boundary.
- Do not cite broad model-performance benchmarks unless a later paper version actually adds model-performance evaluation.
