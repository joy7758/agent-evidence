# Discussion, Limits, and Threats to Validity

## 1. What the Paper Solves

The paper solves a narrow engineering problem: how to represent one operation accountability statement in a form that is specific enough to be checked outside the original runtime context. In the current repository, that means a minimal verifiable profile, a validator that enforces more than schema-only conformance, a small boundary-oriented example set, a CLI path, and a runnable demo. The contribution is therefore a closed method path for a single statement, not a broad framework for all accountability needs in agent systems.

This framing matters because the strength of the paper comes from closure rather than scale. The repository does not merely define a profile. It also ties the profile to a schema, examples, validator behavior, diagnostic codes, and a release-and-archive surface. That coherence is what the paper can defend directly from repository evidence.

## 2. Why the Scope Is Deliberately Minimal

The scope is deliberately minimal because operation accountability becomes difficult to evaluate when it is introduced only as a large architectural aspiration. By constraining the object to one operation statement, the paper keeps the method boundary clear enough to inspect. That makes it possible to reason concretely about fields, references, consistency rules, error codes, and reproducible paths.

This choice has an obvious cost: the method does not attempt to cover full workflow semantics, multi-agent orchestration, or broad ecosystem integration. The paper accepts that cost because a smaller method with an executable validation path is more defensible than a much broader design with weak artifact grounding.

## 3. What Current Repository Evidence Supports

The current repository evidence supports a focused set of claims. First, it supports the existence of a minimal verifiable profile centered on `operation`, `policy`, `provenance`, `evidence`, and `validation`. Second, it supports the existence of a profile-aware validation path that extends schema checking with reference closure, cross-field consistency, minimal integrity checks, and explicit error reporting. Third, it supports boundary-oriented example coverage through 2 valid examples and 5 invalid examples. Fourth, it supports a runnable method path through the CLI and the single-path demo. Fifth, it supports a modest portability statement through second-context reuse, as summarized by Table 4.

These claims remain intentionally narrow and are stated only to the extent supported by the current repository evidence. They are claims about what the current repository implements and exposes, not about what all FDO-based agent systems already do or should do.

## 4. What Current Repository Evidence Does Not Support

The current repository does not support broad cross-framework validation. It does not support claims about convergence across multiple independent implementations. It does not support industrial-scale deployment claims. It does not support claims about large workflow graphs, rich multi-agent coordination, or a full cryptographic trust infrastructure. It also does not support empirical superiority claims over logs, provenance-only approaches, policy-only approaches, or audit trails.

These non-claims therefore need to remain explicit. In particular, the portability language must remain modest. Table 4 supports limited evidence for basic portability, not general portability across frameworks or ecosystems. Similarly, the comparative argument is structural and scenario-grounded, not benchmark-based.

## 5. Threats to Validity

### 5.1 Construct Validity

The paper operationalizes operation accountability through one specific profile structure and one set of validation rules. That is a methodological choice. Readers who define accountability in terms of organizational governance, end-to-end compliance processes, or non-repudiation may find the paper's construct too narrow. The paper partially addresses this threat by stating the scope explicitly and by centering the argument on a single operation statement rather than on accountability in general.

### 5.2 Internal Validity

The profile, validator, examples, tests, and demo all come from the same repository. This supports internal coherence, but it also means that the rule designers and the reference implementation are not independent. The paper therefore cannot claim implementation independence. What it can claim is that the repository exposes a consistent path from specification to execution.

### 5.3 External Validity

External validity is limited in two ways. First, the current repository includes one core demo path, even though the example set now spans two passing contexts. Second, the portability evidence remains modest. The second valid example improves the situation by showing that the same profile and validator path can pass in a different controlled context, but Table 4 also makes clear that this is limited evidence for basic portability rather than broad cross-framework validation.

### 5.4 Artifact Validity

The paper depends on a repository-grounded artifact package, so artifact validity matters directly. The current repository is stronger here than in broader external validity because it already exposes a specification, schema, examples, tests, CLI path, demo, GitHub Release `v0.2.0`, and Zenodo DOI `10.5281/zenodo.19334062`. At the same time, the artifact story still depends on documentation consistency and the continued alignment between repository text, release text, and archive metadata. The artifact package is therefore best treated as supporting evidence, not as a reason to broaden claims elsewhere in the paper.

## 6. Appropriate Next Steps

The next steps should remain on the same mainline rather than expanding the research scope. The most appropriate extensions are additional controlled examples, stronger validator test coverage, and further tightening of the repository-facing artifact package. Those steps reinforce the current claim without turning the work into a broad survey or a general governance platform.

A different kind of future-work narrative should also be avoided: immediate inflation of the contribution into a full-stack accountability ecosystem. That is not what the current evidence supports. The disciplined path forward is to keep the profile boundary stable while thickening the evidence around the same minimal method.
