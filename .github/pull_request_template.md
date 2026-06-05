## Summary

<!-- Describe the user-facing and agent-facing change. -->

## Ledger

- [ ] Updated `DEVELOPMENT_LEDGER.md` if this is a meaningful change
- [ ] Updated `DEVELOPMENT_LEDGER.jsonl` if this is a meaningful change

## Agent-Facing Discovery

- [ ] Updated `AGENTS.md` / `llms.txt` if agent behavior changes
- [ ] Updated `docs/project-facts.md` if project facts change
- [ ] Updated `docs/callable-surfaces.md` if CLI/API/MCP capabilities change

## EEOAP Clause Gate

Affected EEOAP clauses:

- [ ] EEOAP-001: operation accountability statement
- [ ] EEOAP-002: actor / subject / operation / timestamp binding
- [ ] EEOAP-003: policy / evidence / provenance references
- [ ] EEOAP-004: validator-readable validation report
- [ ] EEOAP-005: clause citation in task or pull-request summary
- [ ] Not applicable; explain why in the PR summary

Validator command:

```text
agent-evidence validate-profile examples/minimal-valid-evidence.json
```

Validator result:

```text
<paste result or short PASS/FAIL summary>
```

Examples updated? yes/no:

Known deviations:

Claim hygiene confirmation:

- [ ] This PR does not mark local packages as submitted, accepted, externally reviewed, certified, or published.

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
