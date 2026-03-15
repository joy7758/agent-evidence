from __future__ import annotations

import base64
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from agent_evidence.crypto.hashing import canonical_json_bytes
from agent_evidence.models import utc_now
from agent_evidence.serialization import to_jsonable

MANIFEST_SCHEMA_VERSION = "1.4.0"


class EvidenceManifest(BaseModel):
    """Signed summary of an exported evidence artifact."""

    model_config = ConfigDict(extra="forbid")

    schema_version: Literal["1.0.0", "1.1.0", "1.2.0", "1.3.0", "1.4.0"] = MANIFEST_SCHEMA_VERSION
    export_format: Literal["json", "csv", "xml"]
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
    signature_policy: SignaturePolicy = Field(default_factory=lambda: SignaturePolicy())


class ManifestSignature(BaseModel):
    """Detached signature for a manifest payload."""

    model_config = ConfigDict(extra="forbid")

    algorithm: Literal["ed25519"] = "ed25519"
    key_id: str | None = None
    key_version: str | None = None
    signed_at: str = Field(default_factory=lambda: utc_now().isoformat())
    signer: str | None = None
    role: str | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)
    signature: str


class SignerConfig(BaseModel):
    """Signing material plus metadata used to create a manifest signature."""

    model_config = ConfigDict(extra="forbid")

    private_key_pem: bytes
    key_id: str | None = None
    key_version: str | None = None
    signed_at: str | None = None
    signer: str | None = None
    role: str | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)


class VerificationKey(BaseModel):
    """Verification key metadata used to resolve rotated signing keys."""

    model_config = ConfigDict(extra="forbid")

    public_key_pem: bytes
    key_id: str | None = None
    key_version: str | None = None


class SignaturePolicy(BaseModel):
    """Verification policy for one or more manifest signatures."""

    model_config = ConfigDict(extra="forbid")

    minimum_valid_signatures: int | None = Field(default=None, ge=1)
    minimum_valid_signatures_by_role: dict[str, int] = Field(default_factory=dict)

    @field_validator("minimum_valid_signatures_by_role")
    @classmethod
    def normalize_role_thresholds(cls, value: dict[str, int]) -> dict[str, int]:
        normalized: dict[str, int] = {}
        for role, count in value.items():
            normalized_role = str(role).strip()
            if not normalized_role:
                raise ValueError("signature policy role names must be non-empty")
            if count < 1:
                raise ValueError("signature policy role thresholds must be positive integers")
            if normalized_role in normalized:
                raise ValueError(f"duplicate signature policy role threshold: {normalized_role}")
            normalized[normalized_role] = int(count)
        return normalized

    @model_validator(mode="after")
    def validate_threshold_consistency(self) -> SignaturePolicy:
        role_threshold_total = sum(self.minimum_valid_signatures_by_role.values())
        if (
            self.minimum_valid_signatures is not None
            and self.minimum_valid_signatures < role_threshold_total
        ):
            raise ValueError(
                "minimum_valid_signatures must be greater than or equal to the "
                "sum of role thresholds"
            )
        return self


class ManifestDocument(BaseModel):
    """Serialized manifest document with one or more detached signatures."""

    model_config = ConfigDict(extra="forbid")

    manifest: EvidenceManifest
    signatures: list[ManifestSignature] = Field(default_factory=list)

    @model_validator(mode="before")
    @classmethod
    def upgrade_legacy_signature(cls, value: Any) -> Any:
        if not isinstance(value, dict):
            return value
        if "signatures" in value:
            return value
        legacy_signature = value.get("signature")
        if legacy_signature is None:
            return value

        upgraded = dict(value)
        upgraded.pop("signature", None)
        upgraded["signatures"] = [legacy_signature]
        return upgraded

    @property
    def signature(self) -> ManifestSignature | None:
        return self.signatures[0] if self.signatures else None


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
    key_version: str | None = None,
    signed_at: str | None = None,
    signer: str | None = None,
    role: str | None = None,
    metadata: dict[str, Any] | None = None,
) -> ManifestSignature:
    payload = canonical_json_bytes(manifest_payload(manifest))
    signature_bytes = _load_ed25519_private_key(private_key_pem).sign(payload)
    return ManifestSignature(
        key_id=key_id,
        key_version=key_version,
        signed_at=signed_at or utc_now().isoformat(),
        signer=signer,
        role=role,
        metadata={str(key): to_jsonable(value) for key, value in (metadata or {}).items()},
        signature=base64.b64encode(signature_bytes).decode("ascii"),
    )


