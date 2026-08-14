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
