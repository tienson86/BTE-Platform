"""Pack 07 optimization result shells. No action generation."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping

from engines.detailed_interpretation_engine.codec import as_enum, as_str, as_str_tuple
from engines.detailed_interpretation_engine.constants import SCHEMA_LIFE_OPTIMIZATION
from engines.detailed_interpretation_engine.enums import EvaluationStatus
from engines.detailed_interpretation_engine.value_objects import ConfidenceValue


@dataclass(frozen=True, slots=True)
class LifeOptimizationResult:
    """DI-18 LifeOptimizationResult container. Empty until the engine runs."""

    schema_version: str = SCHEMA_LIFE_OPTIMIZATION
    state: EvaluationStatus = EvaluationStatus.NOT_EVALUATED
    natal_plan: str = ""
    temporal_plan: str = "not_evaluated"
    top_priorities: tuple[str, ...] = ()
    actions: tuple[str, ...] = ()
    conflicts: tuple[str, ...] = ()
    domain_plans: dict[str, str] = field(default_factory=dict)
    element_plan: tuple[str, ...] = ()
    useful_god_plan: str = ""
    conditions: tuple[str, ...] = ()
    warnings: tuple[str, ...] = ()
    evidence_ids: tuple[str, ...] = ()
    trace_ids: tuple[str, ...] = ()
    confidence: ConfidenceValue = field(default_factory=ConfidenceValue)

    @classmethod
    def from_dict(cls, data: Mapping[str, Any] | None) -> LifeOptimizationResult:
        """Rebuild optimization from a mapping."""
        payload = data or {}
        plans_raw = payload.get("domain_plans")
        domain_plans = (
            {str(key): str(item) for key, item in plans_raw.items()}
            if isinstance(plans_raw, Mapping)
            else {}
        )
        return cls(
            schema_version=as_str(payload.get("schema_version"), SCHEMA_LIFE_OPTIMIZATION),
            state=as_enum(
                EvaluationStatus,
                payload.get("state") or payload.get("status"),
                EvaluationStatus.NOT_EVALUATED,
            ),
            natal_plan=as_str(payload.get("natal_plan")),
            temporal_plan=as_str(payload.get("temporal_plan"), "not_evaluated"),
            top_priorities=as_str_tuple(payload.get("top_priorities")),
            actions=as_str_tuple(payload.get("actions")),
            conflicts=as_str_tuple(payload.get("conflicts")),
            domain_plans=domain_plans,
            element_plan=as_str_tuple(payload.get("element_plan")),
            useful_god_plan=as_str(payload.get("useful_god_plan")),
            conditions=as_str_tuple(payload.get("conditions")),
            warnings=as_str_tuple(payload.get("warnings")),
            evidence_ids=as_str_tuple(payload.get("evidence_ids")),
            trace_ids=as_str_tuple(payload.get("trace_ids")),
            confidence=ConfidenceValue.from_dict(payload.get("confidence")),
        )


OptimizationResult = LifeOptimizationResult
