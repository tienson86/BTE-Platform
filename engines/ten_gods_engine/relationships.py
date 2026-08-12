"""Structural Ten Gods relationship graph."""

from __future__ import annotations

from engines.ten_gods_engine.constants import (
    FAMILY_CONTROLS,
    FAMILY_GENERATES,
    GOD_ID_TO_FAMILY,
)
from engines.ten_gods_engine.models import RelationshipEdge


def build_relationship_graph(
    present_god_ids: set[str],
) -> tuple[RelationshipEdge, ...]:
    """Build structural relationships between present Ten Gods.

    Uses family-level generation and control cycles only.
    Does not infer luck, pattern, useful god, or auspiciousness.
    """
    edges: list[RelationshipEdge] = []
    present = sorted(present_god_ids - {"day_master"})

    for left_id in present:
        left_family = GOD_ID_TO_FAMILY.get(left_id)
        if left_family is None:
            continue
        for right_id in present:
            if left_id == right_id:
                continue
            right_family = GOD_ID_TO_FAMILY.get(right_id)
            if right_family is None:
                continue

            if (left_family, right_family) in FAMILY_GENERATES:
                edges.append(
                    RelationshipEdge(
                        from_god_id=left_id,
                        to_god_id=right_id,
                        relation="generation",
                    )
                )
            if (left_family, right_family) in FAMILY_CONTROLS:
                edges.append(
                    RelationshipEdge(
                        from_god_id=left_id,
                        to_god_id=right_id,
                        relation="restriction",
                    )
                )
            if left_family == right_family:
                edges.append(
                    RelationshipEdge(
                        from_god_id=left_id,
                        to_god_id=right_id,
                        relation="support",
                    )
                )

    edges.sort(key=lambda item: (item.from_god_id, item.to_god_id, item.relation))
    return tuple(edges)
