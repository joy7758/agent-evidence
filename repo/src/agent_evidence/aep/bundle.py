from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from .canonicalizer import canonicalize
from .hash_chain import (
    compute_bundle_root_hash,
    compute_payload_hash,
    compute_record_hash,
)

PROFILE_NAME = "agent-evidence-profile"
SCHEMA_VERSION = "0.1.0"
MANIFEST_FILENAME = "manifest.json"
RECORDS_FILENAME = "records.jsonl"

DEFAULT_COMPATIBILITY_TARGETS = {
    "openinference": {
        "status": "compatible-profile",
        "field_paths": {
            "span_kind": "payload.attributes.openinference.span_kind",
        },
    },
    "opentelemetry": {
        "status": "compatible-profile",
        "field_paths": {
            "gen_ai.system": "payload.attributes.gen_ai.system",
            "gen_ai.operation.name": "payload.attributes.gen_ai.operation_name",
        },
    },
}


def build_record(
    *,
    run_id: str,
    event_type: str,
    timestamp: str,
    payload: Any,
    prev_hash: str | None,
    schema_version: str = SCHEMA_VERSION,
) -> dict[str, Any]:
    normalized_payload = canonicalize(payload)
    payload_hash = compute_payload_hash(normalized_payload)
    record_hash = compute_record_hash(
        schema_version=schema_version,
        run_id=str(run_id),
        event_type=str(event_type),
        timestamp=str(timestamp),
        payload_hash=payload_hash,
        prev_hash=prev_hash,
    )
    return {
        "schema_version": schema_version,
        "run_id": str(run_id),
        "event_type": str(event_type),
        "timestamp": str(timestamp),
        "payload": normalized_payload,
        "payload_hash": payload_hash,
        "record_hash": record_hash,
        "prev_hash": prev_hash,
        "bundle_root_hash": None,
    }


def _finalized_records(records: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], str]:
    record_hashes = [record["record_hash"] for record in records]
    bundle_root_hash = compute_bundle_root_hash(record_hashes)
    finalized: list[dict[str, Any]] = []
    for record in records:
        finalized.append(
            {
                **record,
                "bundle_root_hash": bundle_root_hash,
            }
        )
    return finalized, bundle_root_hash


def build_manifest(
    *,
    run_id: str,
    records: list[dict[str, Any]],
    privacy_mode: str = "digest_only",
    redaction: dict[str, bool] | None = None,
    compatibility_targets: dict[str, Any] | None = None,
    source_runtime: str | None = None,
    capture_mode: str | None = None,
    source_runtime_version: str | None = None,
    source_runtime_commit: str | None = None,
    source_runtime_dirty: bool | None = None,
    source_schema_fingerprint: str | None = None,
    identity_ref: str | None = None,
    policy_ref: str | None = None,
    trace_ref: str | None = None,
    export_warnings: list[str] | None = None,
    omitted_sections: list[str] | None = None,
) -> dict[str, Any]:
    finalized_records, bundle_root_hash = _finalized_records(records)
    del finalized_records
    return {
        "schema_version": SCHEMA_VERSION,
        "profile": PROFILE_NAME,
        "run_id": str(run_id),
        "record_count": len(records),
        "bundle_root_hash": bundle_root_hash,
        "digest_algorithm": "sha256",
        "privacy_mode": privacy_mode,
        "redaction": canonicalize(redaction or {}),
        "records_path": RECORDS_FILENAME,
        "event_types": [record["event_type"] for record in records],
        "compatibility_targets": canonicalize(
            compatibility_targets or DEFAULT_COMPATIBILITY_TARGETS
        ),
        "capture_mode": capture_mode,
        "source_runtime_version": source_runtime_version,
        "source_runtime_commit": source_runtime_commit,
        "source_runtime_dirty": source_runtime_dirty,
        "source_schema_fingerprint": source_schema_fingerprint,
        "identity_ref": identity_ref,
        "policy_ref": policy_ref,
        "trace_ref": trace_ref,
        "source_runtime": source_runtime,
        "export_warnings": canonicalize(export_warnings or []),
        "omitted_sections": canonicalize(omitted_sections or []),
    }


