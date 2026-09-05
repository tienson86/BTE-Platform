"""Life Optimization objects. Upstream natal, luck, and temporal stay on their own results."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping

from engines.detailed_interpretation_engine.codec import as_str, as_str_tuple
from engines.detailed_interpretation_engine.enums import EvaluationStatus
from engines.detailed_interpretation_engine.value_objects import ConfidenceValue


def _mapping(value: Any) -> Mapping[str, Any] | None:
    return value if isinstance(value, Mapping) else None


@dataclass(frozen=True, slots=True)
class ActionContraindication:
    """Conditional caution. Not an absolute ban unless a frozen rule says so."""

    condition: str = ""
    reason_key: str = ""
    severity: str = "caution"

    @classmethod
    def from_dict(cls, data: Mapping[str, Any] | None) -> ActionContraindication:
        """Rebuild one contraindication."""
        payload = data or {}
        return cls(
            condition=as_str(payload.get("condition")),
            reason_key=as_str(payload.get("reason_key")),
            severity=as_str(payload.get("severity"), "caution") or "caution",
        )


@dataclass(frozen=True, slots=True)
class OptimizationSaturation:
    """More favorable force is not automatically better."""

    domain: str = ""
    layer: str = ""
    state: str = ""
    guard: str = "protect_before_expand"

    @classmethod
    def from_dict(cls, data: Mapping[str, Any] | None) -> OptimizationSaturation:
        """Rebuild one saturation guard."""
        payload = data or {}
        return cls(
            domain=as_str(payload.get("domain")),
            layer=as_str(payload.get("layer")),
            state=as_str(payload.get("state")),
            guard=as_str(payload.get("guard"), "protect_before_expand") or "protect_before_expand",
        )


@dataclass(frozen=True, slots=True)
class DomainConversionEfficiency:
    """Where capability fails to become useful expression."""

    domain: str = ""
    from_capability: str = ""
    to_expression: str = ""
    efficiency: str = "unresolved"
    bottleneck: str = ""

    @classmethod
    def from_dict(cls, data: Mapping[str, Any] | str | None) -> DomainConversionEfficiency:
        """Rebuild conversion efficiency. String shells stay unresolved."""
        if isinstance(data, str):
            return cls(efficiency=data or "unresolved")
        payload = data or {}
        return cls(
            domain=as_str(payload.get("domain")),
            from_capability=as_str(payload.get("from_capability")),
            to_expression=as_str(payload.get("to_expression")),
            efficiency=as_str(payload.get("efficiency"), "unresolved") or "unresolved",
            bottleneck=as_str(payload.get("bottleneck")),
        )


@dataclass(frozen=True, slots=True)
class OptimizationTarget:
    """Structural function to change. Not an object to buy."""

    target_id: str = ""
    domain: str = ""
    mechanism: str = ""
    action_type: str = "monitor"
    priority: str = "P2"
    reason: str = ""
    conditions: tuple[str, ...] = ()
    contraindications: tuple[ActionContraindication, ...] = ()
    evidence_ids: tuple[str, ...] = ()
    trace_ids: tuple[str, ...] = ()
    confidence: ConfidenceValue = field(default_factory=ConfidenceValue)

    @classmethod
    def from_dict(cls, data: Mapping[str, Any] | None) -> OptimizationTarget:
        """Rebuild one optimization target."""
        payload = data or {}
        raw = payload.get("contraindications") or ()
        return cls(
            target_id=as_str(payload.get("target_id")),
            domain=as_str(payload.get("domain")),
            mechanism=as_str(payload.get("mechanism")),
            action_type=as_str(payload.get("action_type"), "monitor") or "monitor",
            priority=as_str(payload.get("priority"), "P2") or "P2",
            reason=as_str(payload.get("reason")),
            conditions=as_str_tuple(payload.get("conditions")),
            contraindications=tuple(
                ActionContraindication.from_dict(item if isinstance(item, Mapping) else None)
                for item in raw
                if isinstance(item, Mapping)
            ),
            evidence_ids=as_str_tuple(payload.get("evidence_ids")),
            trace_ids=as_str_tuple(payload.get("trace_ids")),
            confidence=ConfidenceValue.from_dict(payload.get("confidence")),
        )


@dataclass(frozen=True, slots=True)
class OptimizationAction:
    """One evidence-backed action. Engine stores keys, not Vietnamese prose."""

    action_id: str = ""
    target_domain: str = ""
    target_mechanism: str = ""
    action_type: str = "monitor"
    priority: str = "P2"
    recommended_action_key: str = ""
    reason_key: str = ""
    conditions: tuple[str, ...] = ()
    contraindications: tuple[ActionContraindication, ...] = ()
    time_scope: str = "natal_long_term"
    expected_structural_effect: str = ""
    evidence_ids: tuple[str, ...] = ()
    trace_ids: tuple[str, ...] = ()
    confidence: ConfidenceValue = field(default_factory=ConfidenceValue)
    state: str = "recommended"
    category: str = "domain_bottleneck"
    driver_kind: str = "domain"

    @classmethod
    def from_dict(cls, data: Mapping[str, Any] | str | None) -> OptimizationAction:
        """Rebuild one action. String shells keep the id only."""
        if isinstance(data, str):
            return cls(action_id=data)
        payload = data or {}
        raw = payload.get("contraindications") or ()
        return cls(
            action_id=as_str(payload.get("action_id")),
            target_domain=as_str(payload.get("target_domain") or payload.get("domain")),
            target_mechanism=as_str(payload.get("target_mechanism") or payload.get("mechanism")),
            action_type=as_str(payload.get("action_type"), "monitor") or "monitor",
            priority=as_str(payload.get("priority"), "P2") or "P2",
            recommended_action_key=as_str(payload.get("recommended_action_key")),
            reason_key=as_str(payload.get("reason_key")),
            conditions=as_str_tuple(payload.get("conditions")),
            contraindications=tuple(
                ActionContraindication.from_dict(item if isinstance(item, Mapping) else None)
                for item in raw
                if isinstance(item, Mapping)
            ),
            time_scope=as_str(payload.get("time_scope"), "natal_long_term") or "natal_long_term",
            expected_structural_effect=as_str(payload.get("expected_structural_effect")),
            evidence_ids=as_str_tuple(payload.get("evidence_ids")),
            trace_ids=as_str_tuple(payload.get("trace_ids")),
            confidence=ConfidenceValue.from_dict(payload.get("confidence")),
            state=as_str(payload.get("state"), "recommended") or "recommended",
            category=as_str(payload.get("category"), "domain_bottleneck") or "domain_bottleneck",
            driver_kind=as_str(payload.get("driver_kind"), "domain") or "domain",
        )


@dataclass(frozen=True, slots=True)
class OptimizationConflict:
    """Cross-domain trade-off. Do not silently choose one side."""

    conflict_id: str = ""
    action_a: str = ""
    action_b: str = ""
    domains: tuple[str, ...] = ()
    severity: str = "moderate"
    resolution_mode: str = "conditional_balance"
    conditions: tuple[str, ...] = ()
    evidence_ids: tuple[str, ...] = ()
    trace_ids: tuple[str, ...] = ()

    @classmethod
    def from_dict(cls, data: Mapping[str, Any] | str | None) -> OptimizationConflict:
        """Rebuild one conflict. String shells keep the id only."""
        if isinstance(data, str):
            return cls(conflict_id=data)
        payload = data or {}
        return cls(
            conflict_id=as_str(payload.get("conflict_id")),
            action_a=as_str(payload.get("action_a")),
            action_b=as_str(payload.get("action_b")),
            domains=as_str_tuple(payload.get("domains")),
            severity=as_str(payload.get("severity"), "moderate") or "moderate",
            resolution_mode=as_str(payload.get("resolution_mode"), "conditional_balance")
            or "conditional_balance",
            conditions=as_str_tuple(payload.get("conditions")),
            evidence_ids=as_str_tuple(payload.get("evidence_ids")),
            trace_ids=as_str_tuple(payload.get("trace_ids")),
        )


@dataclass(frozen=True, slots=True)
class NatalOptimizationPlan:
    """Long-term structural actions. Distinct from the current luck/annual plan."""

    state: EvaluationStatus = EvaluationStatus.NOT_EVALUATED
    summary_key: str = ""
    action_ids: tuple[str, ...] = ()
    conditions: tuple[str, ...] = ()
    warnings: tuple[str, ...] = ()
    trace_ids: tuple[str, ...] = ()

    @classmethod
    def from_dict(cls, data: Mapping[str, Any] | str | None) -> NatalOptimizationPlan:
        """Rebuild natal plan. String shells stay not_evaluated."""
        if isinstance(data, str):
            return cls(summary_key=data)
        payload = data or {}
        status_raw = payload.get("state") or payload.get("status")
        return cls(
            state=_status(status_raw),
            summary_key=as_str(payload.get("summary_key") or payload.get("summary")),
            action_ids=as_str_tuple(payload.get("action_ids")),
            conditions=as_str_tuple(payload.get("conditions")),
            warnings=as_str_tuple(payload.get("warnings")),
            trace_ids=as_str_tuple(payload.get("trace_ids")),
        )


@dataclass(frozen=True, slots=True)
class TemporalOptimizationPlan:
    """Current Đại Vận / current Annual adjustments. Does not rewrite natal."""

    state: EvaluationStatus = EvaluationStatus.NOT_EVALUATED
    summary_key: str = "not_evaluated"
    time_window: str = ""
    luck_window: str = ""
    annual_window: str = ""
    action_ids: tuple[str, ...] = ()
    saturations: tuple[OptimizationSaturation, ...] = ()
    conditions: tuple[str, ...] = ()
    warnings: tuple[str, ...] = ()
    trace_ids: tuple[str, ...] = ()

    @classmethod
    def from_dict(cls, data: Mapping[str, Any] | str | None) -> TemporalOptimizationPlan:
        """Rebuild temporal plan. String shells stay not_evaluated."""
        if isinstance(data, str):
            return cls(summary_key=data or "not_evaluated")
        payload = data or {}
        raw = payload.get("saturations") or ()
        return cls(
            state=_status(payload.get("state") or payload.get("status")),
            summary_key=as_str(payload.get("summary_key") or payload.get("summary"), "not_evaluated")
            or "not_evaluated",
            time_window=as_str(payload.get("time_window")),
            luck_window=as_str(payload.get("luck_window")),
            annual_window=as_str(payload.get("annual_window")),
            action_ids=as_str_tuple(payload.get("action_ids")),
            saturations=tuple(
                OptimizationSaturation.from_dict(item if isinstance(item, Mapping) else None)
                for item in raw
                if isinstance(item, Mapping)
            ),
            conditions=as_str_tuple(payload.get("conditions")),
            warnings=as_str_tuple(payload.get("warnings")),
            trace_ids=as_str_tuple(payload.get("trace_ids")),
        )


@dataclass(frozen=True, slots=True)
class DomainOptimizationPlan:
    """One published domain's natal plan plus temporal adjustments."""

    domain: str = ""
    driver: str = ""
    bottleneck: str = ""
    leakage: str = ""
    conversion_efficiency: DomainConversionEfficiency = field(default_factory=DomainConversionEfficiency)
    priority: str = ""
    recommended_actions: tuple[str, ...] = ()
    avoid_actions: tuple[str, ...] = ()
    conditions: tuple[str, ...] = ()
    temporal_adjustments: tuple[str, ...] = ()
    confidence: ConfidenceValue = field(default_factory=ConfidenceValue)
    trace_ids: tuple[str, ...] = ()
    state: EvaluationStatus = EvaluationStatus.NOT_EVALUATED

    @classmethod
    def from_dict(
        cls,
        data: Mapping[str, Any] | str | None,
        default_id: str = "",
    ) -> DomainOptimizationPlan:
        """Rebuild one domain plan. String shells stay not_evaluated."""
        if isinstance(data, str):
            return cls(domain=default_id, driver=data)
        payload = data or {}
        conversion_raw = payload.get("conversion_efficiency")
        return cls(
            domain=as_str(payload.get("domain"), default_id) or default_id,
            driver=as_str(payload.get("driver")),
            bottleneck=as_str(payload.get("bottleneck")),
            leakage=as_str(payload.get("leakage")),
            conversion_efficiency=DomainConversionEfficiency.from_dict(
                conversion_raw if isinstance(conversion_raw, (Mapping, str)) else None
            ),
            priority=as_str(payload.get("priority")),
            recommended_actions=as_str_tuple(payload.get("recommended_actions")),
            avoid_actions=as_str_tuple(payload.get("avoid_actions")),
            conditions=as_str_tuple(payload.get("conditions")),
            temporal_adjustments=as_str_tuple(payload.get("temporal_adjustments")),
            confidence=ConfidenceValue.from_dict(payload.get("confidence")),
            trace_ids=as_str_tuple(payload.get("trace_ids")),
            state=_status(payload.get("state")),
        )


