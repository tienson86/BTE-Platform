"""Useful God result models."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class UsefulGodCandidate:
    rule_id: str
    rule_group: str
    useful_god: str
    favorable_gods: list[str] = field(default_factory=list)
    unfavorable_gods: list[str] = field(default_factory=list)
    priority: int = 0
    score: float = 0.0
    reason: str = ""
    description: str = ""


@dataclass(slots=True)
class UsefulGodResult:
    success: bool = True
    useful_god: str | None = None
    favorable_gods: list[str] = field(default_factory=list)
    unfavorable_gods: list[str] = field(default_factory=list)
    candidate_list: list[dict[str, Any]] = field(default_factory=list)
    confidence: float = 0.0
    matched_rules: list[str] = field(default_factory=list)
    reasoning: str = ""
    temperature_reason: str | None = None
    season_reason: str | None = None
    strength_reason: str | None = None
    balance_reason: str | None = None
    recommendations: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)
    error: str | None = None

    def to_portal_dict(self) -> dict[str, Any]:
        """Serialize minimal API view fields."""
        return {
            "success": self.success,
            "useful_god": self.useful_god or "",
            "favorable_gods": list(self.favorable_gods),
            "unfavorable_gods": list(self.unfavorable_gods),
            "reasoning": self.reasoning,
            "confidence": float(self.confidence),
            "matched_rules": list(self.matched_rules),
        }
