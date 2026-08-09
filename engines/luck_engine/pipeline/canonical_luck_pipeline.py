"""Canonical Luck Pipeline (Sprint AX-4)."""

from __future__ import annotations

import logging
from datetime import datetime, timezone
from typing import Any, Callable, Mapping, Sequence

from engines.luck_engine.exceptions import (
    LuckContractViolationError,
    LuckDependencyViolationError,
    LuckDuplicatePublicationError,
    LuckMissingInputError,
    LuckPipelineError,
)
from engines.luck_engine.integration.analysis_stage import AnalysisStage
from engines.luck_engine.integration.decision_stage import DecisionStage
from engines.luck_engine.integration.timeline_stage import TimelineStage
from engines.luck_engine.pipeline.diagnostics import (
    DIAG_CONTRACT_VIOLATION,
    DIAG_DEP_VIOLATION,
    DIAG_OUT_DUPLICATE,
    DIAG_PIPE_FAIL,
    LuckPipelineDiagnostic,
    diagnostic,
    disabled_stage_diagnostic,
    execution_order_diagnostic,
    pipeline_fail_diagnostic,
    pipeline_ok_diagnostic,
)
from engines.luck_engine.pipeline.luck_audit import build_luck_audit
from engines.luck_engine.pipeline.luck_result import CanonicalLuckResult, build_canonical_luck_result
from engines.luck_engine.pipeline.luck_trace import LuckTraceStep, build_luck_trace
from engines.luck_engine.pipeline.package_contract import LuckPackageContractVerifier
from engines.luck_engine.pipeline.pipeline_executor import LuckPipelineContext, LuckPipelineExecutor
from engines.luck_engine.pipeline.stage_registry import (
    ACTIVE_LUCK_STAGES,
    PIPELINE_ID,
    PIPELINE_VERSION,
    LuckStageRegistry,
)
from engines.luck_engine.timeline.package_loader import LoadedLuckPackage
from engines.luck_engine.timeline_constants import TIMELINE_VERSION
from engines.luck_engine.analysis_constants import ANALYSIS_VERSION
from engines.luck_engine.decision_constants import DECISION_VERSION

logger = logging.getLogger(__name__)


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


def _iso(moment: datetime) -> str:
    return moment.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


