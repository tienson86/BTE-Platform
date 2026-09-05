"""Ten God combination result models. Structured codes only."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping

from engines.detailed_interpretation_engine.codec import as_enum, as_str, as_str_tuple
from engines.detailed_interpretation_engine.constants import (
    SCHEMA_TEN_GOD_COMBINATIONS,
    TEN_GOD_COMBINATIONS_RULESET_VERSION,
)
from engines.detailed_interpretation_engine.enums import (
    ChainQuality,
    CombinationReach,
    CombinationRelativePower,
    CombinationState,
    CombinationStructuralRole,
    DayMasterBand,
    EvaluationStatus,
    TenGodEffectiveStrength,
    TenGodRootState,
    TenGodStructuralRole,
    TenGodUsefulGodContext,
    TenGodVisibilitySummary,
)
from engines.detailed_interpretation_engine.value_objects import ConfidenceValue


@dataclass(frozen=True, slots=True)
class CombinationParticipant:
    """One concrete Ten God (or carrier) in a combination."""

    ten_god_id: str = ""
    role_in_combination: str = ""
    effective_strength: TenGodEffectiveStrength = TenGodEffectiveStrength.UNRESOLVED
    visibility: TenGodVisibilitySummary = TenGodVisibilitySummary.UNRESOLVED
    root_state: TenGodRootState = TenGodRootState.UNRESOLVED
    structural_role: TenGodStructuralRole = TenGodStructuralRole.UNRESOLVED

    @classmethod
    def from_dict(cls, data: Mapping[str, Any] | None) -> CombinationParticipant:
        """Rebuild one participant."""
        payload = data or {}
        return cls(
            ten_god_id=as_str(payload.get("ten_god_id")),
            role_in_combination=as_str(payload.get("role_in_combination")),
            effective_strength=as_enum(
                TenGodEffectiveStrength,
                payload.get("effective_strength"),
                TenGodEffectiveStrength.UNRESOLVED,
            ),
            visibility=as_enum(
                TenGodVisibilitySummary,
                payload.get("visibility"),
                TenGodVisibilitySummary.UNRESOLVED,
            ),
            root_state=as_enum(TenGodRootState, payload.get("root_state"), TenGodRootState.UNRESOLVED),
            structural_role=as_enum(
                TenGodStructuralRole,
                payload.get("structural_role"),
                TenGodStructuralRole.UNRESOLVED,
            ),
        )


@dataclass(frozen=True, slots=True)
class TenGodChainLink:
    """One directed link inside a chain. Preserve every link."""

    source: str = ""
    target: str = ""
    vector: str = ""
    reach: CombinationReach = CombinationReach.UNRESOLVED
    state: str = "unresolved"

    @classmethod
    def from_dict(cls, data: Mapping[str, Any] | None) -> TenGodChainLink:
        """Rebuild one chain link."""
        payload = data or {}
        return cls(
            source=as_str(payload.get("source")),
            target=as_str(payload.get("target")),
            vector=as_str(payload.get("vector")),
            reach=as_enum(CombinationReach, payload.get("reach"), CombinationReach.UNRESOLVED),
            state=as_str(payload.get("state"), "unresolved"),
        )


@dataclass(frozen=True, slots=True)
class TenGodChainFinding:
    """Structured A→B or A→B→C chain. Quality follows the weakest link."""

    chain_id: str = ""
    nodes: tuple[str, ...] = ()
    links: tuple[TenGodChainLink, ...] = ()
    quality: ChainQuality = ChainQuality.UNRESOLVED
    weakest_link: str = ""
    broken_link_ids: tuple[str, ...] = ()

    @classmethod
    def from_dict(cls, data: Mapping[str, Any] | None) -> TenGodChainFinding:
        """Rebuild a chain finding."""
        payload = data or {}
        links_raw = payload.get("links") or ()
        return cls(
            chain_id=as_str(payload.get("chain_id")),
            nodes=as_str_tuple(payload.get("nodes")),
            links=tuple(
                TenGodChainLink.from_dict(item if isinstance(item, Mapping) else None)
                for item in links_raw
            ),
            quality=as_enum(ChainQuality, payload.get("quality"), ChainQuality.UNRESOLVED),
            weakest_link=as_str(payload.get("weakest_link")),
            broken_link_ids=as_str_tuple(payload.get("broken_link_ids")),
        )


@dataclass(frozen=True, slots=True)
class TenGodCombinationResult:
    """One natal Ten God combination. No customer prose."""

    combination_id: str = ""
    combination_type: tuple[str, ...] = ()
    state: CombinationState = CombinationState.UNRESOLVED
    participants: tuple[CombinationParticipant, ...] = ()
    source: str = ""
    target: str = ""
    mediator: str = ""
    relationship: str = ""
    relative_power: CombinationRelativePower = CombinationRelativePower.UNCERTAIN
    chain: TenGodChainFinding = field(default_factory=TenGodChainFinding)
    chain_quality: ChainQuality = ChainQuality.UNRESOLVED
    structural_role: CombinationStructuralRole = CombinationStructuralRole.UNRESOLVED
    day_master_context: DayMasterBand = DayMasterBand.UNRESOLVED
    pattern_context: str = "unresolved"
    useful_god_context: TenGodUsefulGodContext = TenGodUsefulGodContext.UNRESOLVED
    support_ids: tuple[str, ...] = ()
    damage_ids: tuple[str, ...] = ()
    rescue_ids: tuple[str, ...] = ()
    domain_codes: tuple[str, ...] = ()
    positive_expressions: tuple[str, ...] = ()
    risk_expressions: tuple[str, ...] = ()
    conditions: tuple[str, ...] = ()
    causal_group: str = ""
    source_combination_id: str = ""
    source_chain_id: str = ""
    evidence_ids: tuple[str, ...] = ()
    trace_ids: tuple[str, ...] = ()
    confidence: ConfidenceValue = field(default_factory=ConfidenceValue)

    @classmethod
    def from_dict(cls, data: Mapping[str, Any] | None) -> TenGodCombinationResult:
        """Rebuild one combination result."""
        payload = data or {}
        participants_raw = payload.get("participants") or ()
        chain_raw = payload.get("chain")
        return cls(
            combination_id=as_str(payload.get("combination_id")),
            combination_type=as_str_tuple(payload.get("combination_type")),
            state=as_enum(CombinationState, payload.get("state"), CombinationState.UNRESOLVED),
            participants=tuple(
                CombinationParticipant.from_dict(item if isinstance(item, Mapping) else None)
                for item in participants_raw
            ),
            source=as_str(payload.get("source")),
            target=as_str(payload.get("target")),
            mediator=as_str(payload.get("mediator")),
            relationship=as_str(payload.get("relationship")),
            relative_power=as_enum(
                CombinationRelativePower,
                payload.get("relative_power"),
                CombinationRelativePower.UNCERTAIN,
            ),
            chain=TenGodChainFinding.from_dict(chain_raw if isinstance(chain_raw, Mapping) else None),
            chain_quality=as_enum(ChainQuality, payload.get("chain_quality"), ChainQuality.UNRESOLVED),
            structural_role=as_enum(
                CombinationStructuralRole,
                payload.get("structural_role"),
                CombinationStructuralRole.UNRESOLVED,
            ),
            day_master_context=as_enum(
                DayMasterBand, payload.get("day_master_context"), DayMasterBand.UNRESOLVED
            ),
            pattern_context=as_str(payload.get("pattern_context"), "unresolved"),
            useful_god_context=as_enum(
                TenGodUsefulGodContext,
                payload.get("useful_god_context"),
                TenGodUsefulGodContext.UNRESOLVED,
            ),
            support_ids=as_str_tuple(payload.get("support_ids")),
            damage_ids=as_str_tuple(payload.get("damage_ids")),
            rescue_ids=as_str_tuple(payload.get("rescue_ids")),
            domain_codes=as_str_tuple(payload.get("domain_codes")),
            positive_expressions=as_str_tuple(payload.get("positive_expressions")),
            risk_expressions=as_str_tuple(payload.get("risk_expressions")),
            conditions=as_str_tuple(payload.get("conditions")),
            causal_group=as_str(payload.get("causal_group")),
            source_combination_id=as_str(payload.get("source_combination_id")),
            source_chain_id=as_str(payload.get("source_chain_id")),
            evidence_ids=as_str_tuple(payload.get("evidence_ids")),
            trace_ids=as_str_tuple(payload.get("trace_ids")),
            confidence=ConfidenceValue.from_dict(payload.get("confidence")),
        )


@dataclass(frozen=True, slots=True)
class TenGodCombinationCollection:
    """All V1 combination evaluations for one analysis."""

    analysis_id: str = ""
    state: EvaluationStatus = EvaluationStatus.NOT_EVALUATED
    items: tuple[TenGodCombinationResult, ...] = ()
    evidence_ids: tuple[str, ...] = ()
    trace_ids: tuple[str, ...] = ()
    confidence: ConfidenceValue = field(default_factory=ConfidenceValue)
    schema_version: str = SCHEMA_TEN_GOD_COMBINATIONS
    ruleset_version: str = TEN_GOD_COMBINATIONS_RULESET_VERSION

    @classmethod
    def from_dict(cls, data: Mapping[str, Any] | None) -> TenGodCombinationCollection:
        """Rebuild a combination collection."""
        payload = data or {}
        items_raw = payload.get("items") or ()
        return cls(
            analysis_id=as_str(payload.get("analysis_id")),
            state=as_enum(EvaluationStatus, payload.get("state"), EvaluationStatus.NOT_EVALUATED),
            items=tuple(
                TenGodCombinationResult.from_dict(item if isinstance(item, Mapping) else None)
                for item in items_raw
            ),
            evidence_ids=as_str_tuple(payload.get("evidence_ids")),
            trace_ids=as_str_tuple(payload.get("trace_ids")),
            confidence=ConfidenceValue.from_dict(payload.get("confidence")),
            schema_version=as_str(payload.get("schema_version"), SCHEMA_TEN_GOD_COMBINATIONS),
            ruleset_version=as_str(
                payload.get("ruleset_version"), TEN_GOD_COMBINATIONS_RULESET_VERSION
            ),
        )
