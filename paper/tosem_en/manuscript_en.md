# A Minimal Verifiable Profile for Operation Accountability in FDO-Based Agent Systems

## Abstract

FDO-based agent systems require more than execution traces when a single operation must be checked outside the original runtime context. They need a compact accountability statement that can specify which operation was performed on which digital object context, under which policy basis, with which input and output references, what evidence was produced, and how the statement can be independently validated. This paper presents a minimal verifiable profile for that purpose and grounds it in the current `agent-evidence` repository. The profile is intentionally narrow: it centers operation accountability and binds `operation`, `policy`, `provenance`, `evidence`, and `validation` into one portable, externally checkable statement while keeping only the supporting context needed for independent review. The repository provides a profile specification, a JSON Schema, two valid examples, five invalid examples, a profile-aware validator, a CLI entry point, tests, and a runnable single-path demo. The validator goes beyond structural schema checks to cover reference closure, cross-field consistency, and minimal integrity checks, and it produces machine-readable JSON reports, human-readable summaries, and explicit error codes. The current artifact package is anchored by GitHub Release `v0.2.0` and Zenodo DOI `10.5281/zenodo.19334062`. The paper does not claim broad cross-framework validation or industrial-scale deployment. Its claim is narrower: in the current repository context, operation accountability can be packaged as a minimal, testable, reproducible, and archivable engineering unit.

## Keywords

- FDO-based agent systems
- operation accountability
- provenance
- execution evidence
- profile-aware validation
- JSON Schema
- software artifact

## 1. Introduction

Software systems built around AI agents are increasingly able to emit logs, traces, and runtime events at high volume. Those materials are useful for debugging, observability, and post hoc inspection. In FDO-based agent systems, however, a narrower and harder question often remains unresolved: for one concrete operation, which operation was performed on which digital object context, under which policy constraints, through which input and output references, with what evidence, and through what validation path? In other words, it is not enough to know that an execution happened. A third party may need a compact statement that can be packaged, checked, and archived as an accountability unit for a single operation.

That gap is the starting point of this paper. The problem addressed here is not general AI governance, broad compliance automation, or a full ecosystem mapping for all FDO variants. The problem is smaller and more concrete. Given a single operation in an FDO-based agent system, can we represent its accountability conditions in a minimal form that is still independently verifiable? The repository behind this paper addresses that question through a deliberately constrained engineering path: a minimal profile, a profile-aware validator, a small boundary-oriented example suite, a CLI entry point, a runnable demo, and a release-and-archive surface. The aim is not breadth. The aim is to turn operation accountability from a loose narrative into a testable software artifact.

The need for such a minimal artifact becomes clearer when common alternatives are considered. Ordinary logs can record timestamps, events, paths, and fragments of execution state, but they do not usually form a stable accountability object. They are often distributed across system components, shaped by runtime convenience rather than portability, and weak in explicit policy binding. Provenance-oriented representations can describe derivation links and object relationships more clearly, but provenance alone does not necessarily say under which governing policy the operation was performed, what the minimal evidence block is, or how an external validator should classify failures. Policy-only representations can state constraints and allowed actions, but they do not establish what actually happened for a particular operation, whether input and output references close locally, or whether the statement is independently verifiable. These alternatives are partial capability holders. The narrower claim of this paper is that operation accountability benefits from a minimal unit that binds these dimensions together rather than leaving them split across unrelated surfaces.

The paper therefore adopts a minimal-profile approach. The current repository implements `Execution Evidence and Operation Accountability Profile v0.1`, organized around five fixed parts: `operation`, `policy`, `provenance`, `evidence`, and `validation`. Around those core parts, the profile retains only the supporting context needed to make the statement checkable, such as `actor`, `subject`, `constraints`, `profile`, and `timestamp`. This design is intentionally restrictive. It does not attempt to absorb every metadata field that future governance workflows might request. It does not attempt to model large workflows or multi-agent coordination. Instead, it treats a single operation accountability statement as the primary engineering object and asks what minimum structure is needed for independent verification.

That emphasis on verification shapes the validator as well. In the current repository, validation is not reduced to a schema pass. The validator, implemented in `agent_evidence/oap.py` and exposed through `agent_evidence/cli/main.py`, performs staged checks over the profile. It first checks structural conformance against the expected shape. It then checks local reference closure. It continues with cross-field consistency among policy, provenance, and evidence links. Finally, it applies minimal integrity checks. The output is a validation report with machine-readable JSON, a human-readable summary, and explicit error codes. This is why the validator is described as profile-aware: it does not merely parse a JSON document; it enforces the identity, linkage, and consistency rules defined for this profile.

