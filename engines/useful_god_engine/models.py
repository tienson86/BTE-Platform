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
    useful_ten_god: str = ""
    useful_stem: str = ""
    useful_element: str = ""
    useful_display: str = ""
    favorable_roles: list[dict[str, str]] = field(default_factory=list)
    unfavorable_roles: list[dict[str, str]] = field(default_factory=list)
    favorable_display: str = ""
    unfavorable_display: str = ""
    winning_rule_id: str = ""
    winning_rule_group: str = ""
    overall_incomplete: bool = False
    climate_candidate: str = ""
    climate_display: str = ""
    climate_stem: str = ""
    climate_element: str = ""
    climate_ten_god: str = ""
    climate_rule_id: str = ""
    climate_rule_group: str = ""
    climate_reason: str = ""
    climate_preference_label: str = ""
    overall_candidate_list: list[dict[str, Any]] = field(default_factory=list)
    climate_candidate_list: list[dict[str, Any]] = field(default_factory=list)

    def to_portal_dict(self) -> dict[str, Any]:
        """Serialize API view fields. Overall keys stay backward compatible."""
        return {
            "success": self.success,
            "overall_incomplete": self.overall_incomplete,
            "error": self.error or "",
            "useful_god": self.useful_god or "",
            "overall_useful_god": self.useful_god or "",
            "useful_ten_god": self.useful_ten_god,
            "useful_stem": self.useful_stem,
            "useful_element": self.useful_element,
            "useful_display": self.useful_display,
            "favorable_gods": list(self.favorable_gods),
            "unfavorable_gods": list(self.unfavorable_gods),
            "favorable_roles": [dict(item) for item in self.favorable_roles],
            "unfavorable_roles": [dict(item) for item in self.unfavorable_roles],
            "favorable_display": self.favorable_display,
            "unfavorable_display": self.unfavorable_display,
            "winning_rule_id": self.winning_rule_id,
            "winning_rule_group": self.winning_rule_group,
            "candidate_list": [dict(item) for item in self.candidate_list],
            "overall_candidate_list": [dict(item) for item in self.overall_candidate_list],
            "climate_candidate_list": [dict(item) for item in self.climate_candidate_list],
            "reasoning": self.reasoning,
            "confidence": float(self.confidence),
            "matched_rules": list(self.matched_rules),
            "climate_candidate": self.climate_candidate,
            "climate_display": self.climate_display,
            "climate_stem": self.climate_stem,
            "climate_element": self.climate_element,
            "climate_ten_god": self.climate_ten_god,
            "climate_rule_id": self.climate_rule_id,
            "climate_rule_group": self.climate_rule_group,
            "climate_reason": self.climate_reason,
            "climate_preference_label": self.climate_preference_label,
        }
