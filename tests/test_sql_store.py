import json
from pathlib import Path

from click.testing import CliRunner

from agent_evidence.cli.main import main
from agent_evidence.recorder import EvidenceRecorder
from agent_evidence.storage.local import LocalEvidenceStore
from agent_evidence.storage.sql import SqlEvidenceStore


def sqlite_url(path: Path) -> str:
    return f"sqlite+pysqlite:///{path}"


def test_sql_store_appends_and_queries(tmp_path: Path) -> None:
    store = SqlEvidenceStore(sqlite_url(tmp_path / "evidence.db"))
    recorder = EvidenceRecorder(store)

    first = recorder.record(
        actor="planner",
        event_type="tool.call",
        context={"source": "langchain", "component": "tool"},
        inputs={"query": "weather"},
    )
    second = recorder.record(
        actor="planner",
        event_type="tool.end",
        context={"source": "langchain", "component": "tool"},
        outputs={"status": "ok"},
    )

    records = store.list()
    assert len(records) == 2
    assert store.latest_event_hash() == second.hashes.event_hash
    assert store.latest_chain_hash() == second.hashes.chain_hash

    [tool_end] = store.query(event_type="tool.end")
    assert tool_end.event.outputs["status"] == "ok"

    filtered = store.query(actor="planner", source="langchain", component="tool")
    assert [record.event.event_type for record in filtered] == ["tool.call", "tool.end"]

    since_second = store.query(since=second.event.timestamp, limit=1)
    assert since_second[0].event.event_id == second.event.event_id
    assert records[1].hashes.previous_event_hash == first.hashes.event_hash


def test_sql_store_supports_chain_span_hash_and_pagination_queries(tmp_path: Path) -> None:
    store = SqlEvidenceStore(sqlite_url(tmp_path / "queryable.db"))
    recorder = EvidenceRecorder(store)

    root = recorder.record(
        actor="planner",
        event_type="chain.start",
        context={"source": "langchain", "component": "chain", "span_id": "root"},
    )
    tool_call = recorder.record(
        actor="planner",
        event_type="tool.call",
        context={
            "source": "langchain",
            "component": "tool",
            "span_id": "tool-1",
            "parent_span_id": "root",
        },
        inputs={"query": "weather"},
    )
    tool_end = recorder.record(
        actor="planner",
        event_type="tool.end",
        context={
            "source": "langchain",
            "component": "tool",
            "span_id": "tool-1",
            "parent_span_id": "root",
        },
        outputs={"status": "ok"},
    )
    chain_end = recorder.record(
        actor="planner",
        event_type="chain.end",
        context={"source": "langchain", "component": "chain", "span_id": "root"},
        outputs={"status": "complete"},
    )

    [linked] = store.query(previous_event_hash=root.hashes.event_hash)
    assert linked.event.event_id == tool_call.event.event_id

    span_records = store.query(span_id="tool-1")
    assert [record.event.event_type for record in span_records] == ["tool.call", "tool.end"]

    child_records = store.query(parent_span_id="root")
    assert [record.event.event_type for record in child_records] == ["tool.call", "tool.end"]

    all_records = store.list()
    event_hashes = sorted(record.hashes.event_hash for record in all_records)
    event_lower = event_hashes[1]
    event_upper = event_hashes[2]
    expected_event_range = [
        record for record in all_records if event_lower <= record.hashes.event_hash <= event_upper
    ]
    event_window = store.query(event_hash_from=event_lower, event_hash_to=event_upper)
    assert [record.event.event_id for record in event_window] == [
        record.event.event_id for record in expected_event_range
    ]

    chain_hashes = sorted(record.hashes.chain_hash for record in all_records)
    chain_lower = chain_hashes[1]
    chain_upper = chain_hashes[3]
    expected_chain_range = [
        record for record in all_records if chain_lower <= record.hashes.chain_hash <= chain_upper
    ]
    chain_window = store.query(chain_hash_from=chain_lower, chain_hash_to=chain_upper)
    assert [record.event.event_id for record in chain_window] == [
        record.event.event_id for record in expected_chain_range
    ]

    paged = store.query(offset=1, limit=2)
    assert [record.event.event_type for record in paged] == ["tool.call", "tool.end"]
    assert chain_end.hashes.previous_event_hash == tool_end.hashes.event_hash


def test_cli_migrate_and_query_sqlite(tmp_path: Path) -> None:
    source_path = tmp_path / "evidence.jsonl"
    local_store = LocalEvidenceStore(source_path)
    recorder = EvidenceRecorder(local_store)
    first = recorder.record(
        actor="planner",
        event_type="tool.call",
        context={
            "source": "cli",
            "component": "tool",
            "span_id": "tool-1",
            "parent_span_id": "root",
        },
        inputs={"prompt": "hello"},
    )
    recorder.record(
        actor="planner",
        event_type="tool.end",
        context={
            "source": "cli",
            "component": "tool",
            "span_id": "tool-1",
            "parent_span_id": "root",
        },
        outputs={"status": "ok"},
    )

    db_url = sqlite_url(tmp_path / "migrated.db")
    runner = CliRunner()

    migrated = runner.invoke(main, ["migrate", "--source", str(source_path), "--target", db_url])
    assert migrated.exit_code == 0, migrated.output
    migration_result = json.loads(migrated.output)
    assert migration_result["migrated"] == 2

    queried = runner.invoke(
        main,
        [
            "query",
            "--store",
            db_url,
            "--event-type",
            "tool.end",
            "--source",
            "cli",
            "--component",
            "tool",
            "--span-id",
            "tool-1",
            "--previous-event-hash",
            first.hashes.event_hash,
        ],
    )
    assert queried.exit_code == 0, queried.output
    query_result = json.loads(queried.output)
    assert query_result["count"] == 1
    assert query_result["offset"] == 0
    assert query_result["records"][0]["event"]["event_type"] == "tool.end"

    paged = runner.invoke(
        main,
        [
            "query",
            "--store",
            db_url,
            "--offset",
            "1",
            "--limit",
            "1",
        ],
    )
    assert paged.exit_code == 0, paged.output
    paged_result = json.loads(paged.output)
    assert paged_result["count"] == 1
    assert paged_result["returned"] == 1
    assert paged_result["offset"] == 1
    assert paged_result["records"][0]["event"]["event_type"] == "tool.end"

    verified = runner.invoke(main, ["verify", "--store", db_url])
    assert verified.exit_code == 0, verified.output
    verify_result = json.loads(verified.output)
    assert verify_result["ok"] is True
