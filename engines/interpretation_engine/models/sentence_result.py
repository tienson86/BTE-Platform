"""Interpretation sentence result output model."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping


@dataclass(frozen=True, slots=True)
class SentenceResult:
    """Immutable sentence-level interpretation output shell.

    Stores sentence *references* and structural scores only.
    Does not render report prose or hard-coded sentence text.
    """

    id: str
    sentence_ref_id: str
    section_id: str = ""
    paragraph_id: str = ""
    rank: int | None = None
    score: float | None = None
    template_ref_id: str | None = None
    placeholder_ref_ids: tuple[str, ...] = ()
    success: bool = True
    messages: tuple[str, ...] = ()
    attributes: Mapping[str, Any] = field(default_factory=dict)

    def validate(self) -> bool:
        """Validate sentence result structural integrity."""
        if not self.id or not self.sentence_ref_id:
            return False
        if self.rank is not None and self.rank < 1:
            return False
        return True
