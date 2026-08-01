"""Pattern Interpreter result models (Pack 03 contracts)."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping

from engines.interpretation_engine.models.section_result import SectionResult


@dataclass(frozen=True, slots=True)
class PatternComponentResult:
    """One interpreted pattern pipeline component."""

    component_id: str
    value: str
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
            "score": self.score,
            "priority": self.priority,
            "rule_id": self.rule_id,
            "description": self.description,
            "attributes": dict(self.attributes),
        }


@dataclass(frozen=True, slots=True)
class PatternInterpretationSection:
    """Typed Pattern Interpreter output.

    Wraps a Pack 03 ``SectionResult`` shell and typed pattern components.
    """

    section: SectionResult
    main_pattern: str
    final_pattern: str
    status: str
    score: float
    priority: int
    follow_type: str
    candidate_patterns: tuple[str, ...] = ()
    validated_patterns: tuple[str, ...] = ()
    secondary_patterns: tuple[str, ...] = ()
    discarded_patterns: tuple[str, ...] = ()
    components: Mapping[str, PatternComponentResult] = field(default_factory=dict)
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
        if self.section.section_type != "pattern":
            return False
        return self.success is True or self.success is False

    def to_attributes(self) -> dict[str, Any]:
        """Flatten typed fields into SectionResult attributes."""
        return {
            "main_pattern": self.main_pattern,
            "final_pattern": self.final_pattern,
            "pattern": self.final_pattern or self.main_pattern,
            "status": self.status,
            "score": self.score,
            "priority": self.priority,
            "follow_type": self.follow_type,
            "candidate_patterns": list(self.candidate_patterns),
            "validated_patterns": list(self.validated_patterns),
            "secondary_patterns": list(self.secondary_patterns),
            "discarded_patterns": list(self.discarded_patterns),
            "matched_rules": list(self.matched_rules),
            "confidence": self.confidence,
            "reasoning": self.reasoning,
            "source_final_result_id": self.source_final_result_id,
            "components": {
                key: component.to_dict() for key, component in self.components.items()
            },
            "skeleton": False,
        }