The current repository provides grounded evidence for this claim in a form suitable for a methodology-plus-artifact paper. At the time of writing, the repository contains a profile specification, a JSON Schema, two valid examples, and five invalid examples. The invalid examples are intentionally minimal: each breaks one primary rule so that failure categories remain readable and diagnosable. The two valid examples are also informative beyond simple pass cases. One represents a metadata enrichment context with a single input and a single output. The other represents a retention review context with two inputs and one decision output. Both pass under the same profile model and the same validator path. That does not establish broad cross-framework validation, but it does provide limited evidence for basic portability and a second-context validity check for the same minimal structure.

The artifact surface is broader than the profile files alone. The repository includes tests that exercise the valid and invalid examples, the CLI path, and the validator entry points. It also includes a runnable single-path demo that proceeds from object load or creation, through profile precheck and operation execution, to evidence generation and final validation output. Beyond the repository tree, the current artifact package is anchored by GitHub Release `v0.2.0` and Zenodo DOI `10.5281/zenodo.19334062`. Those anchors do not prove superiority over alternative approaches, but they matter for a software engineering paper because they show that the work is packaged as a releasable, citable, and archivable artifact rather than a purely conceptual proposal.

This paper makes four concrete contributions. First, it defines a minimal verifiable profile for single-operation accountability in FDO-based agent systems, centered on `operation`, `policy`, `provenance`, `evidence`, and `validation`. Second, it presents a profile-aware validation approach that extends structural schema checking with reference closure, cross-field consistency, and explicit error reporting. Third, it provides a boundary-oriented example suite with two valid examples and five single-rule invalid examples, making both passing and failing conditions inspectable. Fourth, it packages these elements into a reproducible artifact package spanning specification, schema, examples, validator, CLI, tests, demo, release, and DOI.

The scope of the paper is deliberately minimal, and that point is important for correct evaluation. The paper does not claim a universal FDO standard. It does not claim full support for complex multi-agent orchestration. It does not claim a complete cryptographic trust infrastructure, non-repudiation, or organizational compliance automation. It also does not claim broad empirical validation across frameworks or implementations. The current evidence is narrower: a single profile model, a single repository implementation, two valid contexts, five invalid boundary cases, a validator path, a CLI surface, a runnable demo, and an artifact package with release-and-archive anchors. The argument of the paper should be read at that scale.

That restraint keeps the contribution aligned with a methodology-, validator-, and artifact-oriented software engineering paper. The repository does not try to win by scope inflation. Instead, it closes a small loop end to end. The specification, JSON Schema, validator path, example suite, CLI, demo, and release-and-archive anchors make that loop directly inspectable in the current repository. The comparative argument is similarly restrained. In the paper, ordinary logs, provenance-only representations, and policy-only representations are not dismissed; they are treated as partial representations that do not by themselves form the same minimal accountability unit. The intended contribution is therefore not a sweeping survey claim, but a concrete engineering claim about what has been implemented as a reproducible, verifiable object in the current repository.

The rest of the paper follows that structure. It first defines the problem and the design goals that motivate a deliberately minimal profile. It then presents the profile model, the validation model, and the reference validator. Next, it describes the artifact package and evaluates the current evidence through examples, tests, CLI behavior, demo execution, and release packaging. Finally, it discusses limits, threats to validity, and the boundary between the current basic portability evidence and the broader claims that the present repository does not yet support.

## 2. Contributions and Scope

### Contributions

1. We define a minimal verifiable profile for single-operation accountability in FDO-based agent systems, centered on `operation`, `policy`, `provenance`, `evidence`, and `validation`.
2. We provide a profile-aware validation approach that extends structural schema checking with reference closure, cross-field consistency, and explicit error reporting.
3. We ground the method with a boundary-oriented example suite consisting of two valid examples and five invalid examples, making both passing and failing conditions inspectable.
4. We package the method as a reproducible artifact package comprising the profile specification, JSON Schema, examples, validator, CLI, tests, demo, GitHub Release `v0.2.0`, and Zenodo DOI `10.5281/zenodo.19334062`.

### Scope Boundary

This paper does not claim broad cross-framework validation, industrial-scale deployment, a complete governance platform, or a universal FDO standard. Its scope is deliberately minimal: one profile model, one validator path, one artifact package, two valid contexts, and five invalid boundary cases.

## 3. Methods: Minimal Profile and Profile-Aware Validation

### 3.1 Problem Setting and Design Goals

The method proposed in this paper addresses a narrow software-engineering problem: how to represent one operation accountability statement in an FDO-based agent system so that a third party can inspect it outside the original runtime context. The target object is deliberately small. It is not a workflow graph, not a registry, and not a general governance model. It is a single statement about one operation on one digital object context.

In the current repository, that statement must support at least the following questions in a checkable form: which operation was performed, on which subject object, under which policy basis and constraints, through which input and output references, with what evidence, and through what validation path. This framing is narrower than general observability and narrower than broad compliance automation. The point is to isolate the smallest unit that can still be specified, validated, tested, demonstrated, and archived as a software artifact.

