# AI Recon (Hybrid: Mock + Real)

AI-assisted, **authorized** recon CLI. Works **offline by default** (mock data), and switches to **real APIs** when keys are present in `.env`.

## Features
- WHOIS lookup (real via `python-whois`, else mock)
- Shodan recon (real via Shodan API, else mock)
- AI summary + pretext (real via OpenAI, else mock)
- Live risk scoring with HIGH-risk heartbeat, color-coded table, wrapped factors
- Clean Markdown report

## Setup
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# edit .env to add keys if you have them
