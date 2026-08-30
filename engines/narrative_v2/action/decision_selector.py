"""Deterministic Decision eligibility for Action Builder."""

from __future__ import annotations

from engines.narrative_v2.interpretation.interpretation_formula import (
    CORE_SEMANTIC_PRIORITY,
    DOMAIN_PRIORITY,
)
from engines.narrative_v2.interpretation.interpretation_model import InterpretationNarrative
from engines.narrative_v2.rewrite.rewrite_context import CommercialRewriteContext
from engines.narrative_v2.rewrite.rewrite_item import RewriteItem

ACTION_CAPABLE_DOMAINS: frozenset[str] = frozenset({"pattern", "strength"})


class DecisionSelector:
    """Choose rewrite units that may carry a Decision. No astrology inference."""

    def select(
        self,
        rewrite: CommercialRewriteContext,
        interpretation: InterpretationNarrative,
    ) -> tuple[RewriteItem, ...]:
        """Return insight rewrite units eligible for Decision lookup."""
        if interpretation.status == "insufficient":
            return ()
        items = _insight_items(rewrite, interpretation)
        eligible = [
            item
            for item in items
            if item.domain in ACTION_CAPABLE_DOMAINS
            and item.semantic_key in CORE_SEMANTIC_PRIORITY
        ]
        return tuple(sorted(eligible, key=_selection_key))


def _insight_items(
    rewrite: CommercialRewriteContext,
    interpretation: InterpretationNarrative,
) -> tuple[RewriteItem, ...]:
    meta = dict(interpretation.metadata)
    ordered_ids: list[str] = []
    primary = meta.get("primary_rewrite_id")
    supporting = meta.get("supporting_rewrite_id")
    if primary:
        ordered_ids.append(primary)
    if supporting:
        ordered_ids.append(supporting)
    items: list[RewriteItem] = []
    for rewrite_id in ordered_ids:
        item = rewrite.item(rewrite_id)
        if item is not None:
            items.append(item)
    return tuple(items)


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
