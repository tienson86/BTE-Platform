"""Deterministic block builder. Logical block types only. No rendering."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Sequence

from engines.report_engine.layout.section_builder import LayoutSection

BLOCK_TEXT = "text"
BLOCK_TABLE = "table"
BLOCK_CHART_PLACEHOLDER = "chart_placeholder"
BLOCK_IMAGE_PLACEHOLDER = "image_placeholder"
BLOCK_DIVIDER = "divider"
BLOCK_LIST = "list"
BLOCK_QUOTE = "quote"
BLOCK_REFERENCE = "reference"
BLOCK_NOTE = "note"
BLOCK_WARNING = "warning"

SUPPORTED_BLOCK_TYPES: tuple[str, ...] = (
    BLOCK_TEXT,
    BLOCK_TABLE,
    BLOCK_CHART_PLACEHOLDER,
    BLOCK_IMAGE_PLACEHOLDER,
    BLOCK_DIVIDER,
    BLOCK_LIST,
    BLOCK_QUOTE,
    BLOCK_REFERENCE,
    BLOCK_NOTE,
    BLOCK_WARNING,
)

_MODULE_BLOCKS: dict[str, tuple[tuple[str, str], ...]] = {
    "cover": ((BLOCK_TEXT, "title.report"), (BLOCK_DIVIDER, "layout.divider"), (BLOCK_NOTE, "report.metadata")),
    "overview": ((BLOCK_TEXT, "interpretation.overview"), (BLOCK_REFERENCE, "decision.final_useful_god")),
    "chart": ((BLOCK_CHART_PLACEHOLDER, "analysis.seasonal"),),
    "analysis": ((BLOCK_TABLE, "analysis.stage_order"), (BLOCK_TEXT, "analysis.strength")),
    "decision": ((BLOCK_LIST, "decision.final_favorable_gods"), (BLOCK_WARNING, "decision.final_unfavorable_gods")),
    "luck": ((BLOCK_NOTE, "luck.overall_luck_result"), (BLOCK_TEXT, "interpretation.luck")),
    "interpretation": ((BLOCK_QUOTE, "interpretation.canonical_interpretation"), (BLOCK_REFERENCE, "interpretation.sections")),
    "appendix": ((BLOCK_IMAGE_PLACEHOLDER, "brand.logo"), (BLOCK_LIST, "layout.attachments")),
    "summary": ((BLOCK_TEXT, "interpretation.summary"), (BLOCK_DIVIDER, "layout.divider")),
}


@dataclass(slots=True)
class LayoutBlock:
    """Logical layout block. Holds type and source refs only."""

    block_id: str
    section_id: str
    block_type: str
    source_refs: tuple[str, ...]
    asset_ids: tuple[str, ...]
    sequence: int
    status: str

    def to_dict(self) -> dict[str, Any]:
        """Serialize one layout block."""
        return {
            "block_id": self.block_id,
            "section_id": self.section_id,
            "block_type": self.block_type,
            "source_refs": list(self.source_refs),
            "asset_ids": list(self.asset_ids),
            "sequence": self.sequence,
            "status": self.status,
        }


def _asset_ids(block_type: str, module_id: str) -> tuple[str, ...]:
    if block_type == BLOCK_CHART_PLACEHOLDER:
        return (f"AST-chart-{module_id}",)
    if block_type == BLOCK_IMAGE_PLACEHOLDER:
        return ("AST-logo",)
    return ()


class BlockBuilder:
    """Build logical blocks for assembled layout sections."""

    def build(self, sections: Sequence[LayoutSection]) -> tuple[LayoutBlock, ...]:
        """Emit declared block types in module order. No formatting."""
        blocks: list[LayoutBlock] = []
        for section in sections:
            specs = _MODULE_BLOCKS.get(section.module_id, ())
            if section.status == "empty":
                continue
            for sequence, (block_type, source_ref) in enumerate(specs):
                blocks.append(
                    LayoutBlock(
                        block_id=f"BLK-{section.module_id}-{block_type}-{sequence}",
                        section_id=section.section_id,
                        block_type=block_type,
                        source_refs=(source_ref,),
                        asset_ids=_asset_ids(block_type, section.module_id),
                        sequence=sequence,
                        status="assembled",
                    )
                )
        return tuple(blocks)
