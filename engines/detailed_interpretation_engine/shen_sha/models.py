"""Shen Sha interpretation and ecosystem result models. Codes only."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping

from engines.detailed_interpretation_engine.codec import as_enum, as_str, as_str_tuple
from engines.detailed_interpretation_engine.constants import (
    SCHEMA_SHEN_SHA,
    SCHEMA_SHEN_SHA_ECOSYSTEM,
    SHEN_SHA_ECOSYSTEM_RULESET_VERSION,
    SHEN_SHA_RULESET_VERSION,
)
from engines.detailed_interpretation_engine.enums import (
    EvaluationStatus,
    ShenShaClusterState,
    ShenShaClusterStrength,
    ShenShaConfidenceModifier,
    ShenShaDependencyState,
    ShenShaInterpretationState,
    ShenShaModifierState,
)
from engines.detailed_interpretation_engine.value_objects import ConfidenceValue


@dataclass(frozen=True, slots=True)
class ShenShaOccurrence:
    """One upstream detection location. Pack 07 does not invent presence."""

    pillar: str = ""
    location: str = ""
    target_value: str = ""

    @classmethod
    def from_dict(cls, data: Mapping[str, Any] | None) -> ShenShaOccurrence:
        """Rebuild one occurrence."""
        payload = data or {}
        return cls(
            pillar=as_str(payload.get("pillar")),
            location=as_str(payload.get("location")),
            target_value=as_str(payload.get("target_value")),
        )


@dataclass(frozen=True, slots=True)
class ShenShaInterpretationResult:
    """Secondary-evidence interpretation of one detected star."""

    shen_sha_id: str = ""
    state: ShenShaInterpretationState = ShenShaInterpretationState.NOT_DETECTED
    detected: bool = False
    positions: tuple[ShenShaOccurrence, ...] = ()
    categories: tuple[str, ...] = ()
    supported_domains: tuple[str, ...] = ()
    required_dependencies: tuple[str, ...] = ()
    dependency_state: ShenShaDependencyState = ShenShaDependencyState.NOT_AVAILABLE
    modifier_state: ShenShaModifierState = ShenShaModifierState.INACTIVE
    confidence_modifier: ShenShaConfidenceModifier = ShenShaConfidenceModifier.NO_EFFECT
    conditions: tuple[str, ...] = ()
    warnings: tuple[str, ...] = ()
    evidence_ids: tuple[str, ...] = ()
    trace_ids: tuple[str, ...] = ()
    confidence: ConfidenceValue = field(default_factory=ConfidenceValue)

    @classmethod
    def from_dict(cls, data: Mapping[str, Any] | None) -> ShenShaInterpretationResult:
        """Rebuild one star interpretation."""
        payload = data or {}
        positions_raw = payload.get("positions") or payload.get("occurrences") or ()
        return cls(
            shen_sha_id=as_str(payload.get("shen_sha_id")),
            state=as_enum(
                ShenShaInterpretationState,
                payload.get("state"),
                ShenShaInterpretationState.NOT_DETECTED,
            ),
            detected=bool(payload.get("detected")),
            positions=tuple(
                ShenShaOccurrence.from_dict(item if isinstance(item, Mapping) else None)
                for item in positions_raw
            ),
            categories=as_str_tuple(payload.get("categories")),
            supported_domains=as_str_tuple(payload.get("supported_domains")),
            required_dependencies=as_str_tuple(payload.get("required_dependencies")),
            dependency_state=as_enum(
                ShenShaDependencyState,
                payload.get("dependency_state"),
                ShenShaDependencyState.NOT_AVAILABLE,
            ),
            modifier_state=as_enum(
                ShenShaModifierState,
                payload.get("modifier_state"),
                ShenShaModifierState.INACTIVE,
            ),
            confidence_modifier=as_enum(
                ShenShaConfidenceModifier,
                payload.get("confidence_modifier"),
                ShenShaConfidenceModifier.NO_EFFECT,
            ),
            conditions=as_str_tuple(payload.get("conditions")),
            warnings=as_str_tuple(payload.get("warnings")),
            evidence_ids=as_str_tuple(payload.get("evidence_ids")),
            trace_ids=as_str_tuple(payload.get("trace_ids")),
            confidence=ConfidenceValue.from_dict(payload.get("confidence")),
        )


@dataclass(frozen=True, slots=True)
class ShenShaInterpretationCollection:
    """DI-05 collection of per-star secondary evidence."""

    analysis_id: str = ""
    schema_version: str = SCHEMA_SHEN_SHA
    ruleset_version: str = SHEN_SHA_RULESET_VERSION
    state: EvaluationStatus = EvaluationStatus.NOT_EVALUATED
    items: tuple[ShenShaInterpretationResult, ...] = ()
    summary: tuple[str, ...] = ()
    warnings: tuple[str, ...] = ()
    evidence_ids: tuple[str, ...] = ()
    trace_ids: tuple[str, ...] = ()
    confidence: ConfidenceValue = field(default_factory=ConfidenceValue)

    @classmethod
    def from_dict(cls, data: Mapping[str, Any] | None) -> ShenShaInterpretationCollection:
        """Rebuild a star interpretation collection."""
        payload = data or {}
        items_raw = payload.get("items") or ()
        return cls(
            analysis_id=as_str(payload.get("analysis_id")),
            schema_version=as_str(payload.get("schema_version"), SCHEMA_SHEN_SHA),
            ruleset_version=as_str(payload.get("ruleset_version"), SHEN_SHA_RULESET_VERSION),
            state=as_enum(EvaluationStatus, payload.get("state"), EvaluationStatus.NOT_EVALUATED),
            items=tuple(
                ShenShaInterpretationResult.from_dict(item if isinstance(item, Mapping) else None)
                for item in items_raw
            ),
            summary=as_str_tuple(payload.get("summary")),
            warnings=as_str_tuple(payload.get("warnings")),
            evidence_ids=as_str_tuple(payload.get("evidence_ids")),
            trace_ids=as_str_tuple(payload.get("trace_ids")),
            confidence=ConfidenceValue.from_dict(payload.get("confidence")),
        )


@dataclass(frozen=True, slots=True)
class ShenShaClusterMember:
    """One candidate or applied member inside a cluster."""

    shen_sha_id: str = ""
    di05_state: str = ""
    contribution: str = "ignored"

    @classmethod
    def from_dict(cls, data: Mapping[str, Any] | None) -> ShenShaClusterMember:
        """Rebuild one cluster member."""
        payload = data or {}
        return cls(
            shen_sha_id=as_str(payload.get("shen_sha_id")),
            di05_state=as_str(payload.get("di05_state")),
            contribution=as_str(payload.get("contribution"), "ignored"),
        )


@dataclass(frozen=True, slots=True)
class ShenShaClusterResult:
    """One Shen Sha evidence cluster. Not a domain classification."""

    cluster_id: str = ""
    state: ShenShaClusterState = ShenShaClusterState.INACTIVE
    members: tuple[ShenShaClusterMember, ...] = ()
    applied_members: tuple[str, ...] = ()
    blocked_members: tuple[str, ...] = ()
    cluster_strength: ShenShaClusterStrength = ShenShaClusterStrength.NONE
    supported_domains: tuple[str, ...] = ()
    dependency_state: ShenShaDependencyState = ShenShaDependencyState.NOT_AVAILABLE
    confidence_modifier: ShenShaConfidenceModifier = ShenShaConfidenceModifier.NO_EFFECT
    conditions: tuple[str, ...] = ()
    warnings: tuple[str, ...] = ()
    evidence_ids: tuple[str, ...] = ()
    trace_ids: tuple[str, ...] = ()

    @classmethod
    def from_dict(cls, data: Mapping[str, Any] | None) -> ShenShaClusterResult:
        """Rebuild one cluster result."""
        payload = data or {}
        members_raw = payload.get("members") or ()
        return cls(
            cluster_id=as_str(payload.get("cluster_id")),
            state=as_enum(ShenShaClusterState, payload.get("state"), ShenShaClusterState.INACTIVE),
            members=tuple(
                ShenShaClusterMember.from_dict(item if isinstance(item, Mapping) else None)
                for item in members_raw
            ),
            applied_members=as_str_tuple(payload.get("applied_members")),
            blocked_members=as_str_tuple(payload.get("blocked_members")),
            cluster_strength=as_enum(
                ShenShaClusterStrength,
                payload.get("cluster_strength"),
                ShenShaClusterStrength.NONE,
            ),
            supported_domains=as_str_tuple(payload.get("supported_domains")),
            dependency_state=as_enum(
                ShenShaDependencyState,
                payload.get("dependency_state"),
                ShenShaDependencyState.NOT_AVAILABLE,
            ),
            confidence_modifier=as_enum(
                ShenShaConfidenceModifier,
                payload.get("confidence_modifier"),
                ShenShaConfidenceModifier.NO_EFFECT,
            ),
            conditions=as_str_tuple(payload.get("conditions")),
            warnings=as_str_tuple(payload.get("warnings")),
            evidence_ids=as_str_tuple(payload.get("evidence_ids")),
            trace_ids=as_str_tuple(payload.get("trace_ids")),
        )


@dataclass(frozen=True, slots=True)
class ShenShaEcosystemResult:
    """Global Shen Sha secondary-evidence ecosystem."""

    analysis_id: str = ""
    schema_version: str = SCHEMA_SHEN_SHA_ECOSYSTEM
    ruleset_version: str = SHEN_SHA_ECOSYSTEM_RULESET_VERSION
    state: EvaluationStatus = EvaluationStatus.NOT_EVALUATED
    clusters: tuple[ShenShaClusterResult, ...] = ()
    active_clusters: tuple[str, ...] = ()
    inactive_clusters: tuple[str, ...] = ()
    blocked_clusters: tuple[str, ...] = ()
    dominant_cluster: str = ""
    supporting_cluster: str = ""
    ecosystem_state: str = "unresolved"
    conditions: tuple[str, ...] = ()
    warnings: tuple[str, ...] = ()
    evidence_ids: tuple[str, ...] = ()
    trace_ids: tuple[str, ...] = ()
    confidence: ConfidenceValue = field(default_factory=ConfidenceValue)

    @classmethod
    def from_dict(cls, data: Mapping[str, Any] | None) -> ShenShaEcosystemResult:
        """Rebuild a Shen Sha ecosystem result."""
        payload = data or {}
        clusters_raw = payload.get("clusters") or ()
        return cls(
            analysis_id=as_str(payload.get("analysis_id")),
            schema_version=as_str(payload.get("schema_version"), SCHEMA_SHEN_SHA_ECOSYSTEM),
            ruleset_version=as_str(
                payload.get("ruleset_version"), SHEN_SHA_ECOSYSTEM_RULESET_VERSION
            ),
            state=as_enum(EvaluationStatus, payload.get("state"), EvaluationStatus.NOT_EVALUATED),
            clusters=tuple(
                ShenShaClusterResult.from_dict(item if isinstance(item, Mapping) else None)
                for item in clusters_raw
            ),
            active_clusters=as_str_tuple(payload.get("active_clusters")),
            inactive_clusters=as_str_tuple(payload.get("inactive_clusters")),
            blocked_clusters=as_str_tuple(payload.get("blocked_clusters")),
            dominant_cluster=as_str(payload.get("dominant_cluster")),
            supporting_cluster=as_str(payload.get("supporting_cluster")),
            ecosystem_state=as_str(payload.get("ecosystem_state"), "unresolved"),
            conditions=as_str_tuple(payload.get("conditions")),
            warnings=as_str_tuple(payload.get("warnings")),
            evidence_ids=as_str_tuple(payload.get("evidence_ids")),
            trace_ids=as_str_tuple(payload.get("trace_ids")),
            confidence=ConfidenceValue.from_dict(payload.get("confidence")),
        )
