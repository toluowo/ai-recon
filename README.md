# AI-RECON

[![CI](https://github.com/toluowo/ai-recon/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/toluowo/ai-recon/actions/workflows/ci.yml)
[![Python](https://img.shields.io/badge/python-%3E%3D3.10-blue.svg)](https://www.python.org/)
[![Version](https://img.shields.io/badge/version-0.2.0-blue.svg)](https://github.com/toluowo/ai-recon/releases)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

> Extensible reconnaissance and external exposure analysis for authorized security assessments.

AI-RECON is a Python-based security assessment tool designed to collect external reconnaissance evidence, normalize the results, analyze observable exposure patterns, and present structured security findings.

The project is built around a modular architecture that separates:

* target definition
* evidence collection
* evidence analysis
* finding generation
* reporting
* application orchestration

AI-RECON is intended for **authorized security assessments only**.

---

## Features

### Evidence Collection

AI-RECON currently supports external evidence collection from:

* **WHOIS**

  * domain registration information
  * authoritative name servers
  * DNS-related metadata

* **Shodan**

  * externally observable services
  * exposed ports
  * service banners
  * available vulnerability information

Shodan integration is optional. The application continues running when a Shodan API key is not configured.

### Evidence Analysis

Collected evidence is passed through analyzers that convert observable patterns into structured security findings.

Current examples include:

* potential single-provider DNS footprint
* remotely accessible services
* known vulnerability exposure
* large externally exposed port footprints
* potentially legacy service banners

Findings include structured information such as:

* severity
* title
* source
* confidence
* description
* evidence references
* remediation guidance

### Reporting

AI-RECON supports:

* human-readable console reports
* structured JSON output

Findings are ordered by severity to make higher-priority issues easier to identify.

### Engineering Quality

The project includes:

* `src/`-based Python package structure
* automated unit tests
* strict MyPy type checking
* Ruff linting
* Ruff formatting
* GitHub Actions CI
* CLI smoke testing

---

# Architecture

The application follows a layered design:

```text
                    ┌───────────────┐
                    │      CLI      │
                    └───────┬───────┘
                            │
                            ▼
                    ┌───────────────┐
                    │  Application  │
                    │ Configuration │
                    └───────┬───────┘
                            │
                            ▼
                    ┌───────────────┐
                    │  Assessment   │
                    │    Service    │
                    └───────┬───────┘
                            │
              ┌─────────────┴─────────────┐
              ▼                           ▼
       ┌───────────────┐           ┌───────────────┐
       │  Collectors   │           │   Analyzers   │
       │               │           │               │
       │ • WHOIS       │           │ • WHOIS       │
       │ • Shodan      │           │ • Shodan      │
       └───────┬───────┘           └───────┬───────┘
               │                           │
               ▼                           ▼
       ┌───────────────┐           ┌───────────────┐
       │   Evidence    │──────────▶│   Findings    │
       └───────────────┘           └───────┬───────┘
                                           │
                                           ▼
                                   ┌───────────────┐
                                   │   Reporters   │
                                   │               │
                                   │ • Console     │
                                   │ • JSON        │
                                   └───────────────┘
```

This separation makes it easier to add new reconnaissance sources, analysis rules, and reporting formats without tightly coupling the components.

---

# Installation

## Requirements

* Python **3.10 or newer**
* `pip`

## Clone the Repository

```bash
git clone <your-repository-url>
cd ai-recon
```

## Create and Activate a Virtual Environment

### macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Windows

```powershell
python -m venv .venv
.venv\Scripts\activate
```

## Install AI-RECON

For normal usage:

```bash
pip install .
```

For development:

```bash
pip install -e ".[dev]"
```

The development installation includes:

* Pytest
* Ruff
* MyPy

---

# Usage

AI-RECON requires explicit confirmation that you are authorized to assess the target.

## Basic Assessment

```bash
ai-recon \
  --target example.com \
  --authorized \
  --format console
```

Example output:

```text
AI-RECON SECURITY ASSESSMENT
===========================

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

---

# Output Formats

## Console Output

Use:

```bash
ai-recon \
  --target example.com \
  --authorized \
  --format console
```

This produces a human-readable assessment containing:

* target information
* collected evidence
* collection errors or unavailable integrations
* findings
* evidence references
* remediation guidance

## JSON Output

Use:

```bash
ai-recon \
  --target example.com \
  --authorized \
  --format json
```

JSON output is useful for:

* automation
* CI/CD workflows
* downstream processing
* dashboards
* security workflow integrations

---

# Shodan Configuration

Shodan is an optional evidence source.

If no Shodan API key is configured, AI-RECON continues the assessment and reports Shodan as unavailable.

Configure your API key through the environment:

```bash
export AI_RECON_SHODAN_API_KEY="your_api_key"
```

Then run an assessment normally:

```bash
ai-recon \
  --target example.com \
  --authorized \
  --format console
```

> Never commit API keys or secrets to the repository.

---

# Development

## Run Tests

```bash
pytest -v
```

## Run Ruff Linting

```bash
ruff check .
```

## Automatically Fix Supported Ruff Issues

```bash
ruff check . --fix
```

## Format the Codebase

```bash
ruff format .
```

## Verify Formatting

```bash
ruff format --check .
```

## Run Type Checking

```bash
mypy src
```

## Recommended Local Validation

Before committing or pushing changes:

```bash
ruff check .
ruff format --check .
mypy src
pytest -v
```

---

# Continuous Integration

GitHub Actions runs the following checks:

```text
Ruff linting
        ↓
Ruff formatting validation
        ↓
MyPy strict type checking
        ↓
Pytest
        ↓
CLI smoke test
```

The CI workflow uses Python 3.11.

The CLI smoke test verifies that the installed application can execute an authorized assessment successfully.

---

# Project Structure

```text
ai-recon/
├── .github/
│   └── workflows/
│       └── ci.yml
│
├── src/
│   └── ai_recon/
│       ├── analyzers/
│       │   ├── shodan.py
│       │   └── whois.py
│       │
│       ├── collectors/
│       │   ├── shodan.py
│       │   └── whois.py
│       │
│       ├── models/
│       │   ├── assessment.py
│       │   ├── evidence.py
│       │   ├── finding.py
│       │   └── target.py
│       │
│       ├── reporters/
│       │   ├── console.py
│       │   └── json.py
│       │
│       ├── services/
│       │   └── assessment.py
│       │
│       ├── application.py
│       └── cli.py
│
├── tests/
│   └── unit/
│
├── .env.example
├── LICENSE
├── pyproject.toml
└── README.md
```

---

# Design Principles

AI-RECON is being developed around several engineering principles.

## Explicit Authorization

Security tooling should make authorization visible rather than implicit.

The CLI therefore requires explicit authorization before an assessment is executed.

## Separation of Concerns

Collectors are responsible for obtaining and normalizing evidence.

Analyzers are responsible for interpreting evidence and generating findings.

Reporters are responsible for presenting the assessment.

The assessment service orchestrates the workflow.

## Evidence Before Findings

Findings are derived from collected evidence rather than being generated independently.

This improves traceability and makes it easier to understand why a finding was produced.

## Graceful Integration Failure

External integrations can fail because of:

* missing credentials
* network issues
* API limits
* service availability

AI-RECON preserves these states as evidence instead of terminating the entire assessment unnecessarily.

## Extensibility

New functionality can be introduced by adding:

* a collector for a new evidence source
* an analyzer for that evidence type
* additional finding logic
* a reporter for another output format

This allows the project to grow without requiring major changes to the core assessment workflow.

---

# Example Workflow

```text
Target
   │
   ▼
Authorization Confirmation
   │
   ▼
Assessment Service
   │
   ├──► WHOIS Collector
   │         │
   │         ▼
   │      Evidence
   │
   ├──► Shodan Collector
   │         │
   │         ▼
   │      Evidence
   │
   ▼
Evidence Analysis
   │
   ├──► WHOIS Analyzer
   │
   └──► Shodan Analyzer
   │
   ▼
Findings
   │
   ▼
Reporter
   │
   ├──► Console
   │
   └──► JSON
```

---

# Roadmap

Potential future development areas include:

* additional reconnaissance collectors
* richer exposure analysis
* expanded finding rules
* additional output formats
* AI-assisted evidence summarization
* risk prioritization improvements
* automated security workflow integrations
* additional CI quality gates
* broader test coverage
* containerized deployment

The architecture is designed to support these additions without tightly coupling them to existing collectors or analyzers.

---

# Responsible Use

AI-RECON is intended for:

* authorized penetration testing
* security assessments
* asset exposure reviews
* security research conducted with permission
* testing systems you own or are explicitly authorized to assess

Do not use this tool against systems without explicit authorization.

Users are responsible for ensuring that their use of AI-RECON complies with applicable laws, contracts, and organizational policies.

---

# License

This project is licensed under the terms of the included `LICENSE` file.

---

# Author

**Toluwalase Owolabi**

Cybersecurity professional focused on:

* security operations
* vulnerability management
* offensive security
* cloud security
* security automation
* AI security

---

## Contributing

Contributions, ideas, and feedback are welcome.

Before submitting changes, please ensure:

```bash
ruff check .
ruff format --check .
mypy src
pytest -v
```

all pass successfully.
