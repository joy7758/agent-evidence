from __future__ import annotations

import json
from pathlib import Path

from agent_evidence.integrations import LangChainAdapter
from agent_evidence.integrations.openai_compatible import OpenAICompatibleAdapter
from agent_evidence.review_pack import ReviewPackAssembler

try:
    from langchain_core.runnables import RunnableLambda
    from langchain_core.tools import tool
except ModuleNotFoundError as exc:  # pragma: no cover - runtime dependency guard
    raise ModuleNotFoundError(
        "langchain-core is required for test_review_pack_assembler. Install agent-evidence "
        "with the [langchain] or [dev] extra."
    ) from exc


@tool
def multiply(x: int, y: int) -> int:
    """Multiply two integers."""

    return x * y


def _build_langchain_artifacts(tmp_path: Path):
    adapter = LangChainAdapter.for_output_dir(
        tmp_path / "langchain-run",
        digest_only=True,
        omit_request=False,
        omit_response=False,
        base_tags=["review-pack"],
    )
    handler = adapter.callback_handler()
    uppercase = RunnableLambda(lambda text: text.upper()).with_config({"run_name": "uppercase"})

    uppercase.invoke(
        "hello world",
        config={
            "callbacks": [handler],
            "metadata": {"scenario": "review-pack"},
            "tags": ["review-pack"],
        },
    )
    multiply.invoke(
        {"x": 6, "y": 7},
        config={
            "callbacks": [handler],
            "metadata": {"scenario": "review-pack"},
            "tags": ["review-pack"],
        },
    )

    return adapter.finalize()


def _build_openai_compatible_artifacts(tmp_path: Path):
    adapter = OpenAICompatibleAdapter.for_output_dir(
        tmp_path / "openai-compatible-run",
        provider_label="openai",
        model="gpt-4.1-mini",
        api_key="sk-review-pack-should-not-appear",
        base_url="https://api.openai.com/v1",
        digest_only=True,
        omit_request=False,
        omit_response=False,
    )
    adapter.record_call(
        operation="responses.create",
        request={"input": "hello world", "api_key": "sk-review-pack-should-not-appear"},
        invoke=lambda: {
            "id": "resp_review_pack",
            "output": [{"type": "output_text", "text": "HELLO WORLD"}],
        },
    )
    return adapter.finalize()


def test_review_pack_assembler_packages_primary_outputs_and_excludes_private_key_by_default(
    tmp_path: Path,
) -> None:
    artifacts = _build_langchain_artifacts(tmp_path)
    assembler = ReviewPackAssembler.for_output_dir(tmp_path / "review-pack")

    pack = assembler.assemble(
        bundle_path=artifacts.bundle_path,
        receipt_path=artifacts.receipt_path,
        summary_path=artifacts.summary_path,
        supporting_files={
            "manifest": artifacts.supporting_files["manifest"],
            "public_key": artifacts.supporting_files["public_key"],
            "runtime_events": artifacts.supporting_files["runtime_events"],
            "private_key": artifacts.supporting_files["private_key"],
        },
    )

    assert pack.primary_files["bundle"].exists()
    assert pack.primary_files["receipt"].exists()
    assert pack.primary_files["summary"].exists()
    assert pack.report_path.exists()
    assert pack.index_path.exists()
    assert "private_key" not in pack.supporting_files
    assert pack.supporting_files["manifest"].exists()
    assert pack.supporting_files["public_key"].exists()
    assert pack.supporting_files["runtime_events"].exists()
    assert not (pack.pack_dir / "supporting" / "manifest-private.pem").exists()

    index_payload = json.loads(pack.index_path.read_text(encoding="utf-8"))
    receipt_payload = json.loads(pack.primary_files["receipt"].read_text(encoding="utf-8"))
    assert index_payload["primary_files"] == {
        "bundle": "primary/bundle.json",
        "receipt": "primary/receipt.json",
        "summary": "primary/summary.json",
    }
    assert index_payload["supporting_files"] == {
        "manifest": "supporting/manifest.json",
        "public_key": "supporting/manifest-public.pem",
        "runtime_events": "supporting/runtime-events.jsonl",
    }
    assert index_payload["excluded_supporting_files"] == ["private_key"]
    assert index_payload["receipt_facts"]["ok"] == receipt_payload["ok"]
    assert index_payload["receipt_facts"]["issues"] == receipt_payload["issues"]
    assert index_payload["receipt_facts"]["record_count"] == receipt_payload["record_count"]

    report_text = pack.report_path.read_text(encoding="utf-8")
    assert "# Review Report" in report_text
    assert "## Overall Status" in report_text
    assert "## Artifact Inventory" in report_text
    assert "## Verification Facts" in report_text
    assert "## Issue / Failure Summary" in report_text
    assert "## Evidence References" in report_text
    assert "## Reviewer Notes" in report_text
    assert "primary/receipt.json" in report_text


