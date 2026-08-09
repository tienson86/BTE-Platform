"""Deterministic layout section builder. Logical structure only."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from engines.report_engine.foundation_constants import CANONICAL_MODULE_ORDER
from engines.report_engine.layout.layout_context import (
    LayoutContext,
    extract_interpretation_sections,
)


@dataclass(slots=True)
class LayoutSection:
    """Logical layout section bound to a registered report module."""

    section_id: str
    module_id: str
    source_section_ids: tuple[str, ...]
    page_id: str
    sequence: int
    status: str

    def to_dict(self) -> dict[str, Any]:
        """Serialize one layout section."""
        return {
            "section_id": self.section_id,
            "module_id": self.module_id,
            "source_section_ids": list(self.source_section_ids),
            "page_id": self.page_id,
            "sequence": self.sequence,
            "status": self.status,
        }


def _source_map(context: LayoutContext) -> dict[str, tuple[str, ...]]:
    by_module: dict[str, list[str]] = {}
    for item in extract_interpretation_sections(context.interpretation_snapshot()):
        module_id = str(item.get("module_id") or "")
        section_id = str(item.get("section_id") or "")
        if module_id in CANONICAL_MODULE_ORDER and section_id:
            by_module.setdefault(module_id, []).append(section_id)
    return {key: tuple(dict.fromkeys(value)) for key, value in by_module.items()}


class SectionBuilder:
    """Convert report / interpretation sections into layout sections."""

    def build(self, context: LayoutContext) -> tuple[LayoutSection, ...]:
        """Emit every registered report module as a layout section."""
        sources = _source_map(context)
        sections: list[LayoutSection] = []
        for sequence, module_id in enumerate(CANONICAL_MODULE_ORDER):
            source_ids = sources.get(module_id, ())
            if module_id in {"cover", "chart", "analysis", "decision", "appendix", "interpretation"}:
                status = "assembled"
            else:
                status = "assembled" if source_ids else "empty"
            sections.append(
                LayoutSection(
                    section_id=f"LSEC-{module_id}",
                    module_id=module_id,
                    source_section_ids=source_ids,
                    page_id=f"PAGE-{module_id}",
                    sequence=sequence,
                    status=status,
                )
            )
        return tuple(sections)
