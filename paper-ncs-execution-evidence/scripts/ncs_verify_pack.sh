#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PAPER_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
CODE_ROOT="${CODE_ROOT:-$(cd "$PAPER_ROOT/.." && pwd)}"

if [ "${1:-}" ]; then
  PACK="$1"
elif [ -f "$PAPER_ROOT/paper_packs/scientific_workflow_public/manifest.json" ]; then
  PACK="$PAPER_ROOT/paper_packs/scientific_workflow_public"
else
  PACK="$PAPER_ROOT/paper_packs/scientific_workflow"
fi

if [ ! -d "$PACK" ]; then
  echo "ERROR: pack directory not found: $PACK" >&2
  exit 3
fi

if [ ! -f "$PACK/manifest.json" ]; then
  echo "ERROR: no manifest.json found in $PACK" >&2
  exit 3
fi

if [ -n "${VERIFY_CMD:-}" ]; then
  read -r -a VERIFIER_ARGS <<< "$VERIFY_CMD"
  STRICT_VALIDATOR_SOURCE="env-override"
elif [ -n "${AGENT_EVIDENCE_BIN:-}" ] && "$AGENT_EVIDENCE_BIN" --help 2>&1 | grep -q "validate-pack"; then
  VERIFIER_ARGS=("$AGENT_EVIDENCE_BIN" "validate-pack")
  STRICT_VALIDATOR_SOURCE="repository"
elif [ -x "$CODE_ROOT/.venv/bin/agent-evidence" ] && "$CODE_ROOT/.venv/bin/agent-evidence" --help 2>&1 | grep -q "validate-pack"; then
  VERIFIER_ARGS=("$CODE_ROOT/.venv/bin/agent-evidence" "validate-pack")
  STRICT_VALIDATOR_SOURCE="repository"
elif command -v agent-evidence >/dev/null 2>&1 && agent-evidence --help 2>&1 | grep -q "validate-pack"; then
  VERIFIER_ARGS=("agent-evidence" "validate-pack")
  STRICT_VALIDATOR_SOURCE="repository"
else
  VERIFIER_ARGS=("python" "$PAPER_ROOT/scripts/validate_ncs_pack.py")
  STRICT_VALIDATOR_SOURCE="paper-local-fallback"
fi

echo "Paper root: $PAPER_ROOT"
echo "Code root: $CODE_ROOT"
echo "Pack: $PACK"
echo "Strict validator source: $STRICT_VALIDATOR_SOURCE"
echo "Verifier command: ${VERIFIER_ARGS[*]}"
echo

set +e
cd "$CODE_ROOT"
"${VERIFIER_ARGS[@]}" --pack "$PACK" --strict
CODE=$?
set -e

echo
echo "Verifier exit code: $CODE"
exit "$CODE"
