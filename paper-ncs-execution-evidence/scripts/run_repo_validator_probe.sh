#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PAPER_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
CODE_ROOT="${CODE_ROOT:-$(cd "$PAPER_ROOT/.." && pwd)}"
PACK="$PAPER_ROOT/paper_packs/scientific_workflow"
SUMMARY="$PACK/repo_validator_probe_summary.txt"
AGENT_EVIDENCE="$CODE_ROOT/.venv/bin/agent-evidence"

cd "$CODE_ROOT"
python "$PAPER_ROOT/scripts/build_scientific_workflow_pack.py" \
  --pack "$PACK" \
  --force
python "$PAPER_ROOT/scripts/build_repo_compat_artifacts.py" \
  --pack "$PACK"

: > "$SUMMARY"
{
  echo "Repository validator probe summary"
  echo "Pack: $PACK"
  echo "Agent evidence command: $AGENT_EVIDENCE"
  echo
} >> "$SUMMARY"

run_probe() {
  local name="$1"
  shift
  {
    echo "---- $name ----"
    echo "$*"
  } >> "$SUMMARY"
  set +e
  "$@" >> "$SUMMARY" 2>&1
  local code=$?
  set -e
  echo "exit_code=$code" >> "$SUMMARY"
  echo >> "$SUMMARY"
  printf "%-62s %s\n" "$name" "$code"
}

printf "%-62s %s\n" "probe" "exit"
if [ -x "$AGENT_EVIDENCE" ]; then
  run_probe \
    "validate-profile compat operation accountability statement" \
    "$AGENT_EVIDENCE" validate-profile "$PACK/repo_compat/operation_accountability_statement.json"
  run_probe \
    "validate-profile native NCS bundle" \
    "$AGENT_EVIDENCE" validate-profile "$PACK/bundle.json"
  run_probe \
    "validate-profile NCS bundle view" \
    "$AGENT_EVIDENCE" validate-profile "$PACK/repo_compat/ncs_bundle_view.json"
  run_probe \
    "verify-bundle NCS pack directory" \
    "$AGENT_EVIDENCE" verify-bundle --bundle-dir "$PACK"
else
  echo "SKIP: .venv/bin/agent-evidence is not executable" | tee -a "$SUMMARY"
fi

{
  echo "---- repo validator adapter ----"
} >> "$SUMMARY"
set +e
python "$PAPER_ROOT/scripts/repo_validator_adapter.py" --pack "$PACK" >> "$SUMMARY" 2>&1
adapter_code=$?
set -e
echo "exit_code=$adapter_code" >> "$SUMMARY"
printf "%-62s %s\n" "repo validator adapter" "$adapter_code"

echo "Wrote $SUMMARY"
