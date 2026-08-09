"""IE-3 Interpretation Composition & Assembly Engine."""

from engines.interpretation_engine.composition.composition_context import (
    ASSEMBLY_VERSION,
    InterpretationAssemblyContext,
    build_assembly_context,
)
from engines.interpretation_engine.composition.composition_engine import (
    InterpretationCompositionEngine,
)
from engines.interpretation_engine.composition.composition_registry import CompositionRegistry
from engines.interpretation_engine.composition.composition_result import (
    CanonicalInterpretationResult,
    InterpretationAudit,
    InterpretationTrace,
)

__all__ = [
    "ASSEMBLY_VERSION",
    "CanonicalInterpretationResult",
    "CompositionRegistry",
    "InterpretationAssemblyContext",
    "InterpretationAudit",
    "InterpretationCompositionEngine",
    "InterpretationTrace",
    "build_assembly_context",
]
