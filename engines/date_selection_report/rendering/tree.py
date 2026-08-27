"""Assemble DateSelectionRenderTree from a validated report model."""

from __future__ import annotations

from engines.date_selection_report.models import DateSelectionReportModel
from engines.date_selection_report.rendering.builders import (
    EmptyRecommendationsSectionBuilder,
    FooterSectionBuilder,
    GuidanceSectionBuilder,
    HeaderSectionBuilder,
    PersonSectionBuilder,
    RecommendationSectionBuilder,
    SearchPeriodSectionBuilder,
)
from engines.date_selection_report.rendering.context import (
    DateSelectionRenderContext,
    create_render_context,
)
from engines.date_selection_report.rendering.labels import LABELS
from engines.date_selection_report.rendering.nodes import DateSelectionRenderTree
from engines.date_selection_report.rendering.tokens import SECTION_ORDER
from engines.date_selection_report.templates.validation import validate_render_tree


class DateSelectionRenderTreeBuilder:
    """Section-by-section tree assembly. Never mutates the report model."""

    def __init__(self) -> None:
        self._header = HeaderSectionBuilder()
        self._person = PersonSectionBuilder()
        self._search = SearchPeriodSectionBuilder()
        self._recommendation = RecommendationSectionBuilder()
        self._guidance = GuidanceSectionBuilder()
        self._footer = FooterSectionBuilder()
        self._empty = EmptyRecommendationsSectionBuilder()

    def build(self, context: DateSelectionRenderContext) -> DateSelectionRenderTree:
        """Build and validate a read-only render tree."""
        report = context.report
        recommendations = tuple(
            self._recommendation.build(item) for item in report.recommendations
        )
        empty_state = None if recommendations else self._empty.build()
        tree = DateSelectionRenderTree(
            header=self._header.build(report.metadata),
            person=self._person.build(report.person),
            search_period=self._search.build(
                report.search_period,
                len(report.recommendations),
            ),
            recommendations=recommendations,
            recommendations_title=LABELS["section_recommendations"],
            empty_state=empty_state,
            guidance=self._guidance.build(report.guidance),
            footer=self._footer.build(report.metadata),
            section_order=context.layout.section_order or SECTION_ORDER,
        )
        validate_render_tree(tree)
        return tree


def build_render_tree(context: DateSelectionRenderContext) -> DateSelectionRenderTree:
    """Public entry: ReportModel via context → render tree."""
    return DateSelectionRenderTreeBuilder().build(context)


def build_render_tree_from_report(
    report: DateSelectionReportModel,
) -> DateSelectionRenderTree:
    """Convenience wrapper from a validated report model."""
    return build_render_tree(create_render_context(report))
