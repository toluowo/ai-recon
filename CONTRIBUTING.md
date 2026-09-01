# Contributing to AI-RECON

Thanks for your interest in contributing to AI-RECON.

AI-RECON is an extensible reconnaissance and external exposure analysis tool intended for authorized security assessments. Contributions that improve reliability, extensibility, analysis quality, testing, and developer experience are welcome.

## Development Setup

Clone the repository and create a virtual environment.

```bash
git clone <repository-url>
cd ai-recon

python3 -m venv .venv
source .venv/bin/activate
```

On Windows:

```powershell
python -m venv .venv
.venv\Scripts\activate
```

Install the project with development dependencies:

```bash
pip install -e ".[dev]"
```

## Development Workflow

Before submitting changes, run:

```bash
ruff check .

ruff format --check .

mypy src

pytest -v
```

All checks should pass before opening a pull request.

## Project Architecture

AI-RECON separates responsibilities across several layers.

* **Collectors** obtain and normalize evidence from external sources.
* **Analyzers** interpret evidence and generate structured findings.
* **Models** define the core domain objects used throughout the application.
* **Services** orchestrate assessment workflows.
* **Reporters** present assessment results.
* **Application configuration** wires the application's components together.
* **CLI** provides the user-facing command-line interface.

When adding functionality, prefer extending the appropriate layer rather than coupling unrelated responsibilities together.

## Adding a New Evidence Source

A new evidence source will typically require:

1. A collector that retrieves and normalizes evidence.
2. Tests for the collector.
3. An analyzer that interprets the evidence when applicable.
4. Tests for the analyzer.
5. Registration of the collector and analyzer in the application configuration.

New integrations should handle external failures gracefully and preserve relevant errors as assessment evidence where possible.

## Testing

New functionality should include appropriate automated tests.

Tests should be:

* deterministic
* isolated from unnecessary external dependencies
* focused on observable behaviour
* clear about expected security outcomes

Avoid requiring live API access for unit tests.

## Code Quality

The project uses:

* Ruff for linting
* Ruff for formatting
* MyPy for strict type checking
* Pytest for automated testing

Please keep new code compatible with the configured Python versions and maintain the existing typing standards.

## Responsible Contributions

AI-RECON is intended for authorized security assessments.

Contributions should support legitimate security testing, exposure analysis, defensive security research, or authorized penetration testing.

Do not submit functionality intended to facilitate unauthorized access to systems.

## Pull Requests

Before opening a pull request:

1. Keep changes focused.
2. Add or update tests where appropriate.
3. Update documentation when behaviour changes.
4. Run the full validation suite.
5. Clearly describe the purpose of the change.

Small, well-scoped pull requests are preferred over large unrelated changes.

