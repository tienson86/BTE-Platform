"""Decision-layer contract. Uses COMMON Decision Engine later. No local engine."""

from __future__ import annotations

from abc import ABC, abstractmethod

from consulting.marriage.decision.context import MarriageDecisionContext
from consulting.marriage.models.decision import MarriageDomainResults, MarriageOverallDecision


class MarriageDecisionResolver(ABC):
    """Resolves domain and overall decisions. Must not duplicate Decision Mathematics."""

    @abstractmethod
    def resolve_domains(self, context: MarriageDecisionContext) -> MarriageDomainResults:
        """Resolve domain decisions from evidence and findings."""

    @abstractmethod
    def resolve_overall(self, context: MarriageDecisionContext) -> MarriageOverallDecision:
        """Resolve the overall marriage decision."""
