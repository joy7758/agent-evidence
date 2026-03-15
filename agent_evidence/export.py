from __future__ import annotations

import csv
import io
import json
from collections import Counter
from pathlib import Path
from typing import Any, Literal, Sequence
from xml.etree import ElementTree as ET

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
        root = ET.fromstring(xml_bytes)
    except ET.ParseError as exc:
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
            ),
        )
    return resolved_keys


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
    artifact_bytes = _csv_bytes(records)
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
        if (
            minimum_valid_signatures is not None
            or (document.manifest.signature_policy.minimum_valid_signatures is not None)
            or required_role_signature_counts
        ):
            issues.append("verification keys are required to evaluate signature policy")
            return (
                [],
                False,
                required_signature_count,
                0,
                required_role_signature_counts,
                {},
                issues,
            )
        return (
            [],
            None,
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
