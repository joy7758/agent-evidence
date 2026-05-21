# Public-safe Submission System Fields

## Article Type Suggestion

Research Article.

## Title

A Minimal Execution Evidence Profile for Verifiable AI Agent Operations in
FDO-style Data Spaces

## Abstract

EEOAP (Execution Evidence and Operation Accountability Profile) defines a minimal operation-level evidence profile for one AI (Artificial Intelligence) agent operation in FDO (FAIR Digital Object)-style data spaces. The profile packages actor, action, subject, policy, output, provenance, evidence references, integrity binding, and validation metadata into a structured object that can be reviewed outside the original runtime. The accompanying artifact provides a local validator path and a reproducible paper_case example. Running make paper-demo reports PASS valid evidence bundle for the valid case and FAIL tampered output hash mismatch for an altered output reference. The tampered case exposes references_digest_mismatch, showing that a stale integrity binding is not silently accepted. Targeted EEOAP tests for the paper case and operation-accountability profile previously reported 19 passed / 1 warning. The contribution is intentionally bounded: it does not claim full repository pytest success, public GitHub Release publication, Zenodo DOI issuance, production readiness, official FDO standard adoption, legal compliance, semantic correctness of AI output, or ZKP (Zero-Knowledge Proof) implementation. The result is a standards-facing research artifact that makes selected operation evidence claims inspectable, replayable, and falsifiable offline, while preserving clear boundaries between validator evidence, artifact availability, and future assurance layers.

## Keywords

execution evidence; operation accountability; validator; FDO; data spaces;
provenance; artifact reproducibility

## Highlights

- Defines a minimal profile for AI agent operation evidence.
- Validator checks structure, references, policy linkage, and integrity.
- Tampered output fails with references_digest_mismatch.
- Maps operation evidence to FDO-style data-space concerns.
- Local paper_case reproduces PASS and expected FAIL results.

## Author

Bin Zhang

## Affiliation

Independent Researcher, China

## Email

joy7759@gmail.com

## ORCID

0009-0002-8861-1481

## CRediT Roles

Conceptualization; Methodology; Software; Validation; Investigation;
Writing - original draft; Writing - review and editing.

## Funding

No specific funding.

## Competing Interests

None declared.

## Ethics

Not applicable. No human participants, no patient data, and no clinical
intervention.

## Generative AI Disclosure

OpenAI ChatGPT/Codex was used for drafting support, command generation, text
organization, and review assistance. The author reviewed and takes
responsibility for all claims, code, artifacts, citations, validation results,
and conclusions. AI tools are not listed as authors.

## Data Availability

This paper uses repository-contained paper_case artifacts. It does not use
human participants, patient data, or an external private dataset. The artifact
remains local-only at initial submission unless later published. No public
GitHub Release or Zenodo DOI is claimed. If required by editors or reviewers,
a private review package may be supplied through the journal workflow.
Reproduction command: make paper-demo.

## Artifact Availability

The local sealed tag eeoap-v0.1-paper exists as a local artifact anchor at
commit 96f444b7ed39b39fe9f47e428af835952e843cb0. The tag is not claimed as
publicly pushed. No public GitHub Release or Zenodo DOI is claimed. The
artifact is scoped to paper_case, the validator path, valid PASS, tampered
FAIL, references_digest_mismatch, and targeted EEOAP tests. It may be supplied
privately through the journal workflow if required.

## Private Contact Note

Phone number and full postal address must be entered privately in the journal
submission system or a non-committed private title page. They are not included
in this Git-tracked file.
