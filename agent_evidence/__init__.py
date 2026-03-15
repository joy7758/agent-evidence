"""Public package API for Agent Evidence."""

from .models import EvidenceContext, EvidenceEnvelope, EvidenceEvent, EvidenceHashes
from .recorder import EvidenceRecorder
from .storage import LocalEvidenceStore, open_store

__all__ = [
    "EvidenceContext",
    "EvidenceEnvelope",
    "EvidenceEvent",
    "EvidenceHashes",
    "EvidenceRecorder",
    "LocalEvidenceStore",
    "open_store",
]

try:
    from .storage import SqlEvidenceStore
except ImportError:  # pragma: no cover - depends on extras
    SqlEvidenceStore = None  # type: ignore[assignment]
else:
    __all__.append("SqlEvidenceStore")
