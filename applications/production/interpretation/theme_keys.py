"""Deterministic theme keys for cross-domain duplicate control."""

from __future__ import annotations

# Primary themes — one customer mention per integrated report.
THEME_ENDURANCE = "ENDURANCE"
THEME_RESPONSIBILITY = "RESPONSIBILITY"
THEME_LONG_STRUCTURE = "LONG_STRUCTURE"
THEME_OUTPUT_RELEASE = "OUTPUT_RELEASE"
THEME_NO_EXTRA_LOAD = "NO_EXTRA_LOAD"
THEME_PRESSURE = "PRESSURE"
THEME_RESOURCE_SUPPORT = "RESOURCE_SUPPORT"
THEME_BALANCE_STRATEGY = "BALANCE_STRATEGY"
THEME_OPERATING_SYSTEM = "OPERATING_SYSTEM"
THEME_STRUCTURAL_FRAME = "STRUCTURAL_FRAME"

# Domain ownership — preferred domain keeps the customer claim.
THEME_PRIMARY_DOMAIN: dict[str, str] = {
    THEME_ENDURANCE: "strength",
    THEME_RESPONSIBILITY: "ten_gods",
    THEME_LONG_STRUCTURE: "pattern",
    THEME_OUTPUT_RELEASE: "useful_god",
    THEME_NO_EXTRA_LOAD: "useful_god",
    THEME_PRESSURE: "ten_gods",
    THEME_RESOURCE_SUPPORT: "ten_gods",
    THEME_BALANCE_STRATEGY: "useful_god",
    THEME_OPERATING_SYSTEM: "ten_gods",
    THEME_STRUCTURAL_FRAME: "pattern",
}

STRENGTH_LEVEL_VI: dict[str, str] = {
    "very_strong": "rất vượng",
    "strong": "vượng",
    "balanced": "trung hòa",
    "weak": "nhược",
    "very_weak": "rất nhược",
}

FAMILY_VI: dict[str, str] = {
    "companion": "đồng hành",
    "output": "đầu ra / tiết khí",
    "wealth": "tài",
    "officer": "quan sát / áp lực chuẩn",
    "resource": "ấn / nền hỗ trợ",
}

RELATION_VI: dict[str, str] = {
    "restriction": "kiểm soát",
    "generation": "sinh hỗ trợ",
    "support": "cộng hưởng",
}
