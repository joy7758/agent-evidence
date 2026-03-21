from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any, Literal, Protocol

from pydantic import BaseModel, ConfigDict, Field, ValidationError

from agent_evidence.crypto.hashing import canonical_json_bytes, sha256_hex
from agent_evidence.manifest import ManifestDocument
from agent_evidence.models import utc_now
from agent_evidence.serialization import to_jsonable

ANCHOR_SCHEMA_VERSION = "1.0.0"


class AnchorRecord(BaseModel):
    """Detached record that anchors a signed manifest outside the export artifact."""

    model_config = ConfigDict(extra="forbid")

    schema_version: Literal["1.0.0"] = ANCHOR_SCHEMA_VERSION
    manifest_digest: str
    anchor_type: str
    anchored_at: str = Field(default_factory=lambda: utc_now().isoformat())
    anchor_payload: dict[str, Any] = Field(default_factory=dict)
    anchor_id: str | None = None


def manifest_document_payload(document: ManifestDocument | dict[str, Any]) -> dict[str, Any]:
    if isinstance(document, ManifestDocument):
        return document.model_dump(mode="json")
    return ManifestDocument.model_validate(document).model_dump(mode="json")


def manifest_document_digest(document: ManifestDocument | dict[str, Any]) -> str:
    payload = manifest_document_payload(document)
    return f"sha256:{sha256_hex(canonical_json_bytes(payload))}"


def default_anchor_path(target_path: str | Path) -> Path:
    target = Path(target_path)
    lower_name = target.name.lower()
    if lower_name.endswith(".tar.gz"):
        base_name = target.name[:-7]
    elif lower_name.endswith(".tgz"):
        base_name = target.name[:-4]
    elif target.suffix == ".json":
        base_name = target.stem
    else:
        base_name = target.name
    return target.with_name(f"{base_name}.anchor.json")


class AnchorBackend(Protocol):
    anchor_type: str

    def create_record(
        self,
        document: ManifestDocument,
        *,
        anchor_id: str | None = None,
        manifest_locator: str | None = None,
        anchor_payload: dict[str, Any] | None = None,
    ) -> AnchorRecord: ...

    def verify_record(self, record: AnchorRecord, document: ManifestDocument) -> list[str]: ...


class LocalTimestampAnchorBackend:
    """Minimal detached anchor backed by a locally generated UTC timestamp record."""

    anchor_type = "local_timestamp"

    def create_record(
        self,
        document: ManifestDocument,
        *,
        anchor_id: str | None = None,
        manifest_locator: str | None = None,
        anchor_payload: dict[str, Any] | None = None,
    ) -> AnchorRecord:
        payload = {"clock_source": "system_utc"}
        if manifest_locator is not None:
            payload["manifest_locator"] = manifest_locator
        for key, value in (anchor_payload or {}).items():
            payload[str(key)] = to_jsonable(value)
        return AnchorRecord(
            manifest_digest=manifest_document_digest(document),
            anchor_type=self.anchor_type,
            anchor_id=anchor_id,
            anchor_payload=payload,
        )

    def verify_record(self, record: AnchorRecord, document: ManifestDocument) -> list[str]:
        issues: list[str] = []
        expected_manifest_digest = manifest_document_digest(document)
        if record.manifest_digest != expected_manifest_digest:
            issues.append("manifest_digest does not match the signed manifest document")
        try:
            datetime.fromisoformat(record.anchored_at.replace("Z", "+00:00"))
        except ValueError:
            issues.append("anchored_at is not a valid ISO-8601 timestamp")

        clock_source = record.anchor_payload.get("clock_source")
        if not isinstance(clock_source, str) or not clock_source:
            issues.append("anchor_payload.clock_source must be a non-empty string")

        manifest_locator = record.anchor_payload.get("manifest_locator")
        if manifest_locator is not None and not isinstance(manifest_locator, str):
            issues.append("anchor_payload.manifest_locator must be a string when present")
        return issues


_ANCHOR_BACKENDS: dict[str, AnchorBackend] = {
    LocalTimestampAnchorBackend.anchor_type: LocalTimestampAnchorBackend(),
}


