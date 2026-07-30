"""Analysis Engine package.

Exposes the Analysis Runtime framework for orchestrating analytical stages.
"""

from __future__ import annotations

from engines.analysis_engine.runtime import (
    AnalysisContext,
    AnalysisResult,
    AnalysisRuntime,
    BaseAnalysisModule,
    StageResult,
)

__all__ = [
    "AnalysisContext",
    "AnalysisResult",
    "AnalysisRuntime",
    "BaseAnalysisModule",
    "StageResult",
]

__version__ = "1.0.0"
