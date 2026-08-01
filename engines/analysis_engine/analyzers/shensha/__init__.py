"""Shen Sha analyzer package."""

from __future__ import annotations

from engines.analysis_engine.analyzers.shensha.analyzer import ShenshaAnalyzer
from engines.analysis_engine.analyzers.shensha.interfaces import (
    ShenshaAnalyzerInterface,
    ShenshaValidatorInterface,
)
from engines.analysis_engine.analyzers.shensha.models import (
    ShenshaAnalyzerInput,
    ShenshaAnalyzerResult,
)
from engines.analysis_engine.analyzers.shensha.validator import ShenshaValidator

from engines.analysis_engine.analyzers.shensha.contracts import (
    ShenshaAnalyzerContracts,
    ShenshaConsumedMetadataContract,
    ShenshaDependenciesContract,
    ShenshaInputContextContract,
    ShenshaOutputResultContract,
    ShenshaProducedMetadataContract,
    ShenshaSupportedResultTypesContract,
    ShenshaSupportedRulesContract,
)

__all__ = [
    "ShenshaAnalyzer",
    "ShenshaAnalyzerContracts",
    "ShenshaAnalyzerInput",
    "ShenshaAnalyzerInterface",
    "ShenshaAnalyzerResult",
    "ShenshaConsumedMetadataContract",
    "ShenshaDependenciesContract",
    "ShenshaInputContextContract",
    "ShenshaOutputResultContract",
    "ShenshaProducedMetadataContract",
    "ShenshaSupportedResultTypesContract",
    "ShenshaSupportedRulesContract",
    "ShenshaValidator",
    "ShenshaValidatorInterface",
]
