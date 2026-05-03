# Review Pack Minimal

## 1) What Review Pack V0.3 is

Review Pack V0.3 is a local, offline package for a human reviewer. It starts
from an already captured signed export bundle, verifies that bundle first, and
then writes a small reviewer-facing directory.

It does not introduce new evidence semantics. CLI/core verification remains
canonical. V0.3 improves reviewer checklist IDs, manifest/receipt clarity,
conservative secret scan status, and structured failure output for agents
without changing evidence schema or core verification.

## 2) What it is not

- It is not legal non-repudiation.
- It is not compliance certification.
- It is not AI Act approval.
- It is not a full AI governance assessment.
- It is not a PDF or HTML report generator.
- It is not a hosted or remote review service.

Review Pack V0.3 does not change OpenAPI or MCP behavior and is not exposed
through OpenAPI or MCP.

## 3) Install

From a local checkout:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -e ".[langchain,openai-compatible,signing]"
```

## 4) LangChain copy/paste path

```bash
rm -rf ./tmp/langchain-minimal-evidence ./tmp/langchain-review-pack

python examples/langchain_minimal_evidence.py \
  --output-dir ./tmp/langchain-minimal-evidence

agent-evidence review-pack create \
  --bundle ./tmp/langchain-minimal-evidence/langchain-evidence.bundle.json \
  --public-key ./tmp/langchain-minimal-evidence/manifest-public.pem \
  --summary ./tmp/langchain-minimal-evidence/summary.json \
  --output-dir ./tmp/langchain-review-pack

find ./tmp/langchain-review-pack -maxdepth 3 -type f | sort
python -m json.tool ./tmp/langchain-review-pack/receipt.json
python -m json.tool ./tmp/langchain-review-pack/findings.json
cat ./tmp/langchain-review-pack/summary.md
```

## 5) OpenAI-compatible mock path

```bash
rm -rf ./tmp/openai-compatible-minimal-evidence ./tmp/openai-compatible-review-pack

python examples/openai_compatible_minimal_evidence.py \
  --output-dir ./tmp/openai-compatible-minimal-evidence \
  --mock

agent-evidence review-pack create \
  --bundle ./tmp/openai-compatible-minimal-evidence/openai-compatible-evidence.bundle.json \
  --public-key ./tmp/openai-compatible-minimal-evidence/manifest-public.pem \
  --summary ./tmp/openai-compatible-minimal-evidence/summary.json \
  --output-dir ./tmp/openai-compatible-review-pack

find ./tmp/openai-compatible-review-pack -maxdepth 3 -type f | sort
```

The OpenAI-compatible path shown here is mock/offline. It does not require an
external API key.

## 6) Output layout

Review Pack V0.3 writes:

```text
review-pack/
  manifest.json
  receipt.json
  findings.json
  summary.md
  artifacts/
    evidence.bundle.json
    manifest-public.pem
    summary.json
```

`artifacts/summary.json` is included only when `--summary` is provided.

Review Pack creation copies only the signed evidence bundle, the manifest
public key, and the optional summary file. It does not copy
`manifest-private.pem` or any arbitrary files from the source directory.

## 7) Reviewer summary

`summary.md` is markdown-only. It includes:

- verification outcome
- reviewer checklist with stable IDs such as `RP-CHECK-001`
- verification details table
- artifact inventory table
- findings summary table
- secret and private key boundary note
- pack creation mode: `local_offline`
- recommended reviewer actions
- what this does not prove

The checklist is a reviewer aid, not an approval workflow. It asks the reviewer
to confirm the verification outcome, inspect the evidence bundle and public
key, review findings and warnings, read limitations, and escalate fail or
unknown findings.

## 8) Manifest and receipt fields

Review Pack V0.3 keeps machine-readable reviewer metadata in `manifest.json`
and `receipt.json`.

Expected fields include:

- `review_pack_version: "0.3"`
- `pack_creation_mode: "local_offline"`
- `verification_ok`
- `record_count`
- `signature_count`
- `verified_signature_count`
- `included_artifacts`
- `artifact_inventory`
- `reviewer_checklist` in `manifest.json`
- `reviewer_checklist_reference` in `receipt.json`
- `secret_scan_status`
- `non_claims`

`secret_scan_status` is deliberately conservative. It records whether Review
Pack creation found configured secret sentinel patterns in the generated pack.
It is not comprehensive DLP and does not prove that all possible secrets are
absent.

## 9) Findings taxonomy

Review Pack V0.3 keeps a small findings taxonomy.

Allowed severity values:

- `pass`
- `warning`
- `fail`
- `unknown`

Finding types remain limited to verification, signature, summary attachment,
artifact inventory, private key exclusion, secret scan, limitation notice, and
fail-closed error categories. V0.3 adds narrow reviewer-package metadata
findings such as `reviewer_checklist_present`,
`review_pack_manifest_complete`, and `secret_scan_status_recorded`. The
taxonomy is intentionally not a compliance taxonomy.

## 10) Failure behavior

Review Pack creation verifies before packaging.

If verification fails:

- the command exits non-zero
- no successful Review Pack is written
- no misleading `summary.md` is written
- the source bundle, public key, and source summary are not modified

If the output directory already exists and is non-empty, the command fails
instead of overwriting it.

For agent callers that need machine-readable failure output, V0.3 adds:

```bash
agent-evidence review-pack create \
  --bundle ./tmp/langchain-minimal-evidence/langchain-evidence.bundle.json \
  --public-key ./tmp/langchain-minimal-evidence/manifest-public.pem \
  --summary ./tmp/langchain-minimal-evidence/summary.json \
  --output-dir ./tmp/langchain-review-pack \
  --json-errors
```

`--json-errors` changes only Review Pack creation failures. Successful output
is already JSON. Default failure output remains human-readable.

## 11) Safety boundaries

Review Pack V0.3:

- runs locally
- requires no network
- requires no external model API key
- does not serialize environment variables
- does not write provider API keys or authorization headers
- does not copy private keys
- does not claim comprehensive DLP

The reviewer summary explains what was verified and what artifacts were
included. It also states the limits: this package is not legal
non-repudiation, compliance certification, AI Act approval, or a full AI
governance assessment.

Review Pack V0.3 does not add PDF/HTML output, dashboard workflows, remote
review service behavior, legal attestation, compliance certification, AI Act
Pack behavior, or OpenAPI/MCP tools.
