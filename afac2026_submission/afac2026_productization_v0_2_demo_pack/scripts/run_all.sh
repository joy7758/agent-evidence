#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PACK_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
AFAC_ROOT="$(cd "${PACK_ROOT}/.." && pwd)"
V1_ROOT="${AFAC_ROOT}/afac2026_productization_v0_1"

if [[ -f "${V1_ROOT}/scripts/run_afac_trps_demo.py" ]]; then
  python3 "${V1_ROOT}/scripts/run_afac_trps_demo.py"
fi

if [[ -f "${V1_ROOT}/scripts/validate_afac_pack.py" ]]; then
  python3 "${V1_ROOT}/scripts/validate_afac_pack.py"
fi

python3 "${SCRIPT_DIR}/build_static_demo.py"
python3 "${SCRIPT_DIR}/generate_submission_pack.py"
python3 "${SCRIPT_DIR}/validate_v0_2_pack.py"
