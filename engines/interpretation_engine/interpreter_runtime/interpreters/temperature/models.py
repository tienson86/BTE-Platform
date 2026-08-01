"""Temperature Interpreter result models (Pack 03 contracts)."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping

from engines.interpretation_engine.models.section_result import SectionResult


@dataclass(frozen=True, slots=True)
class TemperatureComponentResult:
    """One interpreted temperature component (cold/hot/dry/wet/balance)."""

    component_id: str
    score: float
    level: str = ""
    rule_id: str | None = None
    description: str = ""
    recommendation: str = ""
    attributes: Mapping[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Serialize component for section attributes."""
        return {
            "component_id": self.component_id,
            "score": self.score,
            "level": self.level,
            "rule_id": self.rule_id,
            "description": self.description,
            "recommendation": self.recommendation,
            "attributes": dict(self.attributes),
        }


@dataclass(frozen=True, slots=True)
class TemperatureInterpretationSection:
    """Typed Temperature Interpreter output.

    Wraps a Pack 03 ``SectionResult`` shell and typed temperature components.
    """

    section: SectionResult
    cold: float
    hot: float
    dry: float
    wet: float
    balance: float
    temperature_level: str
    temperature_score: float
    components: Mapping[str, TemperatureComponentResult] = field(default_factory=dict)
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
        if self.section.section_type != "temperature":
            return False
        return self.success is True or self.success is False

    def to_attributes(self) -> dict[str, Any]:
        """Flatten typed fields into SectionResult attributes."""
        return {
            "cold": self.cold,
            "hot": self.hot,
            "dry": self.dry,
            "wet": self.wet,
            "balance": self.balance,
            "cold_score": self.cold,
            "warm_score": self.hot,
            "hot_score": self.hot,
            "dry_score": self.dry,
            "humid_score": self.wet,
            "wet_score": self.wet,
            "balance_score": self.balance,
            "temperature_level": self.temperature_level,
            "temperature_score": self.temperature_score,
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
