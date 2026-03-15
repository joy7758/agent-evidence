import json
import tarfile
import zipfile
from pathlib import Path

from click.testing import CliRunner
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

from agent_evidence.cli.main import main
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
from agent_evidence.manifest import SignerConfig, VerificationKey
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


def write_signer_config(
    tmp_path: Path,
    name: str,
    private_key_path: Path,
    *,
    key_id: str,
    key_version: str,
    signer: str,
    role: str,
    metadata: dict[str, str] | None = None,
) -> Path:
    config_path = tmp_path / f"{name}.signer.json"
    config_path.write_text(
        json.dumps(
            {
                "private_key": private_key_path.name,
                "key_id": key_id,
                "key_version": key_version,
                "signer": signer,
                "role": role,
                "metadata": metadata or {},
            },
            indent=2,
            sort_keys=True,
        ),
        encoding="utf-8",
    )
    return config_path


def write_keyring(tmp_path: Path, entries: list[dict[str, str]]) -> Path:
    keyring_path = tmp_path / "manifest-keyring.json"
    keyring_path.write_text(
        json.dumps({"keys": entries}, indent=2, sort_keys=True),
        encoding="utf-8",
    )
    return keyring_path


def rewrite_zip_member(path: Path, member_name: str, old: str, new: str) -> None:
    with zipfile.ZipFile(path, "r") as archive:
        members = {
            info.filename: archive.read(info.filename)
            for info in archive.infolist()
            if not info.is_dir()
        }
    members[member_name] = members[member_name].decode("utf-8").replace(old, new, 1).encode("utf-8")
    with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for name, payload in sorted(members.items()):
            archive.writestr(name, payload)


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
    assert manifest_document["signatures"][0]["key_id"] == "test-key"

    result = verify_json_bundle(bundle_path, public_key_pem=public_pem)
    assert result["ok"] is True
    assert result["signature_count"] == 1
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
    assert verified["signature_count"] == 1
    assert verified["signature_verified"] is True

    csv_path.write_text(
        csv_path.read_text(encoding="utf-8").replace("tool.end", "tool.fail", 1),
        encoding="utf-8",
    )
    tampered = verify_csv_export(csv_path, manifest_path, public_key_pem=public_pem)
    assert tampered["ok"] is False
    assert "artifact_digest mismatch" in tampered["issues"]


def test_export_xml_bundle_detects_tampering(tmp_path: Path) -> None:
    records, _ = build_records(tmp_path)
    _, _, private_pem, public_pem = write_ed25519_keypair(tmp_path)
    xml_path = tmp_path / "bundle.xml"
    manifest_path = default_manifest_path(xml_path)

    document = export_xml_bundle(
        records,
        xml_path,
        private_key_pem=private_pem,
        key_id="xml-key",
    )

    assert document.signature is not None
    verified = verify_xml_export(xml_path, manifest_path, public_key_pem=public_pem)
    assert verified["ok"] is True
    assert verified["format"] == "xml"
    assert verified["signature_count"] == 1
    assert verified["signature_verified"] is True

    xml_path.write_text(
        xml_path.read_text(encoding="utf-8").replace("tool.end", "tool.fail", 1),
        encoding="utf-8",
    )
    tampered = verify_xml_export(xml_path, manifest_path, public_key_pem=public_pem)
    assert tampered["ok"] is False
    assert "artifact_digest mismatch" in tampered["issues"]


def test_package_export_archive_zip_and_detect_tampering(tmp_path: Path) -> None:
    records, _ = build_records(tmp_path)
    _, _, private_pem, public_pem = write_ed25519_keypair(tmp_path)
    archive_path = tmp_path / "bundle-package.zip"

    packaged = package_export_archive(
        records,
        archive_path,
        export_format="xml",
        private_key_pem=private_pem,
        key_id="archive-key",
    )

    assert packaged["archive_format"] == "zip"
    assert packaged["export_format"] == "xml"
    assert packaged["signature_count"] == 1

    verified = verify_export_archive(archive_path, public_key_pem=public_pem)
    assert verified["ok"] is True
    assert verified["packaged"] is True
    assert verified["archive_format"] == "zip"
    assert verified["format"] == "xml"
    assert verified["signature_count"] == 1
    assert verified["signature_verified"] is True

    rewrite_zip_member(
        archive_path,
        "bundle-package.xml",
        "tool.end",
        "tool.fail",
    )
    tampered = verify_export_archive(archive_path, public_key_pem=public_pem)
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
    assert export_result["signature_count"] == 1

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
    assert verify_result["signature_count"] == 1
    assert verify_result["signature_verified"] is True


