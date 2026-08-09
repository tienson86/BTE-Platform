"""Canonical stage catalog for the AX-2 Analysis Pipeline."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Mapping

from engines.analysis_engine.exceptions.pipeline_error import DependencyViolationError

PIPELINE_ID_V2 = "canonical_analysis_pipeline"
PIPELINE_VERSION_V2 = "2.0.0"

CANONICAL_STAGE_ORDER_V2: tuple[str, ...] = (
    "calendar",
    "four_pillars",
    "seasonal",
    "strength",
    "temperature",
    "pattern",
    "pattern_evaluation",
    "useful_god",
    "luck_cycle",
    "interpretation",
    "report",
)

ACTIVE_CANONICAL_STAGES: tuple[str, ...] = (
    "calendar",
    "four_pillars",
    "seasonal",
    "strength",
    "temperature",
    "pattern",
    "pattern_evaluation",
    "useful_god",
)

INACTIVE_FUTURE_STAGES: tuple[str, ...] = (
    "luck_cycle",
    "interpretation",
    "report",
)


@dataclass(frozen=True, slots=True)
class StageRecord:
    """Immutable catalog entry for one pipeline stage."""

    stage_id: str
    package_id: str | None
    version: str
    dependencies: tuple[str, ...]
    produced_outputs: tuple[str, ...]
    consumed_outputs: tuple[str, ...]
    enabled: bool

    def to_dict(self) -> dict[str, object]:
        """Serialize the catalog record."""
        return {
            "stage_id": self.stage_id,
            "package_id": self.package_id,
            "version": self.version,
            "dependencies": list(self.dependencies),
            "produced_outputs": list(self.produced_outputs),
            "consumed_outputs": list(self.consumed_outputs),
            "enabled": self.enabled,
        }


def _default_records() -> tuple[StageRecord, ...]:
    return (
        StageRecord(
            stage_id="calendar",
            package_id=None,
            version="1.0.0",
            dependencies=(),
            produced_outputs=(
                "normalized_datetime",
                "solar_term",
                "lunar_month_index",
            ),
            consumed_outputs=(),
            enabled=True,
        ),
        StageRecord(
            stage_id="four_pillars",
            package_id=None,
            version="1.0.0",
            dependencies=("calendar",),
            produced_outputs=(
                "day_master",
                "day_master_element",
                "month_branch",
                "pillars",
            ),
            consumed_outputs=("normalized_datetime", "solar_term"),
            enabled=True,
        ),
        StageRecord(
            stage_id="seasonal",
            package_id="bz_02_seasonal_core",
            version="1.0.0",
            dependencies=("four_pillars",),
            produced_outputs=("season", "season_phase", "season_score"),
            consumed_outputs=("month_branch", "lunar_month_index"),
            enabled=True,
        ),
        StageRecord(
            stage_id="strength",
            package_id="bz_01_strength_core",
            version="1.2.0",
            dependencies=("seasonal",),
            produced_outputs=("strength_score", "strength_level"),
            consumed_outputs=("season", "season_phase", "month_status"),
            enabled=True,
        ),
        StageRecord(
            stage_id="temperature",
            package_id="bz_03_temperature_core",
            version="1.0.0",
            dependencies=("seasonal", "strength"),
            produced_outputs=(
                "temperature_score",
                "temperature_level",
                "dryness_level",
                "humidity_level",
            ),
            consumed_outputs=(
                "season",
                "season_phase",
                "strength_level",
                "day_master_element",
            ),
            enabled=True,
        ),
        StageRecord(
            stage_id="pattern",
            package_id="bz_04_pattern_core",
            version="1.0.0",
            dependencies=("four_pillars", "seasonal", "strength", "temperature"),
            produced_outputs=(
                "principal_pattern",
                "pattern_confirmed",
                "pattern_conflict",
                "pattern_suppressed",
                "pattern_stability",
                "core_pattern_score",
            ),
            consumed_outputs=(
                "season",
                "season_phase",
                "season_score",
                "strength_score",
                "temperature_score",
            ),
            enabled=True,
        ),
        StageRecord(
            stage_id="pattern_evaluation",
            package_id="bz_05_pattern_evaluation",
            version="1.0.0",
            dependencies=("pattern", "seasonal", "strength", "temperature"),
            produced_outputs=(
                "pattern_quality",
                "pattern_confidence",
                "pattern_integrity",
                "pattern_stability",
                "pattern_score",
                "evaluation_diagnostics",
            ),
            consumed_outputs=(
                "principal_pattern",
                "pattern_confirmed",
                "pattern_conflict",
                "pattern_suppressed",
                "core_pattern_score",
                "season_score",
                "strength_score",
                "temperature_score",
            ),
            enabled=True,
        ),
        StageRecord(
            stage_id="useful_god",
            package_id="bz_06_useful_god_foundation",
            version="1.0.0",
            dependencies=(
                "seasonal",
                "strength",
                "temperature",
                "pattern",
                "pattern_evaluation",
            ),
            produced_outputs=(
                "useful_god",
                "favorable_gods",
                "unfavorable_gods",
                "decision_confidence",
                "decision_score",
                "decision_reasoning",
                "decision_diagnostics",
            ),
            consumed_outputs=(
                "season_score",
                "strength_score",
                "temperature_score",
                "pattern_score",
                "pattern_quality",
                "pattern_confidence",
                "pattern_integrity",
                "pattern_stability",
            ),
            enabled=True,
        ),
        StageRecord(
            stage_id="luck_cycle",
            package_id=None,
            version="1.0.0",
            dependencies=(
                "four_pillars",
                "seasonal",
                "strength",
                "temperature",
                "useful_god",
            ),
            produced_outputs=(),
            consumed_outputs=("useful_god", "decision_score"),
            enabled=False,
        ),
        StageRecord(
            stage_id="interpretation",
            package_id=None,
            version="1.0.0",
            dependencies=(
                "seasonal",
                "strength",
                "temperature",
                "pattern",
                "useful_god",
                "luck_cycle",
            ),
            produced_outputs=(),
            consumed_outputs=(),
            enabled=False,
        ),
        StageRecord(
            stage_id="report",
            package_id=None,
            version="1.0.0",
            dependencies=("interpretation",),
            produced_outputs=(),
            consumed_outputs=(),
            enabled=False,
        ),
    )


class CanonicalStageRegistry:
    """Canonical catalog of Analysis Pipeline stages."""

    def __init__(self, records: Iterable[StageRecord] | None = None) -> None:
        """Index stage records by identifier."""
        ordered = tuple(records) if records is not None else _default_records()
        self._records = {record.stage_id: record for record in ordered}
        self._order = tuple(record.stage_id for record in ordered)

    @classmethod
    def default(cls) -> CanonicalStageRegistry:
        """Return the sealed AX-2 catalog."""
        return cls()

    @property
    def pipeline_id(self) -> str:
        """Return the canonical pipeline identifier."""
        return PIPELINE_ID_V2

    @property
    def pipeline_version(self) -> str:
        """Return the canonical pipeline version."""
        return PIPELINE_VERSION_V2

    @property
    def canonical_order(self) -> tuple[str, ...]:
        """Return catalog order including inactive future stages."""
        return self._order

    def get(self, stage_id: str) -> StageRecord:
        """Return one catalog record or raise."""
        record = self._records.get(stage_id)
        if record is None:
            raise DependencyViolationError(f"unknown_stages:{stage_id}")
        return record

    def list_stages(self) -> tuple[StageRecord, ...]:
        """Return every registered stage in catalog order."""
        return tuple(self._records[stage_id] for stage_id in self._order)

    def enabled_stage_ids(self) -> tuple[str, ...]:
        """Return enabled stage identifiers."""
        return tuple(
            record.stage_id for record in self.list_stages() if record.enabled
        )

    def disabled_stage_ids(self) -> tuple[str, ...]:
        """Return registered but inactive stage identifiers."""
        return tuple(
            record.stage_id for record in self.list_stages() if not record.enabled
        )

    def package_ids(self, stage_ids: Iterable[str] | None = None) -> tuple[str, ...]:
        """Return package identifiers for the requested stages."""
        selected = tuple(stage_ids) if stage_ids is not None else self.enabled_stage_ids()
        package_ids: list[str] = []
        for stage_id in selected:
            record = self.get(stage_id)
            if record.package_id:
                package_ids.append(record.package_id)
        return tuple(package_ids)

    def dependency_map(self) -> dict[str, tuple[str, ...]]:
        """Return stage_id → direct dependencies."""
        return {
            record.stage_id: record.dependencies for record in self.list_stages()
        }

    def resolve_order(self, requested_stages: Iterable[str]) -> tuple[str, ...]:
        """Sort requested stages into catalog order and check prerequisites."""
        requested = tuple(requested_stages)
        unknown = [stage_id for stage_id in requested if stage_id not in self._records]
        if unknown:
            raise DependencyViolationError(f"unknown_stages:{','.join(unknown)}")
        duplicates = sorted(
            {stage_id for stage_id in requested if requested.count(stage_id) > 1}
        )
        if duplicates:
            raise DependencyViolationError(f"duplicate_stages:{','.join(duplicates)}")
        selected = set(requested)
        order = tuple(stage_id for stage_id in self._order if stage_id in selected)
        positions = {stage_id: index for index, stage_id in enumerate(order)}
        for stage_id in order:
            for dependency in self.get(stage_id).dependencies:
                if dependency not in positions:
                    raise DependencyViolationError(
                        f"missing_prerequisite:{stage_id}:{dependency}"
                    )
                if positions[dependency] >= positions[stage_id]:
                    raise DependencyViolationError(
                        f"order_violation:{dependency}:{stage_id}"
                    )
        return order

    def as_mapping(self) -> Mapping[str, Mapping[str, object]]:
        """Return a JSON-friendly catalog snapshot."""
        return {
            record.stage_id: record.to_dict() for record in self.list_stages()
        }
