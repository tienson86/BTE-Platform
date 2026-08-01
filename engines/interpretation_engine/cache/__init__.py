"""Cache architecture package.

Re-exports legacy ``InterpretationCache`` for backward compatibility.
"""

from __future__ import annotations

from engines.interpretation_engine.cache.cache_interface import InterpretationCacheInterface
from engines.interpretation_engine.legacy_runtime.cache import InterpretationCache

__all__ = [
    "InterpretationCache",
    "InterpretationCacheInterface",
]