def write_bundle(
    *,
    bundle_dir: str | Path,
    run_id: str,
    records: list[dict[str, Any]],
    privacy_mode: str = "digest_only",
    redaction: dict[str, bool] | None = None,
    compatibility_targets: dict[str, Any] | None = None,
    source_runtime: str | None = None,
    capture_mode: str | None = None,
    source_runtime_version: str | None = None,
    source_runtime_commit: str | None = None,
    source_runtime_dirty: bool | None = None,
    source_schema_fingerprint: str | None = None,
    identity_ref: str | None = None,
    policy_ref: str | None = None,
    trace_ref: str | None = None,
    export_warnings: list[str] | None = None,
    omitted_sections: list[str] | None = None,
) -> Path:
    target_dir = Path(bundle_dir)
    target_dir.mkdir(parents=True, exist_ok=True)

    finalized_records, _ = _finalized_records(records)
    manifest = build_manifest(
        run_id=run_id,
        records=finalized_records,
        privacy_mode=privacy_mode,
        redaction=redaction,
        compatibility_targets=compatibility_targets,
        source_runtime=source_runtime,
        capture_mode=capture_mode,
        source_runtime_version=source_runtime_version,
        source_runtime_commit=source_runtime_commit,
        source_runtime_dirty=source_runtime_dirty,
        source_schema_fingerprint=source_schema_fingerprint,
        identity_ref=identity_ref,
        policy_ref=policy_ref,
        trace_ref=trace_ref,
        export_warnings=export_warnings,
        omitted_sections=omitted_sections,
    )
    manifest_path = target_dir / MANIFEST_FILENAME
    records_path = target_dir / RECORDS_FILENAME
    manifest_path.write_text(
        json.dumps(canonicalize(manifest), indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    with records_path.open("w", encoding="utf-8") as handle:
        for record in finalized_records:
            handle.write(json.dumps(canonicalize(record), sort_keys=True))
            handle.write("\n")
    return target_dir


def load_bundle_payload(bundle_dir: str | Path) -> dict[str, Any]:
    target_dir = Path(bundle_dir)
    manifest = json.loads((target_dir / MANIFEST_FILENAME).read_text(encoding="utf-8"))
    records: list[dict[str, Any]] = []
    with (target_dir / RECORDS_FILENAME).open("r", encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if not line:
                continue
            records.append(json.loads(line))
    return {
        "manifest": manifest,
        "records": records,
    }


@dataclass
class EvidenceBundleBuilder:
    run_id: str
    privacy_mode: str = "digest_only"
    redaction: dict[str, bool] = field(default_factory=dict)
    compatibility_targets: dict[str, Any] = field(
        default_factory=lambda: canonicalize(DEFAULT_COMPATIBILITY_TARGETS)
    )
    source_runtime: str | None = None
    capture_mode: str | None = None
    source_runtime_version: str | None = None
    source_runtime_commit: str | None = None
    source_runtime_dirty: bool | None = None
    source_schema_fingerprint: str | None = None
    identity_ref: str | None = None
    policy_ref: str | None = None
    trace_ref: str | None = None
    export_warnings: list[str] = field(default_factory=list)
    omitted_sections: list[str] = field(default_factory=list)
    _records: list[dict[str, Any]] = field(default_factory=list)

    @property
    def records(self) -> list[dict[str, Any]]:
        finalized_records, _ = _finalized_records(self._records)
        return finalized_records

    @property
    def bundle_root_hash(self) -> str:
        return compute_bundle_root_hash([record["record_hash"] for record in self._records])

    def add_record(
        self,
        *,
        event_type: str,
        timestamp: str,
        payload: Any,
    ) -> dict[str, Any]:
        prev_hash = self._records[-1]["record_hash"] if self._records else None
        record = build_record(
            run_id=self.run_id,
            event_type=event_type,
            timestamp=timestamp,
            payload=payload,
            prev_hash=prev_hash,
        )
        self._records.append(record)
        return {
            **record,
            "bundle_root_hash": self.bundle_root_hash,
        }

    def manifest(self) -> dict[str, Any]:
        return build_manifest(
            run_id=self.run_id,
            records=self.records,
            privacy_mode=self.privacy_mode,
            redaction=self.redaction,
            compatibility_targets=self.compatibility_targets,
            source_runtime=self.source_runtime,
            capture_mode=self.capture_mode,
            source_runtime_version=self.source_runtime_version,
            source_runtime_commit=self.source_runtime_commit,
            source_runtime_dirty=self.source_runtime_dirty,
            source_schema_fingerprint=self.source_schema_fingerprint,
            identity_ref=self.identity_ref,
            policy_ref=self.policy_ref,
            trace_ref=self.trace_ref,
            export_warnings=self.export_warnings,
            omitted_sections=self.omitted_sections,
        )

    def write_bundle(self, bundle_dir: str | Path) -> Path:
        return write_bundle(
            bundle_dir=bundle_dir,
            run_id=self.run_id,
            records=self._records,
            privacy_mode=self.privacy_mode,
            redaction=self.redaction,
            compatibility_targets=self.compatibility_targets,
            source_runtime=self.source_runtime,
            capture_mode=self.capture_mode,
            source_runtime_version=self.source_runtime_version,
            source_runtime_commit=self.source_runtime_commit,
            source_runtime_dirty=self.source_runtime_dirty,
            source_schema_fingerprint=self.source_schema_fingerprint,
            identity_ref=self.identity_ref,
            policy_ref=self.policy_ref,
            trace_ref=self.trace_ref,
            export_warnings=self.export_warnings,
            omitted_sections=self.omitted_sections,
        )
