# Methods: Minimal Profile and Profile-Aware Validation

## 1. Problem Setting and Design Goals

The method proposed in this paper addresses a narrow software-engineering problem: how to represent one operation accountability statement in an FDO-based agent system so that a third party can inspect it outside the original runtime context. The target object is deliberately small. It is not a workflow graph, not a registry, and not a general governance model. It is a single statement about one operation on one digital object context.

In the current repository, that statement must support at least the following questions in a checkable form: which operation was performed, on which subject object, under which policy basis and constraints, through which input and output references, with what evidence, and through what validation path. This framing is narrower than general observability and narrower than broad compliance automation. The point is to isolate the smallest unit that can still be specified, validated, tested, demonstrated, and archived as a software artifact.

This problem framing leads to five design goals. First, the method should be minimal rather than complete. The profile should retain only the fields needed to support a minimal accountability loop. Second, it should be verifiable rather than merely descriptive. A JSON object is not sufficient unless it can be checked by a validator that enforces profile-specific rules. Third, it should reuse the current repository surface rather than introduce a second implementation stack. Fourth, it should be artifact-oriented, meaning that the method must remain connected to examples, tests, a CLI entry point, and a runnable demo. Fifth, it should stay grounded in an FDO-based object setting without expanding into a broad FDO overview or claiming full coverage of all FDO variants.

These goals imply several explicit tradeoffs. The method uses a profile instead of a platform, staged validation instead of a maximal all-errors-at-once strategy, and a single-path demo instead of a large scenario suite. The resulting scope is intentionally constrained: a minimal verifiable profile, a profile-aware validator, and a repository-grounded artifact package.

## 2. Minimal Verifiable Profile

The current repository defines `execution-evidence-operation-accountability-profile` version `0.1`. The profile describes one operation accountability statement. At the top level, the statement contains `profile`, `statement_id`, `timestamp`, `actor`, `subject`, `operation`, `policy`, `constraints`, `provenance`, `evidence`, and `validation`. Within that top-level structure, the methodological core of the paper is the five-part organization of `operation`, `policy`, `provenance`, `evidence`, and `validation`.

The profile is minimal in three senses. It is minimal in problem scope because it covers only a single operation statement. It is minimal in field scope because it retains only the fields needed to support independent checking. It is minimal in validation scope because it does not try to establish a full trust fabric; it only requires the checks needed to make the statement externally inspectable.

This design can be seen as a disciplined reduction of the accountability problem. Instead of attempting to capture every future governance need, the profile isolates one portable statement and requires that all critical accountability links remain local to that statement. The repository specification makes the reduction explicit by fixing the profile identity and version, enumerating required fields, and defining field relationships that the validator must enforce.

[Insert Fig. 2 here]

Figure 2 summarizes that structure. `operation` is placed at the center because the paper treats operation accountability, not actor identity alone or policy expression alone, as the primary engineering object. The other four components are arranged around it because they bind the surrounding conditions needed to make one operation externally checkable.

## 3. Role of the Five Components

The five core components are not a feature inventory. They are the minimum set of responsibilities that must be co-located if a third party is expected to inspect one accountability statement without reconstructing context from unrelated system surfaces.

`operation` is the accountability center. It identifies the action, its type, its input and output references, and its result status and summary. In the current design, this is the component that answers the core question of what happened. The profile treats `operation` as the organizing object because the paper is concerned with single-operation accountability rather than general event logging.

`policy` captures the governing rule basis for the statement. It identifies the policy and the concrete constraints that the policy references. This component is necessary because an operation record without an explicit policy basis is often insufficient for accountability review. The method therefore requires policy binding to be first-class rather than left to surrounding documentation or external runtime context.

`provenance` connects `actor`, `subject`, `operation`, and the input and output references. Its role is not to replace richer provenance models, but to provide the minimum linkage needed to make the statement traceable as a local object. In the current profile, provenance is valuable precisely because it anchors the operation to a subject and to specific references rather than leaving these relationships implicit.

`evidence` contains the referenced materials that support the statement. In the current repository, this includes local references, artifacts, and integrity-related material. The method does not assume that a log stream or an artifact store elsewhere can stand in for this component. Instead, it requires that the statement carry a minimal evidence block of its own.

`validation` identifies how an external checker should inspect the statement. It records the relevant local objects, the validation method, the validator identity, and the validation status. This component matters because the method is not satisfied with merely describing the operation. It also wants to make the checking path explicit.

The remaining top-level fields support these five components without enlarging the method beyond its minimal scope. `actor` and `subject` provide the executor and the object context. `constraints` make policy references resolvable locally. `statement_id`, `timestamp`, and `profile` make the statement stable and versioned as an independent artifact.

The repository specification further fixes the link rules among these parts. For example, `operation.subject_ref` must equal `subject.id`; `operation.policy_ref` must equal `policy.id`; policy constraint references must resolve to local constraints; operation input and output references must resolve to evidence references; provenance references must match the corresponding actor, subject, and operation identifiers; and validation references must resolve to the local evidence, provenance, and policy objects. These rules explain why the method is described as a minimal verifiable profile rather than a loose schema template.

