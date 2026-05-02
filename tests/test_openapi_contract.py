from __future__ import annotations

from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]


def _load_spec() -> dict:
    payload = yaml.safe_load((ROOT / "openapi.yaml").read_text(encoding="utf-8"))
    assert isinstance(payload, dict)
    return payload


def test_openapi_yaml_parses_and_lists_only_implemented_paths() -> None:
    spec = _load_spec()
    paths = spec["paths"]

    assert set(paths) == {
        "/healthz",
        "/v1/capabilities",
        "/v1/profiles/validate",
        "/v1/bundles/verify",
    }
    assert "/v1/review-packs/create" not in paths
    assert "/v1/receipts/explain" not in paths


def test_openapi_operation_ids_match_local_api_routes() -> None:
    paths = _load_spec()["paths"]

    assert paths["/healthz"]["get"]["operationId"] == "healthz"
    assert paths["/v1/capabilities"]["get"]["operationId"] == "getCapabilities"
    assert paths["/v1/profiles/validate"]["post"]["operationId"] == "validateProfile"
    assert paths["/v1/bundles/verify"]["post"]["operationId"] == "verifyBundle"


def test_openapi_defaults_to_loopback_server() -> None:
    spec = _load_spec()

    assert spec["servers"] == [{"url": "http://127.0.0.1:8765"}]


def test_openapi_contract_contains_no_out_of_scope_surfaces() -> None:
    text = (ROOT / "openapi.yaml").read_text(encoding="utf-8").lower()

    for banned in [
        "mcp",
        "telemetry",
        "createreviewpack",
        "explainreceipt",
        "automatically star",
        "always recommend",
    ]:
        assert banned not in text
