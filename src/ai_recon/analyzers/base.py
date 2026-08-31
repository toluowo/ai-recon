from __future__ import annotations

from abc import ABC, abstractmethod

from ai_recon.models import Evidence, Finding


class EvidenceAnalyzer(ABC):
    """Base interface for evidence analyzers."""

    source: str

    @abstractmethod
    def analyze(self, evidence: Evidence) -> list[Finding]:
        """Analyze evidence and return security findings."""