def test_cli_export_and_verify_archive_tgz(tmp_path: Path) -> None:
    records, store = build_records(tmp_path)
    runner = CliRunner()
    private_path, public_path, _, _ = write_ed25519_keypair(tmp_path)
    archive_path = tmp_path / "cli-package.tgz"

    exported = runner.invoke(
        main,
        [
            "export",
            "--store",
            str(store.path),
            "--format",
            "json",
            "--archive-format",
            "tar.gz",
            "--output",
            str(archive_path),
            "--actor",
            "planner",
            "--private-key",
            str(private_path),
            "--key-id",
            "archive-cli-key",
        ],
    )
    assert exported.exit_code == 0, exported.output
    export_result = json.loads(exported.output)
    assert export_result["archive_format"] == "tar.gz"
    assert export_result["format"] == "json"
    assert export_result["packaged"] is True
    assert export_result["record_count"] == len(records)
    assert export_result["signature_count"] == 1

    with tarfile.open(archive_path, "r:gz") as archive:
        member_names = sorted(member.name for member in archive.getmembers() if member.isfile())
    assert member_names == [
        "cli-package.bundle.json",
        "cli-package.bundle.json.manifest.json",
        "package-manifest.json",
    ]

    verified = runner.invoke(
        main,
        [
            "verify-export",
            "--archive",
            str(archive_path),
            "--public-key",
            str(public_path),
        ],
    )
    assert verified.exit_code == 0, verified.output
    verify_result = json.loads(verified.output)
    assert verify_result["ok"] is True
    assert verify_result["packaged"] is True
    assert verify_result["archive_format"] == "tar.gz"
    assert verify_result["format"] == "json"
    assert verify_result["signature_count"] == 1
    assert verify_result["signature_verified"] is True


def test_cli_export_and_verify_xml_artifact(tmp_path: Path) -> None:
    records, store = build_records(tmp_path)
    runner = CliRunner()
    private_path, public_path, _, _ = write_ed25519_keypair(tmp_path)
    xml_path = tmp_path / "cli-bundle.xml"
    manifest_path = default_manifest_path(xml_path)

    exported = runner.invoke(
        main,
        [
            "export",
            "--store",
            str(store.path),
            "--format",
            "xml",
            "--output",
            str(xml_path),
            "--actor",
            "planner",
            "--private-key",
            str(private_path),
            "--key-id",
            "xml-cli-key",
        ],
    )
    assert exported.exit_code == 0, exported.output
    export_result = json.loads(exported.output)
    assert export_result["format"] == "xml"
    assert export_result["manifest_output"] == str(manifest_path)
    assert export_result["record_count"] == len(records)
    assert export_result["signed"] is True
    assert export_result["signature_count"] == 1

    verified = runner.invoke(
        main,
        [
            "verify-export",
            "--xml",
            str(xml_path),
            "--manifest",
            str(manifest_path),
            "--public-key",
            str(public_path),
        ],
    )
    assert verified.exit_code == 0, verified.output
    verify_result = json.loads(verified.output)
    assert verify_result["ok"] is True
    assert verify_result["format"] == "xml"
    assert verify_result["signature_count"] == 1
    assert verify_result["signature_verified"] is True


def test_verify_json_bundle_accepts_legacy_signature_field(tmp_path: Path) -> None:
    records, _ = build_records(tmp_path)
    _, _, private_pem, public_pem = write_ed25519_keypair(tmp_path)
    bundle_path = tmp_path / "legacy-bundle.json"

    export_json_bundle(
        records,
        bundle_path,
        private_key_pem=private_pem,
        key_id="legacy",
    )
    payload = json.loads(bundle_path.read_text(encoding="utf-8"))
    payload["signature"] = payload["signatures"][0]
    payload.pop("signatures")
    bundle_path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")

    result = verify_json_bundle(bundle_path, public_key_pem=public_pem)
    assert result["ok"] is True
    assert result["signature_count"] == 1
    assert result["signature_verified"] is True


