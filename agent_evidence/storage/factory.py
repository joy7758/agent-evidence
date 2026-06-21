from __future__ import annotations

from pathlib import Path

from agent_evidence.storage.base import EvidenceStore
from agent_evidence.storage.local import LocalEvidenceStore

_SQL_PREFIXES = (
    "sqlite://",
    "sqlite+pysqlite://",
    "postgres://",
    "postgresql://",
    "postgresql+psycopg://",
    "postgresql+psycopg2://",
)


def is_sql_store_target(target: str | Path) -> bool:
    value = str(target)
    return value.startswith(_SQL_PREFIXES)


def open_store(target: str | Path) -> EvidenceStore:
    if is_sql_store_target(target):
        try:
            from agent_evidence.storage.sql import SqlEvidenceStore
        except ModuleNotFoundError as exc:  # pragma: no cover - depends on extras
            raise ModuleNotFoundError(
                "SQL storage requires SQLAlchemy. Install agent-evidence with the [sql] "
                "or [postgres] extra."
            ) from exc
        return SqlEvidenceStore(str(target))
    return LocalEvidenceStore(Path(target))
