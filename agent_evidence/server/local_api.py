from __future__ import annotations

import json
import logging
import os
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
MAX_REQUEST_BYTES = 1 * 1024 * 1024
ALLOWED_ROOT_ENV = "AGENT_EVIDENCE_ALLOWED_ROOT"

logger = logging.getLogger(__name__)


class RequestError(ValueError):
    def __init__(self, code: str, message: str) -> None:
        super().__init__(message)
        self.code = code
        self.message = message


class AgentEvidenceRequestHandler(BaseHTTPRequestHandler):
    server_version = "AgentEvidenceLocalAPI/0.1"

    def do_GET(self) -> None:  # noqa: N802
        try:
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
            self._write_error("not_found", "Route not found.", HTTPStatus.NOT_FOUND)
        except Exception:
            logger.exception("Unhandled local API GET request error.")
            self._internal_error()

    def do_POST(self) -> None:  # noqa: N802
        try:
            path = urlparse(self.path).path
            if path == "/v1/profiles/validate":
                self._handle_validate_profile()
                return
            if path == "/v1/bundles/verify":
                self._handle_verify_bundle()
                return
            self._write_error("not_found", "Route not found.", HTTPStatus.NOT_FOUND)
        except Exception:
            logger.exception("Unhandled local API POST request error.")
            self._internal_error()

    def do_PUT(self) -> None:  # noqa: N802
        self._method_not_allowed()

    def do_PATCH(self) -> None:  # noqa: N802
        self._method_not_allowed()

    def do_DELETE(self) -> None:  # noqa: N802
        self._method_not_allowed()

    def log_message(self, format: str, *args: object) -> None:
        return

    def _method_not_allowed(self) -> None:
        self._write_error(
            "method_not_allowed",
            "Method not allowed.",
            HTTPStatus.METHOD_NOT_ALLOWED,
        )

    def _handle_validate_profile(self) -> None:
        try:
            request = self._read_json_body()
            fail_fast = _optional_bool(request, "fail_fast", default=True)
            if "profile" in request:
                profile = request["profile"]
                if not isinstance(profile, dict):
                    self._invalid_request("profile must be a JSON object.")
                    return
                report = build_validation_report(
                    profile,
                    source="request.profile",
                    fail_fast=fail_fast,
                )
                self._write_json(report)
                return
            if "profile_path" in request:
                profile_path = _required_local_path(
                    request,
                    "profile_path",
                    expected_kind="file",
                )
                try:
                    profile = load_profile(profile_path)
                except (OSError, ValueError):
                    self._invalid_request("Unable to read or parse profile_path.")
                    return
                report = build_validation_report(
                    profile,
                    source=str(profile_path),
                    fail_fast=fail_fast,
                )
                self._write_json(report)
                return
            self._invalid_request("Request must include profile or profile_path.")
        except RequestError as exc:
            self._write_error(exc.code, exc.message, HTTPStatus.BAD_REQUEST)

    def _handle_verify_bundle(self) -> None:
        try:
            request = self._read_json_body()
            bundle_path = _required_local_path(
                request,
                "bundle_path",
                expected_kind="directory",
            )
            self._write_json(verify_bundle(bundle_path))
        except RequestError as exc:
            self._write_error(exc.code, exc.message, HTTPStatus.BAD_REQUEST)

    def _read_json_body(self) -> dict[str, Any]:
        content_length = self.headers.get("Content-Length")
        if content_length is None:
            raise RequestError("invalid_request", "Content-Length header is required.")
        try:
            length = int(content_length)
        except ValueError as exc:
            raise RequestError(
                "invalid_request",
                "Content-Length header must be an integer.",
            ) from exc
        if length < 0:
            raise RequestError("invalid_request", "Content-Length header must be non-negative.")
        if length > MAX_REQUEST_BYTES:
            self.rfile.read(MAX_REQUEST_BYTES + 1)
            raise RequestError("invalid_request", "Request body is too large.")
        try:
            payload = json.loads(self.rfile.read(length).decode("utf-8"))
        except (json.JSONDecodeError, UnicodeDecodeError) as exc:
            raise RequestError("invalid_json", "Request body must be valid JSON.") from exc
        if not isinstance(payload, dict):
            raise RequestError("invalid_request", "Request body must be a JSON object.")
        return payload

    def _invalid_request(self, message: str) -> None:
        self._write_error("invalid_request", message, HTTPStatus.BAD_REQUEST)

    def _internal_error(self) -> None:
        self._write_error(
            "internal_error",
            "Internal server error.",
            HTTPStatus.INTERNAL_SERVER_ERROR,
        )

    def _write_error(self, code: str, message: str, status: int | HTTPStatus) -> None:
        self._write_json(
            {
                "ok": False,
                "error": {
                    "code": code,
                    "message": message,
                },
            },
            status,
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
        raise RequestError("invalid_request", f"{key} must be a non-empty string.")
    return value


def _allowed_root() -> Path:
    raw_root = os.environ.get(ALLOWED_ROOT_ENV)
    if raw_root:
        return Path(raw_root).expanduser().resolve()
    return Path.cwd().resolve()


def _is_relative_to(path: Path, root: Path) -> bool:
    try:
        path.relative_to(root)
    except ValueError:
        return False
    return True


def _contains_symlink(path: Path) -> bool:
    candidates = [path, *path.parents]
    for candidate in candidates:
        try:
            if candidate.is_symlink():
                return True
        except OSError:
            return True
    return False


def _resolve_allowed_path(raw_path: str, *, expected_kind: str) -> Path:
    candidate = Path(raw_path).expanduser()
    if _contains_symlink(candidate):
        raise RequestError("invalid_request", "Path is outside the allowed local boundary.")

    try:
        resolved = candidate.resolve(strict=True)
    except OSError as exc:
        raise RequestError("invalid_request", "Path does not exist.") from exc

    allowed_root = _allowed_root()
    if not _is_relative_to(resolved, allowed_root):
        raise RequestError("invalid_request", "Path is outside the allowed local boundary.")
    if resolved.is_symlink():
        raise RequestError("invalid_request", "Path is outside the allowed local boundary.")
    if expected_kind == "file" and not resolved.is_file():
        raise RequestError("invalid_request", "Path must be a regular file.")
    if expected_kind == "directory" and not resolved.is_dir():
        raise RequestError("invalid_request", "Path must be a directory.")
    return resolved


def _required_local_path(
    payload: dict[str, Any],
    key: str,
    *,
    expected_kind: str,
) -> Path:
    return _resolve_allowed_path(_required_string(payload, key), expected_kind=expected_kind)


def _optional_bool(payload: dict[str, Any], key: str, *, default: bool) -> bool:
    value = payload.get(key, default)
    if not isinstance(value, bool):
        raise RequestError("invalid_request", f"{key} must be a boolean when provided.")
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
