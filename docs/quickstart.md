# Quickstart

This quickstart uses one existing runnable path only: `examples/langchain_minimal_evidence.py`.

It does not stitch together the demo path and the profile-validator path. The goal is a first run that produces the normalized outputs used in this repository today:

- `bundle`
- `receipt`
- `summary`

## 1. Prerequisites

- Python `3.11+`
- No model API key is required for this path
- On Python `3.14`, `langchain_core` may emit a non-blocking warning during the run

## 2. Install

From the repository root:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[langchain,signing]"
```

## 3. Run One Runnable Example

Choose an output directory and run the existing minimal LangChain example:

```bash
OUTPUT_DIR=/tmp/agent-evidence-quickstart
python examples/langchain_minimal_evidence.py --output-dir "$OUTPUT_DIR"
```

What this step already does:

- captures local LangChain runtime events
- exports a signed `bundle`
- verifies the exported bundle in-process
- writes a `summary`

## 4. Export Step

There is no separate export command in this quickstart path. The example above already performs the export step and writes the `bundle`.

Confirm that the `bundle` exists:

```bash
test -f "$OUTPUT_DIR/langchain-evidence.bundle.json"
```

## 5. Verify Step

Generate a standalone `receipt` from the exported `bundle`:

```bash
agent-evidence verify-export \
  --bundle "$OUTPUT_DIR/langchain-evidence.bundle.json" \
  --public-key "$OUTPUT_DIR/manifest-public.pem" \
  > "$OUTPUT_DIR/receipt.json"
```

## 6. Summary / Review Step

Review the generated `summary` and `receipt`:

```bash
sed -n '1,120p' "$OUTPUT_DIR/summary.json"
sed -n '1,120p' "$OUTPUT_DIR/receipt.json"
```

## 7. Expected Output Locations

Primary outputs:

- `bundle`: `$OUTPUT_DIR/langchain-evidence.bundle.json`
- `receipt`: `$OUTPUT_DIR/receipt.json`
- `summary`: `$OUTPUT_DIR/summary.json`

Supporting files produced by the same run:

- manifest: `$OUTPUT_DIR/langchain-evidence.manifest.json`
- verification key: `$OUTPUT_DIR/manifest-public.pem`
- local runtime capture: `$OUTPUT_DIR/runtime-events.jsonl`

## 8. Smoke Checklist

- `pip install -e ".[langchain,signing]"` completes successfully
- `python examples/langchain_minimal_evidence.py --output-dir "$OUTPUT_DIR"` exits with `ok: true`
- `$OUTPUT_DIR/langchain-evidence.bundle.json` exists
- `agent-evidence verify-export ... > "$OUTPUT_DIR/receipt.json"` exits successfully
- `$OUTPUT_DIR/receipt.json` contains `"ok": true`
- `$OUTPUT_DIR/summary.json` exists and contains the generated review summary
