from __future__ import annotations

import json
from pathlib import Path

import click

from agent_evidence.models import EvidenceEnvelope
from agent_evidence.recorder import EvidenceRecorder
from agent_evidence.storage.local import LocalEvidenceStore


def parse_json_option(raw: str | None) -> dict:
    if raw is None:
        return {}
    value = json.loads(raw)
    if not isinstance(value, dict):
        raise click.BadParameter("Value must decode to a JSON object.")
    return value


def build_store(path: str) -> LocalEvidenceStore:
    return LocalEvidenceStore(Path(path))


@click.group()
def main() -> None:
    """CLI for recording and inspecting agent evidence."""


@main.command()
@click.option("--store", "store_path", required=True, type=click.Path(dir_okay=False))
@click.option("--actor", required=True)
@click.option("--action", required=True)
@click.option("--input", "inputs_raw")
@click.option("--output", "outputs_raw")
@click.option("--metadata", "metadata_raw")
@click.option("--tag", "tags", multiple=True)
def record(
    store_path: str,
    actor: str,
    action: str,
    inputs_raw: str | None,
    outputs_raw: str | None,
    metadata_raw: str | None,
    tags: tuple[str, ...],
) -> None:
    """Append one evidence record to the local store."""

    recorder = EvidenceRecorder(build_store(store_path))
    envelope = recorder.record(
        actor=actor,
        action=action,
        inputs=parse_json_option(inputs_raw),
        outputs=parse_json_option(outputs_raw),
        metadata=parse_json_option(metadata_raw),
        tags=list(tags),
    )
    click.echo(envelope.model_dump_json(indent=2))


@main.command(name="list")
@click.option("--store", "store_path", required=True, type=click.Path(dir_okay=False))
def list_records(store_path: str) -> None:
    """List records with compact metadata."""

    store = build_store(store_path)
    for index, envelope in enumerate(store.list()):
        click.echo(
            json.dumps(
                {
                    "index": index,
                    "record_id": envelope.record_id,
                    "timestamp": envelope.timestamp,
                    "actor": envelope.payload.actor,
                    "action": envelope.payload.action,
                    "chain_digest": envelope.chain_digest,
                },
                sort_keys=True,
            )
        )


@main.command()
@click.option("--store", "store_path", required=True, type=click.Path(dir_okay=False))
@click.option("--index", "index_", required=True, type=int)
def show(store_path: str, index_: int) -> None:
    """Show a full record by zero-based index."""

    store = build_store(store_path)
    records = store.list()
    try:
        envelope = records[index_]
    except IndexError as exc:
        raise click.ClickException(f"Record index out of range: {index_}") from exc

    click.echo(envelope.model_dump_json(indent=2))


@main.command()
def schema() -> None:
    """Print the packaged JSON schema."""

    schema_path = Path(__file__).resolve().parents[1] / "schema" / "evidence.schema.json"
    click.echo(schema_path.read_text(encoding="utf-8"))


def load_envelope(raw: str) -> EvidenceEnvelope:
    return EvidenceEnvelope.model_validate_json(raw)
