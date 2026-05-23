# Release Blockers

| Blocker | Current status | Severity | Required before official template conversion? | Required before formal submission? | Action required |
|---|---|---|---|---|---|
| DOI not created | No DOI exists. | blocker | no | yes, if DOI/archive route is chosen | Create only after release package is frozen. |
| GitHub Release not created | No GitHub Release exists. | blocker | no | yes, if GitHub Release route is chosen | Create after final verification. |
| Tags not pushed | EEOAP/AEP tags and package tag are not public. | blocker | no | yes | Decide tag strategy and push only after release approval. |
| Root metadata mismatch | Root `CITATION.cff` and `codemeta.json` describe AEP-Media. | blocker | no | yes | Decide final metadata strategy before public release. |
| Final public release metadata missing | Local drafts exist only. | blocker | no | yes | Finalize CFF/CodeMeta after release scope is fixed. |
| Official SoftwareX `.docx`/`.tex` template not applied | Markdown template-style draft exists. | important | yes | yes | Convert after this package passes clean-clone verification. |
| Final clean-clone verification not executed | Planned but not yet run for v1.15. | important | no | yes | Run after v1.15 commit. |
| Final checksum verification after package creation needed | Performed locally during package creation. | important | no | yes | Re-run after clean-clone/package finalization. |
| Final references need public URLs/DOI/archives | EEOAP/AEP placeholders remain. | blocker | no | yes | Replace after release/archive decisions. |
| Source layout does not use `repo/src` | Adapter is under `tools/`; package under `agent_evidence/`. | important | no | possibly | Explain or adjust only if required. |
| Final declarations need venue wording | Draft declarations included. | important | no | yes | Adapt to final SoftwareX policy wording. |
