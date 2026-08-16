"""Expert translation models — contract only, no rewriting logic."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


class ExpertTranslationError(Exception):
    """Raised when customer text still contains engine or debug language."""


@dataclass(frozen=True, slots=True)
class TranslationRule:
    """Deterministic mapping from engine language to expert language."""

    id: str
    source_pattern: str
    target_pattern: str
    scope: str
    priority: int
    examples: tuple[tuple[str, str], ...]
    notes: str = ""

    def to_dict(self) -> dict[str, Any]:
        """Serialize one translation rule."""
        return {
            "id": self.id,
            "source_pattern": self.source_pattern,
            "target_pattern": self.target_pattern,
            "scope": self.scope,
            "priority": self.priority,
            "examples": [list(item) for item in self.examples],
            "notes": self.notes,
        }


@dataclass(frozen=True, slots=True)
class ConfidenceBand:
    """Inclusive numeric band mapped to one expert label."""

    id: str
    min_inclusive: float
    max_inclusive: float
    label: str


@dataclass(frozen=True, slots=True)
class ForbiddenTermSet:
    """Customer-text leak detector configuration."""

    phrases: tuple[str, ...]
    regex: tuple[str, ...]
    version: str


TRANSLATION_SCOPES: tuple[str, ...] = (
    "engine_terms",
    "ranking_terms",
    "confidence_terms",
    "rule_terms",
    "candidate_terms",
    "debug_terms",
    "relationship_terms",
    "knowledge_terms",
)
