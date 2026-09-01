from __future__ import annotations

from ai_recon.analyzers import ShodanAnalyzer, WhoisAnalyzer
from ai_recon.collectors import ShodanCollector, WhoisCollector
from ai_recon.services import AssessmentService


def create_assessment_service(
    *,
    shodan_api_key: str | None = None,
) -> AssessmentService:
    """Create the application's configured assessment service."""

    collectors = [
        WhoisCollector(),
        ShodanCollector(
            api_key=shodan_api_key,
        ),
    ]

    analyzers = [
        WhoisAnalyzer(),
        ShodanAnalyzer(),
    ]

    return AssessmentService(
        collectors=collectors,
        analyzers=analyzers,
    )