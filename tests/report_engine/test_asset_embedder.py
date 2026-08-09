"""RE-3 asset embedder tests."""

from __future__ import annotations

from engines.report_engine.rendering.asset_embedder import AssetEmbedder
from engines.report_engine.rendering.rendering_context import build_rendering_context
from tests.report_engine.re3_support import assemble_canonical_layout


def test_asset_embedder_uses_references_only() -> None:
    """Embedder publishes embed:// refs and never loads binaries."""
    layout = assemble_canonical_layout()
    context = build_rendering_context(layout=layout, renderer_id="json")
    assets = AssetEmbedder().embed(context)
    assert assets
    kinds = {item.asset_kind for item in assets}
    assert {"logo", "chart", "icon", "image", "attachment"} <= kinds
    for item in assets:
        encoded = item.to_dict()
        assert encoded["embed_ref"].startswith("embed://")
        assert "bytes" not in encoded
        assert "binary_content" not in encoded
