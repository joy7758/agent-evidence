#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CONTAINER_NAME="${AGENT_EVIDENCE_PG_CONTAINER:-agent-evidence-pg-test}"
POSTGRES_PORT="${AGENT_EVIDENCE_PG_PORT:-55432}"
POSTGRES_DB="${AGENT_EVIDENCE_PG_DB:-agent_evidence_test}"
POSTGRES_USER="${AGENT_EVIDENCE_PG_USER:-postgres}"
POSTGRES_PASSWORD="${AGENT_EVIDENCE_PG_PASSWORD:-postgres}"
POSTGRES_IMAGE="${AGENT_EVIDENCE_PG_IMAGE:-postgres:16-alpine}"
TEMP_DOCKER_CONFIG=""

if [[ -z "${DOCKER_CONFIG:-}" ]] && ! command -v docker-credential-desktop >/dev/null 2>&1; then
  TEMP_DOCKER_CONFIG="$(mktemp -d)"
  cat > "${TEMP_DOCKER_CONFIG}/config.json" <<'JSON'
{"auths": {}}
JSON
  export DOCKER_CONFIG="${TEMP_DOCKER_CONFIG}"
fi

cleanup() {
  docker rm -f "${CONTAINER_NAME}" >/dev/null 2>&1 || true
  if [[ -n "${TEMP_DOCKER_CONFIG}" ]]; then
    rm -rf "${TEMP_DOCKER_CONFIG}"
  fi
}

trap cleanup EXIT

cleanup

docker run -d \
  --name "${CONTAINER_NAME}" \
  -e POSTGRES_DB="${POSTGRES_DB}" \
  -e POSTGRES_USER="${POSTGRES_USER}" \
  -e POSTGRES_PASSWORD="${POSTGRES_PASSWORD}" \
  -p "${POSTGRES_PORT}:5432" \
  "${POSTGRES_IMAGE}" >/dev/null

for _ in $(seq 1 30); do
  if docker exec "${CONTAINER_NAME}" pg_isready -U "${POSTGRES_USER}" -d "${POSTGRES_DB}" >/dev/null 2>&1; then
    break
  fi
  sleep 1
done

if ! docker exec "${CONTAINER_NAME}" pg_isready -U "${POSTGRES_USER}" -d "${POSTGRES_DB}" >/dev/null 2>&1; then
  echo "PostgreSQL container did not become ready in time." >&2
  exit 1
fi

export AGENT_EVIDENCE_POSTGRES_URL="postgresql+psycopg://${POSTGRES_USER}:${POSTGRES_PASSWORD}@127.0.0.1:${POSTGRES_PORT}/${POSTGRES_DB}"

cd "${ROOT_DIR}"
./.venv/bin/pytest tests/test_postgres_integration.py
