from __future__ import annotations

from collections.abc import Sequence

from ai_recon.collectors import EvidenceCollector
from ai_recon.models import Assessment, Target


class AssessmentService:
    """Coordinates an authorized reconnaissance assessment workflow."""

    def __init__(
        self,
        collectors: Sequence[EvidenceCollector] = (),
    ) -> None:
        self._collectors = collectors

    def create_assessment(self, target: Target) -> Assessment:
        """Create an assessment for a target."""

        return Assessment(target=target)

    def collect_evidence(
        self,
        assessment: Assessment,
    ) -> Assessment:
        """Collect evidence from all configured collectors."""

        for collector in self._collectors:
            evidence = collector.collect(assessment.target)
            assessment.add_evidence(evidence)

        return assessment
