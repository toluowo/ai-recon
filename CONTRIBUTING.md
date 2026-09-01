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

rm -rf build dist

python -m build

git add pyproject.toml CHANGELOG.md

git commit -m "chore(release): prepare v0.2.1"

git tag -a v0.2.1 -m "Release v0.2.1"

git push origin main

git push origin v0.2.1
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

## Versioning

AI-RECON follows Semantic Versioning.

Version numbers use the format:

MAJOR.MINOR.PATCH

## MAJOR

Increment the major version when introducing incompatible changes to public interfaces or expected behaviour.

Examples include:

* breaking CLI changes
* incompatible changes to public Python APIs
* removal of supported functionality
* major architectural changes that require users to change their integration

## MINOR

Increment the minor version when adding backwards-compatible functionality.

Examples include:

* new collectors
* new analyzers
* new reporting capabilities
* new CLI features
* backwards-compatible configuration options

## PATCH

Increment the patch version for backwards-compatible bug fixes and small improvements.

Examples include:

* bug fixes
* analyzer corrections
* reporting fixes
* documentation corrections
* dependency or packaging fixes that do not introduce new functionality

## Release Process

The package version is defined in pyproject.toml.

Before creating a release:

1. Update the version in pyproject.toml.
2. Move relevant changes from the Unreleased section of CHANGELOG.md into a new version section.
3. Run the complete validation suite.
4. Verify that the package builds successfully.
5. Create a Git commit for the release.
6. Create an annotated Git tag matching the version.
7. Push the release commit and tag.

Example for version 0.2.1:

git checkout main
git pull origin main

# Update pyproject.toml and CHANGELOG.md

ruff check .
ruff format --check .
mypy src
pytest -v

python -m build

git add pyproject.toml CHANGELOG.md
git commit -m "chore(release): prepare v0.2.1"

git tag -a v0.2.1 -m "Release v0.2.1"

git push origin main
git push origin v0.2.1

Release tags should use the format:

vMAJOR.MINOR.PATCH

For example:
v0.2.0
v0.2.1
v0.3.0
v1.0.0

## Responsible Contributions

AI-RECON is intended for authorized security assessments.

Contributions should support legitimate security testing, exposure analysis, defensive security research, or authorized penetration testing.

Do not submit functionality intended to facilitate unauthorized access to systems.

## Pull Requests

Before opening a pull request:

1. Keep changes focused.
2. Add or update tests where appropriate.
3. Update documentation when behaviour changes.
4. Update CHANGELOG.md when user-visible behaviour changes.
5. Run the full validation suite.
6. Clearly describe the purpose of the change.

Small, well-scoped pull requests are preferred over large unrelated changes.