# Citation Verification

Access date for web sources: 2026-05-23.

This file verifies the citation placeholders used in
`papers/opentelemetry-to-eeoap/paper_v0_8_journal_draft.md`. It separates
official external sources from local repository artifacts and avoids inventing
unverified bibliographic metadata.

## Summary

| Placeholder | Verification status | Stability | Main risk |
|---|---|---|---|
| `[OpenTelemetry-GenAI]` | verified | evolving | GenAI semantic conventions are marked Development and may change. |
| `[OpenTelemetry-Agent-Spans]` | verified | evolving | Agent span fields and semantic convention status may change. |
| `[JSON-Schema-2020-12]` | verified | stable | Exact author/editor formatting still depends on target venue style. |
| `[W3C-PROV]` | verified | stable | The paper should cite the specific PROV document used, not only the family label. |
| `[EEOAP-Artifact]` | partially verified | local artifact | Needs immutable release, archive, or DOI before external submission. |
| `[AEP-Artifact]` | partially verified | local artifact | Needs exact artifact scope and immutable identifier before external submission. |
| `[ACM-Artifact-Badging]` | verified | evolving | ACM policy wording may change; re-check before submission. |

## `[OpenTelemetry-GenAI]`

- Where it appears:
  - `paper_v0_8_journal_draft.md:125`
  - `paper_v0_8_journal_draft.md:429`
  - `paper_v0_8_journal_draft.md:481`
- Intended claim supported:
  OpenTelemetry has a Generative AI semantic convention area, and the paper
  uses that official telemetry-side context as the source framing.
- Preferred source type:
  Official documentation or official specification.
- Verified source title:
  `Semantic conventions for generative AI systems | OpenTelemetry`.
- Verified URL:
  <https://opentelemetry.io/docs/specs/semconv/gen-ai/>
- Access date:
  2026-05-23.
- Stability:
  Evolving.
- Bibliographic draft entry:
  OpenTelemetry. `Semantic conventions for generative AI systems`. Official
  OpenTelemetry semantic conventions documentation. Accessed 2026-05-23.
  URL: <https://opentelemetry.io/docs/specs/semconv/gen-ai/>. TODO: verify
  semantic convention version and status immediately before external
  submission.
- Verification status:
  Verified.
- Risk note:
  The official page identifies the GenAI semantic conventions as Development
  and lists agent spans as part of the Generative AI signal area. The paper
  should keep broad compatibility claims out of scope because this source is
  explicitly evolving.

## `[OpenTelemetry-Agent-Spans]`

- Where it appears:
  - `paper_v0_8_journal_draft.md:127`
  - `paper_v0_8_journal_draft.md:431`
  - `paper_v0_8_journal_draft.md:486`
- Intended claim supported:
  OpenTelemetry documents GenAI agent/framework span attributes and related
  span semantics that motivate the adapter's selected fields.
- Preferred source type:
  Official documentation or official specification.
- Verified source title:
  `Semantic Conventions for GenAI agent and framework spans | OpenTelemetry`.
- Verified URL:
  <https://opentelemetry.io/docs/specs/semconv/gen-ai/gen-ai-agent-spans/>
- Access date:
  2026-05-23.
- Stability:
  Evolving.
- Bibliographic draft entry:
  OpenTelemetry. `Semantic Conventions for GenAI agent and framework spans`.
  Official OpenTelemetry semantic conventions documentation. Accessed
  2026-05-23. URL:
  <https://opentelemetry.io/docs/specs/semconv/gen-ai/gen-ai-agent-spans/>.
  TODO: verify listed attributes and current semantic convention version before
  external submission.
- Verification status:
  Verified.
- Risk note:
  The source supports using agent id/name/version, operation name, timestamps,
  error attributes, and related span structure as telemetry-side material. It
  should not be cited as proof that all OpenTelemetry implementations emit a
  compatible trace shape.

## `[JSON-Schema-2020-12]`

- Where it appears:
  - `paper_v0_8_journal_draft.md:160`
  - `paper_v0_8_journal_draft.md:441`
  - `paper_v0_8_journal_draft.md:492`
- Intended claim supported:
  JSON Schema provides the structured validation context for JSON objects such
  as EEOAP-compatible statements.
- Preferred source type:
  Official specification.
- Verified source title:
  `Draft 2020-12`.
- Verified URL:
  <https://json-schema.org/draft/2020-12>
- Access date:
  2026-05-23.
- Stability:
  Stable.
- Bibliographic draft entry:
  Wright, Austin; Andrews, Henry; Hutton, Ben; Dennis, Greg. `JSON Schema Draft
  2020-12`. Published 2022-06-16. URL:
  <https://json-schema.org/draft/2020-12>. TODO: adapt author/editor ordering
  to the target venue style.
- Verification status:
  Verified.
- Risk note:
  The specification metadata is stable, but venue-specific reference formatting
  still needs final cleanup.

## `[W3C-PROV]`

