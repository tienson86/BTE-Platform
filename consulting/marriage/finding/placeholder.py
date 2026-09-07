"""Finding placeholder. No finding rules in TV1-B01."""

from __future__ import annotations

from consulting.marriage.finding.contract import MarriageFindingBuilder
from consulting.marriage.models.evidence import MarriageEvidence
from consulting.marriage.models.finding import MarriageFinding


class PlaceholderMarriageFindingBuilder(MarriageFindingBuilder):
    """Skeleton placeholder. Does not derive findings."""

    def build(self, evidence: list[MarriageEvidence]) -> list[MarriageFinding]:
        """Refuse finding construction."""
        raise NotImplementedError("TV1-B01: finding builder is not implemented")
