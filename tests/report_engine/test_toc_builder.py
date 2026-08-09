"""RE-2 TOC builder tests."""

from __future__ import annotations

from engines.report_engine.layout.layout_context import build_layout_context
from engines.report_engine.layout.section_builder import SectionBuilder
from engines.report_engine.layout.toc_builder import TOC_ID, TocBuilder
from tests.report_engine.re2_support import assemble_layout_inputs


def test_toc_builder_is_hierarchy_only() -> None:
    """TOC lists section identities without page numbers or links."""
    payload = assemble_layout_inputs()
    context = build_layout_context(
        report_context=payload["report_context"],
        interpretation_result=payload["interpretation_result"],
    )
    toc = TocBuilder().build(SectionBuilder().build(context))
    assert toc.toc_id == TOC_ID
    assert toc.entry_ids[0] == "TOC-cover"
    assert toc.entries[-1].module_id == "summary"
    encoded = toc.to_dict()
    assert "page_number" not in encoded
    assert "href" not in encoded
    assert "hyperlink" not in encoded
    for entry in encoded["entries"]:
        assert entry["depth"] == 1
        assert "page_number" not in entry
