from __future__ import annotations

import json
from collections.abc import Callable
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import click
from pydantic import ValidationError

from agent_evidence.aep import load_bundle_payload, verify_bundle
from agent_evidence.anchor import default_anchor_path
from agent_evidence.crypto.chain import verify_chain
from agent_evidence.export import (
    default_manifest_path,
    export_csv_bundle,
    export_json_bundle,
    export_xml_bundle,
    package_export_archive,
    verify_csv_export,
    verify_export_archive,
    verify_json_bundle,
    verify_xml_export,
)
from agent_evidence.integrations import export_automaton_bundle
from agent_evidence.manifest import SignaturePolicy, SignerConfig, VerificationKey
from agent_evidence.models import EvidenceEnvelope
from agent_evidence.recorder import EvidenceRecorder
from agent_evidence.storage import migrate_records, open_store
from agent_evidence.storage.base import EvidenceStore


def parse_json_option(raw: str | None) -> dict:
    if raw is None:
        return {}
    try:
        value = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise click.BadParameter(f"Invalid JSON: {raw}") from exc
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


def load_json_file(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise click.ClickException(f"Invalid JSON file: {path}") from exc


def resolve_path_reference(config_path: Path, raw_path: str) -> Path:
    candidate = Path(raw_path)
    if candidate.is_absolute():
        return candidate
    return (config_path.parent / candidate).resolve()


def load_signer_config(path: Path) -> SignerConfig:
    payload = load_json_file(path)
    if not isinstance(payload, dict):
        raise click.ClickException(f"Signer config must be a JSON object: {path}")

    private_key_ref = payload.get("private_key")
    if not isinstance(private_key_ref, str) or not private_key_ref:
        raise click.ClickException(f"Signer config requires 'private_key': {path}")

    metadata = payload.get("metadata") or {}
    if not isinstance(metadata, dict):
        raise click.ClickException(f"Signer config 'metadata' must be a JSON object: {path}")

    private_key_path = resolve_path_reference(path, private_key_ref)
    return SignerConfig(
        private_key_pem=private_key_path.read_bytes(),
        key_id=payload.get("key_id"),
        key_version=payload.get("key_version"),
        signed_at=payload.get("signed_at"),
        signer=payload.get("signer"),
        role=payload.get("role"),
        metadata=metadata,
    )


def load_keyring(path: Path) -> list[VerificationKey]:
    payload = load_json_file(path)
    raw_keys = payload.get("keys") if isinstance(payload, dict) else payload
    if not isinstance(raw_keys, list):
        raise click.ClickException(f"Keyring must be a JSON array or an object with 'keys': {path}")

    verification_keys: list[VerificationKey] = []
    for index, raw_key in enumerate(raw_keys):
        if not isinstance(raw_key, dict):
            raise click.ClickException(f"Keyring entry {index} must be a JSON object: {path}")
        public_key_ref = raw_key.get("public_key")
        if not isinstance(public_key_ref, str) or not public_key_ref:
            raise click.ClickException(f"Keyring entry {index} requires 'public_key': {path}")

        public_key_path = resolve_path_reference(path, public_key_ref)
        verification_keys.append(
            VerificationKey(
                public_key_pem=public_key_path.read_bytes(),
                key_id=raw_key.get("key_id"),
                key_version=raw_key.get("key_version"),
            )
        )
    return verification_keys


def build_signer_configs(
    *,
    private_key: Path | None,
    key_id: str | None,
    key_version: str | None,
    signer: str | None,
    signature_role: str | None,
    signature_metadata_raw: str | None,
    signed_at: str | None,
    signer_config_paths: tuple[Path, ...],
) -> list[SignerConfig]:
    signer_configs = [load_signer_config(path) for path in signer_config_paths]
    if private_key is not None:
        signer_configs.insert(
            0,
            SignerConfig(
                private_key_pem=private_key.read_bytes(),
                key_id=key_id,
                key_version=key_version,
                signed_at=parse_datetime_option(signed_at).isoformat() if signed_at else None,
                signer=signer,
                role=signature_role,
                metadata=parse_json_option(signature_metadata_raw),
            ),
        )
    return signer_configs


def build_verification_keys(
    *,
    public_key: Path | None,
    key_id: str | None,
    key_version: str | None,
    keyring: Path | None,
) -> list[VerificationKey]:
    verification_keys = load_keyring(keyring) if keyring is not None else []
    if public_key is not None:
        verification_keys.insert(
            0,
            VerificationKey(
                public_key_pem=public_key.read_bytes(),
                key_id=key_id,
                key_version=key_version,
                is_direct=True,
            ),
        )
    return verification_keys


def parse_role_thresholds(raw_values: tuple[str, ...]) -> dict[str, int]:
    role_thresholds: dict[str, int] = {}
    for raw_value in raw_values:
        role, separator, raw_count = raw_value.partition("=")
        normalized_role = role.strip()
        if separator != "=" or not normalized_role or not raw_count.strip():
            raise click.BadParameter("Role thresholds must use the form <role>=<count>.")
        try:
            count = int(raw_count)
        except ValueError as exc:
            raise click.BadParameter(
                f"Role threshold count must be an integer: {raw_value}"
            ) from exc
        if normalized_role in role_thresholds:
            raise click.BadParameter(f"Duplicate role threshold provided: {normalized_role}")
        role_thresholds[normalized_role] = count
    try:
        policy = SignaturePolicy(minimum_valid_signatures_by_role=role_thresholds)
    except ValidationError as exc:
        raise click.BadParameter(str(exc)) from exc
    return policy.minimum_valid_signatures_by_role


def validate_signature_policy(
    *,
    required_signatures: int | None,
    role_thresholds: dict[str, int],
) -> SignaturePolicy:
    try:
        return SignaturePolicy(
            minimum_valid_signatures=required_signatures,
            minimum_valid_signatures_by_role=role_thresholds,
        )
    except ValidationError as exc:
        raise click.BadParameter(str(exc)) from exc


def add_query_filter_options(function: Callable[..., Any]) -> Callable[..., Any]:
    options = [
        click.option("--event-type"),
        click.option("--actor"),
        click.option("--source"),
        click.option("--component"),
        click.option("--span-id"),
        click.option("--parent-span-id"),
        click.option("--previous-event-hash"),
        click.option("--since"),
        click.option("--until"),
        click.option("--event-hash-from"),
        click.option("--event-hash-to"),
        click.option("--chain-hash-from"),
        click.option("--chain-hash-to"),
        click.option("--offset", type=click.IntRange(min=0)),
        click.option("--limit", type=click.IntRange(min=0)),
    ]
    decorated = function
    for option in reversed(options):
        decorated = option(decorated)
    return decorated


def build_query_kwargs(
    *,
    event_type: str | None,
    actor: str | None,
    source: str | None,
    component: str | None,
    span_id: str | None,
    parent_span_id: str | None,
    previous_event_hash: str | None,
    since: str | None,
    until: str | None,
    event_hash_from: str | None,
    event_hash_to: str | None,
    chain_hash_from: str | None,
    chain_hash_to: str | None,
    offset: int | None,
    limit: int | None,
) -> dict[str, Any]:
    return {
        "event_type": event_type,
        "actor": actor,
        "source": source,
        "component": component,
        "span_id": span_id,
        "parent_span_id": parent_span_id,
        "previous_event_hash": previous_event_hash,
        "since": parse_datetime_option(since),
        "until": parse_datetime_option(until),
        "event_hash_from": event_hash_from,
        "event_hash_to": event_hash_to,
        "chain_hash_from": chain_hash_from,
        "chain_hash_to": chain_hash_to,
        "offset": offset,
        "limit": limit,
    }


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
@add_query_filter_options
def query(
    store_target: str,
    event_type: str | None,
    actor: str | None,
    source: str | None,
    component: str | None,
    span_id: str | None,
    parent_span_id: str | None,
    previous_event_hash: str | None,
    since: str | None,
    until: str | None,
    event_hash_from: str | None,
    event_hash_to: str | None,
    chain_hash_from: str | None,
    chain_hash_to: str | None,
    offset: int | None,
    limit: int | None,
) -> None:
    """Query evidence records by semantic fields, chain pointers, and hash ranges."""

    store = build_store(store_target)
    query_kwargs = build_query_kwargs(
        event_type=event_type,
        actor=actor,
        source=source,
        component=component,
        span_id=span_id,
        parent_span_id=parent_span_id,
        previous_event_hash=previous_event_hash,
        since=since,
        until=until,
        event_hash_from=event_hash_from,
        event_hash_to=event_hash_to,
        chain_hash_from=chain_hash_from,
        chain_hash_to=chain_hash_to,
        offset=offset,
        limit=limit,
    )
    records = store.query(**query_kwargs)
    click.echo(
        json.dumps(
            {
                "count": len(records),
                "returned": len(records),
                "offset": offset or 0,
                "limit": limit,
                "records": [record.model_dump(mode="json") for record in records],
            },
            indent=2,
            sort_keys=True,
        )
    )


def _export_records_impl(
    *,
    store_target: str,
    export_format: str,
    output_path: Path,
    manifest_output: Path | None,
    private_key: Path | None,
    key_id: str | None,
    key_version: str | None,
    signer: str | None,
    signature_role: str | None,
    signature_metadata: str | None,
    signed_at: str | None,
    archive_format: str | None,
    should_anchor: bool,
    anchor_output: Path | None,
    anchor_type: str,
    anchor_id: str | None,
    required_signatures: int | None,
    required_signature_roles: tuple[str, ...],
    signer_config_paths: tuple[Path, ...],
    event_type: str | None,
    actor: str | None,
    source: str | None,
    component: str | None,
    span_id: str | None,
    parent_span_id: str | None,
    previous_event_hash: str | None,
    since: str | None,
    until: str | None,
    event_hash_from: str | None,
    event_hash_to: str | None,
    chain_hash_from: str | None,
    chain_hash_to: str | None,
    offset: int | None,
    limit: int | None,
) -> None:
    """Export evidence records as a JSON bundle, CSV artifact, or XML artifact."""

    store = build_store(store_target)
    role_thresholds = parse_role_thresholds(required_signature_roles)
    validate_signature_policy(
        required_signatures=required_signatures,
        role_thresholds=role_thresholds,
    )
    query_kwargs = build_query_kwargs(
        event_type=event_type,
        actor=actor,
        source=source,
        component=component,
        span_id=span_id,
        parent_span_id=parent_span_id,
        previous_event_hash=previous_event_hash,
        since=since,
        until=until,
        event_hash_from=event_hash_from,
        event_hash_to=event_hash_to,
        chain_hash_from=chain_hash_from,
        chain_hash_to=chain_hash_to,
        offset=offset,
        limit=limit,
    )
    records = store.query(**query_kwargs)
    if archive_format is not None and manifest_output is not None:
        raise click.ClickException(
            "--manifest-output cannot be used with --archive-format; "
            "the package includes its own manifest path."
        )
    if archive_format == "zip" and output_path.suffix.lower() != ".zip":
        raise click.ClickException("--archive-format zip requires an output path ending in .zip.")
    if archive_format == "tar.gz" and not (
        output_path.name.lower().endswith(".tar.gz") or output_path.name.lower().endswith(".tgz")
    ):
        raise click.ClickException(
            "--archive-format tar.gz requires an output path ending in .tar.gz or .tgz."
        )
    resolved_anchor_output: Path | None = anchor_output
    if should_anchor or anchor_output is not None:
        if archive_format is not None:
            anchor_target = output_path
        elif export_format == "json":
            anchor_target = manifest_output or output_path
        else:
            anchor_target = manifest_output or default_manifest_path(output_path)
        resolved_anchor_output = anchor_output or default_anchor_path(anchor_target)
    signer_configs = build_signer_configs(
        private_key=private_key,
        key_id=key_id,
        key_version=key_version,
        signer=signer,
        signature_role=signature_role,
        signature_metadata_raw=signature_metadata,
        signed_at=signed_at,
        signer_config_paths=signer_config_paths,
    )

    manifest_path: Path | None = manifest_output
    if archive_format is not None:
        package_result = package_export_archive(
            records,
            output_path,
            export_format=export_format,
            filters=query_kwargs,
            signer_configs=signer_configs,
            minimum_valid_signatures=required_signatures,
            minimum_valid_signatures_by_role=role_thresholds,
            anchor_output_path=resolved_anchor_output,
            anchor_type=anchor_type,
            anchor_id=anchor_id,
        )
        click.echo(
            json.dumps(
                {
                    "archive_format": archive_format,
                    "anchor_output": str(resolved_anchor_output)
                    if resolved_anchor_output
                    else None,
                    "anchor_type": anchor_type if resolved_anchor_output else None,
                    "format": export_format,
                    "output": str(output_path),
                    "artifact_path": package_result["artifact_path"],
                    "manifest_output": package_result["manifest_path"],
                    "packaged": True,
                    "record_count": len(records),
                    "signed": package_result["signature_count"] > 0,
                    "signature_count": package_result["signature_count"],
                    "required_signatures": required_signatures,
                    "required_signature_roles": role_thresholds,
                },
                indent=2,
                sort_keys=True,
            )
        )
        return
    if export_format == "json":
        bundle = export_json_bundle(
            records,
            output_path,
            filters=query_kwargs,
            signer_configs=signer_configs,
            minimum_valid_signatures=required_signatures,
            minimum_valid_signatures_by_role=role_thresholds,
            manifest_output_path=manifest_output,
            anchor_output_path=resolved_anchor_output,
            anchor_type=anchor_type,
            anchor_id=anchor_id,
        )
        signature_count = len(bundle.signatures)
    elif export_format == "csv":
        manifest_path = manifest_output or default_manifest_path(output_path)
        manifest_document = export_csv_bundle(
            records,
            output_path,
            manifest_output_path=manifest_path,
            filters=query_kwargs,
            signer_configs=signer_configs,
            minimum_valid_signatures=required_signatures,
            minimum_valid_signatures_by_role=role_thresholds,
            anchor_output_path=resolved_anchor_output,
            anchor_type=anchor_type,
            anchor_id=anchor_id,
        )
        signature_count = len(manifest_document.signatures)
    else:
        manifest_path = manifest_output or default_manifest_path(output_path)
        manifest_document = export_xml_bundle(
            records,
            output_path,
            manifest_output_path=manifest_path,
            filters=query_kwargs,
            signer_configs=signer_configs,
            minimum_valid_signatures=required_signatures,
            minimum_valid_signatures_by_role=role_thresholds,
            anchor_output_path=resolved_anchor_output,
            anchor_type=anchor_type,
            anchor_id=anchor_id,
        )
        signature_count = len(manifest_document.signatures)

    click.echo(
        json.dumps(
            {
                "anchor_output": str(resolved_anchor_output) if resolved_anchor_output else None,
                "anchor_type": anchor_type if resolved_anchor_output else None,
                "format": export_format,
                "output": str(output_path),
                "manifest_output": str(manifest_path) if manifest_path is not None else None,
                "record_count": len(records),
                "signed": signature_count > 0,
                "signature_count": signature_count,
                "required_signatures": required_signatures,
                "required_signature_roles": role_thresholds,
            },
            indent=2,
            sort_keys=True,
        )
    )


@main.group(name="export", invoke_without_command=True)
@click.pass_context
@click.option("--store", "store_target")
@click.option(
    "--format",
    "export_format",
    type=click.Choice(["json", "csv", "xml"]),
    default="json",
    show_default=True,
)
@click.option(
    "--output",
    "output_path",
    type=click.Path(dir_okay=False, path_type=Path),
)
@click.option(
    "--manifest-output",
    type=click.Path(dir_okay=False, path_type=Path),
)
@click.option(
    "--private-key",
    type=click.Path(exists=True, dir_okay=False, path_type=Path),
)
@click.option("--key-id")
@click.option("--key-version")
@click.option("--signer")
@click.option("--signature-role")
@click.option("--signature-metadata")
@click.option("--signed-at")
@click.option("--archive-format", type=click.Choice(["zip", "tar.gz"]))
@click.option("--anchor", "should_anchor", is_flag=True)
@click.option("--anchor-output", type=click.Path(dir_okay=False, path_type=Path))
@click.option(
    "--anchor-type",
    type=click.Choice(["local_timestamp"]),
    default="local_timestamp",
    show_default=True,
)
@click.option("--anchor-id")
@click.option("--required-signatures", type=click.IntRange(min=1))
@click.option("--required-signature-role", "required_signature_roles", multiple=True)
@click.option(
    "--signer-config",
    "signer_config_paths",
    multiple=True,
    type=click.Path(exists=True, dir_okay=False, path_type=Path),
)
@add_query_filter_options
def export_command(
    ctx: click.Context,
    store_target: str,
    export_format: str,
    output_path: Path | None,
    manifest_output: Path | None,
    private_key: Path | None,
    key_id: str | None,
    key_version: str | None,
    signer: str | None,
    signature_role: str | None,
    signature_metadata: str | None,
    signed_at: str | None,
    archive_format: str | None,
    should_anchor: bool,
    anchor_output: Path | None,
    anchor_type: str,
    anchor_id: str | None,
    required_signatures: int | None,
    required_signature_roles: tuple[str, ...],
    signer_config_paths: tuple[Path, ...],
    event_type: str | None,
    actor: str | None,
    source: str | None,
    component: str | None,
    span_id: str | None,
    parent_span_id: str | None,
    previous_event_hash: str | None,
    since: str | None,
    until: str | None,
    event_hash_from: str | None,
    event_hash_to: str | None,
    chain_hash_from: str | None,
    chain_hash_to: str | None,
    offset: int | None,
    limit: int | None,
) -> None:
    """Export evidence artifacts. Use `export automaton` for the experimental runtime path."""

    if ctx.invoked_subcommand is not None:
        return

    if store_target is None or output_path is None:
        raise click.ClickException(
            "Use `agent-evidence export automaton ...` or provide both --store and --output "
            "for record export."
        )

    _export_records_impl(
        store_target=store_target,
        export_format=export_format,
        output_path=output_path,
        manifest_output=manifest_output,
        private_key=private_key,
        key_id=key_id,
        key_version=key_version,
        signer=signer,
        signature_role=signature_role,
        signature_metadata=signature_metadata,
        signed_at=signed_at,
        archive_format=archive_format,
        should_anchor=should_anchor,
        anchor_output=anchor_output,
        anchor_type=anchor_type,
        anchor_id=anchor_id,
        required_signatures=required_signatures,
        required_signature_roles=required_signature_roles,
        signer_config_paths=signer_config_paths,
        event_type=event_type,
        actor=actor,
        source=source,
        component=component,
        span_id=span_id,
        parent_span_id=parent_span_id,
        previous_event_hash=previous_event_hash,
        since=since,
        until=until,
        event_hash_from=event_hash_from,
        event_hash_to=event_hash_to,
        chain_hash_from=chain_hash_from,
        chain_hash_to=chain_hash_to,
        offset=offset,
        limit=limit,
    )


@export_command.command(name="automaton")
@click.option(
    "--state-db",
    required=True,
    type=click.Path(exists=True, dir_okay=False, path_type=Path),
)
@click.option(
    "--repo",
    "repo_root",
    default=Path.home() / ".automaton",
    show_default=True,
    type=click.Path(file_okay=False, path_type=Path),
)
@click.option(
    "--out",
    "output_dir",
    required=True,
    type=click.Path(file_okay=False, path_type=Path),
)
@click.option(
    "--runtime-root",
    type=click.Path(exists=True, file_okay=False, path_type=Path),
    help="Optional Automaton runtime checkout used to resolve version/commit metadata.",
)
@click.option("--limit", type=click.IntRange(min=1), default=50, show_default=True)
@click.option("--verify/--no-verify", "should_verify", default=True, show_default=True)
def export_automaton_command(
    state_db: Path,
    repo_root: Path,
    output_dir: Path,
    runtime_root: Path | None,
    limit: int,
    should_verify: bool,
) -> None:
    """Experimental: export a read-only Automaton snapshot into an AEP bundle."""

    bundle_dir = export_automaton_bundle(
        state_db_path=state_db,
        repo_root=repo_root,
        runtime_root=runtime_root,
        output_dir=output_dir,
        limit=limit,
    )
    manifest = load_bundle_payload(bundle_dir)["manifest"]
    verify_result = verify_bundle(bundle_dir) if should_verify else None

    click.echo(
        json.dumps(
            {
                "bundle_dir": str(bundle_dir),
                "capture_mode": manifest.get("capture_mode"),
                "experimental": True,
                "manifest": manifest,
                "verified": verify_result["ok"] if verify_result is not None else None,
                "verify_result": verify_result,
            },
            indent=2,
            sort_keys=True,
        )
    )
    if verify_result is not None and not verify_result["ok"]:
        raise click.ClickException("Automaton bundle verification failed.")


@main.command(name="verify-export")
@click.option("--archive", type=click.Path(exists=True, dir_okay=False, path_type=Path))
@click.option("--bundle", type=click.Path(exists=True, dir_okay=False, path_type=Path))
@click.option("--csv", "csv_path", type=click.Path(exists=True, dir_okay=False, path_type=Path))
@click.option("--xml", "xml_path", type=click.Path(exists=True, dir_okay=False, path_type=Path))
@click.option(
    "--anchor", "anchor_path", type=click.Path(exists=True, dir_okay=False, path_type=Path)
)
@click.option(
    "--manifest",
    "manifest_path",
    type=click.Path(exists=True, dir_okay=False, path_type=Path),
)
@click.option(
    "--public-key",
    type=click.Path(exists=True, dir_okay=False, path_type=Path),
)
@click.option("--key-id")
@click.option("--key-version")
@click.option(
    "--keyring",
    type=click.Path(exists=True, dir_okay=False, path_type=Path),
)
@click.option("--required-signatures", type=click.IntRange(min=1))
@click.option("--required-signature-role", "required_signature_roles", multiple=True)
def verify_export_command(
    archive: Path | None,
    bundle: Path | None,
    csv_path: Path | None,
    xml_path: Path | None,
    anchor_path: Path | None,
    manifest_path: Path | None,
    public_key: Path | None,
    key_id: str | None,
    key_version: str | None,
    keyring: Path | None,
    required_signatures: int | None,
    required_signature_roles: tuple[str, ...],
) -> None:
    """Verify an exported JSON bundle, CSV artifact, or XML artifact."""

    if archive is not None and (
        bundle is not None
        or csv_path is not None
        or xml_path is not None
        or manifest_path is not None
    ):
        raise click.ClickException(
            "Use --archive or one of --bundle, --csv/--manifest, or --xml/--manifest, not both."
        )
    if bundle is not None and (
        csv_path is not None or xml_path is not None or manifest_path is not None
    ):
        raise click.ClickException(
            "Use --bundle or one of the --csv/--manifest or --xml/--manifest pairs, not both."
        )
    if archive is None and bundle is None:
        artifact_count = int(csv_path is not None) + int(xml_path is not None)
        if artifact_count != 1 or manifest_path is None:
            raise click.ClickException(
                "Provide --archive, --bundle, or exactly one of --csv or --xml "
                "together with --manifest."
            )

    verification_keys = build_verification_keys(
        public_key=public_key,
        key_id=key_id,
        key_version=key_version,
        keyring=keyring,
    )
    role_thresholds = parse_role_thresholds(required_signature_roles)
    validate_signature_policy(
        required_signatures=required_signatures,
        role_thresholds=role_thresholds,
    )
    if archive is not None:
        result = verify_export_archive(
            archive,
            verification_keys=verification_keys,
            minimum_valid_signatures=required_signatures,
            minimum_valid_signatures_by_role=role_thresholds or None,
            anchor_path=anchor_path,
        )
    elif bundle is not None:
        result = verify_json_bundle(
            bundle,
            verification_keys=verification_keys,
            minimum_valid_signatures=required_signatures,
            minimum_valid_signatures_by_role=role_thresholds or None,
            anchor_path=anchor_path,
        )
    elif csv_path is not None:
        result = verify_csv_export(
            csv_path,
            manifest_path,
            verification_keys=verification_keys,
            minimum_valid_signatures=required_signatures,
            minimum_valid_signatures_by_role=role_thresholds or None,
            anchor_path=anchor_path,
        )
    else:
        result = verify_xml_export(
            xml_path,
            manifest_path,
            verification_keys=verification_keys,
            minimum_valid_signatures=required_signatures,
            minimum_valid_signatures_by_role=role_thresholds or None,
            anchor_path=anchor_path,
        )

    click.echo(json.dumps(result, indent=2, sort_keys=True))
    if not result["ok"]:
        raise click.ClickException("Export verification failed.")


@main.command(name="verify-bundle")
@click.option(
    "--bundle-dir",
    required=True,
    type=click.Path(exists=True, file_okay=False, path_type=Path),
)
def verify_bundle_command(bundle_dir: Path) -> None:
    """Verify an Agent Evidence Profile bundle directory offline."""

    result = verify_bundle(bundle_dir)
    click.echo(json.dumps(result, indent=2, sort_keys=True))
    if not result["ok"]:
        raise click.ClickException("Bundle verification failed.")


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