This problem framing leads to five design goals. First, the method should be minimal rather than complete. The profile should retain only the fields needed to support a minimal accountability loop. Second, it should be verifiable rather than merely descriptive. A JSON object is not sufficient unless it can be checked by a validator that enforces profile-specific rules. Third, it should reuse the current repository surface rather than introduce a second implementation stack. Fourth, it should be artifact-oriented, meaning that the method must remain connected to examples, tests, a CLI entry point, and a runnable demo. Fifth, it should stay grounded in an FDO-based object setting without expanding into a broad FDO overview or claiming full coverage of all FDO variants.

These goals imply several explicit tradeoffs. The method uses a profile instead of a platform, staged validation instead of a maximal all-errors-at-once strategy, and a single-path demo instead of a large scenario suite. The resulting scope is intentionally constrained: a minimal verifiable profile, a profile-aware validator, and a repository-grounded artifact package.

### 3.2 Minimal Verifiable Profile

The current repository defines `execution-evidence-operation-accountability-profile` version `0.1`. The profile describes one operation accountability statement. At the top level, the statement contains `profile`, `statement_id`, `timestamp`, `actor`, `subject`, `operation`, `policy`, `constraints`, `provenance`, `evidence`, and `validation`. Within that top-level structure, the methodological core of the paper is the five-part organization of `operation`, `policy`, `provenance`, `evidence`, and `validation`.

The profile is minimal in three senses. It is minimal in problem scope because it covers only a single operation statement. It is minimal in field scope because it retains only the fields needed to support independent checking. It is minimal in validation scope because it does not try to establish a full trust fabric; it only requires the checks needed to make the statement externally inspectable.

This design can be seen as a disciplined reduction of the accountability problem. Instead of attempting to capture every future governance need, the profile isolates one portable statement and requires that all critical accountability links remain local to that statement. The repository specification makes the reduction explicit by fixing the profile identity and version, enumerating required fields, and defining field relationships that the validator must enforce.

[Insert Fig. 2 here]

Figure 2 summarizes that structure. `operation` is placed at the center because the paper treats operation accountability, not actor identity alone or policy expression alone, as the primary engineering object. The other four components are arranged around it because they bind the surrounding conditions needed to make one operation externally checkable.

### 3.3 Role of the Five Components

The five core components are not a feature inventory. They are the minimum set of responsibilities that must be co-located if a third party is expected to inspect one accountability statement without reconstructing context from unrelated system surfaces.

`operation` is the accountability center. It identifies the action, its type, its input and output references, and its result status and summary. In the current design, this is the component that answers the core question of what happened. The profile treats `operation` as the organizing object because the paper is concerned with single-operation accountability rather than general event logging.

`policy` captures the governing rule basis for the statement. It identifies the policy and the concrete constraints that the policy references. This component is necessary because an operation record without an explicit policy basis is often insufficient for accountability review. The method therefore requires policy binding to be first-class rather than left to surrounding documentation or external runtime context.

`provenance` connects `actor`, `subject`, `operation`, and the input and output references. Its role is not to replace richer provenance models, but to provide the minimum linkage needed to make the statement traceable as a local object. In the current profile, provenance is valuable precisely because it anchors the operation to a subject and to specific references rather than leaving these relationships implicit.

`evidence` contains the referenced materials that support the statement. In the current repository, this includes local references, artifacts, and integrity-related material. The method does not assume that a log stream or an artifact store elsewhere can stand in for this component. Instead, it requires that the statement carry a minimal evidence block of its own.

`validation` identifies how an external checker should inspect the statement. It records the relevant local objects, the validation method, the validator identity, and the validation status. This component matters because the method is not satisfied with merely describing the operation. It also wants to make the checking path explicit.

The remaining top-level fields support these five components without enlarging the method beyond its minimal scope. `actor` and `subject` provide the executor and the object context. `constraints` make policy references resolvable locally. `statement_id`, `timestamp`, and `profile` make the statement stable and versioned as an independent artifact.

The repository specification further fixes the link rules among these parts. For example, `operation.subject_ref` must equal `subject.id`; `operation.policy_ref` must equal `policy.id`; policy constraint references must resolve to local constraints; operation input and output references must resolve to evidence references; provenance references must match the corresponding actor, subject, and operation identifiers; and validation references must resolve to the local evidence, provenance, and policy objects. These rules explain why the method is described as a minimal verifiable profile rather than a loose schema template.

### 3.4 Validation Model

The validation model is designed to enforce the profile as an executable boundary rather than as a descriptive data shape. Conceptually, the method uses a two-layer validation logic, reflected in Figure 6. Structural conformance comes first. Accountability conformance follows. In the current repository implementation, that logic is realized as four ordered stages: schema checks, reference closure checks, cross-field consistency checks, and minimal integrity checks.

