from __future__ import annotations

import csv
import io
import json
from pathlib import Path
from typing import Any, Literal, Sequence

from pydantic import ConfigDict, Field

from agent_evidence.crypto.chain import verify_chain
from agent_evidence.crypto.hashing import canonical_json_bytes, compute_hash, sha256_hex
from agent_evidence.manifest import (
    EvidenceManifest,
    ManifestDocument,
    ManifestSignature,
    normalize_filters,
    sign_manifest,
    verify_manifest_signature,
)
from agent_evidence.models import EvidenceEnvelope
from agent_evidence.serialization import to_jsonable

CSV_FIELDNAMES = [
    "schema_version",
    "event_id",
    "timestamp",
    "event_type",
    "actor",
    "source",
    "component",
    "source_event_type",
    "span_id",
    "parent_span_id",
    "ancestor_span_ids",
    "name",
    "tags",
    "attributes",
    "inputs",
    "outputs",
    "metadata",
    "event_hash",
    "previous_event_hash",
    "chain_hash",
]


class JsonBundleDocument(ManifestDocument):
    """JSON export artifact containing records plus a signed manifest."""

    model_config = ConfigDict(extra="forbid")

    records: list[EvidenceEnvelope] = Field(default_factory=list)


def _records_payload(records: Sequence[EvidenceEnvelope]) -> list[dict[str, Any]]:
    return [record.model_dump(mode="json") for record in records]


def _json_text(payload: Any) -> str:
    return json.dumps(payload, indent=2, sort_keys=True)


