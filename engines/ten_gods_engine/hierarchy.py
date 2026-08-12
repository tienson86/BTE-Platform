"""Hierarchy assignment for Ten Gods Core Engine."""

from __future__ import annotations

from engines.ten_gods_engine.constants import (
    DAY_MASTER_GOD_ID,
    GOD_ID_TO_LABEL,
    SECONDARY_WEIGHT_RATIO,
    TEN_GOD_IDS,
)
from engines.ten_gods_engine.models import DistributionEntry, DominanceResult, HierarchyEntry


def assign_hierarchy(
    distribution: tuple[DistributionEntry, ...],
    dominance: DominanceResult,
) -> tuple[HierarchyEntry, ...]:
    """Assign PRIMARY / SECONDARY / SUPPORTING / DORMANT / UNDETERMINED tiers."""
    by_id = {entry.god_id: entry for entry in distribution}
    present_ids = {
        entry.god_id
        for entry in distribution
        if entry.occurrence_count > 0 or entry.weighted_contribution > 0
    }

    ranked = sorted(
        (
            entry
            for entry in distribution
            if entry.god_id != DAY_MASTER_GOD_ID and entry.god_id in present_ids
        ),
        key=lambda item: (-item.weighted_contribution, item.god_id),
    )

    tier_by_id: dict[str, str] = {}
    if dominance.status == "DETERMINED" and dominance.primary_god_ids:
        primary_id = dominance.primary_god_ids[0]
        tier_by_id[primary_id] = "PRIMARY"
        primary_weight = by_id[primary_id].weighted_contribution
        threshold = primary_weight * SECONDARY_WEIGHT_RATIO
        for entry in ranked:
            if entry.god_id == primary_id:
                continue
            if entry.weighted_contribution >= threshold:
                tier_by_id.setdefault(entry.god_id, "SECONDARY")
            elif entry.weighted_contribution > 0:
                tier_by_id.setdefault(entry.god_id, "SUPPORTING")
    elif dominance.status == "UNDETERMINED" and ranked:
        for index, entry in enumerate(ranked):
            if index == 0:
                tier_by_id[entry.god_id] = "UNDETERMINED"
            elif entry.weighted_contribution > 0:
                tier_by_id.setdefault(entry.god_id, "SUPPORTING")

    entries: list[HierarchyEntry] = []
    for god_id in TEN_GOD_IDS:
        entry = by_id.get(god_id)
        weight = entry.weighted_contribution if entry else 0.0
        tier = tier_by_id.get(god_id)
        if tier is None:
            tier = "DORMANT" if god_id not in present_ids else "SUPPORTING"
        entries.append(
            HierarchyEntry(
                god_id=god_id,
                label=GOD_ID_TO_LABEL[god_id],
                tier=tier,
                weighted_contribution=weight,
            )
        )

    entries.sort(key=lambda item: (item.tier, item.god_id))
    return tuple(entries)
