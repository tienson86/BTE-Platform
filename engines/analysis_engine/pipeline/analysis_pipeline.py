"""Knowledge-package analysis pipeline orchestration (Sprint AX-1)."""

from __future__ import annotations

import logging
from typing import Any, Mapping, Sequence

from engines.analysis_engine.exceptions.pipeline_error import (
    DependencyViolationError,
    DuplicateExecutionError,
    IncompatiblePackageError,
    PackageLoadError,
    PipelineError,
)
from engines.analysis_engine.integration.calendar_stage import CalendarStage
from engines.analysis_engine.integration.four_pillars_stage import FourPillarsStage
from engines.analysis_engine.integration.seasonal_stage import SeasonalStage
from engines.analysis_engine.integration.strength_stage import StrengthStage
from engines.analysis_engine.integration.temperature_stage import TemperatureStage
from engines.analysis_engine.pipeline.dependency_resolver import (
    ACTIVE_KNOWLEDGE_STAGES,
    PIPELINE_VERSION,
    STAGE_PACKAGE_IDS,
    DependencyResolver,
)
from engines.analysis_engine.pipeline.execution_context import (
    AnalysisExecutionContext,
    PipelineDiagnostic,
)
from engines.analysis_engine.pipeline.package_loader import LoadedPackage, PackageLoader
from engines.analysis_engine.pipeline.pipeline_result import (
    AnalysisPipelineResult,
    StageOutcome,
)
from engines.analysis_engine.validation.pipeline_validation import PipelineValidation

logger = logging.getLogger(__name__)

PIPELINE_ID = "analysis_pipeline_ax1"


class AnalysisPipeline:
    """Orchestrate Calendar → Four Pillars → Seasonal → Strength → Temperature.

    Stages communicate only through AnalysisExecutionContext. Knowledge
    packages are bound, not evaluated. Analytical rule logic is unchanged.
    """

    pipeline_id: str = PIPELINE_ID
    pipeline_version: str = PIPELINE_VERSION

    def __init__(
        self,
        *,
        loader: PackageLoader | None = None,
        resolver: DependencyResolver | None = None,
        validator: PipelineValidation | None = None,
        active_stages: Sequence[str] | None = None,
        version_constraints: Mapping[str, str] | None = None,
    ) -> None:
        """Initialize orchestration dependencies."""
        self._loader = loader or PackageLoader()
        self._resolver = resolver or DependencyResolver()
        self._validator = validator or PipelineValidation(resolver=self._resolver)
        self._active_stages = tuple(active_stages or ACTIVE_KNOWLEDGE_STAGES)
        self._version_constraints = dict(version_constraints or {})
        self._calendar = CalendarStage()
        self._four_pillars = FourPillarsStage()
        self._seasonal = SeasonalStage()
        self._strength = StrengthStage()
        self._temperature = TemperatureStage()

    def load_packages(self) -> dict[str, LoadedPackage]:
        """Load released core packages required by active knowledge stages."""
        constraints = dict(self._version_constraints)
        packages: dict[str, LoadedPackage] = {}
        for stage_id in self._active_stages:
            package_id = STAGE_PACKAGE_IDS.get(stage_id)
            if package_id is None:
                continue
            packages[package_id] = self._loader.load(
                package_id,
                version_constraint=constraints.get(package_id),
            )
        if "bz_03_temperature_core" in packages:
            self._loader.assert_optional_dependencies(packages)
        return packages

    def run(
        self,
        chart: Mapping[str, Any] | None = None,
        *,
        context: AnalysisExecutionContext | None = None,
    ) -> AnalysisPipelineResult:
        """Execute the canonical knowledge pipeline once."""
        execution_context = context or AnalysisExecutionContext(chart=dict(chart or {}))
        diagnostics: list[PipelineDiagnostic] = list(execution_context.diagnostics)
        outcomes: list[StageOutcome] = []
        errors: list[str] = []

        try:
            stage_order = self._resolver.resolve_order(self._active_stages)
            packages = self.load_packages()

            for stage_id in stage_order:
                self._resolver.assert_inputs_present(
                    stage_id,
                    execution_context.published_stage_ids(),
                )
                payload = self._execute_stage(
                    stage_id,
                    execution_context,
                    packages,
                )
                outcome = StageOutcome(
                    stage_id=stage_id,
                    success=True,
                    payload=dict(payload),
                    messages=(f"{stage_id}_completed",),
                )
                outcomes.append(outcome)

            report = self._validator.validate_run(
                context=execution_context,
                packages=packages,
                stage_order=stage_order,
            )
            diagnostics.extend(report.diagnostics)
            success = report.success
            if not success:
                errors.extend(item.message for item in report.errors)
        except (
            PackageLoadError,
            IncompatiblePackageError,
            DependencyViolationError,
            DuplicateExecutionError,
            PipelineError,
        ) as exc:
            logger.warning("analysis_pipeline_failed", extra={"error": str(exc)})
            diagnostics.append(
                PipelineDiagnostic(
                    code="PIPE-FAIL",
                    message=str(exc),
                    severity="error",
                )
            )
            errors.append(str(exc))
            stage_order = tuple(execution_context.published_stage_ids())
            success = False

        for diagnostic in diagnostics:
            if diagnostic not in execution_context.diagnostics:
                execution_context.add_diagnostic(diagnostic)

        return AnalysisPipelineResult(
            pipeline_id=self.pipeline_id,
            pipeline_version=self.pipeline_version,
            success=success,
            stage_order=tuple(outcome.stage_id for outcome in outcomes)
            if outcomes
            else tuple(self._active_stages),
            outcomes=tuple(outcomes),
            diagnostics=tuple(execution_context.diagnostics),
            errors=tuple(errors),
            seasonal_result=execution_context.seasonal_result,
            strength_result=execution_context.strength_result,
            temperature_result=execution_context.temperature_result,
            pattern_result=execution_context.pattern_result,
            useful_god_result=execution_context.useful_god_result,
            luck_cycle_result=execution_context.luck_cycle_result,
        )

    def _execute_stage(
        self,
        stage_id: str,
        context: AnalysisExecutionContext,
        packages: Mapping[str, LoadedPackage],
    ) -> Mapping[str, Any]:
        if stage_id == "calendar":
            return self._calendar.execute(context)
        if stage_id == "four_pillars":
            return self._four_pillars.execute(context)
        if stage_id == "seasonal":
            return self._seasonal.execute(context, packages[self._seasonal.package_id])
        if stage_id == "strength":
            return self._strength.execute(context, packages[self._strength.package_id])
        if stage_id == "temperature":
            return self._temperature.execute(
                context,
                packages[self._temperature.package_id],
            )
        raise DependencyViolationError(f"placeholder_stage_not_executable:{stage_id}")

    def _failed_result(
        self,
        *,
        stage_order: Sequence[str],
        outcomes: Sequence[StageOutcome],
        diagnostics: Sequence[PipelineDiagnostic],
        errors: tuple[str, ...],
        context: AnalysisExecutionContext,
    ) -> AnalysisPipelineResult:
        for diagnostic in diagnostics:
            if diagnostic not in context.diagnostics:
                context.add_diagnostic(diagnostic)
        return AnalysisPipelineResult(
            pipeline_id=self.pipeline_id,
            pipeline_version=self.pipeline_version,
            success=False,
            stage_order=tuple(stage_order),
            outcomes=tuple(outcomes),
            diagnostics=tuple(context.diagnostics),
            errors=errors,
            seasonal_result=context.seasonal_result,
            strength_result=context.strength_result,
            temperature_result=context.temperature_result,
        )
