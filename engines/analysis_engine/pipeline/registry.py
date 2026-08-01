"""Pipeline stage registry interface skeleton."""

from __future__ import annotations

from engines.analysis_engine.pipeline.stage_base import StageBase


class StageRegistry:
    """Public registry interface for pipeline stages.

    Stores stage contracts by identifier.
    """

    def register(self, stage: StageBase) -> None:
        """Register a stage contract."""
        raise NotImplementedError

    def unregister(self, stage_id: str) -> None:
        """Remove a registered stage by identifier."""
        raise NotImplementedError

    def get(self, stage_id: str) -> StageBase | None:
        """Return a registered stage by identifier."""
        raise NotImplementedError

    def list_stages(self) -> tuple[StageBase, ...]:
        """Return all registered stages."""
        raise NotImplementedError

    def clear(self) -> None:
        """Remove all registered stages."""
        raise NotImplementedError
