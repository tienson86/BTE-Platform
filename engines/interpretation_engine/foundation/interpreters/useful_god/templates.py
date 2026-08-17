"""Deterministic interpretation templates for Useful God (Sprint B1)."""

from __future__ import annotations

ELEMENT_LABELS: dict[str, str] = {
    "wood": "Mộc",
    "fire": "Hỏa",
    "earth": "Thổ",
    "metal": "Kim",
    "water": "Thủy",
}

STEM_ELEMENT: dict[str, str] = {
    "Giáp": "Mộc",
    "Ất": "Mộc",
    "Bính": "Hỏa",
    "Đinh": "Hỏa",
    "Mậu": "Thổ",
    "Kỷ": "Thổ",
    "Canh": "Kim",
    "Tân": "Kim",
    "Nhâm": "Thủy",
    "Quý": "Thủy",
}

KNOWLEDGE_ENTITY_TYPE_STEM = "stem"
KNOWLEDGE_ENTITY_TYPE_ROLE = "role"
KNOWLEDGE_ENTITY_TYPE_ELEMENT = "element"


def customer_display_label(value: str, entity_type: str) -> str:
    """Format Useful God / Hỷ / Kỵ for customer display from canonical type.

    stem → ``Đinh (Hỏa)`` using STEM_ELEMENT only.
    role → ``Thực Thần`` with no appended element.
    element → canonical element label only.
    Missing type → the value only. Never invent an element.
    """
    text = str(value or "").strip()
    if not text:
        return ""
    kind = str(entity_type or "").strip()
    if kind == KNOWLEDGE_ENTITY_TYPE_STEM:
        element = STEM_ELEMENT.get(text)
        if element:
            return f"{text} ({element})"
        return text
    return text


STRENGTH_VI: dict[str, str] = {
    "strong": "vượng",
    "weak": "nhược",
    "balanced": "trung hòa",
}

TEMPERATURE_VI: dict[str, str] = {
    "hot": "nóng",
    "warm": "ấm",
    "cool": "mát",
    "cold": "lạnh",
}

# Mirror UsefulGodEngine PriorityResolver default group priorities (interpretation only).
GROUP_PRIORITY: dict[str, int] = {
    "special": 100,
    "season": 90,
    "strength": 80,
    "temperature": 70,
    "flow": 60,
}

GROUP_LABEL_VI: dict[str, str] = {
    "special": "cách đặc biệt",
    "season": "mùa / lệnh tháng",
    "strength": "thân vượng nhược",
    "temperature": "điều hậu / khí hậu",
    "flow": "cân bằng ngũ hành",
}

IMPACT_DOMAINS: tuple[str, ...] = (
    "career",
    "wealth",
    "relationships",
    "health",
    "learning_growth",
)

RECOMMENDATION_CATEGORIES: tuple[str, ...] = (
    "priority_actions",
    "supportive_environments",
    "elements_to_cultivate",
    "elements_to_avoid",
    "decision_guidance",
)
