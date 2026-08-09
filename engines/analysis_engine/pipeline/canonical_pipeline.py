"""Canonical end-to-end Analysis Pipeline (Sprint AX-2)."""

from __future__ import annotations

import logging
from datetime import datetime, timezone
from typing import Any, Callable, Mapping, Sequence

from engines.analysis_engine.exceptions.pipeline_error import (
    ContractViolationError,
    DependencyViolationError,
    DuplicateExecutionError,
    IncompatiblePackageError,
    PackageLoadError,
    PipelineError,
)
from engines.analysis_engine.integration.calendar_stage import CalendarStage
from engines.analysis_engine.integration.four_pillars_stage import FourPillarsStage
from engines.analysis_engine.integration.pattern_evaluation_stage import (
    PatternEvaluationStage,
)
from engines.analysis_engine.integration.pattern_stage import PatternStage
from engines.analysis_engine.integration.seasonal_stage import SeasonalStage
from engines.analysis_engine.integration.strength_stage import StrengthStage
from engines.analysis_engine.integration.temperature_stage import TemperatureStage
from engines.analysis_engine.integration.useful_god_stage import UsefulGodStage
from engines.analysis_engine.pipeline.diagnostics import (
    disabled_stage_diagnostic,
    execution_order_diagnostic,
    pipeline_fail_diagnostic,
    pipeline_ok_diagnostic,
)
from engines.analysis_engine.pipeline.execution_context import (
    AnalysisExecutionContext,
    PipelineDiagnostic,
)
from engines.analysis_engine.pipeline.execution_report import (
    CanonicalAnalysisResult,
    ExecutionTrace,
    build_analysis_result,
)
from engines.analysis_engine.pipeline.package_contract import PackageContractVerifier
from engines.analysis_engine.pipeline.package_loader import LoadedPackage, PackageLoader
from engines.analysis_engine.pipeline.pipeline_executor import CanonicalPipelineExecutor
from engines.analysis_engine.pipeline.stage_registry import (
    ACTIVE_CANONICAL_STAGES,
    PIPELINE_ID_V2,
    PIPELINE_VERSION_V2,
    CanonicalStageRegistry,
)

logger = logging.getLogger(__name__)


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


class CanonicalPipeline:
    """Only supported AX-2 execution model for released analysis packages.

    Packages bind through orchestration. Analytical rule logic is unchanged.
    Exceptions are converted to diagnostics and never leave ``run``.
    """

    pipeline_id: str = PIPELINE_ID_V2
    pipeline_version: str = PIPELINE_VERSION_V2

    def __init__(
        self,
        *,
        loader: PackageLoader | None = None,
        registry: CanonicalStageRegistry | None = None,
        verifier: PackageContractVerifier | None = None,
        executor: CanonicalPipelineExecutor | None = None,
        active_stages: Sequence[str] | None = None,
        version_constraints: Mapping[str, str] | None = None,
        clock: Callable[[], datetime] | None = None,
    ) -> None:
        """Initialize canonical orchestration dependencies."""
        self._loader = loader or PackageLoader()
        self._registry = registry or CanonicalStageRegistry.default()
        self._verifier = verifier or PackageContractVerifier(
            version_constraints=version_constraints,
        )
        self._clock = clock or _utc_now
        self._executor = executor or CanonicalPipelineExecutor(
            verifier=self._verifier,
            clock=self._clock,
        )
        self._active_stages = tuple(active_stages or ACTIVE_CANONICAL_STAGES)
        self._version_constraints = dict(version_constraints or {})
        self._calendar = CalendarStage()
        self._four_pillars = FourPillarsStage()
        self._seasonal = SeasonalStage()
        self._strength = StrengthStage()
        self._temperature = TemperatureStage()
        self._pattern = PatternStage()
        self._pattern_evaluation = PatternEvaluationStage()
        self._useful_god = UsefulGodStage()

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
        chart: Mapping[str, Any] | None = None,
        *,
        context: AnalysisExecutionContext | None = None,
    ) -> CanonicalAnalysisResult:
        """Execute the canonical pipeline once. Failures become diagnostics."""
        execution_context = context or AnalysisExecutionContext(chart=dict(chart or {}))
        started_at = self._clock().isoformat()
        diagnostics: list[PipelineDiagnostic] = list(execution_context.diagnostics)
        errors: list[str] = []
        outcomes = ()
        traces = ()
        packages: dict[str, LoadedPackage] = {}
        stage_order: tuple[str, ...] = ()
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
            outcomes, traces = self._executor.execute(
                registry=self._registry,
                stage_order=stage_order,
                context=execution_context,
                packages=packages,
                handlers=self._handlers(),
            )
            diagnostics.append(pipeline_ok_diagnostic())
            success = True
        except (
            PackageLoadError,
            IncompatiblePackageError,
            ContractViolationError,
            DependencyViolationError,
            DuplicateExecutionError,
            PipelineError,
        ) as exc:
            logger.warning("canonical_pipeline_failed", extra={"error": str(exc)})
            diagnostics.append(pipeline_fail_diagnostic(str(exc)))
            errors.append(str(exc))
            success = False

        for diagnostic in diagnostics:
            if diagnostic not in execution_context.diagnostics:
                execution_context.add_diagnostic(diagnostic)

        package_versions = {
            package_id: package.package_version
            for package_id, package in packages.items()
        }
        executed_ids = tuple(outcome.stage_id for outcome in outcomes)
        trace = ExecutionTrace(
            pipeline_id=self.pipeline_id,
            pipeline_version=self.pipeline_version,
            started_at=started_at,
            completed_at=self._clock().isoformat(),
            stages=traces,
            package_versions=package_versions,
            outputs_published=executed_ids,
            diagnostics=tuple(execution_context.diagnostics),
        )
        return build_analysis_result(
            context=execution_context,
            outcomes=outcomes,
            diagnostics=execution_context.diagnostics,
            errors=errors,
            stage_order=executed_ids or stage_order or self._active_stages,
            package_versions=package_versions,
            trace=trace,
            success=success,
            pipeline_id=self.pipeline_id,
            pipeline_version=self.pipeline_version,
        )

    def _handlers(self) -> dict[str, Callable[..., Mapping[str, Any]]]:
        return {
            "calendar": lambda context, package=None: self._calendar.execute(context),
            "four_pillars": lambda context, package=None: self._four_pillars.execute(
                context
            ),
            "seasonal": self._seasonal.execute,
            "strength": self._strength.execute,
            "temperature": self._temperature.execute,
            "pattern": self._pattern.execute,
            "pattern_evaluation": self._pattern_evaluation.execute,
            "useful_god": self._useful_god.execute,
        }
