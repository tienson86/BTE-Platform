"""Pipeline executor for multi-stage orchestration."""

from __future__ import annotations

from collections.abc import Callable, Mapping, Sequence
from datetime import datetime, timezone
from typing import Any

from engines.analysis_engine.exceptions.pipeline_error import (
    ContractViolationError,
    DuplicateExecutionError,
    PipelineError,
)
from engines.analysis_engine.pipeline.execution_context import (
    AnalysisExecutionContext,
    ExecutionContext,
)
from engines.analysis_engine.pipeline.execution_hooks import (
    ExecutionHooks,
    NoOpExecutionHooks,
)
from engines.analysis_engine.pipeline.execution_policy import ExecutionPolicy
from engines.analysis_engine.pipeline.execution_report import StageTraceEntry
from engines.analysis_engine.pipeline.execution_result import ExecutionResult
from engines.analysis_engine.pipeline.execution_state import ExecutionState
from engines.analysis_engine.pipeline.package_contract import PackageContractVerifier
from engines.analysis_engine.pipeline.package_loader import LoadedPackage
from engines.analysis_engine.pipeline.pipeline_result import StageOutcome
from engines.analysis_engine.pipeline.stage_base import StageBase
from engines.analysis_engine.pipeline.stage_executor import StageExecutor
from engines.analysis_engine.pipeline.stage_registry import CanonicalStageRegistry
from engines.analysis_engine.types.status import ExecutionStatus

StageHandler = Callable[..., Mapping[str, Any]]


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


class PipelineExecutor:
    """Orchestrates ordered stage execution without business analysis logic."""

    def __init__(
        self,
        *,
        stage_executor: StageExecutor | None = None,
        hooks: ExecutionHooks | None = None,
    ) -> None:
        """Initialize pipeline orchestration dependencies."""
        self._stage_executor = stage_executor or StageExecutor()
        self._hooks = hooks or NoOpExecutionHooks()

    def execute(
        self,
        *,
        stages: tuple[StageBase, ...],
        context: ExecutionContext,
    ) -> ExecutionResult:
        """Execute stages in deterministic order using immutable state transitions."""
        ordered = self._order_stages(stages, context.policy)
        self._validate_required_stages(ordered, context.policy)

        state = ExecutionState(
            execution_id=context.execution_id,
            pipeline_id=context.pipeline_id,
            status=ExecutionStatus.RUNNING,
            current_stage_id=None,
            completed_stage_ids=(),
            failed_stage_id=None,
            attempt=1,
        )
        self._hooks.before_pipeline(context, state)

        outcomes: list[StageOutcome] = []
        errors: list[str] = []
        current_context = context

        try:
            for stage in ordered:
                state = state.transition(
                    status=ExecutionStatus.RUNNING,
                    current_stage_id=stage.stage_id,
                )
                self._hooks.before_stage(stage, current_context, state)

                outcome = self._run_stage_with_retries(
                    stage=stage,
                    context=current_context,
                    policy=current_context.policy,
                )
                outcomes.append(outcome)
                self._hooks.after_stage(stage, current_context, state, outcome)

                if outcome.success:
                    current_context = current_context.with_stage_output(
                        stage.stage_id,
                        outcome.payload,
                    )
                    state = state.transition(
                        append_completed=stage.stage_id,
                        current_stage_id=None,
                    )
                    continue

                errors.extend(outcome.messages)
                state = state.transition(
                    status=ExecutionStatus.FAILED,
                    failed_stage_id=stage.stage_id,
                    current_stage_id=None,
                )
                if current_context.policy.fail_fast:
                    break

            result = self._build_result(
                context=current_context,
                state=state,
                outcomes=tuple(outcomes),
                errors=tuple(errors),
            )
        except Exception as exc:  # noqa: BLE001 - orchestration boundary
            self._hooks.on_error(None, current_context, state, exc)
            state = state.transition(status=ExecutionStatus.FAILED)
            result = ExecutionResult(
                execution_id=context.execution_id,
                pipeline_id=context.pipeline_id,
                success=False,
                status=ExecutionStatus.FAILED,
                outcomes=tuple(outcomes),
                errors=(f"pipeline_orchestration_error:{type(exc).__name__}:{exc}",),
                completed_stage_ids=state.completed_stage_ids,
                failed_stage_id=state.failed_stage_id,
                messages=("orchestration_failed",),
                metadata={},
            )

        self._hooks.after_pipeline(current_context, state, result)
        return result

    def _run_stage_with_retries(
        self,
        *,
        stage: StageBase,
        context: ExecutionContext,
        policy: ExecutionPolicy,
    ) -> StageOutcome:
        """Run a stage with policy-limited orchestration retries."""
        attempts = max(1, policy.max_attempts)
        last_outcome: StageOutcome | None = None
        pipeline_context = context.to_pipeline_context()

        for _attempt in range(1, attempts + 1):
            try:
                last_outcome = self._stage_executor.execute(stage, pipeline_context)
            except Exception as exc:  # noqa: BLE001 - stage boundary
                self._hooks.on_error(stage, context, ExecutionState(
                    execution_id=context.execution_id,
                    pipeline_id=context.pipeline_id,
                    status=ExecutionStatus.FAILED,
                    current_stage_id=stage.stage_id,
                ), exc)
                last_outcome = StageOutcome(
                    stage_id=stage.stage_id,
                    success=False,
                    payload={},
                    messages=(f"stage_orchestration_error:{type(exc).__name__}:{exc}",),
                )
            if last_outcome.success:
                return last_outcome

        assert last_outcome is not None
        return last_outcome

    def _order_stages(
        self,
        stages: tuple[StageBase, ...],
        policy: ExecutionPolicy,
    ) -> tuple[StageBase, ...]:
        """Order stages deterministically by order then stage_id."""
        if policy.deterministic:
            return tuple(sorted(stages, key=lambda stage: (stage.order, stage.stage_id)))
        return stages

    def _validate_required_stages(
        self,
        stages: tuple[StageBase, ...],
        policy: ExecutionPolicy,
    ) -> None:
        """Validate required stage identifiers are present."""
        available = {stage.stage_id for stage in stages}
        missing = tuple(
            stage_id
            for stage_id in policy.required_stage_ids
            if stage_id not in available
        )
        if missing:
            raise PipelineError(f"missing_required_stages:{','.join(missing)}")

    def _build_result(
        self,
        *,
        context: ExecutionContext,
        state: ExecutionState,
        outcomes: tuple[StageOutcome, ...],
        errors: tuple[str, ...],
    ) -> ExecutionResult:
        """Build an immutable execution result from orchestration state."""
        all_success = bool(outcomes) and all(item.success for item in outcomes)
        any_success = any(item.success for item in outcomes)
        if all_success:
            status = ExecutionStatus.SUCCEEDED
            success = True
        elif any_success and context.policy.allow_partial_success:
            status = ExecutionStatus.PARTIAL
            success = True
        elif not outcomes and not errors:
            status = ExecutionStatus.SUCCEEDED
            success = True
        else:
            status = ExecutionStatus.FAILED
            success = False

        return ExecutionResult(
            execution_id=context.execution_id,
            pipeline_id=context.pipeline_id,
            success=success,
            status=status,
            outcomes=outcomes,
            errors=errors,
            completed_stage_ids=state.completed_stage_ids,
            failed_stage_id=state.failed_stage_id,
            messages=(),
            metadata={"policy_id": context.policy.policy_id},
        )


