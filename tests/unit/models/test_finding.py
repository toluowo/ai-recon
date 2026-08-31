from ai_recon.models import (
    Confidence,
    Finding,
    Severity,
)


def test_finding() -> None:
    finding = Finding(
        id="EXPOSURE-001",
        title="Internet-exposed service",
        severity=Severity.HIGH,
        confidence=Confidence.HIGH,
        description="A service is externally accessible.",
        source="shodan",
    )

    assert finding.id == "EXPOSURE-001"
