#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PAPER_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
CODE_ROOT="${CODE_ROOT:-$(cd "$PAPER_ROOT/.." && pwd)}"
PACK_ROOT="$PAPER_ROOT/paper_packs/scientific_workflow_public"

cd "$CODE_ROOT"
python "$PAPER_ROOT/scripts/build_public_scientific_workflow_pack.py" \
  --pack "$PACK_ROOT" \
  --force

if [ -n "${AGENT_EVIDENCE_BIN:-}" ]; then
  AGENT_EVIDENCE="$AGENT_EVIDENCE_BIN"
elif [ -x "$CODE_ROOT/.venv/bin/agent-evidence" ]; then
  AGENT_EVIDENCE="$CODE_ROOT/.venv/bin/agent-evidence"
elif command -v agent-evidence >/dev/null 2>&1; then
  AGENT_EVIDENCE="agent-evidence"
else
  echo "ERROR: no agent-evidence command found" >&2
  exit 3
fi

CASES=(
  "scientific_workflow_public|$PACK_ROOT|0"
  "failures/tampered_input|$PACK_ROOT/failures/tampered_input|2"
  "failures/tampered_output|$PACK_ROOT/failures/tampered_output|2"
  "failures/missing_policy|$PACK_ROOT/failures/missing_policy|5"
  "failures/broken_evidence_link|$PACK_ROOT/failures/broken_evidence_link|11"
  "failures/version_mismatch|$PACK_ROOT/failures/version_mismatch|4"
  "failures/temporal_inconsistency|$PACK_ROOT/failures/temporal_inconsistency|6"
  "failures/outcome_unverifiable|$PACK_ROOT/failures/outcome_unverifiable|7"
)

echo "repository validator: $AGENT_EVIDENCE validate-pack"
printf "%-42s %8s %8s %s\n" "case" "expected" "observed" "status"
STATUS=0
for item in "${CASES[@]}"; do
  IFS="|" read -r name path expected <<< "$item"
  set +e
  "$AGENT_EVIDENCE" validate-pack --pack "$path" --strict >/tmp/ncs-public-validation-result.txt
  observed=$?
  set -e
  if [ "$observed" = "$expected" ]; then
    result="OK"
  else
    result="MISMATCH"
    STATUS=1
  fi
  printf "%-42s %8s %8s %s\n" "$name" "$expected" "$observed" "$result"
done

exit "$STATUS"
