"""RE-3 export manager tests."""

from __future__ import annotations

import pytest

from engines.report_engine.rendering.asset_embedder import AssetEmbedder
from engines.report_engine.rendering.export_manager import ExportManager
from engines.report_engine.rendering.render_model import build_render_model
from engines.report_engine.rendering.rendering_context import RenderingError, build_rendering_context
from tests.report_engine.re3_support import assemble_canonical_layout


def test_export_manager_selects_renderer_without_persistence() -> None:
    """Export manager returns an in-memory artifact for an enabled renderer."""
    layout = assemble_canonical_layout()
    context = build_rendering_context(layout=layout, renderer_id="html")
    model = build_render_model(context, assets=AssetEmbedder().embed(context))
    artifact = ExportManager().export(renderer_id="html", model=model)
    assert artifact.renderer == "html"
    assert artifact.mime_type == "text/html"
    assert "path" not in artifact.to_dict()
    assert artifact.metadata.get("web_server") is False


def test_export_manager_rejects_disabled_renderer() -> None:
    """Future renderers remain registered but cannot export."""
    layout = assemble_canonical_layout()
    context = build_rendering_context(layout=layout, renderer_id="xlsx")
    model = build_render_model(context, assets=AssetEmbedder().embed(context))
    with pytest.raises(RenderingError, match="renderer_disabled:xlsx"):
        ExportManager().export(renderer_id="xlsx", model=model)
