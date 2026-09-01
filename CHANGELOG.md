# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.2.0] - 2026-09-01

### Added

- Modular evidence collection architecture.
- WHOIS evidence collection and normalization.
- Optional Shodan evidence collection.
- Evidence analyzer framework.
- WHOIS exposure analysis.
- Shodan exposure analysis.
- Structured security findings with severity, confidence, evidence references, and remediation guidance.
- Console reporting.
- JSON reporting.
- CLI support for authorized assessments.
- Shodan API key configuration through CLI arguments and environment variables.
- Automated unit test coverage.
- Multi-version CI validation for Python 3.10, 3.11, and 3.12.
- Package build and clean-environment installation validation.
- Public project documentation including contribution and security guidance.

### Changed

- Refactored the application into modular collectors, analyzers, services, reporters, and domain models.
- Improved package metadata and distribution configuration.
- Improved repository hygiene and development tooling configuration.

### Security

- Added explicit authorization acknowledgement before assessments can run.
- Documented responsible use expectations for authorized security testing.
- Added a security vulnerability reporting policy.

## [0.1.0]

### Added

- Initial reconnaissance and external exposure analysis functionality.