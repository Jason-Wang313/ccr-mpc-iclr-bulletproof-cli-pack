#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

if [[ "${1:-}" == "--no-smoke" ]]; then
  python3 "${SCRIPT_DIR}/verify_pack.py" --root "${ROOT}"
else
  python3 "${SCRIPT_DIR}/verify_pack.py" --root "${ROOT}" --smoke
fi
