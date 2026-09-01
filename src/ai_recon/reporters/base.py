from __future__ import annotations

from abc import ABC, abstractmethod

from ai_recon.models import Assessment


class AssessmentReporter(ABC):
    """Base interface for assessment report renderers."""

    @abstractmethod
    def render(self, assessment: Assessment) -> str:
        """Render an assessment into a report."""
