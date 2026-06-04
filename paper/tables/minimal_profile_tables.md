# Paper-Minimal Profile Tables

These tables support the paper-minimal path for Execution Evidence and
Operation Accountability Profile v0.1. They do not expand the claim beyond the
current profile, validator, controlled examples, demo, and rerun boundary.

## Table A: Profile Sections

| section | role | required review question | validator responsibility |
| --- | --- | --- | --- |
| `profile` | Declares the profile identity and version. | Is the statement bound to the intended EEOAP v0.1 profile? | Check fixed profile name and version. |
| `statement_id` | Gives the statement a stable local identifier. | Can this accountability statement be cited unambiguously? | Require a non-empty statement identifier. |
| `timestamp` | Records statement emission time. | Is the statement time explicitly recorded? | Require a date-time value accepted by the schema. |
| `actor` | Identifies the executor and runtime. | Who executed the operation, and under which runtime label? | Require actor identity, type, name, and runtime fields. |
| `subject` | Identifies the object acted on. | Which object was acted on, and how is it located and digested? | Require subject identity, type, locator, and digest shape. |
| `operation` | Describes the action, result, subject link, policy link, and I/O refs. | What operation was invoked, on which subject, under which policy, and with which I/O refs? | Check required operation fields and prepare references for closure checks. |
| `policy` | Names the governing policy and constraint refs. | Which policy governed the operation, and which constraints did it cite? | Require policy fields and verify constraint references. |
| `constraints` | Lists the concrete rules referenced by policy. | Are the cited constraints present and reviewable? | Require at least one identified constraint with a description. |
| `provenance` | Links actor, subject, operation, and I/O refs. | Do provenance links agree with the operation statement? | Check actor, subject, operation, input, and output reference consistency. |
| `evidence` | Lists referenced materials, artifacts, and integrity digests. | What evidence supports the operation, and can references and digests be checked? | Check evidence links, reference roles, artifact records, and integrity digest fields. |
| `validation` | Records how an independent verifier checks the statement. | Which validator and method make the statement independently checkable? | Require validator metadata and verify links to evidence, provenance, and policy. |

## Table B: Validator Stages

| stage | check target | representative failure | grounded example |
| --- | --- | --- | --- |
| schema conformance | Required fields, field shapes, constants, enums, and digest patterns. | `schema_violation` | `examples/invalid-missing-required.json` |
| reference closure | Local references from operation, policy, provenance, evidence, and validation. | `unresolved_output_ref` | `examples/invalid-unclosed-reference.json` |
| cross-field consistency / policy-evidence linkage | Agreement among policy, operation, provenance, evidence, and validation links. | `unresolved_evidence_policy_ref` | `examples/invalid-policy-link-broken.json` |
| integrity digest recomputation | Canonical digests for evidence references, artifacts, and statement core. | validator-defined surface | no standalone failing specimen in the paper-minimal path |

## Table C: Claim Boundary

| not claimed | reason | future work condition |
| --- | --- | --- |
| registry design | The paper-minimal object is one statement, not a registry protocol. | Define registry data model, lifecycle, lookup behavior, and independent tests. |
| multi-agent orchestration | The rerun checks one operation accountability statement, not a coordinated agent workflow. | Add bounded orchestration semantics, fixtures, and failure cases. |
| full FDO interoperability | The profile uses FDO-oriented object references but does not implement a complete interoperability layer. | Map profile fields to an external FDO implementation and validate round-trip behavior. |
| full cryptographic trust fabric | The current path recomputes digests but does not establish identity, signing, timestamping, or trust anchors. | Add signed statements, key management assumptions, timestamp evidence, and verifier tests. |
| legal non-repudiation | Technical validation is not a legal evidentiary claim. | Define jurisdiction-specific requirements with legal review and supporting controls. |
| production deployment | The artifact is a bounded research rerun, not an operated service. | Add deployment architecture, operational monitoring, security review, and service-level tests. |
| broad platform governance | The current claim is limited to one profile and validator path. | Define platform roles, governance workflows, policy lifecycle, and audit responsibilities. |
| broad runtime integration coverage | The paper-minimal path does not claim coverage across many runtimes. | Add runtime-specific adapters, conformance fixtures, and comparable validator results. |

## Table D: Reproduction Commands

| command | expected exit | expected result |
| --- | ---: | --- |
| `agent-evidence validate-profile examples/minimal-valid-evidence.json` | 0 | `ok: true` / `issue_count: 0` |
| `agent-evidence validate-profile examples/invalid-missing-required.json` | 1 | `schema_violation` |
| `agent-evidence validate-profile examples/invalid-unclosed-reference.json` | 1 | `unresolved_output_ref` |
| `agent-evidence validate-profile examples/invalid-policy-link-broken.json` | 1 | `unresolved_evidence_policy_ref` |
| `python demo/run_operation_accountability_demo.py` | 0 | `PASS` summary line |
