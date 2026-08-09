"""RE-3 HTML renderer tests."""

from __future__ import annotations

from engines.report_engine.rendering.asset_embedder import AssetEmbedder
from engines.report_engine.rendering.html_renderer import HtmlRenderer
from engines.report_engine.rendering.render_model import build_render_model
from engines.report_engine.rendering.rendering_context import build_rendering_context
from tests.report_engine.re3_support import assemble_canonical_layout


def test_html_renderer_is_pure_html_without_server() -> None:
    """HTML renderer emits a document string with identities only."""
    layout = assemble_canonical_layout()
    context = build_rendering_context(layout=layout, renderer_id="html")
    model = build_render_model(context, assets=AssetEmbedder().embed(context))
    artifact = HtmlRenderer().render(model)
    assert artifact.mime_type == "text/html"
    assert artifact.content.startswith("<!DOCTYPE html>")
    assert 'data-document="DOC-report-1"' in artifact.content
    assert "<style" not in artifact.content
    assert artifact.metadata["web_server"] is False
