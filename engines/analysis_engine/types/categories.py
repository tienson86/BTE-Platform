"""Shared category enums, literals, and typed dicts."""

from __future__ import annotations

from enum import Enum
from typing import Literal, TypedDict, TypeAlias

CategoryId: TypeAlias = str


class AnalysisCategory(str, Enum):
    """Top-level analysis categories."""

    STRENGTH = "strength"
    PATTERN = "pattern"
    TEMPERATURE = "temperature"
    USEFUL_GOD = "useful_god"
    TEN_GODS = "ten_gods"
    COMBINATION = "combination"
    SHENSHA = "shensha"
    DAYUN = "dayun"
    LIUNIAN = "liunian"
    LIUYUE = "liuyue"
    SCORING = "scoring"
    CONFLICT = "conflict"


CategoryLiteral = Literal[
    "strength",
    "pattern",
    "temperature",
    "useful_god",
    "ten_gods",
    "combination",
    "shensha",
    "dayun",
    "liunian",
    "liuyue",
    "scoring",
    "conflict",
]


class CategoryPayload(TypedDict):
    """Category payload contract."""

    category_id: CategoryId
    category: CategoryLiteral
    label: str | None