[Insert Fig. 6 here]

The first stage checks structural conformance. This includes required fields, field shape, and schema-level completeness. In the implementation, this stage is grounded in the JSON Schema and yields errors such as `schema_violation`. Structural conformance is necessary because the later stages depend on predictable field locations and types.

The second stage checks reference closure. This stage verifies that local references actually resolve to local identifiers. It covers constraint references, evidence reference identifiers, operation input and output references, and local references in provenance, evidence, and validation. It also detects duplicate identifiers where applicable. The point of this stage is to prevent a statement from looking complete while still relying on missing local objects.

The third stage checks cross-field consistency. Here the validator enforces the profile-specific semantic relationships among the five core components. Examples include checking whether provenance input and output references match the operation input and output references, whether policy-related references remain aligned across `operation`, `evidence`, and `validation`, and whether input and output roles are used consistently. This stage is central to the method because it is where the validator goes beyond schema-only checking.

The fourth stage applies minimal integrity checks. In the current repository, these checks are attached to the evidence block and ensure that the statement is not only structurally and semantically aligned, but also consistent with the minimal integrity material it declares. This is intentionally narrower than a complete cryptographic trust infrastructure. The method only claims minimal integrity checking for the statement surface defined by the profile.

Across these stages, the validator produces explicit error reporting. The report includes stage-level issues, total issue count, an overall `ok` flag, and a summary suitable for human inspection. This output model matters methodologically because it keeps failure conditions inspectable rather than burying them inside an implementation-specific exception path.

The staged design is also a methodological choice. It stabilizes the primary failure surface by checking prerequisite conditions first. A malformed statement should fail at structural conformance before the validator tries to interpret its cross-field relationships. A statement with unresolved local references should fail before the validator attempts deeper consistency checks. That ordering keeps the main failure category readable and aligns the validator with the boundary-oriented example design used in the repository.

### 3.5 Reference Validator and CLI Path

The reference validator is implemented in the current repository, primarily in `agent_evidence/oap.py`, with CLI exposure through `agent_evidence/cli/main.py`. This is important for the paper because the validator is not hypothetical. It is an executable reference path attached to the current artifact package.

At the implementation level, the validator loads a JSON profile payload, checks schema conformance, evaluates reference closure, evaluates consistency constraints, and applies minimal integrity checks over the declared evidence structure. The resulting report is machine-readable JSON. The CLI command `agent-evidence validate-profile <file>` exposes the same path as a command-line surface. This enables both interactive use and scripted integration. When validation fails, the command exits non-zero; when validation succeeds, it returns a passing report. The repository therefore provides not only validation logic but also a concrete validation interface.

The validator path is supported by repository-grounded artifacts. The examples under `examples/` provide controlled pass and fail cases. `tests/test_operation_accountability_profile.py` exercises the two valid examples, the five invalid examples, and the CLI JSON output path. The demo under `demo/run_operation_accountability_demo.py` shows the broader method loop in action: object load, profile precheck, operation execution, evidence generation, validation, and final report emission. These materials matter in the methods section only insofar as they show that the profile and validator are attached to an executable engineering path rather than to a purely textual specification.

The validator is described here as a reference validator rather than as a universal validator. The paper does not claim that the current implementation proves framework-agnostic behavior across multiple independent implementations. It claims something narrower: the repository provides one concrete validator path that makes the profile operational, inspectable, and reproducible.

### 3.6 Boundary of the Method

The boundary of the method should be stated explicitly. The profile does not model multi-step workflows. It does not provide a general registry. It does not attempt to solve full cross-ecosystem FDO mapping. It does not establish industrial deployment, full portability, or a complete trust infrastructure. It also does not claim that the current repository validates all possible operation-accountability cases. The method is intentionally smaller than those ambitions.

What it does claim is more precise. In the current repository, operation accountability has been reduced to a minimal verifiable profile with a profile-aware validation model and a concrete validator path. That path is grounded in specification, schema, examples, tests, a CLI surface, and a runnable demo. The value of the method is therefore not breadth, but closure: the current repository reduces the accountability object to a form that can be inspected and validated outside the original runtime context.

This boundary also clarifies the role of the comparative discussion summarized elsewhere in the paper and reflected in Table 1. Ordinary logs, provenance-oriented approaches, policy-only approaches, and audit trails each provide useful partial views. The present method does not claim to replace all of them. Its narrower claim is that, for single-operation accountability, a minimal verifiable profile can bind operation, policy, provenance, evidence, and validation into one object that can be checked and reproduced within the scope of the current repository.

## 4. Evaluation

### 4.1 Evaluation Goals and Research Questions

