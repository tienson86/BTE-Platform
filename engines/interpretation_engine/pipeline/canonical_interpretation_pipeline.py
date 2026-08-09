"""Canonical Interpretation Pipeline (Sprint IX-1)."""

from __future__ import annotations

import logging
from datetime import datetime, timezone
from typing import Any, Callable, Mapping, Sequence

from engines.interpretation_engine.composition.composition_context import ASSEMBLY_VERSION
from engines.interpretation_engine.foundation_constants import INTERPRETATION_VERSION
from engines.interpretation_engine.integration.composition_stage import CompositionStage
from engines.interpretation_engine.integration.foundation_stage import FoundationStage
from engines.interpretation_engine.integration.knowledge_selection_stage import (
    KnowledgeSelectionStage,
)
from engines.interpretation_engine.knowledge.composition_context import COMPOSITION_VERSION
from engines.interpretation_engine.pipeline.canonical_pipeline_executor import (
    InterpretationPipelineContext,
    InterpretationPipelineExecutor,
)
from engines.interpretation_engine.pipeline.diagnostics import (
    DIAG_CONTRACT_VIOLATION,
    DIAG_DEP_VIOLATION,
    DIAG_OUT_DUPLICATE,
    DIAG_PIPE_FAIL,
    CanonicalInterpretationPipelineError,
    InterpretationContractViolationError,
    InterpretationDependencyViolationError,
    InterpretationDuplicatePublicationError,
    InterpretationMissingInputError,
    InterpretationPipelineDiagnostic,
    diagnostic,
    disabled_stage_diagnostic,
    execution_order_diagnostic,
    pipeline_fail_diagnostic,
    pipeline_ok_diagnostic,
)
from engines.interpretation_engine.pipeline.interpretation_audit import (
    build_interpretation_pipeline_audit,
)
from engines.interpretation_engine.pipeline.interpretation_result import (
    CanonicalInterpretationResult,
    build_canonical_interpretation_result,
)
from engines.interpretation_engine.pipeline.interpretation_trace import (
    InterpretationPipelineTraceStep,
    build_interpretation_pipeline_trace,
)
from engines.interpretation_engine.pipeline.package_contract import (
    InterpretationPackageContractVerifier,
)
from engines.interpretation_engine.pipeline.stage_registry import (
    ACTIVE_INTERPRETATION_STAGES,
    PIPELINE_ID,
    PIPELINE_VERSION,
    STAGE_COMPOSITION,
    STAGE_FOUNDATION,
    STAGE_KNOWLEDGE,
    InterpretationStageRegistry,
)

logger = logging.getLogger(__name__)


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


def _iso(moment: datetime) -> str:
    return moment.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


