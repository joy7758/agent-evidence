import json
import sqlite3
import subprocess
from pathlib import Path

from agent_evidence.aep import load_bundle_payload, verify_bundle
from agent_evidence.integrations import export_automaton_bundle
from agent_evidence.integrations.automaton import DEFAULT_POLICY_REF


def _run(cmd: list[str], cwd: Path) -> None:
    subprocess.run(cmd, cwd=cwd, check=True, capture_output=True, text=True)


def _create_git_repo(repo_root: Path) -> None:
    repo_root.mkdir(parents=True, exist_ok=True)
    _run(["git", "init"], repo_root)
    _run(["git", "config", "user.name", "Test User"], repo_root)
    _run(["git", "config", "user.email", "test@example.com"], repo_root)
    (repo_root / "package.json").write_text(
        json.dumps({"name": "automaton", "version": "0.2.1-test"}) + "\n",
        encoding="utf-8",
    )
    sample_file = repo_root / "worker.py"
    sample_file.write_text("print('v1')\n", encoding="utf-8")
    _run(["git", "add", "package.json", "worker.py"], repo_root)
    _run(["git", "commit", "-m", "genesis worker"], repo_root)
    sample_file.write_text("print('v2')\n", encoding="utf-8")
    _run(["git", "add", "worker.py"], repo_root)
    _run(["git", "commit", "-m", "self modification"], repo_root)


def _mark_repo_dirty(repo_root: Path) -> None:
    sample_file = repo_root / "worker.py"
    sample_file.write_text("print('dirty-runtime')\n", encoding="utf-8")


