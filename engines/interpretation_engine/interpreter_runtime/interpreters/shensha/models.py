"""Shensha Interpreter result models (Pack 03 contracts)."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping

from engines.interpretation_engine.models.section_result import SectionResult


@dataclass(frozen=True, slots=True)
class ShenshaItemResult:
    """One interpreted Shensha / importance / priority / explanation item."""

    item_id: str
    item_type: str
    label: str = ""
    score: float = 0.0
    priority: int = 0
    importance: str = ""
    importance_rank: int = 0
    explanation: str = ""
    recommendation: str = ""
    status: str = ""
    polarity: str = ""
    description: str = ""
    attributes: Mapping[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Serialize item for section attributes."""
        return {
            "item_id": self.item_id,
            "item_type": self.item_type,
            "label": self.label,
            "score": self.score,
            "priority": self.priority,
            "importance": self.importance,
            "importance_rank": self.importance_rank,
            "explanation": self.explanation,
            "recommendation": self.recommendation,
            "status": self.status,
            "polarity": self.polarity,
            "description": self.description,
            "attributes": dict(self.attributes),
        }


@dataclass(frozen=True, slots=True)
class ShenshaComponentResult:
    """One interpreted Shensha domain component."""

    component_id: str
    value: str
    score: float = 0.0
    count: int = 0
    items: tuple[ShenshaItemResult, ...] = ()
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
class ShenshaInterpretationSection:
    """Typed Shensha Interpreter output."""

    section: SectionResult
    detected: tuple[ShenshaItemResult, ...]
    importance: tuple[ShenshaItemResult, ...]
    priorities: tuple[ShenshaItemResult, ...]
    explanations: tuple[ShenshaItemResult, ...]
    shensha_score: float
    components: Mapping[str, ShenshaComponentResult] = field(default_factory=dict)
    matched_rules: tuple[str, ...] = ()
    confidence: float = 0.0
    reasoning: str = ""
    source_final_result_id: str = ""
    success: bool = True
    messages: tuple[str, ...] = ()

    def validate(self) -> bool:
        """Validate typed section and nested Pack 03 section shell."""
        if not self.section.validate():
            return False
        if self.section.section_type != "shensha":
            return False
        return self.success is True or self.success is False

    def to_attributes(self) -> dict[str, Any]:
        """Flatten typed fields into SectionResult attributes."""
        return {
            "detected": [item.to_dict() for item in self.detected],
            "importance": [item.to_dict() for item in self.importance],
            "priorities": [item.to_dict() for item in self.priorities],
            "explanations": [item.to_dict() for item in self.explanations],
            "shensha_score": self.shensha_score,
            "matched_rules": list(self.matched_rules),
            "confidence": self.confidence,
            "reasoning": self.reasoning,
            "source_final_result_id": self.source_final_result_id,
            "components": {
                key: component.to_dict() for key, component in self.components.items()
            },
            "skeleton": False,
        }
