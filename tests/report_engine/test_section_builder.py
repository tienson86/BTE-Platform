"""RE-2 section builder tests."""

from __future__ import annotations

from engines.report_engine.foundation_constants import CANONICAL_MODULE_ORDER
from engines.report_engine.layout.layout_context import build_layout_context
from engines.report_engine.layout.section_builder import SectionBuilder
from tests.report_engine.re2_support import assemble_layout_inputs


def test_section_builder_maps_modules_without_formatting() -> None:
    """Every registered report module becomes a layout section."""
    payload = assemble_layout_inputs()
    context = build_layout_context(
        report_context=payload["report_context"],
        interpretation_result=payload["interpretation_result"],
    )
    sections = SectionBuilder().build(context)
    assert [item.module_id for item in sections] == list(CANONICAL_MODULE_ORDER)
    overview = next(item for item in sections if item.module_id == "overview")
    assert overview.source_section_ids == ("SEC-overview",)
    assert overview.status == "assembled"
    for item in sections:
        encoded = item.to_dict()
        assert "css" not in encoded
        assert "html" not in encoded
        assert "typography" not in encoded
