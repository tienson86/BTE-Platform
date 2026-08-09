"""Canonical Table of Contents model. Hierarchy only."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Sequence

from engines.report_engine.layout.section_builder import LayoutSection

TOC_ID = "TOC-report-1"


@dataclass(slots=True)
class TocEntry:
    """One TOC node. No page numbers or hyperlinks."""

    entry_id: str
    section_id: str
    module_id: str
    depth: int
    children: tuple[str, ...]
    status: str

    def to_dict(self) -> dict[str, Any]:
        """Serialize one TOC entry."""
        return {
            "entry_id": self.entry_id,
            "section_id": self.section_id,
            "module_id": self.module_id,
            "depth": self.depth,
            "children": list(self.children),
            "status": self.status,
        }


@dataclass(slots=True)
class TableOfContents:
    """Canonical TOC. Hierarchy of layout sections only."""

    toc_id: str
    entry_ids: tuple[str, ...]
    entries: tuple[TocEntry, ...]
    status: str

    def to_dict(self) -> dict[str, Any]:
        """Serialize the table of contents."""
        return {
            "toc_id": self.toc_id,
            "entry_ids": list(self.entry_ids),
            "entries": [item.to_dict() for item in self.entries],
            "status": self.status,
        }


class TocBuilder:
    """Build a depth-1 TOC from registered layout sections."""

    def build(self, sections: Sequence[LayoutSection]) -> TableOfContents:
        """Emit one entry per section in document order."""
        entries = tuple(
            TocEntry(
                entry_id=f"TOC-{section.module_id}",
                section_id=section.section_id,
                module_id=section.module_id,
                depth=1,
                children=(),
                status=section.status,
            )
            for section in sections
        )
        return TableOfContents(
            toc_id=TOC_ID,
            entry_ids=tuple(item.entry_id for item in entries),
            entries=entries,
            status="assembled",
        )
