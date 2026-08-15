"""Canonical semantic relationship types — not domain rule encodings."""

from __future__ import annotations

from typing import Final

RELATIONSHIP_SUPPORTS: Final[str] = "supports"
RELATIONSHIP_GENERATES: Final[str] = "generates"
RELATIONSHIP_DRAINS: Final[str] = "drains"
RELATIONSHIP_CONTROLS: Final[str] = "controls"
RELATIONSHIP_BALANCES: Final[str] = "balances"
RELATIONSHIP_CONFLICTS: Final[str] = "conflicts"
RELATIONSHIP_TRANSFORMS: Final[str] = "transforms"
RELATIONSHIP_COMBINES: Final[str] = "combines"

CANONICAL_RELATIONSHIP_TYPES: Final[tuple[str, ...]] = (
    RELATIONSHIP_SUPPORTS,
    RELATIONSHIP_GENERATES,
    RELATIONSHIP_DRAINS,
    RELATIONSHIP_CONTROLS,
    RELATIONSHIP_BALANCES,
    RELATIONSHIP_CONFLICTS,
    RELATIONSHIP_TRANSFORMS,
    RELATIONSHIP_COMBINES,
)

DIRECTION_SOURCE_TO_TARGET: Final[str] = "source_to_target"
DIRECTION_TARGET_TO_SOURCE: Final[str] = "target_to_source"
DIRECTION_BIDIRECTIONAL: Final[str] = "bidirectional"
