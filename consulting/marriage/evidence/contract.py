"""Evidence builder contract. Creates evidence atoms. Does not score."""

from __future__ import annotations

from abc import ABC, abstractmethod

from consulting.marriage.models.context import MarriageRelationshipContext
from consulting.marriage.models.evidence import MarriageEvidence


class MarriageEvidenceBuilder(ABC):
    """Builds relationship evidence from Canonical snapshots."""

    @abstractmethod
    def build(self, context: MarriageRelationshipContext) -> list[MarriageEvidence]:
        """Create evidence atoms. Must not compute compatibility score."""
