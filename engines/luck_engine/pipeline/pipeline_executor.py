"""Deterministic Canonical Luck Pipeline executor."""

from __future__ import annotations

from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any

from engines.luck_engine.exceptions import (
    LuckContractViolationError,
    LuckDuplicatePublicationError,
    LuckPipelineError,
)
from engines.luck_engine.pipeline.diagnostics import LuckPipelineDiagnostic
from engines.luck_engine.pipeline.luck_trace import LuckTraceStep
from engines.luck_engine.pipeline.package_contract import LuckPackageContractVerifier
from engines.luck_engine.pipeline.stage_registry import LuckStageRecord, LuckStageRegistry
from engines.luck_engine.timeline.package_loader import LoadedLuckPackage

StageHandler = Callable[["LuckPipelineContext"], Mapping[str, Any]]


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


def _iso(moment: datetime) -> str:
    return moment.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


@dataclass
class LuckPipelineContext:
    """Append-only luck pipeline context. Upstream outputs are immutable."""

    timeline_input: Any = None
    analysis_input: Any = None
    decision_input: Any = None
    diagnostics: list[LuckPipelineDiagnostic] = field(default_factory=list)
    _outputs: dict[str, Any] = field(default_factory=dict, repr=False)
    _stage_payloads: dict[str, dict[str, Any]] = field(default_factory=dict, repr=False)
    _field_owners: dict[str, str] = field(default_factory=dict, repr=False)

    def add_diagnostic(self, item: LuckPipelineDiagnostic) -> None:
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
            raise LuckDuplicatePublicationError(f"duplicate_execution:{stage_id}")
        snapshot = dict(payload)
        for name in declared_outputs:
            if name in self._field_owners:
                raise LuckDuplicatePublicationError(
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
    def timeline_result(self) -> dict[str, Any] | None:
        """Published timeline snapshot."""
        value = self.get_output("timeline_result")
        return value if isinstance(value, dict) else None

    @property
    def analysis_result(self) -> dict[str, Any] | None:
        """Published luck analysis snapshot."""
        value = self.get_output("analysis_result")
        return value if isinstance(value, dict) else None

    @property
    def decision_result(self) -> dict[str, Any] | None:
        """Published luck decision snapshot."""
        value = self.get_output("decision_result")
        return value if isinstance(value, dict) else None


class LuckPipelineExecutor:
    """Execute enabled luck stages once, in dependency order only."""

    def __init__(
        self,
        *,
        verifier: LuckPackageContractVerifier | None = None,
        clock: Callable[[], datetime] | None = None,
    ) -> None:
        """Initialize contract verification and trace clock."""
        self._verifier = verifier or LuckPackageContractVerifier()
        self._clock = clock or _utc_now

    def execute(
        self,
        *,
        registry: LuckStageRegistry,
        stage_order: Sequence[str],
        context: LuckPipelineContext,
        packages: Mapping[str, LoadedLuckPackage],
        handlers: Mapping[str, StageHandler],
    ) -> tuple[LuckTraceStep, ...]:
        """Execute each enabled stage once. Disabled stages are skipped."""
        steps: list[LuckTraceStep] = []
        for stage_id in stage_order:
            record = registry.get(stage_id)
            if not record.enabled:
                continue
            if context.has_stage(stage_id):
                raise LuckDuplicatePublicationError(f"duplicate_execution:{stage_id}")
            started_at = _iso(self._clock())
            self._verify_stage(record, context, packages)
            handler = handlers.get(stage_id)
            if handler is None:
                raise LuckPipelineError(f"missing_stage_handler:{stage_id}")
            payload = handler(context)
            self._verifier.verify_payload(payload, record)
            context.publish(stage_id, payload, declared_outputs=record.published_outputs)
            completed_at = _iso(self._clock())
            steps.append(
                LuckTraceStep(
                    stage_id=stage_id,
                    component=record.component,
                    version=self._component_version(record, packages),
                    executed=True,
                    outputs_published=record.published_outputs,
                    started_at=started_at,
                    completed_at=completed_at,
                )
            )
        return tuple(steps)

    def _verify_stage(
        self,
        record: LuckStageRecord,
        context: LuckPipelineContext,
        packages: Mapping[str, LoadedLuckPackage],
    ) -> None:
        if record.package_id is not None:
            package = packages.get(record.package_id)
            if package is None:
                raise LuckContractViolationError(f"package_not_loaded:{record.package_id}")
            self._verifier.verify_timeline_package(package)
            return
        if record.stage_id == "analysis":
            if not isinstance(context.analysis_input, Mapping):
                return
            self._verifier.verify_analysis_component(
                analysis_version="1.0.0",
                ax2_version=str(context.analysis_input.get("pipeline_version") or ""),
            )
            return
        if record.stage_id == "decision":
            if not isinstance(context.decision_input, Mapping):
                return
            self._verifier.verify_decision_component(
                decision_version="1.0.0",
                ax3_version=str(context.decision_input.get("decision_pipeline_version") or ""),
            )

    def _component_version(
        self,
        record: LuckStageRecord,
        packages: Mapping[str, LoadedLuckPackage],
    ) -> str:
        if record.package_id is None:
            return record.version
        package = packages.get(record.package_id)
        return record.version if package is None else package.package_version
