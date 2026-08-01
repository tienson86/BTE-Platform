"""Season Interpreter result models (Pack 03 contracts)."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping

from engines.interpretation_engine.models.section_result import SectionResult


@dataclass(frozen=True, slots=True)
class SeasonComponentResult:
    """One interpreted season component."""

    component_id: str
    value: str
    score: float = 0.0
    level: str = ""
    rule_id: str | None = None
    description: str = ""
    recommendation: str = ""
    attributes: Mapping[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Serialize component for section attributes."""
        return {
            "component_id": self.component_id,
            "value": self.value,
            "score": self.score,
            "level": self.level,
            "rule_id": self.rule_id,
            "description": self.description,
            "recommendation": self.recommendation,
            "attributes": dict(self.attributes),
        }


@dataclass(frozen=True, slots=True)
class SeasonInterpretationSection:
    """Typed Season Interpreter output.

    Wraps a Pack 03 ``SectionResult`` shell and typed season components.
    """

    section: SectionResult
    season: str
    month_branch: str
    qi_stage: str
    climate: str
    temperature_level: str
    season_score: float
    temperature_score: float
    components: Mapping[str, SeasonComponentResult] = field(default_factory=dict)
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
        if self.section.section_type != "season":
            return False
        return self.success is True or self.success is False

    def to_attributes(self) -> dict[str, Any]:
        """Flatten typed fields into SectionResult attributes."""
        return {
            "season": self.season,
            "month_branch": self.month_branch,
            "qi_stage": self.qi_stage,
            "season_phase": self.qi_stage,
            "climate": self.climate,
            "climate_type": self.climate,
            "temperature_level": self.temperature_level,
            "season_score": self.season_score,
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
