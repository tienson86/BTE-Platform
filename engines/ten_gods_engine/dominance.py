"""Deterministic dominance policy for Ten Gods Core Engine."""

from __future__ import annotations

from collections import defaultdict

from engines.ten_gods_engine.constants import (
    DAY_MASTER_GOD_ID,
    DOMINANCE_MARGIN,
    GOD_ID_TO_LABEL,
)
from engines.ten_gods_engine.models import DistributionEntry, DominanceResult

DOMINANCE_POLICY = (
    "weighted_contribution_with_margin_"
    f"{DOMINANCE_MARGIN:.2f}_exclude_day_master"
)


def resolve_dominance(
    distribution: tuple[DistributionEntry, ...],
) -> DominanceResult:
    """Resolve dominance using weighted totals; exclude Day Master."""
    totals: dict[str, float] = defaultdict(float)
    for entry in distribution:
        if entry.god_id == DAY_MASTER_GOD_ID:
            continue
        totals[entry.god_id] += entry.weighted_contribution

    if not totals:
        return DominanceResult(
            status="UNDETERMINED",
            primary_god_ids=(),
            policy=DOMINANCE_POLICY,
            weighted_totals=dict(totals),
        )

    ordered = sorted(
        totals.items(),
        key=lambda item: (-item[1], item[0]),
    )
    top_weight = ordered[0][1]
    if top_weight <= 0:
        return DominanceResult(
            status="UNDETERMINED",
            primary_god_ids=(),
            policy=DOMINANCE_POLICY,
            weighted_totals=dict(totals),
        )

    leaders = [god_id for god_id, weight in ordered if weight == top_weight]
    if len(leaders) > 1:
        return DominanceResult(
            status="UNDETERMINED",
            primary_god_ids=tuple(sorted(leaders)),
            policy=DOMINANCE_POLICY,
            weighted_totals=dict(totals),
        )

    second_weight = ordered[1][1] if len(ordered) > 1 else 0.0
    margin = top_weight - second_weight
    if margin < DOMINANCE_MARGIN:
        return DominanceResult(
            status="UNDETERMINED",
            primary_god_ids=tuple(sorted(leaders)),
            policy=DOMINANCE_POLICY,
            weighted_totals=dict(totals),
        )

    return DominanceResult(
        status="DETERMINED",
        primary_god_ids=(leaders[0],),
        policy=DOMINANCE_POLICY,
        weighted_totals=dict(totals),
    )


def label_totals(weighted_totals: dict[str, float]) -> dict[str, float]:
    """Map god_id totals to labels for reporting."""
    return {
        GOD_ID_TO_LABEL.get(god_id, god_id): weight
        for god_id, weight in sorted(weighted_totals.items())
    }
