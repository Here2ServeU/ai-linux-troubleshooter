#!/usr/bin/env bash
set -euo pipefail
sudo apt update && sudo apt install -y python3 python3-pip
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
echo "Setup complete. Export your OPENAI_API_KEY and run: python3 ai_troubleshoot.py"