def test_cli_multisig_export_and_key_rotation_verification(tmp_path: Path) -> None:
    records, store = build_records(tmp_path)
    runner = CliRunner()

    ops_old_private, ops_old_public, _, _ = write_ed25519_keypair(tmp_path)
    ops_new_private, ops_new_public, _, _ = write_ed25519_keypair(tmp_path)
    compliance_private, compliance_public, _, _ = write_ed25519_keypair(tmp_path)

    ops_config = write_signer_config(
        tmp_path,
        "ops-current",
        ops_new_private,
        key_id="operations",
        key_version="2026-q2",
        signer="Operations Bot",
        role="approver",
        metadata={"environment": "prod"},
    )
    compliance_config = write_signer_config(
        tmp_path,
        "compliance",
        compliance_private,
        key_id="compliance",
        key_version="2026-q1",
        signer="Compliance Bot",
        role="attestor",
        metadata={"policy": "evidence-v1"},
    )
    keyring_path = write_keyring(
        tmp_path,
        [
            {
                "key_id": "operations",
                "key_version": "2026-q1",
                "public_key": ops_old_public.name,
            },
            {
                "key_id": "operations",
                "key_version": "2026-q2",
                "public_key": ops_new_public.name,
            },
            {
                "key_id": "compliance",
                "key_version": "2026-q1",
                "public_key": compliance_public.name,
            },
        ],
    )
    bundle_path = tmp_path / "multisig-bundle.json"

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
            "--required-signatures",
            "2",
            "--required-signature-role",
            "approver=1",
            "--required-signature-role",
            "attestor=1",
            "--signer-config",
            str(ops_config),
            "--signer-config",
            str(compliance_config),
        ],
    )
    assert exported.exit_code == 0, exported.output
    export_result = json.loads(exported.output)
    assert export_result["record_count"] == len(records)
    assert export_result["signature_count"] == 2
    assert export_result["required_signature_roles"] == {
        "approver": 1,
        "attestor": 1,
    }

    verified = runner.invoke(
        main,
        [
            "verify-export",
            "--bundle",
            str(bundle_path),
            "--keyring",
            str(keyring_path),
        ],
    )
    assert verified.exit_code == 0, verified.output
    verify_result = json.loads(verified.output)
    assert verify_result["ok"] is True
    assert verify_result["required_signature_count"] == 2
    assert verify_result["verified_signature_count"] == 2
    assert verify_result["required_role_signature_counts"] == {
        "approver": 1,
        "attestor": 1,
    }
    assert verify_result["verified_role_signature_counts"] == {
        "approver": 1,
        "attestor": 1,
    }
    assert verify_result["signature_count"] == 2
    assert verify_result["signature_verified"] is True
    assert sorted(
        (item["key_id"], item["key_version"], item["role"])
        for item in verify_result["signature_results"]
    ) == [
        ("compliance", "2026-q1", "attestor"),
        ("operations", "2026-q2", "approver"),
    ]


def test_verify_json_bundle_threshold_policy_and_override(tmp_path: Path) -> None:
    records, _ = build_records(tmp_path)

    _, _, ops_private_pem, ops_public_pem = write_ed25519_keypair(tmp_path)
    _, _, compliance_private_pem, _ = write_ed25519_keypair(tmp_path)
    bundle_path = tmp_path / "threshold-bundle.json"

    bundle = export_json_bundle(
        records,
        bundle_path,
        signer_configs=[
            SignerConfig(
                private_key_pem=ops_private_pem,
                key_id="operations",
                key_version="2026-q2",
                signer="Operations Bot",
                role="approver",
            ),
            SignerConfig(
                private_key_pem=compliance_private_pem,
                key_id="compliance",
                key_version="2026-q1",
                signer="Compliance Bot",
                role="attestor",
            ),
        ],
        minimum_valid_signatures=1,
    )

    assert bundle.manifest.signature_policy.minimum_valid_signatures == 1

    partial = verify_json_bundle(
        bundle_path,
        verification_keys=[
            VerificationKey(
                public_key_pem=ops_public_pem,
                key_id="operations",
                key_version="2026-q2",
            )
        ],
    )
    assert partial["ok"] is True
    assert partial["required_signature_count"] == 1
    assert partial["verified_signature_count"] == 1
    assert partial["signature_verified"] is True

    strict = verify_json_bundle(
        bundle_path,
        verification_keys=[
            VerificationKey(
                public_key_pem=ops_public_pem,
                key_id="operations",
                key_version="2026-q2",
            )
        ],
        minimum_valid_signatures=2,
    )
    assert strict["ok"] is False
    assert strict["required_signature_count"] == 2
    assert strict["verified_signature_count"] == 1
    assert strict["signature_verified"] is False
    assert strict["issues"] == [
        "signature threshold not met: verified 1 of 2 signatures; required 2"
    ]


