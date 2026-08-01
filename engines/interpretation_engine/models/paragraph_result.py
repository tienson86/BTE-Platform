"""Interpretation paragraph result output model."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping

from engines.interpretation_engine.models.sentence_result import SentenceResult


@dataclass(frozen=True, slots=True)
class ParagraphResult:
    """Immutable paragraph-level interpretation output shell.

    Aggregates sentence results by reference. No report rendering.
    """

    id: str
    section_id: str
    paragraph_ref_id: str | None = None
    title_ref: str | None = None
    sentences: tuple[SentenceResult, ...] = ()
    success: bool = True
    messages: tuple[str, ...] = ()
    attributes: Mapping[str, Any] = field(default_factory=dict)

    def validate(self) -> bool:
        """Validate paragraph result structural integrity."""
        if not self.id or not self.section_id:
            return False
        for sentence in self.sentences:
            if not sentence.validate():
                return False
            if sentence.paragraph_id and sentence.paragraph_id != self.id:
                return False
            if sentence.section_id and sentence.section_id != self.section_id:
                return False
        return True

    def sentence_ref_ids(self) -> tuple[str, ...]:
        """Return ordered sentence reference identifiers."""
        return tuple(sentence.sentence_ref_id for sentence in self.sentences)
