"""Resolve render asset references. No binary loading."""

from __future__ import annotations

from typing import Mapping

from engines.report_engine.rendering.render_model import RenderAssetRef
from engines.report_engine.rendering.rendering_context import RenderingContext


class AssetEmbedder:
    """Publish embed references for layout assets. Never loads bytes."""

    def embed(self, context: RenderingContext) -> tuple[RenderAssetRef, ...]:
        """Map layout assets to deterministic embed refs."""
        layout = context.layout_snapshot()
        rows = [item for item in layout.get("assets") or () if isinstance(item, Mapping)]
        embedded: list[RenderAssetRef] = []
        for item in rows:
            asset_id = str(item.get("asset_id") or "")
            if not asset_id:
                continue
            source_ref = str(item.get("source_ref") or "")
            embedded.append(
                RenderAssetRef(
                    asset_id=asset_id,
                    asset_kind=str(item.get("asset_kind") or ""),
                    source_ref=source_ref,
                    embed_ref=f"embed://{asset_id}",
                )
            )
        return tuple(embedded)
