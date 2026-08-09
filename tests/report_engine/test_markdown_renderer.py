"""RE-3 Markdown renderer tests."""

from __future__ import annotations

from engines.report_engine.rendering.asset_embedder import AssetEmbedder
from engines.report_engine.rendering.markdown_renderer import MarkdownRenderer
from engines.report_engine.rendering.render_model import build_render_model
from engines.report_engine.rendering.rendering_context import build_rendering_context
from tests.report_engine.re3_support import assemble_canonical_layout


def test_markdown_renderer_is_pure_markdown() -> None:
    """Markdown renderer emits heading hierarchy from layout identities."""
    layout = assemble_canonical_layout()
    context = build_rendering_context(layout=layout, renderer_id="markdown")
    model = build_render_model(context, assets=AssetEmbedder().embed(context))
    artifact = MarkdownRenderer().render(model)
    assert artifact.mime_type == "text/markdown"
    assert artifact.content.startswith("# DOC-report-1\n")
    assert "## LSEC-cover" in artifact.content
    assert "<html" not in artifact.content