def _create_state_db(db_path: Path) -> None:
    connection = sqlite3.connect(db_path)
    connection.executescript(
        """
        CREATE TABLE identity (key TEXT PRIMARY KEY, value TEXT NOT NULL);
        CREATE TABLE registry (
          agent_id TEXT PRIMARY KEY,
          agent_uri TEXT NOT NULL,
          chain TEXT NOT NULL,
          contract_address TEXT NOT NULL,
          tx_hash TEXT NOT NULL,
          registered_at TEXT NOT NULL
        );
        CREATE TABLE turns (
          id TEXT PRIMARY KEY,
          timestamp TEXT NOT NULL,
          state TEXT NOT NULL,
          input TEXT,
          input_source TEXT,
          thinking TEXT NOT NULL,
          tool_calls TEXT NOT NULL,
          token_usage TEXT NOT NULL,
          cost_cents INTEGER NOT NULL,
          created_at TEXT NOT NULL
        );
        CREATE TABLE tool_calls (
          id TEXT PRIMARY KEY,
          turn_id TEXT NOT NULL,
          name TEXT NOT NULL,
          arguments TEXT NOT NULL,
          result TEXT NOT NULL,
          duration_ms INTEGER NOT NULL,
          error TEXT,
          created_at TEXT NOT NULL
        );
        CREATE TABLE policy_decisions (
          id TEXT PRIMARY KEY,
          turn_id TEXT,
          tool_name TEXT NOT NULL,
          tool_args_hash TEXT NOT NULL,
          risk_level TEXT NOT NULL,
          decision TEXT NOT NULL,
          rules_evaluated TEXT NOT NULL,
          rules_triggered TEXT NOT NULL,
          reason TEXT NOT NULL,
          latency_ms INTEGER NOT NULL,
          created_at TEXT NOT NULL
        );
        CREATE TABLE modifications (
          id TEXT PRIMARY KEY,
          timestamp TEXT NOT NULL,
          type TEXT NOT NULL,
          description TEXT NOT NULL,
          file_path TEXT,
          diff TEXT,
          reversible INTEGER NOT NULL,
          created_at TEXT NOT NULL
        );
        CREATE TABLE transactions (
          id TEXT PRIMARY KEY,
          type TEXT NOT NULL,
          amount_cents INTEGER,
          balance_after_cents INTEGER,
          description TEXT NOT NULL,
          created_at TEXT NOT NULL
        );
        CREATE TABLE onchain_transactions (
          id TEXT PRIMARY KEY,
          tx_hash TEXT NOT NULL,
          chain TEXT NOT NULL,
          operation TEXT NOT NULL,
          status TEXT NOT NULL,
          gas_used INTEGER,
          metadata TEXT,
          created_at TEXT NOT NULL
        );
        """
    )
    connection.executemany(
        "INSERT INTO identity (key, value) VALUES (?, ?)",
        [
            ("name", "Atlas"),
            ("address", "0xabc123"),
            ("creator", "0xdef456"),
            ("automatonId", "agent-001"),
            ("chainType", "evm"),
        ],
    )
    connection.execute(
        """
        INSERT INTO registry (agent_id, agent_uri, chain, contract_address, tx_hash, registered_at)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            "agent-001",
            "https://registry.example/agents/agent-001",
            "eip155:8453",
            "0xregistry",
            "0xregtx",
            "2026-03-17T00:00:00+00:00",
        ),
    )
    connection.execute(
        """
        INSERT INTO turns (
          id, timestamp, state, input, input_source, thinking,
          tool_calls, token_usage, cost_cents, created_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            "turn-1",
            "2026-03-17T00:00:01+00:00",
            "running",
            "Find a paid task",
            "scheduler",
            "I should call a search tool",
            '[{"id":"tool-1","name":"search"}]',
            '{"input_tokens":12,"output_tokens":8}',
            17,
            "2026-03-17T00:00:01+00:00",
        ),
    )
    connection.execute(
        """
        INSERT INTO tool_calls (
          id, turn_id, name, arguments, result, duration_ms, error, created_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            "tool-1",
            "turn-1",
            "search",
            '{"query":"paid task"}',
            '{"result":"found one"}',
            45,
            None,
            "2026-03-17T00:00:02+00:00",
        ),
    )
    connection.execute(
        """
        INSERT INTO policy_decisions (
          id, turn_id, tool_name, tool_args_hash, risk_level, decision,
          rules_evaluated, rules_triggered, reason, latency_ms, created_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            "policy-1",
            "turn-1",
            "search",
            "sha256:aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
            "safe",
            "allow",
            '["safe-default"]',
            "[]",
            "read-only search permitted",
            4,
            "2026-03-17T00:00:02+00:00",
        ),
    )
    connection.execute(
        """
        INSERT INTO modifications (
          id, timestamp, type, description, file_path, diff, reversible, created_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            "mod-1",
            "2026-03-17T00:00:03+00:00",
            "edit",
            "adjust worker behavior",
            "worker.py",
            "@@ -1 +1 @@\n-print('v1')\n+print('v2')\n",
            1,
            "2026-03-17T00:00:03+00:00",
        ),
    )
    connection.execute(
        """
        INSERT INTO transactions (
          id, type, amount_cents, balance_after_cents, description, created_at
        )
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            "txn-1",
            "x402_payment",
            99,
            4901,
            "paid remote service",
            "2026-03-17T00:00:04+00:00",
        ),
    )
    connection.execute(
        """
        INSERT INTO onchain_transactions (
          id, tx_hash, chain, operation, status, gas_used, metadata, created_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            "chain-1",
            "0xdeadbeef",
            "eip155:8453",
            "transfer",
            "confirmed",
            21000,
            '{"to":"0xfeed","value":"100"}',
            "2026-03-17T00:00:05+00:00",
        ),
    )
    connection.commit()
    connection.close()


def _create_minimal_state_db(db_path: Path) -> None:
    connection = sqlite3.connect(db_path)
    connection.executescript(
        """
        CREATE TABLE identity (key TEXT PRIMARY KEY, value TEXT NOT NULL);
        CREATE TABLE turns (
          id TEXT PRIMARY KEY,
          timestamp TEXT NOT NULL,
          state TEXT NOT NULL,
          input TEXT,
          input_source TEXT,
          thinking TEXT NOT NULL,
          tool_calls TEXT NOT NULL,
          token_usage TEXT NOT NULL,
          cost_cents INTEGER NOT NULL,
          created_at TEXT NOT NULL
        );
        """
    )
    connection.executemany(
        "INSERT INTO identity (key, value) VALUES (?, ?)",
        [
            ("name", "Atlas"),
            ("address", "0xabc123"),
        ],
    )
    connection.execute(
        """
        INSERT INTO turns (
          id, timestamp, state, input, input_source, thinking,
          tool_calls, token_usage, cost_cents, created_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            "turn-1",
            "2026-03-17T00:00:01+00:00",
            "running",
            "status",
            "heartbeat",
            "checking health",
            "[]",
            "{}",
            0,
            "2026-03-17T00:00:01+00:00",
        ),
    )
    connection.commit()
    connection.close()


