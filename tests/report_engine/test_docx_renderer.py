"""RE-3 DOCX renderer tests."""

from __future__ import annotations

from engines.report_engine.rendering.asset_embedder import AssetEmbedder
from engines.report_engine.rendering.docx_renderer import DocxRenderer
from engines.report_engine.rendering.render_model import build_render_model
from engines.report_engine.rendering.rendering_context import build_rendering_context
from tests.report_engine.re3_support import assemble_canonical_layout


def test_docx_renderer_returns_memory_artifact() -> None:
    """DOCX renderer publishes mime-typed content without filesystem writes."""
    layout = assemble_canonical_layout()
    context = build_rendering_context(layout=layout, renderer_id="docx")
    model = build_render_model(context, assets=AssetEmbedder().embed(context))
    artifact = DocxRenderer().render(model)
    assert artifact.renderer == "docx"
    assert artifact.mime_type.endswith("wordprocessingml.document")
    assert artifact.artifact_id == "ART-docx-1"
    assert '"format": "docx"' in artifact.content
    assert artifact.metadata["filesystem"] is False
