# External Pre-Review Packet

## Title

From Agent Telemetry to Portable Operation Evidence: A Minimal Adapter from
OpenTelemetry Agent Spans to EEOAP Evidence Objects

## One-sentence summary

This manuscript studies a bounded adapter path from OpenTelemetry-style agent
telemetry to EEOAP-compatible portable operation evidence.

## Problem

Runtime telemetry helps describe what happened inside an agent system, but it
does not automatically become a portable operation evidence object another
party can validate. A trace can contain span ids, parent links, attributes,
timestamps, and errors, yet still lack a profile-aware statement shape,
evidence references, integrity fields, and validation result.

## Method

- Input: local OpenTelemetry-style agent trace JSON fixtures.
- Adapter: extracts trace/span provenance, agent identity, operation name, tool
  spans, timestamps, errors, and parent-child span relations.
- Output: one EEOAP-compatible operation accountability statement for each
  valid trace.
- Validator: the existing EEOAP validator checks generated statements through
  `schema`, `references`, `consistency`, and `integrity` stages.

## Evidence

- Two valid trace contexts are evaluated.
- Four invalid trace contexts are evaluated.
- Both valid generated EEOAP statements pass the existing validator with
  `ok=true` and `issue_count=0`.
- Scoped adapter tests pass.
- Clean-clone verification exists for the v0.5 frozen package.
- Checksum verification exists for the v0.5 frozen package.

## What this does not claim

- No legal accountability proof.
- No full runtime reconstruction.
- No broad OpenTelemetry compatibility.
- No cross-framework generality.
- No agent-output correctness.
- No production readiness.
- No new EEOAP profile.
- No regulatory compliance.

## What feedback is requested

Please focus on:

- whether the contribution is distinct from EEOAP and AEP;
- whether the telemetry-to-evidence gap is convincing;
- whether two valid traces and four invalid diagnostics are enough for a
  journal route;
- whether the paper reads like a method contribution rather than a tool note;
- whether any claim overreaches the evidence.

## Suggested reviewer questions

- Is the central thesis clear?
- Is the method more than field copying?
- Are the non-claims clear enough?
- Which venue type fits best?
- What minimum evidence would strengthen the paper further?
