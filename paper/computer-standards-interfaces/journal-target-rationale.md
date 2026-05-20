# Journal Target Rationale

Target journal: Computer Standards & Interfaces (计算机标准与接口期刊).

Status: journal-preparation rationale, not a submission statement.

## 1. Fit With the Journal

Computer Standards & Interfaces is an appropriate target for the EEOAP
(Execution Evidence and Operation Accountability Profile, 执行证据与操作问责配置文件)
paper because the contribution is standards-facing and interface-centered
rather than model-centered. The paper studies a minimal profile for one AI
(Artificial Intelligence, 人工智能) agent operation, a validator-backed checking
path, and a reproducible paper artifact. Those concerns align with standards,
interfaces, software quality, conformance validation, data communications,
measurement, tools, protocols, and software process topics.

The core technical object is not a new model architecture or benchmark. It is
a profile method: a structured evidence object that binds actor, action,
subject, policy, output, provenance, evidence references, and integrity values
into a locally reviewable record. The companion validator path checks
structure, references, policy/evidence linkage, and integrity binding. This
makes the work better aligned with a standards and interface journal than with
venues primarily centered on model training, model performance, or machine
learning novelty.

## 2. Standards and Interface Fit

EEOAP is positioned as a small operation-level profile that can be discussed by
standards, data-space, and software-quality reviewers. Its fit comes from:

- standards-facing profile design rather than broad governance marketing;
- a local validator path rather than a hosted service claim;
- explicit conformance-style checks over structure, references, and integrity;
- FDO (FAIR Digital Object, 公平数字对象)-style data-space mapping for discussion;
- artifact reproducibility through `make paper-demo`;
- clear distinction between claims, evidence, and non-claims.

The paper is also relevant to data-space object systems because it treats an
AI agent operation as a reviewable object adjacent to subject descriptors,
policy references, provenance statements, and integrity bindings. It does not
claim official FDO adoption or FDO conformance.

## 3. Better Fit Than Pure AI Model Venues

Pure AI model venues usually expect contributions in model architecture,
learning algorithms, benchmarks, optimization, reasoning performance, or
empirical comparison across models. EEOAP does not make those claims. It does
not evaluate model accuracy, robustness, or semantic correctness of AI output.
It instead asks whether one operation can be packaged as structured execution
evidence and checked after execution.

That question is closer to software quality, conformance validation,
interfaces, protocol design, and artifact review than to model science. A pure
AI model venue could misread the paper as too small because the artifact is a
minimal paper case rather than a broad model evaluation. Computer Standards &
Interfaces gives a more natural review frame: is the evidence profile clear,
is the validator boundary meaningful, is the interface between agent operation
and data-space evidence review well-defined, and are the non-claims preserved?

## 4. Safer Than Top-tier Software Engineering Journals at Current Depth

Top-tier software engineering journals often expect extensive empirical
validation, multi-project studies, industrial deployments, large user studies,
or broad tool comparisons. The current EEOAP artifact is deliberately smaller:
one reproducible `paper_case`, one valid evidence PASS path, one tampered
output FAIL path, and targeted EEOAP tests. That is a sound artifact boundary,
but it is not yet a broad empirical software engineering study.

Computer Standards & Interfaces is safer at the current validation depth
because the paper can be evaluated as a profile, interface, validation, and
standards-discussion contribution. The current evidence supports a narrow
claim: a minimal operation evidence object can be checked offline, and a
tampered output reference can be rejected with
`references_digest_mismatch`. It does not support claims about broad
deployment performance, full repository health, or production maturity.

## 5. Exact Scope Boundary

The paper scope is:

- one minimal operation-level execution evidence profile;
- one local validator-backed checking path;
- one reproducible paper case under `examples/paper_case/`;
- valid evidence bundle PASS through `make paper-demo`;
- tampered-output FAIL with `references_digest_mismatch`;
- targeted EEOAP tests previously reported as `19 passed, 1 warning`;
- FDO-style mapping for standards discussion.

The paper does not claim:

- production readiness;
- official FDO (FAIR Digital Object, 公平数字对象) standard adoption,
  certification, conformance, or endorsement;
- public GitHub Release publication;
- Zenodo DOI (Digital Object Identifier, 数字对象标识符);
- ZKP (Zero-Knowledge Proof, 零知识证明) implementation;
- legal compliance;
- semantic correctness of AI output;
- full repository pytest success.
