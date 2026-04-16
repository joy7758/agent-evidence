from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from agent_evidence.integrations.openai_compatible import OpenAICompatibleAdapter


class FakeChatCompletionResponse:
    def __init__(self, *, id: str, model: str, content: str) -> None:
        self.id = id
        self.model = model
        self.content = content

    def model_dump(self, mode: str = "python") -> dict[str, Any]:
        return {
            "id": self.id,
            "model": self.model,
            "choices": [
                {
                    "index": 0,
                    "message": {"role": "assistant", "content": self.content},
                    "finish_reason": "stop",
                }
            ],
            "usage": {"prompt_tokens": 4, "completion_tokens": 3},
        }


class FakeChatCompletionsClient:
    def __init__(self, response: Any):
        self.calls: list[dict[str, Any]] = []
        self._response = response

    def create(self, **kwargs: Any) -> Any:
        self.calls.append(kwargs)
        return self._response


class FakeResponsesClient:
    def __init__(self, response: Any):
        self.calls: list[dict[str, Any]] = []
        self._response = response

    def create(self, **kwargs: Any) -> Any:
        self.calls.append(kwargs)
        return self._response


@dataclass(frozen=True)
class ProviderCase:
    name: str
    provider_label: str
    model: str
    base_url: str | None
    operation: str
    request: dict[str, Any]
    response: Any


def _bundle_contract_shape(bundle_payload: dict[str, Any]) -> dict[str, Any]:
    return {
        "top_level_keys": sorted(bundle_payload.keys()),
        "manifest_keys": sorted(bundle_payload["manifest"].keys()),
        "signature_keys": sorted(bundle_payload["signatures"][0].keys()),
        "record_keys": [sorted(record.keys()) for record in bundle_payload["records"]],
        "event_keys": [sorted(record["event"].keys()) for record in bundle_payload["records"]],
        "context_keys": [
            sorted(record["event"]["context"].keys()) for record in bundle_payload["records"]
        ],
        "hash_keys": [sorted(record["hashes"].keys()) for record in bundle_payload["records"]],
        "event_types": [record["event"]["event_type"] for record in bundle_payload["records"]],
    }


def _run_provider_case(
    tmp_path: Path,
    case: ProviderCase,
    *,
    api_key: str,
) -> dict[str, Any]:
    adapter = OpenAICompatibleAdapter.for_output_dir(
        tmp_path / case.name,
        provider_label=case.provider_label,
        model=case.model,
        api_key=api_key,
        base_url=case.base_url,
        digest_only=False,
        omit_request=False,
        omit_response=False,
        temperature=0.2,
        max_output_tokens=64,
    )

    if case.operation == "chat.completions.create":
        client = FakeChatCompletionsClient(case.response)

        def invoke() -> Any:
            return client.create(model=case.model, messages=case.request["messages"])

    else:
        client = FakeResponsesClient(case.response)

        def invoke() -> Any:
            return client.create(model=case.model, input=case.request["input"])

    response = adapter.record_call(
        operation=case.operation,
        request={**case.request, "api_key": api_key},
        invoke=invoke,
        metadata={"case": case.name},
        tags=["compatibility"],
    )
    artifacts = adapter.finalize()
    bundle_payload = json.loads(artifacts.bundle_path.read_text(encoding="utf-8"))
    receipt_payload = json.loads(artifacts.receipt_path.read_text(encoding="utf-8"))
    summary_payload = json.loads(artifacts.summary_path.read_text(encoding="utf-8"))
    runtime_text = artifacts.supporting_files["runtime_events"].read_text(encoding="utf-8")

    return {
        "adapter": adapter,
        "artifacts": artifacts,
        "bundle_payload": bundle_payload,
        "receipt_payload": receipt_payload,
        "summary_payload": summary_payload,
        "runtime_text": runtime_text,
        "response": response,
        "client_calls": client.calls,
    }


def test_openai_compatible_adapter_records_provider_call_and_redacts_api_key(
    tmp_path: Path,
) -> None:
    api_key = "sk-test-123"
    adapter = OpenAICompatibleAdapter.for_output_dir(
        tmp_path / "openai-compatible-run",
        provider_label="openai",
        model="gpt-4.1-mini",
        api_key=api_key,
        base_url="https://api.openai.com/v1",
        digest_only=False,
        omit_request=False,
        omit_response=False,
    )

    response = adapter.record_call(
        operation="responses.create",
        request={
            "input": "hello world",
            "api_key": api_key,
            "prompt": "sensitive prompt text",
        },
        invoke=lambda: {
            "id": "resp_123",
            "output_text": "HELLO WORLD",
            "usage": {"input_tokens": 2, "output_tokens": 2},
        },
        metadata={"request_id": "req-123"},
        tags=["smoke"],
    )

    assert response["id"] == "resp_123"

    records = adapter.store.list()
    assert [record.event.event_type for record in records] == [
        "provider.call.start",
        "provider.call.end",
    ]

    start_record, end_record = records
    assert start_record.event.context.source == "openai_compatible"
    assert start_record.event.context.component == "provider_call"
    assert start_record.event.context.source_event_type == "on_provider_call_start"
    assert start_record.event.context.name == "responses.create"
    assert "openai-compatible" in start_record.event.context.tags
    assert "openai" in start_record.event.context.tags
    assert start_record.event.metadata["provider_label"] == "openai"
    assert start_record.event.metadata["model"] == "gpt-4.1-mini"
    assert start_record.event.metadata["base_url"] == "https://api.openai.com/v1"
    assert start_record.event.inputs["mode"] == "inline"
    assert start_record.event.inputs["content"]["api_key"] == "[REDACTED]"
    assert start_record.event.inputs["content"]["prompt"] == "[REDACTED]"
    assert end_record.event.outputs["content"]["output_text"] == "HELLO WORLD"


