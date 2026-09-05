"""Luck Interaction objects. Natal Domain and Luck Activation stay on their own results."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping

from engines.detailed_interpretation_engine.codec import as_str, as_str_tuple
from engines.detailed_interpretation_engine.value_objects import ConfidenceValue


@dataclass(frozen=True, slots=True)
class ResourceShift:
    """One activation consumes structural capacity of another. Not natal rewrite."""

    from_domain: str = ""
    to_domain: str = ""
    capacity_kind: str = "structural_capacity"
    intensity: str = "moderate"
    evidence_ids: tuple[str, ...] = ()
    trace_ids: tuple[str, ...] = ()

    @classmethod
    def from_dict(cls, data: Mapping[str, Any] | None) -> ResourceShift:
        """Rebuild one resource shift."""
        payload = data or {}
        return cls(
            from_domain=as_str(payload.get("from_domain")),
            to_domain=as_str(payload.get("to_domain")),
            capacity_kind=as_str(payload.get("capacity_kind"), "structural_capacity")
            or "structural_capacity",
            intensity=as_str(payload.get("intensity"), "moderate") or "moderate",
            evidence_ids=as_str_tuple(payload.get("evidence_ids")),
            trace_ids=as_str_tuple(payload.get("trace_ids")),
        )


@dataclass(frozen=True, slots=True)
class StressTransfer:
    """Stress on one activation appears as pressure on another. Not a diagnosis."""

    source_domain: str = ""
    target_domain: str = ""
    source_stress_level: str = ""
    transferred_kind: str = "expression_pressure"
    intensity: str = "moderate"
    evidence_ids: tuple[str, ...] = ()
    trace_ids: tuple[str, ...] = ()

    @classmethod
    def from_dict(cls, data: Mapping[str, Any] | None) -> StressTransfer:
        """Rebuild one stress transfer."""
        payload = data or {}
        return cls(
            source_domain=as_str(payload.get("source_domain")),
            target_domain=as_str(payload.get("target_domain")),
            source_stress_level=as_str(payload.get("source_stress_level")),
            transferred_kind=as_str(payload.get("transferred_kind"), "expression_pressure")
            or "expression_pressure",
            intensity=as_str(payload.get("intensity"), "moderate") or "moderate",
            evidence_ids=as_str_tuple(payload.get("evidence_ids")),
            trace_ids=as_str_tuple(payload.get("trace_ids")),
        )


@dataclass(frozen=True, slots=True)
class DomainInteractionFinding:
    """One activation-to-activation finding. Does not rewrite either activation."""

    finding_id: str = ""
    source_domain: str = ""
    target_domain: str = ""
    interaction_type: str = ""
    strength: str = "moderate"
    conditions: tuple[str, ...] = ()
    risks: tuple[str, ...] = ()
    opportunities: tuple[str, ...] = ()
    evidence_ids: tuple[str, ...] = ()
    trace_ids: tuple[str, ...] = ()
    natal_edge_ref: str = ""
    resource_shift: ResourceShift | None = None
    stress_transfer: StressTransfer | None = None
    confidence: ConfidenceValue = field(default_factory=ConfidenceValue)

    @classmethod
    def from_dict(cls, data: Mapping[str, Any] | None) -> DomainInteractionFinding:
        """Rebuild one interaction finding."""
        payload = data or {}
        shift_raw = payload.get("resource_shift")
        stress_raw = payload.get("stress_transfer")
        return cls(
            finding_id=as_str(payload.get("finding_id")),
            source_domain=as_str(payload.get("source_domain")),
            target_domain=as_str(payload.get("target_domain")),
            interaction_type=as_str(payload.get("interaction_type")),
            strength=as_str(payload.get("strength"), "moderate") or "moderate",
            conditions=as_str_tuple(payload.get("conditions")),
            risks=as_str_tuple(payload.get("risks")),
            opportunities=as_str_tuple(payload.get("opportunities")),
            evidence_ids=as_str_tuple(
                payload.get("evidence_ids") or payload.get("supporting_evidence_ids")
            ),
            trace_ids=as_str_tuple(payload.get("trace_ids")),
            natal_edge_ref=as_str(payload.get("natal_edge_ref")),
            resource_shift=ResourceShift.from_dict(shift_raw)
            if isinstance(shift_raw, Mapping)
            else None,
            stress_transfer=StressTransfer.from_dict(stress_raw)
            if isinstance(stress_raw, Mapping)
            else None,
            confidence=ConfidenceValue.from_dict(payload.get("confidence")),
        )


@dataclass(frozen=True, slots=True)
class LuckInteractionGraphEdge:
    """Activated domain ↔ activated domain. Not luck-force → domain."""

    source: str = ""
    target: str = ""
    relation: str = ""
    evidence_ids: tuple[str, ...] = ()
    finding_id: str = ""

    @classmethod
    def from_dict(cls, data: Mapping[str, Any] | None) -> LuckInteractionGraphEdge:
        """Rebuild one interaction graph edge."""
        payload = data or {}
        return cls(
            source=as_str(payload.get("source")),
            target=as_str(payload.get("target")),
            relation=as_str(payload.get("relation")),
            evidence_ids=as_str_tuple(payload.get("evidence_ids")),
            finding_id=as_str(payload.get("finding_id")),
        )


@dataclass(frozen=True, slots=True)
class LuckInteractionGraph:
    """DI-10 interaction graph. Distinct from DomainGraph and ActivationGraph."""

    nodes: tuple[str, ...] = ()
    edges: tuple[LuckInteractionGraphEdge, ...] = ()

    @classmethod
    def from_dict(cls, data: Mapping[str, Any] | None) -> LuckInteractionGraph:
        """Rebuild the interaction graph."""
        payload = data or {}
        raw = payload.get("edges") or ()
        return cls(
            nodes=as_str_tuple(payload.get("nodes")),
            edges=tuple(
                LuckInteractionGraphEdge.from_dict(item if isinstance(item, Mapping) else None)
                for item in raw
            ),
        )


@dataclass(frozen=True, slots=True)
class InteractionPriority:
    """Window interaction ranking. Does not replace natal Evidence Priority."""

    highest_interaction: str = ""
    highest_conflict: str = ""
    highest_opportunity: str = ""
    highest_trade_off: str = ""
    highest_stress: str = ""
    highest_recovery: str = ""

    @classmethod
    def from_dict(cls, data: Mapping[str, Any] | None) -> InteractionPriority:
        """Rebuild interaction priority pointers."""
        payload = data or {}
        return cls(
            highest_interaction=as_str(payload.get("highest_interaction")),
            highest_conflict=as_str(payload.get("highest_conflict")),
            highest_opportunity=as_str(payload.get("highest_opportunity")),
            highest_trade_off=as_str(payload.get("highest_trade_off")),
            highest_stress=as_str(payload.get("highest_stress")),
            highest_recovery=as_str(payload.get("highest_recovery")),
        )


@dataclass(frozen=True, slots=True)
class LifeSituationResult:
    """Temporary luck-window interaction summary. Not fate and not a natal state."""

    situation_id: str = "unresolved"
    situation_state: str = "unresolved"
    primary_domain_ids: tuple[str, ...] = ()
    cost_domain_ids: tuple[str, ...] = ()
    summary_keys: tuple[str, ...] = ()
    supporting_finding_ids: tuple[str, ...] = ()
    confidence: ConfidenceValue = field(default_factory=ConfidenceValue)
    temporality: str = "window_bound"
    trace_ids: tuple[str, ...] = ()

    @classmethod
    def from_dict(cls, data: Mapping[str, Any] | None) -> LifeSituationResult:
        """Rebuild life situation."""
        payload = data or {}
        situation = as_str(payload.get("situation_id") or payload.get("situation_state"), "unresolved")
        return cls(
            situation_id=situation or "unresolved",
            situation_state=as_str(payload.get("situation_state"), situation) or situation or "unresolved",
            primary_domain_ids=as_str_tuple(payload.get("primary_domain_ids")),
            cost_domain_ids=as_str_tuple(payload.get("cost_domain_ids")),
            summary_keys=as_str_tuple(payload.get("summary_keys")),
            supporting_finding_ids=as_str_tuple(payload.get("supporting_finding_ids")),
            confidence=ConfidenceValue.from_dict(payload.get("confidence")),
            temporality=as_str(payload.get("temporality"), "window_bound") or "window_bound",
            trace_ids=as_str_tuple(payload.get("trace_ids")),
        )
