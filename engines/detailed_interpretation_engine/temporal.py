"""Pack 07 temporal result shells. Natal objects stay outside this module."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping

from engines.detailed_interpretation_engine.codec import as_enum, as_str, as_str_tuple
from engines.detailed_interpretation_engine.constants import (
    LUCK_ACTIVATION_RULESET_VERSION,
    LUCK_INTERACTION_RULESET_VERSION,
    SCHEMA_LUCK_ACTIVATION,
    SCHEMA_LUCK_INTERACTION,
    SCHEMA_TEMPORAL,
)
from engines.detailed_interpretation_engine.enums import EvaluationStatus
from engines.detailed_interpretation_engine.luck_activation.models import (
    ActivationGraph,
    DomainActivationResult,
)
from engines.detailed_interpretation_engine.luck_interaction.models import (
    DomainInteractionFinding,
    InteractionPriority,
    LifeSituationResult,
    LuckInteractionGraph,
    ResourceShift,
    StressTransfer,
)
from engines.detailed_interpretation_engine.value_objects import ConfidenceValue


@dataclass(frozen=True, slots=True)
class LuckActivationResult:
    """DI-09 luck activation. Does not rewrite natal state."""

    schema_version: str = SCHEMA_LUCK_ACTIVATION
    ruleset_version: str = LUCK_ACTIVATION_RULESET_VERSION
    status: EvaluationStatus = EvaluationStatus.NOT_EVALUATED
    analysis_id: str = ""
    cycle_kind: str = "dai_van"
    cycle_id: str = ""
    luck_cycle_id: str = ""
    time_window: str = ""
    domain_activation_ids: tuple[str, ...] = ()
    order: tuple[str, ...] = ()
    items: dict[str, DomainActivationResult] = field(default_factory=dict)
    graph: ActivationGraph = field(default_factory=ActivationGraph)
    dominant_activation: str = ""
    dominant_suppression: str = ""
    stress_domains: tuple[str, ...] = ()
    recovery_domains: tuple[str, ...] = ()
    evidence_ids: tuple[str, ...] = ()
    confidence: ConfidenceValue = field(default_factory=ConfidenceValue)
    trace_ids: tuple[str, ...] = ()
    warnings: tuple[str, ...] = ()
    temporal_ten_god: str = ""
    temporal_stem: str = ""
    temporal_branch: str = ""

    @property
    def state(self) -> EvaluationStatus:
        """Ticket alias for evaluation status."""
        return self.status

    @property
    def domain_results(self) -> dict[str, DomainActivationResult]:
        """Ticket alias for per-domain activations."""
        return self.items

    @classmethod
    def from_dict(cls, data: Mapping[str, Any] | None) -> LuckActivationResult:
        """Rebuild luck activation from a mapping."""
        payload = data or {}
        items_raw = payload.get("items") or payload.get("domain_results")
        items: dict[str, DomainActivationResult] = {}
        if isinstance(items_raw, Mapping):
            for key, item in items_raw.items():
                if isinstance(item, Mapping):
                    items[str(key)] = DomainActivationResult.from_dict(item, str(key))
        graph_raw = payload.get("graph")
        cycle_id = as_str(payload.get("cycle_id") or payload.get("luck_cycle_id"))
        return cls(
            schema_version=as_str(payload.get("schema_version"), SCHEMA_LUCK_ACTIVATION),
            ruleset_version=as_str(
                payload.get("ruleset_version"),
                LUCK_ACTIVATION_RULESET_VERSION,
            ),
            status=as_enum(
                EvaluationStatus,
                payload.get("status") or payload.get("state"),
                EvaluationStatus.NOT_EVALUATED,
            ),
            analysis_id=as_str(payload.get("analysis_id")),
            cycle_kind=as_str(payload.get("cycle_kind"), "dai_van") or "dai_van",
            cycle_id=cycle_id,
            luck_cycle_id=as_str(payload.get("luck_cycle_id"), cycle_id) or cycle_id,
            time_window=as_str(payload.get("time_window")),
            domain_activation_ids=as_str_tuple(
                payload.get("domain_activation_ids") or payload.get("order")
            ),
            order=as_str_tuple(payload.get("order") or payload.get("domain_activation_ids")),
            items=items,
            graph=ActivationGraph.from_dict(graph_raw if isinstance(graph_raw, Mapping) else None),
            dominant_activation=as_str(payload.get("dominant_activation")),
            dominant_suppression=as_str(payload.get("dominant_suppression")),
            stress_domains=as_str_tuple(payload.get("stress_domains")),
            recovery_domains=as_str_tuple(payload.get("recovery_domains")),
            evidence_ids=as_str_tuple(payload.get("evidence_ids")),
            confidence=ConfidenceValue.from_dict(payload.get("confidence")),
            trace_ids=as_str_tuple(payload.get("trace_ids")),
            warnings=as_str_tuple(payload.get("warnings")),
            temporal_ten_god=as_str(payload.get("temporal_ten_god")),
            temporal_stem=as_str(payload.get("temporal_stem")),
            temporal_branch=as_str(payload.get("temporal_branch")),
        )


@dataclass(frozen=True, slots=True)
class LuckInteractionResult:
    """DI-10 luck interaction. Window-bound, not fate and not natal rewrite."""

    schema_version: str = SCHEMA_LUCK_INTERACTION
    ruleset_version: str = LUCK_INTERACTION_RULESET_VERSION
    status: EvaluationStatus = EvaluationStatus.NOT_EVALUATED
    analysis_id: str = ""
    cycle_kind: str = "dai_van"
    cycle_id: str = ""
    time_window: str = ""
    findings: tuple[DomainInteractionFinding, ...] = ()
    finding_ids: tuple[str, ...] = ()
    graph: LuckInteractionGraph = field(default_factory=LuckInteractionGraph)
    priority: InteractionPriority = field(default_factory=InteractionPriority)
    life_situation: LifeSituationResult = field(default_factory=LifeSituationResult)
    interaction_driver: str = "not_applicable"
    interaction_bottleneck: str = "not_applicable"
    opportunity: str = ""
    risk: str = ""
    conditions: tuple[str, ...] = ()
    evidence_ids: tuple[str, ...] = ()
    confidence: ConfidenceValue = field(default_factory=ConfidenceValue)
    warnings: tuple[str, ...] = ()
    trace: tuple[str, ...] = ()
    trace_ids: tuple[str, ...] = ()
    resource_shifts: tuple[ResourceShift, ...] = ()
    stress_transfers: tuple[StressTransfer, ...] = ()

    @classmethod
    def from_dict(cls, data: Mapping[str, Any] | None) -> LuckInteractionResult:
        """Rebuild luck interaction from a mapping."""
        payload = data or {}
        raw_findings = payload.get("findings") or ()
        findings = tuple(
            DomainInteractionFinding.from_dict(item if isinstance(item, Mapping) else None)
            for item in raw_findings
        )
        ids = as_str_tuple(payload.get("finding_ids")) or tuple(item.finding_id for item in findings)
        traces = as_str_tuple(payload.get("trace_ids") or payload.get("trace"))
        graph_raw = payload.get("graph")
        shifts_raw = payload.get("resource_shifts") or ()
        transfers_raw = payload.get("stress_transfers") or ()
        return cls(
            schema_version=as_str(payload.get("schema_version"), SCHEMA_LUCK_INTERACTION),
            ruleset_version=as_str(
                payload.get("ruleset_version"),
                LUCK_INTERACTION_RULESET_VERSION,
            ),
            status=as_enum(
                EvaluationStatus,
                payload.get("status"),
                EvaluationStatus.NOT_EVALUATED,
            ),
            analysis_id=as_str(payload.get("analysis_id")),
            cycle_kind=as_str(payload.get("cycle_kind"), "dai_van") or "dai_van",
            cycle_id=as_str(payload.get("cycle_id")),
            time_window=as_str(payload.get("time_window")),
            findings=findings,
            finding_ids=ids,
            graph=LuckInteractionGraph.from_dict(graph_raw if isinstance(graph_raw, Mapping) else None),
            priority=InteractionPriority.from_dict(payload.get("priority")),
            life_situation=LifeSituationResult.from_dict(payload.get("life_situation")),
            interaction_driver=as_str(payload.get("interaction_driver"), "not_applicable")
            or "not_applicable",
            interaction_bottleneck=as_str(payload.get("interaction_bottleneck"), "not_applicable")
            or "not_applicable",
            opportunity=as_str(payload.get("opportunity")),
            risk=as_str(payload.get("risk")),
            conditions=as_str_tuple(payload.get("conditions")),
            evidence_ids=as_str_tuple(payload.get("evidence_ids")),
            confidence=ConfidenceValue.from_dict(payload.get("confidence")),
            warnings=as_str_tuple(payload.get("warnings")),
            trace=traces,
            trace_ids=traces,
            resource_shifts=tuple(
                ResourceShift.from_dict(item if isinstance(item, Mapping) else None)
                for item in shifts_raw
            ),
            stress_transfers=tuple(
                StressTransfer.from_dict(item if isinstance(item, Mapping) else None)
                for item in transfers_raw
            ),
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
