#!/usr/bin/env bash
# Authorized internal lab only.
# Usage: ./scripts/run_full_pipeline.sh TARGET_HOST PROFILE [extra args...]
# Example (dry-run): ./scripts/run_full_pipeline.sh 192.0.2.1 quick
# Example (live):   ./scripts/run_full_pipeline.sh 192.0.2.1 web --execute
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

TARGET="${1:?usage: $0 TARGET_HOST PROFILE [args...]}"
PROFILE="${2:?usage: $0 TARGET_HOST PROFILE [args...]}"
shift 2

PY="${ROOT}/.venv/bin/python"
if [[ ! -x "$PY" ]]; then
  echo "[!] Missing ${PY}; run: python3 -m venv .venv && .venv/bin/pip install -r requirements.txt" >&2
  exit 1
fi

exec "$PY" -m hexstrike_lab pipeline \
  --target "$TARGET" \
  --profile "$PROFILE" \
  --output-base "$ROOT/output" \
  "$@"
