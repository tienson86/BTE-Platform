"""Section builders. Format presentation values only."""

from __future__ import annotations

from engines.date_selection_report.exceptions import DateSelectionReportTemplateError
from engines.date_selection_report.models import (
    CompatibleHourReportData,
    GuidanceReportData,
    Metadata,
    PersonReportData,
    RecommendedDateReportData,
    SearchPeriodReportData,
)
from engines.date_selection_report.rendering.formatters import (
    element_color_token,
    format_compatible_hour_row,
    format_cung,
    format_hour_branch,
    format_lunar_date,
)
from engines.date_selection_report.rendering.labels import (
    EMPTY_STATE_MESSAGE,
    LABELS,
    POSITIVE_GROUP_ORDER,
)
from engines.date_selection_report.rendering.nodes import (
    CompatibleHourRowNode,
    CompatibleHoursNode,
    DateHeaderNode,
    DayInformationNode,
    EmptyRecommendationsNode,
    FieldRow,
    FooterSectionNode,
    GuidanceItemNode,
    GuidanceSectionNode,
    HeaderSectionNode,
    PaginationHints,
    PersonSectionNode,
    PositiveTimeGroupNode,
    PositiveTimeItemNode,
    PositiveTimesNode,
    RecommendationNode,
    SearchPeriodSectionNode,
)
from engines.date_selection_report.rendering.tokens import (
    ICON_TOKENS,
    TYPOGRAPHY_TOKENS,
)


def _row(key: str, value: str, *, color_token: str | None = None) -> FieldRow:
    return FieldRow(
        key=key,
        label=LABELS[key],
        value=value,
        typography_token=TYPOGRAPHY_TOKENS["value"],
        color_token=color_token,
    )


class HeaderSectionBuilder:
    """Build the report header from metadata."""

    def build(self, metadata: Metadata) -> HeaderSectionNode:
        """Return title, subtitle, and secondary identity fields."""
        return HeaderSectionNode(
            section_id="header",
            title=LABELS["report_title"],
            subtitle=LABELS["subtitle"],
            generated_at=metadata.generated_at,
            report_id=metadata.report_id,
            typography_token=TYPOGRAPHY_TOKENS["report_title"],
        )


class PersonSectionBuilder:
    """Build the person card. Combines Cung for display only."""

    def build(self, person: PersonReportData) -> PersonSectionNode:
        """Return person rows in canonical order."""
        cung_display = format_cung(person.cung_phi, person.cung_element)
        rows = (
            _row("full_name", person.full_name),
            _row("gender", person.gender),
            _row("birth_solar", person.birth_solar),
            _row("birth_lunar", person.birth_lunar),
            _row("year_ganzhi", person.year_ganzhi),
            _row("nayin", person.nayin, color_token=element_color_token(person.nayin)),
            _row("cung_phi", cung_display),
            _row("trach_group", person.trach_group),
        )
        return PersonSectionNode(
            section_id="person",
            title=LABELS["section_person"],
            rows=rows,
            cung_display=cung_display,
            icon_token=ICON_TOKENS["person"],
        )


class SearchPeriodSectionBuilder:
    """Build the search-period card."""

    def build(
        self,
        period: SearchPeriodReportData,
        recommendation_count: int,
    ) -> SearchPeriodSectionNode:
        """Return month display and recommendation count."""
        return SearchPeriodSectionNode(
            section_id="search_period",
            title=LABELS["section_search"],
            month_label=LABELS["search_month"],
            month_display=period.display,
            recommendation_count_label=LABELS["recommendation_count"],
            recommendation_count=str(recommendation_count),
            explanation=LABELS["search_explanation"],
            icon_token=ICON_TOKENS["calendar"],
        )


class CompatibleHoursSectionBuilder:
    """Build compatible-hour rows. Does not filter or rank hours."""

    def build(self, hours: tuple[CompatibleHourReportData, ...]) -> CompatibleHoursNode:
        """Preserve source hour order."""
        rows = tuple(
            CompatibleHourRowNode(
                branch=hour.branch,
                time_range=hour.time_range,
                cung_display=format_cung(hour.cung, hour.cung_element),
                display=format_compatible_hour_row(
                    hour.branch,
                    hour.time_range,
                    format_cung(hour.cung, hour.cung_element),
                ),
            )
            for hour in hours
        )
        return CompatibleHoursNode(
            title=LABELS["compatible_hours"],
            rows=rows,
            icon_token=ICON_TOKENS["clock"],
        )


