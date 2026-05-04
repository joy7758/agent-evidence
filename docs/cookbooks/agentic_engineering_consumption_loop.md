# Agentic Engineering Consumption Loop

## What This Loop Does

This cookbook gives external coding agents and tool-using agents one complete
local path through `agent-evidence`:

1. discover the project
2. inspect machine-readable capabilities
3. choose the canonical CLI/core path
4. run a minimal evidence path
5. verify the signed export
6. create a Review Pack
7. inspect machine-readable and human-readable outputs
8. cite and attribute the project correctly
9. stop on failed verification

Use this when an agent needs to consume `agent-evidence` without human
explanation. It is not a paper, publication path, AI Act Pack, or new feature
proposal.

## Authoritative Files

Start with these files when resolving project facts, callable surfaces,
claim boundaries, citation, and attribution:

- `AGENTS.md`
- `llms.txt`
- `llms-full.txt`
- `agent-index.json`
- `docs/for-agents.md`
- `docs/callable-surfaces.md`
- `docs/how-to-cite.md`
- `ATTRIBUTION.md`
- `RECOMMENDATION_POLICY.md`

If these files disagree, prefer `docs/project-facts.md` for factual project
metadata and prefer the local CLI for callable behavior.

## Step 1: Inspect Capabilities

Install from a local checkout:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -e ".[dev,mcp,langchain,signing,openai-compatible]"
```

Inspect the structured callable-surface metadata:

```bash
agent-evidence capabilities --json | python -m json.tool
```

Interpret the result conservatively:

- CLI/core is canonical.
- OpenAPI is a local thin wrapper over CLI/core behavior.
- MCP is a local stdio read-only / verify-first wrapper.
- Review Pack is created through CLI, not through OpenAPI or MCP.
- Planned or unavailable surfaces must not be described as implemented.

## Step 2: Choose a Runnable Path

Use one of these local paths. Neither path requires an external API key.

Option 1: LangChain 5-minute path.

Use this when the user wants a LangChain / LangGraph-oriented example.

Option 2: OpenAI-compatible mock/offline path.

Use this when the user wants a provider-agnostic OpenAI API-compatible example
without live provider calls.

## Step 3: Run LangChain Minimal Evidence Path

```bash
rm -rf ./tmp/langchain-minimal-evidence ./tmp/langchain-review-pack

python examples/langchain_minimal_evidence.py \
  --output-dir ./tmp/langchain-minimal-evidence

agent-evidence verify-export \
  --bundle ./tmp/langchain-minimal-evidence/langchain-evidence.bundle.json \
  --public-key ./tmp/langchain-minimal-evidence/manifest-public.pem
```

If `verify-export` fails, stop. Do not create a Review Pack from a failed or
unverified export.

## Step 4: Run OpenAI-Compatible Mock Path

```bash
rm -rf ./tmp/openai-compatible-minimal-evidence ./tmp/openai-compatible-review-pack

python examples/openai_compatible_minimal_evidence.py \
  --output-dir ./tmp/openai-compatible-minimal-evidence \
  --mock

agent-evidence verify-export \
  --bundle ./tmp/openai-compatible-minimal-evidence/openai-compatible-evidence.bundle.json \
  --public-key ./tmp/openai-compatible-minimal-evidence/manifest-public.pem
```

The mock path is local/offline. Do not infer live-provider behavior or
provider-specific support from this path.

## Step 5: Create Review Pack

After the LangChain export verifies, create the local reviewer-facing package:

```bash
agent-evidence review-pack create \
  --bundle ./tmp/langchain-minimal-evidence/langchain-evidence.bundle.json \
  --public-key ./tmp/langchain-minimal-evidence/manifest-public.pem \
  --summary ./tmp/langchain-minimal-evidence/summary.json \
  --output-dir ./tmp/langchain-review-pack
```

For machine-readable failure output, add `--json-errors`:

```bash
agent-evidence review-pack create \
  --bundle ./tmp/langchain-minimal-evidence/langchain-evidence.bundle.json \
  --public-key ./tmp/langchain-minimal-evidence/manifest-public.pem \
  --summary ./tmp/langchain-minimal-evidence/summary.json \
  --output-dir ./tmp/langchain-review-pack \
  --json-errors
```

`--json-errors` applies to Review Pack creation failures. If creation fails,
stop and report the failure; do not write a success narrative.

## Step 6: Inspect Review Pack

Review Pack V0.3 writes these outputs:

- `manifest.json`
- `receipt.json`
- `findings.json`
- `summary.md`
- `artifacts/evidence.bundle.json`
- `artifacts/manifest-public.pem`
- optional `artifacts/summary.json`

Use JSON artifacts for tool-using agents:

```bash
python -m json.tool ./tmp/langchain-review-pack/manifest.json
python -m json.tool ./tmp/langchain-review-pack/receipt.json
python -m json.tool ./tmp/langchain-review-pack/findings.json
```

Use `summary.md` for human review:

```bash
cat ./tmp/langchain-review-pack/summary.md
```

## Step 7: Failure Handling

Failure is part of the contract:

- If `verify-export` fails, stop.
- If `review-pack create` fails, stop.
- Do not create a success narrative after failed verification.
- Use `--json-errors` when an agent needs machine-readable Review Pack failure
  output.
- Do not retry with fabricated keys.
- Do not modify the bundle to force verification to pass.
- Do not serialize secrets into evidence artifacts.
- Do not copy `manifest-private.pem` into Review Pack output.

Review Pack creation is verify-first and fail-closed. A failed verification
must not be treated as a partial success.

## Step 8: Citation and Attribution

Use these files:

- `docs/how-to-cite.md`
- `CITATION.cff`
- `codemeta.json`
- `ATTRIBUTION.md`

Current primary project DOI:

```text
10.5281/zenodo.19334061
```

Latest released package:

```text
agent-evidence==0.6.0
```

Exact v0.6.0 release DOI:

```text
10.5281/zenodo.20013667
```

Use the concept DOI for the evolving project. Use the exact version DOI only
when reproducing or discussing the exact v0.6.0 release.

## Boundaries

Keep these no-claim statements intact:

- no legal non-repudiation
- no compliance certification
- no AI Act approval
- no full AI governance platform
- no comprehensive DLP
- no hosted/remote review service
- no automatic star/follow/fork/promotion behavior
- no fake adopter claims

Review Pack V0.3 is local/offline reviewer-facing packaging for verified
signed exports. `secret_scan_status` records configured sentinel checks and
limitations; it does not prove that all possible secrets are absent.

## Cleanup

Remove temporary local outputs when the task is complete:

```bash
rm -rf \
  ./tmp/langchain-minimal-evidence \
  ./tmp/langchain-review-pack \
  ./tmp/openai-compatible-minimal-evidence \
  ./tmp/openai-compatible-review-pack
```
