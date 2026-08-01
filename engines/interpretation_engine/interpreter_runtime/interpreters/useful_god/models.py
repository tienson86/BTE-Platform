"""Useful God Interpreter result models (Pack 03 contracts)."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping

from engines.interpretation_engine.models.section_result import SectionResult


@dataclass(frozen=True, slots=True)
class UsefulGodComponentResult:
    """One interpreted useful-god component."""

    component_id: str
    value: str
    values: tuple[str, ...] = ()
    score: float = 0.0
    priority: int = 0
    rule_id: str | None = None
    description: str = ""
    attributes: Mapping[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Serialize component for section attributes."""
        return {
            "component_id": self.component_id,
            "value": self.value,
            "values": list(self.values),
            "score": self.score,
            "priority": self.priority,
            "rule_id": self.rule_id,
            "description": self.description,
            "attributes": dict(self.attributes),
        }


@dataclass(frozen=True, slots=True)
class UsefulGodInterpretationSection:
    """Typed Useful God Interpreter output.

    Wraps a Pack 03 ``SectionResult`` shell and typed useful-god components.
    """

    section: SectionResult
    useful_god: str
    favorable_gods: tuple[str, ...]
    unfavorable_gods: tuple[str, ...]
    supporting_elements: tuple[str, ...]
    score: float = 0.0
    priority: int = 0
    components: Mapping[str, UsefulGodComponentResult] = field(default_factory=dict)
    matched_rules: tuple[str, ...] = ()
    recommendations: tuple[str, ...] = ()
    confidence: float = 0.0
    reasoning: str = ""
    source_final_result_id: str = ""
    success: bool = True
    messages: tuple[str, ...] = ()

    def validate(self) -> bool:
        """Validate typed section and nested Pack 03 section shell."""
        if not self.section.validate():
            return False
        if self.section.section_type != "useful_god":
            return False
        return self.success is True or self.success is False

    def to_attributes(self) -> dict[str, Any]:
        """Flatten typed fields into SectionResult attributes."""
        return {
            "useful_god": self.useful_god,
            "dung_than": self.useful_god,
            "favorable_gods": list(self.favorable_gods),
            "hy_than": list(self.favorable_gods),
            "unfavorable_gods": list(self.unfavorable_gods),
            "ky_than": list(self.unfavorable_gods),
            "supporting_elements": list(self.supporting_elements),
            "support_elements": list(self.supporting_elements),
            "score": self.score,
            "priority": self.priority,
            "matched_rules": list(self.matched_rules),
            "recommendations": list(self.recommendations),
            "confidence": self.confidence,
            "reasoning": self.reasoning,
            "source_final_result_id": self.source_final_result_id,
            "components": {
                key: component.to_dict() for key, component in self.components.items()
            },
            "skeleton": False,
        }
