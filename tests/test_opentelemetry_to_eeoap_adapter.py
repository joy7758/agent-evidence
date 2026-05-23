from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

from agent_evidence.oap import validate_profile_file

ROOT = Path(__file__).resolve().parents[1]
ADAPTER = ROOT / "tools" / "opentelemetry_to_eeoap_adapter.py"
FIXTURES = ROOT / "examples" / "opentelemetry"


def run_adapter(fixture_name: str, tmp_path: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [
            sys.executable,
            str(ADAPTER),
            str(FIXTURES / fixture_name),
            "--output-dir",
            str(tmp_path / "generated"),
        ],
        cwd=ROOT,
        check=False,
        text=True,
        capture_output=True,
    )


def load_report(tmp_path: Path, fixture_name: str) -> dict[str, object]:
    case_name = Path(fixture_name).stem
    report_path = tmp_path / "generated" / f"{case_name}-adapter-report.json"
    return json.loads(report_path.read_text(encoding="utf-8"))


def test_valid_trace_produces_eeoap_statement_and_report(tmp_path: Path) -> None:
    result = run_adapter("valid-agent-trace.json", tmp_path)

    assert result.returncode == 0, result.stderr

    statement_path = tmp_path / "generated" / "valid-agent-trace-eeoap-statement.json"
    report_path = tmp_path / "generated" / "valid-agent-trace-adapter-report.json"
    assert statement_path.exists()
    assert report_path.exists()

    statement = json.loads(statement_path.read_text(encoding="utf-8"))
    assert statement["profile"] == {
        "name": "execution-evidence-operation-accountability-profile",
        "version": "0.1",
    }
    assert statement["actor"]["id"] == "agent:research-assistant-001"
    assert statement["operation"]["type"] == "research.answer"
    assert statement["subject"]["id"] == "otel-trace:aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"

    artifact_ids = {artifact["artifact_id"] for artifact in statement["evidence"]["artifacts"]}
    assert "artifact:otel-agent-span:1111111111111111" in artifact_ids
    assert "artifact:otel-tool-span:2222222222222222" in artifact_ids
    assert "artifact:otel-tool-span:3333333333333333" in artifact_ids

    report = json.loads(report_path.read_text(encoding="utf-8"))
    assert report["ok"] is True
    assert report["diagnostics"] == []
    extracted = report["extracted"]
    assert extracted["trace_id"] == "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
    assert extracted["span_id"] == "1111111111111111"
    assert extracted["parent_span_id"] == ""
    assert extracted["agent"] == {
        "id": "agent:research-assistant-001",
        "name": "research-assistant",
        "version": "0.1.0",
    }
    assert extracted["operation_name"] == "research.answer"
    assert len(extracted["tool_spans"]) == 2


def test_generated_statement_passes_existing_eeoap_validator(tmp_path: Path) -> None:
    result = run_adapter("valid-agent-trace.json", tmp_path)

    assert result.returncode == 0, result.stderr

    statement_path = tmp_path / "generated" / "valid-agent-trace-eeoap-statement.json"
    validation_report = validate_profile_file(statement_path)

    assert validation_report["ok"] is True
    assert validation_report["issue_count"] == 0


def test_valid_workflow_trace_produces_eeoap_statement_and_report(tmp_path: Path) -> None:
    result = run_adapter("valid-agent-workflow-trace.json", tmp_path)

    assert result.returncode == 0, result.stderr

    statement_path = tmp_path / "generated" / "valid-agent-workflow-trace-eeoap-statement.json"
    report_path = tmp_path / "generated" / "valid-agent-workflow-trace-adapter-report.json"
    assert statement_path.exists()
    assert report_path.exists()

    statement = json.loads(statement_path.read_text(encoding="utf-8"))
    assert statement["profile"] == {
        "name": "execution-evidence-operation-accountability-profile",
        "version": "0.1",
    }
    assert statement["actor"]["id"] == "agent:workflow-coordinator-002"
    assert statement["operation"]["type"] == "workflow.execute"
    assert statement["subject"]["id"] == "otel-trace:bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb"

    artifact_ids = {artifact["artifact_id"] for artifact in statement["evidence"]["artifacts"]}
    assert "artifact:otel-agent-span:4444444444444444" in artifact_ids
    assert "artifact:otel-tool-span:6666666666666666" in artifact_ids
    assert "artifact:otel-tool-span:7777777777777777" in artifact_ids

    report = json.loads(report_path.read_text(encoding="utf-8"))
    assert report["ok"] is True
    assert report["diagnostics"] == []
    extracted = report["extracted"]
    assert extracted["trace_id"] == "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb"
    assert extracted["span_id"] == "4444444444444444"
    assert extracted["parent_span_id"] == ""
    assert extracted["agent"] == {
        "id": "agent:workflow-coordinator-002",
        "name": "workflow-coordinator",
        "version": "0.2.0",
    }
    assert extracted["operation_name"] == "workflow.execute"
    assert len(extracted["tool_spans"]) == 2
    assert {span["parent_span_id"] for span in extracted["tool_spans"]} == {"5555555555555555"}


def test_generated_workflow_statement_passes_existing_eeoap_validator(tmp_path: Path) -> None:
    result = run_adapter("valid-agent-workflow-trace.json", tmp_path)

    assert result.returncode == 0, result.stderr

    statement_path = tmp_path / "generated" / "valid-agent-workflow-trace-eeoap-statement.json"
    validation_report = validate_profile_file(statement_path)

    assert validation_report["ok"] is True
    assert validation_report["issue_count"] == 0


@pytest.mark.parametrize(
    ("fixture_name", "expected_code"),
    [
        ("invalid-missing-agent-span.json", "missing_agent_span"),
        ("invalid-unresolved-tool-span.json", "unresolved_tool_span"),
        ("invalid-broken-parent-span.json", "broken_parent_span_relation"),
        ("invalid-missing-operation-name.json", "missing_operation_name"),
    ],
)
def test_invalid_trace_fails_at_expected_adapter_diagnostic_surface(
    fixture_name: str,
    expected_code: str,
    tmp_path: Path,
) -> None:
    result = run_adapter(fixture_name, tmp_path)

    assert result.returncode != 0
    assert expected_code in result.stderr

    report = load_report(tmp_path, fixture_name)
    assert report["ok"] is False
    diagnostics = report["diagnostics"]
    assert diagnostics
    assert diagnostics[0]["code"] == expected_code

    case_name = Path(fixture_name).stem
    statement_path = tmp_path / "generated" / f"{case_name}-eeoap-statement.json"
    assert not statement_path.exists()
