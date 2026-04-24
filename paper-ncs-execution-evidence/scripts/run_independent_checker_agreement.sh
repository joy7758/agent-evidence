#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PAPER_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
CODE_ROOT="${CODE_ROOT:-$(cd "$PAPER_ROOT/.." && pwd)}"
PACK_ROOT="${1:-$PAPER_ROOT/paper_packs/scientific_workflow_public}"

cd "$CODE_ROOT"
if [ "$(basename "$PACK_ROOT")" = "scientific_workflow_public" ]; then
  python "$PAPER_ROOT/scripts/build_public_scientific_workflow_pack.py" \
    --pack "$PACK_ROOT" \
    --force
elif [ "$(basename "$PACK_ROOT")" = "scientific_workflow" ]; then
  python "$PAPER_ROOT/scripts/build_scientific_workflow_pack.py" \
    --pack "$PACK_ROOT" \
    --force
fi

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

RESULT_JSON="$PACK_ROOT/independent_checker_agreement.json"
RESULT_MD="$PACK_ROOT/independent_checker_agreement.md"

python - "$PACK_ROOT" "$AGENT_EVIDENCE" "$PAPER_ROOT/scripts/independent_check_ncs_pack.py" "$RESULT_JSON" "$RESULT_MD" <<'PY'
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

pack_root = Path(sys.argv[1])
agent_evidence = sys.argv[2]
checker = sys.argv[3]
result_json = Path(sys.argv[4])
result_md = Path(sys.argv[5])

classes = {
    0: "PASS",
    2: "CONTENT_OR_DIGEST_MISMATCH",
    3: "INCOMPLETE_EVIDENCE",
    4: "VERSION_OR_PROFILE_MISMATCH",
    5: "POLICY_LINKAGE_FAILURE",
    6: "TEMPORAL_INCONSISTENCY",
    7: "OUTCOME_UNVERIFIABLE",
    8: "IMPLEMENTATION_COUPLING",
    9: "AMBIGUOUS_OPERATION",
    10: "SIGNATURE_OR_KEY_FAILURE",
    11: "REFERENCE_RESOLUTION_FAILURE",
}
descriptions = {
    0: "Pack satisfies profile and verification checks.",
    2: "Recomputed content digest differs from the declared digest.",
    4: "Pack declares an unsupported profile version.",
    5: "Policy reference or policy digest linkage is broken.",
    6: "Execution and validation timestamps violate required ordering.",
    7: "Claimed outcome cannot be linked to digest-backed primary output evidence.",
    11: "Referenced evidence artifact cannot be resolved inside the pack.",
}
cases = [
    ("scientific_workflow_public", pack_root, 0),
    ("failures/tampered_input", pack_root / "failures" / "tampered_input", 2),
    ("failures/tampered_output", pack_root / "failures" / "tampered_output", 2),
    ("failures/missing_policy", pack_root / "failures" / "missing_policy", 5),
    ("failures/broken_evidence_link", pack_root / "failures" / "broken_evidence_link", 11),
    ("failures/version_mismatch", pack_root / "failures" / "version_mismatch", 4),
    ("failures/temporal_inconsistency", pack_root / "failures" / "temporal_inconsistency", 6),
    ("failures/outcome_unverifiable", pack_root / "failures" / "outcome_unverifiable", 7),
]

rows = []
status = 0
for name, path, expected in cases:
    repo = subprocess.run(
        [agent_evidence, "validate-pack", "--pack", str(path), "--strict"],
        text=True,
        capture_output=True,
        check=False,
    )
    independent = subprocess.run(
        [sys.executable, checker, "--pack", str(path), "--strict", "--json"],
        text=True,
        capture_output=True,
        check=False,
    )
    try:
        independent_payload = json.loads(independent.stdout)
    except json.JSONDecodeError:
        independent_payload = {
            "failure_class": "UNPARSEABLE",
            "reason": independent.stdout[:1000] or independent.stderr[:1000],
        }
    repo_code = repo.returncode
    independent_code = independent.returncode
    expected_class = classes[expected]
    agreement = (
        repo_code == expected
        and independent_code == expected
        and independent_payload.get("failure_class") == expected_class
    )
    if not agreement:
        status = 1
    rows.append(
        {
            "case": name,
            "description": descriptions.get(expected, expected_class),
            "expected_exit_code": expected,
            "expected_failure_class": expected_class,
            "repository_exit_code": repo_code,
            "repository_stdout": repo.stdout[:1000],
            "repository_stderr": repo.stderr[:1000],
            "independent_exit_code": independent_code,
            "independent_failure_class": independent_payload.get("failure_class"),
            "independent_reason": independent_payload.get("reason"),
            "agreement": agreement,
        }
    )

payload = {
    "pack": str(pack_root),
    "repository_validator": f"{agent_evidence} validate-pack --pack <pack> --strict",
    "independent_checker": checker,
    "overall_agreement": all(row["agreement"] for row in rows),
    "rows": rows,
}
result_json.write_text(json.dumps(payload, ensure_ascii=False, sort_keys=True, indent=2) + "\n", encoding="utf-8")

lines = [
    "# Independent checker agreement table",
    "",
    f"Pack: `{pack_root}`",
    "",
    "| Case | Description | Expected class | Expected code | Repository code | Independent class | Independent code | Agreement |",
    "|---|---|---|---:|---:|---|---:|---:|",
]
for row in rows:
    lines.append(
        "| {case} | {description} | {expected_failure_class} | {expected_exit_code} | {repository_exit_code} | {independent_failure_class} | {independent_exit_code} | {agreement} |".format(
            **row
        )
    )
result_md.write_text("\n".join(lines) + "\n", encoding="utf-8")

print(f"Wrote {result_json}")
print(f"Wrote {result_md}")
print("case expected repo independent class agreement")
for row in rows:
    print(
        row["case"],
        row["expected_exit_code"],
        row["repository_exit_code"],
        row["independent_exit_code"],
        row["independent_failure_class"],
        row["agreement"],
    )
raise SystemExit(status)
PY
