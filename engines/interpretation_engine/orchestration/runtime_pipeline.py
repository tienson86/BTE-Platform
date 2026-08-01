"""Pack 03 Runtime Pipeline orchestration.

PackInterpretationContext
  -> Interpreter Runtime
  -> Sentence Runtime
  -> Template Runtime
  -> Placeholder Runtime
  -> Explanation Runtime
  -> InterpretationResult

Infrastructure only. No business logic / no rendering.
"""

from __future__ import annotations

import logging
from typing import Any

from engines.interpretation_engine.context.interpretation_context import (
    PackInterpretationContext,
)
from engines.interpretation_engine.explanation_runtime.runtime import ExplanationRuntime
from engines.interpretation_engine.interpreter_runtime.runtime import InterpreterRuntime
from engines.interpretation_engine.models.interpretation_result import InterpretationResult
from engines.interpretation_engine.models.metadata import Metadata
from engines.interpretation_engine.models.trace_information import TraceInformation
from engines.interpretation_engine.models.version_info import VersionInfo
from engines.interpretation_engine.placeholder_runtime.runtime import PlaceholderRuntime
from engines.interpretation_engine.runtime.base import BaseRuntime
from engines.interpretation_engine.runtime.contracts import RuntimeExecuteResult
from engines.interpretation_engine.sentence_runtime.runtime import SentenceRuntime
from engines.interpretation_engine.template_runtime.runtime import TemplateRuntime

logger = logging.getLogger(__name__)

_STAGE_ORDER = (
    "interpreter_runtime",
    "sentence_runtime",
    "template_runtime",
    "placeholder_runtime",
    "explanation_runtime",
)


class RuntimePipeline(BaseRuntime):
    """Orchestrates Pack 03 stage runtimes into InterpretationResult shells."""

    def __init__(
        self,
        *,
        runtime_id: str = "runtime_pipeline",
        interpreter_runtime: InterpreterRuntime | None = None,
        sentence_runtime: SentenceRuntime | None = None,
        template_runtime: TemplateRuntime | None = None,
        placeholder_runtime: PlaceholderRuntime | None = None,
        explanation_runtime: ExplanationRuntime | None = None,
    ) -> None:
        """Initialize pipeline with injected stage runtimes (DI only)."""
        super().__init__(runtime_id=runtime_id)
        self._interpreter = interpreter_runtime or InterpreterRuntime()
        self._sentence = sentence_runtime or SentenceRuntime()
        self._template = template_runtime or TemplateRuntime()
        self._placeholder = placeholder_runtime or PlaceholderRuntime()
        self._explanation = explanation_runtime or ExplanationRuntime()
        self._stages: tuple[BaseRuntime, ...] = (
            self._interpreter,
            self._sentence,
            self._template,
            self._placeholder,
            self._explanation,
        )

    @property
    def stages(self) -> tuple[BaseRuntime, ...]:
        """Return ordered stage runtimes."""
        return self._stages

    def initialize(self) -> None:
        """Initialize pipeline and all stage runtimes."""
        for stage in self._stages:
            stage.initialize()
        super().initialize()

    def shutdown(self) -> None:
        """Shutdown all stage runtimes then the pipeline."""
        for stage in reversed(self._stages):
            stage.shutdown()
        super().shutdown()

    def validate(self) -> bool:
        """Validate pipeline and every stage runtime."""
        if not super().validate():
            return False
        return all(stage.validate() for stage in self._stages)

    def _execute_body(self, context: Any) -> RuntimeExecuteResult:
        """Execute ordered stage shells and assemble InterpretationResult."""
        if not isinstance(context, PackInterpretationContext):
            return RuntimeExecuteResult(
                runtime_id=self.runtime_id,
                success=False,
                messages=("pack_interpretation_context_required",),
            )
        if not context.validate():
            return RuntimeExecuteResult(
                runtime_id=self.runtime_id,
                success=False,
                messages=("pack_interpretation_context_invalid",),
            )

        stage_results: dict[str, RuntimeExecuteResult] = {}
        stage_ids: list[str] = []
        messages: list[str] = []
        for stage in self._stages:
            result = stage.execute(context)
            stage_results[stage.runtime_id] = result
            stage_ids.append(stage.runtime_id)
            messages.extend(result.messages)
            if not result.success:
                logger.error(
                    "runtime_pipeline_stage_failed",
                    extra={
                        "pipeline_id": self.runtime_id,
                        "stage": stage.runtime_id,
                        "messages": list(result.messages),
                    },
                )
                return RuntimeExecuteResult(
                    runtime_id=self.runtime_id,
                    success=False,
                    payload={
                        "context_id": context.id,
                        "failed_stage": stage.runtime_id,
                        "stage_ids": list(stage_ids),
                        "stage_results": {
                            key: {
                                "success": value.success,
                                "messages": list(value.messages),
                            }
                            for key, value in stage_results.items()
                        },
                    },
                    messages=tuple(messages) + ("runtime_pipeline_failed",),
                )

        explanation_payload = stage_results["explanation_runtime"].payload
        explanation_refs = tuple(explanation_payload.get("explanation_refs", ()))
        interpretation_result = self._build_result(
            context=context,
            stage_ids=tuple(stage_ids),
            explanation_refs=explanation_refs,
            messages=tuple(messages) + ("runtime_pipeline_ok",),
        )
        logger.info(
            "runtime_pipeline_ok",
            extra={
                "pipeline_id": self.runtime_id,
                "context_id": context.id,
                "stages": list(stage_ids),
            },
        )
        return RuntimeExecuteResult(
            runtime_id=self.runtime_id,
            success=True,
            payload={
                "context_id": context.id,
                "stage_ids": list(stage_ids),
                "interpretation_result": interpretation_result,
                "stage_order": list(_STAGE_ORDER),
            },
            messages=tuple(messages) + ("runtime_pipeline_ok",),
        )

    def _build_result(
        self,
        *,
        context: PackInterpretationContext,
        stage_ids: tuple[str, ...],
        explanation_refs: tuple[str, ...],
        messages: tuple[str, ...],
    ) -> InterpretationResult:
        """Build a structural InterpretationResult shell (no narrative content)."""
        metadata = Metadata(
            id=f"meta_{context.id}",
            version_info=VersionInfo(schema_version=context.version or "1.0.0"),
            created_at=context.created_at,
            updated_at=context.updated_at,
            completed_at=context.completed_at,
            attributes={"source": "runtime_pipeline"},
        )
        trace = TraceInformation(
            trace_id=f"trace_{context.id}",
            pipeline_id=context.pipeline_id,
            source_final_result_id=context.source_final_result_id,
            stage_ids=stage_ids,
            events=tuple(context.trace) + ("runtime_pipeline_complete",),
        )
        return InterpretationResult(
            id=f"ir_{context.id}",
            metadata=metadata,
            trace=trace,
            source_final_result_id=context.source_final_result_id,
            pipeline_id=context.pipeline_id,
            success=True,
            sections=(),
            explanation_refs=explanation_refs,
            messages=messages,
            attributes={"runtime_id": self.runtime_id},
        )