def _json_cell(value: Any) -> str:
    return json.dumps(to_jsonable(value), sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def _envelope_to_csv_row(envelope: EvidenceEnvelope) -> dict[str, str]:
    event = envelope.event
    context = event.context
    hashes = envelope.hashes
    return {
        "schema_version": envelope.schema_version,
        "event_id": event.event_id,
        "timestamp": event.timestamp.isoformat(),
        "event_type": event.event_type,
        "actor": event.actor,
        "source": context.source,
        "component": context.component or "",
        "source_event_type": context.source_event_type or "",
        "span_id": context.span_id or "",
        "parent_span_id": context.parent_span_id or "",
        "ancestor_span_ids": _json_cell(context.ancestor_span_ids),
        "name": context.name or "",
        "tags": _json_cell(context.tags),
        "attributes": _json_cell(context.attributes),
        "inputs": _json_cell(event.inputs),
        "outputs": _json_cell(event.outputs),
        "metadata": _json_cell(event.metadata),
        "event_hash": hashes.event_hash,
        "previous_event_hash": hashes.previous_event_hash or "",
        "chain_hash": hashes.chain_hash,
    }


def _csv_bytes(records: Sequence[EvidenceEnvelope]) -> bytes:
    buffer = io.StringIO(newline="")
    writer = csv.DictWriter(buffer, fieldnames=CSV_FIELDNAMES, lineterminator="\n")
    writer.writeheader()
    for envelope in records:
        writer.writerow(_envelope_to_csv_row(envelope))
    return buffer.getvalue().encode("utf-8")


def _build_manifest(
    records: Sequence[EvidenceEnvelope],
    *,
    export_format: Literal["json", "csv"],
    artifact_digest: str,
    filters: dict[str, Any] | None = None,
) -> EvidenceManifest:
    event_hashes = [record.hashes.event_hash for record in records]
    chain_hashes = [record.hashes.chain_hash for record in records]
    return EvidenceManifest(
        export_format=export_format,
        record_count=len(records),
        artifact_digest=artifact_digest,
        event_hash_list_digest=compute_hash(event_hashes),
        chain_hash_list_digest=compute_hash(chain_hashes),
        first_event_hash=event_hashes[0] if event_hashes else None,
        last_event_hash=event_hashes[-1] if event_hashes else None,
        latest_chain_hash=chain_hashes[-1] if chain_hashes else None,
        filters=normalize_filters(filters),
    )


def _manifest_document(
    manifest: EvidenceManifest,
    *,
    private_key_pem: bytes | None = None,
    key_id: str | None = None,
) -> ManifestDocument:
    signature: ManifestSignature | None = None
    if private_key_pem is not None:
        signature = sign_manifest(manifest, private_key_pem, key_id=key_id)
    return ManifestDocument(manifest=manifest, signature=signature)


def default_manifest_path(output_path: str | Path) -> Path:
    output = Path(output_path)
    return output.with_name(f"{output.name}.manifest.json")


def write_manifest_document(document: ManifestDocument, output_path: str | Path) -> None:
    Path(output_path).write_text(_json_text(document.model_dump(mode="json")), encoding="utf-8")


def export_json_bundle(
    records: Sequence[EvidenceEnvelope],
    output_path: str | Path,
    *,
    filters: dict[str, Any] | None = None,
    private_key_pem: bytes | None = None,
    key_id: str | None = None,
    manifest_output_path: str | Path | None = None,
) -> JsonBundleDocument:
    records_payload = _records_payload(records)
    manifest = _build_manifest(
        records,
        export_format="json",
        artifact_digest=sha256_hex(canonical_json_bytes(records_payload)),
        filters=filters,
    )
    manifest_document = _manifest_document(
        manifest,
        private_key_pem=private_key_pem,
        key_id=key_id,
    )
    bundle = JsonBundleDocument(
        manifest=manifest_document.manifest,
        signature=manifest_document.signature,
        records=list(records),
    )
    Path(output_path).write_text(_json_text(bundle.model_dump(mode="json")), encoding="utf-8")
    if manifest_output_path is not None:
        write_manifest_document(manifest_document, manifest_output_path)
    return bundle


def export_csv_bundle(
    records: Sequence[EvidenceEnvelope],
    output_path: str | Path,
    *,
    manifest_output_path: str | Path | None = None,
    filters: dict[str, Any] | None = None,
    private_key_pem: bytes | None = None,
    key_id: str | None = None,
) -> ManifestDocument:
    artifact_bytes = _csv_bytes(records)
    output = Path(output_path)
    output.write_bytes(artifact_bytes)

    manifest = _build_manifest(
        records,
        export_format="csv",
        artifact_digest=sha256_hex(artifact_bytes),
        filters=filters,
    )
    document = _manifest_document(
        manifest,
        private_key_pem=private_key_pem,
        key_id=key_id,
    )
    write_manifest_document(document, manifest_output_path or default_manifest_path(output))
    return document


def _issues_for_manifest_summary(
    manifest: EvidenceManifest,
    *,
    export_format: Literal["json", "csv"],
    artifact_digest: str,
    event_hashes: Sequence[str],
    chain_hashes: Sequence[str],
) -> list[str]:
    issues: list[str] = []
    if manifest.export_format != export_format:
        issues.append(
            "manifest export_format mismatch: "
            f"expected {export_format}, found {manifest.export_format}"
        )
    if manifest.artifact_digest != artifact_digest:
        issues.append("artifact_digest mismatch")
    if manifest.record_count != len(event_hashes):
        issues.append("record_count mismatch")
    if manifest.event_hash_list_digest != compute_hash(list(event_hashes)):
        issues.append("event_hash_list_digest mismatch")
    if manifest.chain_hash_list_digest != compute_hash(list(chain_hashes)):
        issues.append("chain_hash_list_digest mismatch")

    first_event_hash = event_hashes[0] if event_hashes else None
    last_event_hash = event_hashes[-1] if event_hashes else None
    latest_chain_hash = chain_hashes[-1] if chain_hashes else None
    if manifest.first_event_hash != first_event_hash:
        issues.append("first_event_hash mismatch")
    if manifest.last_event_hash != last_event_hash:
        issues.append("last_event_hash mismatch")
    if manifest.latest_chain_hash != latest_chain_hash:
        issues.append("latest_chain_hash mismatch")
    return issues


def verify_json_bundle(
    bundle_path: str | Path,
    *,
    public_key_pem: bytes | None = None,
) -> dict[str, Any]:
    document = JsonBundleDocument.model_validate_json(Path(bundle_path).read_text(encoding="utf-8"))
    records_payload = _records_payload(document.records)
    event_hashes = [record.hashes.event_hash for record in document.records]
    chain_hashes = [record.hashes.chain_hash for record in document.records]
    issues = _issues_for_manifest_summary(
        document.manifest,
        export_format="json",
        artifact_digest=sha256_hex(canonical_json_bytes(records_payload)),
        event_hashes=event_hashes,
        chain_hashes=chain_hashes,
    )
    issues.extend(f"chain: {issue}" for issue in verify_chain(document.records))

    signature_verified: bool | None = None
    if document.signature is not None and public_key_pem is not None:
        signature_verified = verify_manifest_signature(
            document.manifest,
            document.signature,
            public_key_pem,
        )
        if not signature_verified:
            issues.append("manifest signature verification failed")

    return {
        "ok": not issues,
        "format": "json",
        "record_count": len(document.records),
        "latest_chain_hash": document.manifest.latest_chain_hash,
        "signature_present": document.signature is not None,
        "signature_verified": signature_verified,
        "issues": issues,
    }


def verify_csv_export(
    csv_path: str | Path,
    manifest_path: str | Path,
    *,
    public_key_pem: bytes | None = None,
) -> dict[str, Any]:
    csv_bytes = Path(csv_path).read_bytes()
    document = ManifestDocument.model_validate_json(Path(manifest_path).read_text(encoding="utf-8"))

    with Path(csv_path).open("r", encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))

    event_hashes = [row["event_hash"] for row in rows]
    chain_hashes = [row["chain_hash"] for row in rows]
    issues = _issues_for_manifest_summary(
        document.manifest,
        export_format="csv",
        artifact_digest=sha256_hex(csv_bytes),
        event_hashes=event_hashes,
        chain_hashes=chain_hashes,
    )

    signature_verified: bool | None = None
    if document.signature is not None and public_key_pem is not None:
        signature_verified = verify_manifest_signature(
            document.manifest,
            document.signature,
            public_key_pem,
        )
        if not signature_verified:
            issues.append("manifest signature verification failed")

    return {
        "ok": not issues,
        "format": "csv",
        "record_count": len(rows),
        "latest_chain_hash": document.manifest.latest_chain_hash,
        "signature_present": document.signature is not None,
        "signature_verified": signature_verified,
        "issues": issues,
    }
