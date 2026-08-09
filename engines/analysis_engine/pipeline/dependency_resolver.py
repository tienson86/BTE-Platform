"""Resolve Analysis Engine execution order from the Dependency Map."""

from __future__ import annotations

import logging
from typing import Iterable, Mapping, Sequence

from engines.analysis_engine.exceptions.pipeline_error import DependencyViolationError

logger = logging.getLogger(__name__)

PIPELINE_VERSION = "1.0.0"

CANONICAL_STAGE_ORDER: tuple[str, ...] = (
    "calendar",
    "four_pillars",
    "seasonal",
    "strength",
    "temperature",
    "pattern",
    "useful_god",
    "luck_cycle",
    "interpretation",
    "report",
)

ACTIVE_KNOWLEDGE_STAGES: tuple[str, ...] = (
    "calendar",
    "four_pillars",
    "seasonal",
    "strength",
    "temperature",
)

PLACEHOLDER_STAGES: tuple[str, ...] = (
    "pattern",
    "useful_god",
    "luck_cycle",
    "interpretation",
    "report",
)

DEFAULT_STAGE_DEPENDENCIES: dict[str, tuple[str, ...]] = {
    "calendar": (),
    "four_pillars": ("calendar",),
    "seasonal": ("four_pillars",),
    "strength": ("seasonal",),
    "temperature": ("seasonal", "strength"),
    "pattern": ("four_pillars", "seasonal", "strength", "temperature"),
    "useful_god": ("seasonal", "strength", "temperature", "pattern"),
    "luck_cycle": ("four_pillars", "seasonal", "strength", "temperature", "useful_god"),
    "interpretation": (
        "seasonal",
        "strength",
        "temperature",
        "pattern",
        "useful_god",
        "luck_cycle",
    ),
    "report": ("interpretation",),
}

STAGE_PACKAGE_IDS: dict[str, str] = {
    "seasonal": "bz_02_seasonal_core",
    "strength": "bz_01_strength_core",
    "temperature": "bz_03_temperature_core",
}


class DependencyResolver:
    """Deterministic resolver for ANALYSIS_DEPENDENCY_MAP stage order."""

    def __init__(
        self,
        *,
        canonical_order: Sequence[str] | None = None,
        dependencies: Mapping[str, Sequence[str]] | None = None,
    ) -> None:
        """Initialize canonical order and declared prerequisites."""
        self._canonical_order = tuple(canonical_order or CANONICAL_STAGE_ORDER)
        self._dependencies = {
            stage_id: tuple(deps)
            for stage_id, deps in (
                dependencies or DEFAULT_STAGE_DEPENDENCIES
            ).items()
        }

    @property
    def canonical_order(self) -> tuple[str, ...]:
        """Return the full canonical stage sequence."""
        return self._canonical_order

    def dependencies_of(self, stage_id: str) -> tuple[str, ...]:
        """Return declared direct dependencies for a stage."""
        return self._dependencies.get(stage_id, ())

    def resolve_order(self, requested_stages: Iterable[str]) -> tuple[str, ...]:
        """Return requested stages in canonical order.

        Unknown stages and forward dependencies are rejected. Placeholder
        stages may be requested later without changing active execution.
        """
        requested = tuple(requested_stages)
        unknown = [stage_id for stage_id in requested if stage_id not in self._canonical_order]
        if unknown:
            raise DependencyViolationError(f"unknown_stages:{','.join(unknown)}")

        duplicates = sorted(
            {
                stage_id
                for stage_id in requested
                if requested.count(stage_id) > 1
            }
        )
        if duplicates:
            raise DependencyViolationError(f"duplicate_stages:{','.join(duplicates)}")

        selected = set(requested)
        order = tuple(
            stage_id for stage_id in self._canonical_order if stage_id in selected
        )
        self.assert_prerequisites(order)
        logger.debug("dependency_order_resolved", extra={"order": list(order)})
        return order

    def assert_prerequisites(self, order: Sequence[str]) -> None:
        """Fail when a dependency is missing or follows its consumer."""
        positions = {stage_id: index for index, stage_id in enumerate(order)}
        for stage_id in order:
            for dependency in self.dependencies_of(stage_id):
                if dependency not in positions:
                    raise DependencyViolationError(
                        f"missing_prerequisite:{stage_id}:{dependency}"
                    )
                if positions[dependency] >= positions[stage_id]:
                    raise DependencyViolationError(
                        f"order_violation:{dependency}:{stage_id}"
                    )

    def assert_inputs_present(
        self,
        stage_id: str,
        published_stage_ids: Iterable[str],
    ) -> None:
        """Fail when required upstream outputs are not published."""
        published = set(published_stage_ids)
        missing = [
            dependency
            for dependency in self.dependencies_of(stage_id)
            if dependency not in published
        ]
        if missing:
            raise DependencyViolationError(
                f"missing_inputs:{stage_id}:{','.join(missing)}"
            )
