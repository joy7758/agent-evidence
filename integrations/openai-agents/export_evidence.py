from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def _compute_hash(value: Any) -> str:
    payload = json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def capture_runtime_trace() -> dict[str, Any]:
    return {
        "agent_framework": "openai-agents",
        "run_id": "run-openai-001",
        "agent_id": "assistant",
        "steps": [
            {
                "id": "span-1",
                "type": "tool.call",
                "name": "weather.lookup",
                "status": "completed",
            }
        ],
        "context": {
            "source": "openai-agents",
            "scenario": "integration-demo",
        },
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


def build_runtime_evidence_export(runtime_trace: dict[str, Any]) -> dict[str, Any]:
    steps = [
        {
            "step_id": step["id"],
            "step_type": step["type"],
            "action": step["name"],
            "status": step["status"],
        }
        for step in runtime_trace["steps"]
    ]
    context = {
        "agent_id": runtime_trace["agent_id"],
        "source": runtime_trace["context"]["source"],
        "scenario": runtime_trace["context"]["scenario"],
    }
    action_hash = "sha256:" + _compute_hash(steps)
    trace_hash = "sha256:" + _compute_hash(
        {
            "agent_framework": runtime_trace["agent_framework"],
            "run_id": runtime_trace["run_id"],
            "steps": steps,
            "context": context,
            "timestamp": runtime_trace["timestamp"],
        }
    )
    proof_hash = "sha256:" + _compute_hash(
        {
            "action_hash": action_hash,
            "trace_hash": trace_hash,
        }
    )
    return {
        "object_type": "runtime-evidence-export",
        "agent_framework": runtime_trace["agent_framework"],
        "run_id": runtime_trace["run_id"],
        "steps": steps,
        "hashes": {
            "action_hash": action_hash,
            "trace_hash": trace_hash,
            "proof_hash": proof_hash,
        },
        "context": context,
        "timestamp": runtime_trace["timestamp"],
    }


def export_json_evidence_bundle(output_path: str | Path) -> Path:
    runtime_trace = capture_runtime_trace()
    runtime_evidence_export = build_runtime_evidence_export(runtime_trace)
    target = Path(output_path)
    target.write_text(json.dumps(runtime_evidence_export, indent=2) + "\n", encoding="utf-8")
    return target


if __name__ == "__main__":
    destination = Path(__file__).with_name("openai-runtime-evidence-export.json")
    written = export_json_evidence_bundle(destination)
    print(written)
