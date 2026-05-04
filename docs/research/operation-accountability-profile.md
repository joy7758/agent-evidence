# Operation Accountability Profile

Operation Accountability Profile is a working research frame for describing
evidence-bearing AI agent operations in a way that supports post-execution
review.

It is a minimal profile concept, not an official standard.

## Working definition

An Operation Accountability Profile describes one operation in terms of:

- what happened
- who or what acted
- what runtime events were recorded
- which evidence records were exported
- how the exported bundle was verified
- which reviewer-facing package was produced

The goal is not to capture every possible runtime detail. The goal is to keep
enough structure for another party to review the operation later.

## Role in agent-evidence

In `agent-evidence`, the profile idea connects these layers:

- runtime evidence records
- exported evidence bundle
- manifest and optional signature metadata
- verification result or receipt
- Review Pack V0.3
- reviewer-facing `summary.md`

The CLI and local wrappers should preserve this layering. Wrappers should call
the same validation, export, and verification behavior rather than inventing
parallel evidence semantics.

## Minimal object model

The research object model can stay small:

| Concept | Meaning |
| --- | --- |
| Operation | The accountable run or service action under review. |
| Actor / agent | The runtime, tool-using system, or service identity involved. |
| Runtime event | A recorded event from the operation path. |
| Tool call or action | A concrete action inside the run. |
| Evidence record | A structured record emitted by the runtime evidence layer. |
| Verification result | The result of validating or verifying the exported evidence. |
| Reviewer-facing package | A local package that helps a reviewer inspect verified artifacts. |

This model is intentionally review-oriented. It does not require a hosted
control plane or a new governance platform.

## Non-claims

Operation Accountability Profile, as used here, is not:

- an official FDO standard
- an official AI Act compliance profile
- legal non-repudiation
- compliance certification
- full governance automation
- comprehensive DLP
- a remote registry
- a complete data-space connector

## Research questions

The profile raises practical research questions:

- What evidence is sufficient for post-execution accountability?
- How can agent runs be packaged for independent review?
- How can profiles remain minimal and interoperable?
- How can review artifacts avoid leaking secrets or raw sensitive content?
- Which verification results are useful to both humans and tool-using agents?
- How should a future compliance-oriented interpretation layer reference
  evidence without overclaiming what the evidence proves?

## Near-term use

For now, the profile should be used as a research and documentation frame for
`agent-evidence`. It should not be promoted as a standard, certification
method, or official regulatory profile.
