"""Structured cross-reference builder. No hyperlink rendering."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Sequence

from engines.interpretation_engine.composition.chapter_builder import AssembledChapter
from engines.interpretation_engine.composition.section_builder import AssembledSection


@dataclass(slots=True)
class CrossReference:
    """Typed identity link between assembled artifacts."""

    reference_id: str
    source_type: str
    source_id: str
    target_type: str
    target_id: str

    def to_dict(self) -> dict[str, Any]:
        """Serialize one cross reference."""
        return {
            "reference_id": self.reference_id,
            "source_type": self.source_type,
            "source_id": self.source_id,
            "target_type": self.target_type,
            "target_id": self.target_id,
        }


class CrossReferenceBuilder:
    """Link sections, chapters, knowledge, evidence, and reasoning ids."""

    def build(
        self,
        sections: Sequence[AssembledSection],
        chapters: Sequence[AssembledChapter],
    ) -> tuple[CrossReference, ...]:
        """Emit deterministic structured references. No href or anchors."""
        references: list[CrossReference] = []
        chapter_by_module = {item.module_id: item for item in chapters}
        for section in sections:
            chapter = chapter_by_module.get(section.module_id)
            if chapter is not None:
                references.append(
                    self._ref("chapter", chapter.chapter_id, "section", section.section_id)
                )
                references.append(
                    self._ref("section", section.section_id, "chapter", chapter.chapter_id)
                )
            for knowledge_id in section.knowledge_ids:
                references.append(
                    self._ref("section", section.section_id, "knowledge", knowledge_id)
                )
            for evidence_id in section.evidence_ids:
                references.append(
                    self._ref("section", section.section_id, "evidence", evidence_id)
                )
            for reasoning_id in section.reasoning_ids:
                references.append(
                    self._ref("section", section.section_id, "reasoning", reasoning_id)
                )
        return tuple(sorted(references, key=lambda item: item.reference_id))

    def _ref(
        self,
        source_type: str,
        source_id: str,
        target_type: str,
        target_id: str,
    ) -> CrossReference:
        return CrossReference(
            reference_id=f"XREF-{source_type}-{source_id}-{target_type}-{target_id}",
            source_type=source_type,
            source_id=source_id,
            target_type=target_type,
            target_id=target_id,
        )
