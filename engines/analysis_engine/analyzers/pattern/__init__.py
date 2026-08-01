"""Pattern analyzer package."""

from __future__ import annotations

from engines.analysis_engine.analyzers.pattern.analyzer import PatternAnalyzer
from engines.analysis_engine.analyzers.pattern.interfaces import (
    PatternAnalyzerInterface,
    PatternValidatorInterface,
)
from engines.analysis_engine.analyzers.pattern.models import (
    PatternAnalyzerInput,
    PatternAnalyzerResult,
)
from engines.analysis_engine.analyzers.pattern.validator import PatternValidator

from engines.analysis_engine.analyzers.pattern.contracts import (
    PatternAnalyzerContracts,
    PatternConsumedMetadataContract,
    PatternDependenciesContract,
    PatternInputContextContract,
    PatternOutputResultContract,
    PatternProducedMetadataContract,
    PatternSupportedResultTypesContract,
    PatternSupportedRulesContract,
)

__all__ = [
    "PatternAnalyzer",
    "PatternAnalyzerContracts",
    "PatternAnalyzerInput",
    "PatternAnalyzerInterface",
    "PatternAnalyzerResult",
    "PatternConsumedMetadataContract",
    "PatternDependenciesContract",
    "PatternInputContextContract",
    "PatternOutputResultContract",
    "PatternProducedMetadataContract",
    "PatternSupportedResultTypesContract",
    "PatternSupportedRulesContract",
    "PatternValidator",
    "PatternValidatorInterface",
]
