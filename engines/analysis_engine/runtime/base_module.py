"""Optional base class for Analysis Modules."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Sequence

from engines.analysis_engine.runtime.models import AnalysisContext, StageResult


class BaseAnalysisModule(ABC):
    """Convenience base for stage modules.

    Subclasses implement :meth:`evaluate` only. Stage identity and dependencies
    are provided via constructor or class attributes.
    """

    stage_id: str = ""
    version: str = "1.0.0"
    dependencies: Sequence[str] = ()

    def __init__(
        self,
        *,
        stage_id: str | None = None,
        version: str | None = None,
        dependencies: Sequence[str] | None = None,
    ) -> None:
        if stage_id is not None:
            self.stage_id = stage_id
        if version is not None:
            self.version = version
        if dependencies is not None:
            self.dependencies = tuple(dependencies)

    @abstractmethod
    def evaluate(self, context: AnalysisContext) -> StageResult:
        """Execute stage logic and return StageResult."""
        raise NotImplementedError
