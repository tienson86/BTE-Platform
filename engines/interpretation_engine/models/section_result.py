"""Interpretation section result output model."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping

from engines.interpretation_engine.models.paragraph_result import ParagraphResult


@dataclass(frozen=True, slots=True)
class SectionResult:
    """Immutable section-level interpretation output shell.

    Aggregates paragraph results by reference. No report rendering.
    """

    id: str
    section_type: str
    title_ref: str | None = None
    interpreter_id: str | None = None
    paragraphs: tuple[ParagraphResult, ...] = ()
    success: bool = True
    messages: tuple[str, ...] = ()
    attributes: Mapping[str, Any] = field(default_factory=dict)

    def validate(self) -> bool:
        """Validate section result structural integrity."""
        if not self.id or not self.section_type:
            return False
        for paragraph in self.paragraphs:
            if not paragraph.validate():
                return False
            if paragraph.section_id != self.id:
                return False
        return True

    def paragraph_ids(self) -> tuple[str, ...]:
        """Return ordered paragraph identifiers."""
        return tuple(paragraph.id for paragraph in self.paragraphs)

    def sentence_ref_ids(self) -> tuple[str, ...]:
        """Return ordered sentence reference identifiers across paragraphs."""
        refs: list[str] = []
        for paragraph in self.paragraphs:
            refs.extend(paragraph.sentence_ref_ids())
        return tuple(refs)
