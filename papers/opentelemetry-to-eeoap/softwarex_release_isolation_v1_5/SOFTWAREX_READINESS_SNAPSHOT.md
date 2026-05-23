# SoftwareX Readiness Snapshot

| Readiness item | Present? | Evidence path | Risk | Required action |
|---|---|---|---|---|
| Root README | yes | `README.md` | Broad repository README; not focused on OpenTelemetry-to-EEOAP. | Prepare SoftwareX-facing adapter README material later. |
| Root LICENSE / LICENSE.txt | partial | `LICENSE` exists; `LICENSE.txt` absent. | SoftwareX guidance names `LICENSE.txt`; repository has Apache-2.0 in `LICENSE`. | Decide whether to add `LICENSE.txt` in release package or confirm `LICENSE` is accepted. |
| Source code location | partial | `agent_evidence/`, `tools/opentelemetry_to_eeoap_adapter.py` | No `src/` directory or `repo/src` layout. | Decide release-layout strategy before public release. |
| Tests | yes | `tests/test_opentelemetry_to_eeoap_adapter.py` | Scoped tests are good, but final release candidate needs another clean verification. | Re-run before release. |
| Examples | yes | `examples/opentelemetry/` | Synthetic fixtures only. | Preserve claim boundary. |
| Generated evidence artifacts | yes | `generated/valid-agent-trace-eeoap-statement.json`, `generated/valid-agent-workflow-trace-eeoap-statement.json` | Generated outputs must remain tied to fixture and adapter versions. | Include in final support material with checksums. |
| Frozen package | yes | `papers/opentelemetry-to-eeoap/frozen_v0_5/` | Frozen package predates v0.7 second trace. | Build final SoftwareX supplement later. |
| SoftwareX route analysis | yes | `papers/opentelemetry-to-eeoap/softwarex_route_v1_4/` | Analysis only; not submission material. | Convert into preparation checklist next. |
| Artifact tags | yes, local | `eeoap-v0.1-artifact`, `aep-v0.1-artifact` | Tags are local and not pushed. | Decide public tag/archive/DOI strategy. |
| CITATION.cff | yes | `CITATION.cff` | Currently describes AEP-Media, not OpenTelemetry-to-EEOAP. | Prepare package-specific citation metadata later. |
| codemeta.json | yes | `codemeta.json` | Currently describes AEP-Media, not OpenTelemetry-to-EEOAP. | Prepare package-specific CodeMeta later. |
| Clean worktree | yes | `/tmp/agent-evidence-softwarex-otel-eeoap-rc` | Temporary worktree needs preservation until next step completes. | Continue SoftwareX prep in this isolated branch. |
| Scoped tests | yes | `8 passed in 2.30s` before docs; `8 passed in 2.69s` after docs. | Shared virtual environment warning may appear during validator commands. | Keep warning disclosed. |
| Validator checks | yes | Both generated statements validate with `ok=true`, `issue_count=0`. | CLI uses shared virtual environment. | Prefer a self-contained release environment later. |
| Checksum checks | yes | `shasum -a 256 -c CHECKSUMS.sha256` in `frozen_v0_5/` | Covers frozen v0.5 package, not final SoftwareX supplement. | Generate final checksums after final supplement is cut. |
| Dirty out-of-scope worktree risk | isolated | Current dirty repository is separate from this worktree. | Preparing release in the original dirty worktree would be risky. | Keep release work inside isolated branch/worktree. |

## Summary

The clean worktree is a suitable base for the next SoftwareX preparation step.
It is not yet a public release candidate because source layout, citation
metadata, public tag/archive/DOI strategy, and final support material remain
open.
