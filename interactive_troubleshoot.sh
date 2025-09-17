#!/usr/bin/env bash
set -euo pipefail

if [[ "${1:-}" == "--help" ]]; then
  echo "Usage: ./interactive_troubleshoot.sh"
  echo "Prompts for an error message and asks the AI (OpenAI) for next steps."
  exit 0
fi

read -rp "Enter your Linux error or symptom: " ERROR

python3 - <<'PYCODE'
import os, sys
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
model = os.getenv("OPENAI_MODEL","gpt-4o-mini")
base_url = os.getenv("OPENAI_BASE_URL")

if not api_key:
    print("[Error] OPENAI_API_KEY is not set.")
    sys.exit(1)

client = OpenAI(api_key=api_key, base_url=base_url) if base_url else OpenAI(api_key=api_key)

error = """ + '"${ERROR}"' + r"""
prompt = f"""You are a Linux troubleshooting assistant. The user reports:
{error}

Explain likely cause(s) and give 3–5 concrete next steps with commands.
"""

resp = client.chat.completions.create(
    model=model,
    messages=[{"role":"user","content":prompt}],
    temperature=0.2
)

print(resp.choices[0].message.content.strip())
PYCODE
