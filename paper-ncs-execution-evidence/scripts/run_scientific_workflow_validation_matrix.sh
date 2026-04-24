#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PAPER_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
CODE_ROOT="${CODE_ROOT:-$(cd "$PAPER_ROOT/.." && pwd)}"
if [ "${1:-}" ]; then
  PACK_ROOT="$1"
elif [ -f "$PAPER_ROOT/paper_packs/scientific_workflow_public/manifest.json" ]; then
  PACK_ROOT="$PAPER_ROOT/paper_packs/scientific_workflow_public"
else
  PACK_ROOT="$PAPER_ROOT/paper_packs/scientific_workflow"
fi
PACK_NAME="$(basename "$PACK_ROOT")"

cd "$CODE_ROOT"
if [ "$PACK_NAME" = "scientific_workflow_public" ]; then
  python "$PAPER_ROOT/scripts/build_public_scientific_workflow_pack.py" \
    --pack "$PACK_ROOT" \
    --force
  VALID_CASE_NAME="scientific_workflow_public"
else
  python "$PAPER_ROOT/scripts/build_scientific_workflow_pack.py" \
    --pack "$PACK_ROOT" \
    --force
  VALID_CASE_NAME="scientific_workflow"
fi

if [ -n "${VERIFY_CMD:-}" ]; then
  read -r -a VERIFIER_ARGS <<< "$VERIFY_CMD"
  STRICT_VALIDATOR_SOURCE="env-override"
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

CASES=(
  "$VALID_CASE_NAME|$PACK_ROOT|0"
  "failures/tampered_input|$PACK_ROOT/failures/tampered_input|2"
  "failures/tampered_output|$PACK_ROOT/failures/tampered_output|2"
  "failures/missing_policy|$PACK_ROOT/failures/missing_policy|5"
  "failures/broken_evidence_link|$PACK_ROOT/failures/broken_evidence_link|11"
  "failures/version_mismatch|$PACK_ROOT/failures/version_mismatch|4"
  "failures/temporal_inconsistency|$PACK_ROOT/failures/temporal_inconsistency|6"
  "failures/outcome_unverifiable|$PACK_ROOT/failures/outcome_unverifiable|7"
)

echo "strict validator source: $STRICT_VALIDATOR_SOURCE"
echo "verifier command: ${VERIFIER_ARGS[*]}"
printf "%-42s %8s %8s %s\n" "case" "expected" "actual" "status"
STATUS=0
for item in "${CASES[@]}"; do
  IFS="|" read -r name path expected <<< "$item"
  set +e
  "${VERIFIER_ARGS[@]}" --pack "$path" --strict >/tmp/ncs-validation-result.txt
  actual=$?
  set -e
  if [ "$actual" = "$expected" ]; then
    result="OK"
  else
    result="MISMATCH"
    STATUS=1
  fi
  printf "%-42s %8s %8s %s\n" "$name" "$expected" "$actual" "$result"
done

exit "$STATUS"
