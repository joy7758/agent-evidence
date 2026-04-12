#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
EXTENSION_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
PROPERTIES_PATH="${RUNTIME_PROPERTIES_PATH:-${SCRIPT_DIR}/src/main/resources/agent-evidence-runtime.properties}"
LAUNCHER_PATH="${LAUNCHER_PATH:-${SCRIPT_DIR}/build/install/runtime-module-sample/bin/runtime-module-sample}"
LOG_PATH="${LOG_PATH:-${SCRIPT_DIR}/build/runtime-startup-smoke.log}"
OUTPUT_DIR="${OUTPUT_DIR:-${SCRIPT_DIR}/output}"
TIMEOUT_SECONDS="${TIMEOUT_SECONDS:-120}"
POLL_INTERVAL_SECONDS="${POLL_INTERVAL_SECONDS:-1}"
REFRESH_INSTALL_DIST="${REFRESH_INSTALL_DIST:-1}"
EFFECTIVE_WEB_PORT=""

if [[ -z "${JAVA_HOME:-}" ]] && [[ -d "/opt/homebrew/opt/openjdk@17/libexec/openjdk.jdk/Contents/Home" ]]; then
  export JAVA_HOME="/opt/homebrew/opt/openjdk@17/libexec/openjdk.jdk/Contents/Home"
  export PATH="${JAVA_HOME}/bin:/opt/homebrew/bin:${PATH}"
fi

mkdir -p "$(dirname "${LOG_PATH}")"
rm -f "${LOG_PATH}"
rm -rf "${OUTPUT_DIR}"

if [[ "${REFRESH_INSTALL_DIST}" == "1" ]] || [[ ! -x "${LAUNCHER_PATH}" ]]; then
  (
    cd "${EXTENSION_ROOT}"
    ./gradlew :runtime-module-sample:installDist >/dev/null
  )
fi

RUNTIME_PID=""

cleanup() {
  if [[ -n "${RUNTIME_PID}" ]] && kill -0 "${RUNTIME_PID}" 2>/dev/null; then
    kill "${RUNTIME_PID}" 2>/dev/null || true
    wait "${RUNTIME_PID}" 2>/dev/null || true
  fi
}

read_configured_web_port() {
  if [[ -f "${PROPERTIES_PATH}" ]]; then
    sed -n "s/^web\\.http\\.port=\\([0-9][0-9]*\\)$/\\1/p" "${PROPERTIES_PATH}" | head -n 1
  fi
}

find_free_port() {
  python3 - <<'PY'
import socket
s = socket.socket()
s.bind(("127.0.0.1", 0))
print(s.getsockname()[1])
s.close()
PY
}

emit_failure_summary() {
  local raw_port="${EFFECTIVE_WEB_PORT:-$(read_configured_web_port)}"
  local port_label="${raw_port:-configured-port}"

  if [[ -f "${LOG_PATH}" ]]; then
    if grep -Eq "Address already in use|BindException|port[^[:alnum:]]+${port_label}[^[:alnum:]]+is already in use|Port ${port_label} is already in use" "${LOG_PATH}"; then
      echo "Error: Port ${port_label} is already in use." >&2
    elif grep -q "Missing Event SPI for '" "${LOG_PATH}"; then
      local missing_spi
      missing_spi="$(sed -n "s/.*Missing Event SPI for '\\([^']*\\)'.*/\\1/p" "${LOG_PATH}" | head -n 1)"
      echo "Error: Missing Event SPI for ${missing_spi:-unknown-event-family}." >&2
    elif grep -q "Invalid exporter type '" "${LOG_PATH}"; then
      local invalid_exporter
      invalid_exporter="$(sed -n "s/.*Invalid exporter type '\\([^']*\\)'.*/\\1/p" "${LOG_PATH}" | head -n 1)"
      echo "Error: Invalid exporter type ${invalid_exporter:-unknown} specified." >&2
    else
      echo "Runtime initialization failed. See startup log for details." >&2
    fi
  else
    echo "Runtime initialization failed before startup log was written." >&2
  fi
}

trap cleanup EXIT

JAVA_OPTS_VALUE="-Dedc.fs.config=${PROPERTIES_PATH}"
if [[ "${JAVA_OPTS:-}" =~ -Dweb\.http\.port=([0-9]+) ]]; then
  EFFECTIVE_WEB_PORT="${BASH_REMATCH[1]}"
else
  EFFECTIVE_WEB_PORT="$(find_free_port)"
  JAVA_OPTS_VALUE="${JAVA_OPTS_VALUE} -Dweb.http.port=${EFFECTIVE_WEB_PORT}"
fi
if [[ -n "${JAVA_OPTS:-}" ]]; then
  JAVA_OPTS_VALUE="${JAVA_OPTS_VALUE} ${JAVA_OPTS}"
fi

(
  cd "${EXTENSION_ROOT}"
  JAVA_OPTS="${JAVA_OPTS_VALUE}" "${LAUNCHER_PATH}" >"${LOG_PATH}" 2>&1
) &
RUNTIME_PID=$!

deadline=$(( $(date +%s) + TIMEOUT_SECONDS ))

while true; do
  if [[ -f "${LOG_PATH}" ]] \
    && grep -q "Using agent-evidence exporter type 'filesystem'" "${LOG_PATH}" \
    && grep -q "Using agent-evidence output directory" "${LOG_PATH}" \
    && grep -q "Registered control-plane event subscribers for agent-evidence spike" "${LOG_PATH}" \
    && grep -Eq "Runtime .+ ready" "${LOG_PATH}"; then
    echo "Runtime startup successful"
    exit 0
  fi

  if ! kill -0 "${RUNTIME_PID}" 2>/dev/null; then
    emit_failure_summary
    if [[ -f "${LOG_PATH}" ]]; then
      cat "${LOG_PATH}" >&2
    fi
    exit 1
  fi

  if (( $(date +%s) >= deadline )); then
    echo "Runtime startup exceeded timeout of ${TIMEOUT_SECONDS} seconds" >&2
    if [[ -f "${LOG_PATH}" ]]; then
      emit_failure_summary
      cat "${LOG_PATH}" >&2
    fi
    exit 1
  fi

  sleep "${POLL_INTERVAL_SECONDS}"
done
