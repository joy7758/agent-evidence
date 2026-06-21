#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

if [[ -x ".venv/bin/python" ]]; then
  PYTHON_BIN="${PYTHON_BIN:-.venv/bin/python}"
else
  PYTHON_BIN="${PYTHON_BIN:-python3}"
fi

run_agent_evidence() {
  if [[ -n "${AGENT_EVIDENCE_BIN:-}" ]]; then
    "$AGENT_EVIDENCE_BIN" "$@"
  elif [[ -x ".venv/bin/agent-evidence" ]]; then
    .venv/bin/agent-evidence "$@"
  elif command -v agent-evidence >/dev/null; then
    agent-evidence "$@"
  else
    PYTHONPATH="$PWD${PYTHONPATH:+:$PYTHONPATH}" "$PYTHON_BIN" -c \
      'from agent_evidence.cli.main import main; import sys; main(args=sys.argv[1:])' "$@"
  fi
}

if [[ -x ".venv/bin/agent-evidence" ]]; then
  AGENT_EVIDENCE_BIN="${AGENT_EVIDENCE_BIN:-.venv/bin/agent-evidence}"
else
  AGENT_EVIDENCE_BIN="${AGENT_EVIDENCE_BIN:-}"
fi

PAPER_TEST_TARGETS="${PAPER_TEST_TARGETS:-tests/test_cli.py tests/test_aep_profile.py}"

echo "Step 1: Validate schema"
command -v "$PYTHON_BIN" >/dev/null
"$PYTHON_BIN" -m pytest --version >/dev/null
"$PYTHON_BIN" -m json.tool specs/eeoap/v0.1/eeoap.schema.json >/dev/null
run_agent_evidence validate-profile examples/minimal-valid-evidence.json >/dev/null

echo "Step 2: Run real trace conversion"
"$PYTHON_BIN" experiments/exp2_real_trace.py >/dev/null

echo "Step 3: Run baseline comparison"
"$PYTHON_BIN" experiments/baselines/otel_native_vs_eeoap.py >/dev/null

echo "Step 4: Run determinism oracle"
"$PYTHON_BIN" experiments/exp4_determinism_oracle.py >/dev/null

echo "Step 5: Run evaluation suite"
"$PYTHON_BIN" -m pytest -q $PAPER_TEST_TARGETS

echo "Step 6: Generate tables"
"$PYTHON_BIN" experiments/generate_tables.py >/dev/null

echo "DONE: Reproducibility workflow complete"