class CanonicalPipelineExecutor:
    """Deterministic AX-2 executor: once, ordered, immutable, declared outputs."""

    def __init__(
        self,
        *,
        verifier: PackageContractVerifier | None = None,
        clock: Callable[[], datetime] | None = None,
    ) -> None:
        """Initialize contract verification and trace clock."""
        self._verifier = verifier or PackageContractVerifier()
        self._clock = clock or _utc_now

    def execute(
        self,
        *,
        registry: CanonicalStageRegistry,
        stage_order: Sequence[str],
        context: AnalysisExecutionContext,
        packages: Mapping[str, LoadedPackage],
        handlers: Mapping[str, StageHandler],
    ) -> tuple[tuple[StageOutcome, ...], tuple[StageTraceEntry, ...]]:
        """Execute enabled stages once in dependency order."""
        outcomes: list[StageOutcome] = []
        traces: list[StageTraceEntry] = []
        for stage_id in stage_order:
            record = registry.get(stage_id)
            started = self._clock().isoformat()
            if not record.enabled:
                traces.append(
                    StageTraceEntry(
                        stage_id=stage_id,
                        package_id=record.package_id,
                        package_version=None,
                        enabled=False,
                        executed=False,
                        started_at=started,
                        completed_at=self._clock().isoformat(),
                    )
                )
                continue
            if context.has_result(stage_id):
                raise DuplicateExecutionError(f"duplicate_execution:{stage_id}")
            package = self._package_for(record.package_id, packages)
            if package is not None:
                self._verifier.verify(
                    package,
                    stage=record,
                    loaded_packages=packages,
                )
            handler = handlers.get(stage_id)
            if handler is None:
                raise PipelineError(f"missing_stage_handler:{stage_id}")
            payload = handler(context, package) if package is not None else handler(context)
            self._verifier.verify_payload(payload, record)
            published = tuple(payload.get("produced_signals") or record.produced_outputs)
            outcomes.append(
                StageOutcome(
                    stage_id=stage_id,
                    success=True,
                    payload=dict(payload),
                    messages=(f"{stage_id}_completed",),
                )
            )
            traces.append(
                StageTraceEntry(
                    stage_id=stage_id,
                    package_id=record.package_id,
                    package_version=None if package is None else package.package_version,
                    enabled=True,
                    executed=True,
                    outputs_published=published,
                    started_at=started,
                    completed_at=self._clock().isoformat(),
                )
            )
        return tuple(outcomes), tuple(traces)

    def _package_for(
        self,
        package_id: str | None,
        packages: Mapping[str, LoadedPackage],
    ) -> LoadedPackage | None:
        if package_id is None:
            return None
        package = packages.get(package_id)
        if package is None:
            raise ContractViolationError(f"package_not_loaded:{package_id}")
        return package
