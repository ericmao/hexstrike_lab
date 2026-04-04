#!/usr/bin/env bash
# Run ON the deployed Kali (or any host with ~/hexstrike_lab + venv).
# Authorized lab use only.
set -euo pipefail

HL_HOME="${HEXSTRIKE_LAB_HOME:-$HOME/hexstrike_lab}"
VENV_PY="${HL_HOME}/.venv/bin/python"
OUT_BASE="${VERIFY_OUTPUT_BASE:-/tmp/hexstrike_lab_verify_out}"

echo "=== hexstrike_lab repo tests ==="
if [[ ! -x "$VENV_PY" ]]; then
  echo "ERROR: missing venv at $HL_HOME/.venv — run: cd $HL_HOME && python3 -m venv .venv && .venv/bin/pip install -r requirements.txt" >&2
  exit 1
fi
cd "$HL_HOME"
"$VENV_PY" -m pytest tests/ -q

echo "=== hexstrike_lab CLI smoke ==="
"$VENV_PY" -m hexstrike_lab --help >/dev/null
"$VENV_PY" -m hexstrike_lab pipeline --target 127.0.0.1 --profile quick --output-base "$OUT_BASE"
echo "Pipeline dry-run artifacts under $OUT_BASE"

echo "=== Ollama (Lab06) — optional ==="
if ! command -v ollama >/dev/null 2>&1; then
  echo "WARN: ollama not in PATH. Install: curl -fsSL https://ollama.com/install.sh | sh"
  if [[ "${REQUIRE_OLLAMA:-0}" == "1" ]]; then
    exit 2
  fi
else
  ollama --version || true
  if ! curl -sf --max-time 3 "http://127.0.0.1:11434/api/tags" >/dev/null 2>&1; then
    echo "WARN: Ollama API not reachable on 127.0.0.1:11434 (start daemon: ollama serve, or systemd service)."
    if [[ "${REQUIRE_OLLAMA:-0}" == "1" ]]; then
      exit 2
    fi
  else
    _ollama_smoke() {
      local sec="$1"
      python3 - <<PY
import os, re, subprocess, sys
try:
    env = os.environ.copy()
    env.setdefault("TERM", "dumb")
    env.setdefault("CI", "true")
    p = subprocess.run(
        ["ollama", "run", "llama3", "Reply with exactly: OK"],
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        text=True,
        timeout=int("${sec}"),
        env=env,
    )
    out = (p.stdout or "").strip()
    ansi = re.compile(r"\x1b\[[0-9;?]*[a-zA-Z]")
    clean = [ansi.sub("", L).strip() for L in out.splitlines() if L.strip()]
    braille = re.compile(r"^[⠀-⣿\s]+$")
    clean = [L for L in clean if not braille.fullmatch(L)]
    print(clean[-1] if clean else "(no stdout from ollama run)")
except FileNotFoundError:
    print("ERROR: ollama binary not found", file=sys.stderr)
    sys.exit(1)
except subprocess.TimeoutExpired:
    print("WARN: ollama run timed out after ${sec}s (model may be loading); daemon is up.")
PY
    }
    if ollama list 2>/dev/null | grep -qE 'llama3|llama3:'; then
      echo "Model llama3 present; smoke inference (90s max):"
      _ollama_smoke 90
    else
      echo "Pulling llama3 (large download; first time only)..."
      ollama pull llama3
      echo "Smoke inference (120s max):"
      _ollama_smoke 120
    fi
  fi
fi

echo "=== hexstrike-ai health (optional) ==="
if curl -sf --max-time 2 "http://127.0.0.1:8888/health" >/dev/null 2>&1; then
  echo "OK http://127.0.0.1:8888/health"
else
  echo "SKIP: hexstrike_server not on 8888 (start separately per docs/DEPLOY_KALI.md)"
fi

echo "=== All required checks passed ==="
