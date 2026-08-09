"""RE-2 layout resolver tests."""

from __future__ import annotations

from engines.report_engine.layout.block_builder import BlockBuilder
from engines.report_engine.layout.document_builder import DocumentBuilder
from engines.report_engine.layout.layout_context import build_layout_context
from engines.report_engine.layout.layout_resolver import LayoutResolver
from engines.report_engine.layout.section_builder import SectionBuilder
from tests.report_engine.re2_support import assemble_layout_inputs


def test_layout_resolver_emits_hierarchy_metadata_only() -> None:
    """Page breaks and keep-together are metadata, not rendered pages."""
    payload = assemble_layout_inputs()
    context = build_layout_context(
        report_context=payload["report_context"],
        interpretation_result=payload["interpretation_result"],
    )
    document = DocumentBuilder().build(context)
    sections = SectionBuilder().build(context)
    blocks = BlockBuilder().build(sections)
    layout = LayoutResolver().resolve(document, sections, blocks)
    assert layout.page_hierarchy[0] == "PAGE-cover"
    assert layout.column_metadata["columns"] == 1
    assert layout.widows_orphans == {"widows": 2, "orphans": 2}
    assert layout.page_breaks
    assert layout.keep_together
    encoded = layout.to_dict()
    assert "html" not in encoded
    assert "pdf" not in encoded
