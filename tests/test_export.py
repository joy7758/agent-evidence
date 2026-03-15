import json
from pathlib import Path

from click.testing import CliRunner
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

from agent_evidence.cli.main import main
from agent_evidence.export import (
    default_manifest_path,
    export_csv_bundle,
    export_json_bundle,
    verify_csv_export,
    verify_json_bundle,
)
from agent_evidence.recorder import EvidenceRecorder
from agent_evidence.storage.local import LocalEvidenceStore


def write_ed25519_keypair(tmp_path: Path) -> tuple[Path, Path, bytes, bytes]:
    private_key = Ed25519PrivateKey.generate()
    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    )
    public_pem = private_key.public_key().public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )
    private_path = tmp_path / "manifest-private.pem"
    public_path = tmp_path / "manifest-public.pem"
    private_path.write_bytes(private_pem)
    public_path.write_bytes(public_pem)
    return private_path, public_path, private_pem, public_pem


def build_records(tmp_path: Path):
    store = LocalEvidenceStore(tmp_path / "evidence.jsonl")
    recorder = EvidenceRecorder(store)
    recorder.record(
        actor="planner",
        event_type="tool.call",
        context={"source": "cli", "component": "tool", "span_id": "tool-1"},
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
    return store.list(), store


def test_export_json_bundle_and_verify_signature(tmp_path: Path) -> None:
    records, _ = build_records(tmp_path)
    _, _, private_pem, public_pem = write_ed25519_keypair(tmp_path)
    bundle_path = tmp_path / "bundle.json"
    manifest_path = tmp_path / "bundle.manifest.json"

    bundle = export_json_bundle(
        records,
        bundle_path,
        filters={"actor": "planner", "limit": 10},
        private_key_pem=private_pem,
        key_id="test-key",
        manifest_output_path=manifest_path,
    )

    assert bundle.signature is not None
    manifest_document = json.loads(manifest_path.read_text(encoding="utf-8"))
    assert manifest_document["signature"]["key_id"] == "test-key"

    result = verify_json_bundle(bundle_path, public_key_pem=public_pem)
    assert result["ok"] is True
    assert result["signature_present"] is True
    assert result["signature_verified"] is True


def test_export_csv_bundle_detects_tampering(tmp_path: Path) -> None:
    records, _ = build_records(tmp_path)
    _, _, private_pem, public_pem = write_ed25519_keypair(tmp_path)
    csv_path = tmp_path / "bundle.csv"
    manifest_path = default_manifest_path(csv_path)

    document = export_csv_bundle(
        records,
        csv_path,
        private_key_pem=private_pem,
        key_id="csv-key",
    )

    assert document.signature is not None
    verified = verify_csv_export(csv_path, manifest_path, public_key_pem=public_pem)
    assert verified["ok"] is True
    assert verified["signature_verified"] is True

    csv_path.write_text(
        csv_path.read_text(encoding="utf-8").replace("tool.end", "tool.fail", 1),
        encoding="utf-8",
    )
    tampered = verify_csv_export(csv_path, manifest_path, public_key_pem=public_pem)
    assert tampered["ok"] is False
    assert "artifact_digest mismatch" in tampered["issues"]


def test_cli_export_and_verify_bundle(tmp_path: Path) -> None:
    records, store = build_records(tmp_path)
    runner = CliRunner()
    private_path, public_path, _, _ = write_ed25519_keypair(tmp_path)
    bundle_path = tmp_path / "cli-bundle.json"

    exported = runner.invoke(
        main,
        [
            "export",
            "--store",
            str(store.path),
            "--format",
            "json",
            "--output",
            str(bundle_path),
            "--actor",
            "planner",
            "--private-key",
            str(private_path),
            "--key-id",
            "cli-key",
        ],
    )
    assert exported.exit_code == 0, exported.output
    export_result = json.loads(exported.output)
    assert export_result["format"] == "json"
    assert export_result["record_count"] == len(records)
    assert export_result["signed"] is True

    verified = runner.invoke(
        main,
        [
            "verify-export",
            "--bundle",
            str(bundle_path),
            "--public-key",
            str(public_path),
        ],
    )
    assert verified.exit_code == 0, verified.output
    verify_result = json.loads(verified.output)
    assert verify_result["ok"] is True
    assert verify_result["signature_verified"] is True
