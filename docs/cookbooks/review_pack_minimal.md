# Review Pack Minimal

## 1) What Review Pack V0.1 is

Review Pack V0.1 is a local, offline package for a human reviewer. It starts
from an already captured signed export bundle, verifies that bundle first, and
then writes a small reviewer-facing directory.

It does not introduce new evidence semantics. CLI/core verification remains
canonical.

## 2) What it is not

- It is not legal non-repudiation.
- It is not compliance certification.
- It is not AI Act approval.
- It is not a full AI governance assessment.
- It is not a PDF or HTML report generator.
- It is not a hosted or remote review service.

Review Pack V0.1 does not change OpenAPI or MCP behavior.

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

Review Pack V0.1 writes:

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

## 7) Failure behavior

Review Pack creation verifies before packaging.

If verification fails:

- the command exits non-zero
- no successful Review Pack is written
- no misleading `summary.md` is written
- the source bundle, public key, and source summary are not modified

If the output directory already exists and is non-empty, the command fails
instead of overwriting it.

## 8) Safety boundaries

Review Pack V0.1:

- runs locally
- requires no network
- requires no external model API key
- does not serialize environment variables
- does not write provider API keys or authorization headers
- does not copy private keys

The reviewer summary explains what was verified and what artifacts were
included. It also states the limits: this package is not legal
non-repudiation, compliance certification, AI Act approval, or a full AI
governance assessment.
