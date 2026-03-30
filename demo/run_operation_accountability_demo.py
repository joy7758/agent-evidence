#!/usr/bin/env python3
from __future__ import annotations

import copy
import json
import sys
from pathlib import Path

DEMO_ROOT = Path(__file__).resolve().parent
REPO_ROOT = DEMO_ROOT.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from agent_evidence.oap import (  # noqa: E402
    render_summary_lines,
    sha256_digest,
    validate_profile_file,
    with_recomputed_integrity,
)

ARTIFACTS_DIR = DEMO_ROOT / "artifacts"


def write_json(path: Path, payload: object) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def load_source_object() -> dict[str, object]:
    return {
        "object_id": "obj:client-note-001",
        "type": "client-note",
        "content": "Client asked for the next delivery estimate and follow-up report.",
        "metadata": {
            "source": "visit-note",
            "owner": "sales-ops",
        },
    }


def profile_precheck(source_object: dict[str, object]) -> list[str]:
    issues: list[str] = []
    for field in ("object_id", "type", "content", "metadata"):
        if field not in source_object:
            issues.append(f"missing source field: {field}")
    metadata = source_object.get("metadata")
    if not isinstance(metadata, dict):
        issues.append("source metadata must be an object")
    return issues


def apply_operation(
    source_object: dict[str, object],
) -> tuple[dict[str, object], dict[str, object]]:
    derived_object = copy.deepcopy(source_object)
    derived_object["object_id"] = "obj:client-note-001-derived"
    metadata = dict(derived_object["metadata"])
    metadata["review_status"] = "approved"
    metadata["tags"] = ["client-visit", "delivery-follow-up"]
    derived_object["metadata"] = metadata

    operation_log = {
        "operation": "metadata.enrich",
        "policy": "approved-metadata-policy",
        "added_fields": ["review_status", "tags"],
        "content_changed": False,
    }
    return derived_object, operation_log


def build_statement(
    source_object: dict[str, object],
    derived_object: dict[str, object],
    operation_log: dict[str, object],
) -> dict[str, object]:
    statement = {
        "profile": {
            "name": "execution-evidence-operation-accountability-profile",
            "version": "0.1",
        },
        "statement_id": "eeoap:demo-metadata-enrichment-001",
        "timestamp": "2026-03-30T00:00:00Z",
        "actor": {
            "id": "actor:metadata-enricher",
            "type": "agent",
            "name": "metadata-enricher",
            "runtime": "openai-agents",
        },
        "subject": {
            "id": source_object["object_id"],
            "type": "fdo-record",
            "digest": sha256_digest(source_object),
            "locator": "demo/artifacts/input-object.json",
        },
        "operation": {
            "id": "op:metadata-enrich-001",
            "type": "metadata.enrich",
            "description": "Add approved metadata tags to one client note object.",
            "subject_ref": source_object["object_id"],
            "policy_ref": "policy:approved-metadata-v1",
            "input_refs": ["ref:input-note"],
            "output_refs": ["ref:output-note"],
            "result": {
                "status": "succeeded",
                "summary": "one derived note object emitted",
            },
        },
        "policy": {
            "id": "policy:approved-metadata-v1",
            "name": "approved-metadata-policy",
            "constraint_refs": [
                "constraint:approved-fields",
                "constraint:no-content-rewrite",
            ],
        },
        "constraints": [
            {
                "id": "constraint:approved-fields",
                "description": "Only approved metadata fields may be added.",
            },
            {
                "id": "constraint:no-content-rewrite",
                "description": "The note body must remain unchanged.",
            },
        ],
        "provenance": {
            "id": "prov:metadata-enrich-001",
            "actor_ref": "actor:metadata-enricher",
            "operation_ref": "op:metadata-enrich-001",
            "subject_ref": source_object["object_id"],
            "input_refs": ["ref:input-note"],
            "output_refs": ["ref:output-note"],
        },
        "evidence": {
            "id": "evidence:metadata-enrich-001",
            "subject_ref": source_object["object_id"],
            "operation_ref": "op:metadata-enrich-001",
            "policy_ref": "policy:approved-metadata-v1",
            "references": [
                {
                    "ref_id": "ref:input-note",
                    "role": "input",
                    "object_id": source_object["object_id"],
                    "digest": sha256_digest(source_object),
                    "locator": "demo/artifacts/input-object.json",
                },
                {
                    "ref_id": "ref:output-note",
                    "role": "output",
                    "object_id": derived_object["object_id"],
                    "digest": sha256_digest(derived_object),
                    "locator": "demo/artifacts/derived-object.json",
                },
            ],
            "artifacts": [
                {
                    "artifact_id": "artifact:operation-log-001",
                    "type": "execution-log",
                    "digest": sha256_digest(operation_log),
                    "locator": "demo/artifacts/operation-log.json",
                }
            ],
            "integrity": {},
        },
        "validation": {
            "id": "validation:metadata-enrich-001",
            "evidence_ref": "evidence:metadata-enrich-001",
            "provenance_ref": "prov:metadata-enrich-001",
            "policy_ref": "policy:approved-metadata-v1",
            "validator": "agent-evidence validate-profile",
            "method": "schema+reference+consistency",
            "status": "verifiable",
        },
    }
    return with_recomputed_integrity(statement)


def main() -> int:
    ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)

    print("Step 1: object load or creation")
    source_object = load_source_object()
    write_json(ARTIFACTS_DIR / "input-object.json", source_object)
    print(f"- loaded {source_object['object_id']}")

    print("Step 2: profile precheck")
    precheck_issues = profile_precheck(source_object)
    if precheck_issues:
        for issue in precheck_issues:
            print(f"- {issue}")
        return 1
    print("- source object is ready for the minimal profile")

    print("Step 3: operation call")
    derived_object, operation_log = apply_operation(source_object)
    write_json(ARTIFACTS_DIR / "derived-object.json", derived_object)
    write_json(ARTIFACTS_DIR / "operation-log.json", operation_log)
    print(f"- emitted {derived_object['object_id']}")

    print("Step 4: evidence generation")
    statement = build_statement(source_object, derived_object, operation_log)
    statement_path = ARTIFACTS_DIR / "minimal-profile-evidence.json"
    write_json(statement_path, statement)
    print(f"- wrote {statement_path.name}")

    print("Step 5: validator verification")
    report = validate_profile_file(statement_path)
    report_path = ARTIFACTS_DIR / "validation-report.json"
    write_json(report_path, report)
    for line in render_summary_lines(
        {
            "ok": report["ok"],
            "profile": report["profile"],
            "source": report["source"],
            "issue_count": report["issue_count"],
            "issues": [issue for stage in report["stages"] for issue in stage["issues"]],
        }
    ):
        print(f"- {line}")

    print("Step 6: output verification result")
    print(f"- evidence: {statement_path}")
    print(f"- report:   {report_path}")
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
