"""Internal DecisionContext. Not a customer Action Plan field."""

from __future__ import annotations

from dataclasses import dataclass

from engines.narrative_v2.action.decision_model import DecisionItem


@dataclass(frozen=True, slots=True)
class DecisionContext:
    """Selected decisions. Internal Narrative logic only."""

    items: tuple[DecisionItem, ...]
    status: str
    metadata: tuple[tuple[str, str], ...] = ()
