"""Deterministic chapter builder. Registered chapters only. No rendering."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Sequence

from engines.interpretation_engine.composition.section_builder import AssembledSection
from engines.interpretation_engine.foundation_constants import CANONICAL_MODULE_ORDER


@dataclass(slots=True)
class AssembledChapter:
    """Structural chapter wrapping zero or more assembled sections."""

    chapter_id: str
    module_id: str
    section_ids: tuple[str, ...]
    sequence: int
    status: str

    def to_dict(self) -> dict[str, Any]:
        """Serialize one assembled chapter."""
        return {
            "chapter_id": self.chapter_id,
            "module_id": self.module_id,
            "section_ids": list(self.section_ids),
            "sequence": self.sequence,
            "status": self.status,
        }


class ChapterBuilder:
    """Assemble sections into the nine registered interpretation chapters."""

    def build(self, sections: Sequence[AssembledSection]) -> tuple[AssembledChapter, ...]:
        """Emit every registered chapter in canonical order."""
        by_module = {item.module_id: item for item in sections}
        chapters: list[AssembledChapter] = []
        for sequence, module_id in enumerate(CANONICAL_MODULE_ORDER):
            section = by_module.get(module_id)
            section_ids = () if section is None else (section.section_id,)
            chapters.append(
                AssembledChapter(
                    chapter_id=f"CH-{module_id}",
                    module_id=module_id,
                    section_ids=section_ids,
                    sequence=sequence,
                    status="assembled" if section_ids else "empty",
                )
            )
        return tuple(chapters)
