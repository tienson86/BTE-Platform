"""Resolve logical layout metadata. No pagination rendering."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Sequence

from engines.report_engine.layout.block_builder import LayoutBlock
from engines.report_engine.layout.document_builder import DocumentLayout
from engines.report_engine.layout.section_builder import LayoutSection


@dataclass(slots=True)
class LayoutResolution:
    """Logical page hierarchy and block-flow metadata."""

    page_hierarchy: tuple[str, ...]
    block_order: tuple[str, ...]
    column_metadata: dict[str, Any]
    page_breaks: tuple[dict[str, str], ...]
    keep_together: tuple[dict[str, Any], ...]
    widows_orphans: dict[str, int]
    status: str

    def to_dict(self) -> dict[str, Any]:
        """Serialize layout resolution metadata."""
        return {
            "page_hierarchy": list(self.page_hierarchy),
            "block_order": list(self.block_order),
            "column_metadata": dict(self.column_metadata),
            "page_breaks": [dict(item) for item in self.page_breaks],
            "keep_together": [dict(item) for item in self.keep_together],
            "widows_orphans": dict(self.widows_orphans),
            "status": self.status,
        }


class LayoutResolver:
    """Order pages and blocks. Emit break / keep-together metadata only."""

    def resolve(
        self,
        document: DocumentLayout,
        sections: Sequence[LayoutSection],
        blocks: Sequence[LayoutBlock],
    ) -> LayoutResolution:
        """Derive hierarchy from assembled document, sections, and blocks."""
        page_hierarchy = tuple(page.page_id for page in document.pages)
        block_order = tuple(item.block_id for item in blocks)
        page_breaks = tuple(
            {"break_id": f"BRK-{section.module_id}", "after_section_id": section.section_id}
            for section in sections[:-1]
            if section.status == "assembled"
        )
        keep_together = tuple(
            {
                "group_id": f"KT-{section.section_id}",
                "block_ids": [item.block_id for item in blocks if item.section_id == section.section_id],
            }
            for section in sections
            if any(item.section_id == section.section_id for item in blocks)
        )
        return LayoutResolution(
            page_hierarchy=page_hierarchy,
            block_order=block_order,
            column_metadata={"columns": 1, "column_id": "COL-primary"},
            page_breaks=page_breaks,
            keep_together=keep_together,
            widows_orphans={"widows": 2, "orphans": 2},
            status="resolved",
        )
