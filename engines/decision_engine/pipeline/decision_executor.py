"""Deterministic Decision Pipeline executor."""

from __future__ import annotations

from collections.abc import Callable, Mapping, Sequence
from datetime import datetime, timezone
from typing import Any

from engines.decision_engine.exceptions import (
    ContractViolationError,
    DuplicatePublicationError,
    DecisionPipelineError,
)
from engines.decision_engine.pipeline.decision_context import DecisionExecutionContext
from engines.decision_engine.pipeline.decision_trace import DecisionTraceStep, build_trace_steps
from engines.decision_engine.pipeline.package_contract import DecisionPackageContractVerifier
from engines.decision_engine.pipeline.package_loader import LoadedPackage
from engines.decision_engine.pipeline.stage_registry import DecisionStageRegistry

StageHandler = Callable[..., Mapping[str, Any]]


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


class DecisionExecutor:
    """Execute enabled stages once, in dependency order, with immutable outputs."""

    def __init__(
        self,
        *,
        verifier: DecisionPackageContractVerifier | None = None,
        clock: Callable[[], datetime] | None = None,
    ) -> None:
        """Initialize contract verification and trace clock."""
        self._verifier = verifier or DecisionPackageContractVerifier()
        self._clock = clock or _utc_now

    def execute(
        self,
        *,
        registry: DecisionStageRegistry,
        stage_order: Sequence[str],
        context: DecisionExecutionContext,
        packages: Mapping[str, LoadedPackage],
        handlers: Mapping[str, StageHandler],
    ) -> tuple[DecisionTraceStep, ...]:
        """Execute enabled stages once. Disabled stages are skipped."""
        steps: list[DecisionTraceStep] = []
        for stage_id in stage_order:
            record = registry.get(stage_id)
            if not record.enabled:
                continue
            if context.has_result(stage_id):
                raise DuplicatePublicationError(f"duplicate_execution:{stage_id}")
            package = self._package_for(record.package_id, packages)
            if package is not None:
                self._verifier.verify(
                    package,
                    stage=record,
                    loaded_packages=packages,
                )
            handler = handlers.get(stage_id)
            if handler is None:
                raise DecisionPipelineError(f"missing_stage_handler:{stage_id}")
            payload = (
                handler(context, package)
                if package is not None
                else handler(context)
            )
            self._verifier.verify_payload(payload, record)
            published = tuple(payload.get("produced_signals") or record.published_outputs)
            timestamp = self._clock().isoformat()
            steps.extend(
                build_trace_steps(
                    stage_id=stage_id,
                    package_id=record.package_id,
                    package_version=None if package is None else package.package_version,
                    rule_ids=tuple(payload.get("rule_ids") or (package.rule_ids if package else ())),
                    outputs=published,
                    timestamp=timestamp,
                    payload={"status": payload.get("status")},
                )
            )
        return tuple(steps)

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
