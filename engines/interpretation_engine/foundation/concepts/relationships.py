"""Concept graph relationship types (K1.5)."""

from __future__ import annotations

from enum import Enum
from typing import Final

CANONICAL_RELATIONSHIP_TYPES: Final[tuple[str, ...]] = (
    "supports",
    "requires",
    "opposes",
    "extends",
    "specializes",
    "related_to",
)


class ConceptRelationshipType(str, Enum):
    """Supported concept graph edge types."""

    SUPPORTS = "supports"
    REQUIRES = "requires"
    OPPOSES = "opposes"
    EXTENDS = "extends"
    SPECIALIZES = "specializes"
    RELATED_TO = "related_to"
