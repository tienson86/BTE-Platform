"""Interpretation context architecture package.

Re-exports legacy ``InterpretationContext`` for backward compatibility.
"""

from __future__ import annotations

from engines.interpretation_engine.context.context_builder_interface import (
    InterpretationContextBuilderInterface,
)
from engines.interpretation_engine.context.context_provider_interface import (
    InterpretationContextProviderInterface,
)
from engines.interpretation_engine.legacy_runtime.context import InterpretationContext

__all__ = [
    "InterpretationContext",
    "InterpretationContextBuilderInterface",
    "InterpretationContextProviderInterface",
]
