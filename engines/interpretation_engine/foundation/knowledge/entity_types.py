"""Canonical knowledge entity types and engine inventories."""

from __future__ import annotations

from typing import Final

CANONICAL_KNOWLEDGE_ENTITY_TYPES: Final[tuple[str, ...]] = (
    "stem",
    "role",
    "element",
    "state",
)

KNOWLEDGE_ENTITY_TYPE_STATE: Final[str] = "state"

# Strength Engine V2 level rules (database/12_strength/06_priority_rules.csv).
# Engine inventory is strong | balanced | weak. very_strong / very_weak are not emitted.
STRENGTH_STATE_KEYS: Final[tuple[str, ...]] = (
    "strong",
    "balanced",
    "weak",
)

# Heavenly stems produced as Useful God values by season/temperature/flow rules.
USEFUL_GOD_STEM_KEYS: Final[tuple[str, ...]] = (
    "Giáp",
    "Ất",
    "Bính",
    "Đinh",
    "Mậu",
    "Kỷ",
    "Canh",
    "Tân",
    "Nhâm",
    "Quý",
)

# Ten-god role names produced as Useful God / Hỷ / Kỵ by strength and special rules.
# Engine candidate_type for these values is ``ten_god``; knowledge entity_type is ``role``.
USEFUL_GOD_ROLE_KEYS: Final[tuple[str, ...]] = (
    "Thực Thần",
    "Thương Quan",
    "Tỷ Kiên",
    "Kiếp Tài",
    "Chính Tài",
    "Thiên Tài",
    "Chính Quan",
    "Thất Sát",
    "Chính Ấn",
    "Thiên Ấn",
)

ENGINE_CANDIDATE_TYPES: Final[tuple[str, ...]] = (
    "stem",
    "ten_god",
)

KNOWLEDGE_READINESS_READY = "READY"
KNOWLEDGE_READINESS_PARTIAL = "PARTIAL"
