"""Canonical runtime pipeline definition."""

from __future__ import annotations

import logging
from typing import Sequence

from engines.analysis_engine.runtime.constants import CANONICAL_STAGES
from engines.analysis_engine.runtime.dependency_resolver import DependencyResolver
from engines.analysis_engine.runtime.exceptions import StateError

logger = logging.getLogger(__name__)


class RuntimePipeline:
    """Defines and resolves the sequential Analysis Runtime pipeline."""

    def __init__(
        self,
        *,
        dependency_resolver: DependencyResolver | None = None,
        stages: Sequence[str] | None = None,
    ) -> None:
        self._dependencies = dependency_resolver or DependencyResolver()
        self._stages = tuple(stages or CANONICAL_STAGES)

    @property
    def stages(self) -> tuple[str, ...]:
        """Canonical stage identities."""
        return self._stages

    def resolve(self, registered_stages: Sequence[str]) -> tuple[str, ...]:
        """Resolve execution order for currently registered modules."""
        order = self._dependencies.resolve_order(registered_stages)
        logger.debug(
            "pipeline_resolved",
            extra={"order": list(order)},
        )
        return order

    def ensure_complete(self, registered_stages: Sequence[str]) -> None:
        """Require all canonical stages to be registered (default V1.0)."""
        missing = [
            stage_id
            for stage_id in self._stages
            if stage_id not in set(registered_stages)
        ]
        if missing:
            raise StateError(
                f"Pipeline incomplete; missing modules: {missing}",
                details={"missing": missing},
            )

    def describe(self) -> dict[str, object]:
        """Return a serializable pipeline description."""
        return {
            "stages": list(self._stages),
            "dependencies": {
                stage_id: list(self._dependencies.dependencies_of(stage_id))
                for stage_id in self._stages
            },
        }
