from __future__ import annotations

from typing import Protocol

from ai_recon.models import Evidence, Target


class EvidenceCollector(Protocol):
    """Interface implemented by reconnaissance evidence collectors."""

    source: str

    def collect(self, target: Target) -> Evidence:
        """Collect normalized evidence for a target."""