class PositiveTimesSectionBuilder:
    """Group positive khắc for display. Does not calculate khắc."""

    def build(self, hours: tuple[CompatibleHourReportData, ...]) -> PositiveTimesNode:
        """Group existing slots as Đại An → Tốc Hỷ → Tiểu Cát. Hide empty groups."""
        buckets: dict[str, list[PositiveTimeItemNode]] = {
            name: [] for name in POSITIVE_GROUP_ORDER
        }
        for hour in hours:
            for slot in hour.positive_ke:
                if slot.result not in buckets:
                    raise DateSelectionReportTemplateError(
                        f"disallowed positive class: {slot.result!r}"
                    )
                buckets[slot.result].append(
                    PositiveTimeItemNode(
                        branch_display=format_hour_branch(hour.branch),
                        time_range=slot.time_range,
                        result=slot.result,
                    )
                )
        groups = tuple(
            PositiveTimeGroupNode(label=name, items=tuple(items))
            for name, items in buckets.items()
            if items
        )
        return PositiveTimesNode(title=LABELS["positive_times"], groups=groups)


class RecommendationSectionBuilder:
    """Build one recommendation block from already-validated data."""

    def __init__(self) -> None:
        self._hours = CompatibleHoursSectionBuilder()
        self._positive = PositiveTimesSectionBuilder()

    def build(self, recommendation: RecommendedDateReportData) -> RecommendationNode:
        """Preserve day-field order. Prefer keep_together."""
        cung_display = format_cung(recommendation.cung, recommendation.cung_element)
        day_information = DayInformationNode(
            rows=(
                _row("year_ganzhi", recommendation.year_ganzhi),
                _row("month_ganzhi", recommendation.month_ganzhi),
                _row("day_ganzhi", recommendation.day_ganzhi),
                _row(
                    "nayin",
                    recommendation.nayin,
                    color_token=element_color_token(recommendation.nayin),
                ),
                _row("cung_phi", cung_display),
                _row("trach_group", recommendation.trach_group),
            ),
            cung_display=cung_display,
        )
        return RecommendationNode(
            rank=recommendation.rank,
            date_header=DateHeaderNode(
                solar_date=recommendation.solar_date,
                lunar_date=recommendation.lunar_date,
                lunar_display=format_lunar_date(recommendation.lunar_date),
                day_result=recommendation.day_result,
                rank=recommendation.rank,
            ),
            day_information=day_information,
            compatible_hours=self._hours.build(recommendation.compatible_hours),
            positive_times=self._positive.build(recommendation.compatible_hours),
            pagination=PaginationHints(
                keep_together=True,
                do_not_split=("date_header", "day_information"),
            ),
        )


class GuidanceSectionBuilder:
    """Build educational guidance from the report model."""

    def build(self, guidance: GuidanceReportData) -> GuidanceSectionNode:
        """Preserve model item order. Do not invent promises."""
        items = tuple(
            GuidanceItemNode(label=item.label, text=item.text) for item in guidance.items
        )
        return GuidanceSectionNode(
            section_id="guidance",
            title=LABELS["section_guidance"],
            items=items,
        )


class FooterSectionBuilder:
    """Build the footer identity block."""

    def build(self, metadata: Metadata) -> FooterSectionNode:
        """Return generator and schema version. No page numbers yet."""
        return FooterSectionNode(
            section_id="footer",
            generated_by_label=LABELS["footer_generated_by"],
            generator=LABELS["subtitle"],
            product=LABELS["footer_product"],
            report_version=metadata.report_schema_version,
        )


class EmptyRecommendationsSectionBuilder:
    """Approved empty-state node. Dormant under current P6-01 validation."""

    def build(self) -> EmptyRecommendationsNode:
        """Return the canonical empty-state message without fabricating dates."""
        return EmptyRecommendationsNode(
            section_id="empty_recommendations",
            message=EMPTY_STATE_MESSAGE,
        )
