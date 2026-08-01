"""Explanation runtime assembler shell.

Assembles explanation *refs* only. No explanation narrative logic.
"""

from __future__ import annotations

from engines.interpretation_engine.explanation_runtime.registry import (
    ExplanationRuntimeRegistry,
)


class ExplanationAssembler:
    """Assemble ordered explanation reference ids from registry."""

    def __init__(self, registry: ExplanationRuntimeRegistry) -> None:
        """Initialize with registry dependency."""
        self._registry = registry

    def assemble(self) -> tuple[str, ...]:
        """Return registered explanation refs in deterministic order."""
        return self._registry.list()