The evaluation in this paper is intentionally restrained. It does not report large-scale benchmarks, framework comparisons, or user studies, because the current repository does not provide evidence for those claims. Instead, the evaluation asks a smaller set of questions that match the paper's scope as a methodology-, validator-, and artifact-oriented software engineering study.

The first question is whether the current repository exercises the profile boundary through controlled passing and failing examples. The second is whether the validator currently provides detectable and inspectable failure categories rather than opaque rejection. The third is whether the repository supports a limited portability claim for the same minimal profile across more than one context. The fourth is what this evidence does not yet establish.

Under this framing, the evaluation is closer to conformance checking, boundary coverage inspection, diagnostic usefulness, and artifact sanity checking than to a broad empirical performance study. That limitation is not hidden; it is part of the paper's methodological position [@knublauch2017shacl; @wright2022jsonschemavalidation].

### 4.2 Boundary Coverage over Valid and Invalid Examples

The current repository provides a compact but structured validation boundary: 2 valid examples and 5 invalid examples. The valid examples show passing conditions for the profile. The invalid examples show controlled violations in which each file is designed to break one primary rule. This setup is central to the evaluation because it lets the paper talk about the behavior of the validator at the boundary of the method rather than only in a nominal success path.

[Insert Table 3 here]

Table 3 summarizes the currently grounded example set and the current evidence source for each case. The two valid examples are `minimal-valid-evidence.json` and `valid-retention-review-evidence.json`. The first uses a metadata enrichment context with a single input and a single output. The second uses a retention review context with two inputs and one decision output. Both are important because they show that the same minimal profile can pass in more than one controlled context.

The five invalid examples cover a small but meaningful range of failure modes. `invalid-missing-required.json` breaks required-field completeness by removing `validation.method`. `invalid-unclosed-reference.json` breaks reference closure by introducing an unresolved output reference. `invalid-policy-link-broken.json` breaks policy/evidence linkage consistency. `invalid-provenance-output-mismatch.json` breaks a provenance/operation cross-field binding. `invalid-validation-provenance-link-broken.json` breaks validation/provenance reference closure. Because these failures are single-rule violations, they help keep the main failure category readable and tied to the design of the profile.

This example design does not establish exhaustive failure coverage. It does, however, support the narrower claim that the repository currently exercises the main validation surface through both passing and failing cases. That distinction matters. The paper is not arguing that every possible failure has been enumerated. It is arguing that the boundary of the current method is concrete enough to be probed and reported.

### 4.3 Failure Detectability and Diagnostic Usefulness

Boundary coverage is only useful if failures are detectable and interpretable. In the current repository, the validator supports that requirement in two ways: through structured reports and through explicit main error codes.

The reference path under `tests/test_operation_accountability_profile.py` checks that the two valid examples pass and that each invalid example fails with its expected primary code. The currently exercised codes include `schema_violation`, `unresolved_output_ref`, `unresolved_evidence_policy_ref`, `provenance_output_refs_mismatch`, and `unresolved_validation_provenance_ref`. This does not prove a complete failure taxonomy, but it does show that the repository already associates controlled failure modes with stable diagnostic labels.

The CLI path strengthens this point because validation is not confined to internal function calls. The command `agent-evidence validate-profile <file>` returns a machine-readable JSON report and supports non-zero exit behavior on failure. In other words, the failure diagnostics are not merely implementation details inside the test suite; they are exposed through the reference command surface. Table 3 captures this distinction by recording whether the current evidence for each example comes from tests, CLI use, or both.

The current repository also includes a runnable demo path in `demo/run_operation_accountability_demo.py`. The demo is not a separate evaluation benchmark, but it matters because it closes the loop from object load or creation through profile precheck, operation execution, evidence generation, and final validation output. In the evaluation context, that demo helps show that the validator is integrated into a method path rather than attached as an isolated checker.

Taken together, these materials support a modest diagnostic claim: the current repository can not only reject malformed or inconsistent statements, but can do so in a way that remains inspectable through stage-level reporting, explicit primary codes, and human-readable summaries. The evaluation does not claim that these diagnostics have been validated through usability studies or external reviewer trials. It claims only that the current repository already exposes a readable diagnostic surface.

### 4.4 Comparative Case Observation

The paper includes one qualitative comparative observation based on a single repository-grounded scenario: the retention review example represented by `valid-retention-review-evidence.json`. This comparison is not an experiment. It is a structural contrast used to anchor the paper's method discussion and the qualitative claims summarized in Table 1.

[Insert Table 1 here]

In that scenario, ordinary logs can record events, messages, and execution fragments [@oliner2012loganalysis], but they do not by themselves form a stable accountability statement. Provenance-oriented representations can describe linkage among objects more clearly [@moreau2013provdm], but they do not necessarily carry an explicit policy basis, a minimal evidence block, and a fixed validation path in the same local statement. Policy-oriented representations can describe the governing rule basis [@iannella2018odrl], but in the setting studied here they do not by themselves establish a minimal executed operation-accountability object because policy, provenance, evidence, and validation remain unbound.

