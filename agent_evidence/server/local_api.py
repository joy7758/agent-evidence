from __future__ import annotations

import json
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

from agent_evidence.aep import verify_bundle
from agent_evidence.cli.main import build_capabilities_payload
from agent_evidence.oap import build_validation_report, load_profile

DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 8765
SERVICE_NAME = "agent-evidence-local-api"
MAX_REQUEST_BYTES = 2 * 1024 * 1024


class AgentEvidenceRequestHandler(BaseHTTPRequestHandler):
    server_version = "AgentEvidenceLocalAPI/0.1"

    def do_GET(self) -> None:  # noqa: N802
        path = urlparse(self.path).path
        if path == "/healthz":
            self._write_json(
                {
                    "status": "ok",
                    "service": SERVICE_NAME,
                }
            )
            return
        if path == "/v1/capabilities":
            self._write_json(build_capabilities_payload())
            return
        self._write_json({"error": {"code": "not_found", "message": "Route not found."}}, 404)

    def do_POST(self) -> None:  # noqa: N802
        path = urlparse(self.path).path
        if path == "/v1/profiles/validate":
            self._handle_validate_profile()
            return
        if path == "/v1/bundles/verify":
            self._handle_verify_bundle()
            return
        self._write_json({"error": {"code": "not_found", "message": "Route not found."}}, 404)

    def do_PUT(self) -> None:  # noqa: N802
        self._method_not_allowed()

    def do_PATCH(self) -> None:  # noqa: N802
        self._method_not_allowed()

    def do_DELETE(self) -> None:  # noqa: N802
        self._method_not_allowed()

    def log_message(self, format: str, *args: object) -> None:
        return

    def _method_not_allowed(self) -> None:
        self._write_json(
            {"error": {"code": "method_not_allowed", "message": "Method not allowed."}},
            HTTPStatus.METHOD_NOT_ALLOWED,
        )

    def _handle_validate_profile(self) -> None:
        try:
            request = self._read_json_body()
            fail_fast = _optional_bool(request, "fail_fast", default=True)
            if "profile" in request:
                profile = request["profile"]
                if not isinstance(profile, dict):
                    self._bad_request("profile must be a JSON object.")
                    return
                report = build_validation_report(
                    profile,
                    source="request.profile",
                    fail_fast=fail_fast,
                )
                self._write_json(report)
                return
            if "profile_path" in request:
                profile_path = _required_string(request, "profile_path")
                profile = load_profile(Path(profile_path))
                report = build_validation_report(
                    profile,
                    source=profile_path,
                    fail_fast=fail_fast,
                )
                self._write_json(report)
                return
            self._bad_request("Request must include profile or profile_path.")
        except (OSError, ValueError) as exc:
            self._bad_request(str(exc))

    def _handle_verify_bundle(self) -> None:
        try:
            request = self._read_json_body()
            bundle_path = _required_string(request, "bundle_path")
            self._write_json(verify_bundle(Path(bundle_path)))
        except (OSError, ValueError) as exc:
            self._bad_request(str(exc))

    def _read_json_body(self) -> dict[str, Any]:
        content_length = self.headers.get("Content-Length")
        if content_length is None:
            raise ValueError("Content-Length header is required.")
        try:
            length = int(content_length)
        except ValueError as exc:
            raise ValueError("Content-Length header must be an integer.") from exc
        if length > MAX_REQUEST_BYTES:
            raise ValueError("Request body is too large.")
        try:
            payload = json.loads(self.rfile.read(length).decode("utf-8"))
        except json.JSONDecodeError as exc:
            raise ValueError(f"Invalid JSON body: {exc.msg}.") from exc
        if not isinstance(payload, dict):
            raise ValueError("Request body must be a JSON object.")
        return payload

    def _bad_request(self, message: str) -> None:
        self._write_json(
            {"error": {"code": "bad_request", "message": message}},
            HTTPStatus.BAD_REQUEST,
        )

    def _write_json(
        self, payload: dict[str, Any], status: int | HTTPStatus = HTTPStatus.OK
    ) -> None:
        body = json.dumps(payload, indent=2, sort_keys=True).encode("utf-8")
        self.send_response(int(status))
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


def _required_string(payload: dict[str, Any], key: str) -> str:
    value = payload.get(key)
    if not isinstance(value, str) or not value:
        raise ValueError(f"{key} must be a non-empty string.")
    return value


def _optional_bool(payload: dict[str, Any], key: str, *, default: bool) -> bool:
    value = payload.get(key, default)
    if not isinstance(value, bool):
        raise ValueError(f"{key} must be a boolean when provided.")
    return value


def create_server(
    host: str = DEFAULT_HOST,
    port: int = DEFAULT_PORT,
) -> ThreadingHTTPServer:
    return ThreadingHTTPServer((host, port), AgentEvidenceRequestHandler)


def serve(host: str = DEFAULT_HOST, port: int = DEFAULT_PORT) -> None:
    server = create_server(host, port)
    address, resolved_port = server.server_address[:2]
    print(f"agent-evidence local API listening on http://{address}:{resolved_port}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
