## Summary

<!-- Describe the user-facing and agent-facing change. -->

## Ledger

- [ ] Updated `DEVELOPMENT_LEDGER.md` if this is a meaningful change
- [ ] Updated `DEVELOPMENT_LEDGER.jsonl` if this is a meaningful change

## Agent-Facing Discovery

- [ ] Updated `AGENTS.md` / `llms.txt` if agent behavior changes
- [ ] Updated `docs/project-facts.md` if project facts change
- [ ] Updated `docs/callable-surfaces.md` if CLI/API/MCP capabilities change

## EEOAP Clause Citation

This Pull Request must comply with the Execution Evidence and Operation Accountability
Profile (EEOAP) when it changes protocol metadata, validation behavior, examples,
agent-facing documentation, or operation-accountability code paths.

List all applicable EEOAP clause identifiers implemented or affected:

- [ ] EEOAP-001: Completed operation must produce an operation accountability statement
- [ ] EEOAP-002: Statement must bind actor, subject, operation, and timestamp
- [ ] EEOAP-003: Statement must bind policy, evidence, and provenance references
- [ ] EEOAP-004: Statement must produce or reference a validator-readable validation report
- [ ] EEOAP-005: Implementation changes must cite affected EEOAP clauses in the task or PR summary
- [ ] Not applicable; explain why in the PR summary

Cited clauses:

```text
EEOAP-XXX, EEOAP-YYY
```

## EEOAP Protocol Validation

Run the protocol gate commands and include the results before requesting review:

```bash
python -m json.tool protocol/manifest.json
python -m json.tool protocol/clause-index.json
python scripts/check_protocol_citations.py
agent-evidence validate-profile examples/minimal-valid-evidence.json
```

Validation output:

```text
<paste "ok": true, PASS output, or a brief failure summary>
```

Any validation failure should be fixed before requesting review.

Example update check:

- [ ] Updated minimal examples if contract fields changed
- [ ] Updated tests if behavior changed
- [ ] Updated documentation under `docs/protocol/` if protocol behavior changed

Affected example files:

```text
examples/...
```

Known deviations:

```text
EEOAP-XXX deviation explanation...
```

Final EEOAP statement:

- [ ] All relevant EEOAP clauses have been cited above
- [ ] All protocol validation commands have been executed and passed
- [ ] This PR complies with EEOAP unless deviations are listed above

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
