"""RE-3 JSON renderer tests."""

from __future__ import annotations

import json

from engines.report_engine.rendering.asset_embedder import AssetEmbedder
from engines.report_engine.rendering.json_renderer import JsonRenderer
from engines.report_engine.rendering.render_model import build_render_model
from engines.report_engine.rendering.rendering_context import build_rendering_context
from tests.report_engine.re3_support import assemble_canonical_layout


def test_json_renderer_is_machine_readable_and_sorted() -> None:
    """JSON renderer publishes canonical sorted JSON of the render model."""
    layout = assemble_canonical_layout()
    context = build_rendering_context(layout=layout, renderer_id="json")
    model = build_render_model(context, assets=AssetEmbedder().embed(context))
    artifact = JsonRenderer().render(model)
    assert artifact.mime_type == "application/json"
    decoded = json.loads(artifact.content)
    assert decoded["format"] == "json"
    assert decoded["model"]["document_id"] == "DOC-report-1"
    assert decoded["model"]["styles"]["theme_id"] == "bte.report.theme.v1"
    assert artifact.metadata["machine_readable"] is True
