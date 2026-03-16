from __future__ import annotations

import json
import sqlite3
import subprocess
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

from agent_evidence.aep import EvidenceBundleBuilder, load_bundle_payload
from agent_evidence.aep.bundle import DEFAULT_COMPATIBILITY_TARGETS
from agent_evidence.aep.canonicalizer import canonicalize
from agent_evidence.aep.hash_chain import sha256_digest

AUTOMATON_COMPATIBILITY_TARGETS = canonicalize(
    {
        **DEFAULT_COMPATIBILITY_TARGETS,
        "automaton": {
            "status": "reference-runtime",
            "field_paths": {
                "identity.address": "payload.attributes.automaton.identity.address",
                "identity.creator": "payload.attributes.automaton.identity.creator",
                "source_table": "payload.source_table",
            },
        },
    }
)


@dataclass(frozen=True)
class RuntimeMetadata:
    version: str | None = None
    commit: str | None = None
    dirty: bool | None = None


def _safe_json(value: Any) -> Any:
    if value is None or not isinstance(value, str):
        return value
    text = value.strip()
    if not text:
        return ""
    if text[0] not in "[{":
        return value
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return value


def _digest_slot(value: Any, *, omit: bool = False) -> dict[str, Any]:
    if omit:
        return {"mode": "omitted"}
    normalized = canonicalize(_safe_json(value))
    if normalized is None or normalized == "" or normalized == {} or normalized == []:
        return {"mode": "absent"}
    return {
        "mode": "digest_only",
        "digest": sha256_digest(normalized),
    }


def _open_readonly_database(state_db_path: str | Path) -> sqlite3.Connection:
    target = Path(state_db_path).expanduser().resolve()
    connection = sqlite3.connect(f"file:{target}?mode=ro", uri=True)
    connection.row_factory = sqlite3.Row
    return connection


def _table_exists(connection: sqlite3.Connection, table_name: str) -> bool:
    row = connection.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name = ?",
        (table_name,),
    ).fetchone()
    return row is not None


def _query_rows(
    connection: sqlite3.Connection,
    *,
    table_name: str,
    order_by: str,
    limit: int,
) -> list[dict[str, Any]]:
    if not _table_exists(connection, table_name):
        return []
    rows = connection.execute(
        f"SELECT * FROM {table_name} ORDER BY {order_by} ASC LIMIT ?",
        (limit,),
    ).fetchall()
    return [dict(row) for row in rows]


def _list_table_names(connection: sqlite3.Connection) -> list[str]:
    rows = connection.execute(
        "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name ASC"
    ).fetchall()
    return [str(row["name"]) for row in rows]


def _load_identity_snapshot(
    connection: sqlite3.Connection,
) -> tuple[dict[str, Any], dict[str, Any] | None]:
    identity: dict[str, Any] = {}
    if _table_exists(connection, "identity"):
        rows = connection.execute("SELECT key, value FROM identity ORDER BY key ASC").fetchall()
        identity = {str(row["key"]): row["value"] for row in rows}

    registry_entry: dict[str, Any] | None = None
    if _table_exists(connection, "registry"):
        row = connection.execute(
            "SELECT * FROM registry ORDER BY registered_at DESC LIMIT 1"
        ).fetchone()
        if row is not None:
            registry_entry = dict(row)
    return identity, registry_entry


def _identity_ref(identity: dict[str, Any], registry_entry: dict[str, Any] | None) -> str | None:
    if registry_entry and registry_entry.get("agent_uri"):
        return str(registry_entry["agent_uri"])
    address = identity.get("address")
    if not address:
        return None
    chain_type = identity.get("chainType") or "evm"
    if chain_type == "solana":
        return f"solana:mainnet:{address}"
    return f"eip155:8453:{address}"


