# SoftwareX Blocker List

| Blocker | Severity | Current status | Recommended action |
|---|---|---|---|
| Public repository release state | blocker | Repository remote exists, but OpenTelemetry-to-EEOAP package branch/tags are not pushed or released. | Clean release branch first, then decide push/release/archive strategy. |
| README readiness | important | Root README exists but is broader than this adapter package. | Add SoftwareX-facing adapter README material in the release package. |
| LICENSE readiness | important | `LICENSE` exists and is Apache-2.0; `LICENSE.txt` does not exist. | Add `LICENSE.txt` or confirm `LICENSE` satisfies SoftwareX handling. |
| Source layout vs `repo/src` requirement | blocker | Source uses `agent_evidence/` and adapter is in `tools/`; no `src/` directory. | Decide whether to restructure, create a release package with `src/`, or ask SoftwareX editorial office. |
| Final software citation | blocker | `CITATION.cff` and `codemeta.json` describe AEP-Media, not OpenTelemetry-to-EEOAP. | Add package-specific citation metadata after release strategy is chosen. |
| EEOAP/AEP tag push or DOI decision | blocker | Local immutable tags exist but are not pushed or archived. | Decide public tag/archive/DOI route before final submission. |
| Final references | important | v0.9 references are draft and local artifact references changed after v1.3. | Update references with final public artifact identifiers. |
| 3000-word adaptation | blocker | v1.0 manuscript is about 3692 words and not SoftwareX-shaped. | Rewrite and compress into a SoftwareX article draft. |
| SoftwareX template conversion | blocker | Not done by design. | Convert only after release and article scope are fixed. |
| Data availability statement | important | Not final. | Draft venue-specific data/software availability statement. |
| Generative AI disclosure | important | Not final. | Add required disclosure if AI-assisted drafting is acknowledged. |
| Conflict of interest declaration | important | Not final. | Prepare final declaration. |
| Funding declaration | important | Not final. | Prepare final funding statement. |
| Repository hygiene / dirty out-of-scope items | blocker | Current worktree has unrelated modified/untracked files. | Clean or isolate release branch before any public package work. |
| Final clean-clone check after release candidate | blocker | v0.5 clean-clone exists, but not for final SoftwareX release candidate. | Re-run clean-clone and checksum verification after release package is frozen. |
