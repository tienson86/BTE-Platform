"""Deterministic insight selection for Interpretation.

One primary insight. At most one supporting unit on the same semantic key.
"""

from __future__ import annotations

from dataclasses import dataclass

from engines.narrative_v2.rewrite.rewrite_item import RewriteItem
from engines.narrative_v2.interpretation.interpretation_formula import (
    CORE_SEMANTIC_PRIORITY,
    DOMAIN_PRIORITY,
)


@dataclass(frozen=True, slots=True)
class InterpretationSelection:
    """Exactly one primary rewrite unit and at most one supporting unit."""

    primary: RewriteItem
    supporting: RewriteItem | None


class InterpretationSelector:
    """Select the primary interpretation insight from rewrite units."""

    def select(self, items: tuple[RewriteItem, ...]) -> InterpretationSelection | None:
        """Return one insight or None when no core rewrite unit exists."""
        candidates = [item for item in items if item.semantic_key in CORE_SEMANTIC_PRIORITY]
        if not candidates:
            return None
        ordered = sorted(candidates, key=_selection_key)
        primary = ordered[0]
        supporting = _supporting_unit(ordered, primary)
        return InterpretationSelection(primary=primary, supporting=supporting)


def _selection_key(item: RewriteItem) -> tuple[int, int, str]:
    semantic_rank = (
        CORE_SEMANTIC_PRIORITY.index(item.semantic_key)
        if item.semantic_key in CORE_SEMANTIC_PRIORITY
        else len(CORE_SEMANTIC_PRIORITY)
    )
    domain_rank = (
        DOMAIN_PRIORITY.index(item.domain)
        if item.domain in DOMAIN_PRIORITY
        else len(DOMAIN_PRIORITY)
    )
    return (semantic_rank, domain_rank, item.rewrite_id)


def _supporting_unit(
    ordered: list[RewriteItem],
    primary: RewriteItem,
) -> RewriteItem | None:
    for item in ordered:
        if item.rewrite_id == primary.rewrite_id:
            continue
        if item.semantic_key != primary.semantic_key:
            continue
        return item
    return None