def _load_package_version(start: Path) -> str | None:
    candidates = [start] + list(start.parents)
    for candidate in candidates:
        package_json = candidate / "package.json"
        if not package_json.exists():
            continue
        try:
            payload = json.loads(package_json.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            continue
        version = payload.get("version")
        if isinstance(version, str) and version.strip():
            return version.strip()
    return None


def _git_stdout(runtime_root: Path, *args: str, allow_empty: bool = False) -> str | None:
    try:
        result = subprocess.run(
            ["git", "-C", str(runtime_root), *args],
            check=True,
            capture_output=True,
            text=True,
        )
    except (OSError, subprocess.CalledProcessError):
        return None
    value = result.stdout.strip()
    if value:
        return value
    if allow_empty:
        return ""
    return None


def _detect_runtime_metadata(runtime_root: str | Path | None) -> RuntimeMetadata:
    if runtime_root is None:
        return RuntimeMetadata()

    target = Path(runtime_root).expanduser().resolve()
    version: str | None = None
    commit = _git_stdout(target, "rev-parse", "HEAD")
    dirty_output = _git_stdout(target, "status", "--short", allow_empty=True)
    dirty = None if dirty_output is None else bool(dirty_output)

    describe = _git_stdout(target, "describe", "--tags", "--always")
    if describe is not None:
        version = describe

    if version is None:
        version = _load_package_version(target)

    if version is None:
        version = "unknown-but-provided-runtime-root"

    return RuntimeMetadata(version=version, commit=commit, dirty=dirty)


def _source_schema_fingerprint(connection: sqlite3.Connection, *, table_names: list[str]) -> str:
    schema_snapshot: dict[str, Any] = {}
    for table_name in table_names:
        columns = connection.execute(f"PRAGMA table_info({table_name})").fetchall()
        schema_snapshot[table_name] = [
            {
                "name": row["name"],
                "type": row["type"],
                "notnull": row["notnull"],
                "pk": row["pk"],
            }
            for row in columns
        ]
    return sha256_digest(schema_snapshot)


DEFAULT_POLICY_REF = "urn:aep:policy:automaton-readonly-export"


def _policy_ref(policy_rows: list[dict[str, Any]]) -> str:
    if not policy_rows:
        return DEFAULT_POLICY_REF
    digest = sha256_digest(
        [
            {
                "id": row.get("id"),
                "tool_name": row.get("tool_name"),
                "decision": row.get("decision"),
            }
            for row in policy_rows
        ]
    )
    return f"urn:aep:policy:{digest[7:19]}"


def _stable_run_id(
    *,
    identity: dict[str, Any],
    turn_rows: list[dict[str, Any]],
    tool_rows: list[dict[str, Any]],
    modification_rows: list[dict[str, Any]],
    transaction_rows: list[dict[str, Any]],
    onchain_rows: list[dict[str, Any]],
) -> str:
    digest = sha256_digest(
        {
            "identity": {
                "address": identity.get("address"),
                "creator": identity.get("creator"),
                "automatonId": identity.get("automatonId"),
            },
            "turn_ids": [row.get("id") for row in turn_rows],
            "tool_ids": [row.get("id") for row in tool_rows],
            "modification_ids": [row.get("id") for row in modification_rows],
            "transaction_ids": [row.get("id") for row in transaction_rows],
            "onchain_ids": [row.get("id") or row.get("tx_hash") for row in onchain_rows],
        }
    )
    return f"automaton-export-{digest[7:19]}"


def _trace_ref(run_id: str) -> str:
    return f"urn:aep:trace:{run_id}"


def _base_attributes(
    identity: dict[str, Any],
    registry_entry: dict[str, Any] | None,
    *,
    span_kind: str,
    operation_name: str,
) -> dict[str, Any]:
    return {
        "automaton": {
            "identity": {
                "address": identity.get("address"),
                "creator": identity.get("creator"),
                "automaton_id": identity.get("automatonId"),
                "chain_type": identity.get("chainType"),
                "name": identity.get("name"),
            },
            "registry": registry_entry or {},
        },
        "openinference": {
            "span_kind": span_kind,
        },
        "gen_ai": {
            "system": "automaton",
            "operation_name": operation_name,
        },
    }


def _event_timestamp(row: dict[str, Any], *keys: str) -> str:
    for key in keys:
        value = row.get(key)
        if value:
            return str(value)
    return "1970-01-01T00:00:00+00:00"


def _sort_timestamp(timestamp: str) -> datetime:
    return datetime.fromisoformat(timestamp.replace("Z", "+00:00"))


def _turn_events(
    rows: list[dict[str, Any]], identity: dict[str, Any], registry_entry: dict[str, Any] | None
) -> list[dict[str, Any]]:
    events = []
    for row in rows:
        events.append(
            {
                "sort_key": ("turns", str(row.get("id"))),
                "timestamp": _event_timestamp(row, "timestamp", "created_at"),
                "event_type": "trace.turn",
                "payload": {
                    "source": "automaton",
                    "source_table": "turns",
                    "record_id": row.get("id"),
                    "body": {
                        "state": row.get("state"),
                        "input_source": row.get("input_source"),
                        "cost_cents": row.get("cost_cents"),
                        "created_at": row.get("created_at"),
                    },
                    "attributes": _base_attributes(
                        identity,
                        registry_entry,
                        span_kind="AGENT",
                        operation_name="turn",
                    ),
                    "request": _digest_slot(row.get("input")),
                    "response": _digest_slot(
                        {
                            "thinking": row.get("thinking"),
                            "tool_calls": _safe_json(row.get("tool_calls")),
                            "token_usage": _safe_json(row.get("token_usage")),
                        }
                    ),
                },
            }
        )
    return events


def _tool_events(
    rows: list[dict[str, Any]], identity: dict[str, Any], registry_entry: dict[str, Any] | None
) -> list[dict[str, Any]]:
    events = []
    for row in rows:
        events.append(
            {
                "sort_key": ("tool_calls", str(row.get("id"))),
                "timestamp": _event_timestamp(row, "created_at"),
                "event_type": "action.tool",
                "payload": {
                    "source": "automaton",
                    "source_table": "tool_calls",
                    "record_id": row.get("id"),
                    "body": {
                        "turn_id": row.get("turn_id"),
                        "name": row.get("name"),
                        "duration_ms": row.get("duration_ms"),
                        "error_present": row.get("error") is not None,
                        "created_at": row.get("created_at"),
                    },
                    "attributes": _base_attributes(
                        identity,
                        registry_entry,
                        span_kind="TOOL",
                        operation_name="tool_call",
                    ),
                    "request": _digest_slot(row.get("arguments")),
                    "response": _digest_slot(
                        {
                            "result": row.get("result"),
                            "error": row.get("error"),
                        }
                    ),
                },
            }
        )
    return events


def _policy_events(
    rows: list[dict[str, Any]], identity: dict[str, Any], registry_entry: dict[str, Any] | None
) -> list[dict[str, Any]]:
    events = []
    for row in rows:
        events.append(
            {
                "sort_key": ("policy_decisions", str(row.get("id"))),
                "timestamp": _event_timestamp(row, "created_at"),
                "event_type": "event.policy",
                "payload": {
                    "source": "automaton",
                    "source_table": "policy_decisions",
                    "record_id": row.get("id"),
                    "body": {
                        "turn_id": row.get("turn_id"),
                        "tool_name": row.get("tool_name"),
                        "risk_level": row.get("risk_level"),
                        "decision": row.get("decision"),
                        "latency_ms": row.get("latency_ms"),
                        "created_at": row.get("created_at"),
                    },
                    "attributes": _base_attributes(
                        identity,
                        registry_entry,
                        span_kind="CHAIN",
                        operation_name="policy_decision",
                    ),
                    "request": _digest_slot(
                        {
                            "tool_args_hash": row.get("tool_args_hash"),
                            "rules_evaluated": _safe_json(row.get("rules_evaluated")),
                            "rules_triggered": _safe_json(row.get("rules_triggered")),
                        }
                    ),
                    "response": _digest_slot(row.get("reason")),
                },
            }
        )
    return events


def _modification_events(
    rows: list[dict[str, Any]], identity: dict[str, Any], registry_entry: dict[str, Any] | None
) -> list[dict[str, Any]]:
    events = []
    for row in rows:
        events.append(
            {
                "sort_key": ("modifications", str(row.get("id"))),
                "timestamp": _event_timestamp(row, "timestamp", "created_at"),
                "event_type": "code.modification",
                "payload": {
                    "source": "automaton",
                    "source_table": "modifications",
                    "record_id": row.get("id"),
                    "body": {
                        "type": row.get("type"),
                        "description": row.get("description"),
                        "file_path": row.get("file_path"),
                        "reversible": bool(row.get("reversible")),
                        "created_at": row.get("created_at"),
                    },
                    "attributes": _base_attributes(
                        identity,
                        registry_entry,
                        span_kind="AGENT",
                        operation_name="self_modification",
                    ),
                    "request": _digest_slot(row.get("diff")),
                    "response": {"mode": "absent"},
                },
            }
        )
    return events


def _transaction_events(
    rows: list[dict[str, Any]], identity: dict[str, Any], registry_entry: dict[str, Any] | None
) -> list[dict[str, Any]]:
    events = []
    for row in rows:
        events.append(
            {
                "sort_key": ("transactions", str(row.get("id"))),
                "timestamp": _event_timestamp(row, "created_at"),
                "event_type": "transaction.reference",
                "payload": {
                    "source": "automaton",
                    "source_table": "transactions",
                    "record_id": row.get("id"),
                    "body": {
                        "type": row.get("type"),
                        "amount_cents": row.get("amount_cents"),
                        "balance_after_cents": row.get("balance_after_cents"),
                        "created_at": row.get("created_at"),
                    },
                    "attributes": _base_attributes(
                        identity,
                        registry_entry,
                        span_kind="CHAIN",
                        operation_name="transaction",
                    ),
                    "request": _digest_slot(row.get("description")),
                    "response": {"mode": "absent"},
                },
            }
        )
    return events


def _onchain_events(
    rows: list[dict[str, Any]], identity: dict[str, Any], registry_entry: dict[str, Any] | None
) -> list[dict[str, Any]]:
    events = []
    for row in rows:
        events.append(
            {
                "sort_key": ("onchain_transactions", str(row.get("id") or row.get("tx_hash"))),
                "timestamp": _event_timestamp(row, "created_at"),
                "event_type": "transaction.onchain",
                "payload": {
                    "source": "automaton",
                    "source_table": "onchain_transactions",
                    "record_id": row.get("id") or row.get("tx_hash"),
                    "body": {
                        "tx_hash": row.get("tx_hash"),
                        "chain": row.get("chain"),
                        "operation": row.get("operation"),
                        "status": row.get("status"),
                        "gas_used": row.get("gas_used"),
                        "created_at": row.get("created_at"),
                    },
                    "attributes": _base_attributes(
                        identity,
                        registry_entry,
                        span_kind="CHAIN",
                        operation_name="onchain_transaction",
                    ),
                    "request": _digest_slot(row.get("metadata")),
                    "response": {"mode": "absent"},
                },
            }
        )
    return events


def _git_commit_events(
    repo_root: str | Path | None,
    identity: dict[str, Any],
    registry_entry: dict[str, Any] | None,
    *,
    limit: int,
) -> list[dict[str, Any]]:
    if repo_root is None:
        return []

    target = Path(repo_root).expanduser().resolve()
    if not (target / ".git").exists():
        return []

    log_result = subprocess.run(
        [
            "git",
            "-C",
            str(target),
            "log",
            "--reverse",
            f"-n{limit}",
            "--pretty=format:%H%x1f%cI%x1f%s",
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    events: list[dict[str, Any]] = []
    for line in log_result.stdout.splitlines():
        if not line.strip():
            continue
        commit_hash, committed_at, subject = line.split("\x1f", 2)
        diff_result = subprocess.run(
            ["git", "-C", str(target), "show", "--format=", "--no-ext-diff", commit_hash],
            check=True,
            capture_output=True,
            text=True,
        )
        events.append(
            {
                "sort_key": ("git", commit_hash),
                "timestamp": committed_at,
                "event_type": "code.commit",
                "payload": {
                    "source": "automaton",
                    "source_table": "git",
                    "record_id": commit_hash,
                    "body": {
                        "commit": commit_hash,
                        "subject": subject,
                        "repo_name": target.name,
                        "repo_root_digest": sha256_digest(str(target)),
                    },
                    "attributes": _base_attributes(
                        identity,
                        registry_entry,
                        span_kind="AGENT",
                        operation_name="git_commit",
                    ),
                    "request": _digest_slot(diff_result.stdout),
                    "response": {"mode": "absent"},
                },
            }
        )
    return events


def build_fdo_stub(bundle_dir: str | Path) -> Path:
    bundle_payload = load_bundle_payload(bundle_dir)
    manifest = bundle_payload["manifest"]
    fdo_stub = {
        "object_type": "fdo-ready-agent-evidence-bundle",
        "schema_version": manifest["schema_version"],
        "source_runtime": manifest.get("source_runtime"),
        "bundle_root_hash": manifest["bundle_root_hash"],
        "identity_ref": manifest.get("identity_ref"),
        "policy_ref": manifest.get("policy_ref"),
        "trace_ref": manifest.get("trace_ref"),
    }
    target = Path(bundle_dir) / "fdo-stub.json"
    target.write_text(
        json.dumps(canonicalize(fdo_stub), indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return target


def build_erc8004_validation_stub(bundle_dir: str | Path) -> Path:
    bundle_payload = load_bundle_payload(bundle_dir)
    manifest = bundle_payload["manifest"]
    fdo_stub_path = Path(bundle_dir) / "fdo-stub.json"
    response_hash = sha256_digest(json.loads(fdo_stub_path.read_text(encoding="utf-8")))
    validation_stub = {
        "schema_version": manifest["schema_version"],
        "validation_payload_type": "erc-8004-stub",
        "identity_ref": manifest.get("identity_ref"),
        "policy_ref": manifest.get("policy_ref"),
        "trace_ref": manifest.get("trace_ref"),
        "requestURI": None,
        "requestHash": None,
        "responseURI": "./fdo-stub.json",
        "responseHash": response_hash,
    }
    target = Path(bundle_dir) / "erc8004-validation-stub.json"
    target.write_text(
        json.dumps(canonicalize(validation_stub), indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return target


def export_automaton_bundle(
    *,
    state_db_path: str | Path,
    output_dir: str | Path,
    repo_root: str | Path | None = None,
    runtime_root: str | Path | None = None,
    limit: int = 50,
) -> Path:
    export_warnings: list[str] = []
    omitted_sections: list[str] = []

    with _open_readonly_database(state_db_path) as connection:
        table_names = _list_table_names(connection)
        identity, registry_entry = _load_identity_snapshot(connection)
        turn_rows = _query_rows(
            connection,
            table_name="turns",
            order_by="timestamp",
            limit=limit,
        )
        tool_rows = _query_rows(
            connection,
            table_name="tool_calls",
            order_by="created_at",
            limit=limit,
        )
        policy_rows = _query_rows(
            connection,
            table_name="policy_decisions",
            order_by="created_at",
            limit=limit,
        )
        modification_rows = _query_rows(
            connection,
            table_name="modifications",
            order_by="timestamp",
            limit=limit,
        )
        transaction_rows = _query_rows(
            connection,
            table_name="transactions",
            order_by="created_at",
            limit=limit,
        )
        onchain_rows = _query_rows(
            connection,
            table_name="onchain_transactions",
            order_by="created_at",
            limit=limit,
        )
        source_schema_fingerprint = _source_schema_fingerprint(
            connection,
            table_names=table_names,
        )

    runtime_metadata = _detect_runtime_metadata(runtime_root)
    if runtime_metadata.version is None:
        export_warnings.append("source_runtime_version unavailable")
    if runtime_metadata.commit is None:
        export_warnings.append("source_runtime_commit unavailable")
    if runtime_metadata.dirty is None:
        export_warnings.append("source_runtime_dirty unavailable")

    expected_tables = {
        "turns": turn_rows,
        "tool_calls": tool_rows,
        "policy_decisions": policy_rows,
        "modifications": modification_rows,
        "transactions": transaction_rows,
        "onchain_transactions": onchain_rows,
    }
    for table_name, rows in expected_tables.items():
        if table_name not in table_names:
            omitted_sections.append(f"missing_table:{table_name}")
        elif not rows:
            export_warnings.append(f"empty_table:{table_name}")

    if repo_root is None:
        omitted_sections.append("git_history")
    else:
        repo_path = Path(repo_root).expanduser().resolve()
        if not repo_path.exists() or not (repo_path / ".git").exists():
            omitted_sections.append("git_history")

    run_id = _stable_run_id(
        identity=identity,
        turn_rows=turn_rows,
        tool_rows=tool_rows,
        modification_rows=modification_rows,
        transaction_rows=transaction_rows,
        onchain_rows=onchain_rows,
    )
    builder = EvidenceBundleBuilder(
        run_id=run_id,
        source_runtime="automaton",
        capture_mode="readonly",
        source_runtime_version=runtime_metadata.version,
        source_runtime_commit=runtime_metadata.commit,
        source_runtime_dirty=runtime_metadata.dirty,
        source_schema_fingerprint=source_schema_fingerprint,
        compatibility_targets=AUTOMATON_COMPATIBILITY_TARGETS,
        identity_ref=_identity_ref(identity, registry_entry),
        policy_ref=_policy_ref(policy_rows),
        trace_ref=_trace_ref(run_id),
        export_warnings=export_warnings,
        omitted_sections=omitted_sections,
    )
    builder.redaction.update(
        {
            "digest_only": True,
            "automaton_readonly_export": True,
        }
    )

    events = []
    events.extend(_turn_events(turn_rows, identity, registry_entry))
    events.extend(_tool_events(tool_rows, identity, registry_entry))
    events.extend(_policy_events(policy_rows, identity, registry_entry))
    events.extend(_modification_events(modification_rows, identity, registry_entry))
    events.extend(_transaction_events(transaction_rows, identity, registry_entry))
    events.extend(_onchain_events(onchain_rows, identity, registry_entry))
    events.extend(_git_commit_events(repo_root, identity, registry_entry, limit=limit))

    if not identity:
        builder.export_warnings.append("identity table empty")
    if registry_entry is None:
        builder.export_warnings.append("registry entry unavailable")

    for event in sorted(
        events,
        key=lambda item: (
            _sort_timestamp(item["timestamp"]),
            item["sort_key"][0],
            item["sort_key"][1],
        ),
    ):
        builder.add_record(
            event_type=event["event_type"],
            timestamp=event["timestamp"],
            payload=event["payload"],
        )

    bundle_dir = builder.write_bundle(output_dir)
    build_fdo_stub(bundle_dir)
    build_erc8004_validation_stub(bundle_dir)
    return bundle_dir
