"""Machine-readable Decision Trace for every Decision Pipeline run."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Sequence

TRACE_STEPS: tuple[str, ...] = (
    "candidate_generation",
    "priority_ordering",
    "conflict_resolution",
    "override_decision",
    "final_publication",
)


@dataclass(slots=True)
class DecisionTraceStep:
    """One ordered trace step with stage, package, rules, outputs, timestamp."""

    step_id: str
    stage_id: str
    package_id: str | None
    package_version: str | None
    rule_ids: tuple[str, ...]
    outputs: tuple[str, ...]
    timestamp: str
    payload: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Serialize one trace step."""
        return {
            "step_id": self.step_id,
            "stage": self.stage_id,
            "package": self.package_id,
            "package_version": self.package_version,
            "rule_ids": list(self.rule_ids),
            "outputs": list(self.outputs),
            "timestamp": self.timestamp,
            "payload": dict(self.payload),
        }


@dataclass(slots=True)
class DecisionTrace:
    """Complete decision trace consumed by future Report / AI layers."""

    pipeline_id: str
    pipeline_version: str
    started_at: str | None = None
    completed_at: str | None = None
    steps: tuple[DecisionTraceStep, ...] = ()

    def to_dict(self) -> dict[str, Any]:
        """Serialize the decision trace."""
        return {
            "pipeline_id": self.pipeline_id,
            "pipeline_version": self.pipeline_version,
            "started_at": self.started_at,
            "completed_at": self.completed_at,
            "steps": [step.to_dict() for step in self.steps],
        }


def build_trace_steps(
    *,
    stage_id: str,
    package_id: str | None,
    package_version: str | None,
    rule_ids: Sequence[str],
    outputs: Sequence[str],
    timestamp: str,
    payload: dict[str, Any],
) -> tuple[DecisionTraceStep, ...]:
    """Map an executed stage onto one or more canonical trace steps."""
    mapping = {
        "useful_god_foundation": ("candidate_generation",),
        "useful_god_priority": ("priority_ordering", "conflict_resolution"),
        "useful_god_override": ("override_decision", "final_publication"),
    }
    step_ids = mapping.get(stage_id, ())
    return tuple(
        DecisionTraceStep(
            step_id=step_id,
            stage_id=stage_id,
            package_id=package_id,
            package_version=package_version,
            rule_ids=tuple(rule_ids),
            outputs=tuple(outputs),
            timestamp=timestamp,
            payload=dict(payload),
        )
        for step_id in step_ids
    )
