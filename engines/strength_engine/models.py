"""Strength Engine V2 result models."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class StrengthRuleMatch:
    """A matched strength rule."""

    rule_id: str
    rule_group: str
    score_target: str
    score: float
    priority: int = 0
    strength_level: str = ""
    reason: str = ""
    description: str = ""


@dataclass(slots=True)
class StrengthResult:
    """Data-driven strength analysis result."""

    success: bool = True
    strength_level: str = "balanced"
    strength_score: float = 0.0
    season_score: float = 0.0
    root_score: float = 0.0
    support_score: float = 0.0
    drain_score: float = 0.0
    control_score: float = 0.0
    confidence: float = 0.0
    matched_rules: list[str] = field(default_factory=list)
    reasoning: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)
    error: str | None = None

    def to_portal_dict(self) -> dict[str, Any]:
        """Serialize minimal API view fields."""
        return {
            "success": self.success,
            "strength_level": self.strength_level or "balanced",
            "strength_score": float(self.strength_score),
            "season_score": float(self.season_score),
            "root_score": float(self.root_score),
            "support_score": float(self.support_score),
            "drain_score": float(self.drain_score),
            "control_score": float(self.control_score),
            "confidence": float(self.confidence),
            "matched_rules": list(self.matched_rules),
            "reasoning": self.reasoning or "",
        }
