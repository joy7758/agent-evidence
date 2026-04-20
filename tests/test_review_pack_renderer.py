from __future__ import annotations

import json
from pathlib import Path

from agent_evidence.review_pack import ReviewPackAssembler, ReviewPackRenderer


def _bundle_payload(*, record_count: int = 2) -> dict[str, object]:
    records = []
    for index in range(record_count):
        records.append(
            {
                "schema_version": "1.0",
                "event": {
                    "event_id": f"evt-{index + 1}",
                    "event_type": "provider.call" if index == 0 else "provider.result",
                    "actor": "openai",
                },
                "hashes": {
                    "event_hash": f"event-{index + 1}",
                    "previous_event_hash": None if index == 0 else f"event-{index}",
                    "chain_hash": f"chain-{index + 1}",
                },
            }
        )
    return {
        "manifest": {
            "export_format": "json",
            "record_count": record_count,
            "artifact_digest": "artifact-digest-123",
            "latest_chain_hash": f"chain-{record_count}",
        },
        "records": records,
        "signatures": [{"algorithm": "ed25519", "signed_at": "2026-04-16T00:00:00Z"}],
    }


def _summary_payload() -> dict[str, object]:
    return {
        "ok": True,
        "provider_label": "openai",
        "model": "gpt-4.1-mini",
        "base_url": "https://api.openai.com/v1",
        "record_count": 2,
        "signature_count": 1,
        "call_count": 1,
        "verify_command": (
            "agent-evidence verify-export --bundle ./bundle.json --public-key ./manifest-public.pem"
        ),
    }


def _write_json(path: Path, payload: dict[str, object]) -> Path:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return path


def test_review_pack_renderer_renders_deterministic_success_report() -> None:
    renderer = ReviewPackRenderer()
    bundle = _bundle_payload()
    receipt = {
        "ok": True,
        "issues": [],
        "record_count": 2,
        "signature_count": 1,
        "required_signature_count": 1,
        "signature_verified": True,
        "latest_chain_hash": "chain-2",
    }
    summary = _summary_payload()

    first = renderer.render(
        bundle=bundle,
        receipt=receipt,
        summary=summary,
        primary_files={
            "bundle": "primary/bundle.json",
            "receipt": "primary/receipt.json",
            "summary": "primary/summary.json",
        },
        supporting_files={"manifest": "supporting/manifest.json"},
        missing_supporting=[],
    )
    second = renderer.render(
        bundle=bundle,
        receipt=receipt,
        summary=summary,
        primary_files={
            "bundle": "primary/bundle.json",
            "receipt": "primary/receipt.json",
            "summary": "primary/summary.json",
        },
        supporting_files={"manifest": "supporting/manifest.json"},
        missing_supporting=[],
    )

    assert first.markdown == second.markdown
    assert first.taxonomy_labels == ("Verification passed",)
    assert "# 审阅报告" in first.markdown
    assert "## 总体状态" in first.markdown
    assert "## 交付物清单" in first.markdown
    assert "## 校验结果" in first.markdown
    assert "## 问题摘要" in first.markdown
    assert "## 证据引用" in first.markdown
    assert "## 审阅备注" in first.markdown
    assert "签名校验结果（receipt.signature_verified）：`True`" in first.markdown
    assert (
        "交付摘要指纹（bundle.manifest.artifact_digest）：`artifact-digest-123`" in first.markdown
    )
    assert "回执未报告问题。" in first.markdown
    assert "结果：`校验通过`" in first.markdown


def test_review_pack_renderer_keeps_taxonomy_labels_in_renderer_only(tmp_path: Path) -> None:
    bundle_path = _write_json(tmp_path / "bundle.json", _bundle_payload())
    receipt_path = _write_json(
        tmp_path / "receipt.json",
        {
            "ok": False,
            "issues": [
                "chain: record 1: chain_hash mismatch",
                "signature verification failed",
            ],
            "record_count": 2,
            "signature_verified": False,
            "latest_chain_hash": "broken-chain",
        },
    )
    summary_path = _write_json(tmp_path / "summary.json", _summary_payload())

    pack = ReviewPackAssembler.for_output_dir(tmp_path / "review-pack").assemble(
        bundle_path=bundle_path,
        receipt_path=receipt_path,
        summary_path=summary_path,
        supporting_files={"manifest": tmp_path / "missing.manifest.json"},
    )

    report_text = pack.report_path.read_text(encoding="utf-8")
    index_payload = json.loads(pack.index_path.read_text(encoding="utf-8"))

    assert "校验未通过" in report_text
    assert "链路连续性异常" in report_text
    assert "签名校验失败" in report_text
    assert "缺少可选附属文件" in report_text
    assert "chain: record 1: chain_hash mismatch" in report_text
    assert "signature verification failed" in report_text
    assert "taxonomy_labels" not in index_payload
    assert "renderer_labels" not in index_payload
    assert index_payload["receipt_facts"]["ok"] is False
    assert index_payload["receipt_facts"]["issues"] == [
        "chain: record 1: chain_hash mismatch",
        "signature verification failed",
    ]
