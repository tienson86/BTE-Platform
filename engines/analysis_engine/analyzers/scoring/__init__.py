"""Scoring analyzer package."""

from __future__ import annotations

from engines.analysis_engine.analyzers.scoring.analyzer import ScoringAnalyzer
from engines.analysis_engine.analyzers.scoring.interfaces import (
    ScoringAnalyzerInterface,
    ScoringValidatorInterface,
)
from engines.analysis_engine.analyzers.scoring.models import (
    ScoringAnalyzerInput,
    ScoringAnalyzerResult,
)
from engines.analysis_engine.analyzers.scoring.validator import ScoringValidator

from engines.analysis_engine.analyzers.scoring.contracts import (
    ScoringAnalyzerContracts,
    ScoringConsumedMetadataContract,
    ScoringDependenciesContract,
    ScoringInputContextContract,
    ScoringOutputResultContract,
    ScoringProducedMetadataContract,
    ScoringSupportedResultTypesContract,
    ScoringSupportedRulesContract,
)

__all__ = [
    "ScoringAnalyzer",
    "ScoringAnalyzerContracts",
    "ScoringAnalyzerInput",
    "ScoringAnalyzerInterface",
    "ScoringAnalyzerResult",
    "ScoringConsumedMetadataContract",
    "ScoringDependenciesContract",
    "ScoringInputContextContract",
    "ScoringOutputResultContract",
    "ScoringProducedMetadataContract",
    "ScoringSupportedResultTypesContract",
    "ScoringSupportedRulesContract",
    "ScoringValidator",
    "ScoringValidatorInterface",
]
