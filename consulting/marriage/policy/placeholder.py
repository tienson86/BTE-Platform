"""Policy placeholder. No Marriage Policy evaluation in TV1-B01."""

from __future__ import annotations

from consulting.marriage.decision.context import MarriageDecisionContext
from consulting.marriage.policy.contract import MarriagePolicyDescriptor, MarriagePolicyProvider


class PlaceholderMarriagePolicyProvider(MarriagePolicyProvider):
    """Skeleton placeholder. Does not load or apply Marriage Policy."""

    def descriptor(self) -> MarriagePolicyDescriptor:
        """Refuse policy identity resolution."""
        raise NotImplementedError("TV1-B01: marriage policy is not implemented")

    def provide(self, context: MarriageDecisionContext) -> MarriagePolicyDescriptor:
        """Refuse policy resolution."""
        raise NotImplementedError("TV1-B01: marriage policy is not implemented")
