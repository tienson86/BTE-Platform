"""Combination Interpreter result models (Pack 03 contracts)."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping

from engines.interpretation_engine.models.section_result import SectionResult


@dataclass(frozen=True, slots=True)
class CombinationItemResult:
    """One interpreted combination / transformation item."""

    item_id: str
    item_type: str
    members: tuple[str, ...] = ()
    result_element: str = ""
    status: str = ""
    score: float = 0.0
    priority: int = 0
    success: bool | None = None
    description: str = ""
    attributes: Mapping[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Serialize item for section attributes."""
        return {
            "item_id": self.item_id,
            "item_type": self.item_type,
            "members": list(self.members),
            "result_element": self.result_element,
            "status": self.status,
            "score": self.score,
            "priority": self.priority,
            "success": self.success,
            "description": self.description,
            "attributes": dict(self.attributes),
        }


@dataclass(frozen=True, slots=True)
class CombinationComponentResult:
    """One interpreted combination domain component."""

    component_id: str
    value: str
    score: float = 0.0
    count: int = 0
    items: tuple[CombinationItemResult, ...] = ()
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
class CombinationInterpretationSection:
    """Typed Combination Interpreter output."""

    section: SectionResult
    stem_combinations: tuple[CombinationItemResult, ...]
    branch_combinations: tuple[CombinationItemResult, ...]
    transformations: tuple[CombinationItemResult, ...]
    combination_score: float
    components: Mapping[str, CombinationComponentResult] = field(default_factory=dict)
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
        if self.section.section_type != "combination":
            return False
        return self.success is True or self.success is False

    def to_attributes(self) -> dict[str, Any]:
        """Flatten typed fields into SectionResult attributes."""
        return {
            "stem_combinations": [item.to_dict() for item in self.stem_combinations],
            "branch_combinations": [item.to_dict() for item in self.branch_combinations],
            "transformations": [item.to_dict() for item in self.transformations],
            "combination_score": self.combination_score,
            "matched_rules": list(self.matched_rules),
            "confidence": self.confidence,
            "reasoning": self.reasoning,
            "source_final_result_id": self.source_final_result_id,
            "components": {
                key: component.to_dict() for key, component in self.components.items()
            },
            "skeleton": False,
        }
