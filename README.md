# AI-RECON

[![CI](https://github.com/toluowo/ai-recon/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/toluowo/ai-recon/actions/workflows/ci.yml)
[![Python](https://img.shields.io/badge/python-%3E%3D3.10-blue.svg)](https://www.python.org/)
[![Version](https://img.shields.io/badge/version-0.2.0-blue.svg)](https://github.com/toluowo/ai-recon/releases)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

> Evidence-driven reconnaissance and external exposure analysis for authorized security assessments.

AI-RECON is a modular Python security-assessment tool that collects externally observable evidence, normalizes it into security-domain models, analyzes exposure patterns, and produces structured findings with severity, confidence, evidence references, and remediation guidance.

The project demonstrates security-engineering practices across **collection, analysis, reporting, testing, packaging, and CI validation**.

**AI-RECON is intended for authorized security assessments only.**

---

## Why AI-RECON?

Security assessments often produce fragmented reconnaissance data. AI-RECON turns that data into a repeatable workflow:

```text
Collect → Normalize → Analyze → Prioritize → Report
```

The architecture separates evidence collection from analysis and reporting so that new intelligence sources, detection rules, and output formats can be added without tightly coupling the application.

## Current Capabilities

### Evidence collection

**WHOIS**
- Domain registration metadata
- Authoritative name servers
- DNS-related information

**Shodan**
- Externally observable services
- Exposed ports
- Service banners
- Available vulnerability metadata

Shodan is optional. If its API key is unavailable, the assessment continues and records the integration as unavailable.

### Exposure analysis

Current analyzers identify patterns such as:

- Potential single-provider DNS footprints
- Remotely accessible services
- Known vulnerability exposure
- Large externally exposed port footprints
- Potentially legacy service banners

Findings include:

- Severity
- Confidence
- Source
- Description
- Evidence references
- Remediation guidance

### Reporting

```text
Console → human-readable assessment
JSON    → automation / downstream security workflows
```

JSON output can be consumed by scripts, CI/CD workflows, dashboards, or future security integrations.

---

## Architecture

```text
                         Authorized Operator
                                  |
                                  v
                         +------------------+
                         |   CLI / Config   |
                         +--------+---------+
                                  |
                                  v
                         +------------------+
                         | Assessment       |
                         | Service          |
                         +--------+---------+
                                  |
                    +-------------+-------------+
                    |                           |
                    v                           v
             +-------------+             +-------------+
             | WHOIS       |             | Shodan      |
             | Collector   |             | Collector   |
             +------+------+             +------+------+
                    |                           |
                    +-------------+-------------+
                                  v
                         +------------------+
                         | Evidence Models |
                         +--------+---------+
                                  |
                                  v
                         +------------------+
                         | Analyzers        |
                         +--------+---------+
                                  |
                                  v
                         +------------------+
                         | Structured       |
                         | Findings         |
                         +--------+---------+
                                  |
                         +--------+--------+
                         |                 |
                         v                 v
                  +-------------+   +-------------+
                  | Console     |   | JSON        |
                  | Reporter    |   | Reporter    |
                  +-------------+   +-------------+
```

See [`docs/SECURITY_ARCHITECTURE.md`](docs/SECURITY_ARCHITECTURE.md) for the security boundaries, trust model, data flow, and hardening considerations.

---

## Example Assessment

Run an authorized assessment:

```bash
ai-recon \
  --target example.com \
  --authorized \
  --format console
```

Representative workflow:

```text
AI-RECON SECURITY ASSESSMENT
============================

Target: example.com
Type: domain

EVIDENCE
--------

[SUCCESS] WHOIS (live)

[UNAVAILABLE] SHODAN (live)
  Error: AI_RECON_SHODAN_API_KEY is not configured.

FINDINGS
--------

[LOW] WHOIS_SINGLE_PROVIDER_DNS

Potential single-provider DNS footprint

Source: whois
Confidence: LOW
```

The exact findings depend on the target and live evidence available at assessment time.

---

## JSON Output

```bash
ai-recon \
  --target example.com \
  --authorized \
  --format json
```

JSON is intended for:

- Automation
- CI/CD security workflows
- Dashboards
- Downstream processing
- Future security-tool integrations

The structured model preserves the relationship between collected evidence and generated findings.

---

## Installation

### Requirements

- Python 3.10+
- pip

### Clone

```bash
git clone https://github.com/toluowo/ai-recon.git
cd ai-recon
```

### Install

```bash
pip install .
```

For development:

```bash
pip install -e ".[dev]"
```

Development dependencies include:

- Pytest
- Ruff
- MyPy

---

## Shodan Configuration

Shodan is optional.

```bash
export AI_RECON_SHODAN_API_KEY="your_api_key"
```

Never commit API keys or other secrets to the repository.

---

## Development Validation

Run the same quality checks used by CI:

```bash
ruff check .
ruff format --check .
mypy src
pytest -v
```

The project also validates package creation and installation in a clean environment.

---

## CI / Engineering Quality

GitHub Actions validates the project across Python 3.10, 3.11, and 3.12.

```text
Ruff linting
      ↓
Ruff formatting validation
      ↓
MyPy strict type checking
      ↓
Pytest
      ↓
Package build
      ↓
Clean-environment installation
      ↓
Installed CLI smoke test
```

The release workflow additionally validates tagged releases before publication.

---

## Security Engineering Principles

### Explicit authorization

The CLI requires an explicit authorization acknowledgement before an assessment runs.

### Evidence before findings

Findings are derived from normalized evidence rather than generated independently. This improves traceability and reviewability.

### Separation of concerns

Collectors, domain models, analyzers, services, and reporters have separate responsibilities.

### Graceful integration failure

Unavailable credentials, network failures, API failures, and optional integrations are represented explicitly rather than silently producing misleading results.

### Secure credential handling

External credentials are supplied through configuration/environment variables and are not stored in source control.

---

## Project Structure

```text
ai-recon/
├── .github/
│   └── workflows/
│       ├── ci.yml
│       └── release.yml
├── docs/
│   └── SECURITY_ARCHITECTURE.md
├── src/
│   └── ai_recon/
│       ├── analyzers/
│       ├── collectors/
│       ├── models/
│       ├── reporters/
│       ├── services/
│       ├── application.py
│       └── cli.py
├── tests/
│   └── unit/
├── .env.example
├── CHANGELOG.md
├── LICENSE
├── pyproject.toml
├── SECURITY.md
└── README.md
```

---

## Roadmap

Potential future development includes:

- Additional reconnaissance collectors
- Expanded exposure analysis
- More finding rules
- Additional output formats such as SARIF
- Richer evidence provenance
- Risk prioritization improvements
- Security workflow integrations
- Additional CI security gates
- Broader test coverage
- Containerized deployment
- Optional evidence summarization with provenance preservation

AI-RECON is deliberately designed so these capabilities can be added without tightly coupling them to the existing assessment workflow.

---

## Responsible Use

AI-RECON is intended for:

- Authorized penetration testing
- Security assessments
- Asset exposure reviews
- Security research conducted with permission
- Testing systems you own or are explicitly authorized to assess

Do not use this tool against systems without explicit authorization.

Users are responsible for ensuring their use of AI-RECON complies with applicable laws, contracts, and organizational policies.

---

## Versioning

AI-RECON follows Semantic Versioning.

Current version:

```text
0.2.0
```

Release tags use:

```text
vMAJOR.MINOR.PATCH
```

For example:

```text
v0.2.0
v0.2.1
v0.3.0
v1.0.0
```

See [`CHANGELOG.md`](CHANGELOG.md) for release history.

---

## Contributing

Before submitting changes:

```bash
ruff check .
ruff format --check .
mypy src
pytest -v
```

All checks should pass.

---

## License

This project is licensed under the terms of the included `LICENSE` file.

## Author

**Toluwalase Owolabi**

Cybersecurity professional focused on:

- Security Operations
- Security Engineering
- Vulnerability Management
- Offensive Security
- Cloud Security
- Security Automation
- AI Security
