"""Pack 03 AnalysisResult aggregate root."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from .nodes import (
    ConfidenceSummary,
    EvidenceCollection,
    FiveElementAnalysis,
    OverallAnalysis,
    PatternAnalysis,
    SeasonAnalysis,
    StrengthAnalysis,
    TemperatureAnalysis,
    TenGodAnalysis,
    UsefulGodAnalysis,
)


@dataclass(slots=True)
class AnalysisResult:
    """
    Canonical Pack 03 analytical aggregate.

    Built from production ``ScoreResult`` + RuleContext.
    Does not replace ``ScoreResult`` on the orchestrator path.
    """

    strength: StrengthAnalysis = field(default_factory=StrengthAnalysis)
    season: SeasonAnalysis = field(default_factory=SeasonAnalysis)
    temperature: TemperatureAnalysis = field(default_factory=TemperatureAnalysis)
    five_elements: FiveElementAnalysis = field(default_factory=FiveElementAnalysis)
    ten_gods: TenGodAnalysis = field(default_factory=TenGodAnalysis)
    pattern: PatternAnalysis = field(default_factory=PatternAnalysis)
    useful_god: UsefulGodAnalysis = field(default_factory=UsefulGodAnalysis)
    overall: OverallAnalysis = field(default_factory=OverallAnalysis)
    evidence: EvidenceCollection = field(default_factory=EvidenceCollection)
    confidence: ConfidenceSummary = field(default_factory=ConfidenceSummary)
    success: bool = True
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Serialize aggregate for diagnostics / Pack 03 consumers."""
        return {
            "success": self.success,
            "strength": {
                "value": self.strength.value,
                "score": self.strength.score,
                "confidence": self.strength.confidence,
            },
            "season": {
                "season": self.season.season,
                "season_status": self.season.season_status,
                "score": self.season.score,
                "confidence": self.season.confidence,
            },
            "temperature": {
                "status": self.temperature.status,
                "score": self.temperature.score,
                "cold_score": self.temperature.cold_score,
                "hot_score": self.temperature.hot_score,
                "confidence": self.temperature.confidence,
            },
            "five_elements": {
                "score": self.five_elements.score,
                "confidence": self.five_elements.confidence,
                "elements": [
                    {
                        "name": item.name,
                        "structural_score": item.structural_score,
                        "seasonal_score": item.seasonal_score,
                        "final_score": item.final_score,
                    }
                    for item in self.five_elements.elements
                ],
            },
            "ten_gods": {
                "score": self.ten_gods.score,
                "confidence": self.ten_gods.confidence,
                "items": [
                    {"name": item.name, "value": item.value, "score": item.score}
                    for item in self.ten_gods.items
                ],
            },
            "pattern": {
                "pattern_name": self.pattern.pattern_name,
                "pattern_category": self.pattern.pattern_category,
                "score": self.pattern.score,
                "confidence": self.pattern.confidence,
            },
            "useful_god": {
                "useful_god": self.useful_god.useful_god,
                "favorable_elements": list(self.useful_god.favorable_elements),
                "unfavorable_elements": list(self.useful_god.unfavorable_elements),
                "score": self.useful_god.score,
                "confidence": self.useful_god.confidence,
            },
            "overall": {
                "overall_score": self.overall.overall_score,
                "overall_confidence": self.overall.overall_confidence,
                "grade": self.overall.grade,
                "summary_code": self.overall.summary_code,
                "recommendation_code": self.overall.recommendation_code,
            },
            "evidence_count": len(self.evidence.items),
            "confidence": {
                "overall": self.confidence.overall,
                "by_dimension": dict(self.confidence.by_dimension),
            },
            "metadata": dict(self.metadata),
        }
