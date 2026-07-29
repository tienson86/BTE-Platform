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

    def to_portal_dict(self) -> dict[str, Any]:
        """Serialize minimal API view fields."""
        return {
            "success": self.success,
            "temperature_level": self.temperature_level or "warm",
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
        """Map level to PatternContext.temperature_type for Useful God."""
        level = self.temperature_level or "warm"
        if level in {"cold", "cool", "warm", "hot"}:
            return level
        if self.temperature_score >= 0.65:
            return "hot"
        if self.temperature_score <= 0.35:
            return "cold"
        if self.temperature_score >= 0.50:
            return "warm"
        return "cool"