@dataclass(frozen=True, slots=True)
class UsefulGodOptimizationPlan:
    """Function-first Useful God plan. Not color, object, or direction advice."""

    useful_god: str = ""
    supporting_gods: tuple[str, ...] = ()
    avoidance_context: tuple[str, ...] = ()
    functional_targets: tuple[str, ...] = ()
    domain_mappings: tuple[str, ...] = ()
    actions: tuple[str, ...] = ()
    conditions: tuple[str, ...] = ()
    confidence: ConfidenceValue = field(default_factory=ConfidenceValue)
    trace_ids: tuple[str, ...] = ()

    @classmethod
    def from_dict(cls, data: Mapping[str, Any] | str | None) -> UsefulGodOptimizationPlan:
        """Rebuild Useful God plan. String shells stay empty."""
        if isinstance(data, str):
            return cls(useful_god=data)
        payload = data or {}
        return cls(
            useful_god=as_str(payload.get("useful_god")),
            supporting_gods=as_str_tuple(payload.get("supporting_gods")),
            avoidance_context=as_str_tuple(payload.get("avoidance_context")),
            functional_targets=as_str_tuple(payload.get("functional_targets")),
            domain_mappings=as_str_tuple(payload.get("domain_mappings")),
            actions=as_str_tuple(payload.get("actions")),
            conditions=as_str_tuple(payload.get("conditions")),
            confidence=ConfidenceValue.from_dict(payload.get("confidence")),
            trace_ids=as_str_tuple(payload.get("trace_ids")),
        )


