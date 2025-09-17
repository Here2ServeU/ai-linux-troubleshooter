#!/usr/bin/env python3
import os, subprocess, sys, textwrap
from pathlib import Path
from dotenv import load_dotenv

# Load .env if present
load_dotenv()

# --- OpenAI client (official SDK v1.x) ---
from openai import OpenAI

MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
BASE_URL = os.getenv("OPENAI_BASE_URL")  # optional
API_KEY = os.getenv("OPENAI_API_KEY")

if not API_KEY:
    print("[Error] OPENAI_API_KEY is not set. Export it or fill .env.")
    sys.exit(1)

client = OpenAI(api_key=API_KEY, base_url=BASE_URL) if BASE_URL else OpenAI(api_key=API_KEY)

def try_read_logs():
    # Common log sources across distros
    candidates = [
        "tail -n 80 /var/log/syslog",
        "journalctl -xe --no-pager | tail -n 120",
        "tail -n 80 /var/log/messages",
        "dmesg | tail -n 120",
    ]
    for cmd in candidates:
        try:
            out = subprocess.check_output(cmd, shell=True, text=True, stderr=subprocess.STDOUT, timeout=5)
            if out.strip():
                return f"$ {cmd}\n{out}"
        except Exception:
            continue
    # Fallback to sample logs (for students on minimal VMs)
    sample = Path("sample_logs/syslog.sample")
    if sample.exists():
        return sample.read_text()
    return "[No logs available; create some activity or run as sudo.]"

def build_prompt(logs: str) -> str:
    return textwrap.dedent(f"""
    You are a senior Linux SRE tutor. Analyze the logs and produce:
    1) Likely root cause (one paragraph)
    2) 3–5 concrete next steps with specific commands
    3) If relevant, prevention tips (limits, alerts, config hardening)

    Logs:
    -----
    {logs}
    -----

    Be concise and practical. Use bullet points for steps.
    """).strip()

def main():
    logs = try_read_logs()
    prompt = build_prompt(logs)

    try:
        resp = client.chat.completions.create(
            model=MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
        )
        answer = resp.choices[0].message.content.strip()
    except Exception as e:
        print("[OpenAI API error]", e)
        sys.exit(2)

    print("=== Logs (tail) ===")
    print(logs)
    print("\n=== AI Troubleshooting Suggestion ===")
    print(answer)

if __name__ == "__main__":
    main()
