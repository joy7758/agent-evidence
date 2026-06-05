# Measurement Source Policy

## Allowed Measurement Sources

Use only public or authorized sources:

- GitHub traffic API, if authorized
- GitHub public search
- PyPI public download statistics
- PyPI BigQuery / PyPIStats
- public issues / PRs / docs / blogs
- Zenodo public records
- manual agent task tests

These sources provide indirect signals. They do not identify private users or
private agents.

## Disallowed Sources

Do not use:

- private user data
- private repositories
- private conversations
- hidden telemetry
- credentials
- leaked data
- scraping private services
- user profiling

Do not add code, tracking, cookies, analytics, GitHub Actions, scheduled jobs,
MCP registry publication, OpenAPI changes, or automated promotion to collect
these measurements.

## Attribution and Privacy

- do not identify individual users
- do not attribute private behavior to agents
- report aggregate or public signals only
- keep manual task test notes anonymized if needed
- do not collect secrets or private runtime artifacts

Manual task evaluation should focus on the tested tool behavior, the repository
state, and the observed task outcome. It should not name private users or infer
private deployment patterns.

## Interpretation Cautions

- GitHub traffic cannot prove agent identity
- PyPI downloads cannot prove agent use
- public search mentions do not equal adoption
- stars do not equal usage
- task success rate is controlled evaluation, not real-world adoption
- citation and DOI signals can lag behind actual reading or use
- absence of public mentions does not prove absence of private evaluation

## Decision Policy

- scorecard suggests improvements
- humans decide
- accepted actions require separate PR
- no automatic release
- no automatic promotion
- no automatic code changes
- no fake adoption claims
- no legal non-repudiation interpretation
- no compliance certification interpretation
- no AI Act approval interpretation
