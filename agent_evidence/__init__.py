"""Public package API for Agent Evidence."""

from .export import (
    export_csv_bundle,
    export_json_bundle,
    verify_csv_export,
    verify_json_bundle,
)
from .manifest import EvidenceManifest, ManifestDocument, ManifestSignature
from .models import EvidenceContext, EvidenceEnvelope, EvidenceEvent, EvidenceHashes
from .recorder import EvidenceRecorder
from .storage import LocalEvidenceStore, open_store

__all__ = [
    "EvidenceManifest",
    "EvidenceContext",
    "EvidenceEnvelope",
    "EvidenceEvent",
    "EvidenceHashes",
    "EvidenceRecorder",
    "LocalEvidenceStore",
    "ManifestDocument",
    "ManifestSignature",
    "export_csv_bundle",
    "export_json_bundle",
    "open_store",
    "verify_csv_export",
    "verify_json_bundle",
]

try:
    from .storage import SqlEvidenceStore
except ImportError:  # pragma: no cover - depends on extras
    SqlEvidenceStore = None  # type: ignore[assignment]
else:
    __all__.append("SqlEvidenceStore")
