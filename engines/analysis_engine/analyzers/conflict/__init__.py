"""Conflict analyzer package."""

from __future__ import annotations

from engines.analysis_engine.analyzers.conflict.analyzer import ConflictAnalyzer
from engines.analysis_engine.analyzers.conflict.interfaces import (
    ConflictAnalyzerInterface,
    ConflictValidatorInterface,
)
from engines.analysis_engine.analyzers.conflict.models import (
    ConflictAnalyzerInput,
    ConflictAnalyzerResult,
)
from engines.analysis_engine.analyzers.conflict.validator import ConflictValidator

from engines.analysis_engine.analyzers.conflict.contracts import (
    ConflictAnalyzerContracts,
    ConflictConsumedMetadataContract,
    ConflictDependenciesContract,
    ConflictInputContextContract,
    ConflictOutputResultContract,
    ConflictProducedMetadataContract,
    ConflictSupportedResultTypesContract,
    ConflictSupportedRulesContract,
)

__all__ = [
    "ConflictAnalyzer",
    "ConflictAnalyzerContracts",
    "ConflictAnalyzerInput",
    "ConflictAnalyzerInterface",
    "ConflictAnalyzerResult",
    "ConflictConsumedMetadataContract",
    "ConflictDependenciesContract",
    "ConflictInputContextContract",
    "ConflictOutputResultContract",
    "ConflictProducedMetadataContract",
    "ConflictSupportedResultTypesContract",
    "ConflictSupportedRulesContract",
    "ConflictValidator",
    "ConflictValidatorInterface",
]
