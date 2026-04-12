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

if [[ -z "${JAVA_HOME:-}" ]] && [[ -d "/opt/homebrew/opt/openjdk@17/libexec/openjdk.jdk/Contents/Home" ]]; then
  export JAVA_HOME="/opt/homebrew/opt/openjdk@17/libexec/openjdk.jdk/Contents/Home"
  export PATH="${JAVA_HOME}/bin:/opt/homebrew/bin:${PATH}"
fi

mkdir -p "$(dirname "${LOG_PATH}")"
rm -f "${LOG_PATH}"
rm -rf "${OUTPUT_DIR}"

if [[ ! -x "${LAUNCHER_PATH}" ]]; then
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

trap cleanup EXIT

(
  cd "${EXTENSION_ROOT}"
  JAVA_OPTS_VALUE="-Dedc.fs.config=${PROPERTIES_PATH}"
  if [[ -n "${JAVA_OPTS:-}" ]]; then
    JAVA_OPTS_VALUE="${JAVA_OPTS_VALUE} ${JAVA_OPTS}"
  fi
  JAVA_OPTS="${JAVA_OPTS_VALUE}" "${LAUNCHER_PATH}" >"${LOG_PATH}" 2>&1
) &
RUNTIME_PID=$!

deadline=$(( $(date +%s) + TIMEOUT_SECONDS ))

while true; do
  if [[ -f "${LOG_PATH}" ]] \
    && grep -q "Using agent-evidence exporter type 'filesystem'" "${LOG_PATH}" \
    && grep -q "Registered control-plane event subscribers for agent-evidence spike" "${LOG_PATH}" \
    && grep -Eq "Runtime .+ ready" "${LOG_PATH}"; then
    echo "Runtime startup successful"
    exit 0
  fi

  if ! kill -0 "${RUNTIME_PID}" 2>/dev/null; then
    echo "Runtime process exited before readiness checks passed" >&2
    if [[ -f "${LOG_PATH}" ]]; then
      cat "${LOG_PATH}" >&2
    fi
    exit 1
  fi

  if (( $(date +%s) >= deadline )); then
    echo "Runtime startup exceeded timeout of ${TIMEOUT_SECONDS} seconds" >&2
    if [[ -f "${LOG_PATH}" ]]; then
      cat "${LOG_PATH}" >&2
    fi
    exit 1
  fi

  sleep "${POLL_INTERVAL_SECONDS}"
done
