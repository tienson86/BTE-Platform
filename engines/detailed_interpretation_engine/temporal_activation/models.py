"""Temporal Activation objects. Natal, luck, and interaction stay on their own results."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping

from engines.detailed_interpretation_engine.codec import as_enum, as_str, as_str_tuple
from engines.detailed_interpretation_engine.enums import EvaluationStatus
from engines.detailed_interpretation_engine.value_objects import ConfidenceValue


@dataclass(frozen=True, slots=True)
class TemporalActor:
    """Annual (or layer) actor. Never appended into natal Ten Gods or Five Elements."""

    actor_kind: str = ""
    actor_id: str = ""
    label: str = ""
    role: str = "annual"
    action: str = ""

    @classmethod
    def from_dict(cls, data: Mapping[str, Any] | None) -> TemporalActor:
        """Rebuild one temporal actor."""
        payload = data or {}
        return cls(
            actor_kind=as_str(payload.get("actor_kind")),
            actor_id=as_str(payload.get("actor_id")),
            label=as_str(payload.get("label")),
            role=as_str(payload.get("role"), "annual") or "annual",
            action=as_str(payload.get("action")),
        )


@dataclass(frozen=True, slots=True)
class TemporalActivationModifier:
    """Layer-local modifier. No good/bad flag and no event prediction."""

    domain_id: str = ""
    effect: str = "stabilize"
    source_layer: str = "annual"
    conditions: tuple[str, ...] = ()

    @classmethod
    def from_dict(cls, data: Mapping[str, Any] | None) -> TemporalActivationModifier:
        """Rebuild one annual modifier."""
        payload = data or {}
        return cls(
            domain_id=as_str(payload.get("domain_id")),
            effect=as_str(payload.get("effect"), "stabilize") or "stabilize",
            source_layer=as_str(payload.get("source_layer"), "annual") or "annual",
            conditions=as_str_tuple(payload.get("conditions")),
        )


@dataclass(frozen=True, slots=True)
class ActivationEnvelope:
    """Parent luck activation copied as the annual operating envelope."""

    domain_id: str = ""
    parent_layer: str = "luck_cycle"
    parent_state: str = ""
    child_layer: str = "annual"
    expression_state: str = ""

    @classmethod
    def from_dict(cls, data: Mapping[str, Any] | None) -> ActivationEnvelope:
        """Rebuild one activation envelope."""
        payload = data or {}
        return cls(
            domain_id=as_str(payload.get("domain_id")),
            parent_layer=as_str(payload.get("parent_layer"), "luck_cycle") or "luck_cycle",
            parent_state=as_str(payload.get("parent_state")),
            child_layer=as_str(payload.get("child_layer"), "annual") or "annual",
            expression_state=as_str(payload.get("expression_state")),
        )


@dataclass(frozen=True, slots=True)
class TemporalDomainActivationResult:
    """One domain's annual expression inside the luck envelope. Does not rewrite natal or luck."""

    domain_id: str = ""
    natal_state: str = ""
    luck_activation_state: str = ""
    annual_modifier: str = "stabilize"
    annual_expression_state: str = "unresolved"
    temporal_driver: str = "not_applicable"
    temporal_bottleneck: str = "none"
    support: str = "none"
    stress: str = "none"
    recovery: str = "none"
    conditions: tuple[str, ...] = ()
    confidence: ConfidenceValue = field(default_factory=ConfidenceValue)
    evidence_ids: tuple[str, ...] = ()
    trace_ids: tuple[str, ...] = ()
    envelope: ActivationEnvelope = field(default_factory=ActivationEnvelope)

    @property
    def parent_activation_state(self) -> str:
        """Spec alias for the luck-cycle envelope state."""
        return self.luck_activation_state

    @property
    def expression_state(self) -> str:
        """Spec alias for annual expression."""
        return self.annual_expression_state

    @classmethod
    def from_dict(
        cls,
        data: Mapping[str, Any] | None,
        default_id: str = "",
    ) -> TemporalDomainActivationResult:
        """Rebuild one annual domain result."""
        payload = data or {}
        domain_id = as_str(payload.get("domain_id"), default_id) or default_id
        envelope_raw = payload.get("envelope")
        luck_state = as_str(
            payload.get("luck_activation_state") or payload.get("parent_activation_state")
        )
        expression = as_str(
            payload.get("annual_expression_state") or payload.get("expression_state"),
            "unresolved",
        ) or "unresolved"
        return cls(
            domain_id=domain_id,
            natal_state=as_str(payload.get("natal_state")),
            luck_activation_state=luck_state,
            annual_modifier=as_str(
                payload.get("annual_modifier") or payload.get("current_modifier"),
                "stabilize",
            )
            or "stabilize",
            annual_expression_state=expression,
            temporal_driver=as_str(
                payload.get("temporal_driver") or payload.get("driver"),
                "not_applicable",
            )
            or "not_applicable",
            temporal_bottleneck=as_str(
                payload.get("temporal_bottleneck") or payload.get("bottleneck"),
                "none",
            )
            or "none",
            support=as_str(payload.get("support"), "none") or "none",
            stress=as_str(payload.get("stress"), "none") or "none",
            recovery=as_str(payload.get("recovery"), "none") or "none",
            conditions=as_str_tuple(payload.get("conditions")),
            confidence=ConfidenceValue.from_dict(payload.get("confidence")),
            evidence_ids=as_str_tuple(payload.get("evidence_ids")),
            trace_ids=as_str_tuple(payload.get("trace_ids")),
            envelope=ActivationEnvelope.from_dict(
                envelope_raw if isinstance(envelope_raw, Mapping) else None
            )
            if isinstance(envelope_raw, Mapping)
            else ActivationEnvelope(
                domain_id=domain_id,
                parent_state=luck_state,
                expression_state=expression,
            ),
        )


