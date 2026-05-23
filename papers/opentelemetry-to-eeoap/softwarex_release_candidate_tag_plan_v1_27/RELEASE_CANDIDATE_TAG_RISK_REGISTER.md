# Release-Candidate Tag Risk Register

| Risk | Severity | Likelihood | Mitigation | Next action |
|---|---|---|---|---|
| Tagging wrong commit | high | medium | Use recorded target commit; verify `git rev-parse <TAG_NAME>^{}` equals target commit | Create local tag only after target commit is known |
| Tagging before metadata stable | medium | medium | Treat the tag as RC only; keep final release URL, DOI, and GitHub Release as TODO | Do not push until release metadata is stable |
| Tag name confusion with EEOAP/AEP artifact tags | medium | low | Use explicit `opentelemetry-to-eeoap-softwarex-rc-v1.0` name | Keep relation to `eeoap-v0.1-artifact` and `aep-v0.1-artifact` documented |
| Pushing tag too early | high | medium | Separate local tag creation from tag push; require author approval before push | Do not push in v1.27 or local tag creation step |
| Private metadata accidentally included | high | low | Run privacy checks and keep support contact through GitHub Issues | Repeat privacy check before local tag and before push |
| Root metadata still mismatched | medium | high | Keep root metadata unchanged and use package-local metadata | Do not overwrite root metadata without explicit focused release decision |
| CFF YAML validation skipped | medium | high | Keep skip reason documented; validate if PyYAML or equivalent becomes available | Accept documented skip for RC only or add parser check later |
| Release fields still TODO | high | high | Keep RC scope explicit; do not claim DOI, release URL, or GitHub Release | Resolve before public release or formal submission |
| GitHub Release/DOI not created | medium | high | Keep RC tag local until release route is approved | Plan release sequence separately |
| Tag points to branch with template drafts but not final release artifacts | medium | medium | State RC scope clearly and keep final submission blockers documented | Do not present RC tag as final SoftwareX submission |
