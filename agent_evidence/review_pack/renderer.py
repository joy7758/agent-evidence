from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping

_PRIMARY_ORDER = ("bundle", "receipt", "summary")
_SUPPORTING_ORDER = ("manifest", "public_key", "runtime_events", "private_key")
_SUMMARY_ORIENTATION_KEYS = (
    "provider_label",
    "model",
    "base_url",
    "record_count",
    "signature_count",
    "call_count",
    "verify_command",
)
_RECEIPT_FACT_KEYS = (
    "ok",
    "format",
    "profile",
    "source",
    "record_count",
    "issue_count",
    "signature_present",
    "signature_count",
    "required_signature_count",
    "signature_verified",
    "latest_chain_hash",
)
_TAXONOMY_LABELS_ZH = {
    "Verification passed": "校验通过",
    "Verification issues present": "校验未通过",
    "Chain continuity failed": "链路连续性异常",
    "Signature failure": "签名校验失败",
    "Integrity failure": "完整性校验失败",
    "Profile validation failure": "规范校验失败",
    "Optional support material missing": "缺少可选附属文件",
}
_PRIMARY_DISPLAY_NAMES = {
    "bundle": "证据包文件（bundle）",
    "receipt": "校验回执文件（receipt）",
    "summary": "摘要文件（summary）",
}
_SUPPORTING_DISPLAY_NAMES = {
    "manifest": "清单文件（manifest）",
    "public_key": "公钥文件（public key）",
    "runtime_events": "运行事件文件（runtime events）",
    "private_key": "私钥文件（private key）",
}
_SUMMARY_ORIENTATION_LABELS = {
    "provider_label": "服务提供方",
    "model": "模型",
    "base_url": "接口地址",
    "record_count": "记录数",
    "signature_count": "签名数",
    "call_count": "调用次数",
    "verify_command": "建议校验命令",
}
_RECEIPT_FACT_LABELS = {
    "ok": "回执结论",
    "format": "回执格式",
    "profile": "适用规范",
    "source": "回执来源",
    "record_count": "记录数",
    "issue_count": "问题数",
    "signature_present": "是否带签名",
    "signature_count": "签名数量",
    "required_signature_count": "必需签名数量",
    "signature_verified": "签名校验结果",
    "latest_chain_hash": "最新链哈希",
}
_MANIFEST_FACT_LABELS = {
    "export_format": "导出格式",
    "record_count": "记录数",
    "artifact_digest": "交付摘要指纹",
    "latest_chain_hash": "最新链哈希",
}


@dataclass(frozen=True)
class RenderedReviewReport:
    """Deterministic reviewer-facing report output."""

    markdown: str
    taxonomy_labels: tuple[str, ...]


def _receipt_issues(receipt: Mapping[str, Any]) -> tuple[str, ...]:
    issues = receipt.get("issues", [])
    if not isinstance(issues, list):
        return ()
    return tuple(str(issue) for issue in issues)


def _append_label(labels: list[str], label: str) -> None:
    if label not in labels:
        labels.append(label)


def _taxonomy_labels(
    receipt: Mapping[str, Any],
    *,
    missing_supporting: list[str],
) -> tuple[str, ...]:
    labels: list[str] = []
    issues = _receipt_issues(receipt)
    issue_text = "\n".join(issues).lower()

    if receipt.get("ok") is True:
        _append_label(labels, "Verification passed")
    else:
        _append_label(labels, "Verification issues present")

    if "chain" in issue_text:
        _append_label(labels, "Chain continuity failed")
    if "signature" in issue_text or receipt.get("signature_verified") is False:
        _append_label(labels, "Signature failure")
    if any(word in issue_text for word in ("integrity", "manifest", "artifact digest")):
        _append_label(labels, "Integrity failure")
    if receipt.get("profile") or "validation" in issue_text:
        _append_label(labels, "Profile validation failure")
    if missing_supporting:
        _append_label(labels, "Optional support material missing")
    return tuple(labels)


def _overall_explanation(
    receipt: Mapping[str, Any],
    *,
    missing_supporting: list[str],
) -> str:
    if receipt.get("ok") is True and not missing_supporting:
        return "校验通过，主交付物已经齐备，可直接进入审阅。"
    if receipt.get("ok") is True and missing_supporting:
        return "校验通过，但本次审阅包未包含部分可选附属文件。"
    return "校验发现需人工复核的问题，请先查看问题摘要和证据引用。"


def _path_text(value: str | Path) -> str:
    return str(value)


def _taxonomy_label_zh(label: str) -> str:
    return _TAXONOMY_LABELS_ZH.get(label, label)


def _yes_no(value: bool) -> str:
    return "是" if value else "否"


def _field_display_name(field: str) -> str:
    return _PRIMARY_DISPLAY_NAMES.get(
        field,
        _SUPPORTING_DISPLAY_NAMES.get(field, f"附属文件（{field}）"),
    )


