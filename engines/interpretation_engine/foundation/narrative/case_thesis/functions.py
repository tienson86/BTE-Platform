"""Operating functions of already-validated chart roles.

These labels classify existing Pattern / Ten God / stem inventories.
They are not a persona registry and are not customer-facing.
"""

from __future__ import annotations

from engines.interpretation_engine.foundation.knowledge.entity_types import (
    TEN_GOD_ROLE_KEYS,
    USEFUL_GOD_STEM_KEYS,
)
from engines.interpretation_engine.foundation.interpreters.useful_god.templates import (
    STEM_ELEMENT,
)
from engines.interpretation_engine.foundation.narrative.input import ChartFocus

ROLE_FUNCTION: dict[str, str] = {
    "Chính Ấn": "support",
    "Thiên Ấn": "support",
    "Chính Tài": "resource",
    "Thiên Tài": "resource",
    "Chính Quan": "authority",
    "Thất Sát": "authority",
    "Thực Thần": "output",
    "Thương Quan": "output",
    "Tỷ Kiên": "peer",
    "Kiếp Tài": "peer",
}

ELEMENT_FUNCTION: dict[str, str] = {
    "Mộc": "growth",
    "Hỏa": "visibility",
    "Thổ": "stability",
    "Kim": "discipline",
    "Thủy": "circulation",
}

STRENGTH_FUNCTION: dict[str, str] = {
    "strong": "surplus",
    "very_strong": "surplus",
    "weak": "deficit",
    "very_weak": "deficit",
    "balanced": "balance",
    "thân vượng": "surplus",
    "vượng": "surplus",
    "thân nhược": "deficit",
    "nhược": "deficit",
    "trung hòa": "balance",
}

CORRECTIVE_ID: dict[str, str] = {
    "output": "release_output",
    "discipline": "introduce_discipline",
    "circulation": "improve_circulation",
    "resource": "circulate_resource",
    "visibility": "refine_visibility",
    "support": "strengthen_support",
    "authority": "introduce_structure",
    "growth": "open_growth",
    "stability": "stabilize_base",
    "peer": "stand_independently",
}

GOVERNING_DOMAINS: tuple[str, ...] = ("Pattern", "Strength", "UsefulGod")
SUPPORTING_DOMAINS: tuple[str, ...] = ("TenGods", "ShenSha")
CROSS_CASE_SIMILARITY_MAX: float = 0.50
TITLE_WORD_LIMIT: int = 8
SHORT_THESIS_SENTENCE_MIN: int = 2
SHORT_THESIS_SENTENCE_MAX: int = 4
EXPANDED_THESIS_WORD_LIMIT: int = 180


def strength_function(focus: ChartFocus) -> str:
    """Map copied strength state/label onto surplus / balance / deficit."""
    for raw in (focus.strength_state, focus.strength_label):
        key = str(raw or "").strip().casefold()
        if key in STRENGTH_FUNCTION:
            return STRENGTH_FUNCTION[key]
    return ""


def function_of(
    key: str,
    *,
    stem_roles: tuple[tuple[str, str], ...] = (),
) -> str:
    """Resolve one copied name to an operating function. No new astrology."""
    text = str(key or "").strip()
    if not text:
        return ""
    if text in ROLE_FUNCTION:
        return ROLE_FUNCTION[text]
    for stem, role in stem_roles:
        if stem == text and role in ROLE_FUNCTION:
            return ROLE_FUNCTION[role]
    element = STEM_ELEMENT.get(text, "")
    if element in ELEMENT_FUNCTION:
        return ELEMENT_FUNCTION[element]
    if text in ELEMENT_FUNCTION:
        return ELEMENT_FUNCTION[text]
    return ""


def majority_function(
    keys: tuple[str, ...],
    *,
    stem_roles: tuple[tuple[str, str], ...] = (),
) -> str:
    """Pick the dominant function from a copied name list."""
    counts: dict[str, int] = {}
    order: list[str] = []
    for key in keys:
        item = function_of(key, stem_roles=stem_roles)
        if not item:
            continue
        if item not in counts:
            order.append(item)
        counts[item] = counts.get(item, 0) + 1
    if not counts:
        return ""
    return max(order, key=lambda name: (counts[name], -order.index(name)))


def useful_function(focus: ChartFocus) -> str:
    """Useful God function: role if selected is a Ten God, else stem element."""
    if is_ten_god_role(focus.selected):
        return function_of(focus.selected, stem_roles=focus.stem_roles)
    if is_stem(focus.selected):
        mapped = function_of(focus.selected, stem_roles=())
        if mapped:
            return mapped
    if focus.useful_god_role:
        mapped = function_of(focus.useful_god_role, stem_roles=focus.stem_roles)
        if mapped:
            return mapped
    return function_of(focus.selected, stem_roles=focus.stem_roles)


def dominant_element(focus: ChartFocus) -> str:
    """Copy the highest five-element count when present."""
    if focus.dominant_element:
        return focus.dominant_element
    if not focus.five_elements:
        return ""
    name, _count = max(focus.five_elements, key=lambda item: item[1])
    return name


def is_ten_god_role(key: str) -> bool:
    """True when the copied name is a Ten God role, not a stem."""
    return key in TEN_GOD_ROLE_KEYS


def is_stem(key: str) -> bool:
    """True when the copied name is a heavenly stem."""
    return key in USEFUL_GOD_STEM_KEYS
