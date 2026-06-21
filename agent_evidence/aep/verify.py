from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

from .bundle import MANIFEST_FILENAME, RECORDS_FILENAME, load_bundle_payload
from .hash_chain import (
    compute_bundle_root_hash,
    compute_payload_hash,
    compute_record_hash,
)

SCHEMA_PATH = Path(__file__).with_name("schema_v0.1.json")


def _issue(stage: str, code: str, path: str, message: str) -> dict[str, str]:
    return {
        "stage": stage,
        "code": code,
        "path": path,
        "message": message,
    }


def _validate_schema(
    bundle_payload: dict[str, Any], schema_path: str | Path
) -> list[dict[str, str]]:
    schema = json.loads(Path(schema_path).read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema)
    issues: list[dict[str, str]] = []
    for error in sorted(validator.iter_errors(bundle_payload), key=lambda item: list(item.path)):
        path = ".".join(str(part) for part in error.path) or "root"
        issues.append(_issue("schema", "schema_violation", path, error.message))
    return issues


def _validate_integrity(
    manifest: dict[str, Any], records: list[dict[str, Any]]
) -> list[dict[str, str]]:
    issues: list[dict[str, str]] = []
    expected_prev_hash: str | None = None
    record_hashes: list[str] = []

    for index, record in enumerate(records):
        expected_payload_hash = compute_payload_hash(record.get("payload"))
        if record.get("payload_hash") != expected_payload_hash:
            issues.append(
                _issue(
                    "integrity",
                    "payload_hash_mismatch",
                    f"records[{index}].payload_hash",
                    "payload_hash does not match canonical payload.",
                )
            )

        expected_record_hash = compute_record_hash(
            schema_version=str(record.get("schema_version")),
            run_id=str(record.get("run_id")),
            event_type=str(record.get("event_type")),
            timestamp=str(record.get("timestamp")),
            payload_hash=str(record.get("payload_hash")),
            prev_hash=record.get("prev_hash"),
        )
        if record.get("record_hash") != expected_record_hash:
            issues.append(
                _issue(
                    "integrity",
                    "record_hash_mismatch",
                    f"records[{index}].record_hash",
                    "record_hash does not match record fields.",
                )
            )

        if record.get("prev_hash") != expected_prev_hash:
            issues.append(
                _issue(
                    "integrity",
                    "prev_hash_mismatch",
                    f"records[{index}].prev_hash",
                    "prev_hash does not point to the previous record_hash.",
                )
            )

        record_hashes.append(str(record.get("record_hash")))
        expected_prev_hash = str(record.get("record_hash"))

    expected_root_hash = compute_bundle_root_hash(record_hashes)
    if manifest.get("bundle_root_hash") != expected_root_hash:
        issues.append(
            _issue(
                "integrity",
                "bundle_root_hash_mismatch",
                "manifest.bundle_root_hash",
                "manifest bundle_root_hash does not match the record hash chain.",
            )
        )
    if manifest.get("record_count") != len(records):
        issues.append(
            _issue(
                "integrity",
                "record_count_mismatch",
                "manifest.record_count",
                "manifest record_count does not match the number of records.",
            )
        )

    for index, record in enumerate(records):
        if record.get("bundle_root_hash") != expected_root_hash:
            issues.append(
                _issue(
                    "integrity",
                    "record_bundle_root_hash_mismatch",
                    f"records[{index}].bundle_root_hash",
                    "record bundle_root_hash does not match the manifest root hash.",
                )
            )
    return issues


