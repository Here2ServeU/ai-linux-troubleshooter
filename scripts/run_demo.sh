#!/usr/bin/env bash
set -euo pipefail
echo "[1/3] Showing recent logs (best-effort)"
tail -n 20 /var/log/syslog || true
echo
echo "[2/3] Running OpenAI version (needs OPENAI_API_KEY)"
if [[ -n "${OPENAI_API_KEY:-}" ]]; then
  python3 ai_troubleshoot.py || true
else
  echo "Skip: OPENAI_API_KEY not set."
fi
echo
echo "[3/3] Running Ollama version (needs local model)"
python3 ai_troubleshoot_ollama.py || true
