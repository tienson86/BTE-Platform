"""Pack 07 Life Optimization result container.

Nested natal/temporal objects live here. Upstream layers stay unchanged.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping

from engines.detailed_interpretation_engine.codec import as_enum, as_str, as_str_tuple
from engines.detailed_interpretation_engine.constants import (
    LIFE_OPTIMIZATION_RULESET_VERSION,
    SCHEMA_LIFE_OPTIMIZATION,
)
from engines.detailed_interpretation_engine.enums import EvaluationStatus
from engines.detailed_interpretation_engine.life_optimization.models import (
    DomainOptimizationPlan,
    FiveElementOptimizationPlan,
    NatalOptimizationPlan,
    OptimizationAction,
    OptimizationConflict,
    OptimizationSaturation,
    TemporalOptimizationPlan,
    UsefulGodOptimizationPlan,
)
from engines.detailed_interpretation_engine.value_objects import ConfidenceValue


def _as_actions(value: Any) -> tuple[OptimizationAction, ...]:
    if value is None:
        return ()
    items: list[OptimizationAction] = []
    for item in value:
        if isinstance(item, OptimizationAction):
            items.append(item)
        elif isinstance(item, (Mapping, str)):
            items.append(OptimizationAction.from_dict(item))
    return tuple(items)


def _as_conflicts(value: Any) -> tuple[OptimizationConflict, ...]:
    if value is None:
        return ()
    return tuple(
        item if isinstance(item, OptimizationConflict) else OptimizationConflict.from_dict(item)
        for item in value
        if isinstance(item, (OptimizationConflict, Mapping, str))
    )


def _as_elements(value: Any) -> tuple[FiveElementOptimizationPlan, ...]:
    if value is None:
        return ()
    return tuple(
        item
        if isinstance(item, FiveElementOptimizationPlan)
        else FiveElementOptimizationPlan.from_dict(item)
        for item in value
        if isinstance(item, (FiveElementOptimizationPlan, Mapping, str))
    )


def _as_domain_plans(value: Any) -> dict[str, DomainOptimizationPlan]:
    if not isinstance(value, Mapping):
        return {}
    plans: dict[str, DomainOptimizationPlan] = {}
    for key, item in value.items():
        domain_id = str(key)
        if isinstance(item, DomainOptimizationPlan):
            plans[domain_id] = item
        elif isinstance(item, (Mapping, str)):
            plans[domain_id] = DomainOptimizationPlan.from_dict(item, domain_id)
    return plans


def _as_natal(value: Any) -> NatalOptimizationPlan:
    if isinstance(value, NatalOptimizationPlan):
        return value
    return NatalOptimizationPlan.from_dict(value if isinstance(value, (Mapping, str)) else None)


def _as_temporal(value: Any) -> TemporalOptimizationPlan:
    if isinstance(value, TemporalOptimizationPlan):
        return value
    if value is None:
        return TemporalOptimizationPlan()
    return TemporalOptimizationPlan.from_dict(value if isinstance(value, (Mapping, str)) else None)


def _as_useful(value: Any) -> UsefulGodOptimizationPlan:
    if isinstance(value, UsefulGodOptimizationPlan):
        return value
    return UsefulGodOptimizationPlan.from_dict(value if isinstance(value, (Mapping, str)) else None)


def _as_saturations(value: Any) -> tuple[OptimizationSaturation, ...]:
    if value is None:
        return ()
    return tuple(
        item if isinstance(item, OptimizationSaturation) else OptimizationSaturation.from_dict(item)
        for item in value
        if isinstance(item, (OptimizationSaturation, Mapping))
    )


@dataclass(frozen=True, slots=True)
class LifeOptimizationResult:
    """DI-18 LifeOptimizationResult. Empty until the engine runs."""

    schema_version: str = SCHEMA_LIFE_OPTIMIZATION
    analysis_id: str = ""
    ruleset_version: str = LIFE_OPTIMIZATION_RULESET_VERSION
    state: EvaluationStatus = EvaluationStatus.NOT_EVALUATED
    natal_plan: NatalOptimizationPlan = field(default_factory=NatalOptimizationPlan)
    temporal_plan: TemporalOptimizationPlan = field(default_factory=TemporalOptimizationPlan)
    top_priorities: tuple[str, ...] = ()
    actions: tuple[OptimizationAction, ...] = ()
    conflicts: tuple[OptimizationConflict, ...] = ()
    domain_plans: dict[str, DomainOptimizationPlan] = field(default_factory=dict)
    element_plan: tuple[FiveElementOptimizationPlan, ...] = ()
    useful_god_plan: UsefulGodOptimizationPlan = field(default_factory=UsefulGodOptimizationPlan)
    saturations: tuple[OptimizationSaturation, ...] = ()
    conditions: tuple[str, ...] = ()
    warnings: tuple[str, ...] = ()
    evidence_ids: tuple[str, ...] = ()
    trace_ids: tuple[str, ...] = ()
    confidence: ConfidenceValue = field(default_factory=ConfidenceValue)

    @classmethod
    def from_dict(cls, data: Mapping[str, Any] | None) -> LifeOptimizationResult:
        """Rebuild optimization from a mapping. String shells stay compatible."""
        payload = data or {}
        return cls(
            schema_version=as_str(payload.get("schema_version"), SCHEMA_LIFE_OPTIMIZATION),
            analysis_id=as_str(payload.get("analysis_id")),
            ruleset_version=as_str(
                payload.get("ruleset_version"),
                LIFE_OPTIMIZATION_RULESET_VERSION,
            ),
            state=as_enum(
                EvaluationStatus,
                payload.get("state") or payload.get("status"),
                EvaluationStatus.NOT_EVALUATED,
            ),
            natal_plan=_as_natal(payload.get("natal_plan")),
            temporal_plan=_as_temporal(payload.get("temporal_plan")),
            top_priorities=as_str_tuple(payload.get("top_priorities")),
            actions=_as_actions(payload.get("actions")),
            conflicts=_as_conflicts(payload.get("conflicts")),
            domain_plans=_as_domain_plans(payload.get("domain_plans")),
            element_plan=_as_elements(payload.get("element_plan")),
            useful_god_plan=_as_useful(payload.get("useful_god_plan")),
            saturations=_as_saturations(payload.get("saturations")),
            conditions=as_str_tuple(payload.get("conditions")),
            warnings=as_str_tuple(payload.get("warnings")),
            evidence_ids=as_str_tuple(payload.get("evidence_ids")),
            trace_ids=as_str_tuple(payload.get("trace_ids")),
            confidence=ConfidenceValue.from_dict(payload.get("confidence")),
        )


OptimizationResult = LifeOptimizationResult
