# Reviewer Positioning

## One-Sentence Position

This is a method and artifact paper showing how OpenTelemetry-style agent
telemetry can be transformed into validator-checkable EEOAP operation evidence
without defining a new profile.

## What the Paper Is

- An adapter paper.
- A mapping paper.
- A local artifact and evaluation paper.
- A bounded demonstration that one valid trace can become an
  EEOAP-compatible operation accountability statement.
- A negative-case evaluation showing four adapter diagnostic surfaces:
  `missing_agent_span`, `unresolved_tool_span`,
  `broken_parent_span_relation`, and `missing_operation_name`.

## What the Paper Is Not

- Not a new EEOAP profile paper.
- Not a second EEOAP definition paper.
- Not an AEP replacement.
- Not a general agent governance framework.
- Not a legal accountability proof.
- Not a cross-framework comparison.
- Not a general OpenTelemetry compatibility study.
- Not a claim that agent outputs are correct.

## Distinction from Earlier EEOAP Work

Earlier EEOAP work defines and validates the target operation accountability
statement shape. This paper assumes that target exists and shows how an
external telemetry source can enter it.

The novelty is not a new statement schema. The novelty is the bounded bridge:

```text
OpenTelemetry-style trace
-> adapter
-> EEOAP v0.1 statement
-> existing EEOAP validator
```

## Distinction from AEP

AEP is broader evidence-object and artifact work in the repository. This paper
does not create an AEP profile, media bundle, release pack, or broad artifact
framework. It targets the EEOAP v0.1 validator path and uses
OpenTelemetry-style GenAI traces as input.

## How to Present the Ruff Issue

The paper should state that full-repository ruff is currently not a clean
artifact-wide signal because unrelated pre-existing lint debt exists in
out-of-scope directories such as `pd-oap/`.

The adapter should be defended with the narrower evidence:

- scoped adapter tests passed;
- full pytest passed;
- generated statement passed the existing EEOAP validator;
- staged adapter pre-commit ruff checks passed;
- no EEOAP schema change was made.

This is an honest limitation of repository hygiene, not a failure of the
OpenTelemetry-to-EEOAP adapter artifact.