def _resolve_anchor_backend(anchor_type: str) -> AnchorBackend:
    try:
        return _ANCHOR_BACKENDS[anchor_type]
    except KeyError as exc:
        raise ValueError(f"Unsupported anchor_type: {anchor_type}") from exc


def create_anchor_record(
    document: ManifestDocument | dict[str, Any],
    *,
    anchor_type: str = LocalTimestampAnchorBackend.anchor_type,
    anchor_id: str | None = None,
    manifest_locator: str | None = None,
    anchor_payload: dict[str, Any] | None = None,
) -> AnchorRecord:
    manifest_document = (
        document
        if isinstance(document, ManifestDocument)
        else ManifestDocument.model_validate(document)
    )
    backend = _resolve_anchor_backend(anchor_type)
    return backend.create_record(
        manifest_document,
        anchor_id=anchor_id,
        manifest_locator=manifest_locator,
        anchor_payload=anchor_payload,
    )


def write_anchor_record(record: AnchorRecord, output_path: str | Path) -> None:
    Path(output_path).write_text(
        json.dumps(record.model_dump(mode="json"), indent=2, sort_keys=True),
        encoding="utf-8",
    )


def anchor_manifest_document(
    document: ManifestDocument | dict[str, Any],
    output_path: str | Path,
    *,
    anchor_type: str = LocalTimestampAnchorBackend.anchor_type,
    anchor_id: str | None = None,
    manifest_locator: str | None = None,
    anchor_payload: dict[str, Any] | None = None,
) -> AnchorRecord:
    record = create_anchor_record(
        document,
        anchor_type=anchor_type,
        anchor_id=anchor_id,
        manifest_locator=manifest_locator,
        anchor_payload=anchor_payload,
    )
    write_anchor_record(record, output_path)
    return record


def load_anchor_record(path: str | Path) -> AnchorRecord:
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    return AnchorRecord.model_validate(payload)


def verify_anchor_record(
    record: AnchorRecord | dict[str, Any],
    document: ManifestDocument | dict[str, Any],
) -> dict[str, Any]:
    anchor_record = (
        record if isinstance(record, AnchorRecord) else AnchorRecord.model_validate(record)
    )
    manifest_document = (
        document
        if isinstance(document, ManifestDocument)
        else ManifestDocument.model_validate(document)
    )
    try:
        backend = _resolve_anchor_backend(anchor_record.anchor_type)
    except ValueError as exc:
        issues = [str(exc)]
    else:
        issues = backend.verify_record(anchor_record, manifest_document)
    return {
        "ok": not issues,
        "anchor_id": anchor_record.anchor_id,
        "anchor_type": anchor_record.anchor_type,
        "anchored_at": anchor_record.anchored_at,
        "manifest_digest": anchor_record.manifest_digest,
        "expected_manifest_digest": manifest_document_digest(manifest_document),
        "issues": issues,
    }


def verify_anchor_record_file(
    path: str | Path, document: ManifestDocument | dict[str, Any]
) -> dict[str, Any]:
    try:
        anchor_record = load_anchor_record(path)
    except OSError as exc:
        return {
            "ok": False,
            "anchor_id": None,
            "anchor_type": None,
            "anchored_at": None,
            "manifest_digest": None,
            "expected_manifest_digest": manifest_document_digest(document),
            "issues": [f"unable to read anchor record: {exc}"],
        }
    except json.JSONDecodeError as exc:
        return {
            "ok": False,
            "anchor_id": None,
            "anchor_type": None,
            "anchored_at": None,
            "manifest_digest": None,
            "expected_manifest_digest": manifest_document_digest(document),
            "issues": [f"invalid anchor record JSON: {exc.msg}"],
        }
    except ValidationError as exc:
        return {
            "ok": False,
            "anchor_id": None,
            "anchor_type": None,
            "anchored_at": None,
            "manifest_digest": None,
            "expected_manifest_digest": manifest_document_digest(document),
            "issues": [f"invalid anchor record: {exc}"],
        }

    result = verify_anchor_record(anchor_record, document)
    result["anchor_path"] = str(path)
    return result
