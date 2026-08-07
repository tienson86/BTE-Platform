"""Narrative context built from Score Engine AnalysisResult."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from engines.score_engine.analysis import AnalysisResult


@dataclass(slots=True)
class NarrativeContext:
    """Runtime context for Pack 04 narrative pipeline."""

    analysis: Any
    placeholders: dict[str, str] = field(default_factory=dict)
    evidence_ids: list[str] = field(default_factory=list)
    analysis_id: str = ""
    facts: dict[str, Any] = field(default_factory=dict)


class NarrativeContextBuilder:
    """Stage 01 — build NarrativeContext from AnalysisResult."""

    def build(self, analysis: Any) -> NarrativeContext:
        """Prepare placeholders, facts, and analysis id."""
        from engines.score_engine.analysis import AnalysisResult

        if analysis is None or not isinstance(analysis, AnalysisResult):
            raise ValueError("AnalysisResult is required.")

        analysis_id = str(
            (analysis.metadata or {}).get("analysis_id")
            or (analysis.metadata or {}).get("source")
            or "analysis"
        )
        placeholders = {
            "strength_value": str(analysis.strength.value or "unknown"),
            "strength_score": self._fmt(analysis.strength.score),
            "season": str(analysis.season.season or "unknown"),
            "season_status": str(analysis.season.season_status or "unknown"),
            "season_score": self._fmt(analysis.season.score),
            "temperature_status": str(analysis.temperature.status or "unknown"),
            "temperature_score": self._fmt(analysis.temperature.score),
            "five_elements_score": self._fmt(analysis.five_elements.score),
            "ten_gods_score": self._fmt(analysis.ten_gods.score),
            "pattern_name": str(analysis.pattern.pattern_name or "Chưa xác định"),
            "pattern_score": self._fmt(analysis.pattern.score),
            "useful_god": str(analysis.useful_god.useful_god or "Chưa xác định"),
            "useful_god_score": self._fmt(analysis.useful_god.score),
            "overall_score": self._fmt(analysis.overall.overall_score),
            "grade": str(analysis.overall.grade or "N/A"),
            "overall_confidence": str(analysis.overall.overall_confidence or "unknown"),
        }
        facts = {
            "strength.value": analysis.strength.value,
            "strength.score": analysis.strength.score,
            "season.season": analysis.season.season,
            "season.score": analysis.season.score,
            "temperature.status": analysis.temperature.status,
            "temperature.score": analysis.temperature.score,
            "five_elements.score": analysis.five_elements.score,
            "ten_gods.score": analysis.ten_gods.score,
            "pattern.pattern_name": analysis.pattern.pattern_name,
            "pattern.score": analysis.pattern.score,
            "useful_god.useful_god": analysis.useful_god.useful_god,
            "useful_god.score": analysis.useful_god.score,
            "overall.overall_score": analysis.overall.overall_score,
            "overall.grade": analysis.overall.grade,
            "success": analysis.success,
        }
        return NarrativeContext(
            analysis=analysis,
            placeholders=placeholders,
            analysis_id=analysis_id,
            facts=facts,
        )

    @staticmethod
    def _fmt(value: Any) -> str:
        try:
            return f"{float(value):.2f}".rstrip("0").rstrip(".")
        except (TypeError, ValueError):
            return str(value or "0")
