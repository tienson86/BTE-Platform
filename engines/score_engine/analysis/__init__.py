"""
Pack 03 AnalysisResult aggregate (Score Engine domain).

Production pipeline continues to emit ``ScoreResult``.
``AnalysisResult`` is the canonical Pack 03 aggregate built from ScoreResult.
"""

from .analysis_result import AnalysisResult
from .builder import AnalysisResultBuilder
from .nodes import (
    ConfidenceSummary,
    Evidence,
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

__all__ = [
    "AnalysisResult",
    "AnalysisResultBuilder",
    "ConfidenceSummary",
    "Evidence",
    "EvidenceCollection",
    "FiveElementAnalysis",
    "OverallAnalysis",
    "PatternAnalysis",
    "SeasonAnalysis",
    "StrengthAnalysis",
    "TemperatureAnalysis",
    "TenGodAnalysis",
    "UsefulGodAnalysis",
]
