"""AX-1 pipeline validation for knowledge-package orchestration."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping, Sequence

from engines.analysis_engine.pipeline.dependency_resolver import (
    ACTIVE_KNOWLEDGE_STAGES,
    STAGE_PACKAGE_IDS,
    DependencyResolver,
)
from engines.analysis_engine.pipeline.execution_context import (
    AnalysisExecutionContext,
    PipelineDiagnostic,
)
from engines.analysis_engine.pipeline.package_loader import (
    REQUIRED_SCHEMA_VERSION,
    LoadedPackage,
    satisfies_version_constraint,
)

EXPECTED_CONSTRAINTS: dict[str, str] = {
    "bz_01_strength_core": "^1.0.0",
    "bz_02_seasonal_core": "^1.0.0",
    "bz_03_temperature_core": "^1.0.0",
}


@dataclass(slots=True)
class PipelineValidationReport:
    """Structured validation report for one pipeline run or plan."""

    success: bool
    diagnostics: tuple[PipelineDiagnostic, ...] = ()

    @property
    def errors(self) -> tuple[PipelineDiagnostic, ...]:
        """Return diagnostics with error severity."""
        return tuple(item for item in self.diagnostics if item.severity == "error")


class PipelineValidation:
    """Validate package load, order, inputs, outputs, and compatibility."""

    def __init__(self, *, resolver: DependencyResolver | None = None) -> None:
        """Initialize validation against the canonical dependency resolver."""
        self._resolver = resolver or DependencyResolver()

    def validator_id(self) -> str:
        """Return the stable validator identifier."""
        return "ax1_pipeline_validation"

    def validate_packages(
        self,
        packages: Mapping[str, LoadedPackage],
        *,
        required_package_ids: Sequence[str] | None = None,
    ) -> list[PipelineDiagnostic]:
        """Validate that required released packages are loaded and compatible."""
        diagnostics: list[PipelineDiagnostic] = []
        required = tuple(required_package_ids or STAGE_PACKAGE_IDS.values())
        for package_id in required:
            package = packages.get(package_id)
            if package is None:
                diagnostics.append(
                    PipelineDiagnostic(
                        code="PKG-MISSING",
                        message=f"Required package not loaded: {package_id}",
                        severity="error",
                    )
                )
                continue
            diagnostics.extend(self._package_diagnostics(package))
        return diagnostics

    def validate_order(self, stage_order: Sequence[str]) -> list[PipelineDiagnostic]:
        """Validate deterministic canonical order and prerequisites."""
        diagnostics: list[PipelineDiagnostic] = []
        try:
            resolved = self._resolver.resolve_order(stage_order)
        except Exception as exc:
            diagnostics.append(
                PipelineDiagnostic(
                    code="DEP-ORDER",
                    message=str(exc),
                    severity="error",
                )
            )
            return diagnostics
        if tuple(stage_order) != resolved:
            diagnostics.append(
                PipelineDiagnostic(
                    code="DEP-ORDER",
                    message="Requested stage order is not canonical",
                    severity="error",
                    details={"expected": list(resolved), "actual": list(stage_order)},
                )
            )
        return diagnostics

    def validate_context(
        self,
        context: AnalysisExecutionContext,
        *,
        expected_stages: Sequence[str] = ACTIVE_KNOWLEDGE_STAGES,
    ) -> list[PipelineDiagnostic]:
        """Validate published outputs and reject duplicate gaps."""
        diagnostics: list[PipelineDiagnostic] = []
        published = context.published_stage_ids()
        if len(published) != len(set(published)):
            diagnostics.append(
                PipelineDiagnostic(
                    code="DUP-EXEC",
                    message="Duplicate stage identifiers in execution trace",
                    severity="error",
                )
            )
        for stage_id in expected_stages:
            if not context.has_result(stage_id):
                diagnostics.append(
                    PipelineDiagnostic(
                        code="OUT-MISSING",
                        message=f"Stage output not produced: {stage_id}",
                        severity="error",
                        stage_id=stage_id,
                    )
                )
        for stage_id in published:
            try:
                self._resolver.assert_inputs_present(stage_id, published)
            except Exception as exc:
                diagnostics.append(
                    PipelineDiagnostic(
                        code="IN-MISSING",
                        message=str(exc),
                        severity="error",
                        stage_id=stage_id,
                    )
                )
        return diagnostics

    def validate_run(
        self,
        *,
        context: AnalysisExecutionContext,
        packages: Mapping[str, LoadedPackage],
        stage_order: Sequence[str],
    ) -> PipelineValidationReport:
        """Run all AX-1 pipeline checks and return a structured report."""
        diagnostics: list[PipelineDiagnostic] = []
        diagnostics.extend(self.validate_packages(packages))
        diagnostics.extend(self.validate_order(stage_order))
        diagnostics.extend(
            self.validate_context(context, expected_stages=stage_order)
        )
        success = not any(item.severity == "error" for item in diagnostics)
        if success:
            diagnostics.append(
                PipelineDiagnostic(
                    code="PIPE-OK",
                    message="Pipeline validation passed",
                    severity="info",
                )
            )
        return PipelineValidationReport(
            success=success,
            diagnostics=tuple(diagnostics),
        )

    def _package_diagnostics(self, package: LoadedPackage) -> list[PipelineDiagnostic]:
        diagnostics: list[PipelineDiagnostic] = []
        if package.status != "released":
            diagnostics.append(
                PipelineDiagnostic(
                    code="PKG-STATUS",
                    message=f"Package is not released: {package.package_id}",
                    severity="error",
                )
            )
        if package.schema_version != REQUIRED_SCHEMA_VERSION:
            diagnostics.append(
                PipelineDiagnostic(
                    code="PKG-SCHEMA",
                    message=f"Incompatible schema: {package.schema_version}",
                    severity="error",
                )
            )
        constraint = EXPECTED_CONSTRAINTS.get(package.package_id)
        if constraint and not satisfies_version_constraint(
            package.package_version,
            constraint,
        ):
            diagnostics.append(
                PipelineDiagnostic(
                    code="PKG-VERSION",
                    message=(
                        f"Incompatible version {package.package_version} "
                        f"for {package.package_id}"
                    ),
                    severity="error",
                )
            )
        else:
            diagnostics.append(
                PipelineDiagnostic(
                    code="PKG-LOADED",
                    message=f"Package loaded: {package.package_id}@{package.package_version}",
                    severity="info",
                )
            )
        return diagnostics
