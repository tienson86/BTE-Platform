"""Date Selection report template package.

Declarative section/placeholder catalog. Reuses PACK 05 PlaceholderModel.
Does not introduce a second templating framework or HTML renderer.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from engines.date_selection_report.rendering.tokens import (
    SECTION_ORDER,
    TEMPLATE_ID,
    TEMPLATE_VERSION,
    THEME_REF,
)
from engines.report_engine.models.foundation_models import PlaceholderModel

REQUIRED_SECTIONS: tuple[str, ...] = SECTION_ORDER

REQUIRED_PLACEHOLDERS: tuple[tuple[str, str], ...] = (
    ("header.title", "metadata.title"),
    ("header.subtitle", "metadata.generator"),
    ("person.full_name", "person.full_name"),
    ("person.gender", "person.gender"),
    ("person.birth_solar", "person.birth_solar"),
    ("person.birth_lunar", "person.birth_lunar"),
    ("person.year_ganzhi", "person.year_ganzhi"),
    ("person.nayin", "person.nayin"),
    ("person.cung_phi", "person.cung_phi"),
    ("person.trach_group", "person.trach_group"),
    ("search_period.display", "search_period.display"),
    ("recommendation.solar_date", "recommendation.solar_date"),
    ("recommendation.lunar_date", "recommendation.lunar_date"),
    ("recommendation.day_result", "recommendation.day_result"),
    ("recommendation.year_ganzhi", "recommendation.year_ganzhi"),
    ("recommendation.month_ganzhi", "recommendation.month_ganzhi"),
    ("recommendation.day_ganzhi", "recommendation.day_ganzhi"),
    ("recommendation.nayin", "recommendation.nayin"),
    ("recommendation.cung_phi", "recommendation.cung"),
    ("recommendation.trach_group", "recommendation.trach_group"),
    ("hour.branch", "hour.branch"),
    ("hour.time_range", "hour.time_range"),
    ("hour.cung", "hour.cung"),
    ("guidance.title", "guidance.title"),
    ("footer.generator", "metadata.generator"),
)

SECTION_TEMPLATES: tuple[str, ...] = (
    "root",
    "header",
    "person",
    "search_period",
    "recommendation",
    "compatible_hours",
    "positive_times",
    "guidance",
    "footer",
)


def _placeholders() -> tuple[PlaceholderModel, ...]:
    return tuple(
        PlaceholderModel(placeholder_id=placeholder_id, binding_path=binding_path)
        for placeholder_id, binding_path in REQUIRED_PLACEHOLDERS
    )


@dataclass(frozen=True, slots=True)
class DateSelectionTemplatePackage:
    """Logical template package shared by future PDF and DOCX renderers."""

    template_id: str
    template_version: str
    section_ids: tuple[str, ...]
    nested_templates: tuple[str, ...]
    placeholders: tuple[PlaceholderModel, ...]
    theme_id: str
    palette_id: str
    spacing_id: str
    typography_id: str
    icon_set_id: str

    def to_dict(self) -> dict[str, Any]:
        """Serialize template identity and placeholder catalog."""
        return {
            "template_id": self.template_id,
            "template_version": self.template_version,
            "section_ids": list(self.section_ids),
            "nested_templates": list(self.nested_templates),
            "placeholders": [item.to_dict() for item in self.placeholders],
            "theme_id": self.theme_id,
            "palette_id": self.palette_id,
            "spacing_id": self.spacing_id,
            "typography_id": self.typography_id,
            "icon_set_id": self.icon_set_id,
        }


def load_date_selection_template_package() -> DateSelectionTemplatePackage:
    """Return the canonical Date Selection template catalog."""
    return DateSelectionTemplatePackage(
        template_id=TEMPLATE_ID,
        template_version=TEMPLATE_VERSION,
        section_ids=REQUIRED_SECTIONS,
        nested_templates=SECTION_TEMPLATES,
        placeholders=_placeholders(),
        theme_id=THEME_REF["theme_id"],
        palette_id=THEME_REF["palette_id"],
        spacing_id=THEME_REF["spacing_id"],
        typography_id=THEME_REF["typography_id"],
        icon_set_id=THEME_REF["icon_set_id"],
    )
