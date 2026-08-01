"""Pipeline stage loader interface skeleton."""

from __future__ import annotations

from engines.analysis_engine.pipeline.stage_base import StageBase


class StageLoader:
    """Public interface for loading stage contracts.

    Resolves stage definitions into StageBase instances.
    """

    def load(self, stage_id: str) -> StageBase:
        """Load a single stage by identifier."""
        raise NotImplementedError

    def load_many(self, stage_ids: tuple[str, ...]) -> tuple[StageBase, ...]:
        """Load multiple stages by identifier."""
        raise NotImplementedError

    def discover(self) -> tuple[str, ...]:
        """Discover available stage identifiers."""
        raise NotImplementedError
