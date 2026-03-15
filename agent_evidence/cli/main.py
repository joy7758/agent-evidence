from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

import click

from agent_evidence.crypto.chain import verify_chain
from agent_evidence.models import EvidenceEnvelope
from agent_evidence.recorder import EvidenceRecorder
from agent_evidence.storage import migrate_records, open_store
from agent_evidence.storage.base import EvidenceStore


def parse_json_option(raw: str | None) -> dict:
    if raw is None:
        return {}
    value = json.loads(raw)
    if not isinstance(value, dict):
        raise click.BadParameter("Value must decode to a JSON object.")
    return value


def build_store(target: str) -> EvidenceStore:
    return open_store(target)


def parse_datetime_option(raw: str | None) -> datetime | None:
    if raw is None:
        return None
    normalized = raw.replace("Z", "+00:00")
    try:
        value = datetime.fromisoformat(normalized)
    except ValueError as exc:
        raise click.BadParameter(f"Invalid ISO datetime: {raw}") from exc
    if value.tzinfo is None:
        return value.replace(tzinfo=timezone.utc)
    return value


@click.group()
def main() -> None:
    """CLI for recording and inspecting agent evidence."""


@main.command()
@click.option("--store", "store_target", required=True)
@click.option("--actor", required=True)
@click.option("--event-type", "event_type")
@click.option("--action", help="Deprecated alias for --event-type.")
@click.option("--input", "inputs_raw")
@click.option("--output", "outputs_raw")
@click.option("--context", "context_raw")
@click.option("--metadata", "metadata_raw")
@click.option("--tag", "tags", multiple=True)
def record(
    store_target: str,
    actor: str,
    event_type: str | None,
    action: str | None,
    inputs_raw: str | None,
    outputs_raw: str | None,
    context_raw: str | None,
    metadata_raw: str | None,
    tags: tuple[str, ...],
) -> None:
    """Append one evidence record to the local store."""

    resolved_event_type = event_type or action
    if not resolved_event_type:
        raise click.ClickException("One of --event-type or --action is required.")

    recorder = EvidenceRecorder(build_store(store_target))
    envelope = recorder.record(
        actor=actor,
        event_type=resolved_event_type,
        inputs=parse_json_option(inputs_raw),
        outputs=parse_json_option(outputs_raw),
        context=parse_json_option(context_raw),
        metadata=parse_json_option(metadata_raw),
        tags=list(tags),
    )
    click.echo(envelope.model_dump_json(indent=2))


@main.command(name="list")
@click.option("--store", "store_target", required=True)
def list_records(store_target: str) -> None:
    """List records with compact metadata."""

    store = build_store(store_target)
    for index, envelope in enumerate(store.list()):
        click.echo(
            json.dumps(
                {
                    "index": index,
                    "event_id": envelope.event.event_id,
                    "timestamp": envelope.event.timestamp.isoformat(),
                    "actor": envelope.event.actor,
                    "event_type": envelope.event.event_type,
                    "chain_hash": envelope.hashes.chain_hash,
                },
                sort_keys=True,
            )
        )


@main.command()
@click.option("--store", "store_target", required=True)
@click.option("--index", "index_", required=True, type=int)
def show(store_target: str, index_: int) -> None:
    """Show a full record by zero-based index."""

    store = build_store(store_target)
    records = store.list()
    try:
        envelope = records[index_]
    except IndexError as exc:
        raise click.ClickException(f"Record index out of range: {index_}") from exc

    click.echo(envelope.model_dump_json(indent=2))


@main.command()
@click.option("--store", "store_target", required=True)
def verify(store_target: str) -> None:
    """Verify chain integrity for all records in a local store."""

    store = build_store(store_target)
    records = store.list()
    issues = verify_chain(records)
    result = {
        "ok": not issues,
        "records": len(records),
        "latest_chain_hash": records[-1].hashes.chain_hash if records else None,
        "issues": issues,
    }
    click.echo(json.dumps(result, indent=2, sort_keys=True))
    if issues:
        raise click.ClickException("Evidence chain verification failed.")


@main.command()
@click.option("--store", "store_target", required=True)
@click.option("--event-type")
@click.option("--actor")
@click.option("--source")
@click.option("--component")
@click.option("--since")
@click.option("--until")
@click.option("--limit", type=int)
def query(
    store_target: str,
    event_type: str | None,
    actor: str | None,
    source: str | None,
    component: str | None,
    since: str | None,
    until: str | None,
    limit: int | None,
) -> None:
    """Query evidence records by semantic fields and time range."""

    store = build_store(store_target)
    records = store.query(
        event_type=event_type,
        actor=actor,
        source=source,
        component=component,
        since=parse_datetime_option(since),
        until=parse_datetime_option(until),
        limit=limit,
    )
    click.echo(
        json.dumps(
            {
                "count": len(records),
                "records": [record.model_dump(mode="json") for record in records],
            },
            indent=2,
            sort_keys=True,
        )
    )


@main.command()
@click.option("--source", "source_target", required=True)
@click.option("--target", "target_target", required=True)
@click.option("--append", "allow_existing", is_flag=True)
def migrate(source_target: str, target_target: str, allow_existing: bool) -> None:
    """Copy evidence records between local files and SQL backends."""

    source_store = build_store(source_target)
    target_store = build_store(target_target)
    migrated = migrate_records(
        source_store=source_store,
        target_store=target_store,
        allow_existing=allow_existing,
    )
    click.echo(
        json.dumps(
            {
                "migrated": migrated,
                "source": source_target,
                "target": target_target,
            },
            indent=2,
            sort_keys=True,
        )
    )


@main.command()
def schema() -> None:
    """Print the packaged JSON schema."""

    schema_path = Path(__file__).resolve().parents[1] / "schema" / "evidence.schema.json"
    click.echo(schema_path.read_text(encoding="utf-8"))


def load_envelope(raw: str) -> EvidenceEnvelope:
    return EvidenceEnvelope.model_validate_json(raw)
