# Public-safe Submission System Fields

## Article Type Suggestion

Research Article.

## Title

A Minimal Execution Evidence Profile for Validator-Checkable AI Agent
Operation Records in FAIR Digital Object-Inspired Data-Space Settings

## Abstract

The Execution Evidence and Operation Accountability Profile (EEOAP) is a minimal evidence profile for validator-checkable records of individual artificial intelligence (AI) agent operations in FAIR Digital Object-inspired data-space settings. AI-agent outputs are often reviewed after the originating runtime, logs, credentials, or prompts are unavailable. EEOAP packages actor, action, subject, policy reference, output reference, provenance, evidence references, integrity binding, and validation metadata into one offline review object. The paper contributes the profile boundary, a local validator path, and a repository-contained paper_case artifact. The validator enforces required structure, reference closure, and integrity-linked consistency conditions over fields used by the review object. Running make paper-demo demonstrates the intended boundary: the valid evidence bundle reports PASS valid evidence bundle, while a controlled tampered-output case reports FAIL tampered output hash mismatch with references_digest_mismatch as the primary error code. Targeted tests support the operation-accountability and paper-case behavior, but exhaustive validator assurance, semantic correctness of AI output, legal compliance, production readiness, public release, and archival DOI claims are outside scope. The result is a standards- and interfaces-oriented artifact for making selected post hoc operation evidence claims inspectable and falsifiable offline.

## Keywords

execution evidence; operation accountability; validator-checkable records;
FAIR Digital Object; data-space interfaces; provenance; artifact reproducibility

## Highlights

- Defines a minimal profile for AI agent operation evidence.
- Validator checks structure, reference closure, and integrity linkage.
- Tampered output fails with references_digest_mismatch.
- Maps operation evidence to FAIR Digital Object-inspired settings.
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

During the preparation of this work, the author used OpenAI ChatGPT and Codex
to support language editing, structural reorganization, command generation,
and drafting of submission-packaging text. After using these tools, the
author reviewed and edited the content as needed and takes full
responsibility for the content of the article. AI tools are not listed as
authors.

## Data Availability

This submission uses repository-contained paper_case artifacts and does not
use human-participant data, patient data, clinical-intervention data, or
external private datasets. At initial submission, the supporting software
artifact is not deposited in a public repository because the author is
maintaining a sealed review-state package and does not yet claim a public
release or archival identifier. A private review package can be supplied to
editors and reviewers through the journal workflow on request. If the artifact
is later publicly released, this statement will be updated to include the
persistent access point.

## Artifact Availability

The artifact supporting the bounded claims of this paper consists of the
paper_case files, the local validator path, and the make paper-demo
reproduction command. This submission does not claim a public GitHub Release
or a Zenodo DOI. The artifact is available as a private review package upon
editorial request. The claims supported by this artifact are limited to
acceptance of the valid paper case, rejection of a controlled tampered case
with the expected error boundary, and the bounded targeted-test evidence
described in the manuscript.

## Private Contact Note

Phone number and full postal address must be entered privately in the journal
submission system or a non-committed private title page. They are not included
in this Git-tracked file.
