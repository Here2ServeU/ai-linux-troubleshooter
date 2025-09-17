# AI Linux Troubleshooter (B2M Demo)

Use AI (OpenAI or Ollama) to analyze Linux logs and turn raw errors into clear next steps.

## What you'll learn
- Tail Linux logs (`syslog`, `journalctl`, `dmesg`) and capture real errors.
- Ask an LLM to explain: “What’s the likely cause, and what should I try next?”
- Compare cloud API (OpenAI) vs. local/offline (Ollama).

---

## 1) Quick Start (Ubuntu/Debian)

### A. OpenAI path (cloud)
```bash
# 1) System deps
sudo apt update && sudo apt install -y python3 python3-pip

# 2) Project setup
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# 3) Put your key in the environment (or copy .env.example to .env)
export OPENAI_API_KEY="sk-..."
# (Optional) export OPENAI_BASE_URL="https://api.openai.com/v1"
# (Optional) export OPENAI_MODEL="gpt-4o-mini"

# 4) Run
python3 ai_troubleshoot.py
```

### B. Ollama path (local/offline)
```bash
# 1) Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# 2) Pull a model (choose one you have resources for)
ollama pull llama3.1

# 3) Python deps
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# 4) Run local version
python3 ai_troubleshoot_ollama.py
```

> Tip: If `/var/log/syslog` doesn’t exist (e.g., Amazon Linux), the script automatically tries common alternatives.

---

## 2) Interactive one‑liner (OpenAI)
```bash
bash interactive_troubleshoot.sh
```
Type a short error like `Permission denied while accessing /etc/hosts` and get an explanation + actions.

---

## 3) Teaching flow (suggested live demo)
1. **Cause an error** (e.g., start a service with wrong unit file or create a permission issue).
2. **Show raw logs**:
   ```bash
   tail -n 30 /var/log/syslog || journalctl -xe --no-pager | tail -n 30
   dmesg | tail -n 30
   ```
3. **Run the AI script** and read the **plain‑English** diagnosis + next steps.
4. **Try the fix**, re‑run and confirm it’s resolved.
5. **Discuss extensions**: networking (ip/ss), storage (df/mount), systemd (systemctl), containers (docker/kubectl).

---

## 4) Repository layout
```
ai-linux-troubleshooter/
├─ README.md
├─ requirements.txt
├─ .env.example
├─ ai_troubleshoot.py            # OpenAI API version
├─ ai_troubleshoot_ollama.py     # Local Ollama version
├─ interactive_troubleshoot.sh   # Bash wrapper for quick Q&A
├─ sample_logs/
│  ├─ syslog.sample
│  └─ dmesg.sample
└─ scripts/
   ├─ setup_openai.sh
   ├─ setup_ollama.sh
   └─ run_demo.sh
```

---

## 5) Troubleshooting
- **No key / 401 error**: Export `OPENAI_API_KEY`. If using a proxy or Azure/OpenRouter, export `OPENAI_BASE_URL`.
- **Model not found**: Change `OPENAI_MODEL` in environment or at top of the script.
- **Ollama not running**: Start it (`ollama serve`), then `ollama pull llama3.1`.
- **No syslog**: The script falls back to `journalctl`, `/var/log/messages`, then sample logs.
- **Permissions**: Some logs require `sudo`. You can run: `sudo -E python3 ai_troubleshoot.py` (preserves env).

---

## 6) Safety & cost notes
- **Data**: Logs can contain secrets. Sanitize before sending to cloud APIs or use the local Ollama script.
- **Spend**: Cloud LLM calls cost money; keep prompts concise and use small models for demos.

---

## 7) Extend this demo
- Add specialized prompts for **network**, **disk**, **CPU/memory**, **service crashes**, **container** issues.
- Output JSON with fields like `{root_cause, commands_to_run, risk, confidence}` for piping into runbooks.
- Wrap in a TUI/web UI; save analyses to a class portfolio folder.
