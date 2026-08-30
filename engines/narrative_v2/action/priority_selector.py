"""Select exactly one Top Priority from Decisions."""

from __future__ import annotations

from engines.narrative_v2.action.action_model import TopPriority
from engines.narrative_v2.action.decision_model import DecisionItem


class PrioritySelector:
    """One Top Priority. Explicit asset priority, then decision_id."""

    def select(self, decisions: tuple[DecisionItem, ...]) -> TopPriority | None:
        """Return the highest-priority Decision as Top Priority."""
        if not decisions:
            return None
        ordered = sorted(decisions, key=lambda item: (-item.priority, item.decision_id))
        chosen = ordered[0]
        return TopPriority(
            title=chosen.title,
            description=chosen.description,
            decision_id=chosen.decision_id,
        )
