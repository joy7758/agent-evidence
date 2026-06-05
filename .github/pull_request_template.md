## Summary

<!-- Describe the user-facing and agent-facing change. -->

## Ledger

- [ ] Updated `DEVELOPMENT_LEDGER.md` if this is a meaningful change
- [ ] Updated `DEVELOPMENT_LEDGER.jsonl` if this is a meaningful change

## Agent-Facing Discovery

- [ ] Updated `AGENTS.md` / `llms.txt` if agent behavior changes
- [ ] Updated `docs/project-facts.md` if project facts change
- [ ] Updated `docs/callable-surfaces.md` if CLI/API/MCP capabilities change

## Citation and Attribution

- [ ] Updated `CITATION.cff` / `codemeta.json` if citation metadata changes
- [ ] Updated `ATTRIBUTION.md` / `docs/how-to-cite.md` if attribution guidance changes

## Verification

- [ ] `pytest -q`
- [ ] `agent-evidence capabilities --json | python -m json.tool`
- [ ] Metadata validation checks pass
- [ ] AEP-Media targeted tests pass if media validation behavior changed
- [ ] No large binary artifacts or private evidence/media were added

## Claims-to-Avoid Check

- [ ] Does not claim official FDO standard status
- [ ] Does not claim legal non-repudiation
- [ ] Does not claim a full AI governance platform
- [ ] Does not claim OpenAPI/MCP availability unless implemented
- [ ] Does not add hidden promotion, reputation automation, or outbound promotion
- [ ] Does not claim legal admissibility, chain of custody, trusted timestamping, real PTP proof, full MP4 PRFT parsing, real C2PA signature verification, or production deployment

## AI Assistance Disclosure

- [ ] I did not use substantial AI assistance for this change
- [ ] I used substantial AI assistance and disclosed the scope in the PR notes
