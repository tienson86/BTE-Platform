"""Marriage policy provider contract. Identity only. No policy rules."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass

from consulting.marriage.decision.context import MarriageDecisionContext


@dataclass(frozen=True, slots=True)
class MarriagePolicyDescriptor:
    """Identity of a Marriage Decision Policy. Contains no rules."""

    policy_id: str
    version: str


class MarriagePolicyProvider(ABC):
    """Provides the Marriage Decision Policy. Must not evaluate evidence."""

    @abstractmethod
    def descriptor(self) -> MarriagePolicyDescriptor:
        """Return policy identity."""

    @abstractmethod
    def provide(self, context: MarriageDecisionContext) -> MarriagePolicyDescriptor:
        """Resolve the policy for a decision context. No rule evaluation in TV1-B01."""
