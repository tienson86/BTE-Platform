"""Reusable narrative evidence classification contract. Topic-agnostic."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Final, Mapping

CLASSIFICATION_POSITIVE: Final[str] = "positive"
CLASSIFICATION_NEUTRAL: Final[str] = "neutral"
CLASSIFICATION_NEGATIVE: Final[str] = "negative"

EVIDENCE_CLASSIFICATIONS: Final[tuple[str, ...]] = (
    CLASSIFICATION_POSITIVE,
    CLASSIFICATION_NEUTRAL,
    CLASSIFICATION_NEGATIVE,
)


@dataclass(slots=True)
class NarrativeEvidenceItem:
    """One classified evidence fact relative to an analytical target."""

    id: str
    topic: str
    component: str
    classification: str
    source_path: str
    value: Any = None
    display_value: str = ""
    reason: str = ""
    confidence: float | None = None
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Serialize the evidence item."""
        return {
            "id": self.id,
            "topic": self.topic,
            "component": self.component,
            "value": self.value,
            "display_value": self.display_value,
            "classification": self.classification,
            "reason": self.reason,
            "source_path": self.source_path,
            "confidence": self.confidence,
            "metadata": dict(self.metadata),
        }
