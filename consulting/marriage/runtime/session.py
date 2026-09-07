"""Runtime session. Holds B01 context plus B02 lifecycle and traces."""

from __future__ import annotations

from dataclasses import dataclass, field

from consulting.marriage.dto.response import RuntimeError, RuntimeWarning, StageTiming
from consulting.marriage.exceptions import MarriageInternalError
from consulting.marriage.runtime.context import MarriageRuntimeContext
from consulting.marriage.runtime.lifecycle import LIFECYCLE_ORDER, RuntimeLifecycleState
from consulting.marriage.runtime.trace import StageTrace


@dataclass(slots=True)
class MarriageRuntimeSession:
    """Per-consultation runtime session. No global mutable state."""

    context: MarriageRuntimeContext
    lifecycle_state: RuntimeLifecycleState = RuntimeLifecycleState.CREATED
    traces: list[StageTrace] = field(default_factory=list)
    errors: list[RuntimeError] = field(default_factory=list)

    def transition(self, target: RuntimeLifecycleState) -> None:
        """Move lifecycle forward. Reverse transitions are rejected."""
        current_index = LIFECYCLE_ORDER.index(self.lifecycle_state)
        target_index = LIFECYCLE_ORDER.index(target)
        if target_index < current_index:
            raise MarriageInternalError(
                f"invalid_lifecycle_transition:{self.lifecycle_state.value}:{target.value}"
            )
        self.lifecycle_state = target

    def add_warning(self, warning: RuntimeWarning) -> None:
        """Append a runtime warning onto the inner context."""
        self.context.warnings.append(warning)

    def add_trace(self, trace: StageTrace) -> None:
        """Record a completed stage trace and duration."""
        self.traces.append(trace)
        self.context.timings.append(
            StageTiming(stage=trace.stage, duration_ms=trace.duration_ms)
        )
