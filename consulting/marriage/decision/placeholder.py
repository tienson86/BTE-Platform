"""Decision placeholder. No Decision Engine duplication in TV1-B01."""

from __future__ import annotations

from consulting.marriage.decision.context import MarriageDecisionContext
from consulting.marriage.decision.contract import MarriageDecisionResolver
from consulting.marriage.models.decision import MarriageDomainResults, MarriageOverallDecision


class PlaceholderMarriageDecisionResolver(MarriageDecisionResolver):
    """Skeleton placeholder. Does not compute decisions."""

    def resolve_domains(self, context: MarriageDecisionContext) -> MarriageDomainResults:
        """Refuse domain resolution. Decision integration belongs to TV1-B02/B03."""
        raise NotImplementedError("TV1-B01: marriage decision is not implemented")

    def resolve_overall(self, context: MarriageDecisionContext) -> MarriageOverallDecision:
        """Refuse overall resolution. Decision integration belongs to TV1-B02/B03."""
        raise NotImplementedError("TV1-B01: marriage decision is not implemented")