@dataclass(frozen=True, slots=True)
class TemporalLayerResult:
    """One temporal layer shell. Child refines parent; specificity is not dominance."""

    layer: str = ""
    time_window: str = ""
    parent_layer: str = ""
    temporal_pillar: str = ""
    temporal_actors: tuple[TemporalActor, ...] = ()
    modifiers: tuple[TemporalActivationModifier, ...] = ()
    domain_activation: dict[str, TemporalDomainActivationResult] = field(default_factory=dict)
    confidence: ConfidenceValue = field(default_factory=ConfidenceValue)
    evidence_ids: tuple[str, ...] = ()
    trace_ids: tuple[str, ...] = ()
    state: EvaluationStatus = EvaluationStatus.NOT_EVALUATED
    source_identity: str = ""

    @classmethod
    def from_dict(
        cls,
        data: Mapping[str, Any] | None,
        default_layer: str = "",
    ) -> TemporalLayerResult:
        """Rebuild one layer result. String shells stay not_evaluated."""
        payload = data or {}
        domains_raw = payload.get("domain_activation")
        domains: dict[str, TemporalDomainActivationResult] = {}
        if isinstance(domains_raw, Mapping):
            for key, item in domains_raw.items():
                if isinstance(item, Mapping):
                    domains[str(key)] = TemporalDomainActivationResult.from_dict(item, str(key))
        actors_raw = payload.get("temporal_actors") or ()
        modifiers_raw = payload.get("modifiers") or ()
        return cls(
            layer=as_str(payload.get("layer"), default_layer) or default_layer,
            time_window=as_str(payload.get("time_window")),
            parent_layer=as_str(payload.get("parent_layer")),
            temporal_pillar=as_str(payload.get("temporal_pillar")),
            temporal_actors=tuple(
                TemporalActor.from_dict(item if isinstance(item, Mapping) else None)
                for item in actors_raw
            ),
            modifiers=tuple(
                TemporalActivationModifier.from_dict(item if isinstance(item, Mapping) else None)
                for item in modifiers_raw
            ),
            domain_activation=domains,
            confidence=ConfidenceValue.from_dict(payload.get("confidence")),
            evidence_ids=as_str_tuple(payload.get("evidence_ids")),
            trace_ids=as_str_tuple(payload.get("trace_ids")),
            state=as_enum(
                EvaluationStatus,
                payload.get("state") or payload.get("status"),
                EvaluationStatus.NOT_EVALUATED,
            ),
            source_identity=as_str(payload.get("source_identity")),
        )
