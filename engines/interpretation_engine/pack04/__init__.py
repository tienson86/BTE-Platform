"""
Pack 04 Interpretation Engine package.

Canonical narrative path:

AnalysisResult → Evidence → Rule Matching → Sentence Selection
→ Placeholder Binding → Interpretation Builder → NarrativeInterpretationResult
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from .models import (
    EngineResult,
    InterpretationMetadata,
    InterpretationSection,
    NarrativeInterpretationResult,
    NarrativeSentence,
)

if TYPE_CHECKING:
    from .pipeline import Pack04Pipeline

__all__ = [
    "EngineResult",
    "InterpretationMetadata",
    "InterpretationSection",
    "NarrativeInterpretationResult",
    "NarrativeSentence",
    "Pack04Pipeline",
]


def __getattr__(name: str) -> Any:
    """Lazy-load pipeline to avoid Score Engine import at package init."""
    if name == "Pack04Pipeline":
        from .pipeline import Pack04Pipeline as _Pack04Pipeline

        return _Pack04Pipeline
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
