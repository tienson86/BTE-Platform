"""A. RenderContext construction."""

from __future__ import annotations

from engines.date_selection_report.models import DateSelectionReportModel
from engines.date_selection_report.rendering.context import create_render_context
from engines.date_selection_report.rendering.tokens import THEME_REF
from engines.report_engine.layout.theme_resolver import THEME_ID


def test_render_context_holds_report_by_reference(
    presentation_model: DateSelectionReportModel,
) -> None:
    context = create_render_context(presentation_model)
    assert context.report is presentation_model
    assert context.locale == "vi-VN"
    assert context.theme_id == THEME_ID
    assert context.theme_id == THEME_REF["theme_id"]
    assert context.template_version == "1.0"
    assert context.page.paper == "A4"
    assert context.page.orientation == "portrait"
    assert context.layout.section_order == (
        "header",
        "person",
        "search_period",
        "recommendations",
        "guidance",
        "footer",
    )
    payload = context.to_dict()
    assert "recommendations" not in payload
    assert payload["report_id"] == presentation_model.metadata.report_id
