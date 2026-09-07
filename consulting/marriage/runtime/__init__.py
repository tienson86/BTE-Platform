"""Runtime package."""

from __future__ import annotations

from consulting.marriage.runtime.container import MarriageContainer
from consulting.marriage.runtime.context import CanonicalAnalysis, MarriageRuntimeContext
from consulting.marriage.runtime.wiring import wire_marriage_runtime

__all__ = [
    "CanonicalAnalysis",
    "MarriageContainer",
    "MarriageRuntimeContext",
    "wire_marriage_runtime",
]
