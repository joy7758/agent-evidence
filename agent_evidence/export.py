from __future__ import annotations

import csv
import io
import json
import tarfile
import zipfile
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any, Literal, Sequence
from xml.etree import ElementTree as ET

try:  # pragma: no cover - optional hardening dependency
    from defusedxml import ElementTree as SafeET
    from defusedxml.common import DefusedXmlException
except ModuleNotFoundError:  # pragma: no cover - optional hardening dependency
    SafeET = None
    DefusedXmlException = None

from pydantic import ConfigDict, Field

from agent_evidence.crypto.chain import verify_chain
from agent_evidence.crypto.hashing import canonical_json_bytes, compute_hash, sha256_hex
from agent_evidence.manifest import (
    EvidenceManifest,
    ManifestDocument,
    SignaturePolicy,
    SignerConfig,
    VerificationKey,
    normalize_filters,
    sign_manifest_set,
    verify_manifest_signatures,
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

ARCHIVE_DESCRIPTOR_NAME = "package-manifest.json"
DEFAULT_ARCHIVE_MAX_MEMBERS = 1_000
DEFAULT_ARCHIVE_MAX_TOTAL_UNPACKED_BYTES = 100 * 1024 * 1024
DEFAULT_ARCHIVE_MAX_MEMBER_BYTES = 50 * 1024 * 1024
DEFAULT_ARCHIVE_MAX_ZIP_RATIO = 200.0
_XML_PARSE_ERRORS = ((DefusedXmlException,) if DefusedXmlException else ()) + (ET.ParseError,)
_CSV_FORMULA_PREFIXES = ("=", "+", "-", "@")


@dataclass(frozen=True)
class PackagedExportDescriptor:
    archive_format: Literal["zip", "tar.gz"]
    export_format: Literal["json", "csv", "xml"]
    artifact_path: str
    manifest_path: str
    record_count: int
    signature_count: int


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


def _csv_safe_text(value: str) -> str:
    text = value or ""
    stripped = text.lstrip(" \t\r\n")
    if stripped and stripped[0] in _CSV_FORMULA_PREFIXES:
        return "\t" + text
    return text


def _envelope_to_csv_row(
    envelope: EvidenceEnvelope,
    *,
    sanitize_for_spreadsheet: bool = True,
) -> dict[str, str]:
    event = envelope.event
    context = event.context
    hashes = envelope.hashes
    text = _csv_safe_text if sanitize_for_spreadsheet else (lambda value: value or "")
    return {
        "schema_version": envelope.schema_version,
        "event_id": event.event_id,
        "timestamp": event.timestamp.isoformat(),
        "event_type": text(event.event_type),
        "actor": text(event.actor),
        "source": text(context.source),
        "component": text(context.component or ""),
        "source_event_type": text(context.source_event_type or ""),
        "span_id": text(context.span_id or ""),
        "parent_span_id": text(context.parent_span_id or ""),
        "ancestor_span_ids": _json_cell(context.ancestor_span_ids),
        "name": text(context.name or ""),
        "tags": _json_cell(context.tags),
        "attributes": _json_cell(context.attributes),
        "inputs": _json_cell(event.inputs),
        "outputs": _json_cell(event.outputs),
        "metadata": _json_cell(event.metadata),
        "event_hash": hashes.event_hash,
        "previous_event_hash": hashes.previous_event_hash or "",
        "chain_hash": hashes.chain_hash,
    }


def _csv_bytes(
    records: Sequence[EvidenceEnvelope],
    *,
    sanitize_for_spreadsheet: bool = True,
) -> bytes:
    buffer = io.StringIO(newline="")
    writer = csv.DictWriter(buffer, fieldnames=CSV_FIELDNAMES, lineterminator="\n")
    writer.writeheader()
    for envelope in records:
        writer.writerow(
            _envelope_to_csv_row(envelope, sanitize_for_spreadsheet=sanitize_for_spreadsheet)
        )
    return buffer.getvalue().encode("utf-8")


def _text_element(parent: ET.Element, name: str, value: str) -> None:
    element = ET.SubElement(parent, name)
    element.text = value


def _xml_bytes(records: Sequence[EvidenceEnvelope]) -> bytes:
    root = ET.Element("agent_evidence_export", {"schema_version": "1.0"})
    for envelope in records:
        event = envelope.event
        context = event.context
        hashes = envelope.hashes

        record_element = ET.SubElement(
            root,
            "record",
            {"schema_version": envelope.schema_version},
        )
        event_element = ET.SubElement(record_element, "event")
        _text_element(event_element, "event_id", event.event_id)
        _text_element(event_element, "timestamp", event.timestamp.isoformat())
        _text_element(event_element, "event_type", event.event_type)
        _text_element(event_element, "actor", event.actor)
        _text_element(event_element, "inputs", _json_cell(event.inputs))
        _text_element(event_element, "outputs", _json_cell(event.outputs))
        _text_element(event_element, "metadata", _json_cell(event.metadata))

        context_element = ET.SubElement(event_element, "context")
        _text_element(context_element, "source", context.source)
        _text_element(context_element, "component", context.component or "")
        _text_element(context_element, "source_event_type", context.source_event_type or "")
        _text_element(context_element, "span_id", context.span_id or "")
        _text_element(context_element, "parent_span_id", context.parent_span_id or "")
        _text_element(
            context_element,
            "ancestor_span_ids",
            _json_cell(context.ancestor_span_ids),
        )
        _text_element(context_element, "name", context.name or "")
        _text_element(context_element, "tags", _json_cell(context.tags))
        _text_element(context_element, "attributes", _json_cell(context.attributes))

        hashes_element = ET.SubElement(record_element, "hashes")
        _text_element(hashes_element, "event_hash", hashes.event_hash)
        _text_element(hashes_element, "previous_event_hash", hashes.previous_event_hash or "")
        _text_element(hashes_element, "chain_hash", hashes.chain_hash)
    return ET.tostring(root, encoding="utf-8", xml_declaration=True)


def _xml_hash_rows(xml_bytes: bytes) -> list[dict[str, str]]:
    try:
        parser = SafeET if SafeET is not None else ET
        root = parser.fromstring(xml_bytes)
    except _XML_PARSE_ERRORS as exc:
        raise ValueError("artifact XML is not well-formed") from exc
    rows: list[dict[str, str]] = []
    for record_element in root.findall("record"):
        hashes_element = record_element.find("hashes")
        rows.append(
            {
                "event_hash": (
                    "" if hashes_element is None else hashes_element.findtext("event_hash", "")
                ),
                "chain_hash": (
                    "" if hashes_element is None else hashes_element.findtext("chain_hash", "")
                ),
            }
        )
    return rows


def _build_manifest(
    records: Sequence[EvidenceEnvelope],
    *,
    export_format: Literal["json", "csv", "xml"],
    artifact_digest: str,
    filters: dict[str, Any] | None = None,
    minimum_valid_signatures: int | None = None,
    minimum_valid_signatures_by_role: dict[str, int] | None = None,
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
        signature_policy=SignaturePolicy(
            minimum_valid_signatures=minimum_valid_signatures,
            minimum_valid_signatures_by_role=minimum_valid_signatures_by_role or {},
        ),
    )


def _manifest_document(
    manifest: EvidenceManifest,
    *,
    private_key_pem: bytes | None = None,
    key_id: str | None = None,
    key_version: str | None = None,
    signer: str | None = None,
    role: str | None = None,
    signature_metadata: dict[str, Any] | None = None,
    signer_configs: Sequence[SignerConfig] | None = None,
) -> ManifestDocument:
    resolved_signer_configs = list(signer_configs or [])
    if private_key_pem is not None:
        resolved_signer_configs.insert(
            0,
            SignerConfig(
                private_key_pem=private_key_pem,
                key_id=key_id,
                key_version=key_version,
                signer=signer,
                role=role,
                metadata=signature_metadata or {},
            ),
        )
    signatures = sign_manifest_set(manifest, resolved_signer_configs)
    return ManifestDocument(manifest=manifest, signatures=signatures)


def _verification_keys(
    *,
    public_key_pem: bytes | None = None,
    key_id: str | None = None,
    key_version: str | None = None,
    verification_keys: Sequence[VerificationKey] | None = None,
) -> list[VerificationKey]:
    resolved_keys = list(verification_keys or [])
    if public_key_pem is not None:
        resolved_keys.insert(
            0,
            VerificationKey(
                public_key_pem=public_key_pem,
                key_id=key_id,
                key_version=key_version,
                is_direct=True,
            ),
        )
    return resolved_keys


def default_manifest_path(output_path: str | Path) -> Path:
    output = Path(output_path)
    return output.with_name(f"{output.name}.manifest.json")


def write_manifest_document(document: ManifestDocument, output_path: str | Path) -> None:
    Path(output_path).write_text(_json_text(document.model_dump(mode="json")), encoding="utf-8")


def _archive_format_for_path(archive_path: str | Path) -> Literal["zip", "tar.gz"]:
    archive_name = Path(archive_path).name.lower()
    if archive_name.endswith(".zip"):
        return "zip"
    if archive_name.endswith(".tar.gz") or archive_name.endswith(".tgz"):
        return "tar.gz"
    raise ValueError("archive path must end with .zip, .tar.gz, or .tgz")


def _archive_basename(archive_path: str | Path) -> str:
    archive_name = Path(archive_path).name
    if archive_name.lower().endswith(".tar.gz"):
        return archive_name[:-7] or "evidence-export"
    if archive_name.lower().endswith(".tgz"):
        return archive_name[:-4] or "evidence-export"
    suffix = Path(archive_name).suffix
    if suffix:
        return Path(archive_name).stem or "evidence-export"
    return archive_name or "evidence-export"


def _packaged_export_names(
    archive_path: str | Path,
    export_format: Literal["json", "csv", "xml"],
) -> tuple[str, str]:
    base_name = _archive_basename(archive_path)
    if export_format == "json":
        artifact_name = f"{base_name}.bundle.json"
    else:
        artifact_name = f"{base_name}.{export_format}"
    return artifact_name, f"{artifact_name}.manifest.json"


def _package_manifest_payload(descriptor: PackagedExportDescriptor) -> dict[str, Any]:
    return {
        "schema_version": "1.0.0",
        "archive_format": descriptor.archive_format,
        "export_format": descriptor.export_format,
        "artifact_path": descriptor.artifact_path,
        "manifest_path": descriptor.manifest_path,
        "record_count": descriptor.record_count,
        "signature_count": descriptor.signature_count,
    }


def export_json_bundle(
    records: Sequence[EvidenceEnvelope],
    output_path: str | Path,
    *,
    filters: dict[str, Any] | None = None,
    private_key_pem: bytes | None = None,
    key_id: str | None = None,
    key_version: str | None = None,
    signer: str | None = None,
    role: str | None = None,
    signature_metadata: dict[str, Any] | None = None,
    signer_configs: Sequence[SignerConfig] | None = None,
    minimum_valid_signatures: int | None = None,
    minimum_valid_signatures_by_role: dict[str, int] | None = None,
    manifest_output_path: str | Path | None = None,
) -> JsonBundleDocument:
    records_payload = _records_payload(records)
    manifest = _build_manifest(
        records,
        export_format="json",
        artifact_digest=sha256_hex(canonical_json_bytes(records_payload)),
        filters=filters,
        minimum_valid_signatures=minimum_valid_signatures,
        minimum_valid_signatures_by_role=minimum_valid_signatures_by_role,
    )
    manifest_document = _manifest_document(
        manifest,
        private_key_pem=private_key_pem,
        key_id=key_id,
        key_version=key_version,
        signer=signer,
        role=role,
        signature_metadata=signature_metadata,
        signer_configs=signer_configs,
    )
    bundle = JsonBundleDocument(
        manifest=manifest_document.manifest,
        signatures=manifest_document.signatures,
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
    sanitize_for_spreadsheet: bool = True,
    filters: dict[str, Any] | None = None,
    private_key_pem: bytes | None = None,
    key_id: str | None = None,
    key_version: str | None = None,
    signer: str | None = None,
    role: str | None = None,
    signature_metadata: dict[str, Any] | None = None,
    signer_configs: Sequence[SignerConfig] | None = None,
    minimum_valid_signatures: int | None = None,
    minimum_valid_signatures_by_role: dict[str, int] | None = None,
) -> ManifestDocument:
    artifact_bytes = _csv_bytes(records, sanitize_for_spreadsheet=sanitize_for_spreadsheet)
    output = Path(output_path)
    output.write_bytes(artifact_bytes)

    manifest = _build_manifest(
        records,
        export_format="csv",
        artifact_digest=sha256_hex(artifact_bytes),
        filters=filters,
        minimum_valid_signatures=minimum_valid_signatures,
        minimum_valid_signatures_by_role=minimum_valid_signatures_by_role,
    )
    document = _manifest_document(
        manifest,
        private_key_pem=private_key_pem,
        key_id=key_id,
        key_version=key_version,
        signer=signer,
        role=role,
        signature_metadata=signature_metadata,
        signer_configs=signer_configs,
    )
    write_manifest_document(document, manifest_output_path or default_manifest_path(output))
    return document


def export_xml_bundle(
    records: Sequence[EvidenceEnvelope],
    output_path: str | Path,
    *,
    manifest_output_path: str | Path | None = None,
    filters: dict[str, Any] | None = None,
    private_key_pem: bytes | None = None,
    key_id: str | None = None,
    key_version: str | None = None,
    signer: str | None = None,
    role: str | None = None,
    signature_metadata: dict[str, Any] | None = None,
    signer_configs: Sequence[SignerConfig] | None = None,
    minimum_valid_signatures: int | None = None,
    minimum_valid_signatures_by_role: dict[str, int] | None = None,
) -> ManifestDocument:
    artifact_bytes = _xml_bytes(records)
    output = Path(output_path)
    output.write_bytes(artifact_bytes)

    manifest = _build_manifest(
        records,
        export_format="xml",
        artifact_digest=sha256_hex(artifact_bytes),
        filters=filters,
        minimum_valid_signatures=minimum_valid_signatures,
        minimum_valid_signatures_by_role=minimum_valid_signatures_by_role,
    )
    document = _manifest_document(
        manifest,
        private_key_pem=private_key_pem,
        key_id=key_id,
        key_version=key_version,
        signer=signer,
        role=role,
        signature_metadata=signature_metadata,
        signer_configs=signer_configs,
    )
    write_manifest_document(document, manifest_output_path or default_manifest_path(output))
    return document


def package_export_archive(
    records: Sequence[EvidenceEnvelope],
    archive_path: str | Path,
    *,
    export_format: Literal["json", "csv", "xml"],
    sanitize_csv_for_spreadsheet: bool = True,
    filters: dict[str, Any] | None = None,
    private_key_pem: bytes | None = None,
    key_id: str | None = None,
    key_version: str | None = None,
    signer: str | None = None,
    role: str | None = None,
    signature_metadata: dict[str, Any] | None = None,
    signer_configs: Sequence[SignerConfig] | None = None,
    minimum_valid_signatures: int | None = None,
    minimum_valid_signatures_by_role: dict[str, int] | None = None,
) -> dict[str, Any]:
    archive_format = _archive_format_for_path(archive_path)
    artifact_name, manifest_name = _packaged_export_names(archive_path, export_format)

    with TemporaryDirectory(prefix="agent-evidence-package-") as temp_dir:
        temp_root = Path(temp_dir)
        artifact_path = temp_root / artifact_name
        manifest_path = temp_root / manifest_name

        if export_format == "json":
            bundle = export_json_bundle(
                records,
                artifact_path,
                filters=filters,
                private_key_pem=private_key_pem,
                key_id=key_id,
                key_version=key_version,
                signer=signer,
                role=role,
                signature_metadata=signature_metadata,
                signer_configs=signer_configs,
                minimum_valid_signatures=minimum_valid_signatures,
                minimum_valid_signatures_by_role=minimum_valid_signatures_by_role,
                manifest_output_path=manifest_path,
            )
            signature_count = len(bundle.signatures)
        elif export_format == "csv":
            document = export_csv_bundle(
                records,
                artifact_path,
                manifest_output_path=manifest_path,
                sanitize_for_spreadsheet=sanitize_csv_for_spreadsheet,
                filters=filters,
                private_key_pem=private_key_pem,
                key_id=key_id,
                key_version=key_version,
                signer=signer,
                role=role,
                signature_metadata=signature_metadata,
                signer_configs=signer_configs,
                minimum_valid_signatures=minimum_valid_signatures,
                minimum_valid_signatures_by_role=minimum_valid_signatures_by_role,
            )
            signature_count = len(document.signatures)
        else:
            document = export_xml_bundle(
                records,
                artifact_path,
                manifest_output_path=manifest_path,
                filters=filters,
                private_key_pem=private_key_pem,
                key_id=key_id,
                key_version=key_version,
                signer=signer,
                role=role,
                signature_metadata=signature_metadata,
                signer_configs=signer_configs,
                minimum_valid_signatures=minimum_valid_signatures,
                minimum_valid_signatures_by_role=minimum_valid_signatures_by_role,
            )
            signature_count = len(document.signatures)

        descriptor = PackagedExportDescriptor(
            archive_format=archive_format,
            export_format=export_format,
            artifact_path=artifact_name,
            manifest_path=manifest_name,
            record_count=len(records),
            signature_count=signature_count,
        )
        descriptor_path = temp_root / ARCHIVE_DESCRIPTOR_NAME
        descriptor_path.write_text(
            _json_text(_package_manifest_payload(descriptor)),
            encoding="utf-8",
        )

        members = {
            artifact_name: artifact_path.read_bytes(),
            manifest_name: manifest_path.read_bytes(),
            ARCHIVE_DESCRIPTOR_NAME: descriptor_path.read_bytes(),
        }
        output = Path(archive_path)
        if archive_format == "zip":
            with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED) as archive:
                for member_name, member_bytes in sorted(members.items()):
                    archive.writestr(member_name, member_bytes)
        else:
            with tarfile.open(output, "w:gz") as archive:
                for member_name, member_bytes in sorted(members.items()):
                    info = tarfile.TarInfo(member_name)
                    info.size = len(member_bytes)
                    archive.addfile(info, io.BytesIO(member_bytes))

    return {
        "archive_format": archive_format,
        "archive_path": str(archive_path),
        "export_format": export_format,
        "artifact_path": artifact_name,
        "manifest_path": manifest_name,
        "record_count": len(records),
        "signature_count": signature_count,
    }


