"""RE-2 asset resolver tests."""

from __future__ import annotations

from engines.report_engine.layout.asset_resolver import AssetResolver
from engines.report_engine.layout.block_builder import BlockBuilder
from engines.report_engine.layout.layout_context import build_layout_context
from engines.report_engine.layout.section_builder import SectionBuilder
from tests.report_engine.re2_support import assemble_layout_inputs


def test_asset_resolver_publishes_references_without_binaries() -> None:
    """Logo, chart, icon, image, and attachment ids are references only."""
    payload = assemble_layout_inputs()
    context = build_layout_context(
        report_context=payload["report_context"],
        interpretation_result=payload["interpretation_result"],
    )
    blocks = BlockBuilder().build(SectionBuilder().build(context))
    assets = AssetResolver().resolve(context, blocks)
    kinds = {item.asset_kind for item in assets}
    assert kinds == {"image", "logo", "chart", "icon", "attachment"}
    assert all(item.status == "resolved" for item in assets)
    for item in assets:
        encoded = item.to_dict()
        assert encoded["source_ref"]
        assert "bytes" not in encoded
        assert "binary_content" not in encoded