class CanonicalLuckPipeline:
    """Only supported AX-4 execution model for Luck Timeline → Analysis → Decision.

    Released LE-1 / LE-2 / LE-3 components remain independently importable for
    backward compatibility. New Luck computation should use this pipeline.
    Exceptions are converted to diagnostics and never leave ``run``.
    """

    pipeline_id: str = PIPELINE_ID
    pipeline_version: str = PIPELINE_VERSION

    def __init__(
        self,
        *,
        registry: LuckStageRegistry | None = None,
        verifier: LuckPackageContractVerifier | None = None,
        executor: LuckPipelineExecutor | None = None,
        active_stages: Sequence[str] | None = None,
        version_constraints: Mapping[str, str] | None = None,
        clock: Callable[[], datetime] | None = None,
    ) -> None:
        """Initialize canonical luck orchestration dependencies."""
        self._registry = registry or LuckStageRegistry.default()
        self._verifier = verifier or LuckPackageContractVerifier(
            version_constraints=version_constraints,
        )
        self._clock = clock or _utc_now
        self._executor = executor or LuckPipelineExecutor(
            verifier=self._verifier,
            clock=self._clock,
        )
        self._active_stages = tuple(active_stages or ACTIVE_LUCK_STAGES)
        self._version_constraints = dict(version_constraints or {})
        self._timeline = TimelineStage()
        self._analysis = AnalysisStage(clock=self._clock)
        self._decision = DecisionStage(clock=self._clock)

    def load_packages(self) -> dict[str, LoadedLuckPackage]:
        """Load released packages declared by active enabled stages."""
        packages: dict[str, LoadedLuckPackage] = {}
        for stage_id in self._active_stages:
            record = self._registry.get(stage_id)
            if not record.enabled or record.package_id is None:
                continue
            packages[record.package_id] = self._verifier.load_timeline_package()
        return packages

    def run(
        self,
        *,
        timeline: Any = None,
        analysis_result: Any = None,
        decision_result: Any = None,
        context: LuckPipelineContext | None = None,
    ) -> CanonicalLuckResult:
        """Execute the canonical luck pipeline once. Failures become diagnostics."""
        execution_context = context or LuckPipelineContext(
            timeline_input=timeline,
            analysis_input=analysis_result,
            decision_input=decision_result,
        )
        started_at = _iso(self._clock())
        diagnostics: list[LuckPipelineDiagnostic] = list(execution_context.diagnostics)
        errors: list[str] = []
        packages: dict[str, LoadedLuckPackage] = {}
        stage_order: tuple[str, ...] = ()
        steps: tuple[LuckTraceStep, ...] = ()
        success = False
        try:
            stage_order = self._registry.resolve_order(self._active_stages)
            diagnostics.append(execution_order_diagnostic(stage_order))
            for stage_id in self._registry.disabled_stage_ids():
                diagnostics.append(disabled_stage_diagnostic(stage_id))
            packages = self.load_packages()
            steps = self._executor.execute(
                registry=self._registry,
                stage_order=stage_order,
                context=execution_context,
                packages=packages,
                handlers=self._handlers(),
            )
            diagnostics.append(pipeline_ok_diagnostic())
            success = True
        except LuckMissingInputError as exc:
            logger.warning("luck_pipeline_missing_input %s", exc)
            diagnostics.append(diagnostic(exc.diagnostic_code, str(exc)))
            diagnostics.append(pipeline_fail_diagnostic(str(exc)))
            errors.append(str(exc))
        except LuckDuplicatePublicationError as exc:
            logger.warning("luck_pipeline_duplicate %s", exc)
            diagnostics.append(diagnostic(DIAG_OUT_DUPLICATE, str(exc)))
            diagnostics.append(pipeline_fail_diagnostic(str(exc)))
            errors.append(str(exc))
        except LuckDependencyViolationError as exc:
            logger.warning("luck_pipeline_dependency %s", exc)
            diagnostics.append(diagnostic(DIAG_DEP_VIOLATION, str(exc)))
            diagnostics.append(pipeline_fail_diagnostic(str(exc)))
            errors.append(str(exc))
        except LuckContractViolationError as exc:
            logger.warning("luck_pipeline_contract %s", exc)
            diagnostics.append(diagnostic(DIAG_CONTRACT_VIOLATION, str(exc)))
            diagnostics.append(pipeline_fail_diagnostic(str(exc)))
            errors.append(str(exc))
        except LuckPipelineError as exc:
            logger.warning("luck_pipeline_failed %s", exc)
            diagnostics.append(pipeline_fail_diagnostic(str(exc)))
            errors.append(str(exc))
        except Exception as exc:  # noqa: BLE001 — boundary must not raise
            logger.exception("luck_pipeline_unexpected")
            diagnostics.append(pipeline_fail_diagnostic(DIAG_PIPE_FAIL))
            errors.append(str(exc))

        for item in diagnostics:
            if item not in execution_context.diagnostics:
                execution_context.add_diagnostic(item)

        executed = execution_context.published_stage_ids()
        component_versions = self._component_versions(packages)
        completed_at = _iso(self._clock())
        trace = build_luck_trace(
            steps=steps,
            published_outputs=execution_context.published_output_names(),
            component_versions=component_versions,
            started_at=started_at,
            completed_at=completed_at,
        )
        audit = build_luck_audit(
            diagnostics=execution_context.diagnostics,
            executed_stages=executed,
        )
        return build_canonical_luck_result(
            success=success,
            timeline_result=execution_context.timeline_result,
            analysis_result=execution_context.analysis_result,
            decision_result=execution_context.decision_result,
            luck_trace=trace,
            luck_audit=audit,
            diagnostics=execution_context.diagnostics,
            component_versions=component_versions,
            errors=errors,
            pipeline_id=self.pipeline_id,
            pipeline_version=self.pipeline_version,
        )

    def _handlers(self) -> dict[str, Callable[[LuckPipelineContext], Mapping[str, Any]]]:
        return {
            "timeline": self._timeline.execute,
            "analysis": self._analysis.execute,
            "decision": self._decision.execute,
        }

    def _component_versions(self, packages: Mapping[str, LoadedLuckPackage]) -> dict[str, str]:
        versions = {
            "timeline": TIMELINE_VERSION,
            "luck_analysis": ANALYSIS_VERSION,
            "luck_decision": DECISION_VERSION,
        }
        for package_id, package in packages.items():
            versions[package_id] = package.package_version
        return versions
