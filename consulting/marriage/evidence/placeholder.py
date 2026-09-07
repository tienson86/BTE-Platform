"""Evidence placeholder. No evidence rules in TV1-B01."""

from __future__ import annotations

from consulting.marriage.evidence.contract import MarriageEvidenceBuilder
from consulting.marriage.models.context import MarriageRelationshipContext
from consulting.marriage.models.evidence import MarriageEvidence


class PlaceholderMarriageEvidenceBuilder(MarriageEvidenceBuilder):
    """Skeleton placeholder. Does not extract evidence."""

    def build(self, context: MarriageRelationshipContext) -> list[MarriageEvidence]:
        """Refuse evidence construction."""
        raise NotImplementedError("TV1-B01: evidence builder is not implemented")