class CanonicalInterpretationPipeline:
    """Only supported IX-1 execution model for Foundation → Knowledge → Composition.

    Released IE-1 / IE-2 / IE-3 components remain independently importable for
    backward compatibility. New interpretation work should use this pipeline.
    Exceptions are converted to diagnostics and never leave ``run``.
    """

    pipeline_id: str = PIPELINE_ID
    pipeline_version: str = PIPELINE_VERSION

    def __init__(
        self,
        *,
        registry: InterpretationStageRegistry | None = None,
        verifier: InterpretationPackageContractVerifier | None = None,
        executor: InterpretationPipelineExecutor | None = None,
        active_stages: Sequence[str] | None = None,
        version_constraints: Mapping[str, str] | None = None,
        clock: Callable[[], datetime] | None = None,
    ) -> None:
        """Initialize canonical interpretation orchestration dependencies."""
        self._registry = registry or InterpretationStageRegistry.default()
        self._verifier = verifier or InterpretationPackageContractVerifier(
            version_constraints=version_constraints,
        )
        self._clock = clock or _utc_now
        self._executor = executor or InterpretationPipelineExecutor(
            verifier=self._verifier,
            clock=self._clock,
        )
        self._active_stages = tuple(active_stages or ACTIVE_INTERPRETATION_STAGES)
        self._foundation = FoundationStage()
        self._knowledge = KnowledgeSelectionStage()
        self._composition = CompositionStage(clock=self._clock)

    def run(
        self,
        *,
        analysis_result: Any = None,
        decision_result: Any = None,
        luck_result: Any = None,
        foundation_result: Any = None,
        knowledge_result: Any = None,
        context: InterpretationPipelineContext | None = None,
    ) -> CanonicalInterpretationResult:
        """Execute the canonical interpretation pipeline once. Failures become diagnostics."""
        execution_context = context or InterpretationPipelineContext(
            analysis_input=analysis_result,
            decision_input=decision_result,
            luck_input=luck_result,
            foundation_input=foundation_result,
            knowledge_input=knowledge_result,
        )
        started_at = _iso(self._clock())
        diagnostics: list[InterpretationPipelineDiagnostic] = list(execution_context.diagnostics)
        errors: list[str] = []
        stage_order: tuple[str, ...] = ()
        steps: tuple[InterpretationPipelineTraceStep, ...] = ()
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
        except InterpretationMissingInputError as exc:
            logger.warning("interpretation_pipeline_missing_input %s", exc)
            diagnostics.append(diagnostic(exc.diagnostic_code, str(exc)))
            diagnostics.append(pipeline_fail_diagnostic(str(exc)))
            errors.append(str(exc))
        except InterpretationDuplicatePublicationError as exc:
            logger.warning("interpretation_pipeline_duplicate %s", exc)
            diagnostics.append(diagnostic(DIAG_OUT_DUPLICATE, str(exc)))
            diagnostics.append(pipeline_fail_diagnostic(str(exc)))
            errors.append(str(exc))
        except InterpretationDependencyViolationError as exc:
            logger.warning("interpretation_pipeline_dependency %s", exc)
            diagnostics.append(diagnostic(DIAG_DEP_VIOLATION, str(exc)))
            diagnostics.append(pipeline_fail_diagnostic(str(exc)))
            errors.append(str(exc))
        except InterpretationContractViolationError as exc:
            logger.warning("interpretation_pipeline_contract %s", exc)
            diagnostics.append(diagnostic(DIAG_CONTRACT_VIOLATION, str(exc)))
            diagnostics.append(pipeline_fail_diagnostic(str(exc)))
            errors.append(str(exc))
        except CanonicalInterpretationPipelineError as exc:
            logger.warning("interpretation_pipeline_failed %s", exc)
            diagnostics.append(pipeline_fail_diagnostic(str(exc)))
            errors.append(str(exc))
        except Exception as exc:  # noqa: BLE001 — boundary must not raise
            logger.exception("interpretation_pipeline_unexpected")
            diagnostics.append(pipeline_fail_diagnostic(DIAG_PIPE_FAIL))
            errors.append(str(exc))

        for item in diagnostics:
            if item not in execution_context.diagnostics:
                execution_context.add_diagnostic(item)

        executed = execution_context.published_stage_ids()
        component_versions = {
            "interpretation_foundation": INTERPRETATION_VERSION,
            "knowledge_selection_engine": COMPOSITION_VERSION,
            "interpretation_composition_engine": ASSEMBLY_VERSION,
        }
        completed_at = _iso(self._clock())
        trace = build_interpretation_pipeline_trace(
            steps=steps,
            published_outputs=execution_context.published_output_names(),
            component_versions=component_versions,
            started_at=started_at,
            completed_at=completed_at,
        )
        audit = build_interpretation_pipeline_audit(
            diagnostics=execution_context.diagnostics,
            executed_stages=executed,
        )
        return build_canonical_interpretation_result(
            success=success,
            foundation_result=execution_context.foundation_result,
            knowledge_result=execution_context.knowledge_result,
            composition_result=execution_context.composition_result,
            interpretation_trace=trace,
            interpretation_audit=audit,
            diagnostics=execution_context.diagnostics,
            component_versions=component_versions,
            errors=errors,
            pipeline_id=self.pipeline_id,
            pipeline_version=self.pipeline_version,
        )

    def _handlers(self) -> dict[str, Callable[[InterpretationPipelineContext], Mapping[str, Any]]]:
        return {
            STAGE_FOUNDATION: self._foundation.execute,
            STAGE_KNOWLEDGE: self._knowledge.execute,
            STAGE_COMPOSITION: self._composition.execute,
        }
