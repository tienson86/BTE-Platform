"""Interpretation context architecture and runtime package.

Re-exports legacy ``InterpretationContext`` for backward compatibility.
Pack 03 runtime context is ``PackInterpretationContext`` (canonical).
"""

from __future__ import annotations

from engines.interpretation_engine.context.builder import ContextBuilder, utc_now
from engines.interpretation_engine.context.canonical_interpretation_context import (
    CanonicalInterpretationContext,
    build_interpretation_context,
)
from engines.interpretation_engine.context.context_builder_interface import (
    InterpretationContextBuilderInterface,
)
from engines.interpretation_engine.context.context_provider_interface import (
    InterpretationContextProviderInterface,
)
from engines.interpretation_engine.context.factory import ContextFactory
from engines.interpretation_engine.context.history import ContextHistory
from engines.interpretation_engine.context.interpretation_context import (
    PackInterpretationContext,
)
from engines.interpretation_engine.context.manager import ContextManager
from engines.interpretation_engine.context.revision import (
    ContextLifecyclePhase,
    ContextRevision,
)
from engines.interpretation_engine.context.serializer import ContextSerializer
from engines.interpretation_engine.context.snapshot import ContextSnapshot
from engines.interpretation_engine.legacy_runtime.context import InterpretationContext

__all__ = [
    "CanonicalInterpretationContext",
    "ContextBuilder",
    "ContextFactory",
    "ContextHistory",
    "ContextLifecyclePhase",
    "ContextManager",
    "ContextRevision",
    "ContextSerializer",
    "ContextSnapshot",
    "InterpretationContext",
    "InterpretationContextBuilderInterface",
    "InterpretationContextProviderInterface",
    "PackInterpretationContext",
    "build_interpretation_context",
    "utc_now",
]
