from __future__ import annotations

import json
import threading
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator
from urllib.error import HTTPError
from urllib.request import Request, urlopen

from click.testing import CliRunner

from agent_evidence.aep import verify_bundle
from agent_evidence.cli.main import build_capabilities_payload, main
from agent_evidence.oap import build_validation_report, load_profile
from agent_evidence.server.local_api import DEFAULT_HOST, DEFAULT_PORT, create_server

ROOT = Path(__file__).resolve().parents[1]


@contextmanager
def running_server() -> Iterator[str]:
    server = create_server(DEFAULT_HOST, 0)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        host, port = server.server_address[:2]
        yield f"http://{host}:{port}"
    finally:
        server.shutdown()
        thread.join(timeout=5)
        server.server_close()


def get_json(url: str) -> dict:
    with urlopen(url, timeout=5) as response:
        return json.loads(response.read().decode("utf-8"))


def post_json(url: str, payload: dict) -> dict:
    request = Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urlopen(request, timeout=5) as response:
        return json.loads(response.read().decode("utf-8"))


def test_local_api_healthz() -> None:
    with running_server() as base_url:
        assert get_json(f"{base_url}/healthz") == {
            "service": "agent-evidence-local-api",
            "status": "ok",
        }


def test_local_api_capabilities_matches_cli_payload_builder() -> None:
    with running_server() as base_url:
        assert get_json(f"{base_url}/v1/capabilities") == build_capabilities_payload()


def test_cli_capabilities_json_still_parses() -> None:
    result = CliRunner().invoke(main, ["capabilities", "--json"])

    assert result.exit_code == 0, result.output
    assert json.loads(result.output) == build_capabilities_payload()


def test_serve_command_defaults_to_loopback_host() -> None:
    result = CliRunner().invoke(main, ["serve", "--help"])

    assert result.exit_code == 0, result.output
    assert DEFAULT_HOST == "127.0.0.1"
    assert DEFAULT_PORT == 8765
    assert "[default: 127.0.0.1]" in result.output
    assert "[default: 8765]" in result.output


def test_local_api_validate_profile_matches_core_behavior() -> None:
    profile = load_profile(ROOT / "examples/minimal-valid-evidence.json")
    expected = build_validation_report(profile, source="request.profile", fail_fast=True)

    with running_server() as base_url:
        assert post_json(f"{base_url}/v1/profiles/validate", {"profile": profile}) == expected


def test_local_api_validate_profile_path_matches_core_behavior() -> None:
    profile_path = ROOT / "examples/minimal-valid-evidence.json"
    profile = load_profile(profile_path)
    expected = build_validation_report(profile, source=str(profile_path), fail_fast=True)

    with running_server() as base_url:
        assert (
            post_json(f"{base_url}/v1/profiles/validate", {"profile_path": str(profile_path)})
            == expected
        )


def test_local_api_verify_bundle_matches_core_behavior() -> None:
    bundle_path = ROOT / "tests/fixtures/agent_evidence_profile/valid/basic-bundle"
    expected = verify_bundle(bundle_path)

    with running_server() as base_url:
        assert (
            post_json(f"{base_url}/v1/bundles/verify", {"bundle_path": str(bundle_path)})
            == expected
        )


def test_local_api_rejects_unsupported_validate_shape() -> None:
    with running_server() as base_url:
        request = Request(
            f"{base_url}/v1/profiles/validate",
            data=json.dumps({"unexpected": True}).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        try:
            urlopen(request, timeout=5)
        except HTTPError as exc:
            assert exc.code == 400
            payload = json.loads(exc.read().decode("utf-8"))
            assert payload["error"]["code"] == "bad_request"
        else:
            raise AssertionError("unsupported request shape should fail")