class ReviewPackRenderer:
    """Render a deterministic reviewer-facing report from current pack inputs."""

    def render(
        self,
        *,
        bundle: Mapping[str, Any],
        receipt: Mapping[str, Any],
        summary: Mapping[str, Any],
        primary_files: Mapping[str, str | Path],
        supporting_files: Mapping[str, str | Path],
        missing_supporting: list[str],
    ) -> RenderedReviewReport:
        taxonomy_labels = _taxonomy_labels(receipt, missing_supporting=missing_supporting)
        taxonomy_labels_zh = tuple(_taxonomy_label_zh(label) for label in taxonomy_labels)
        explanation = _overall_explanation(receipt, missing_supporting=missing_supporting)
        verdict = "校验通过" if receipt.get("ok") else "校验未通过"

        lines = [
            "# 审阅报告",
            "",
            "## 总体状态",
            f"- 结果：`{verdict}`",
            f"- 回执结论（receipt.ok）：`{receipt.get('ok')}`",
            f"- 是否需人工复核：`{_yes_no(receipt.get('ok') is not True)}`",
            (
                f"- 重点标签：{', '.join(f'`{label}`' for label in taxonomy_labels_zh)}"
                if taxonomy_labels_zh
                else "- 重点标签：`无`"
            ),
            f"- 说明：{explanation}",
            "",
            "## 交付物清单",
        ]
        lines.extend(
            self._artifact_inventory_lines(
                summary,
                primary_files,
                supporting_files,
                missing_supporting,
            )
        )
        lines.extend(["", "## 校验结果"])
        lines.extend(self._verification_fact_lines(receipt))
        lines.extend(["", "## 问题摘要"])
        lines.extend(self._issue_summary_lines(receipt, taxonomy_labels, missing_supporting))
        lines.extend(["", "## 证据引用"])
        lines.extend(self._evidence_reference_lines(bundle, primary_files))
        lines.extend(
            [
                "",
                "## 审阅备注",
                "- 占位：请在此补充审阅备注。",
                (
                    "- 建议顺序：先查看 `primary/receipt.json`，再查看 "
                    "`primary/bundle.json`，最后查看 `primary/summary.json`。"
                ),
                "",
            ]
        )
        return RenderedReviewReport(markdown="\n".join(lines), taxonomy_labels=taxonomy_labels)

    def _artifact_inventory_lines(
        self,
        summary: Mapping[str, Any],
        primary_files: Mapping[str, str | Path],
        supporting_files: Mapping[str, str | Path],
        missing_supporting: list[str],
    ) -> list[str]:
        lines: list[str] = []
        for name in _PRIMARY_ORDER:
            if name in primary_files:
                lines.append(f"- {_field_display_name(name)}：`{_path_text(primary_files[name])}`")
        for name in _SUPPORTING_ORDER:
            if name in supporting_files:
                lines.append(
                    f"- {_field_display_name(name)}：`{_path_text(supporting_files[name])}`"
                )
        for name in sorted(name for name in supporting_files if name not in _SUPPORTING_ORDER):
            lines.append(f"- {_field_display_name(name)}：`{_path_text(supporting_files[name])}`")
        for name in sorted(missing_supporting):
            lines.append(f"- 缺少可选附属文件：`{_field_display_name(name)}`")
        for key in _SUMMARY_ORIENTATION_KEYS:
            value = summary.get(key)
            if value is not None:
                label = _SUMMARY_ORIENTATION_LABELS.get(key, key)
                lines.append(f"- {label}（summary.{key}）：`{value}`")
        if not lines:
            lines.append("- 未提供交付物清单明细。")
        return lines

    def _verification_fact_lines(self, receipt: Mapping[str, Any]) -> list[str]:
        lines: list[str] = []
        for key in _RECEIPT_FACT_KEYS:
            if key in receipt:
                label = _RECEIPT_FACT_LABELS.get(key, key)
                lines.append(f"- {label}（receipt.{key}）：`{receipt[key]}`")
        if not lines:
            lines.append("- 未提供可用的回执校验事实。")
        return lines

    def _issue_summary_lines(
        self,
        receipt: Mapping[str, Any],
        taxonomy_labels: tuple[str, ...],
        missing_supporting: list[str],
    ) -> list[str]:
        labels_zh = tuple(_taxonomy_label_zh(label) for label in taxonomy_labels)
        lines = [f"- 重点标签：{', '.join(f'`{label}`' for label in labels_zh)}"]
        issues = _receipt_issues(receipt)
        if issues:
            lines.extend(f"- 回执问题：`{issue}`" for issue in issues)
        else:
            lines.append("- 回执未报告问题。")
        for name in sorted(missing_supporting):
            lines.append(f"- 缺少可选附属文件：`{_field_display_name(name)}`")
        return lines

    def _evidence_reference_lines(
        self,
        bundle: Mapping[str, Any],
        primary_files: Mapping[str, str | Path],
    ) -> list[str]:
        manifest = bundle.get("manifest")
        if not isinstance(manifest, Mapping):
            manifest = {}
        records = bundle.get("records")
        if not isinstance(records, list):
            records = []
        signatures = bundle.get("signatures")
        if not isinstance(signatures, list):
            signatures = []

        lines: list[str] = []
        if "bundle" in primary_files:
            lines.append(f"- 证据包文件（bundle）：`{_path_text(primary_files['bundle'])}`")
        for key in ("export_format", "record_count", "artifact_digest", "latest_chain_hash"):
            if key in manifest:
                label = _MANIFEST_FACT_LABELS.get(key, key)
                lines.append(f"- {label}（bundle.manifest.{key}）：`{manifest[key]}`")
        lines.append(f"- 事件记录数（bundle.records）：`{len(records)}`")
        lines.append(f"- 签名记录数（bundle.signatures）：`{len(signatures)}`")
        for index, record in enumerate(records[:3]):
            if not isinstance(record, Mapping):
                continue
            event = record.get("event")
            if not isinstance(event, Mapping):
                continue
            event_id = event.get("event_id")
            event_type = event.get("event_type")
            if event_id is None and event_type is None:
                continue
            lines.append(
                (
                    f"- 记录 {index}（bundle.record[{index}]）："
                    f"`event_id={event_id}` `event_type={event_type}`"
                )
            )
        if len(records) > 3:
            lines.append(f"- 其余未展开记录：`{len(records) - 3}`")
        return lines
