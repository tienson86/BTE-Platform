"""Scoring Interpreter result models (Pack 03 contracts)."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping

from engines.interpretation_engine.models.section_result import SectionResult


@dataclass(frozen=True, slots=True)
class ScoringItemResult:
    """One interpreted overall / dimension / confidence / quality item."""

    item_id: str
    item_type: str
    label: str = ""
    value: float = 0.0
    level: str = ""
    rating: str = ""
    score: float = 0.0
    priority: int = 0
    description: str = ""
    recommendation: str = ""
    attributes: Mapping[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Serialize item for section attributes."""
        return {
            "item_id": self.item_id,
            "item_type": self.item_type,
            "label": self.label,
            "value": self.value,
            "level": self.level,
            "rating": self.rating,
            "score": self.score,
            "priority": self.priority,
            "description": self.description,
            "recommendation": self.recommendation,
            "attributes": dict(self.attributes),
        }


@dataclass(frozen=True, slots=True)
class ScoringComponentResult:
    """One interpreted Scoring domain component."""

    component_id: str
    value: str
    score: float = 0.0
    count: int = 0
    items: tuple[ScoringItemResult, ...] = ()
    description: str = ""
    attributes: Mapping[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Serialize component for section attributes."""
        return {
            "component_id": self.component_id,
            "value": self.value,
            "score": self.score,
            "count": self.count,
            "items": [item.to_dict() for item in self.items],
            "description": self.description,
            "attributes": dict(self.attributes),
        }


@dataclass(frozen=True, slots=True)
class ScoringInterpretationSection:
    """Typed Scoring Interpreter output."""

    section: SectionResult
    overall: tuple[ScoringItemResult, ...]
    dimensions: tuple[ScoringItemResult, ...]
    confidence: tuple[ScoringItemResult, ...]
    quality: tuple[ScoringItemResult, ...]
    overall_score: float
    confidence_value: float
    grade: str = ""
    components: Mapping[str, ScoringComponentResult] = field(default_factory=dict)
    matched_rules: tuple[str, ...] = ()
    reasoning: str = ""
    source_final_result_id: str = ""
    success: bool = True
    messages: tuple[str, ...] = ()

    def validate(self) -> bool:
        """Validate typed section and nested Pack 03 section shell."""
        if not self.section.validate():
            return False
        if self.section.section_type != "scoring":
            return False
        return self.success is True or self.success is False

    def to_attributes(self) -> dict[str, Any]:
        """Flatten typed fields into SectionResult attributes."""
        return {
            "overall": [item.to_dict() for item in self.overall],
            "dimensions": [item.to_dict() for item in self.dimensions],
            "confidence": [item.to_dict() for item in self.confidence],
            "quality": [item.to_dict() for item in self.quality],
            "overall_score": self.overall_score,
            "confidence_value": self.confidence_value,
            "grade": self.grade,
            "matched_rules": list(self.matched_rules),
            "reasoning": self.reasoning,
            "source_final_result_id": self.source_final_result_id,
            "components": {
                key: component.to_dict() for key, component in self.components.items()
            },
            "skeleton": False,
        }
