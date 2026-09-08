"""TV-01 adapter for canonical Du Niên. No local relationship matrix."""

from __future__ import annotations

from consulting.canon.du_nien import is_favorable, lookup, summary_for_label


def palace_relation(cung_a: str, cung_b: str) -> str | None:
    """Return the canonical Du Niên label of two existing palaces."""
    relation = lookup(cung_a, cung_b)
    if relation is None:
        return None
    return relation.relationship_label


def relation_meaning(relation: str) -> str:
    """Short customer meaning from the canonical catalog."""
    return summary_for_label(relation)


def is_auspicious(relation: str) -> bool:
    """True for the four favorable canonical relationship labels."""
    return is_favorable(relation)
