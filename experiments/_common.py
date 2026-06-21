from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
RESULTS_DIR = ROOT / "experiments" / "results"

sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

from agent_evidence.oap import build_validation_report  # noqa: E402
from convert_otel_trace_to_eeoap import flatten_spans  # noqa: E402


def repo_locator(path: Path) -> str:
    resolved = path.resolve()
    try:
        return resolved.relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def load_json(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return payload


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def validate_profile(profile: dict[str, Any], source: str) -> dict[str, Any]:
    return build_validation_report(profile, source=source, fail_fast=False)


def experiment_result(
    *,
    experiment_id: str,
    description: str,
    source_type: str,
    trace: dict[str, Any],
    output_profile: Path,
    validation_report: dict[str, Any],
    extra: dict[str, Any] | None = None,
) -> dict[str, Any]:
    spans = flatten_spans(trace)
    result = {
        "experiment_id": experiment_id,
        "description": description,
        "source_type": source_type,
        "span_count": len(spans),
        "output_profile": repo_locator(output_profile),
        "validator_ok": validation_report["ok"],
        "issue_count": validation_report["issue_count"],
        "primary_error_code": validation_report["primary_error_code"],
        "affected_clauses": ["EEOAP-001", "EEOAP-002", "EEOAP-003", "EEOAP-004", "EEOAP-005"],
        "boundary": (
            "Local experiment receipt only; not production telemetry, external validation, "
            "certification, publication status, or deployment proof."
        ),
    }
    if extra:
        result.update(extra)
    return result
