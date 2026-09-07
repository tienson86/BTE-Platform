"""Decision package."""

from __future__ import annotations

from consulting.marriage.decision.context import MarriageDecisionContext
from consulting.marriage.decision.contract import MarriageDecisionResolver
from consulting.marriage.decision.placeholder import PlaceholderMarriageDecisionResolver

__all__ = [
    "MarriageDecisionContext",
    "MarriageDecisionResolver",
    "PlaceholderMarriageDecisionResolver",
]
