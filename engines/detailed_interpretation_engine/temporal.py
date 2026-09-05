"""Pack 07 temporal result shells. Natal objects stay outside this module."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping

from engines.detailed_interpretation_engine.codec import as_enum, as_str, as_str_tuple
from engines.detailed_interpretation_engine.constants import (
    SCHEMA_LUCK_ACTIVATION,
    SCHEMA_LUCK_INTERACTION,
    SCHEMA_TEMPORAL,
)
from engines.detailed_interpretation_engine.enums import EvaluationStatus
from engines.detailed_interpretation_engine.value_objects import ConfidenceValue


@dataclass(frozen=True, slots=True)
class LuckActivationResult:
    """DI-09 luck activation shell. Does not rewrite natal state."""

    schema_version: str = SCHEMA_LUCK_ACTIVATION
    status: EvaluationStatus = EvaluationStatus.NOT_EVALUATED
    cycle_kind: str = ""
    cycle_id: str = ""
    domain_activation_ids: tuple[str, ...] = ()
    confidence: ConfidenceValue = field(default_factory=ConfidenceValue)
    trace_ids: tuple[str, ...] = ()
    warnings: tuple[str, ...] = ()

    @classmethod
    def from_dict(cls, data: Mapping[str, Any] | None) -> LuckActivationResult:
        """Rebuild luck activation from a mapping."""
        payload = data or {}
        return cls(
            schema_version=as_str(payload.get("schema_version"), SCHEMA_LUCK_ACTIVATION),
            status=as_enum(
                EvaluationStatus,
                payload.get("status"),
                EvaluationStatus.NOT_EVALUATED,
            ),
            cycle_kind=as_str(payload.get("cycle_kind")),
            cycle_id=as_str(payload.get("cycle_id")),
            domain_activation_ids=as_str_tuple(payload.get("domain_activation_ids")),
            confidence=ConfidenceValue.from_dict(payload.get("confidence")),
            trace_ids=as_str_tuple(payload.get("trace_ids")),
            warnings=as_str_tuple(payload.get("warnings")),
        )


@dataclass(frozen=True, slots=True)
class LuckInteractionResult:
    """DI-10 luck interaction shell. Window-bound, not fate."""

    schema_version: str = SCHEMA_LUCK_INTERACTION
    status: EvaluationStatus = EvaluationStatus.NOT_EVALUATED
    cycle_kind: str = ""
    cycle_id: str = ""
    finding_ids: tuple[str, ...] = ()
    confidence: ConfidenceValue = field(default_factory=ConfidenceValue)
    warnings: tuple[str, ...] = ()
    trace: tuple[str, ...] = ()

    @classmethod
    def from_dict(cls, data: Mapping[str, Any] | None) -> LuckInteractionResult:
        """Rebuild luck interaction from a mapping."""
        payload = data or {}
        return cls(
            schema_version=as_str(payload.get("schema_version"), SCHEMA_LUCK_INTERACTION),
            status=as_enum(
                EvaluationStatus,
                payload.get("status"),
                EvaluationStatus.NOT_EVALUATED,
            ),
            cycle_kind=as_str(payload.get("cycle_kind")),
            cycle_id=as_str(payload.get("cycle_id")),
            finding_ids=as_str_tuple(payload.get("finding_ids")),
            confidence=ConfidenceValue.from_dict(payload.get("confidence")),
            warnings=as_str_tuple(payload.get("warnings")),
            trace=as_str_tuple(payload.get("trace")),
        )


@dataclass(frozen=True, slots=True)
class TemporalActivationResult:
    """DI-11 temporal activation shell. Specificity is not dominance."""

    schema_version: str = SCHEMA_TEMPORAL
    ruleset_version: str = ""
    state: EvaluationStatus = EvaluationStatus.NOT_EVALUATED
    requested_layers: tuple[str, ...] = ()
    evaluated_layers: tuple[str, ...] = ()
    time_window: str = ""
    active_layer: str = ""
    parent_layer: str = ""
    layer_results: dict[str, str] = field(default_factory=dict)
    domain_results: dict[str, str] = field(default_factory=dict)
    conditions: tuple[str, ...] = ()
    warnings: tuple[str, ...] = ()
    confidence: ConfidenceValue = field(default_factory=ConfidenceValue)
    evidence_ids: tuple[str, ...] = ()
    trace_ids: tuple[str, ...] = ()

    @classmethod
    def from_dict(cls, data: Mapping[str, Any] | None) -> TemporalActivationResult:
        """Rebuild temporal activation from a mapping."""
        payload = data or {}
        layer_raw = payload.get("layer_results")
        domain_raw = payload.get("domain_results")
        layer_results = (
            {str(key): str(item) for key, item in layer_raw.items()}
            if isinstance(layer_raw, Mapping)
            else {}
        )
        domain_results = (
            {str(key): str(item) for key, item in domain_raw.items()}
            if isinstance(domain_raw, Mapping)
            else {}
        )
        return cls(
            schema_version=as_str(payload.get("schema_version"), SCHEMA_TEMPORAL),
            ruleset_version=as_str(payload.get("ruleset_version")),
            state=as_enum(
                EvaluationStatus,
                payload.get("state") or payload.get("status"),
                EvaluationStatus.NOT_EVALUATED,
            ),
            requested_layers=as_str_tuple(payload.get("requested_layers")),
            evaluated_layers=as_str_tuple(payload.get("evaluated_layers")),
            time_window=as_str(payload.get("time_window")),
            active_layer=as_str(payload.get("active_layer")),
            parent_layer=as_str(payload.get("parent_layer")),
            layer_results=layer_results,
            domain_results=domain_results,
            conditions=as_str_tuple(payload.get("conditions")),
            warnings=as_str_tuple(payload.get("warnings")),
            confidence=ConfidenceValue.from_dict(payload.get("confidence")),
            evidence_ids=as_str_tuple(payload.get("evidence_ids")),
            trace_ids=as_str_tuple(payload.get("trace_ids")),
        )


@dataclass(frozen=True, slots=True)
class TemporalSection:
    """Published temporal layer of CanonicalRuntimeResult."""

    luck_activation: LuckActivationResult = field(default_factory=LuckActivationResult)
    luck_interaction: LuckInteractionResult = field(default_factory=LuckInteractionResult)
    temporal_activation: TemporalActivationResult = field(default_factory=TemporalActivationResult)
    requested_layers: tuple[str, ...] = ()
    time_windows: dict[str, str] = field(default_factory=dict)
    status: EvaluationStatus = EvaluationStatus.NOT_EVALUATED

    @classmethod
    def from_dict(cls, data: Mapping[str, Any] | None) -> TemporalSection:
        """Rebuild the temporal section."""
        payload = data or {}
        windows_raw = payload.get("time_windows")
        windows = (
            {str(key): str(item) for key, item in windows_raw.items()}
            if isinstance(windows_raw, Mapping)
            else {}
        )
        return cls(
            luck_activation=LuckActivationResult.from_dict(
                payload.get("luck_activation")
                if isinstance(payload.get("luck_activation"), Mapping)
                else None
            ),
            luck_interaction=LuckInteractionResult.from_dict(
                payload.get("luck_interaction")
                if isinstance(payload.get("luck_interaction"), Mapping)
                else None
            ),
            temporal_activation=TemporalActivationResult.from_dict(
                payload.get("temporal_activation")
                if isinstance(payload.get("temporal_activation"), Mapping)
                else None
            ),
            requested_layers=as_str_tuple(payload.get("requested_layers")),
            time_windows=windows,
            status=as_enum(
                EvaluationStatus,
                payload.get("status"),
                EvaluationStatus.NOT_EVALUATED,
            ),
        )