def test_openai_compatible_adapter_preserves_artifact_contract_across_provider_switches(
    tmp_path: Path,
) -> None:
    api_key = "sk-provider-switch-should-not-appear"
    default_case = ProviderCase(
        name="default-openai",
        provider_label="openai",
        model="gpt-4.1-mini",
        base_url=None,
        operation="chat.completions.create",
        request={"messages": [{"role": "user", "content": "hello from default config"}]},
        response=FakeChatCompletionResponse(
            id="chatcmpl_default",
            model="gpt-4.1-mini",
            content="hello from default config",
        ),
    )
    alternate_case = ProviderCase(
        name="alternate-base-url",
        provider_label="lm-studio",
        model="qwen2.5-7b-instruct",
        base_url="http://localhost:1234/v1",
        operation="responses.create",
        request={"input": "hello from alternate config"},
        response={
            "id": "resp_alternate",
            "output": [{"type": "output_text", "text": "hello from alternate config"}],
            "usage": {"input_tokens": 5, "output_tokens": 4},
        },
    )

    default_result = _run_provider_case(tmp_path, default_case, api_key=api_key)
    alternate_result = _run_provider_case(tmp_path, alternate_case, api_key=api_key)

    for result, case in (
        (default_result, default_case),
        (alternate_result, alternate_case),
    ):
        artifacts = result["artifacts"]
        bundle_payload = result["bundle_payload"]
        receipt_payload = result["receipt_payload"]
        summary_payload = result["summary_payload"]
        runtime_text = result["runtime_text"]

        assert len(result["client_calls"]) == 1
        assert artifacts.bundle_path.exists()
        assert artifacts.receipt_path.exists()
        assert artifacts.summary_path.exists()
        assert artifacts.supporting_files["manifest"].exists()
        assert artifacts.supporting_files["public_key"].exists()
        assert artifacts.supporting_files["private_key"].exists()
        assert artifacts.supporting_files["runtime_events"].exists()

        assert receipt_payload["ok"] is True
        assert summary_payload["ok"] is True
        assert summary_payload["provider_label"] == case.provider_label
        assert summary_payload["model"] == case.model
        assert summary_payload["base_url"] == case.base_url
        assert summary_payload["call_count"] == 1
        assert summary_payload["receipt_path"] == str(artifacts.receipt_path)
        assert summary_payload["verify_result"] == receipt_payload

        start_record, end_record = bundle_payload["records"]
        assert start_record["event"]["event_type"] == "provider.call.start"
        assert end_record["event"]["event_type"] == "provider.call.end"
        assert start_record["event"]["metadata"]["provider_label"] == case.provider_label
        assert start_record["event"]["metadata"]["model"] == case.model
        assert (
            start_record["event"]["context"]["attributes"]["provider_label"] == case.provider_label
        )
        assert start_record["event"]["context"]["attributes"]["model"] == case.model

        if case.base_url is None:
            assert "base_url" not in start_record["event"]["metadata"]
            assert "base_url" not in start_record["event"]["context"]["attributes"]
        else:
            assert start_record["event"]["metadata"]["base_url"] == case.base_url
            assert start_record["event"]["context"]["attributes"]["base_url"] == case.base_url

        bundle_text = artifacts.bundle_path.read_text(encoding="utf-8")
        summary_text = artifacts.summary_path.read_text(encoding="utf-8")
        assert api_key not in bundle_text
        assert api_key not in summary_text
        assert api_key not in runtime_text

    default_contract = _bundle_contract_shape(default_result["bundle_payload"])
    alternate_contract = _bundle_contract_shape(alternate_result["bundle_payload"])

    assert default_contract == alternate_contract
    assert set(default_result["receipt_payload"]) == set(alternate_result["receipt_payload"])
    assert set(default_result["summary_payload"]) == set(alternate_result["summary_payload"])
    assert set(default_result["artifacts"].supporting_files) == set(
        alternate_result["artifacts"].supporting_files
    )

    default_end_record = default_result["bundle_payload"]["records"][1]
    alternate_end_record = alternate_result["bundle_payload"]["records"][1]
    assert (
        default_end_record["event"]["outputs"]["content"]["choices"][0]["message"]["content"]
        == "hello from default config"
    )
    assert alternate_end_record["event"]["outputs"]["content"]["output"][0]["text"] == (
        "hello from alternate config"
    )