def test_automaton_exporter_generates_bundle_and_stubs(tmp_path: Path) -> None:
    state_db = tmp_path / "state.db"
    repo_root = tmp_path / "state-repo"
    runtime_root = tmp_path / "runtime-root"
    output_dir = tmp_path / "automaton-bundle"

    _create_state_db(state_db)
    _create_git_repo(repo_root)
    _create_git_repo(runtime_root)
    _mark_repo_dirty(runtime_root)
    expected_runtime_version = subprocess.run(
        ["git", "-C", str(runtime_root), "describe", "--tags", "--always"],
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()
    expected_runtime_commit = subprocess.run(
        ["git", "-C", str(runtime_root), "rev-parse", "HEAD"],
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()

    bundle_dir = export_automaton_bundle(
        state_db_path=state_db,
        repo_root=repo_root,
        runtime_root=runtime_root,
        output_dir=output_dir,
        limit=20,
    )

    report = verify_bundle(bundle_dir)
    payload = load_bundle_payload(bundle_dir)
    fdo_stub = json.loads((bundle_dir / "fdo-stub.json").read_text(encoding="utf-8"))
    erc8004_stub = json.loads(
        (bundle_dir / "erc8004-validation-stub.json").read_text(encoding="utf-8")
    )

    assert report["ok"] is True
    assert payload["manifest"]["source_runtime"] == "automaton"
    assert payload["manifest"]["capture_mode"] == "readonly"
    assert payload["manifest"]["source_runtime_version"] == expected_runtime_version
    assert payload["manifest"]["source_runtime_commit"] == expected_runtime_commit
    assert payload["manifest"]["source_runtime_dirty"] is True
    assert payload["manifest"]["source_schema_fingerprint"].startswith("sha256:")
    assert payload["manifest"]["identity_ref"] == "https://registry.example/agents/agent-001"
    assert payload["manifest"]["policy_ref"].startswith("urn:aep:policy:")
    assert payload["manifest"]["trace_ref"].startswith("urn:aep:trace:")

    event_types = [record["event_type"] for record in payload["records"]]
    assert "trace.turn" in event_types
    assert "action.tool" in event_types
    assert "event.policy" in event_types
    assert "code.modification" in event_types
    assert "code.commit" in event_types
    assert "transaction.reference" in event_types
    assert "transaction.onchain" in event_types

    assert fdo_stub["identity_ref"] == payload["manifest"]["identity_ref"]
    assert fdo_stub["policy_ref"] == payload["manifest"]["policy_ref"]
    assert fdo_stub["trace_ref"] == payload["manifest"]["trace_ref"]

    assert erc8004_stub["identity_ref"] == payload["manifest"]["identity_ref"]
    assert erc8004_stub["policy_ref"] == payload["manifest"]["policy_ref"]
    assert erc8004_stub["trace_ref"] == payload["manifest"]["trace_ref"]
    assert erc8004_stub["responseURI"] == "./fdo-stub.json"


def test_automaton_exporter_degrades_without_optional_sections(tmp_path: Path) -> None:
    state_db = tmp_path / "minimal-state.db"
    output_dir = tmp_path / "minimal-bundle"

    _create_minimal_state_db(state_db)

    bundle_dir = export_automaton_bundle(
        state_db_path=state_db,
        repo_root=tmp_path / "missing-repo",
        output_dir=output_dir,
        limit=20,
    )

    report = verify_bundle(bundle_dir)
    payload = load_bundle_payload(bundle_dir)
    manifest = payload["manifest"]

    assert report["ok"] is True
    assert manifest["capture_mode"] == "readonly"
    assert manifest["source_runtime_version"] is None
    assert manifest["source_runtime_commit"] is None
    assert manifest["source_runtime_dirty"] is None
    assert manifest["source_schema_fingerprint"].startswith("sha256:")
    assert manifest["policy_ref"] == DEFAULT_POLICY_REF
    assert "source_runtime_version unavailable" in manifest["export_warnings"]
    assert "source_runtime_commit unavailable" in manifest["export_warnings"]
    assert "source_runtime_dirty unavailable" in manifest["export_warnings"]
    assert "git_history" in manifest["omitted_sections"]
    assert "missing_table:policy_decisions" in manifest["omitted_sections"]
    assert "missing_table:onchain_transactions" in manifest["omitted_sections"]


def test_automaton_exporter_runtime_root_falls_back_to_package_version(tmp_path: Path) -> None:
    state_db = tmp_path / "minimal-state.db"
    runtime_root = tmp_path / "runtime-root"
    output_dir = tmp_path / "runtime-fallback-bundle"

    _create_minimal_state_db(state_db)
    runtime_root.mkdir(parents=True, exist_ok=True)
    (runtime_root / "package.json").write_text(
        json.dumps({"name": "@conway/automaton", "version": "9.9.9-test"}) + "\n",
        encoding="utf-8",
    )

    bundle_dir = export_automaton_bundle(
        state_db_path=state_db,
        output_dir=output_dir,
        runtime_root=runtime_root,
        limit=20,
    )

    manifest = load_bundle_payload(bundle_dir)["manifest"]

    assert manifest["source_runtime_version"] == "9.9.9-test"
    assert manifest["source_runtime_commit"] is None
    assert manifest["source_runtime_dirty"] is None
    assert "source_runtime_version unavailable" not in manifest["export_warnings"]
    assert "source_runtime_commit unavailable" in manifest["export_warnings"]
    assert "source_runtime_dirty unavailable" in manifest["export_warnings"]