## 4. Validation Model

The validation model is designed to enforce the profile as an executable boundary rather than as a descriptive data shape. Conceptually, the method uses a two-layer validation logic, reflected in Figure 6. Structural conformance comes first. Accountability conformance follows. In the current repository implementation, that logic is realized as four ordered stages: schema checks, reference closure checks, cross-field consistency checks, and minimal integrity checks.

[Insert Fig. 6 here]

The first stage checks structural conformance. This includes required fields, field shape, and schema-level completeness. In the implementation, this stage is grounded in the JSON Schema and yields errors such as `schema_violation`. Structural conformance is necessary because the later stages depend on predictable field locations and types.

The second stage checks reference closure. This stage verifies that local references actually resolve to local identifiers. It covers constraint references, evidence reference identifiers, operation input and output references, and local references in provenance, evidence, and validation. It also detects duplicate identifiers where applicable. The point of this stage is to prevent a statement from looking complete while still relying on missing local objects.

The third stage checks cross-field consistency. Here the validator enforces the profile-specific semantic relationships among the five core components. Examples include checking whether provenance input and output references match the operation input and output references, whether policy-related references remain aligned across `operation`, `evidence`, and `validation`, and whether input and output roles are used consistently. This stage is central to the method because it is where the validator goes beyond schema-only checking.

The fourth stage applies minimal integrity checks. In the current repository, these checks are attached to the evidence block and ensure that the statement is not only structurally and semantically aligned, but also consistent with the minimal integrity material it declares. This is intentionally narrower than a complete cryptographic trust infrastructure. The method only claims minimal integrity checking for the statement surface defined by the profile.

Across these stages, the validator produces explicit error reporting. The report includes stage-level issues, total issue count, an overall `ok` flag, and a summary suitable for human inspection. This output model matters methodologically because it keeps failure conditions inspectable rather than burying them inside an implementation-specific exception path.

The staged design is also a methodological choice. It stabilizes the primary failure surface by checking prerequisite conditions first. A malformed statement should fail at structural conformance before the validator tries to interpret its cross-field relationships. A statement with unresolved local references should fail before the validator attempts deeper consistency checks. That ordering keeps the main failure category readable and aligns the validator with the boundary-oriented example design used in the repository.

## 5. Reference Validator and CLI Path

The reference validator is implemented in the current repository, primarily in `agent_evidence/oap.py`, with CLI exposure through `agent_evidence/cli/main.py`. This is important for the paper because the validator is not hypothetical. It is an executable reference path attached to the current artifact package.

At the implementation level, the validator loads a JSON profile payload, checks schema conformance, evaluates reference closure, evaluates consistency constraints, and applies minimal integrity checks over the declared evidence structure. The resulting report is machine-readable JSON. The CLI command `agent-evidence validate-profile <file>` exposes the same path as a command-line surface. This enables both interactive use and scripted integration. When validation fails, the command exits non-zero; when validation succeeds, it returns a passing report. The repository therefore provides not only validation logic but also a concrete validation interface.

The validator path is supported by repository-grounded artifacts. The examples under `examples/` provide controlled pass and fail cases. `tests/test_operation_accountability_profile.py` exercises the two valid examples, the five invalid examples, and the CLI JSON output path. The demo under `demo/run_operation_accountability_demo.py` shows the broader method loop in action: object load, profile precheck, operation execution, evidence generation, validation, and final report emission. These materials matter in the methods section only insofar as they show that the profile and validator are attached to an executable engineering path rather than to a purely textual specification.

The validator is described here as a reference validator rather than as a universal validator. The paper does not claim that the current implementation proves framework-agnostic behavior across multiple independent implementations. It claims something narrower: the repository provides one concrete validator path that makes the profile operational, inspectable, and reproducible.

## 6. Boundary of the Method

The boundary of the method should be stated explicitly. The profile does not model multi-step workflows. It does not provide a general registry. It does not attempt to solve full cross-ecosystem FDO mapping. It does not establish industrial deployment, full portability, or a complete trust infrastructure. It also does not claim that the current repository validates all possible operation-accountability cases. The method is intentionally smaller than those ambitions.

What it does claim is more precise. In the current repository, operation accountability has been reduced to a minimal verifiable profile with a profile-aware validation model and a concrete validator path. That path is grounded in specification, schema, examples, tests, a CLI surface, and a runnable demo. The value of the method is therefore not breadth, but closure: the current repository reduces the accountability object to a form that can be inspected and validated outside the original runtime context.

This boundary also clarifies the role of the comparative discussion summarized elsewhere in the paper and reflected in Table 1. Ordinary logs, provenance-oriented approaches, policy-only approaches, and audit trails each provide useful partial views. The present method does not claim to replace all of them. Its narrower claim is that, for single-operation accountability, a minimal verifiable profile can bind operation, policy, provenance, evidence, and validation into one object that can be checked and reproduced within the scope of the current repository.
