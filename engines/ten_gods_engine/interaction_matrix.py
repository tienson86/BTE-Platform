"""Deterministic Ten Gods interaction matrix."""

from __future__ import annotations

from engines.ten_gods_engine.constants import (
    FAMILY_CONTROLS,
    FAMILY_GENERATES,
    GOD_ID_TO_FAMILY,
)
from engines.ten_gods_engine.models import InteractionCell

INTERACTION_SEMANTICS = {
    "SUPPORT": "Row family generates Column family (生).",
    "CONTROL": "Row family controls Column family (克).",
    "DRAIN": "Column family generates Row family — Row loses energy to Column (泄).",
    "SAME": "Same god_id or same structural family.",
    "INDIRECT": "One-hop mixed generate/control relation between families.",
    "NONE": "No direct structural relation between families.",
    "UNKNOWN": "God not present in chart inventory.",
}


def _family_generates(source: str, target: str) -> bool:
    return (source, target) in FAMILY_GENERATES


def _family_controls(source: str, target: str) -> bool:
    return (source, target) in FAMILY_CONTROLS


def _one_hop_related(family_a: str, family_b: str) -> bool:
    if family_a == family_b:
        return False
    families = {item[0] for item in FAMILY_GENERATES} | {
        item[1] for item in FAMILY_GENERATES
    }
    for mid in families:
        forward = _family_generates(family_a, mid) and (
            _family_generates(mid, family_b) or _family_controls(mid, family_b)
        )
        reverse = _family_generates(family_b, mid) and (
            _family_generates(mid, family_a) or _family_controls(mid, family_a)
        )
        if forward or reverse:
            return True
    return False


def resolve_interaction(row_id: str, col_id: str) -> str:
    """Resolve one matrix cell using structural family semantics."""
    if row_id == col_id:
        return "SAME"

    row_family = GOD_ID_TO_FAMILY.get(row_id)
    col_family = GOD_ID_TO_FAMILY.get(col_id)
    if row_family is None or col_family is None:
        return "UNKNOWN"

    if row_family == col_family:
        return "SAME"
    if _family_generates(row_family, col_family):
        return "SUPPORT"
    if _family_controls(row_family, col_family):
        return "CONTROL"
    if _family_generates(col_family, row_family):
        return "DRAIN"
    if _one_hop_related(row_family, col_family):
        return "INDIRECT"
    return "NONE"


def build_interaction_matrix(
    present_god_ids: set[str],
) -> tuple[InteractionCell, ...]:
    """Build full matrix for Ten Gods present in chart (excludes day_master)."""
    gods = sorted(present_god_ids - {"day_master"})
    cells: list[InteractionCell] = []
    for row_id in gods:
        for col_id in gods:
            cells.append(
                InteractionCell(
                    row_god_id=row_id,
                    col_god_id=col_id,
                    state=resolve_interaction(row_id, col_id),
                )
            )
    return tuple(cells)
