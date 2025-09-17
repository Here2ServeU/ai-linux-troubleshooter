#!/usr/bin/env python3
import os, subprocess, sys, textwrap
from pathlib import Path
from dotenv import load_dotenv
import ollama  # pip install ollama

load_dotenv()

MODEL = os.getenv("OLLAMA_MODEL", "llama3.1")  # adjust to whatever you've pulled

def try_read_logs():
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
        # Stream is optional; keeping it simple
        resp = ollama.chat(model=MODEL, messages=[{"role":"user","content":prompt}])
        answer = resp.get("message", {}).get("content", "").strip()
    except Exception as e:
        print("[Ollama error]", e)
        sys.exit(2)

    print("=== Logs (tail) ===")
    print(logs)
    print("\n=== AI Troubleshooting Suggestion ===")
    print(answer or "[No response from model]")

if __name__ == "__main__":
    main()
