# Release Metadata Update Map

Purpose: map where version 1.24 package-local metadata drafts will be used
later.

| Field or file | Current v1.24 draft source | Future target file | Update timing | Requires release URL? | Requires DOI? | Notes |
|---|---|---|---|---:|---:|---|
| Author metadata | `CITATION_OTEL_EEOAP_RELEASE_DRAFT.cff`; `codemeta-otel-eeoap-release-draft.json`; `SOFTWARE_RELEASE_METADATA.md` | SoftwareX template manuscript; final support package metadata | Before final template package | no | no | Confirmed author metadata is usable now. |
| License | CFF, CodeMeta, software metadata draft | SoftwareX metadata table; support package metadata | Before final support package | no | no | Apache-2.0 remains root license. |
| Provisional tag | `SOFTWARE_RELEASE_METADATA.md`; `RELEASE_REFERENCE_DRAFTS.md` | GitHub Release notes; final references | After tag approval | yes | no | Do not create or push tag yet. |
| Release URL | TODO in all drafts | SoftwareX template manuscript; final references; GitHub Release notes | After public release exists | yes | no | Do not invent. |
| DOI | TODO in release/reference drafts | CFF; CodeMeta; SoftwareX metadata table; final references | After DOI exists | yes | yes | Omit DOI identifiers until real. |
| Support issue URL | `SUPPORT_CONTACT_RELEASE_DRAFT.md` | SoftwareX metadata table; CodeMeta `issueTracker`; support package metadata | After public issue URL exists | yes | no | GitHub Issues is preferred. |
| Artifact availability | `ARTIFACT_AVAILABILITY_RELEASE_DRAFT.md` | Manuscript artifact availability; final support package | After release URL and DOI decision | yes | optional | Use pre-release wording until public identifiers exist. |
| Data availability | `DATA_AVAILABILITY_RELEASE_DRAFT.md` | Manuscript data availability; final declarations | Before final template | optional | optional | Needs final release URL/DOI only for public artifact pointer. |
| Final references | `RELEASE_REFERENCE_DRAFTS.md` | SoftwareX references; release notes | After public identifiers exist | yes | optional | Placeholders only now. |
| Root `CITATION.cff` | Not changed | Root metadata only if focused release branch decision is approved | Later, only after explicit approval | yes | optional | Root currently describes AEP-Media. |
| Root `codemeta.json` | Not changed | Root metadata only if focused release branch decision is approved | Later, only after explicit approval | yes | optional | Blind overwrite remains risky. |
