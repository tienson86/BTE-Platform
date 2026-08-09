"""Deterministic in-memory PDF renderer. No filesystem writes."""

from __future__ import annotations

import json

from engines.report_engine.rendering.render_model import RenderArtifact, RenderModel
from engines.report_engine.rendering.renderer_registry import MIME_PDF, RENDERER_PDF


class PdfRenderer:
    """Render the canonical model as an in-memory PDF artifact envelope."""

    renderer_id: str = RENDERER_PDF
    mime_type: str = MIME_PDF

    def render(self, model: RenderModel) -> RenderArtifact:
        """Return a deterministic PDF-targeted memory object."""
        payload = json.dumps(
            {"format": RENDERER_PDF, "model": model.to_dict()},
            sort_keys=True,
            ensure_ascii=False,
        )
        return RenderArtifact(
            artifact_id="ART-pdf-1",
            renderer=self.renderer_id,
            mime_type=self.mime_type,
            content=payload,
            metadata={"format": RENDERER_PDF, "filesystem": False, "printing": False},
            assets=tuple(item.to_dict() for item in model.assets),
        )