The minimal verifiable profile proposed in this paper does not invalidate those partial views. Rather, it binds the minimum accountability conditions that those views leave separated: operation, policy, provenance, evidence, and validation. The evaluation claim is therefore limited and qualitative. The current repository supports a structural comparison showing why the method is different from ordinary logs, provenance-only expressions, and policy-only expressions. It does not support an experimental superiority claim over any of them.

### 4.5 Limited Evidence for Basic Portability

The current repository includes only modest portability evidence, and the paper should state that directly. The relevant evidence comes from the two valid examples, which reuse the same profile model and the same validator path while differing in context and reference pattern.

[Insert Table 4 here]

Table 4 organizes that evidence into a small portability matrix. The first point is context diversity: one valid example represents metadata enrichment, while the second represents retention review. The second point is linkage-pattern diversity: one valid example uses a single-input/single-output pattern, and the other uses a two-input/one-output pattern. The third point is validator reuse: both examples pass under the same profile identity and the same validation path. The fourth point is field-model reuse: both examples preserve the same core organization of operation, policy, provenance, evidence, and validation.

What this supports is a narrow claim of basic portability evidence. The same minimal profile is not confined to one hand-crafted passing case. It can also pass in a second controlled context with a different input/output linkage pattern. That is useful evidence for the paper because it reduces the risk that the method appears tailored to a single illustrative example.

What this evidence does not support is equally important. It does not establish broad cross-framework validation. It does not establish convergence across multiple independent implementations. It does not establish support for large workflow graphs, complex object networks, or multi-agent coordination. The point of Table 4 is therefore not to inflate the portability claim, but to stabilize it at the level the repository can actually support.

### 4.6 Current Evaluation Limits

The current evaluation remains bounded by the repository that implements the method. First, all evidence comes from one implementation stack. That strengthens internal consistency but limits external validity. Second, the repository includes only one core demo path, even though the example set now contains two passing contexts. Third, the comparison to logs, provenance-only representations, and policy-only representations is structural and scenario-grounded rather than experimental. Fourth, the evaluation does not include performance results, user studies, or broad framework comparisons.

These limits should not be blurred in the submission draft. The current evidence supports the following narrow claims: the profile boundary is exercised through 2 valid and 5 invalid examples; the validator exposes explicit failure diagnostics; the CLI and test path make those diagnostics reproducible; the demo closes the minimal loop; and the second valid example provides limited evidence for basic portability. The current evidence does not support claims of broad portability, industrial deployment, empirical superiority over alternative approaches, or large-scale operational validation.

In summary, the evaluation supports a small but coherent argument. The current repository evidence covers conformance, boundary-oriented example coverage, diagnosable failure cases, a runnable validation path, and limited second-context reuse. These results support the paper's methodological, validation, and artifact claims. They do not support a broader empirical generalization, and the paper states that limit explicitly.

## 5. Related Work

### 5.1 Ordinary Logs and Audit Trails

Ordinary logs and audit trails are natural comparison points because they already play an important role in software operations. Logs are useful for debugging, observability, and post hoc reconstruction of runtime behavior. Audit trails can go further by collecting structured records of actions, timestamps, and actors within an application or platform boundary. For many engineering tasks, these materials are entirely appropriate [@kent2006sp80092; @oliner2012loganalysis].

The problem addressed in this paper, however, is narrower and more specific. A single operation accountability statement must remain inspectable outside the original runtime context. In the retention review scenario used elsewhere in the paper, logs can record that a review occurred, which files or objects were touched, and which components emitted output. Audit trails can often do more, especially when an application already maintains structured action histories. Yet neither logs nor audit trails necessarily reduce the event into one local object that explicitly binds the operation, the governing policy basis, the relevant input and output references, the supporting evidence, and the validation path.

This distinction is why the paper treats logs and audit trails as partial capability holders rather than as strawman alternatives. They can preserve useful execution traces and operational history. What they do not necessarily provide is the same minimal accountability object targeted here: one statement that can be checked as a self-contained unit by an external validator. Table 1 summarizes that difference at the method level, while the retention review comparison provides a scenario-grounded reading of it.

### 5.2 Provenance-Oriented Approaches

Provenance-oriented approaches are closer to the present work because they already focus on linkage among entities, activities, and derived objects. In the current problem setting, provenance is essential: without an explicit link between the operation, the subject, and the referenced inputs and outputs, an accountability statement risks becoming only a descriptive wrapper around unrelated metadata [@moreau2013provdm; @herschel2017surveyprovenance].

