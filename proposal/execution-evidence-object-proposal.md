# Execution Evidence Object Proposal

## 1 Motivation

Current AI agent systems generate many traces, callbacks, logs, and export
artifacts, but they rarely converge on a bounded execution evidence object that
can be discussed as a standards-oriented unit.

Execution Evidence Object is proposed as that bounded unit.

## 2 Problem in current AI agents

Today most agent runtimes expose:

- framework-specific traces
- callback streams
- debugging logs
- storage-specific exports

These are useful for engineering, but they do not automatically provide a
portable object that is stable enough for verification, review, and
standardization discussion.

## 3 Evidence object model

The proposed object model includes:

- `object_type`
- `agent_framework`
- `run_id`
- `steps`
- `hashes`
- `context`
- `timestamp`

Reference material:

- Schema: [schema/execution-evidence-object.schema.json](../schema/execution-evidence-object.schema.json)
- Spec: [spec/execution-evidence-object.md](../spec/execution-evidence-object.md)
- Minimal example: [examples/minimal-evidence-object.json](../examples/minimal-evidence-object.json)
- OpenAI run example: [examples/evidence-object-openai-run.json](../examples/evidence-object-openai-run.json)

## 4 FDO compatibility

The object can be discussed as a Digital Object-oriented artifact through:

- object identity
- metadata context
- integrity references
- provenance-oriented runtime origin

Reference mapping:

- [docs/fdo-mapping/execution-evidence-to-fdo.md](../docs/fdo-mapping/execution-evidence-to-fdo.md)

## 5 Prototype implementation

This repository includes a minimal working prototype:

- Verification script: [scripts/verify_evidence_object.py](../scripts/verify_evidence_object.py)
- OpenAI Agents integration: [integrations/openai-agents](../integrations/openai-agents)
- LangChain integration: [integrations/langchain](../integrations/langchain)
- CrewAI integration: [integrations/crewai](../integrations/crewai)

The goal is to show that different runtimes can export toward the same object
shape.

## 6 Future standardization path

Near-term next steps are:

- stabilize the object field set
- clarify integrity and provenance requirements
- compare export behavior across frameworks
- refine FDO-facing mapping language
- turn the prototype into a discussion-ready standards profile candidate