@dataclass(frozen=True, slots=True)
class FiveElementOptimizationPlan:
    """Function-first elemental direction. Low count does not auto-add the element."""

    element: str = ""
    current_role: str = ""
    desired_role: str = ""
    action_direction: str = "monitor"
    target_domains: tuple[str, ...] = ()
    conditions: tuple[str, ...] = ()
    contraindications: tuple[ActionContraindication, ...] = ()
    confidence: ConfidenceValue = field(default_factory=ConfidenceValue)
    trace_ids: tuple[str, ...] = ()

    @classmethod
    def from_dict(cls, data: Mapping[str, Any] | str | None) -> FiveElementOptimizationPlan:
        """Rebuild one element plan. String shells keep the element token."""
        if isinstance(data, str):
            return cls(element=data)
        payload = data or {}
        raw = payload.get("contraindications") or ()
        return cls(
            element=as_str(payload.get("element")),
            current_role=as_str(payload.get("current_role")),
            desired_role=as_str(payload.get("desired_role")),
            action_direction=as_str(payload.get("action_direction"), "monitor") or "monitor",
            target_domains=as_str_tuple(payload.get("target_domains")),
            conditions=as_str_tuple(payload.get("conditions")),
            contraindications=tuple(
                ActionContraindication.from_dict(item if isinstance(item, Mapping) else None)
                for item in raw
                if isinstance(item, Mapping)
            ),
            confidence=ConfidenceValue.from_dict(payload.get("confidence")),
            trace_ids=as_str_tuple(payload.get("trace_ids")),
        )


def _status(value: Any) -> EvaluationStatus:
    if value is None or value == "":
        return EvaluationStatus.NOT_EVALUATED
    if isinstance(value, EvaluationStatus):
        return value
    try:
        return EvaluationStatus(str(value))
    except ValueError:
        return EvaluationStatus.NOT_EVALUATED
