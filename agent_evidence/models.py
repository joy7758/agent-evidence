from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Literal
from uuid import uuid4

from pydantic import BaseModel, ConfigDict, Field

SCHEMA_VERSION = "2.0.0"


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class EvidenceContext(BaseModel):
    """Framework-neutral execution context for an evidence event."""

    model_config = ConfigDict(extra="forbid")

    source: str = Field(default="application", description="Originating runtime or adapter.")
    component: str | None = Field(
        default=None,
        description="Component class such as chain, tool, retriever, or llm.",
    )
    source_event_type: str | None = Field(
        default=None,
        description="Original framework event name before semantic normalization.",
    )
    span_id: str | None = Field(default=None, description="Current execution span identifier.")
    parent_span_id: str | None = Field(
        default=None, description="Parent execution span identifier."
    )
    ancestor_span_ids: list[str] = Field(
        default_factory=list,
        description="Ordered ancestor span identifiers from root to immediate parent.",
    )
    name: str | None = Field(default=None, description="Human-readable runtime name.")
    tags: list[str] = Field(default_factory=list, description="Normalized event tags.")
    attributes: dict[str, Any] = Field(
        default_factory=dict,
        description="Additional execution context not modeled as first-class fields.",
    )


class EvidenceEvent(BaseModel):
    """Stable semantic event recorded by Agent Evidence."""

    model_config = ConfigDict(extra="forbid")

    event_id: str = Field(default_factory=lambda: str(uuid4()))
    timestamp: datetime = Field(default_factory=utc_now)
    event_type: str = Field(..., description="Framework-neutral semantic event name.")
    actor: str = Field(..., description="Logical actor that produced the event.")
    inputs: dict[str, Any] = Field(default_factory=dict, description="Structured event inputs.")
    outputs: dict[str, Any] = Field(default_factory=dict, description="Structured event outputs.")
    context: EvidenceContext = Field(default_factory=EvidenceContext)
    metadata: dict[str, Any] = Field(
        default_factory=dict,
        description="User-level metadata or execution configuration.",
    )


class EvidenceHashes(BaseModel):
    """Hash material that links one event envelope to the prior chain state."""

    model_config = ConfigDict(extra="forbid")

    event_hash: str = Field(..., description="Deterministic hash of the semantic event.")
    previous_event_hash: str | None = Field(
        default=None,
        description="Hash pointer to the immediately preceding event.",
    )
    chain_hash: str = Field(..., description="Cumulative chain tip digest.")


class EvidenceEnvelope(BaseModel):
    """Persisted evidence record combining a semantic event with chain hashes."""

    model_config = ConfigDict(extra="forbid")

    schema_version: Literal["2.0.0"] = SCHEMA_VERSION
    event: EvidenceEvent
    hashes: EvidenceHashes
