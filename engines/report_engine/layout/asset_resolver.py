"""Resolve layout asset references. No binary loading."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Sequence

from engines.report_engine.layout.block_builder import LayoutBlock
from engines.report_engine.layout.layout_context import LayoutContext
from engines.report_engine.layout.theme_resolver import ICON_SET_ID

ASSET_IMAGE = "image"
ASSET_LOGO = "logo"
ASSET_CHART = "chart"
ASSET_ICON = "icon"
ASSET_ATTACHMENT = "attachment"


@dataclass(slots=True)
class LayoutAsset:
    """Asset identity and source reference. No bytes."""

    asset_id: str
    asset_kind: str
    source_ref: str
    status: str

    def to_dict(self) -> dict[str, Any]:
        """Serialize one asset reference."""
        return {
            "asset_id": self.asset_id,
            "asset_kind": self.asset_kind,
            "source_ref": self.source_ref,
            "status": self.status,
        }


class AssetResolver:
    """Publish logo, chart, icon, image, and attachment references."""

    def resolve(
        self,
        context: LayoutContext,
        blocks: Sequence[LayoutBlock],
    ) -> tuple[LayoutAsset, ...]:
        """Resolve declared and catalog asset identities against upstream snapshots."""
        analysis = context.analysis_snapshot()
        interpretation = context.interpretation_snapshot()
        chart_status = "resolved" if "seasonal" in analysis else "missing"
        attachment_status = "resolved" if interpretation else "missing"
        catalog = (
            LayoutAsset("AST-logo", ASSET_LOGO, "brand.logo", "resolved"),
            LayoutAsset("AST-image-cover", ASSET_IMAGE, "brand.cover_mark", "resolved"),
            LayoutAsset("AST-icon-cover", ASSET_ICON, ICON_SET_ID, "resolved"),
            LayoutAsset("AST-chart-chart", ASSET_CHART, "analysis.seasonal", chart_status),
            LayoutAsset(
                "AST-attachment-audit",
                ASSET_ATTACHMENT,
                "interpretation.audit",
                attachment_status,
            ),
        )
        declared = {asset_id for item in blocks for asset_id in item.asset_ids}
        extras = tuple(
            LayoutAsset(asset_id, ASSET_CHART, "analysis.seasonal", "missing")
            for asset_id in sorted(declared)
            if asset_id not in {item.asset_id for item in catalog}
        )
        return catalog + extras
