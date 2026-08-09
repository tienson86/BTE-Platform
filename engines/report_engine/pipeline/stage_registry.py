"""Canonical stage catalog for the RX-1 Report Pipeline."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Sequence

from engines.report_engine.pipeline.diagnostics import (
    CanonicalReportPipelineError,
    ReportDependencyViolationError,
)

PIPELINE_ID = "canonical_report_pipeline"
PIPELINE_VERSION = "1.0.0"

STAGE_FOUNDATION = "foundation"
STAGE_LAYOUT = "layout"
STAGE_RENDERING = "rendering"
STAGE_PUBLISHER = "publisher"
STAGE_DELIVERY = "delivery"
STAGE_PRINT = "print"

CANONICAL_STAGE_ORDER: tuple[str, ...] = (
    STAGE_FOUNDATION,
    STAGE_LAYOUT,
    STAGE_RENDERING,
    STAGE_PUBLISHER,
    STAGE_DELIVERY,
    STAGE_PRINT,
)

ACTIVE_REPORT_STAGES: tuple[str, ...] = (
    STAGE_FOUNDATION,
    STAGE_LAYOUT,
    STAGE_RENDERING,
)

INACTIVE_FUTURE_STAGES: tuple[str, ...] = (
    STAGE_PUBLISHER,
    STAGE_DELIVERY,
    STAGE_PRINT,
)


@dataclass(frozen=True, slots=True)
class ReportStageRecord:
    """Immutable catalog entry for one report pipeline stage."""

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


def _default_records() -> tuple[ReportStageRecord, ...]:
    upstream = (
        "canonical_analysis_result",
        "canonical_decision_result",
        "canonical_luck_result",
        "canonical_interpretation_result",
    )
    return (
        ReportStageRecord(
            stage_id=STAGE_FOUNDATION,
            component="report_foundation",
            version="1.0.0",
            dependencies=(),
            consumed_inputs=upstream,
            published_outputs=("foundation_result",),
            enabled=True,
        ),
        ReportStageRecord(
            stage_id=STAGE_LAYOUT,
            component="report_layout_engine",
            version="1.0.0",
            dependencies=(STAGE_FOUNDATION,),
            consumed_inputs=upstream + ("foundation_result",),
            published_outputs=("layout_result",),
            enabled=True,
        ),
        ReportStageRecord(
            stage_id=STAGE_RENDERING,
            component="report_rendering_engine",
            version="1.0.0",
            dependencies=(STAGE_FOUNDATION, STAGE_LAYOUT),
            consumed_inputs=("layout_result",),
            published_outputs=("rendering_result",),
            enabled=True,
        ),
        ReportStageRecord(
            stage_id=STAGE_PUBLISHER,
            component="cloud_publisher",
            version="1.0.0",
            dependencies=(STAGE_RENDERING,),
            consumed_inputs=("rendering_result",),
            published_outputs=("publisher_result",),
            enabled=False,
        ),
        ReportStageRecord(
            stage_id=STAGE_DELIVERY,
            component="email_delivery",
            version="1.0.0",
            dependencies=(STAGE_RENDERING,),
            consumed_inputs=("rendering_result",),
            published_outputs=("delivery_result",),
            enabled=False,
        ),
        ReportStageRecord(
            stage_id=STAGE_PRINT,
            component="print_engine",
            version="1.0.0",
            dependencies=(STAGE_RENDERING,),
            consumed_inputs=("rendering_result",),
            published_outputs=("print_result",),
            enabled=False,
        ),
    )


class ReportStageRegistry:
    """Read-only registry of Canonical Report Pipeline stages."""

    def __init__(self, records: Iterable[ReportStageRecord] | None = None) -> None:
        """Load default or injected catalog records."""
        catalog = tuple(records) if records is not None else _default_records()
        ids = [item.stage_id for item in catalog]
        if len(ids) != len(set(ids)):
            raise CanonicalReportPipelineError("duplicate_stage_id")
        by_id = {item.stage_id: item for item in catalog}
        ordered = tuple(by_id[stage_id] for stage_id in CANONICAL_STAGE_ORDER if stage_id in by_id)
        extra = tuple(item for item in catalog if item.stage_id not in CANONICAL_STAGE_ORDER)
        self._records = ordered + extra
        self._by_id = {item.stage_id: item for item in self._records}

    @classmethod
    def default(cls) -> ReportStageRegistry:
        """Return the frozen default catalog."""
        return cls()

    def get(self, stage_id: str) -> ReportStageRecord:
        """Return one stage record or raise."""
        try:
            return self._by_id[stage_id]
        except KeyError as exc:
            raise ReportDependencyViolationError(f"unknown_stage:{stage_id}") from exc

    def disabled_stage_ids(self) -> tuple[str, ...]:
        """Return registered but inactive stage identifiers."""
        return tuple(item.stage_id for item in self._records if not item.enabled)

    def resolve_order(self, requested: Sequence[str]) -> tuple[str, ...]:
        """Return requested enabled stages in dependency order."""
        requested_set = set(requested)
        unknown = requested_set - set(self._by_id)
        if unknown:
            raise ReportDependencyViolationError(f"unknown_stages:{','.join(sorted(unknown))}")
        ordered: list[str] = []
        for stage_id in CANONICAL_STAGE_ORDER:
            if stage_id not in requested_set:
                continue
            record = self.get(stage_id)
            if not record.enabled:
                continue
            missing = [dep for dep in record.dependencies if dep not in ordered]
            if missing:
                raise ReportDependencyViolationError(
                    f"missing_inputs:{stage_id}:{','.join(missing)}"
                )
            ordered.append(stage_id)
        return tuple(ordered)

    def to_list(self) -> list[dict[str, object]]:
        """Serialize the full registry."""
        return [item.to_dict() for item in self._records]
