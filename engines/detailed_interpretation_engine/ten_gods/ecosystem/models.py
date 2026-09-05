"""Ten Gods ecosystem result models. Structured assignments only."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping

from engines.detailed_interpretation_engine.codec import as_enum, as_str, as_str_tuple
from engines.detailed_interpretation_engine.constants import (
    SCHEMA_TEN_GODS_BALANCE,
    TEN_GODS_BALANCE_RULESET_VERSION,
)
from engines.detailed_interpretation_engine.enums import (
    EcosystemRole,
    EcosystemState,
    EvaluationStatus,
    FlowQuality,
)
from engines.detailed_interpretation_engine.value_objects import ConfidenceValue


@dataclass(frozen=True, slots=True)
class EcosystemRoleAssignment:
    """One ecosystem role assignment. Subject may be a deity or a family."""

    subject: str = ""
    subject_kind: str = "ten_god"
    role: EcosystemRole = EcosystemRole.UNRESOLVED
    state: EvaluationStatus = EvaluationStatus.NOT_APPLICABLE
    basis: tuple[str, ...] = ()
    source_chain_ids: tuple[str, ...] = ()
    support_ids: tuple[str, ...] = ()
    damage_ids: tuple[str, ...] = ()
    rescue_ids: tuple[str, ...] = ()
    evidence_ids: tuple[str, ...] = ()
    confidence: ConfidenceValue = field(default_factory=ConfidenceValue)

    @classmethod
    def from_dict(cls, data: Mapping[str, Any] | None) -> EcosystemRoleAssignment:
        """Rebuild one role assignment."""
        payload = data or {}
        return cls(
            subject=as_str(payload.get("subject")),
            subject_kind=as_str(payload.get("subject_kind"), "ten_god"),
            role=as_enum(EcosystemRole, payload.get("role"), EcosystemRole.UNRESOLVED),
            state=as_enum(EvaluationStatus, payload.get("state"), EvaluationStatus.NOT_APPLICABLE),
            basis=as_str_tuple(payload.get("basis")),
            source_chain_ids=as_str_tuple(payload.get("source_chain_ids")),
            support_ids=as_str_tuple(payload.get("support_ids")),
            damage_ids=as_str_tuple(payload.get("damage_ids")),
            rescue_ids=as_str_tuple(payload.get("rescue_ids")),
            evidence_ids=as_str_tuple(payload.get("evidence_ids")),
            confidence=ConfidenceValue.from_dict(payload.get("confidence")),
        )


@dataclass(frozen=True, slots=True)
class FamilyBalance:
    """Five-family structural contribution. Not occurrence count."""

    family_id: str = ""
    state: str = "unresolved"
    dominance: str = "unresolved"
    notes_key: str = ""
    evidence_ids: tuple[str, ...] = ()
    confidence: ConfidenceValue = field(default_factory=ConfidenceValue)

    @classmethod
    def from_dict(cls, data: Mapping[str, Any] | None) -> FamilyBalance:
        """Rebuild one family balance."""
        payload = data or {}
        return cls(
            family_id=as_str(payload.get("family_id")),
            state=as_str(payload.get("state"), "unresolved"),
            dominance=as_str(payload.get("dominance"), "unresolved"),
            notes_key=as_str(payload.get("notes_key")),
            evidence_ids=as_str_tuple(payload.get("evidence_ids")),
            confidence=ConfidenceValue.from_dict(payload.get("confidence")),
        )


@dataclass(frozen=True, slots=True)
class EcosystemFlow:
    """Directed family flow built only from active combination links."""

    flow_id: str = ""
    nodes: tuple[str, ...] = ()
    source_chain_ids: tuple[str, ...] = ()
    quality: FlowQuality = FlowQuality.UNRESOLVED

    @classmethod
    def from_dict(cls, data: Mapping[str, Any] | None) -> EcosystemFlow:
        """Rebuild one flow."""
        payload = data or {}
        return cls(
            flow_id=as_str(payload.get("flow_id")),
            nodes=as_str_tuple(payload.get("nodes")),
            source_chain_ids=as_str_tuple(payload.get("source_chain_ids")),
            quality=as_enum(FlowQuality, payload.get("quality"), FlowQuality.UNRESOLVED),
        )


def _assignment(data: Any) -> EcosystemRoleAssignment:
    return EcosystemRoleAssignment.from_dict(data if isinstance(data, Mapping) else None)


@dataclass(frozen=True, slots=True)
class TenGodEcosystemResult:
    """Natal Ten Gods ecosystem. Not a second Grade or Damage engine."""

    analysis_id: str = ""
    state: EvaluationStatus = EvaluationStatus.NOT_EVALUATED
    driver: EcosystemRoleAssignment = field(default_factory=EcosystemRoleAssignment)
    support: EcosystemRoleAssignment = field(default_factory=EcosystemRoleAssignment)
    suppressed: EcosystemRoleAssignment = field(default_factory=EcosystemRoleAssignment)
    blocked: EcosystemRoleAssignment = field(default_factory=EcosystemRoleAssignment)
    excessive: EcosystemRoleAssignment = field(default_factory=EcosystemRoleAssignment)
    deficient: EcosystemRoleAssignment = field(default_factory=EcosystemRoleAssignment)
    missing: EcosystemRoleAssignment = field(default_factory=EcosystemRoleAssignment)
    bottleneck: EcosystemRoleAssignment = field(default_factory=EcosystemRoleAssignment)
    balancer: EcosystemRoleAssignment = field(default_factory=EcosystemRoleAssignment)
    neutral: tuple[EcosystemRoleAssignment, ...] = ()
    family_balances: tuple[FamilyBalance, ...] = ()
    flow: tuple[EcosystemFlow, ...] = ()
    flow_quality: FlowQuality = FlowQuality.UNRESOLVED
    ecosystem_state: EcosystemState = EcosystemState.UNRESOLVED
    evidence_ids: tuple[str, ...] = ()
    trace_ids: tuple[str, ...] = ()
    confidence: ConfidenceValue = field(default_factory=ConfidenceValue)
    schema_version: str = SCHEMA_TEN_GODS_BALANCE
    ruleset_version: str = TEN_GODS_BALANCE_RULESET_VERSION

    @classmethod
    def from_dict(cls, data: Mapping[str, Any] | None) -> TenGodEcosystemResult:
        """Rebuild an ecosystem result."""
        payload = data or {}
        flow_raw = payload.get("flow") or ()
        family_raw = payload.get("family_balances") or ()
        neutral_raw = payload.get("neutral") or ()
        return cls(
            analysis_id=as_str(payload.get("analysis_id")),
            state=as_enum(EvaluationStatus, payload.get("state"), EvaluationStatus.NOT_EVALUATED),
            driver=_assignment(payload.get("driver")),
            support=_assignment(payload.get("support")),
            suppressed=_assignment(payload.get("suppressed")),
            blocked=_assignment(payload.get("blocked")),
            excessive=_assignment(payload.get("excessive")),
            deficient=_assignment(payload.get("deficient")),
            missing=_assignment(payload.get("missing")),
            bottleneck=_assignment(payload.get("bottleneck")),
            balancer=_assignment(payload.get("balancer")),
            neutral=tuple(_assignment(item) for item in neutral_raw),
            family_balances=tuple(
                FamilyBalance.from_dict(item if isinstance(item, Mapping) else None)
                for item in family_raw
            ),
            flow=tuple(
                EcosystemFlow.from_dict(item if isinstance(item, Mapping) else None)
                for item in flow_raw
            ),
            flow_quality=as_enum(FlowQuality, payload.get("flow_quality"), FlowQuality.UNRESOLVED),
            ecosystem_state=as_enum(
                EcosystemState, payload.get("ecosystem_state"), EcosystemState.UNRESOLVED
            ),
            evidence_ids=as_str_tuple(payload.get("evidence_ids")),
            trace_ids=as_str_tuple(payload.get("trace_ids")),
            confidence=ConfidenceValue.from_dict(payload.get("confidence")),
            schema_version=as_str(payload.get("schema_version"), SCHEMA_TEN_GODS_BALANCE),
            ruleset_version=as_str(payload.get("ruleset_version"), TEN_GODS_BALANCE_RULESET_VERSION),
        )
