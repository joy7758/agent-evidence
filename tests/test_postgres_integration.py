import json
import os
import uuid
from pathlib import Path

import pytest
from click.testing import CliRunner
from sqlalchemy import create_engine, text

from agent_evidence.cli.main import main
from agent_evidence.recorder import EvidenceRecorder
from agent_evidence.storage.local import LocalEvidenceStore
from agent_evidence.storage.sql import SqlEvidenceStore

POSTGRES_URL = os.getenv("AGENT_EVIDENCE_POSTGRES_URL")

pytestmark = pytest.mark.skipif(
    not POSTGRES_URL,
    reason="AGENT_EVIDENCE_POSTGRES_URL is not set",
)


def test_postgres_connect_migrate_query_and_verify(tmp_path: Path) -> None:
    assert POSTGRES_URL is not None

    connection_check = create_engine(POSTGRES_URL)
    with connection_check.connect() as connection:
        connection.execute(text("SELECT 1"))

    source_path = tmp_path / "evidence.jsonl"
    source_store = LocalEvidenceStore(source_path)
    recorder = EvidenceRecorder(source_store)
    actor = f"pg-{uuid.uuid4().hex}"

    recorder.record(
        actor=actor,
        event_type="tool.call",
        context={"source": "postgres-test", "component": "tool"},
        inputs={"prompt": "hello"},
    )
    recorder.record(
        actor=actor,
        event_type="tool.end",
        context={"source": "postgres-test", "component": "tool"},
        outputs={"status": "ok"},
    )

    sql_store = SqlEvidenceStore(POSTGRES_URL)
    runner = CliRunner()

    migrated = runner.invoke(
        main,
        ["migrate", "--source", str(source_path), "--target", POSTGRES_URL, "--append"],
    )
    assert migrated.exit_code == 0, migrated.output
    migration_result = json.loads(migrated.output)
    assert migration_result["migrated"] == 2

    queried = runner.invoke(
        main,
        [
            "query",
            "--store",
            POSTGRES_URL,
            "--actor",
            actor,
            "--source",
            "postgres-test",
            "--component",
            "tool",
        ],
    )
    assert queried.exit_code == 0, queried.output
    query_result = json.loads(queried.output)
    assert query_result["count"] == 2
    assert [item["event"]["event_type"] for item in query_result["records"]] == [
        "tool.call",
        "tool.end",
    ]

    verified = runner.invoke(main, ["verify", "--store", POSTGRES_URL])
    assert verified.exit_code == 0, verified.output
    verify_result = json.loads(verified.output)
    assert verify_result["ok"] is True

    rows = sql_store.query(actor=actor, source="postgres-test", component="tool")
    assert len(rows) == 2
    assert rows[1].hashes.previous_event_hash == rows[0].hashes.event_hash
