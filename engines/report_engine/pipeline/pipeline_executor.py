"""Deterministic Canonical Report Pipeline executor."""

from __future__ import annotations

from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any

from engines.report_engine.pipeline.diagnostics import (
    CanonicalReportPipelineError,
    ReportDuplicatePublicationError,
    ReportPipelineDiagnostic,
)
from engines.report_engine.pipeline.package_contract import ReportPackageContractVerifier
from engines.report_engine.pipeline.report_trace import ReportPipelineTraceStep
from engines.report_engine.pipeline.stage_registry import (
    STAGE_FOUNDATION,
    STAGE_LAYOUT,
    STAGE_RENDERING,
    ReportStageRecord,
    ReportStageRegistry,
)

StageHandler = Callable[["ReportPipelineContext"], Mapping[str, Any]]


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


def _iso(moment: datetime) -> str:
    return moment.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


@dataclass
class ReportPipelineContext:
    """Append-only report pipeline context. Upstream outputs are immutable."""

    analysis_input: Any = None
    decision_input: Any = None
    luck_input: Any = None
    interpretation_input: Any = None
    foundation_input: Any = None
    layout_input: Any = None
    rendering_input: Any = None
    renderer_id: str = "json"
    diagnostics: list[ReportPipelineDiagnostic] = field(default_factory=list)
    _outputs: dict[str, Any] = field(default_factory=dict, repr=False)
    _stage_payloads: dict[str, dict[str, Any]] = field(default_factory=dict, repr=False)
    _field_owners: dict[str, str] = field(default_factory=dict, repr=False)

    def add_diagnostic(self, item: ReportPipelineDiagnostic) -> None:
        """Append a structured diagnostic."""
        self.diagnostics.append(item)

    def publish(
        self,
        stage_id: str,
        payload: Mapping[str, Any],
        *,
        declared_outputs: tuple[str, ...],
    ) -> None:
        """Publish declared stage outputs once. Duplicate names are rejected."""
        if stage_id in self._stage_payloads:
            raise ReportDuplicatePublicationError(f"duplicate_execution:{stage_id}")
        snapshot = dict(payload)
        for name in declared_outputs:
            if name in self._field_owners:
                raise ReportDuplicatePublicationError(
                    f"duplicate_output:{name}:{self._field_owners[name]}:{stage_id}"
                )
            if name not in snapshot:
                continue
            self._field_owners[name] = stage_id
            value = snapshot[name]
            self._outputs[name] = dict(value) if isinstance(value, Mapping) else value
        self._stage_payloads[stage_id] = snapshot

    def get_output(self, name: str) -> Any:
        """Return a published output copy when present."""
        value = self._outputs.get(name)
        if isinstance(value, Mapping):
            return dict(value)
        return value

    def has_stage(self, stage_id: str) -> bool:
        """Return True when the stage has already published."""
        return stage_id in self._stage_payloads

    def published_stage_ids(self) -> tuple[str, ...]:
        """Return executed stage identifiers in publication order."""
        return tuple(self._stage_payloads)

    def published_output_names(self) -> tuple[str, ...]:
        """Return published output names in insertion order."""
        return tuple(self._outputs)

    @property
    def foundation_result(self) -> dict[str, Any] | None:
        """Published RE-1 foundation snapshot."""
        value = self.get_output("foundation_result")
        return value if isinstance(value, dict) else None

    @property
    def layout_result(self) -> dict[str, Any] | None:
        """Published RE-2 layout snapshot."""
        value = self.get_output("layout_result")
        return value if isinstance(value, dict) else None

    @property
    def rendering_result(self) -> dict[str, Any] | None:
        """Published RE-3 rendering snapshot."""
        value = self.get_output("rendering_result")
        return value if isinstance(value, dict) else None


class ReportPipelineExecutor:
    """Execute enabled report stages once, in dependency order only."""

    def __init__(
        self,
        *,
        verifier: ReportPackageContractVerifier | None = None,
        clock: Callable[[], datetime] | None = None,
    ) -> None:
        """Initialize contract verification and trace clock."""
        self._verifier = verifier or ReportPackageContractVerifier()
        self._clock = clock or _utc_now

    def execute(
        self,
        *,
        registry: ReportStageRegistry,
        stage_order: Sequence[str],
        context: ReportPipelineContext,
        handlers: Mapping[str, StageHandler],
    ) -> tuple[ReportPipelineTraceStep, ...]:
        """Execute each enabled stage once. Disabled stages are skipped."""
        steps: list[ReportPipelineTraceStep] = []
        for stage_id in stage_order:
            record = registry.get(stage_id)
            if not record.enabled:
                continue
            if context.has_stage(stage_id):
                raise ReportDuplicatePublicationError(f"duplicate_execution:{stage_id}")
            started_at = _iso(self._clock())
            self._verify_stage(record, context)
            handler = handlers.get(stage_id)
            if handler is None:
                raise CanonicalReportPipelineError(f"missing_stage_handler:{stage_id}")
            payload = handler(context)
            self._verifier.verify_payload(payload, record)
            context.publish(stage_id, payload, declared_outputs=record.published_outputs)
            completed_at = _iso(self._clock())
            steps.append(
                ReportPipelineTraceStep(
                    stage_id=stage_id,
                    component=record.component,
                    version=record.version,
                    executed=True,
                    outputs_published=record.published_outputs,
                    started_at=started_at,
                    completed_at=completed_at,
                )
            )
        return tuple(steps)

    def _verify_stage(self, record: ReportStageRecord, context: ReportPipelineContext) -> None:
        ax2 = _version(context.analysis_input, "pipeline_version")
        ax3 = _version(context.decision_input, "decision_pipeline_version")
        ax4 = _version(context.luck_input, "luck_pipeline_version")
        ix1 = _interpretation_version(context.interpretation_input)
        if record.stage_id == STAGE_FOUNDATION:
            self._verifier.verify_foundation_component(report_version="1.0.0")
            if not isinstance(context.analysis_input, Mapping):
                return
            self._verifier.verify_layout_component(
                layout_version="1.0.0",
                ax2_version=ax2,
                ax3_version=ax3,
                ax4_version=ax4,
                ix1_version=ix1,
            )
            return
        if record.stage_id == STAGE_LAYOUT:
            if not isinstance(context.analysis_input, Mapping):
                return
            self._verifier.verify_layout_component(
                layout_version="1.0.0",
                ax2_version=ax2,
                ax3_version=ax3,
                ax4_version=ax4,
                ix1_version=ix1,
            )
            return
        if record.stage_id == STAGE_RENDERING:
            if not isinstance(context.analysis_input, Mapping) and context.layout_input is None:
                return
            if not isinstance(context.analysis_input, Mapping):
                return
            self._verifier.verify_rendering_component(
                render_version="1.0.0",
                ax2_version=ax2,
                ax3_version=ax3,
                ax4_version=ax4,
                ix1_version=ix1,
            )


def _version(value: Any, key: str) -> str:
    if isinstance(value, Mapping):
        return str(value.get(key) or "")
    return ""


def _interpretation_version(value: Any) -> str:
    if not isinstance(value, Mapping):
        return ""
    return str(
        value.get("interpretation_pipeline_version") or value.get("interpretation_version") or ""
    )
