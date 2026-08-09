"""Canonical Decision Pipeline (Sprint AX-3)."""

from __future__ import annotations

import logging
from datetime import datetime, timezone
from typing import Any, Callable, Mapping, Sequence

from engines.decision_engine.exceptions import (
    ContractViolationError,
    DecisionPipelineError,
    DependencyViolationError,
    DuplicatePublicationError,
    IncompatiblePackageError,
    PackageLoadError,
)
from engines.decision_engine.integration.foundation_stage import UsefulGodFoundationStage
from engines.decision_engine.integration.override_stage import UsefulGodOverrideStage
from engines.decision_engine.integration.priority_stage import UsefulGodPriorityStage
from engines.decision_engine.pipeline.decision_audit import failing_audit, passing_audit
from engines.decision_engine.pipeline.decision_context import DecisionExecutionContext
from engines.decision_engine.pipeline.decision_executor import DecisionExecutor
from engines.decision_engine.pipeline.decision_result import (
    CanonicalDecisionResult,
    build_decision_result,
)
from engines.decision_engine.pipeline.decision_trace import DecisionTrace
from engines.decision_engine.pipeline.diagnostics import (
    DecisionDiagnostic,
    disabled_stage_diagnostic,
    execution_order_diagnostic,
    pipeline_fail_diagnostic,
    pipeline_ok_diagnostic,
)
from engines.decision_engine.pipeline.package_contract import DecisionPackageContractVerifier
from engines.decision_engine.pipeline.package_loader import DecisionPackageLoader, LoadedPackage
from engines.decision_engine.pipeline.stage_registry import (
    ACTIVE_DECISION_STAGES,
    PIPELINE_ID,
    PIPELINE_VERSION,
    DecisionStageRegistry,
)

logger = logging.getLogger(__name__)


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


class CanonicalDecisionPipeline:
    """Only supported AX-3 execution model for released Decision Packages.

    Packages bind through orchestration. Decision rule logic is unchanged.
    Exceptions are converted to diagnostics and never leave ``run``.
    """

    pipeline_id: str = PIPELINE_ID
    pipeline_version: str = PIPELINE_VERSION

    def __init__(
        self,
        *,
        loader: DecisionPackageLoader | None = None,
        registry: DecisionStageRegistry | None = None,
        verifier: DecisionPackageContractVerifier | None = None,
        executor: DecisionExecutor | None = None,
        active_stages: Sequence[str] | None = None,
        version_constraints: Mapping[str, str] | None = None,
        clock: Callable[[], datetime] | None = None,
    ) -> None:
        """Initialize canonical decision orchestration dependencies."""
        self._loader = loader or DecisionPackageLoader()
        self._registry = registry or DecisionStageRegistry.default()
        self._verifier = verifier or DecisionPackageContractVerifier(
            version_constraints=version_constraints,
        )
        self._clock = clock or _utc_now
        self._executor = executor or DecisionExecutor(
            verifier=self._verifier,
            clock=self._clock,
        )
        self._active_stages = tuple(active_stages or ACTIVE_DECISION_STAGES)
        self._version_constraints = dict(version_constraints or {})
        self._foundation = UsefulGodFoundationStage()
        self._priority = UsefulGodPriorityStage()
        self._override = UsefulGodOverrideStage()

    def load_packages(self) -> dict[str, LoadedPackage]:
        """Load released packages declared by active enabled stages."""
        constraints = dict(self._version_constraints)
        packages: dict[str, LoadedPackage] = {}
        for stage_id in self._active_stages:
            record = self._registry.get(stage_id)
            if not record.enabled or record.package_id is None:
                continue
            packages[record.package_id] = self._loader.load(
                record.package_id,
                version_constraint=constraints.get(record.package_id),
            )
        if packages:
            self._loader.assert_optional_dependencies(packages)
        return packages

    def run(
        self,
        snapshot: Mapping[str, Any] | None = None,
        *,
        context: DecisionExecutionContext | None = None,
    ) -> CanonicalDecisionResult:
        """Execute the canonical decision pipeline once. Failures become diagnostics."""
        execution_context = context or DecisionExecutionContext(snapshot=dict(snapshot or {}))
        started_at = self._clock().isoformat()
        diagnostics: list[DecisionDiagnostic] = list(execution_context.diagnostics)
        errors: list[str] = []
        packages: dict[str, LoadedPackage] = {}
        stage_order: tuple[str, ...] = ()
        steps = ()
        try:
            stage_order = self._registry.resolve_order(self._active_stages)
            diagnostics.append(execution_order_diagnostic(stage_order))
            for stage_id in self._registry.disabled_stage_ids():
                diagnostics.append(disabled_stage_diagnostic(stage_id))
            packages = self.load_packages()
            for package in packages.values():
                stage = next(
                    (
                        self._registry.get(item)
                        for item in stage_order
                        if self._registry.get(item).package_id == package.package_id
                    ),
                    None,
                )
                self._verifier.verify(
                    package,
                    stage=stage,
                    loaded_packages=packages,
                )
            steps = self._executor.execute(
                registry=self._registry,
                stage_order=stage_order,
                context=execution_context,
                packages=packages,
                handlers=self._handlers(),
            )
            diagnostics.append(pipeline_ok_diagnostic())
            success = True
            audit = passing_audit()
        except (
            PackageLoadError,
            IncompatiblePackageError,
            ContractViolationError,
            DependencyViolationError,
            DuplicatePublicationError,
            DecisionPipelineError,
        ) as exc:
            logger.warning("decision_pipeline_failed", extra={"error": str(exc)})
            diagnostics.append(pipeline_fail_diagnostic(str(exc)))
            errors.append(str(exc))
            success = False
            audit = failing_audit(str(exc))

        for diagnostic in diagnostics:
            if diagnostic not in execution_context.diagnostics:
                execution_context.add_diagnostic(diagnostic)

        package_versions = {
            package_id: package.package_version
            for package_id, package in packages.items()
        }
        executed = tuple(execution_context.published_stage_ids())
        trace = DecisionTrace(
            pipeline_id=self.pipeline_id,
            pipeline_version=self.pipeline_version,
            started_at=started_at,
            completed_at=self._clock().isoformat(),
            steps=steps,
        )
        return build_decision_result(
            context=execution_context,
            diagnostics=execution_context.diagnostics,
            errors=errors,
            stage_order=executed or stage_order or self._active_stages,
            package_versions=package_versions,
            trace=trace,
            audit=audit,
            success=success,
            pipeline_id=self.pipeline_id,
            pipeline_version=self.pipeline_version,
        )

    def _handlers(self) -> dict[str, Callable[..., Mapping[str, Any]]]:
        return {
            "useful_god_foundation": self._foundation.execute,
            "useful_god_priority": self._priority.execute,
            "useful_god_override": self._override.execute,
        }
