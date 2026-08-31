from __future__ import annotations

from ai_recon.collectors import EvidenceCollector
from ai_recon.models import (
    Assessment,
    Evidence,
    EvidenceMode,
    EvidenceStatus,
    Target,
)
from ai_recon.services.assessment import AssessmentService


class FakeCollector(EvidenceCollector):
    """Test collector that records the targets it receives."""

    source = "fake"

    def __init__(
        self,
        source: str,
        status: EvidenceStatus = EvidenceStatus.SUCCESS,
    ) -> None:
        self.source = source
        self.status = status
        self.received_targets: list[Target] = []

    def collect(self, target: Target) -> Evidence:
        self.received_targets.append(target)

        return Evidence(
            source=self.source,
            target=target.identifier,
            observations={"collector": self.source},
            mode=EvidenceMode.LIVE,
            status=self.status,
            error=(
                "Collection failed."
                if self.status == EvidenceStatus.ERROR
                else None
            ),
        )


def test_create_assessment_returns_assessment_for_target() -> None:
    target = Target(identifier="example.com")
    service = AssessmentService()

    assessment = service.create_assessment(target)

    assert isinstance(assessment, Assessment)
    assert assessment.target == target
    assert assessment.evidence == []
    assert assessment.findings == []


def test_collect_evidence_executes_all_collectors() -> None:
    target = Target(identifier="example.com")

    whois_collector = FakeCollector("whois")
    shodan_collector = FakeCollector("shodan")

    service = AssessmentService(
        collectors=[
            whois_collector,
            shodan_collector,
        ]
    )

    assessment = service.create_assessment(target)
    result = service.collect_evidence(assessment)

    assert result is assessment

    assert whois_collector.received_targets == [target]
    assert shodan_collector.received_targets == [target]

    assert len(assessment.evidence) == 2

    assert assessment.evidence[0].source == "whois"
    assert assessment.evidence[1].source == "shodan"


def test_collect_evidence_allows_empty_collector_configuration() -> None:
    target = Target(identifier="example.com")
    service = AssessmentService()

    assessment = service.create_assessment(target)
    result = service.collect_evidence(assessment)

    assert result is assessment
    assert assessment.evidence == []


def test_collect_evidence_preserves_error_evidence() -> None:
    target = Target(identifier="example.com")

    failing_collector = FakeCollector(
        "failing",
        status=EvidenceStatus.ERROR,
    )

    service = AssessmentService(
        collectors=[failing_collector]
    )

    assessment = service.create_assessment(target)
    service.collect_evidence(assessment)

    assert len(assessment.evidence) == 1

    evidence = assessment.evidence[0]

    assert evidence.status is EvidenceStatus.ERROR
    assert evidence.error == "Collection failed."
    assert assessment.has_collection_errors
