# Execution Evidence Object Architecture Note

Execution Evidence Object is the architecture-facing object surface for this
repository.

## Why this note exists

The repository still contains toolkit components for runtime capture, hashing,
storage, and export.

For standards-oriented discussion, the main entry should be the object model
rather than the implementation internals.

## Architectural role

Execution Evidence Object sits between:

- agent runtime execution
- integrity verification
- portable export
- standards-facing object discussion

## Repository role

This repository can now be read through two layers:

- implementation toolkit under `agent_evidence/`
- proposal prototype surfaces under `spec/`, `schema/`, and `examples/`

## Interpretation

The object is not a full observability replacement.

It is a bounded execution evidence artifact designed for review, integrity
checks, and object-oriented interoperability discussion.
