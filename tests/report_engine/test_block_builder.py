"""RE-2 block builder tests."""

from __future__ import annotations

from engines.report_engine.layout.block_builder import SUPPORTED_BLOCK_TYPES, BlockBuilder
from engines.report_engine.layout.layout_context import build_layout_context
from engines.report_engine.layout.section_builder import SectionBuilder
from tests.report_engine.re2_support import assemble_layout_inputs


def test_block_builder_emits_supported_types_without_rendering() -> None:
    """All declared logical block types appear as identities only."""
    payload = assemble_layout_inputs()
    context = build_layout_context(
        report_context=payload["report_context"],
        interpretation_result=payload["interpretation_result"],
    )
    sections = SectionBuilder().build(context)
    blocks = BlockBuilder().build(sections)
    types = {item.block_type for item in blocks}
    assert types == set(SUPPORTED_BLOCK_TYPES)
    for item in blocks:
        encoded = item.to_dict()
        assert encoded["source_refs"]
        assert "markdown" not in encoded
        assert "html" not in encoded
        assert "pdf" not in encoded
