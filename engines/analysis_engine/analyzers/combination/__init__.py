"""Combination analyzer package."""

from __future__ import annotations

from engines.analysis_engine.analyzers.combination.analyzer import CombinationAnalyzer
from engines.analysis_engine.analyzers.combination.interfaces import (
    CombinationAnalyzerInterface,
    CombinationValidatorInterface,
)
from engines.analysis_engine.analyzers.combination.models import (
    CombinationAnalyzerInput,
    CombinationAnalyzerResult,
)
from engines.analysis_engine.analyzers.combination.validator import CombinationValidator

from engines.analysis_engine.analyzers.combination.contracts import (
    CombinationAnalyzerContracts,
    CombinationConsumedMetadataContract,
    CombinationDependenciesContract,
    CombinationInputContextContract,
    CombinationOutputResultContract,
    CombinationProducedMetadataContract,
    CombinationSupportedResultTypesContract,
    CombinationSupportedRulesContract,
)

__all__ = [
    "CombinationAnalyzer",
    "CombinationAnalyzerContracts",
    "CombinationAnalyzerInput",
    "CombinationAnalyzerInterface",
    "CombinationAnalyzerResult",
    "CombinationConsumedMetadataContract",
    "CombinationDependenciesContract",
    "CombinationInputContextContract",
    "CombinationOutputResultContract",
    "CombinationProducedMetadataContract",
    "CombinationSupportedResultTypesContract",
    "CombinationSupportedRulesContract",
    "CombinationValidator",
    "CombinationValidatorInterface",
]
