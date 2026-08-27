"""Immutable Date Selection render tree. Renderer-neutral."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True, slots=True)
class FieldRow:
    """One labelled presentation row."""

    key: str
    label: str
    value: str
    typography_token: str
    color_token: str | None = None

    def to_dict(self) -> dict[str, Any]:
        """Serialize a field row."""
        return {
            "key": self.key,
            "label": self.label,
            "value": self.value,
            "typography_token": self.typography_token,
            "color_token": self.color_token,
        }


@dataclass(frozen=True, slots=True)
class PaginationHints:
    """Hints only. PDF pagination is a later sprint."""

    keep_together: bool
    do_not_split: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        """Serialize pagination hints."""
        return {
            "keep_together": self.keep_together,
            "do_not_split": list(self.do_not_split),
        }


@dataclass(frozen=True, slots=True)
class HeaderSectionNode:
    """Cover / header identity."""

    section_id: str
    title: str
    subtitle: str
    generated_at: str
    report_id: str
    typography_token: str

    def to_dict(self) -> dict[str, Any]:
        """Serialize header."""
        return {
            "section_id": self.section_id,
            "title": self.title,
            "subtitle": self.subtitle,
            "generated_at": self.generated_at,
            "report_id": self.report_id,
            "typography_token": self.typography_token,
        }


@dataclass(frozen=True, slots=True)
class PersonSectionNode:
    """Person card."""

    section_id: str
    title: str
    rows: tuple[FieldRow, ...]
    cung_display: str
    icon_token: str

    def to_dict(self) -> dict[str, Any]:
        """Serialize person section."""
        return {
            "section_id": self.section_id,
            "title": self.title,
            "rows": [row.to_dict() for row in self.rows],
            "cung_display": self.cung_display,
            "icon_token": self.icon_token,
        }


@dataclass(frozen=True, slots=True)
class SearchPeriodSectionNode:
    """Search-period card."""

    section_id: str
    title: str
    month_label: str
    month_display: str
    recommendation_count_label: str
    recommendation_count: str
    explanation: str
    icon_token: str

    def to_dict(self) -> dict[str, Any]:
        """Serialize search-period section."""
        return {
            "section_id": self.section_id,
            "title": self.title,
            "month_label": self.month_label,
            "month_display": self.month_display,
            "recommendation_count_label": self.recommendation_count_label,
            "recommendation_count": self.recommendation_count,
            "explanation": self.explanation,
            "icon_token": self.icon_token,
        }


@dataclass(frozen=True, slots=True)
class DateHeaderNode:
    """Solar date, lunar date, day result."""

    solar_date: str
    lunar_date: str
    lunar_display: str
    day_result: str
    rank: int

    def to_dict(self) -> dict[str, Any]:
        """Serialize date header."""
        return {
            "solar_date": self.solar_date,
            "lunar_date": self.lunar_date,
            "lunar_display": self.lunar_display,
            "day_result": self.day_result,
            "rank": self.rank,
        }


@dataclass(frozen=True, slots=True)
class DayInformationNode:
    """Compact day fields after the date header."""

    rows: tuple[FieldRow, ...]
    cung_display: str

    def to_dict(self) -> dict[str, Any]:
        """Serialize day information."""
        return {
            "rows": [row.to_dict() for row in self.rows],
            "cung_display": self.cung_display,
        }


@dataclass(frozen=True, slots=True)
class CompatibleHourRowNode:
    """One same-Trạch hour line. Never carries hour_result."""

    branch: str
    time_range: str
    cung_display: str
    display: str

    def to_dict(self) -> dict[str, Any]:
        """Serialize a compatible-hour row."""
        return {
            "branch": self.branch,
            "time_range": self.time_range,
            "cung_display": self.cung_display,
            "display": self.display,
        }


@dataclass(frozen=True, slots=True)
class CompatibleHoursNode:
    """Compatible-hour list under a recommendation."""

    title: str
    rows: tuple[CompatibleHourRowNode, ...]
    icon_token: str

    def to_dict(self) -> dict[str, Any]:
        """Serialize compatible hours."""
        return {
            "title": self.title,
            "rows": [row.to_dict() for row in self.rows],
            "icon_token": self.icon_token,
        }


@dataclass(frozen=True, slots=True)
class PositiveTimeItemNode:
    """One positive khắc slot with its parent hour branch."""

    branch_display: str
    time_range: str
    result: str

    def to_dict(self) -> dict[str, Any]:
        """Serialize a positive-time item."""
        return {
            "branch_display": self.branch_display,
            "time_range": self.time_range,
            "result": self.result,
        }


@dataclass(frozen=True, slots=True)
class PositiveTimeGroupNode:
    """One positive class group. Empty groups are omitted by the builder."""

    label: str
    items: tuple[PositiveTimeItemNode, ...]

    def to_dict(self) -> dict[str, Any]:
        """Serialize a positive-time group."""
        return {
            "label": self.label,
            "items": [item.to_dict() for item in self.items],
        }


@dataclass(frozen=True, slots=True)
class PositiveTimesNode:
    """Grouped positive khắc. Only non-empty groups appear."""

    title: str
    groups: tuple[PositiveTimeGroupNode, ...]

    def to_dict(self) -> dict[str, Any]:
        """Serialize positive times."""
        return {
            "title": self.title,
            "groups": [group.to_dict() for group in self.groups],
        }


@dataclass(frozen=True, slots=True)
class RecommendationNode:
    """One recommendation block. Prefer keep_together."""

    rank: int
    date_header: DateHeaderNode
    day_information: DayInformationNode
    compatible_hours: CompatibleHoursNode
    positive_times: PositiveTimesNode
    pagination: PaginationHints

    def presentation_field_keys(self) -> tuple[str, ...]:
        """Public day-field order for this block."""
        return (
            "solar_date",
            "lunar_date",
            "day_result",
            *(row.key for row in self.day_information.rows),
        )

    def to_dict(self) -> dict[str, Any]:
        """Serialize a recommendation block."""
        return {
            "rank": self.rank,
            "date_header": self.date_header.to_dict(),
            "day_information": self.day_information.to_dict(),
            "compatible_hours": self.compatible_hours.to_dict(),
            "positive_times": self.positive_times.to_dict(),
            "pagination": self.pagination.to_dict(),
            "presentation_field_keys": list(self.presentation_field_keys()),
        }


@dataclass(frozen=True, slots=True)
class EmptyRecommendationsNode:
    """Approved empty-state copy. Dormant while P6-01 rejects zero dates."""

    section_id: str
    message: str

    def to_dict(self) -> dict[str, Any]:
        """Serialize empty state."""
        return {"section_id": self.section_id, "message": self.message}


@dataclass(frozen=True, slots=True)
class GuidanceItemNode:
    """Educational guidance row."""

    label: str
    text: str

    def to_dict(self) -> dict[str, Any]:
        """Serialize a guidance item."""
        return {"label": self.label, "text": self.text}


@dataclass(frozen=True, slots=True)
class GuidanceSectionNode:
    """Educational positive-class notes."""

    section_id: str
    title: str
    items: tuple[GuidanceItemNode, ...]

    def to_dict(self) -> dict[str, Any]:
        """Serialize guidance."""
        return {
            "section_id": self.section_id,
            "title": self.title,
            "items": [item.to_dict() for item in self.items],
        }


@dataclass(frozen=True, slots=True)
class FooterSectionNode:
    """Minimal footer identity."""

    section_id: str
    generated_by_label: str
    generator: str
    product: str
    report_version: str

    def to_dict(self) -> dict[str, Any]:
        """Serialize footer."""
        return {
            "section_id": self.section_id,
            "generated_by_label": self.generated_by_label,
            "generator": self.generator,
            "product": self.product,
            "report_version": self.report_version,
        }


@dataclass(frozen=True, slots=True)
class DateSelectionRenderTree:
    """Read-only render tree shared by future PDF and DOCX exporters."""

    header: HeaderSectionNode
    person: PersonSectionNode
    search_period: SearchPeriodSectionNode
    recommendations: tuple[RecommendationNode, ...]
    recommendations_title: str
    empty_state: EmptyRecommendationsNode | None
    guidance: GuidanceSectionNode
    footer: FooterSectionNode
    section_order: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        """Serialize the render tree."""
        return {
            "header": self.header.to_dict(),
            "person": self.person.to_dict(),
            "search_period": self.search_period.to_dict(),
            "recommendations": [item.to_dict() for item in self.recommendations],
            "recommendations_title": self.recommendations_title,
            "empty_state": None if self.empty_state is None else self.empty_state.to_dict(),
            "guidance": self.guidance.to_dict(),
            "footer": self.footer.to_dict(),
            "section_order": list(self.section_order),
        }
