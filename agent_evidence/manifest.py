from __future__ import annotations

import base64
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field

from agent_evidence.crypto.hashing import canonical_json_bytes
from agent_evidence.models import utc_now
from agent_evidence.serialization import to_jsonable

MANIFEST_SCHEMA_VERSION = "1.0.0"


class EvidenceManifest(BaseModel):
    """Signed summary of an exported evidence artifact."""

    model_config = ConfigDict(extra="forbid")

    schema_version: Literal["1.0.0"] = MANIFEST_SCHEMA_VERSION
    export_format: Literal["json", "csv"]
    digest_algorithm: Literal["sha256"] = "sha256"
    generated_at: str = Field(default_factory=lambda: utc_now().isoformat())
    record_count: int
    artifact_digest: str
    event_hash_list_digest: str
    chain_hash_list_digest: str
    first_event_hash: str | None = None
    last_event_hash: str | None = None
    latest_chain_hash: str | None = None
    filters: dict[str, Any] = Field(default_factory=dict)


class ManifestSignature(BaseModel):
    """Detached signature for a manifest payload."""

    model_config = ConfigDict(extra="forbid")

    algorithm: Literal["ed25519"] = "ed25519"
    key_id: str | None = None
    signature: str


class ManifestDocument(BaseModel):
    """Serialized manifest document with optional signature."""

    model_config = ConfigDict(extra="forbid")

    manifest: EvidenceManifest
    signature: ManifestSignature | None = None


def normalize_filters(filters: dict[str, Any] | None) -> dict[str, Any]:
    if not filters:
        return {}
    return {str(key): to_jsonable(value) for key, value in filters.items() if value is not None}


def manifest_payload(manifest: EvidenceManifest | dict[str, Any]) -> dict[str, Any]:
    if isinstance(manifest, EvidenceManifest):
        return manifest.model_dump(mode="json")
    return EvidenceManifest.model_validate(manifest).model_dump(mode="json")


def _load_ed25519_private_key(pem_bytes: bytes):
    try:
        from cryptography.hazmat.primitives import serialization
        from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
    except ModuleNotFoundError as exc:  # pragma: no cover - depends on extras
        raise ModuleNotFoundError(
            "Manifest signing requires cryptography. Install agent-evidence with the "
            "[signing] or [dev] extra."
        ) from exc

    key = serialization.load_pem_private_key(pem_bytes, password=None)
    if not isinstance(key, Ed25519PrivateKey):
        raise TypeError("Manifest signing requires an Ed25519 private key in PEM format.")
    return key


def _load_ed25519_public_key(pem_bytes: bytes):
    try:
        from cryptography.hazmat.primitives import serialization
        from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey
    except ModuleNotFoundError as exc:  # pragma: no cover - depends on extras
        raise ModuleNotFoundError(
            "Manifest verification requires cryptography. Install agent-evidence with "
            "the [signing] or [dev] extra."
        ) from exc

    key = serialization.load_pem_public_key(pem_bytes)
    if not isinstance(key, Ed25519PublicKey):
        raise TypeError("Manifest verification requires an Ed25519 public key in PEM format.")
    return key


def sign_manifest(
    manifest: EvidenceManifest | dict[str, Any],
    private_key_pem: bytes,
    *,
    key_id: str | None = None,
) -> ManifestSignature:
    payload = canonical_json_bytes(manifest_payload(manifest))
    signature_bytes = _load_ed25519_private_key(private_key_pem).sign(payload)
    return ManifestSignature(
        key_id=key_id,
        signature=base64.b64encode(signature_bytes).decode("ascii"),
    )


def verify_manifest_signature(
    manifest: EvidenceManifest | dict[str, Any],
    signature: ManifestSignature | dict[str, Any],
    public_key_pem: bytes,
) -> bool:
    try:
        from cryptography.exceptions import InvalidSignature
    except ModuleNotFoundError as exc:  # pragma: no cover - depends on extras
        raise ModuleNotFoundError(
            "Manifest verification requires cryptography. Install agent-evidence with "
            "the [signing] or [dev] extra."
        ) from exc

    signature_model = (
        signature
        if isinstance(signature, ManifestSignature)
        else ManifestSignature.model_validate(signature)
    )
    payload = canonical_json_bytes(manifest_payload(manifest))
    signature_bytes = base64.b64decode(signature_model.signature.encode("ascii"))
    public_key = _load_ed25519_public_key(public_key_pem)
    try:
        public_key.verify(signature_bytes, payload)
    except InvalidSignature:
        return False
    return True
