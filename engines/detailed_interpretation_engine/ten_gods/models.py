"""Structured Ten God interpretation models. Codes only; no customer prose."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping

from engines.detailed_interpretation_engine.codec import as_enum, as_str, as_str_tuple
from engines.detailed_interpretation_engine.constants import (
    SCHEMA_TEN_GODS,
    TEN_GODS_RULESET_VERSION,
)
from engines.detailed_interpretation_engine.enums import (
    DayMasterBand,
    EvaluationStatus,
    TenGodConfidenceBand,
    TenGodEffectiveStrength,
    TenGodPresenceState,
    TenGodRootState,
    TenGodStructuralRole,
    TenGodUsability,
    TenGodUsefulGodContext,
    TenGodVisibilitySummary,
)
from engines.detailed_interpretation_engine.value_objects import ConfidenceValue


@dataclass(frozen=True, slots=True)
class TenGodOccurrence:
    """One unflattened upstream Ten God appearance."""

    pillar: str = ""
    layer: str = ""
    stem: str = ""
    branch: str = ""
    visible: bool = False
    evidence_id: str = ""

    @classmethod
    def from_dict(cls, data: Mapping[str, Any] | None) -> TenGodOccurrence:
        """Rebuild one occurrence."""
        payload = data or {}
        return cls(
            pillar=as_str(payload.get("pillar")),
            layer=as_str(payload.get("layer")),
            stem=as_str(payload.get("stem")),
            branch=as_str(payload.get("branch")),
            visible=bool(payload.get("visible")),
            evidence_id=as_str(payload.get("evidence_id")),
        )


@dataclass(frozen=True, slots=True)
class TenGodVisibilityInventory:
    """Per-location visibility. Do not collapse to a count."""

    year_stem: bool = False
    month_stem: bool = False
    day_context: bool = False
    hour_stem: bool = False
    branch_hidden: bool = False
    main_qi: bool = False
    middle_qi: bool = False
    residual_qi: bool = False
    summary: TenGodVisibilitySummary = TenGodVisibilitySummary.ABSENT
    hour_unknown: bool = False

    @classmethod
    def from_dict(cls, data: Mapping[str, Any] | None) -> TenGodVisibilityInventory:
        """Rebuild visibility inventory."""
        payload = data or {}
        return cls(
            year_stem=bool(payload.get("year_stem")),
            month_stem=bool(payload.get("month_stem")),
            day_context=bool(payload.get("day_context")),
            hour_stem=bool(payload.get("hour_stem")),
            branch_hidden=bool(payload.get("branch_hidden")),
            main_qi=bool(payload.get("main_qi")),
            middle_qi=bool(payload.get("middle_qi")),
            residual_qi=bool(payload.get("residual_qi")),
            summary=as_enum(
                TenGodVisibilitySummary,
                payload.get("summary"),
                TenGodVisibilitySummary.ABSENT,
            ),
            hour_unknown=bool(payload.get("hour_unknown")),
        )


@dataclass(frozen=True, slots=True)
class TenGodInterpretationResult:
    """Natal interpretation of one canonical Ten God."""

    ten_god_id: str = ""
    state: EvaluationStatus = EvaluationStatus.NOT_EVALUATED
    presence_state: TenGodPresenceState = TenGodPresenceState.UNRESOLVED
    occurrences: tuple[TenGodOccurrence, ...] = ()
    visibility: TenGodVisibilityInventory = field(default_factory=TenGodVisibilityInventory)
    root_state: TenGodRootState = TenGodRootState.UNRESOLVED
    effective_strength: TenGodEffectiveStrength = TenGodEffectiveStrength.UNRESOLVED
    structural_role: TenGodStructuralRole = TenGodStructuralRole.UNRESOLVED
    day_master_context: DayMasterBand = DayMasterBand.UNRESOLVED
    pattern_context: str = "unresolved"
    useful_god_context: TenGodUsefulGodContext = TenGodUsefulGodContext.UNRESOLVED
    structural_usability: TenGodUsability = TenGodUsability.UNRESOLVED
    positive_expressions: tuple[str, ...] = ()
    risk_expressions: tuple[str, ...] = ()
    conditions: tuple[str, ...] = ()
    evidence_ids: tuple[str, ...] = ()
    trace_ids: tuple[str, ...] = ()
    confidence: ConfidenceValue = field(default_factory=ConfidenceValue)
    damage_ids: tuple[str, ...] = ()
    rescue_ids: tuple[str, ...] = ()

    @classmethod
    def from_dict(cls, data: Mapping[str, Any] | None) -> TenGodInterpretationResult:
        """Rebuild one Ten God result."""
        payload = data or {}
        occurrences_raw = payload.get("occurrences") or ()
        confidence_raw = payload.get("confidence")
        visibility_raw = payload.get("visibility")
        return cls(
            ten_god_id=as_str(payload.get("ten_god_id")),
            state=as_enum(EvaluationStatus, payload.get("state"), EvaluationStatus.NOT_EVALUATED),
            presence_state=as_enum(
                TenGodPresenceState,
                payload.get("presence_state"),
                TenGodPresenceState.UNRESOLVED,
            ),
            occurrences=tuple(
                TenGodOccurrence.from_dict(item if isinstance(item, Mapping) else None)
                for item in occurrences_raw
            ),
            visibility=TenGodVisibilityInventory.from_dict(
                visibility_raw if isinstance(visibility_raw, Mapping) else None
            ),
            root_state=as_enum(
                TenGodRootState, payload.get("root_state"), TenGodRootState.UNRESOLVED
            ),
            effective_strength=as_enum(
                TenGodEffectiveStrength,
                payload.get("effective_strength"),
                TenGodEffectiveStrength.UNRESOLVED,
            ),
            structural_role=as_enum(
                TenGodStructuralRole,
                payload.get("structural_role"),
                TenGodStructuralRole.UNRESOLVED,
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
            structural_usability=as_enum(
                TenGodUsability,
                payload.get("structural_usability"),
                TenGodUsability.UNRESOLVED,
            ),
            positive_expressions=as_str_tuple(payload.get("positive_expressions")),
            risk_expressions=as_str_tuple(payload.get("risk_expressions")),
            conditions=as_str_tuple(payload.get("conditions")),
            evidence_ids=as_str_tuple(payload.get("evidence_ids")),
            trace_ids=as_str_tuple(payload.get("trace_ids")),
            confidence=ConfidenceValue.from_dict(confidence_raw),
            damage_ids=as_str_tuple(payload.get("damage_ids")),
            rescue_ids=as_str_tuple(payload.get("rescue_ids")),
        )


@dataclass(frozen=True, slots=True)
class TenGodInterpretationCollection:
    """All 10 natal Ten God results. Summary is structured, not a paragraph."""

    analysis_id: str = ""
    state: EvaluationStatus = EvaluationStatus.NOT_EVALUATED
    items: tuple[TenGodInterpretationResult, ...] = ()
    summary: tuple[str, ...] = ()
    evidence_ids: tuple[str, ...] = ()
    trace_ids: tuple[str, ...] = ()
    confidence: ConfidenceValue = field(default_factory=ConfidenceValue)
    schema_version: str = SCHEMA_TEN_GODS
    ruleset_version: str = TEN_GODS_RULESET_VERSION

    @classmethod
    def from_dict(cls, data: Mapping[str, Any] | None) -> TenGodInterpretationCollection:
        """Rebuild a Ten God collection."""
        payload = data or {}
        items_raw = payload.get("items") or ()
        confidence_raw = payload.get("confidence")
        return cls(
            analysis_id=as_str(payload.get("analysis_id")),
            state=as_enum(EvaluationStatus, payload.get("state"), EvaluationStatus.NOT_EVALUATED),
            items=tuple(
                TenGodInterpretationResult.from_dict(item if isinstance(item, Mapping) else None)
                for item in items_raw
            ),
            summary=as_str_tuple(payload.get("summary")),
            evidence_ids=as_str_tuple(payload.get("evidence_ids")),
            trace_ids=as_str_tuple(payload.get("trace_ids")),
            confidence=ConfidenceValue.from_dict(confidence_raw),
            schema_version=as_str(payload.get("schema_version"), SCHEMA_TEN_GODS),
            ruleset_version=as_str(payload.get("ruleset_version"), TEN_GODS_RULESET_VERSION),
        )


def confidence_band(value: ConfidenceValue) -> TenGodConfidenceBand:
    """Read categorical confidence from the summary field."""
    try:
        return TenGodConfidenceBand(value.summary) if value.summary else TenGodConfidenceBand.UNRESOLVED
    except ValueError:
        return TenGodConfidenceBand.UNRESOLVED
