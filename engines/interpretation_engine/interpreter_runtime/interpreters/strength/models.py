"""Strength Interpreter result models (Pack 03 contracts)."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping

from engines.interpretation_engine.models.section_result import SectionResult


@dataclass(frozen=True, slots=True)
class StrengthComponentScore:
    """One interpreted strength component."""

    component_id: str
    score: float
    level: str = ""
    rule_id: str | None = None
    description: str = ""
    attributes: Mapping[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Serialize component for section attributes."""
        return {
            "component_id": self.component_id,
            "score": self.score,
            "level": self.level,
            "rule_id": self.rule_id,
            "description": self.description,
            "attributes": dict(self.attributes),
        }


@dataclass(frozen=True, slots=True)
class StrengthInterpretationSection:
    """Typed Strength Interpreter output.

    Wraps a Pack 03 ``SectionResult`` shell and typed strength components.
    """

    section: SectionResult
    body_strength: float
    season_strength: float
    root_strength: float
    stem_strength: float
    support_score: float
    drain_score: float
    balance_score: float
    final_strength: str
    final_strength_score: float
    components: Mapping[str, StrengthComponentScore] = field(default_factory=dict)
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
        if self.section.section_type != "strength":
            return False
        return self.success is True or self.success is False

    def to_attributes(self) -> dict[str, Any]:
        """Flatten typed fields into SectionResult attributes."""
        return {
            "body_strength": self.body_strength,
            "season_strength": self.season_strength,
            "root_strength": self.root_strength,
            "stem_strength": self.stem_strength,
            "support_score": self.support_score,
            "drain_score": self.drain_score,
            "balance_score": self.balance_score,
            "final_strength": self.final_strength,
            "final_strength_score": self.final_strength_score,
            "matched_rules": list(self.matched_rules),
            "confidence": self.confidence,
            "reasoning": self.reasoning,
            "source_final_result_id": self.source_final_result_id,
            "components": {
                key: component.to_dict() for key, component in self.components.items()
            },
            "skeleton": False,
        }
