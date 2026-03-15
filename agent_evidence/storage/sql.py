from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from sqlalchemy import JSON, BigInteger, Index, Integer, String, create_engine, select
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column

from agent_evidence.models import EvidenceEnvelope
from agent_evidence.storage.base import EvidenceStore


def _to_epoch_micros(value: datetime) -> int:
    normalized = value.astimezone(timezone.utc)
    return int(normalized.timestamp() * 1_000_000)


class Base(DeclarativeBase):
    pass


class EvidenceRecordRow(Base):
    __tablename__ = "evidence_records"
    __table_args__ = (
        Index("ix_evidence_records_event_type_ts", "event_type", "timestamp_epoch_us"),
        Index("ix_evidence_records_source_component", "source", "component"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    schema_version: Mapped[str] = mapped_column(String(32), nullable=False)
    event_id: Mapped[str] = mapped_column(String(64), nullable=False, unique=True, index=True)
    event_type: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    actor: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    timestamp: Mapped[str] = mapped_column(String(64), nullable=False)
    timestamp_epoch_us: Mapped[int] = mapped_column(BigInteger, nullable=False, index=True)
    source: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    component: Mapped[str | None] = mapped_column(String(128), nullable=True, index=True)
    span_id: Mapped[str | None] = mapped_column(String(128), nullable=True, index=True)
    parent_span_id: Mapped[str | None] = mapped_column(String(128), nullable=True, index=True)
    previous_event_hash: Mapped[str | None] = mapped_column(String(128), nullable=True, index=True)
    event_hash: Mapped[str] = mapped_column(String(128), nullable=False, unique=True, index=True)
    chain_hash: Mapped[str] = mapped_column(String(128), nullable=False, unique=True, index=True)
    event_json: Mapped[dict[str, Any]] = mapped_column("event", JSON, nullable=False)
    context_json: Mapped[dict[str, Any]] = mapped_column("context", JSON, nullable=False)
    metadata_json: Mapped[dict[str, Any]] = mapped_column("metadata", JSON, nullable=False)
    hashes_json: Mapped[dict[str, Any]] = mapped_column("hashes", JSON, nullable=False)


class SqlEvidenceStore(EvidenceStore):
    """SQLAlchemy-backed evidence store for SQLite and PostgreSQL."""

    def __init__(self, url: str):
        self.url = url
        self.engine = create_engine(url)
        Base.metadata.create_all(self.engine)

    def _from_row(self, row: EvidenceRecordRow) -> EvidenceEnvelope:
        return EvidenceEnvelope.model_validate(
            {
                "schema_version": row.schema_version,
                "event": row.event_json,
                "hashes": row.hashes_json,
            }
        )

    def append(self, envelope: EvidenceEnvelope) -> None:
        payload = envelope.model_dump(mode="json")
        event = payload["event"]
        context = event["context"]
        hashes = payload["hashes"]
        row = EvidenceRecordRow(
            schema_version=payload["schema_version"],
            event_id=event["event_id"],
            event_type=event["event_type"],
            actor=event["actor"],
            timestamp=event["timestamp"],
            timestamp_epoch_us=_to_epoch_micros(envelope.event.timestamp),
            source=context["source"],
            component=context.get("component"),
            span_id=context.get("span_id"),
            parent_span_id=context.get("parent_span_id"),
            previous_event_hash=hashes.get("previous_event_hash"),
            event_hash=hashes["event_hash"],
            chain_hash=hashes["chain_hash"],
            event_json=event,
            context_json=context,
            metadata_json=event["metadata"],
            hashes_json=hashes,
        )
        with Session(self.engine) as session:
            session.add(row)
            session.commit()

    def list(self) -> list[EvidenceEnvelope]:
        return self.query()

    def latest_event_hash(self) -> str | None:
        statement = select(EvidenceRecordRow.event_hash).order_by(
            EvidenceRecordRow.timestamp_epoch_us.desc(),
            EvidenceRecordRow.id.desc(),
        )
        with Session(self.engine) as session:
            return session.execute(statement.limit(1)).scalar_one_or_none()

    def latest_chain_hash(self) -> str | None:
        statement = select(EvidenceRecordRow.chain_hash).order_by(
            EvidenceRecordRow.timestamp_epoch_us.desc(),
            EvidenceRecordRow.id.desc(),
        )
        with Session(self.engine) as session:
            return session.execute(statement.limit(1)).scalar_one_or_none()

    def query(
        self,
        *,
        event_type: str | None = None,
        actor: str | None = None,
        source: str | None = None,
        component: str | None = None,
        span_id: str | None = None,
        parent_span_id: str | None = None,
        previous_event_hash: str | None = None,
        since: datetime | None = None,
        until: datetime | None = None,
        event_hash_from: str | None = None,
        event_hash_to: str | None = None,
        chain_hash_from: str | None = None,
        chain_hash_to: str | None = None,
        offset: int | None = None,
        limit: int | None = None,
    ) -> list[EvidenceEnvelope]:
        statement = select(EvidenceRecordRow).order_by(
            EvidenceRecordRow.timestamp_epoch_us.asc(),
            EvidenceRecordRow.id.asc(),
        )
        if event_type is not None:
            statement = statement.where(EvidenceRecordRow.event_type == event_type)
        if actor is not None:
            statement = statement.where(EvidenceRecordRow.actor == actor)
        if source is not None:
            statement = statement.where(EvidenceRecordRow.source == source)
        if component is not None:
            statement = statement.where(EvidenceRecordRow.component == component)
        if span_id is not None:
            statement = statement.where(EvidenceRecordRow.span_id == span_id)
        if parent_span_id is not None:
            statement = statement.where(EvidenceRecordRow.parent_span_id == parent_span_id)
        if previous_event_hash is not None:
            statement = statement.where(
                EvidenceRecordRow.previous_event_hash == previous_event_hash
            )
        if since is not None:
            statement = statement.where(
                EvidenceRecordRow.timestamp_epoch_us >= _to_epoch_micros(since)
            )
        if until is not None:
            statement = statement.where(
                EvidenceRecordRow.timestamp_epoch_us <= _to_epoch_micros(until)
            )
        if event_hash_from is not None:
            statement = statement.where(EvidenceRecordRow.event_hash >= event_hash_from)
        if event_hash_to is not None:
            statement = statement.where(EvidenceRecordRow.event_hash <= event_hash_to)
        if chain_hash_from is not None:
            statement = statement.where(EvidenceRecordRow.chain_hash >= chain_hash_from)
        if chain_hash_to is not None:
            statement = statement.where(EvidenceRecordRow.chain_hash <= chain_hash_to)
        if offset is not None:
            statement = statement.offset(offset)
        if limit is not None:
            statement = statement.limit(limit)

        with Session(self.engine) as session:
            rows = session.scalars(statement).all()
        return [self._from_row(row) for row in rows]
