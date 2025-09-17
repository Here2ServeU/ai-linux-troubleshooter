#!/usr/bin/env bash
set -euo pipefail
curl -fsSL https://ollama.com/install.sh | sh
ollama pull llama3.1
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
echo "Ollama setup complete. Run: python3 ai_troubleshoot_ollama.py"
