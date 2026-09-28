# AI-RECON Security Architecture

AI-RECON is designed as a defensive security-assessment pipeline: collect externally observable evidence, preserve provenance, analyze that evidence into structured findings, and report the result in machine- and human-readable formats.

## Architecture

```text
Authorized Operator
        |
        v
Authorization / CLI
        |
        v
Assessment Service
        |
   +----+----+
   |         |
   v         v
WHOIS     Shodan
Collector Collector
   |         |
   +----+----+
        v
   Evidence Model
        |
        v
    Analyzers
        |
        v
 Structured Findings
        |
   +----+----+
   |         |
   v         v
Console      JSON
```

## Trust Boundaries

External API responses and target-derived data are treated as untrusted input. Collectors normalize external responses before they reach analysis logic. Analyzer components operate on normalized evidence rather than directly on provider-specific responses.

The authorization acknowledgement is an operational safety control. It does not replace legal authorization, contractual approval, or organizational security procedures.

## Data Flow

1. The operator supplies a target and explicitly confirms authorization.
2. The assessment service validates the target and loads configuration.
3. Collectors obtain permitted external evidence.
4. Evidence is normalized into domain models.
5. Analyzers evaluate observable exposure patterns.
6. Findings include severity, confidence, source, evidence references, and remediation guidance.
7. Reporters serialize the assessment for human review or downstream automation.

## Security Design Principles

### Evidence before findings

Findings should be explainable from collected evidence. This improves traceability and makes assessment results easier to validate.

### Least privilege for integrations

External API credentials are supplied through supported configuration mechanisms and must never be committed to source control.

### Graceful integration failure

Missing credentials, API errors, network failures, and unavailable providers are represented as collection state instead of silently producing successful evidence.

### Separation of concerns

Collectors, analyzers, domain models, services, and reporters have separate responsibilities. This limits the blast radius of changes and makes security controls easier to test independently.

### Deterministic validation

CI validates linting, formatting, strict type checking, automated tests, package creation, clean-environment installation, and an installed CLI smoke test.

## Current Security Controls

- Explicit authorization acknowledgement before an assessment runs.
- No credentials stored in source control.
- Structured evidence and finding models.
- Evidence references attached to findings.
- Graceful handling of unavailable optional integrations.
- Strict static type checking with MyPy.
- Automated unit tests with Pytest.
- Ruff linting and formatting validation.
- Multi-version CI for Python 3.10, 3.11, and 3.12.
- Clean-environment package installation validation.
- Dedicated security vulnerability reporting policy.

## Future Hardening Opportunities

Potential future improvements include:

- Signed assessment artifacts
- Stronger evidence integrity metadata
- SARIF output
- Configurable policy gates
- Dependency/security scanning
- Structured audit logging
- Additional authorization controls for any future hosted deployment