def sign_manifest_set(
    manifest: EvidenceManifest | dict[str, Any],
    signer_configs: list[SignerConfig],
) -> list[ManifestSignature]:
    signatures: list[ManifestSignature] = []
    for signer_config in signer_configs:
        signatures.append(
            sign_manifest(
                manifest,
                signer_config.private_key_pem,
                key_id=signer_config.key_id,
                key_version=signer_config.key_version,
                signed_at=signer_config.signed_at,
                signer=signer_config.signer,
                role=signer_config.role,
                metadata=signer_config.metadata,
            )
        )
    return signatures


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
    try:
        signature_bytes = base64.b64decode(signature_model.signature.encode("ascii"), validate=True)
    except ValueError:
        return False
    public_key = _load_ed25519_public_key(public_key_pem)
    try:
        public_key.verify(signature_bytes, payload)
    except InvalidSignature:
        return False
    return True


def resolve_verification_key(
    signature: ManifestSignature | dict[str, Any],
    verification_keys: list[VerificationKey],
) -> tuple[bytes | None, str | None]:
    signature_model = (
        signature
        if isinstance(signature, ManifestSignature)
        else ManifestSignature.model_validate(signature)
    )
    if not verification_keys:
        return None, "no verification keys were provided"

    if signature_model.key_id is None and signature_model.key_version is None:
        if len(verification_keys) == 1:
            return verification_keys[0].public_key_pem, None
        return None, "signature has no key identity and multiple verification keys were provided"

    candidates = verification_keys
    if signature_model.key_id is not None:
        candidates = [item for item in candidates if item.key_id == signature_model.key_id]
    if signature_model.key_version is not None:
        candidates = [
            item for item in candidates if item.key_version == signature_model.key_version
        ]

    if len(candidates) == 1:
        return candidates[0].public_key_pem, None
    if not candidates:
        anonymous_keys = [
            item for item in verification_keys if item.key_id is None and item.key_version is None
        ]
        if len(anonymous_keys) == 1:
            return anonymous_keys[0].public_key_pem, None
    if not candidates:
        if signature_model.key_version is not None:
            return (
                None,
                "no verification key matched "
                f"{signature_model.key_id}@{signature_model.key_version}",
            )
        return None, f"no verification key matched {signature_model.key_id}"
    return (
        None,
        f"multiple verification keys matched {signature_model.key_id or 'anonymous signature'}",
    )


def verify_manifest_signatures(
    manifest: EvidenceManifest | dict[str, Any],
    signatures: list[ManifestSignature] | list[dict[str, Any]],
    verification_keys: list[VerificationKey],
) -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []
    for raw_signature in signatures:
        signature = (
            raw_signature
            if isinstance(raw_signature, ManifestSignature)
            else ManifestSignature.model_validate(raw_signature)
        )
        public_key_pem, resolution_error = resolve_verification_key(signature, verification_keys)
        verified = False
        error = resolution_error
        if public_key_pem is not None:
            verified = verify_manifest_signature(manifest, signature, public_key_pem)
            if not verified:
                error = "manifest signature verification failed"

        results.append(
            {
                "algorithm": signature.algorithm,
                "key_id": signature.key_id,
                "key_version": signature.key_version,
                "signed_at": signature.signed_at,
                "signer": signature.signer,
                "role": signature.role,
                "verified": verified,
                "error": error,
                "metadata": signature.metadata,
            }
        )
    return results
