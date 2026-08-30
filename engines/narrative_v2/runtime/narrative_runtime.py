"""Narrative V2 runtime facade.

Shadow-mode skeleton. Does not replace Pack05. Does not generate narrative.
"""

from __future__ import annotations

import logging
from typing import Any

from engines.narrative_v2.runtime.runtime_context import NarrativeRuntimeContext, PipelineTrace
from engines.narrative_v2.runtime.runtime_errors import (
    PipelineError,
    RuntimeError as V2RuntimeError,
)
from engines.narrative_v2.runtime.runtime_events import EventLog, RuntimeEvent, RuntimeFailed, now
from engines.narrative_v2.runtime.runtime_metrics import RuntimeMetrics
from engines.narrative_v2.runtime.runtime_pipeline import RuntimePipeline
from engines.narrative_v2.runtime.runtime_registry import RuntimeRegistry
from engines.narrative_v2.runtime.runtime_result import NarrativeRuntimeResult
from engines.narrative_v2.runtime.runtime_state import RuntimeState, transition
from engines.narrative_v2.runtime.runtime_validator import RuntimeValidator

logger = logging.getLogger(__name__)

SHADOW_MODE = True
RUNTIME_VERSION = "0.1.0-skeleton"
NARRATIVE_VERSION = "bte.narrative.v2"


class NarrativeRuntime:
    """Orchestrates the Narrative V2 pipeline skeleton.

    Pack05 remains production. This runtime executes independently.
    """

    SHADOW_MODE = SHADOW_MODE
    VERSION = RUNTIME_VERSION

    def __init__(
        self,
        *,
        registry: RuntimeRegistry | None = None,
        validator: RuntimeValidator | None = None,
    ) -> None:
        self._registry = registry or RuntimeRegistry()
        self._validator = validator or RuntimeValidator()
        self._pipeline = RuntimePipeline(self)
        self._metrics = RuntimeMetrics()
        self._events = EventLog()
        self._errors: list[str] = []
        self._executed_stages: list[str] = []
        self._context: NarrativeRuntimeContext | None = None
        self._result: NarrativeRuntimeResult | None = None

    @property
    def shadow_mode(self) -> bool:
        """True while Narrative V2 must not replace Pack05."""
        return True

    @property
    def replaces_pack05(self) -> bool:
        """Production switch. Always False in N-IMP-01."""
        return False

    @property
    def portal_connected(self) -> bool:
        """Portal integration. Always False in N-IMP-01."""
        return False

    @property
    def pipeline(self) -> RuntimePipeline:
        """Bound skeleton pipeline."""
        return self._pipeline

    @property
    def registry(self) -> RuntimeRegistry:
        """Builder registry (identities only)."""
        return self._registry

    @property
    def validator(self) -> RuntimeValidator:
        """Skeleton validator."""
        return self._validator

    @property
    def metrics(self) -> RuntimeMetrics:
        """Collected runtime metrics."""
        return self._metrics

    @property
    def context(self) -> NarrativeRuntimeContext | None:
        """Current runtime context, if initialized."""
        return self._context

    @property
    def events(self) -> tuple[RuntimeEvent, ...]:
        """Emitted runtime events."""
        return self._events.events

    @property
    def executed_stages(self) -> tuple[str, ...]:
        """Completed stage names in order."""
        return tuple(self._executed_stages)

    def require_context(self) -> NarrativeRuntimeContext:
        """Return context or raise if initialize has not run."""
        if self._context is None:
            raise PipelineError("Runtime is not initialized")
        return self._context

    def emit(self, event: RuntimeEvent) -> RuntimeEvent:
        """Record a runtime event."""
        return self._events.emit(event)

    def record_stage(self, stage: str) -> None:
        """Append a completed stage name."""
        self._executed_stages.append(stage)

    def initialize(
        self,
        canonical_analysis: object | None = None,
    ) -> NarrativeRuntimeContext:
        """Create runtime context. Does not interpret Canonical Analysis."""
        if self._context is not None:
            raise PipelineError("Runtime already initialized")
        self._context = NarrativeRuntimeContext(
            canonical_analysis=canonical_analysis,
            runtime_state=RuntimeState.NOT_STARTED,
            metadata=self._base_metadata(),
            trace=PipelineTrace(),
        )
        self._pipeline.initialize()
        logger.debug("narrative_runtime_initialized")
        return self._context

    def run(
        self,
        canonical_analysis: object | None = None,
    ) -> NarrativeRuntimeResult:
        """Execute the empty pipeline in canonical order."""
        started = now()
        try:
            if self._context is None:
                self.initialize(canonical_analysis)
            for stage in self._pipeline.stages:
                if stage in self._executed_stages:
                    continue
                self._pipeline.execute_stage(stage)
            self._metrics.runtime_duration = now() - started
            self._metrics.builder_count = self._registry.builder_count
            self._result = self._build_result()
            return self._result
        except V2RuntimeError as exc:
            self._fail(str(exc))
            self._metrics.runtime_duration = now() - started
            self._metrics.builder_count = self._registry.builder_count
            self._result = self._build_result()
            return self._result

    def _fail(self, message: str) -> None:
        self._errors.append(message)
        self._metrics.error_count = len(self._errors)
        self.emit(RuntimeFailed(timestamp=now()))
        if self._context is None:
            return
        try:
            self._context.runtime_state = transition(
                self._context.runtime_state,
                RuntimeState.FAILED,
            )
        except PipelineError:
            logger.debug("runtime_already_terminal")

    def _build_result(self) -> NarrativeRuntimeResult:
        context = self.require_context()
        self._metrics.builder_count = self._registry.builder_count
        self._metrics.error_count = len(self._errors)
        return NarrativeRuntimeResult(
            status=context.runtime_state.value,
            runtime_metadata=dict(context.metadata),
            pipeline_trace=context.trace.snapshot(),
            presentation=context.presentation,
            errors=tuple(self._errors),
        )

    def _base_metadata(self) -> dict[str, Any]:
        return {
            "shadow_mode": True,
            "replaces_pack05": False,
            "portal_connected": False,
            "runtime_version": RUNTIME_VERSION,
            "narrative_version": NARRATIVE_VERSION,
            "generates_narrative": False,
        }
