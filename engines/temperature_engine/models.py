"""Temperature Engine V2 result models."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class TemperatureResult:
    """Data-driven temperature analysis result."""

    success: bool = True
    temperature_level: str = "warm"
    temperature_score: float = 0.5
    warm_score: float = 0.0
    cold_score: float = 0.0
    dry_score: float = 0.0
    humid_score: float = 0.0
    confidence: float = 0.0
    matched_rules: list[str] = field(default_factory=list)
    reasoning: str = ""
    recommendations: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)
    error: str | None = None
    climate_state: str = ""
    balancing_need: str = ""
    climate_state_label: str = ""
    balancing_need_label: str = ""
    evidence_compact: str = ""
    month_branch: str = ""
    season: str = ""
    score_semantic: str = "imbalance_intensity"
    climate_source: str = ""

    def to_portal_dict(self) -> dict[str, Any]:
        """Serialize API view fields. Score is intensity, not a cold→hot axis."""
        climate_state = self.climate_state or self.temperature_level or "warm"
        return {
            "success": self.success,
            "temperature_level": climate_state,
            "climate_state": climate_state,
            "balancing_need": self.balancing_need or "",
            "climate_state_label": self.climate_state_label or "",
            "balancing_need_label": self.balancing_need_label or "",
            "evidence_compact": self.evidence_compact or "",
            "month_branch": self.month_branch or "",
            "season": self.season or "",
            "score_semantic": self.score_semantic or "imbalance_intensity",
            "climate_source": self.climate_source or "",
            "temperature_score": float(self.temperature_score),
            "warm_score": float(self.warm_score),
            "cold_score": float(self.cold_score),
            "dry_score": float(self.dry_score),
            "humid_score": float(self.humid_score),
            "confidence": float(self.confidence),
            "matched_rules": list(self.matched_rules),
            "reasoning": self.reasoning or "",
            "recommendations": list(self.recommendations),
        }

    def to_pattern_temperature_type(self) -> str:
        """Climate state for PatternContext. Does not use score thresholds."""
        level = self.climate_state or self.temperature_level or "warm"
        if level in {"cold", "cool", "warm", "hot"}:
            return level
        return "warm"

    def useful_god_temperature_overlay(self) -> str:
        """Climate state for Useful God. Does not classify score as hot/cold."""
        return self.to_pattern_temperature_type()
