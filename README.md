# AI Recon (Hybrid: Mock + Real)

![CI](https://github.com/toluowo/ai-recon/actions/workflows/ci.yml/badge.svg)

AI-assisted, **offline-first** recon CLI that flips to real APIs when keys exist.

AI‑assisted, **authorized** recon CLI that works **offline by default** and switches to **real APIs** if keys exist in `.env`.

## Features
- WHOIS lookup (real via `python-whois`, else mock)
- Shodan recon (real via Shodan API, else mock)
- AI summary + pretext (real via OpenAI, else mock)
- Live risk scoring with color‑coded table and heartbeat when HIGH
- Markdown report output

## Quickstart
```bash
git clone https://github.com/toluowo/ai-recon.git
cd ai-recon
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # fill OPENAI_API_KEY and/or SHODAN_API_KEY
```

## Usage
```bash
python recon_ai.py --domain example.com --summary --score --pretext --company "Example Inc." --output reports/example.com_report.md
```

### Flags
- `--domain` (required): target domain
- `--company` (optional): name used in pretext shaping
- `--summary`: include AI/mock summary
- `--pretext`: include safe pretext outline (training only)
- `--score`: live risk scoring
- `--output`: path to write Markdown report (default: `reports/recon_report.md`)

> Works without API keys (falls back to mock data).

## Env Vars
- `OPENAI_API_KEY`, `OPENAI_MODEL` (e.g., `gpt-4o-mini`)
- `SHODAN_API_KEY`

## Requirements
See `requirements.txt`.