def test_verify_json_bundle_role_threshold_policy_and_override(tmp_path: Path) -> None:
    records, _ = build_records(tmp_path)

    _, _, ops_private_pem, ops_public_pem = write_ed25519_keypair(tmp_path)
    _, _, compliance_private_pem, compliance_public_pem = write_ed25519_keypair(tmp_path)
    _, _, observer_private_pem, _ = write_ed25519_keypair(tmp_path)
    bundle_path = tmp_path / "role-threshold-bundle.json"

    bundle = export_json_bundle(
        records,
        bundle_path,
        signer_configs=[
            SignerConfig(
                private_key_pem=ops_private_pem,
                key_id="operations",
                key_version="2026-q2",
                signer="Operations Bot",
                role="approver",
            ),
            SignerConfig(
                private_key_pem=compliance_private_pem,
                key_id="compliance",
                key_version="2026-q1",
                signer="Compliance Bot",
                role="attestor",
            ),
            SignerConfig(
                private_key_pem=observer_private_pem,
                key_id="observer",
                key_version="2026-q1",
                signer="Observer Bot",
                role="observer",
            ),
        ],
        minimum_valid_signatures_by_role={"approver": 1, "attestor": 1},
    )

    assert bundle.manifest.signature_policy.minimum_valid_signatures is None
    assert bundle.manifest.signature_policy.minimum_valid_signatures_by_role == {
        "approver": 1,
        "attestor": 1,
    }

    partial = verify_json_bundle(
        bundle_path,
        verification_keys=[
            VerificationKey(
                public_key_pem=ops_public_pem,
                key_id="operations",
                key_version="2026-q2",
            ),
            VerificationKey(
                public_key_pem=compliance_public_pem,
                key_id="compliance",
                key_version="2026-q1",
            ),
        ],
    )
    assert partial["ok"] is True
    assert partial["required_signature_count"] == 2
    assert partial["verified_signature_count"] == 2
    assert partial["required_role_signature_counts"] == {
        "approver": 1,
        "attestor": 1,
    }
    assert partial["verified_role_signature_counts"] == {
        "approver": 1,
        "attestor": 1,
    }
    assert partial["signature_verified"] is True

    strict = verify_json_bundle(
        bundle_path,
        verification_keys=[
            VerificationKey(
                public_key_pem=ops_public_pem,
                key_id="operations",
                key_version="2026-q2",
            ),
            VerificationKey(
                public_key_pem=compliance_public_pem,
                key_id="compliance",
                key_version="2026-q1",
            ),
        ],
        minimum_valid_signatures_by_role={"approver": 1, "attestor": 1, "observer": 1},
    )
    assert strict["ok"] is False
    assert strict["required_signature_count"] == 3
    assert strict["verified_signature_count"] == 2
    assert strict["required_role_signature_counts"] == {
        "approver": 1,
        "attestor": 1,
        "observer": 1,
    }
    assert strict["verified_role_signature_counts"] == {
        "approver": 1,
        "attestor": 1,
    }
    assert strict["signature_verified"] is False
    assert strict["issues"] == [
        "signature threshold not met: verified 2 of 3 signatures; required 3",
        "role signature threshold not met: role observer verified 0 of 1 signatures; required 1",
    ]
