"""Ten Gods analyzer package."""

from __future__ import annotations

from engines.analysis_engine.analyzers.ten_gods.analyzer import TenGodsAnalyzer
from engines.analysis_engine.analyzers.ten_gods.interfaces import (
    TenGodsAnalyzerInterface,
    TenGodsValidatorInterface,
)
from engines.analysis_engine.analyzers.ten_gods.models import (
    TenGodsAnalyzerInput,
    TenGodsAnalyzerResult,
)
from engines.analysis_engine.analyzers.ten_gods.validator import TenGodsValidator

from engines.analysis_engine.analyzers.ten_gods.contracts import (
    TenGodsAnalyzerContracts,
    TenGodsConsumedMetadataContract,
    TenGodsDependenciesContract,
    TenGodsInputContextContract,
    TenGodsOutputResultContract,
    TenGodsProducedMetadataContract,
    TenGodsSupportedResultTypesContract,
    TenGodsSupportedRulesContract,
)

__all__ = [
    "TenGodsAnalyzer",
    "TenGodsAnalyzerContracts",
    "TenGodsAnalyzerInput",
    "TenGodsAnalyzerInterface",
    "TenGodsAnalyzerResult",
    "TenGodsConsumedMetadataContract",
    "TenGodsDependenciesContract",
    "TenGodsInputContextContract",
    "TenGodsOutputResultContract",
    "TenGodsProducedMetadataContract",
    "TenGodsSupportedResultTypesContract",
    "TenGodsSupportedRulesContract",
    "TenGodsValidator",
    "TenGodsValidatorInterface",
]
