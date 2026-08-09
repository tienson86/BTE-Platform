"""Deterministic in-memory DOCX renderer. No filesystem writes."""

from __future__ import annotations

import json

from engines.report_engine.rendering.render_model import RenderArtifact, RenderModel
from engines.report_engine.rendering.renderer_registry import MIME_DOCX, RENDERER_DOCX


class DocxRenderer:
    """Render the canonical model as an in-memory DOCX artifact envelope."""

    renderer_id: str = RENDERER_DOCX
    mime_type: str = MIME_DOCX

    def render(self, model: RenderModel) -> RenderArtifact:
        """Return a deterministic DOCX-targeted memory object."""
        payload = json.dumps(
            {"format": RENDERER_DOCX, "model": model.to_dict()},
            sort_keys=True,
            ensure_ascii=False,
        )
        return RenderArtifact(
            artifact_id="ART-docx-1",
            renderer=self.renderer_id,
            mime_type=self.mime_type,
            content=payload,
            metadata={"format": RENDERER_DOCX, "filesystem": False, "printing": False},
            assets=tuple(item.to_dict() for item in model.assets),
        )
