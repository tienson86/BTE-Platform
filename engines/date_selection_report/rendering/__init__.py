"""PACK 06 Date Selection presentation layer (P6-02)."""

from engines.date_selection_report.rendering.builders import (
    CompatibleHoursSectionBuilder,
    EmptyRecommendationsSectionBuilder,
    FooterSectionBuilder,
    GuidanceSectionBuilder,
    HeaderSectionBuilder,
    PersonSectionBuilder,
    PositiveTimesSectionBuilder,
    RecommendationSectionBuilder,
    SearchPeriodSectionBuilder,
)
from engines.date_selection_report.rendering.context import (
    DateSelectionRenderContext,
    LayoutConfiguration,
    PageConfiguration,
    create_render_context,
)
from engines.date_selection_report.rendering.nodes import DateSelectionRenderTree
from engines.date_selection_report.rendering.tree import (
    DateSelectionRenderTreeBuilder,
    build_render_tree,
    build_render_tree_from_report,
)

__all__ = [
    "CompatibleHoursSectionBuilder",
    "DateSelectionRenderContext",
    "DateSelectionRenderTree",
    "DateSelectionRenderTreeBuilder",
    "EmptyRecommendationsSectionBuilder",
    "FooterSectionBuilder",
    "GuidanceSectionBuilder",
    "HeaderSectionBuilder",
    "LayoutConfiguration",
    "PageConfiguration",
    "PersonSectionBuilder",
    "PositiveTimesSectionBuilder",
    "RecommendationSectionBuilder",
    "SearchPeriodSectionBuilder",
    "build_render_tree",
    "build_render_tree_from_report",
    "create_render_context",
]
