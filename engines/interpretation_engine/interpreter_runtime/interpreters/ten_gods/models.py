"""Ten Gods Interpreter result models (Pack 03 contracts)."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping

from engines.interpretation_engine.models.section_result import SectionResult


@dataclass(frozen=True, slots=True)
class TenGodsItemResult:
    """One interpreted Ten God / distribution / strength / interaction item."""

    item_id: str
    item_type: str
    label: str = ""
    count: int = 0
    score: float = 0.0
    priority: int = 0
    status: str = ""
    description: str = ""
    attributes: Mapping[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Serialize item for section attributes."""
        return {
            "item_id": self.item_id,
            "item_type": self.item_type,
            "label": self.label,
            "count": self.count,
            "score": self.score,
            "priority": self.priority,
            "status": self.status,
            "description": self.description,
            "attributes": dict(self.attributes),
        }


@dataclass(frozen=True, slots=True)
class TenGodsComponentResult:
    """One interpreted Ten Gods domain component."""

    component_id: str
    value: str
    score: float = 0.0
    count: int = 0
    items: tuple[TenGodsItemResult, ...] = ()
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
class TenGodsInterpretationSection:
    """Typed Ten Gods Interpreter output."""

    section: SectionResult
    ten_gods: tuple[TenGodsItemResult, ...]
    distribution: tuple[TenGodsItemResult, ...]
    strength: tuple[TenGodsItemResult, ...]
    interactions: tuple[TenGodsItemResult, ...]
    ten_gods_score: float
    dominant_god: str = ""
    components: Mapping[str, TenGodsComponentResult] = field(default_factory=dict)
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
        if self.section.section_type != "ten_gods":
            return False
        return self.success is True or self.success is False

    def to_attributes(self) -> dict[str, Any]:
        """Flatten typed fields into SectionResult attributes."""
        return {
            "ten_gods": [item.to_dict() for item in self.ten_gods],
            "distribution": [item.to_dict() for item in self.distribution],
            "strength": [item.to_dict() for item in self.strength],
            "interactions": [item.to_dict() for item in self.interactions],
            "ten_gods_score": self.ten_gods_score,
            "dominant_god": self.dominant_god,
            "matched_rules": list(self.matched_rules),
            "confidence": self.confidence,
            "reasoning": self.reasoning,
            "source_final_result_id": self.source_final_result_id,
            "components": {
                key: component.to_dict() for key, component in self.components.items()
            },
            "skeleton": False,
        }
