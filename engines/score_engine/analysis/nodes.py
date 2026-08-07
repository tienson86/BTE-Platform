"""Pack 03 analytical nodes — structured scores only, no interpretation text."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class Evidence:
    """Immutable evidence record supporting an analytical conclusion."""

    evidence_id: str
    source: str
    category: str
    description: str
    weight: float = 0.0
    priority: int = 0


@dataclass(slots=True)
class EvidenceCollection:
    """Collection of evidence produced during scoring."""

    items: list[Evidence] = field(default_factory=list)

    def add(self, evidence: Evidence) -> None:
        """Append one evidence record."""
        self.items.append(evidence)

    def by_category(self, category: str) -> list[Evidence]:
        """Return evidence filtered by category."""
        return [item for item in self.items if item.category == category]


@dataclass(slots=True)
class StrengthAnalysis:
    """Day Master strength analytical node."""

    value: str = "unknown"
    score: float = 0.0
    confidence: float = 0.0
    matched_rules: list[dict[str, Any]] = field(default_factory=list)


@dataclass(slots=True)
class SeasonAnalysis:
    """Season / month-command analytical node."""

    season: str = ""
    season_status: str = ""
    score: float = 0.0
    confidence: float = 0.0
    matched_rules: list[dict[str, Any]] = field(default_factory=list)


@dataclass(slots=True)
class TemperatureAnalysis:
    """Temperature / climate analytical node."""

    status: str = ""
    score: float = 0.0
    cold_score: float = 0.0
    hot_score: float = 0.0
    confidence: float = 0.0
    matched_rules: list[dict[str, Any]] = field(default_factory=list)


@dataclass(slots=True)
class ElementScore:
    """Per-element structural score within Five Element analysis."""

    name: str
    structural_score: float = 0.0
    seasonal_score: float = 0.0
    final_score: float = 0.0
    confidence: float = 0.0


@dataclass(slots=True)
class FiveElementAnalysis:
    """Five Elements (Ngũ hành) analytical node."""

    score: float = 0.0
    confidence: float = 0.0
    elements: list[ElementScore] = field(default_factory=list)
    matched_rules: list[dict[str, Any]] = field(default_factory=list)


@dataclass(slots=True)
class TenGodItem:
    """One Ten God analytical item."""

    name: str
    value: float = 0.0
    score: float = 0.0
    confidence: float = 0.0


@dataclass(slots=True)
class TenGodAnalysis:
    """Ten Gods analytical node."""

    score: float = 0.0
    confidence: float = 0.0
    items: list[TenGodItem] = field(default_factory=list)
    matched_rules: list[dict[str, Any]] = field(default_factory=list)


@dataclass(slots=True)
class PatternAnalysis:
    """Pattern (Cách Cục) analytical node."""

    pattern_name: str = ""
    pattern_category: str = ""
    score: float = 0.0
    confidence: float = 0.0
    matched_rules: list[dict[str, Any]] = field(default_factory=list)


@dataclass(slots=True)
class UsefulGodAnalysis:
    """Useful God analytical node."""

    useful_god: str = ""
    favorable_elements: list[str] = field(default_factory=list)
    unfavorable_elements: list[str] = field(default_factory=list)
    score: float = 0.0
    confidence: float = 0.0
    matched_rules: list[dict[str, Any]] = field(default_factory=list)


@dataclass(slots=True)
class OverallAnalysis:
    """Overall analytical summary node."""

    overall_score: float = 0.0
    overall_confidence: str = ""
    grade: str = ""
    summary_code: str = ""
    recommendation_code: str = ""


@dataclass(slots=True)
class ConfidenceSummary:
    """Aggregate confidence metrics."""

    overall: str = ""
    by_dimension: dict[str, float] = field(default_factory=dict)
