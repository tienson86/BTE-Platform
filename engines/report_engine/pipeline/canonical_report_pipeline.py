"""Canonical Report Pipeline (Sprint RX-1)."""

from __future__ import annotations

import logging
from datetime import datetime, timezone
from typing import Any, Callable, Mapping, Sequence

from engines.report_engine.foundation_constants import REPORT_VERSION
from engines.report_engine.integration.foundation_stage import FoundationStage
from engines.report_engine.integration.layout_stage import LayoutStage
from engines.report_engine.integration.rendering_stage import RenderingStage
from engines.report_engine.layout.layout_context import LAYOUT_VERSION
from engines.report_engine.pipeline.diagnostics import (
    DIAG_CONTRACT_VIOLATION,
    DIAG_DEP_VIOLATION,
    DIAG_OUT_DUPLICATE,
    DIAG_PIPE_FAIL,
    CanonicalReportPipelineError,
    ReportContractViolationError,
    ReportDependencyViolationError,
    ReportDuplicatePublicationError,
    ReportMissingInputError,
    ReportPipelineDiagnostic,
    diagnostic,
    disabled_stage_diagnostic,
    execution_order_diagnostic,
    pipeline_fail_diagnostic,
    pipeline_ok_diagnostic,
)
from engines.report_engine.pipeline.package_contract import ReportPackageContractVerifier
from engines.report_engine.pipeline.pipeline_executor import (
    ReportPipelineContext,
    ReportPipelineExecutor,
)
from engines.report_engine.pipeline.report_audit import build_report_pipeline_audit
from engines.report_engine.pipeline.report_result import (
    CanonicalReportResult,
    build_canonical_report_result,
)
from engines.report_engine.pipeline.report_trace import (
    ReportPipelineTraceStep,
    build_report_pipeline_trace,
)
from engines.report_engine.pipeline.stage_registry import (
    ACTIVE_REPORT_STAGES,
    PIPELINE_ID,
    PIPELINE_VERSION,
    STAGE_FOUNDATION,
    STAGE_LAYOUT,
    STAGE_RENDERING,
    ReportStageRegistry,
)
from engines.report_engine.rendering.rendering_context import RENDER_VERSION

logger = logging.getLogger(__name__)


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


def _iso(moment: datetime) -> str:
    return moment.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


