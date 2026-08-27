"""Semantic layout tokens for Date Selection reports.

Identifiers only. PACK 05 Theme Engine resolves actual visual values.
"""

from __future__ import annotations

from engines.report_engine.layout.theme_resolver import (
    ICON_SET_ID,
    PALETTE_ID,
    SPACING_ID,
    THEME_ID,
    TYPOGRAPHY_ID,
)

TEMPLATE_ID = "date_selection_report"
TEMPLATE_VERSION = "1.0"

TYPOGRAPHY_TOKENS: dict[str, str] = {
    "report_title": "typography.report_title",
    "section_title": "typography.section_title",
    "recommendation_date": "typography.recommendation_date",
    "recommendation_result": "typography.recommendation_result",
    "label": "typography.label",
    "value": "typography.value",
    "secondary": "typography.secondary",
}

SPACING_TOKENS: dict[str, str] = {
    "section_gap": "spacing.section_gap",
    "card_padding": "spacing.card_padding",
    "row_gap": "spacing.row_gap",
}

COLOR_TOKENS: dict[str, str] = {
    "primary": "color.primary",
    "muted": "color.muted",
    "divider": "color.divider",
    "element_moc": "color.element_moc",
    "element_hoa": "color.element_hoa",
    "element_tho": "color.element_tho",
    "element_kim": "color.element_kim",
    "element_thuy": "color.element_thuy",
}

ICON_TOKENS: dict[str, str] = {
    "calendar": "icon.calendar",
    "person": "icon.person",
    "clock": "icon.clock",
}

ELEMENT_COLOR_TOKEN: dict[str, str] = {
    "Mộc": COLOR_TOKENS["element_moc"],
    "Hỏa": COLOR_TOKENS["element_hoa"],
    "Thổ": COLOR_TOKENS["element_tho"],
    "Kim": COLOR_TOKENS["element_kim"],
    "Thủy": COLOR_TOKENS["element_thuy"],
}

THEME_REF: dict[str, str] = {
    "theme_id": THEME_ID,
    "palette_id": PALETTE_ID,
    "spacing_id": SPACING_ID,
    "typography_id": TYPOGRAPHY_ID,
    "icon_set_id": ICON_SET_ID,
}

SECTION_ORDER: tuple[str, ...] = (
    "header",
    "person",
    "search_period",
    "recommendations",
    "guidance",
    "footer",
)

DAY_PRESENTATION_ORDER: tuple[str, ...] = (
    "solar_date",
    "lunar_date",
    "day_result",
    "year_ganzhi",
    "month_ganzhi",
    "day_ganzhi",
    "nayin",
    "cung_phi",
    "trach_group",
)

PERSON_FIELD_ORDER: tuple[str, ...] = (
    "full_name",
    "gender",
    "birth_solar",
    "birth_lunar",
    "year_ganzhi",
    "nayin",
    "cung_phi",
    "trach_group",
)