At the same time, provenance alone is not the same thing as operation accountability in the sense defined by this paper. Provenance can explain how objects are related, how outputs derive from inputs, and how an action participates in a chain of derivation. That is valuable, and the present profile depends on it. But provenance-oriented representations do not necessarily carry the full minimum set of conditions that this paper keeps together in one statement. In particular, they may leave the governing policy basis external, treat evidence artifacts as surrounding context rather than as part of the statement core, or omit an explicit validation object and validator path.

The current method therefore does not compete with provenance as such. It relies on provenance as one of its five core components. The point of difference is compositional: provenance is necessary but not sufficient for the minimal accountability object proposed here. The paper's contribution is to keep provenance fixed together with policy, evidence, and validation so that the statement can be independently checked as one unit rather than reconstructed across several surfaces.

### 5.3 Policy-Oriented Approaches

Policy-oriented approaches address a different but closely related problem. They can define what is allowed, what constraints apply, and what rule basis governs a given class of operations [@iannella2018odrl; @hu2014abac]. In the retention review scenario, this corresponds to statements about approved retention classes, escalation rules, and other rule-level conditions under which the operation should be performed.

From the perspective of this paper, policy information is indispensable but incomplete when used alone. A policy can describe what should happen, but it does not by itself establish what did happen in one concrete operation. In the setting studied here, a policy-oriented representation therefore does not by itself establish a minimal executed operation-accountability object, because policy, provenance, evidence, and validation remain unbound.

This is why the proposed profile treats policy as a first-class component rather than as external documentation. The method does not diminish the role of policy. It narrows it and binds it to one operation statement so that a review can inspect the policy basis and the executed statement in the same object. In the comparative case logic used in this paper, policy-only representations remain partial capability holders because they do not by themselves form the same minimal accountability unit.

### 5.4 Profile-, Conformance-, and Validation-Oriented Approaches

The closest conceptual neighbors to this paper are profile-, conformance-, and validation-oriented approaches. These approaches matter because the present work does not stop at data modeling. It also defines what a conforming statement must contain and how non-conforming statements should fail [@atkinson2019profiles; @knublauch2017shacl; @wright2022jsonschemavalidation].

A profile-oriented view matters here because the paper is not proposing an unconstrained JSON format. It fixes a narrow object model, a fixed identity and version, and a defined set of field relationships. A conformance-oriented view matters because the method requires statements to be checked against more than a structural schema. A validation-oriented view matters because the repository includes a concrete reference validator and a CLI path rather than only a specification document.

This is also where the paper differs from generic schema checking. A schema can enforce field presence and field shape, but it does not automatically enforce the full local semantics of the profile. In the current repository, the validator checks structural conformance, reference closure, cross-field consistency, and explicit failure reporting. That design places the work closer to profile-aware conformance checking than to generic document validation [@wright2022jsonschema; @wright2022jsonschemavalidation].

The paper's claim remains narrow. It does not claim to settle a general theory of profile conformance for all FDO-based systems. It claims that, for one operation accountability statement, a minimal verifiable profile and a profile-aware validator can be specified, implemented, and packaged together. In relation to the other categories discussed above, the contribution is therefore not that policy, provenance, logs, or audit trails are unnecessary. The contribution is that the current repository binds the minimum needed slices of these concerns into one accountability object that can be checked, reproduced, and archived as a software artifact.

## 6. Discussion, Limits, and Threats to Validity

### 6.1 What the Paper Solves

The paper solves a narrow engineering problem: how to represent one operation accountability statement in a form that is specific enough to be checked outside the original runtime context. In the current repository, that means a minimal verifiable profile, a validator that enforces more than schema-only conformance, a small boundary-oriented example set, a CLI path, and a runnable demo. The contribution is therefore a closed method path for a single statement, not a broad framework for all accountability needs in agent systems.

This framing matters because the strength of the paper comes from closure rather than scale. The repository does not merely define a profile. It also ties the profile to a schema, examples, validator behavior, diagnostic codes, and a release-and-archive surface. That coherence is what the paper can defend directly from repository evidence.

### 6.2 Why the Scope Is Deliberately Minimal

The scope is deliberately minimal because operation accountability becomes difficult to evaluate when it is introduced only as a large architectural aspiration. By constraining the object to one operation statement, the paper keeps the method boundary clear enough to inspect. That makes it possible to reason concretely about fields, references, consistency rules, error codes, and reproducible paths.

This choice has an obvious cost: the method does not attempt to cover full workflow semantics, multi-agent orchestration, or broad ecosystem integration. The paper accepts that cost because a smaller method with an executable validation path is more defensible than a much broader design with weak artifact grounding.

### 6.3 What Current Repository Evidence Supports

