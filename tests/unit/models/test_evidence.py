import pytest

from ai_recon.models import (
    Evidence,
    EvidenceMode,
    EvidenceStatus,
)


def test_live_evidence() -> None:
    evidence = Evidence(
        source="whois",
        target="example.com",
        observations={"registrar": "Example"},
        mode=EvidenceMode.LIVE,
    )

    assert evidence.status is EvidenceStatus.SUCCESS


def test_error_evidence_requires_error_message() -> None:
    with pytest.raises(ValueError):
        Evidence(
            source="shodan",
            target="example.com",
            observations={},
            mode=EvidenceMode.LIVE,
            status=EvidenceStatus.ERROR,
        )
