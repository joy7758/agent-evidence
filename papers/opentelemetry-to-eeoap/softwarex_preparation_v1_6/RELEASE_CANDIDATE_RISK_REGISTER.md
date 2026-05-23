# Release Candidate Risk Register

| Risk | Severity | Likelihood | Mitigation | Owner / next action |
|---|---|---|---|---|
| Public release before metadata is corrected | high | medium | Do not release until metadata strategy identifies the OpenTelemetry-to-EEOAP software object. | Resolve metadata strategy. |
| Tag push before target scope is decided | high | medium | Keep local tags local until public release scope is approved. | Resolve release strategy. |
| Root metadata still AEP-Media-specific | high | high | Do not use current root metadata for OpenTelemetry-to-EEOAP citation. | Create metadata strategy note. |
| SoftwareX article exceeds word limit | high | high | Compress v1.0 into SoftwareX structure under 3000 words. | Create article draft only after metadata strategy. |
| No `repo/src` layout | high | medium | Decide whether to restructure, create release package layout, or ask SoftwareX editorial office. | Resolve source-layout strategy. |
| Local tags not archived | medium | high | Push/archive only after release candidate is stable. | Release strategy gate. |
| `frozen_v0_5` predates second valid trace | medium | high | Build final SoftwareX support package including v0.7 second-trace evidence. | Final package checklist. |
| Dirty original worktree causing accidental release contamination | high | medium | Continue release prep only inside isolated worktree. | Keep isolation discipline. |
| References not final | medium | high | Update after public identifiers are chosen. | Final reference pass. |
| Generative AI disclosure not venue-final | medium | medium | Draft venue-specific disclosure before submission. | Declarations pass. |

## Register Interpretation

The highest-risk item is not adapter correctness. The highest-risk item is
misidentifying the public software object and publishing metadata or tags that
refer to the wrong package.
