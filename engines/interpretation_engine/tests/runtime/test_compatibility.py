"""Pack boundary and compatibility smoke tests for runtime foundation."""

from __future__ import annotations

from engines.interpretation_engine.context import (
    InterpretationContext as PackageLegacyContext,
    PackInterpretationContext,
)
from engines.interpretation_engine.context.interpretation_context import (
    InterpretationContext as PackAlias,
    PackInterpretationContext as CanonicalPackContext,
)
from engines.interpretation_engine.legacy_runtime import InterpretationContext as LegacyContext
from engines.interpretation_engine.orchestration import ExecutionManager, RuntimePipeline


def test_pack_context_naming_and_legacy_coexistence() -> None:
    """PackInterpretationContext is canonical; legacy context remains available."""
    assert CanonicalPackContext is PackInterpretationContext
    assert PackAlias is PackInterpretationContext
    assert PackageLegacyContext is LegacyContext
    assert PackageLegacyContext is not PackInterpretationContext


def test_orchestration_exports() -> None:
    """Orchestration package exports RuntimePipeline and ExecutionManager."""
    assert RuntimePipeline is not None
    assert ExecutionManager is not None
