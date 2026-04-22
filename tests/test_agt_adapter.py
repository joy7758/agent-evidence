from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from agent_evidence.oap import validate_profile_file

ROOT = Path(__file__).resolve().parents[1]
AGT_DIR = ROOT / "integrations" / "agt"
CONVERTER = AGT_DIR / "convert_agt_evidence_to_eeoap.py"
FIXTURE = AGT_DIR / "fixtures" / "agt-evidence-minimal.synthetic.json"
EXPECTED = AGT_DIR / "fixtures" / "eeoap-from-agt.expected.json"


def test_agt_adapter_generates_valid_eeoap_statement(tmp_path: Path) -> None:
    output = tmp_path / "eeoap-from-agt.generated.json"

    subprocess.run(
        [
            sys.executable,
            str(CONVERTER),
            "--input",
            str(FIXTURE),
            "--output",
            str(output),
        ],
        check=True,
        cwd=ROOT,
    )

    generated = json.loads(output.read_text(encoding="utf-8"))
    expected = json.loads(EXPECTED.read_text(encoding="utf-8"))
    assert generated == expected

    report = validate_profile_file(output)
    assert report["ok"] is True
    assert report["issue_count"] == 0

    expected_top_level = {
        "profile",
        "statement_id",
        "timestamp",
        "actor",
        "subject",
        "operation",
        "policy",
        "constraints",
        "provenance",
        "evidence",
        "validation",
    }
    assert set(generated) == expected_top_level
    assert not {"agent", "action", "policy_decision", "audit_artifact"} & set(generated)
    assert all(not key.startswith("agt_") for key in generated)

    artifact_ids = {artifact["artifact_id"] for artifact in generated["evidence"]["artifacts"]}
    assert "artifact:agt-runtime-evidence-001" in artifact_ids
    assert "artifact:agt-decision-receipt-001" in artifact_ids
