"""Finding builder contract. Findings come from evidence only."""

from __future__ import annotations

from abc import ABC, abstractmethod

from consulting.marriage.models.evidence import MarriageEvidence
from consulting.marriage.models.finding import MarriageFinding


class MarriageFindingBuilder(ABC):
    """Builds findings from evidence. Must not invent findings."""

    @abstractmethod
    def build(self, evidence: list[MarriageEvidence]) -> list[MarriageFinding]:
        """Create findings from evidence atoms."""
