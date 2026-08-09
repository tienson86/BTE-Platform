"""Canonical JSON renderer. Machine-readable only."""

from __future__ import annotations

import json

from engines.report_engine.rendering.render_model import RenderArtifact, RenderModel
from engines.report_engine.rendering.renderer_registry import MIME_JSON, RENDERER_JSON


class JsonRenderer:
    """Render the canonical model as sorted JSON."""

    renderer_id: str = RENDERER_JSON
    mime_type: str = MIME_JSON

    def render(self, model: RenderModel) -> RenderArtifact:
        """Return deterministic machine-readable JSON."""
        payload = json.dumps(
            {"format": RENDERER_JSON, "model": model.to_dict()},
            sort_keys=True,
            ensure_ascii=False,
        )
        return RenderArtifact(
            artifact_id="ART-json-1",
            renderer=self.renderer_id,
            mime_type=self.mime_type,
            content=payload,
            metadata={"format": RENDERER_JSON, "machine_readable": True},
            assets=tuple(item.to_dict() for item in model.assets),
        )
