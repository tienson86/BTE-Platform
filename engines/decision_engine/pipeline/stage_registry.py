"""Canonical stage catalog for Decision Packages."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Mapping

from engines.decision_engine.exceptions import DependencyViolationError

PIPELINE_ID = "canonical_decision_pipeline"
PIPELINE_VERSION = "1.0.0"

CANONICAL_STAGE_ORDER: tuple[str, ...] = (
    "useful_god_foundation",
    "useful_god_priority",
    "useful_god_override",
    "luck_cycle",
    "annual_luck",
    "monthly_luck",
    "interpretation",
)

ACTIVE_DECISION_STAGES: tuple[str, ...] = (
    "useful_god_foundation",
    "useful_god_priority",
    "useful_god_override",
)

INACTIVE_FUTURE_STAGES: tuple[str, ...] = (
    "luck_cycle",
    "annual_luck",
    "monthly_luck",
    "interpretation",
)

FOUNDATION_INPUTS: tuple[str, ...] = (
    "season_score",
    "strength_score",
    "temperature_score",
    "pattern_score",
    "pattern_quality",
    "pattern_confidence",
    "pattern_integrity",
    "pattern_stability",
)
FOUNDATION_OUTPUTS: tuple[str, ...] = (
    "useful_god",
    "favorable_gods",
    "unfavorable_gods",
    "decision_confidence",
    "decision_score",
    "decision_reasoning",
    "decision_diagnostics",
)
PRIORITY_INPUTS: tuple[str, ...] = FOUNDATION_INPUTS + (
    "useful_god",
    "favorable_gods",
    "unfavorable_gods",
    "decision_confidence",
    "decision_score",
    "decision_reasoning",
    "decision_diagnostics",
)
PRIORITY_OUTPUTS: tuple[str, ...] = (
    "resolved_useful_god",
    "resolved_favorable_gods",
    "resolved_unfavorable_gods",
    "decision_priority",
    "conflict_resolution",
    "resolution_confidence",
    "resolution_reasoning",
    "resolution_diagnostics",
)
OVERRIDE_INPUTS: tuple[str, ...] = (
    "season_score",
    "strength_score",
    "temperature_score",
    "pattern_score",
    "pattern_quality",
    "pattern_confidence",
    "resolved_useful_god",
    "decision_priority",
    "resolution_confidence",
    "resolution_reasoning",
    "resolution_diagnostics",
)
OVERRIDE_OUTPUTS: tuple[str, ...] = (
    "final_useful_god",
    "final_favorable_gods",
    "final_unfavorable_gods",
    "override_applied",
    "override_reason",
    "override_confidence",
    "decision_trace",
    "decision_audit",
)


@dataclass(frozen=True, slots=True)
class DecisionStageRecord:
    """Immutable catalog entry for one decision stage."""

    stage_id: str
    package_id: str | None
    package_version: str
    dependencies: tuple[str, ...]
    published_inputs: tuple[str, ...]
    published_outputs: tuple[str, ...]
    enabled: bool

    def to_dict(self) -> dict[str, object]:
        """Serialize the catalog record."""
        return {
            "stage_id": self.stage_id,
            "package_id": self.package_id,
            "package_version": self.package_version,
            "dependencies": list(self.dependencies),
            "published_inputs": list(self.published_inputs),
            "published_outputs": list(self.published_outputs),
            "enabled": self.enabled,
        }


def _default_records() -> tuple[DecisionStageRecord, ...]:
    return (
        DecisionStageRecord(
            stage_id="useful_god_foundation",
            package_id="bz_06_useful_god_foundation",
            package_version="1.0.0",
            dependencies=(),
            published_inputs=FOUNDATION_INPUTS,
            published_outputs=FOUNDATION_OUTPUTS,
            enabled=True,
        ),
        DecisionStageRecord(
            stage_id="useful_god_priority",
            package_id="bz_07_useful_god_priority",
            package_version="1.0.0",
            dependencies=("useful_god_foundation",),
            published_inputs=PRIORITY_INPUTS,
            published_outputs=PRIORITY_OUTPUTS,
            enabled=True,
        ),
        DecisionStageRecord(
            stage_id="useful_god_override",
            package_id="bz_08_useful_god_override",
            package_version="1.0.0",
            dependencies=("useful_god_foundation", "useful_god_priority"),
            published_inputs=OVERRIDE_INPUTS,
            published_outputs=OVERRIDE_OUTPUTS,
            enabled=True,
        ),
        DecisionStageRecord(
            stage_id="luck_cycle",
            package_id=None,
            package_version="1.0.0",
            dependencies=("useful_god_override",),
            published_inputs=("final_useful_god",),
            published_outputs=(),
            enabled=False,
        ),
        DecisionStageRecord(
            stage_id="annual_luck",
            package_id=None,
            package_version="1.0.0",
            dependencies=("luck_cycle",),
            published_inputs=(),
            published_outputs=(),
            enabled=False,
        ),
        DecisionStageRecord(
            stage_id="monthly_luck",
            package_id=None,
            package_version="1.0.0",
            dependencies=("annual_luck",),
            published_inputs=(),
            published_outputs=(),
            enabled=False,
        ),
        DecisionStageRecord(
            stage_id="interpretation",
            package_id=None,
            package_version="1.0.0",
            dependencies=("useful_god_override", "luck_cycle"),
            published_inputs=("final_useful_god",),
            published_outputs=(),
            enabled=False,
        ),
    )


class DecisionStageRegistry:
    """Canonical catalog of Decision Pipeline stages."""

    def __init__(self, records: Iterable[DecisionStageRecord] | None = None) -> None:
        """Index stage records by identifier."""
        ordered = tuple(records) if records is not None else _default_records()
        self._records = {record.stage_id: record for record in ordered}
        self._order = tuple(record.stage_id for record in ordered)

    @classmethod
    def default(cls) -> DecisionStageRegistry:
        """Return the sealed AX-3 catalog."""
        return cls()

    @property
    def pipeline_id(self) -> str:
        """Return the canonical pipeline identifier."""
        return PIPELINE_ID

    @property
    def pipeline_version(self) -> str:
        """Return the canonical pipeline version."""
        return PIPELINE_VERSION

    @property
    def canonical_order(self) -> tuple[str, ...]:
        """Return catalog order including inactive future stages."""
        return self._order

    def get(self, stage_id: str) -> DecisionStageRecord:
        """Return one catalog record or raise."""
        record = self._records.get(stage_id)
        if record is None:
            raise DependencyViolationError(f"unknown_stages:{stage_id}")
        return record

    def list_stages(self) -> tuple[DecisionStageRecord, ...]:
        """Return every registered stage in catalog order."""
        return tuple(self._records[stage_id] for stage_id in self._order)

    def enabled_stage_ids(self) -> tuple[str, ...]:
        """Return enabled stage identifiers."""
        return tuple(record.stage_id for record in self.list_stages() if record.enabled)

    def disabled_stage_ids(self) -> tuple[str, ...]:
        """Return registered but inactive stage identifiers."""
        return tuple(record.stage_id for record in self.list_stages() if not record.enabled)

    def resolve_order(self, requested_stages: Iterable[str]) -> tuple[str, ...]:
        """Sort requested stages into catalog order and check prerequisites."""
        requested = tuple(requested_stages)
        unknown = [stage_id for stage_id in requested if stage_id not in self._records]
        if unknown:
            raise DependencyViolationError(f"unknown_stages:{','.join(unknown)}")
        duplicates = sorted({sid for sid in requested if requested.count(sid) > 1})
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
        return {record.stage_id: record.to_dict() for record in self.list_stages()}