def _validate_semantics(
    manifest: dict[str, Any], records: list[dict[str, Any]]
) -> list[dict[str, str]]:
    issues: list[dict[str, str]] = []
    previous_timestamp: datetime | None = None

    for index, record in enumerate(records):
        if record.get("run_id") != manifest.get("run_id"):
            issues.append(
                _issue(
                    "semantic",
                    "run_id_mismatch",
                    f"records[{index}].run_id",
                    "record run_id must match manifest run_id.",
                )
            )

        try:
            current_timestamp = datetime.fromisoformat(str(record.get("timestamp")))
        except ValueError:
            issues.append(
                _issue(
                    "semantic",
                    "timestamp_invalid",
                    f"records[{index}].timestamp",
                    "timestamp must be a valid ISO-8601 string.",
                )
            )
        else:
            if previous_timestamp is not None and current_timestamp < previous_timestamp:
                issues.append(
                    _issue(
                        "semantic",
                        "timestamp_out_of_order",
                        f"records[{index}].timestamp",
                        "timestamps must be non-decreasing within one bundle.",
                    )
                )
            previous_timestamp = current_timestamp

        if str(record.get("event_type", "")).endswith(".token"):
            issues.append(
                _issue(
                    "semantic",
                    "token_event_disallowed",
                    f"records[{index}].event_type",
                    "token-level events are not allowed in the evidence profile.",
                )
            )

        payload = record.get("payload") or {}
        if manifest.get("privacy_mode") == "digest_only":
            for slot_name in ("request", "response"):
                slot = payload.get(slot_name)
                if isinstance(slot, dict) and "content" in slot:
                    issues.append(
                        _issue(
                            "semantic",
                            "privacy_mode_violation",
                            f"records[{index}].payload.{slot_name}.content",
                            "digest_only bundles must not store plaintext "
                            "request/response content.",
                        )
                    )

        attributes = payload.get("attributes") or {}
        openinference = attributes.get("openinference") or {}
        if openinference and not isinstance(openinference.get("span_kind"), str):
            issues.append(
                _issue(
                    "semantic",
                    "openinference_span_kind_invalid",
                    f"records[{index}].payload.attributes.openinference.span_kind",
                    "OpenInference-compatible span_kind must be a string when present.",
                )
            )
        gen_ai = attributes.get("gen_ai") or {}
        if gen_ai and not isinstance(gen_ai.get("operation_name"), str):
            issues.append(
                _issue(
                    "semantic",
                    "otel_operation_name_invalid",
                    f"records[{index}].payload.attributes.gen_ai.operation_name",
                    "OTel-compatible gen_ai.operation_name must be a string when present.",
                )
            )

    return issues


def verify_bundle(
    bundle_dir: str | Path,
    *,
    schema_path: str | Path = SCHEMA_PATH,
) -> dict[str, Any]:
    target_dir = Path(bundle_dir)
    report = {
        "ok": False,
        "bundle_dir": str(target_dir),
        "stages": [],
    }

    parse_issues: list[dict[str, str]] = []
    if not (target_dir / MANIFEST_FILENAME).exists():
        parse_issues.append(
            _issue("parse", "manifest_missing", MANIFEST_FILENAME, "manifest.json is missing.")
        )
    if not (target_dir / RECORDS_FILENAME).exists():
        parse_issues.append(
            _issue("parse", "records_missing", RECORDS_FILENAME, "records.jsonl is missing.")
        )

    bundle_payload: dict[str, Any] | None = None
    if not parse_issues:
        try:
            bundle_payload = load_bundle_payload(target_dir)
        except json.JSONDecodeError as exc:
            parse_issues.append(
                _issue("parse", "json_decode_error", "bundle", f"Invalid JSON: {exc.msg}")
            )
        except OSError as exc:
            parse_issues.append(_issue("parse", "bundle_read_error", "bundle", str(exc)))

    report["stages"].append(
        {
            "name": "parse",
            "ok": not parse_issues,
            "issues": parse_issues,
        }
    )
    if parse_issues or bundle_payload is None:
        report["stages"].extend(
            [
                {
                    "name": "schema",
                    "ok": False,
                    "issues": [
                        _issue("schema", "skipped", "schema", "Skipped because parse failed.")
                    ],
                },
                {
                    "name": "integrity",
                    "ok": False,
                    "issues": [
                        _issue(
                            "integrity",
                            "skipped",
                            "integrity",
                            "Skipped because parse failed.",
                        )
                    ],
                },
                {
                    "name": "semantic",
                    "ok": False,
                    "issues": [
                        _issue("semantic", "skipped", "semantic", "Skipped because parse failed.")
                    ],
                },
            ]
        )
        return report

    schema_issues = _validate_schema(bundle_payload, schema_path)
    report["stages"].append(
        {
            "name": "schema",
            "ok": not schema_issues,
            "issues": schema_issues,
        }
    )
    if schema_issues:
        report["stages"].extend(
            [
                {
                    "name": "integrity",
                    "ok": False,
                    "issues": [
                        _issue(
                            "integrity",
                            "skipped",
                            "integrity",
                            "Skipped because schema failed.",
                        )
                    ],
                },
                {
                    "name": "semantic",
                    "ok": False,
                    "issues": [
                        _issue("semantic", "skipped", "semantic", "Skipped because schema failed.")
                    ],
                },
            ]
        )
        return report

    manifest = bundle_payload["manifest"]
    records = bundle_payload["records"]
    integrity_issues = _validate_integrity(manifest, records)
    semantic_issues = _validate_semantics(manifest, records)
    report["stages"].append(
        {
            "name": "integrity",
            "ok": not integrity_issues,
            "issues": integrity_issues,
        }
    )
    report["stages"].append(
        {
            "name": "semantic",
            "ok": not semantic_issues,
            "issues": semantic_issues,
        }
    )
    report["ok"] = all(stage["ok"] for stage in report["stages"])
    return report
