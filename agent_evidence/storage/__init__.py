from .base import EvidenceStore
from .factory import is_sql_store_target, open_store
from .local import LocalEvidenceStore
from .migrate import migrate_records

try:
    from .sql import SqlEvidenceStore
except ModuleNotFoundError:  # pragma: no cover - depends on extras
    SqlEvidenceStore = None  # type: ignore[assignment]

__all__ = [
    "EvidenceStore",
    "LocalEvidenceStore",
    "open_store",
    "is_sql_store_target",
    "migrate_records",
]

if SqlEvidenceStore is not None:
    __all__.append("SqlEvidenceStore")
