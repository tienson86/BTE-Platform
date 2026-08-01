"""Legacy runtime modules relocated for Pack 03 architecture coexistence.

LEGACY — retained for backward compatibility. Do not delete.
New Pack 03 runtime code must use PackInterpretationContext and *_runtime packages.
"""

from __future__ import annotations

from engines.interpretation_engine.legacy_runtime.cache import InterpretationCache
from engines.interpretation_engine.legacy_runtime.context import InterpretationContext
from engines.interpretation_engine.legacy_runtime.exceptions import (
    InterpretationError,
    InterpretationValidationError,
    InvalidContextError,
)
from engines.interpretation_engine.legacy_runtime.pipeline import InterpretationPipeline

__all__ = [
    "InterpretationCache",
    "InterpretationContext",
    "InterpretationError",
    "InterpretationPipeline",
    "InterpretationValidationError",
    "InvalidContextError",
]