The current repository evidence supports a focused set of claims. First, it supports the existence of a minimal verifiable profile centered on `operation`, `policy`, `provenance`, `evidence`, and `validation`. Second, it supports the existence of a profile-aware validation path that extends schema checking with reference closure, cross-field consistency, minimal integrity checks, and explicit error reporting. Third, it supports boundary-oriented example coverage through 2 valid examples and 5 invalid examples. Fourth, it supports a runnable method path through the CLI and the single-path demo. Fifth, it supports a modest portability statement through second-context reuse, as summarized by Table 4.

These claims remain intentionally narrow and are stated only to the extent supported by the current repository evidence. They are claims about what the current repository implements and exposes, not about what all FDO-based agent systems already do or should do.

### 6.4 What Current Repository Evidence Does Not Support

The current repository does not support broad cross-framework validation. It does not support claims about convergence across multiple independent implementations. It does not support industrial-scale deployment claims. It does not support claims about large workflow graphs, rich multi-agent coordination, or a full cryptographic trust infrastructure. It also does not support empirical superiority claims over logs, provenance-only approaches, policy-only approaches, or audit trails.

These non-claims therefore need to remain explicit. In particular, the portability language must remain modest. Table 4 supports limited evidence for basic portability, not general portability across frameworks or ecosystems. Similarly, the comparative argument is structural and scenario-grounded, not benchmark-based.

### 6.5 Threats to Validity

#### Construct Validity

The paper operationalizes operation accountability through one specific profile structure and one set of validation rules. That is a methodological choice. Readers who define accountability in terms of organizational governance, end-to-end compliance processes, or non-repudiation may find the paper's construct too narrow. The paper partially addresses this threat by stating the scope explicitly and by centering the argument on a single operation statement rather than on accountability in general.

#### Internal Validity

The profile, validator, examples, tests, and demo all come from the same repository. This supports internal coherence, but it also means that the rule designers and the reference implementation are not independent. The paper therefore cannot claim implementation independence. What it can claim is that the repository exposes a consistent path from specification to execution.

#### External Validity

External validity is limited in two ways. First, the current repository includes one core demo path, even though the example set now spans two passing contexts. Second, the portability evidence remains modest. The second valid example improves the situation by showing that the same profile and validator path can pass in a different controlled context, but Table 4 also makes clear that this is limited evidence for basic portability rather than broad cross-framework validation.

#### Artifact Validity

The paper depends on a repository-grounded artifact package, so artifact validity matters directly. The current repository is stronger here than in broader external validity because it already exposes a specification, schema, examples, tests, CLI path, demo, GitHub Release `v0.2.0`, and Zenodo DOI `10.5281/zenodo.19334062`. At the same time, the artifact story still depends on documentation consistency and the continued alignment between repository text, release text, and archive metadata. The artifact package is therefore best treated as supporting evidence, not as a reason to broaden claims elsewhere in the paper.

### 6.6 Appropriate Next Steps

The next steps should remain on the same mainline rather than expanding the research scope. The most appropriate extensions are additional controlled examples, stronger validator test coverage, and further tightening of the repository-facing artifact package. Those steps reinforce the current claim without turning the work into a broad survey or a general governance platform.

A different kind of future-work narrative should also be avoided: immediate inflation of the contribution into a full-stack accountability ecosystem. That is not what the current evidence supports. The disciplined path forward is to keep the profile boundary stable while thickening the evidence around the same minimal method.

## 7. Conclusion

This paper advances a deliberately narrow claim. It does not propose a general governance platform for FDO-based agent systems. It proposes a minimal verifiable profile for single-operation accountability, together with a profile-aware validator and a repository-grounded artifact package. In the current repository, that claim is supported by the profile specification, the JSON Schema, 2 valid examples, 5 invalid examples, the validator and CLI path, a runnable single-path demo, GitHub Release `v0.2.0`, and Zenodo DOI `10.5281/zenodo.19334062`.

This work reduces operation accountability to a form that can be specified, checked, reproduced, and archived before broader system claims are made. The paper therefore argues for a small engineering object with explicit links among `operation`, `policy`, `provenance`, `evidence`, and `validation`, rather than for a broad theory of accountability across all agent-system settings.

What the paper does not claim is equally important. It does not claim broad cross-framework validation, industrial deployment, complete workflow coverage, or a full cryptographic trust infrastructure. The current repository evidence supports a narrower conclusion: one operation accountability statement can be represented as a minimal verifiable profile with a concrete validation path and a reproducible artifact package.

Near-term follow-on work should remain on the same mainline: add a small number of controlled examples, strengthen validator tests, complete the remaining citation and packaging cleanup, and keep the profile boundary stable while the evidence base is thickened. The next step is not to inflate the scope into a broad governance framework, but to reinforce the same minimal profile, validator, and artifact package with incrementally stronger repository-grounded evidence.
