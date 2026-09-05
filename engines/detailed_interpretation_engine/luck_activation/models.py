"""Domain activation objects. Natal DomainResult stays on CanonicalRuntimeResult.domains."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping

from engines.detailed_interpretation_engine.codec import as_enum, as_str, as_str_tuple
from engines.detailed_interpretation_engine.enums import ActivationState
from engines.detailed_interpretation_engine.value_objects import ConfidenceValue

ACTIVATION_GRAPH_RELATIONS: frozenset[str] = frozenset(
    {"activate", "suppress", "stress", "recover", "accelerate", "delay"}
)


@dataclass(frozen=True, slots=True)
class DomainActivationResult:
    """One domain's luck-window expression. Does not rewrite natal capability."""

    domain_id: str = ""
    natal_state: str = ""
    natal_driver_id: str = ""
    natal_driver: str = ""
    natal_bottleneck: str = ""
    activation_state: ActivationState = ActivationState.UNRESOLVED
    activation_types: tuple[str, ...] = ()
    activation_driver: str = ""
    activation_driver_id: str = ""
    activation_bottleneck: str = ""
    support: str = "none"
    stress: str = "none"
    conditions: tuple[str, ...] = ()
    warnings: tuple[str, ...] = ()
    confidence: ConfidenceValue = field(default_factory=ConfidenceValue)
    evidence_ids: tuple[str, ...] = ()
    trace_ids: tuple[str, ...] = ()

    @classmethod
    def from_dict(cls, data: Mapping[str, Any] | None, default_id: str = "") -> DomainActivationResult:
        """Rebuild one domain activation."""
        payload = data or {}
        return cls(
            domain_id=as_str(payload.get("domain_id"), default_id) or default_id,
            natal_state=as_str(payload.get("natal_state")),
            natal_driver_id=as_str(payload.get("natal_driver_id")),
            natal_driver=as_str(payload.get("natal_driver")),
            natal_bottleneck=as_str(payload.get("natal_bottleneck")),
            activation_state=as_enum(
                ActivationState,
                payload.get("activation_state"),
                ActivationState.UNRESOLVED,
            ),
            activation_types=as_str_tuple(payload.get("activation_types")),
            activation_driver=as_str(payload.get("activation_driver")),
            activation_driver_id=as_str(payload.get("activation_driver_id")),
            activation_bottleneck=as_str(payload.get("activation_bottleneck")),
            support=as_str(payload.get("support"), "none") or "none",
            stress=as_str(payload.get("stress"), "none") or "none",
            conditions=as_str_tuple(payload.get("conditions")),
            warnings=as_str_tuple(payload.get("warnings")),
            confidence=ConfidenceValue.from_dict(payload.get("confidence")),
            evidence_ids=as_str_tuple(payload.get("evidence_ids")),
            trace_ids=as_str_tuple(payload.get("trace_ids")),
        )


@dataclass(frozen=True, slots=True)
class ActivationGraphEdge:
    """Luck force → domain. Not a domain-to-domain interaction edge."""

    source: str = "luck_cycle"
    target: str = ""
    relation: str = ""
    evidence_ids: tuple[str, ...] = ()

    @classmethod
    def from_dict(cls, data: Mapping[str, Any] | None) -> ActivationGraphEdge:
        """Rebuild one activation edge."""
        payload = data or {}
        return cls(
            source=as_str(payload.get("source"), "luck_cycle") or "luck_cycle",
            target=as_str(payload.get("target")),
            relation=as_str(payload.get("relation")),
            evidence_ids=as_str_tuple(payload.get("evidence_ids")),
        )


@dataclass(frozen=True, slots=True)
class ActivationGraph:
    """DI-09 activation graph. Luck Interaction (DI-10) is a different object."""

    nodes: tuple[str, ...] = ()
    edges: tuple[ActivationGraphEdge, ...] = ()

    @classmethod
    def from_dict(cls, data: Mapping[str, Any] | None) -> ActivationGraph:
        """Rebuild the activation graph."""
        payload = data or {}
        raw = payload.get("edges") or ()
        return cls(
            nodes=as_str_tuple(payload.get("nodes")),
            edges=tuple(
                ActivationGraphEdge.from_dict(item if isinstance(item, Mapping) else None)
                for item in raw
            ),
        )