class CanonicalReportPipeline:
    """Only supported RX-1 execution model for Foundation → Layout → Rendering.

    Released RE-1 / RE-2 / RE-3 components remain independently importable for
    backward compatibility. New report work should use this pipeline.
    Exceptions are converted to diagnostics and never leave ``run``.
    """

    pipeline_id: str = PIPELINE_ID
    pipeline_version: str = PIPELINE_VERSION

    def __init__(
        self,
        *,
        registry: ReportStageRegistry | None = None,
        verifier: ReportPackageContractVerifier | None = None,
        executor: ReportPipelineExecutor | None = None,
        active_stages: Sequence[str] | None = None,
        version_constraints: Mapping[str, str] | None = None,
        clock: Callable[[], datetime] | None = None,
        renderer: str = "json",
    ) -> None:
        """Initialize canonical report orchestration dependencies."""
        self._registry = registry or ReportStageRegistry.default()
        self._verifier = verifier or ReportPackageContractVerifier(
            version_constraints=version_constraints,
        )
        self._clock = clock or _utc_now
        self._executor = executor or ReportPipelineExecutor(
            verifier=self._verifier,
            clock=self._clock,
        )
        self._active_stages = tuple(active_stages or ACTIVE_REPORT_STAGES)
        self._renderer = renderer
        self._foundation = FoundationStage()
        self._layout = LayoutStage(clock=self._clock)
        self._rendering = RenderingStage(clock=self._clock)

    def run(
        self,
        *,
        analysis_result: Any = None,
        decision_result: Any = None,
        luck_result: Any = None,
        interpretation_result: Any = None,
        foundation_result: Any = None,
        layout_result: Any = None,
        rendering_result: Any = None,
        renderer: str | None = None,
        context: ReportPipelineContext | None = None,
    ) -> CanonicalReportResult:
        """Execute the canonical report pipeline once. Failures become diagnostics."""
        execution_context = context or ReportPipelineContext(
            analysis_input=analysis_result,
            decision_input=decision_result,
            luck_input=luck_result,
            interpretation_input=interpretation_result,
            foundation_input=foundation_result,
            layout_input=layout_result,
            rendering_input=rendering_result,
            renderer_id=renderer or self._renderer,
        )
        started_at = _iso(self._clock())
        diagnostics: list[ReportPipelineDiagnostic] = list(execution_context.diagnostics)
        errors: list[str] = []
        stage_order: tuple[str, ...] = ()
        steps: tuple[ReportPipelineTraceStep, ...] = ()
        success = False
        try:
            stage_order = self._registry.resolve_order(self._active_stages)
            diagnostics.append(execution_order_diagnostic(stage_order))
            for stage_id in self._registry.disabled_stage_ids():
                diagnostics.append(disabled_stage_diagnostic(stage_id))
            steps = self._executor.execute(
                registry=self._registry,
                stage_order=stage_order,
                context=execution_context,
                handlers=self._handlers(),
            )
            diagnostics.append(pipeline_ok_diagnostic())
            success = True
        except ReportMissingInputError as exc:
            logger.warning("report_pipeline_missing_input %s", exc)
            diagnostics.append(diagnostic(exc.diagnostic_code, str(exc)))
            diagnostics.append(pipeline_fail_diagnostic(str(exc)))
            errors.append(str(exc))
        except ReportDuplicatePublicationError as exc:
            logger.warning("report_pipeline_duplicate %s", exc)
            diagnostics.append(diagnostic(DIAG_OUT_DUPLICATE, str(exc)))
            diagnostics.append(pipeline_fail_diagnostic(str(exc)))
            errors.append(str(exc))
        except ReportDependencyViolationError as exc:
            logger.warning("report_pipeline_dependency %s", exc)
            diagnostics.append(diagnostic(DIAG_DEP_VIOLATION, str(exc)))
            diagnostics.append(pipeline_fail_diagnostic(str(exc)))
            errors.append(str(exc))
        except ReportContractViolationError as exc:
            logger.warning("report_pipeline_contract %s", exc)
            diagnostics.append(diagnostic(DIAG_CONTRACT_VIOLATION, str(exc)))
            diagnostics.append(pipeline_fail_diagnostic(str(exc)))
            errors.append(str(exc))
        except CanonicalReportPipelineError as exc:
            logger.warning("report_pipeline_failed %s", exc)
            diagnostics.append(pipeline_fail_diagnostic(str(exc)))
            errors.append(str(exc))
        except Exception as exc:  # noqa: BLE001 — boundary must not raise
            logger.exception("report_pipeline_unexpected")
            diagnostics.append(pipeline_fail_diagnostic(DIAG_PIPE_FAIL))
            errors.append(str(exc))

        for item in diagnostics:
            if item not in execution_context.diagnostics:
                execution_context.add_diagnostic(item)

        executed = execution_context.published_stage_ids()
        component_versions = {
            "report_foundation": REPORT_VERSION,
            "report_layout_engine": LAYOUT_VERSION,
            "report_rendering_engine": RENDER_VERSION,
        }
        completed_at = _iso(self._clock())
        rendering = execution_context.rendering_result
        artifact_id = None
        if isinstance(rendering, Mapping):
            artifact_id = rendering.get("artifact_id")
        trace = build_report_pipeline_trace(
            steps=steps,
            published_outputs=execution_context.published_output_names(),
            component_versions=component_versions,
            artifact_id=str(artifact_id) if artifact_id else None,
            started_at=started_at,
            completed_at=completed_at,
        )
        audit = build_report_pipeline_audit(
            diagnostics=execution_context.diagnostics,
            executed_stages=executed,
        )
        return build_canonical_report_result(
            success=success,
            foundation_result=execution_context.foundation_result,
            layout_result=execution_context.layout_result,
            rendering_result=execution_context.rendering_result,
            report_trace=trace,
            report_audit=audit,
            diagnostics=execution_context.diagnostics,
            component_versions=component_versions,
            errors=errors,
            pipeline_id=self.pipeline_id,
            pipeline_version=self.pipeline_version,
        )

    def _handlers(self) -> dict[str, Callable[[ReportPipelineContext], Mapping[str, Any]]]:
        return {
            STAGE_FOUNDATION: self._foundation.execute,
            STAGE_LAYOUT: self._layout.execute,
            STAGE_RENDERING: self._rendering.execute,
        }
