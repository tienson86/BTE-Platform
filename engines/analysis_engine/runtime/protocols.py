"""Analysis module protocol and registration descriptor."""

from __future__ import annotations

from typing import Protocol, Sequence, runtime_checkable

from engines.analysis_engine.runtime.models import AnalysisContext, StageResult


@runtime_checkable
class AnalysisModule(Protocol):
    """Contract every analysis stage module must satisfy."""

    @property
    def stage_id(self) -> str:
        """Stable stage identity (e.g. ``strength``)."""

    @property
    def version(self) -> str:
        """Module version string."""

    @property
    def dependencies(self) -> Sequence[str]:
        """Prior stage ids required before evaluate."""

    def evaluate(self, context: AnalysisContext) -> StageResult:
        """Execute stage logic and return an immutable StageResult."""


class ModuleDescriptor:
    """Registered module metadata held by the runtime."""

    __slots__ = ("module", "stage_id", "version", "dependencies")

    def __init__(
        self,
        module: AnalysisModule,
        dependencies: Sequence[str] | None = None,
    ) -> None:
        self.module = module
        self.stage_id = module.stage_id
        self.version = module.version
        if dependencies is not None:
            self.dependencies = tuple(dependencies)
        else:
            self.dependencies = tuple(module.dependencies)