def _issues_for_manifest_summary(
    manifest: EvidenceManifest,
    *,
    export_format: Literal["json", "csv", "xml"],
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


def _validated_archive_member_name(name: str) -> str:
    candidate = Path(name)
    if candidate.is_absolute() or ".." in candidate.parts:
        raise ValueError(f"archive contains unsafe member path: {name}")
    normalized = candidate.as_posix()
    if not normalized or normalized == ".":
        raise ValueError(f"archive contains invalid member path: {name}")
    return normalized


def _extract_archive_to_directory(
    archive_path: str | Path,
    output_dir: Path,
    *,
    max_members: int = DEFAULT_ARCHIVE_MAX_MEMBERS,
    max_total_unpacked_bytes: int = DEFAULT_ARCHIVE_MAX_TOTAL_UNPACKED_BYTES,
    max_member_bytes: int = DEFAULT_ARCHIVE_MAX_MEMBER_BYTES,
    max_zip_ratio: float | None = DEFAULT_ARCHIVE_MAX_ZIP_RATIO,
) -> Literal["zip", "tar.gz"]:
    archive_format = _archive_format_for_path(archive_path)
    archive = Path(archive_path)

    def copy_stream(source: Any, destination: Path, member_name: str) -> int:
        copied = 0
        with destination.open("wb") as handle:
            while True:
                chunk = source.read(1024 * 1024)
                if not chunk:
                    break
                copied += len(chunk)
                if copied > max_member_bytes:
                    raise ValueError(f"archive member too large: {member_name}")
                handle.write(chunk)
        return copied

    if archive_format == "zip":
        with zipfile.ZipFile(archive, "r") as zip_handle:
            members = 0
            total_unpacked = 0
            for info in zip_handle.infolist():
                if info.is_dir():
                    continue
                members += 1
                if members > max_members:
                    raise ValueError("archive contains too many members")
                member_name = _validated_archive_member_name(info.filename)
                if info.file_size > max_member_bytes:
                    raise ValueError(f"archive member too large: {member_name}")
                if max_zip_ratio is not None and info.compress_size > 0:
                    ratio = info.file_size / info.compress_size
                    if ratio > max_zip_ratio:
                        raise ValueError(
                            f"archive member compression ratio too high: {member_name}"
                        )
                destination = output_dir / member_name
                destination.parent.mkdir(parents=True, exist_ok=True)
                with zip_handle.open(info, "r") as source:
                    total_unpacked += copy_stream(source, destination, member_name)
                if total_unpacked > max_total_unpacked_bytes:
                    raise ValueError("archive expands beyond allowed size")
    else:
        with tarfile.open(archive, "r:gz") as tar_handle:
            members = 0
            total_unpacked = 0
            for member in tar_handle.getmembers():
                if not member.isfile():
                    continue
                members += 1
                if members > max_members:
                    raise ValueError("archive contains too many members")
                member_name = _validated_archive_member_name(member.name)
                if member.size > max_member_bytes:
                    raise ValueError(f"archive member too large: {member_name}")
                extracted = tar_handle.extractfile(member)
                if extracted is None:
                    continue
                destination = output_dir / member_name
                destination.parent.mkdir(parents=True, exist_ok=True)
                total_unpacked += copy_stream(extracted, destination, member_name)
                if total_unpacked > max_total_unpacked_bytes:
                    raise ValueError("archive expands beyond allowed size")
    return archive_format


def _load_packaged_export_descriptor(path: Path) -> PackagedExportDescriptor:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("package manifest must be a JSON object")

    archive_format = payload.get("archive_format")
    export_format = payload.get("export_format")
    artifact_path = payload.get("artifact_path")
    manifest_path = payload.get("manifest_path")
    record_count = payload.get("record_count")
    signature_count = payload.get("signature_count")
    if archive_format not in {"zip", "tar.gz"}:
        raise ValueError("package manifest has unsupported archive_format")
    if export_format not in {"json", "csv", "xml"}:
        raise ValueError("package manifest has unsupported export_format")
    if not isinstance(artifact_path, str) or not artifact_path:
        raise ValueError("package manifest requires artifact_path")
    if not isinstance(manifest_path, str) or not manifest_path:
        raise ValueError("package manifest requires manifest_path")
    if not isinstance(record_count, int) or record_count < 0:
        raise ValueError("package manifest requires a non-negative record_count")
    if not isinstance(signature_count, int) or signature_count < 0:
        raise ValueError("package manifest requires a non-negative signature_count")

    return PackagedExportDescriptor(
        archive_format=archive_format,
        export_format=export_format,
        artifact_path=artifact_path,
        manifest_path=manifest_path,
        record_count=record_count,
        signature_count=signature_count,
    )


def _required_signature_count(
    document: ManifestDocument,
    minimum_valid_signatures: int | None,
    minimum_valid_signatures_by_role: dict[str, int],
) -> int:
    if minimum_valid_signatures is not None:
        return minimum_valid_signatures
    if document.manifest.signature_policy.minimum_valid_signatures is not None:
        return document.manifest.signature_policy.minimum_valid_signatures
    if minimum_valid_signatures_by_role:
        return sum(minimum_valid_signatures_by_role.values())
    return len(document.signatures)


def _required_role_signature_counts(
    document: ManifestDocument,
    minimum_valid_signatures_by_role: dict[str, int] | None,
) -> dict[str, int]:
    if minimum_valid_signatures_by_role is not None:
        return dict(minimum_valid_signatures_by_role)
    return dict(document.manifest.signature_policy.minimum_valid_signatures_by_role)


def _evaluate_signature_results(
    document: ManifestDocument,
    *,
    public_key_pem: bytes | None = None,
    key_id: str | None = None,
    key_version: str | None = None,
    verification_keys: Sequence[VerificationKey] | None = None,
    minimum_valid_signatures: int | None = None,
    minimum_valid_signatures_by_role: dict[str, int] | None = None,
) -> tuple[list[dict[str, Any]], bool | None, int, int, dict[str, int], dict[str, int], list[str]]:
    required_role_signature_counts = _required_role_signature_counts(
        document,
        minimum_valid_signatures_by_role,
    )
    required_signature_count = _required_signature_count(
        document,
        minimum_valid_signatures,
        required_role_signature_counts,
    )
    signature_count = len(document.signatures)
    issues: list[str] = []
    role_threshold_total = sum(required_role_signature_counts.values())

    if required_signature_count < role_threshold_total:
        issues.append(
            "signature policy invalid: "
            f"required {required_signature_count} total signatures but role thresholds "
            f"sum to {role_threshold_total}"
        )
        return (
            [],
            False,
            required_signature_count,
            0,
            required_role_signature_counts,
            {},
            issues,
        )

    if required_signature_count > signature_count:
        issues.append(
            "signature threshold invalid: "
            f"required {required_signature_count} but only {signature_count} signatures are present"
        )
        return (
            [],
            False,
            required_signature_count,
            0,
            required_role_signature_counts,
            {},
            issues,
        )

    available_role_signature_counts = Counter(
        signature.role for signature in document.signatures if signature.role
    )
    role_threshold_issues = [
        (
            "role signature threshold invalid: "
            f"role {role} requires {count} signatures but only "
            f"{available_role_signature_counts.get(role, 0)} signatures are present"
        )
        for role, count in required_role_signature_counts.items()
        if count > available_role_signature_counts.get(role, 0)
    ]
    if role_threshold_issues:
        issues.extend(role_threshold_issues)
        return (
            [],
            False,
            required_signature_count,
            0,
            required_role_signature_counts,
            {},
            issues,
        )

    if not document.signatures:
        return (
            [],
            None,
            required_signature_count,
            0,
            required_role_signature_counts,
            {},
            issues,
        )

    resolved_verification_keys = _verification_keys(
        public_key_pem=public_key_pem,
        key_id=key_id,
        key_version=key_version,
        verification_keys=verification_keys,
    )
    if not resolved_verification_keys:
        issues.append(
            "verification keys are required to verify signatures "
            "(provide --public-key or --keyring)"
        )
        return (
            [],
            False,
            required_signature_count,
            0,
            required_role_signature_counts,
            {},
            issues,
        )

    signature_results = verify_manifest_signatures(
        document.manifest,
        document.signatures,
        resolved_verification_keys,
    )
    verified_signature_count = sum(1 for item in signature_results if item["verified"])
    verified_role_signature_counts = dict(
        Counter(item["role"] for item in signature_results if item["verified"] and item["role"])
    )
    signature_verified = verified_signature_count >= required_signature_count
    if not signature_verified:
        issues.append(
            "signature threshold not met: "
            f"verified {verified_signature_count} of {signature_count} signatures; "
            f"required {required_signature_count}"
        )
    for role, count in required_role_signature_counts.items():
        verified_role_count = verified_role_signature_counts.get(role, 0)
        available_role_count = available_role_signature_counts.get(role, 0)
        if verified_role_count < count:
            signature_verified = False
            issues.append(
                "role signature threshold not met: "
                f"role {role} verified {verified_role_count} of {available_role_count} signatures; "
                f"required {count}"
            )
    return (
        signature_results,
        signature_verified,
        required_signature_count,
        verified_signature_count,
        required_role_signature_counts,
        verified_role_signature_counts,
        issues,
    )


def verify_json_bundle(
    bundle_path: str | Path,
    *,
    public_key_pem: bytes | None = None,
    key_id: str | None = None,
    key_version: str | None = None,
    verification_keys: Sequence[VerificationKey] | None = None,
    minimum_valid_signatures: int | None = None,
    minimum_valid_signatures_by_role: dict[str, int] | None = None,
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

    (
        signature_results,
        signature_verified,
        required_signature_count,
        verified_signature_count,
        required_role_signature_counts,
        verified_role_signature_counts,
        signature_issues,
    ) = _evaluate_signature_results(
        document,
        public_key_pem=public_key_pem,
        key_id=key_id,
        key_version=key_version,
        verification_keys=verification_keys,
        minimum_valid_signatures=minimum_valid_signatures,
        minimum_valid_signatures_by_role=minimum_valid_signatures_by_role,
    )
    issues.extend(signature_issues)

    return {
        "ok": not issues,
        "format": "json",
        "record_count": len(document.records),
        "latest_chain_hash": document.manifest.latest_chain_hash,
        "signature_policy": document.manifest.signature_policy.model_dump(mode="json"),
        "signature_count": len(document.signatures),
        "signature_present": bool(document.signatures),
        "required_signature_count": required_signature_count,
        "verified_signature_count": verified_signature_count,
        "required_role_signature_counts": required_role_signature_counts,
        "verified_role_signature_counts": verified_role_signature_counts,
        "signature_verified": signature_verified,
        "signature_results": signature_results,
        "issues": issues,
    }


def verify_csv_export(
    csv_path: str | Path,
    manifest_path: str | Path,
    *,
    public_key_pem: bytes | None = None,
    key_id: str | None = None,
    key_version: str | None = None,
    verification_keys: Sequence[VerificationKey] | None = None,
    minimum_valid_signatures: int | None = None,
    minimum_valid_signatures_by_role: dict[str, int] | None = None,
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

    (
        signature_results,
        signature_verified,
        required_signature_count,
        verified_signature_count,
        required_role_signature_counts,
        verified_role_signature_counts,
        signature_issues,
    ) = _evaluate_signature_results(
        document,
        public_key_pem=public_key_pem,
        key_id=key_id,
        key_version=key_version,
        verification_keys=verification_keys,
        minimum_valid_signatures=minimum_valid_signatures,
        minimum_valid_signatures_by_role=minimum_valid_signatures_by_role,
    )
    issues.extend(signature_issues)

    return {
        "ok": not issues,
        "format": "csv",
        "record_count": len(rows),
        "latest_chain_hash": document.manifest.latest_chain_hash,
        "signature_policy": document.manifest.signature_policy.model_dump(mode="json"),
        "signature_count": len(document.signatures),
        "signature_present": bool(document.signatures),
        "required_signature_count": required_signature_count,
        "verified_signature_count": verified_signature_count,
        "required_role_signature_counts": required_role_signature_counts,
        "verified_role_signature_counts": verified_role_signature_counts,
        "signature_verified": signature_verified,
        "signature_results": signature_results,
        "issues": issues,
    }


def verify_xml_export(
    xml_path: str | Path,
    manifest_path: str | Path,
    *,
    public_key_pem: bytes | None = None,
    key_id: str | None = None,
    key_version: str | None = None,
    verification_keys: Sequence[VerificationKey] | None = None,
    minimum_valid_signatures: int | None = None,
    minimum_valid_signatures_by_role: dict[str, int] | None = None,
) -> dict[str, Any]:
    xml_bytes = Path(xml_path).read_bytes()
    document = ManifestDocument.model_validate_json(Path(manifest_path).read_text(encoding="utf-8"))
    issues: list[str] = []
    try:
        rows = _xml_hash_rows(xml_bytes)
    except ValueError as exc:
        rows = []
        issues.append(str(exc))
    event_hashes = [row["event_hash"] for row in rows]
    chain_hashes = [row["chain_hash"] for row in rows]
    issues.extend(
        _issues_for_manifest_summary(
            document.manifest,
            export_format="xml",
            artifact_digest=sha256_hex(xml_bytes),
            event_hashes=event_hashes,
            chain_hashes=chain_hashes,
        )
    )

    (
        signature_results,
        signature_verified,
        required_signature_count,
        verified_signature_count,
        required_role_signature_counts,
        verified_role_signature_counts,
        signature_issues,
    ) = _evaluate_signature_results(
        document,
        public_key_pem=public_key_pem,
        key_id=key_id,
        key_version=key_version,
        verification_keys=verification_keys,
        minimum_valid_signatures=minimum_valid_signatures,
        minimum_valid_signatures_by_role=minimum_valid_signatures_by_role,
    )
    issues.extend(signature_issues)

    return {
        "ok": not issues,
        "format": "xml",
        "record_count": len(rows),
        "latest_chain_hash": document.manifest.latest_chain_hash,
        "signature_policy": document.manifest.signature_policy.model_dump(mode="json"),
        "signature_count": len(document.signatures),
        "signature_present": bool(document.signatures),
        "required_signature_count": required_signature_count,
        "verified_signature_count": verified_signature_count,
        "required_role_signature_counts": required_role_signature_counts,
        "verified_role_signature_counts": verified_role_signature_counts,
        "signature_verified": signature_verified,
        "signature_results": signature_results,
        "issues": issues,
    }


def verify_export_archive(
    archive_path: str | Path,
    *,
    public_key_pem: bytes | None = None,
    key_id: str | None = None,
    key_version: str | None = None,
    verification_keys: Sequence[VerificationKey] | None = None,
    minimum_valid_signatures: int | None = None,
    minimum_valid_signatures_by_role: dict[str, int] | None = None,
    max_members: int = DEFAULT_ARCHIVE_MAX_MEMBERS,
    max_total_unpacked_bytes: int = DEFAULT_ARCHIVE_MAX_TOTAL_UNPACKED_BYTES,
    max_member_bytes: int = DEFAULT_ARCHIVE_MAX_MEMBER_BYTES,
    max_zip_ratio: float | None = DEFAULT_ARCHIVE_MAX_ZIP_RATIO,
) -> dict[str, Any]:
    with TemporaryDirectory(prefix="agent-evidence-verify-archive-") as temp_dir:
        temp_root = Path(temp_dir)
        try:
            archive_format = _extract_archive_to_directory(
                archive_path,
                temp_root,
                max_members=max_members,
                max_total_unpacked_bytes=max_total_unpacked_bytes,
                max_member_bytes=max_member_bytes,
                max_zip_ratio=max_zip_ratio,
            )
        except ValueError as exc:
            return {
                "ok": False,
                "packaged": True,
                "archive_path": str(archive_path),
                "issues": [str(exc)],
            }

        descriptor_path = temp_root / ARCHIVE_DESCRIPTOR_NAME
        if not descriptor_path.exists():
            return {
                "ok": False,
                "packaged": True,
                "archive_path": str(archive_path),
                "issues": [f"archive is missing {ARCHIVE_DESCRIPTOR_NAME}"],
            }

        try:
            descriptor = _load_packaged_export_descriptor(descriptor_path)
        except (ValueError, json.JSONDecodeError) as exc:
            return {
                "ok": False,
                "packaged": True,
                "archive_path": str(archive_path),
                "issues": [f"invalid package manifest: {exc}"],
            }

        if descriptor.archive_format != archive_format:
            return {
                "ok": False,
                "packaged": True,
                "archive_path": str(archive_path),
                "issues": [
                    "package manifest archive_format mismatch: "
                    f"expected {archive_format}, found {descriptor.archive_format}"
                ],
            }

        artifact_path = temp_root / _validated_archive_member_name(descriptor.artifact_path)
        manifest_path = temp_root / _validated_archive_member_name(descriptor.manifest_path)
        if not artifact_path.exists():
            return {
                "ok": False,
                "packaged": True,
                "archive_path": str(archive_path),
                "issues": [f"archive artifact is missing: {descriptor.artifact_path}"],
            }
        if not manifest_path.exists():
            return {
                "ok": False,
                "packaged": True,
                "archive_path": str(archive_path),
                "issues": [f"archive manifest is missing: {descriptor.manifest_path}"],
            }

        verify_kwargs = {
            "public_key_pem": public_key_pem,
            "key_id": key_id,
            "key_version": key_version,
            "verification_keys": verification_keys,
            "minimum_valid_signatures": minimum_valid_signatures,
            "minimum_valid_signatures_by_role": minimum_valid_signatures_by_role,
        }
        if descriptor.export_format == "json":
            result = verify_json_bundle(artifact_path, **verify_kwargs)
        elif descriptor.export_format == "csv":
            result = verify_csv_export(artifact_path, manifest_path, **verify_kwargs)
        else:
            result = verify_xml_export(artifact_path, manifest_path, **verify_kwargs)

    return {
        **result,
        "packaged": True,
        "archive_format": archive_format,
        "archive_path": str(archive_path),
        "artifact_path": descriptor.artifact_path,
        "manifest_path": descriptor.manifest_path,
        "package_manifest": _package_manifest_payload(descriptor),
    }
