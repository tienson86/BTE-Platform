"""RE-3 PDF renderer tests."""

from __future__ import annotations

from engines.report_engine.rendering.asset_embedder import AssetEmbedder
from engines.report_engine.rendering.pdf_renderer import PdfRenderer
from engines.report_engine.rendering.render_model import build_render_model
from engines.report_engine.rendering.rendering_context import build_rendering_context
from tests.report_engine.re3_support import assemble_canonical_layout


def test_pdf_renderer_returns_memory_artifact() -> None:
    """PDF renderer publishes mime-typed content without filesystem writes."""
    layout = assemble_canonical_layout()
    context = build_rendering_context(layout=layout, renderer_id="pdf")
    model = build_render_model(context, assets=AssetEmbedder().embed(context))
    artifact = PdfRenderer().render(model)
    assert artifact.renderer == "pdf"
    assert artifact.mime_type == "application/pdf"
    assert artifact.artifact_id == "ART-pdf-1"
    assert '"format": "pdf"' in artifact.content
    assert artifact.metadata["filesystem"] is False
    assert artifact.metadata["printing"] is False
    assert "path" not in artifact.to_dict()