def test_review_pack_assembler_supporting_files_are_optional(tmp_path: Path) -> None:
    artifacts = _build_openai_compatible_artifacts(tmp_path)
    assembler = ReviewPackAssembler.for_output_dir(tmp_path / "review-pack")

    pack = assembler.assemble(
        bundle_path=artifacts.bundle_path,
        receipt_path=artifacts.receipt_path,
        summary_path=artifacts.summary_path,
        supporting_files={"manifest": tmp_path / "missing.manifest.json"},
    )

    assert pack.primary_files["bundle"].exists()
    assert pack.primary_files["receipt"].exists()
    assert pack.primary_files["summary"].exists()
    assert pack.supporting_files == {}
    assert not (pack.pack_dir / "supporting").exists()

    index_payload = json.loads(pack.index_path.read_text(encoding="utf-8"))
    assert index_payload["supporting_files"] == {}
    assert index_payload["missing_supporting_files"] == ["manifest"]

    report_text = pack.report_path.read_text(encoding="utf-8")
    assert "Optional support material missing" in report_text


def test_review_pack_assembler_preserves_pack_shape_across_adapter_lines(tmp_path: Path) -> None:
    langchain_artifacts = _build_langchain_artifacts(tmp_path / "langchain")
    openai_artifacts = _build_openai_compatible_artifacts(tmp_path / "openai")

    langchain_pack = ReviewPackAssembler.for_output_dir(tmp_path / "langchain-pack").assemble(
        bundle_path=langchain_artifacts.bundle_path,
        receipt_path=langchain_artifacts.receipt_path,
        summary_path=langchain_artifacts.summary_path,
        supporting_files={
            "manifest": langchain_artifacts.supporting_files["manifest"],
            "public_key": langchain_artifacts.supporting_files["public_key"],
            "runtime_events": langchain_artifacts.supporting_files["runtime_events"],
        },
    )
    openai_pack = ReviewPackAssembler.for_output_dir(tmp_path / "openai-pack").assemble(
        bundle_path=openai_artifacts.bundle_path,
        receipt_path=openai_artifacts.receipt_path,
        summary_path=openai_artifacts.summary_path,
        supporting_files={
            "manifest": openai_artifacts.supporting_files["manifest"],
            "public_key": openai_artifacts.supporting_files["public_key"],
            "runtime_events": openai_artifacts.supporting_files["runtime_events"],
        },
    )

    langchain_index = json.loads(langchain_pack.index_path.read_text(encoding="utf-8"))
    openai_index = json.loads(openai_pack.index_path.read_text(encoding="utf-8"))

    assert (
        set(langchain_pack.primary_files)
        == set(openai_pack.primary_files)
        == {
            "bundle",
            "receipt",
            "summary",
        }
    )
    assert (
        set(langchain_pack.supporting_files)
        == set(openai_pack.supporting_files)
        == {
            "manifest",
            "public_key",
            "runtime_events",
        }
    )
    assert set(langchain_index["receipt_facts"]) == set(openai_index["receipt_facts"])
    assert set(langchain_index["summary_orientation"]) == set(openai_index["summary_orientation"])
    assert set(langchain_index["primary_files"]) == set(openai_index["primary_files"])

    langchain_report = langchain_pack.report_path.read_text(encoding="utf-8")
    openai_report = openai_pack.report_path.read_text(encoding="utf-8")
    for heading in (
        "## Overall Status",
        "## Artifact Inventory",
        "## Verification Facts",
        "## Issue / Failure Summary",
        "## Evidence References",
        "## Reviewer Notes",
    ):
        assert heading in langchain_report
        assert heading in openai_report
