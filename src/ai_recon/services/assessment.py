from __future__ import annotations

from ai_recon.models import Assessment, Target


class AssessmentService:
    """Coordinates an authorized reconnaissance assessment workflow."""

    def create_assessment(self, target: Target) -> Assessment:
        return Assessment(target=target)
