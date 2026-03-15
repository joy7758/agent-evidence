from __future__ import annotations

from datetime import datetime, timezone
from typing import Any
from uuid import uuid4

from pydantic import BaseModel, ConfigDict, Field


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


class EvidencePayload(BaseModel):
    """Normalized event content captured from an agent runtime."""

    model_config = ConfigDict(extra="allow")

    actor: str = Field(..., description="Logical actor or component producing the event.")
    action: str = Field(..., description="Action or event name.")
    inputs: dict[str, Any] = Field(default_factory=dict, description="Structured inputs.")
    outputs: dict[str, Any] = Field(default_factory=dict, description="Structured outputs.")
    metadata: dict[str, Any] = Field(default_factory=dict, description="Additional context.")
    tags: list[str] = Field(default_factory=list, description="Free-form classification tags.")


class EvidenceEnvelope(BaseModel):
    """Persisted evidence document with deterministic hashing metadata."""

    model_config = ConfigDict(extra="forbid")

    record_id: str = Field(default_factory=lambda: str(uuid4()))
    timestamp: str = Field(default_factory=utc_now_iso)
    payload: EvidencePayload
    payload_digest: str
    previous_digest: str | None = None
    chain_digest: str
    schema_version: str = "1.0.0"
