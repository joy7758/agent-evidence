"""Public package API for Agent Evidence."""

from .aep import EvidenceBundleBuilder, verify_bundle
from .anchor import (
    AnchorRecord,
    anchor_manifest_document,
    create_anchor_record,
    default_anchor_path,
    manifest_document_digest,
    verify_anchor_record,
    verify_anchor_record_file,
)
from .export import (
    export_csv_bundle,
    export_json_bundle,
    export_xml_bundle,
    package_export_archive,
    verify_csv_export,
    verify_export_archive,
    verify_json_bundle,
    verify_xml_export,
)
from .manifest import (
    EvidenceManifest,
    ManifestDocument,
    ManifestSignature,
    SignaturePolicy,
    SignerConfig,
    VerificationKey,
)
from .models import EvidenceContext, EvidenceEnvelope, EvidenceEvent, EvidenceHashes
from .recorder import EvidenceRecorder
from .storage import LocalEvidenceStore, open_store

__all__ = [
    "EvidenceBundleBuilder",
    "EvidenceManifest",
    "EvidenceContext",
    "EvidenceEnvelope",
    "EvidenceEvent",
    "EvidenceHashes",
    "EvidenceRecorder",
    "LocalEvidenceStore",
    "ManifestDocument",
    "ManifestSignature",
    "AnchorRecord",
    "SignaturePolicy",
    "SignerConfig",
    "VerificationKey",
    "anchor_manifest_document",
    "create_anchor_record",
    "default_anchor_path",
    "export_csv_bundle",
    "export_json_bundle",
    "export_xml_bundle",
    "manifest_document_digest",
    "open_store",
    "package_export_archive",
    "verify_anchor_record",
    "verify_anchor_record_file",
    "verify_bundle",
    "verify_csv_export",
    "verify_export_archive",
    "verify_json_bundle",
    "verify_xml_export",
]

try:
    from .storage import SqlEvidenceStore
except ImportError:  # pragma: no cover - depends on extras
    SqlEvidenceStore = None  # type: ignore[assignment]
else:
    __all__.append("SqlEvidenceStore")
