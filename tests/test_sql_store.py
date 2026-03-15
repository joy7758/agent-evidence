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


def test_cli_migrate_and_query_sqlite(tmp_path: Path) -> None:
    source_path = tmp_path / "evidence.jsonl"
    local_store = LocalEvidenceStore(source_path)
    recorder = EvidenceRecorder(local_store)
    recorder.record(
        actor="planner",
        event_type="tool.call",
        context={"source": "cli", "component": "tool"},
        inputs={"prompt": "hello"},
    )
    recorder.record(
        actor="planner",
        event_type="tool.end",
        context={"source": "cli", "component": "tool"},
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
        ],
    )
    assert queried.exit_code == 0, queried.output
    query_result = json.loads(queried.output)
    assert query_result["count"] == 1
    assert query_result["records"][0]["event"]["event_type"] == "tool.end"

    verified = runner.invoke(main, ["verify", "--store", db_url])
    assert verified.exit_code == 0, verified.output
    verify_result = json.loads(verified.output)
    assert verify_result["ok"] is True
