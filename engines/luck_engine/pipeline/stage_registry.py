"""Canonical stage catalog for the AX-4 Luck Pipeline."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Sequence

from engines.luck_engine.exceptions import LuckDependencyViolationError, LuckPipelineError

PIPELINE_ID = "canonical_luck_pipeline"
PIPELINE_VERSION = "1.0.0"

STAGE_TIMELINE = "timeline"
STAGE_ANALYSIS = "analysis"
STAGE_DECISION = "decision"
STAGE_INTERPRETATION = "interpretation"
STAGE_REPORT = "report"

CANONICAL_STAGE_ORDER: tuple[str, ...] = (
    STAGE_TIMELINE,
    STAGE_ANALYSIS,
    STAGE_DECISION,
    STAGE_INTERPRETATION,
    STAGE_REPORT,
)

ACTIVE_LUCK_STAGES: tuple[str, ...] = (
    STAGE_TIMELINE,
    STAGE_ANALYSIS,
    STAGE_DECISION,
)

INACTIVE_FUTURE_STAGES: tuple[str, ...] = (
    STAGE_INTERPRETATION,
    STAGE_REPORT,
)


@dataclass(frozen=True, slots=True)
class LuckStageRecord:
    """Immutable catalog entry for one luck pipeline stage."""

    stage_id: str
    component: str
    version: str
    dependencies: tuple[str, ...]
    consumed_inputs: tuple[str, ...]
    published_outputs: tuple[str, ...]
    enabled: bool
    package_id: str | None = None

    def to_dict(self) -> dict[str, object]:
        """Serialize the catalog record."""
        return {
            "stage_id": self.stage_id,
            "component": self.component,
            "version": self.version,
            "dependencies": list(self.dependencies),
            "consumed_inputs": list(self.consumed_inputs),
            "published_outputs": list(self.published_outputs),
            "enabled": self.enabled,
            "package_id": self.package_id,
        }


def _default_records() -> tuple[LuckStageRecord, ...]:
    return (
        LuckStageRecord(
            stage_id=STAGE_TIMELINE,
            component="luck_timeline_foundation",
            version="1.0.0",
            dependencies=(),
            consumed_inputs=("natal_chart", "major_cycles", "annual_cycles", "monthly_cycles"),
            published_outputs=("timeline_result",),
            enabled=True,
            package_id="bz_09_luck_foundation",
        ),
        LuckStageRecord(
            stage_id=STAGE_ANALYSIS,
            component="luck_analysis_engine",
            version="1.0.0",
            dependencies=(STAGE_TIMELINE,),
            consumed_inputs=("timeline_result", "canonical_analysis_result", "canonical_decision_result"),
            published_outputs=("analysis_result",),
            enabled=True,
            package_id=None,
        ),
        LuckStageRecord(
            stage_id=STAGE_DECISION,
            component="luck_decision_engine",
            version="1.0.0",
            dependencies=(STAGE_TIMELINE, STAGE_ANALYSIS),
            consumed_inputs=("timeline_result", "analysis_result", "canonical_analysis_result", "canonical_decision_result"),
            published_outputs=("decision_result",),
            enabled=True,
            package_id=None,
        ),
        LuckStageRecord(
            stage_id=STAGE_INTERPRETATION,
            component="interpretation_engine",
            version="1.0.0",
            dependencies=(STAGE_DECISION,),
            consumed_inputs=("decision_result",),
            published_outputs=("interpretation_result",),
            enabled=False,
            package_id=None,
        ),
        LuckStageRecord(
            stage_id=STAGE_REPORT,
            component="report_engine",
            version="1.0.0",
            dependencies=(STAGE_INTERPRETATION,),
            consumed_inputs=("interpretation_result",),
            published_outputs=("report_result",),
            enabled=False,
            package_id=None,
        ),
    )


class LuckStageRegistry:
    """Read-only registry of Canonical Luck Pipeline stages."""

    def __init__(self, records: Iterable[LuckStageRecord] | None = None) -> None:
        """Load default or injected catalog records."""
        catalog = tuple(records) if records is not None else _default_records()
        ids = [item.stage_id for item in catalog]
        if len(ids) != len(set(ids)):
            raise LuckPipelineError("duplicate_stage_id")
        by_id = {item.stage_id: item for item in catalog}
        ordered = tuple(by_id[stage_id] for stage_id in CANONICAL_STAGE_ORDER if stage_id in by_id)
        extra = tuple(item for item in catalog if item.stage_id not in CANONICAL_STAGE_ORDER)
        self._records = ordered + extra
        self._by_id = {item.stage_id: item for item in self._records}

    @classmethod
    def default(cls) -> LuckStageRegistry:
        """Return the frozen default catalog."""
        return cls()

    def get(self, stage_id: str) -> LuckStageRecord:
        """Return one stage record or raise."""
        try:
            return self._by_id[stage_id]
        except KeyError as exc:
            raise LuckDependencyViolationError(f"unknown_stage:{stage_id}") from exc

    def disabled_stage_ids(self) -> tuple[str, ...]:
        """Return registered but inactive stage identifiers."""
        return tuple(item.stage_id for item in self._records if not item.enabled)

    def enabled_stage_ids(self) -> tuple[str, ...]:
        """Return enabled stage identifiers in catalog order."""
        return tuple(item.stage_id for item in self._records if item.enabled)

    def resolve_order(self, requested: Sequence[str]) -> tuple[str, ...]:
        """Return requested enabled stages in dependency order."""
        requested_set = set(requested)
        ordered: list[str] = []
        for stage_id in CANONICAL_STAGE_ORDER:
            if stage_id not in requested_set:
                continue
            record = self.get(stage_id)
            if not record.enabled:
                continue
            missing = [dep for dep in record.dependencies if dep not in ordered]
            if missing:
                raise LuckDependencyViolationError(
                    f"missing_inputs:{stage_id}:{','.join(missing)}"
                )
            ordered.append(stage_id)
        unknown = requested_set - set(CANONICAL_STAGE_ORDER) - set(self._by_id)
        if unknown:
            raise LuckDependencyViolationError(f"unknown_stages:{','.join(sorted(unknown))}")
        extra = [item for item in requested if item not in ordered and item in requested_set]
        for stage_id in extra:
            record = self.get(stage_id)
            if record.enabled:
                missing = [dep for dep in record.dependencies if dep not in ordered]
                if missing:
                    raise LuckDependencyViolationError(
                        f"missing_inputs:{stage_id}:{','.join(missing)}"
                    )
                ordered.append(stage_id)
        return tuple(ordered)

    def to_list(self) -> list[dict[str, object]]:
        """Serialize the full registry."""
        return [item.to_dict() for item in self._records]