- Where it appears:
  - `paper_v0_8_journal_draft.md:159`
  - `paper_v0_8_journal_draft.md:441`
  - `paper_v0_8_journal_draft.md:444`
  - `paper_v0_8_journal_draft.md:496`
- Intended claim supported:
  W3C PROV is the adjacent provenance model family for representing agents,
  activities, entities, and provenance relations.
- Preferred source type:
  Official W3C recommendation or official W3C document.
- Verified source title:
  `PROV-O: The PROV Ontology`.
- Verified URL:
  <https://www.w3.org/TR/prov-o/>
- Access date:
  2026-05-23.
- Stability:
  Stable.
- Bibliographic draft entry:
  Lebo, Timothy; Sahoo, Satya; McGuinness, Deborah. `PROV-O: The PROV
  Ontology`. W3C Recommendation, 2013-04-30. URL:
  <https://www.w3.org/TR/prov-o/>. TODO: decide whether the final paper should
  cite PROV-O alone or also cite PROV-DM and the PROV Overview.
- Verification status:
  Verified.
- Risk note:
  The current placeholder says "PROV provenance recommendation family." For a
  final manuscript, use specific W3C documents. PROV-O is stable reference
  material, but the overview document is a Working Group Note rather than the
  primary recommendation.

## `[EEOAP-Artifact]`

- Where it appears:
  - `paper_v0_8_journal_draft.md:146`
  - `paper_v0_8_journal_draft.md:436`
  - `paper_v0_8_journal_draft.md:500`
- Intended claim supported:
  EEOAP supplies the target operation accountability statement shape and the
  existing validator path reused by the adapter.
- Preferred source type:
  Repository artifact, release, archived artifact, or DOI.
- Verified source title:
  Local `agent-evidence` repository EEOAP and OpenTelemetry adapter materials.
- Verified local repository paths:
  - `tools/opentelemetry_to_eeoap_adapter.py`
  - `tests/test_opentelemetry_to_eeoap_adapter.py`
  - `generated/valid-agent-trace-eeoap-statement.json`
  - `generated/valid-agent-workflow-trace-eeoap-statement.json`
  - `papers/opentelemetry-to-eeoap/frozen_v0_5/`
- Access date:
  2026-05-23.
- Stability:
  Local artifact; requires DOI later.
- Bibliographic draft entry:
  `agent-evidence` repository. Execution Evidence and Operation Accountability
  Profile artifacts and OpenTelemetry-to-EEOAP adapter materials. Local branch
  `opentelemetry-to-eeoap-adapter`; v0.8 draft commit
  `d5879f3678ab22896b36d1d81e7a4f18a466ebcf`. TODO: replace with immutable
  release, archive, tag, or DOI before external submission.
- Verification status:
  Partially verified.
- Risk note:
  The local artifact is strong for internal review but not enough as a final
  public citation. The final paper needs an immutable artifact reference.

## `[AEP-Artifact]`

- Where it appears:
  - `paper_v0_8_journal_draft.md:162`
  - `paper_v0_8_journal_draft.md:449`
  - `paper_v0_8_journal_draft.md:506`
- Intended claim supported:
  AEP is a related local evidence-artifact line used for positioning against
  runtime evidence bundles and integrity-verifiable packaging.
- Preferred source type:
  Repository artifact, archived artifact, or DOI.
- Verified source title:
  Local `agent-evidence` repository AEP-related materials.
- Verified local repository path:
  `docs/paper/` and related local AEP materials are present, but many are
  out-of-scope dirty or untracked in the current worktree and were not modified
  by this v0.9 analysis.
- Access date:
  2026-05-23.
- Stability:
  Local artifact; requires DOI later.
- Bibliographic draft entry:
  `agent-evidence` repository. AEP-related evidence artifact materials used for
  positioning. TODO: identify the exact public artifact, release, tag, commit,
  or DOI before submission.
- Verification status:
  Partially verified.
- Risk note:
  The current AEP placeholder is too broad for external citation. The final
  manuscript should cite a specific public artifact and avoid relying on
  untracked or private local files.

## `[ACM-Artifact-Badging]`

- Where it appears:
  - `paper_v0_8_journal_draft.md:452`
  - `paper_v0_8_journal_draft.md:511`
- Intended claim supported:
  Artifact review and reproducibility expectations provide a neighboring
  publication-practice context for the package's clean-clone, checksum, and
  test evidence.
- Preferred source type:
  Official policy page.
- Verified source title:
  `Artifact Review and Badging - Current`.
- Verified URL:
  <https://www.acm.org/publications/policies/artifact-review-and-badging-current>
- Access date:
  2026-05-23.
- Stability:
  Evolving.
- Bibliographic draft entry:
  Association for Computing Machinery. `Artifact Review and Badging - Current`.
  ACM Publications Policy. Accessed 2026-05-23. URL:
  <https://www.acm.org/publications/policies/artifact-review-and-badging-current>.
  TODO: re-check current policy wording before external submission.
- Verification status:
  Verified.
- Risk note:
  This page is a policy document and may change. It is useful for framing
  artifact-readiness expectations, not as evidence that the package has been
  formally badged.
