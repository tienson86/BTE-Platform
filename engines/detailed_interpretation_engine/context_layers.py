"""Pack 07 layered context containers.

These objects hold structure only. They do not rank, score, or narrate.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping

from engines.detailed_interpretation_engine.codec import as_enum, as_str
from engines.detailed_interpretation_engine.constants import (
    SCHEMA_COMPOSER,
    SCHEMA_CONTEXT,
    SCHEMA_DOMAIN,
    SCHEMA_EVIDENCE_PRIORITY,
    SCHEMA_LIFE_OPTIMIZATION,
    SCHEMA_TEMPORAL,
)
from engines.detailed_interpretation_engine.context import InterpretationContext
from engines.detailed_interpretation_engine.domains import (
    AuthorityResult,
    CareerResult,
    DomainSection,
    LegacyResult,
    RelationshipResult,
    VitalityResult,
    WealthResult,
)
from engines.detailed_interpretation_engine.enums import EvaluationStatus
from engines.detailed_interpretation_engine.evidence import (
    EvidencePriorityResult,
    ShenShaEcosystem,
    TenGodEcosystem,
)
from engines.detailed_interpretation_engine.narrative import NarrativeSection
from engines.detailed_interpretation_engine.optimization import LifeOptimizationResult
from engines.detailed_interpretation_engine.runtime import CanonicalRuntimeResult
from engines.detailed_interpretation_engine.temporal import (
    LuckActivationResult,
    LuckInteractionResult,
    TemporalActivationResult,
    TemporalSection,
)


@dataclass(frozen=True, slots=True)
class EvidenceContext:
    """Evidence containers only. No Evidence Priority calculation."""

    analysis_id: str = ""
    status: EvaluationStatus = EvaluationStatus.NOT_EVALUATED
    evidence: EvidencePriorityResult = field(default_factory=EvidencePriorityResult)
    ten_gods: TenGodEcosystem = field(default_factory=TenGodEcosystem)
    shen_sha: ShenShaEcosystem = field(default_factory=ShenShaEcosystem)
    schema_version: str = SCHEMA_EVIDENCE_PRIORITY

    @classmethod
    def from_dict(cls, data: Mapping[str, Any] | None) -> EvidenceContext:
        """Rebuild evidence context from a mapping."""
        payload = data or {}
        return cls(
            analysis_id=as_str(payload.get("analysis_id")),
            status=as_enum(
                EvaluationStatus,
                payload.get("status"),
                EvaluationStatus.NOT_EVALUATED,
            ),
            evidence=EvidencePriorityResult.from_dict(
                payload.get("evidence") if isinstance(payload.get("evidence"), Mapping) else None
            ),
            ten_gods=TenGodEcosystem.from_dict(
                payload.get("ten_gods") if isinstance(payload.get("ten_gods"), Mapping) else None
            ),
            shen_sha=ShenShaEcosystem.from_dict(
                payload.get("shen_sha") if isinstance(payload.get("shen_sha"), Mapping) else None
            ),
            schema_version=as_str(payload.get("schema_version"), SCHEMA_EVIDENCE_PRIORITY),
        )


@dataclass(frozen=True, slots=True)
class DomainContext:
    """Natal domain containers only. No domain logic."""

    analysis_id: str = ""
    status: EvaluationStatus = EvaluationStatus.NOT_EVALUATED
    domains: DomainSection = field(default_factory=DomainSection)
    schema_version: str = SCHEMA_DOMAIN

    @property
    def authority(self) -> AuthorityResult:
        """Authority container."""
        return self.domains.authority

    @property
    def career(self) -> CareerResult:
        """Career container."""
        return self.domains.career

    @property
    def wealth(self) -> WealthResult:
        """Wealth container."""
        return self.domains.wealth

    @property
    def relationship(self) -> RelationshipResult:
        """Relationship container."""
        return self.domains.relationship

    @property
    def legacy(self) -> LegacyResult:
        """Legacy container."""
        return self.domains.legacy

    @property
    def vitality(self) -> VitalityResult:
        """Vitality container."""
        return self.domains.vitality

    @classmethod
    def from_dict(cls, data: Mapping[str, Any] | None) -> DomainContext:
        """Rebuild domain context from a mapping."""
        payload = data or {}
        domains_raw = payload.get("domains")
        return cls(
            analysis_id=as_str(payload.get("analysis_id")),
            status=as_enum(
                EvaluationStatus,
                payload.get("status"),
                EvaluationStatus.NOT_EVALUATED,
            ),
            domains=DomainSection.from_dict(
                domains_raw if isinstance(domains_raw, Mapping) else payload
            ),
            schema_version=as_str(payload.get("schema_version"), SCHEMA_DOMAIN),
        )


@dataclass(frozen=True, slots=True)
class TemporalContext:
    """Luck / interaction / temporal containers. No activation logic."""

    analysis_id: str = ""
    status: EvaluationStatus = EvaluationStatus.NOT_EVALUATED
    luck: LuckActivationResult = field(default_factory=LuckActivationResult)
    interaction: LuckInteractionResult = field(default_factory=LuckInteractionResult)
    temporal: TemporalActivationResult = field(default_factory=TemporalActivationResult)
    section: TemporalSection = field(default_factory=TemporalSection)
    schema_version: str = SCHEMA_TEMPORAL

    @classmethod
    def from_dict(cls, data: Mapping[str, Any] | None) -> TemporalContext:
        """Rebuild temporal context from a mapping."""
        payload = data or {}
        section = TemporalSection.from_dict(
            payload.get("section") if isinstance(payload.get("section"), Mapping) else payload
        )
        luck_raw = payload.get("luck")
        interaction_raw = payload.get("interaction")
        temporal_raw = payload.get("temporal")
        return cls(
            analysis_id=as_str(payload.get("analysis_id")),
            status=as_enum(
                EvaluationStatus,
                payload.get("status"),
                EvaluationStatus.NOT_EVALUATED,
            ),
            luck=LuckActivationResult.from_dict(
                luck_raw if isinstance(luck_raw, Mapping) else None
            )
            if luck_raw is not None
            else section.luck_activation,
            interaction=LuckInteractionResult.from_dict(
                interaction_raw if isinstance(interaction_raw, Mapping) else None
            )
            if interaction_raw is not None
            else section.luck_interaction,
            temporal=TemporalActivationResult.from_dict(
                temporal_raw if isinstance(temporal_raw, Mapping) else None
            )
            if temporal_raw is not None
            else section.temporal_activation,
            section=section,
            schema_version=as_str(payload.get("schema_version"), SCHEMA_TEMPORAL),
        )


@dataclass(frozen=True, slots=True)
class OptimizationContext:
    """Optimization input container. No optimization decisions."""

    analysis_id: str = ""
    status: EvaluationStatus = EvaluationStatus.NOT_EVALUATED
    inputs: LifeOptimizationResult = field(default_factory=LifeOptimizationResult)
    schema_version: str = SCHEMA_LIFE_OPTIMIZATION

    @classmethod
    def from_dict(cls, data: Mapping[str, Any] | None) -> OptimizationContext:
        """Rebuild optimization context from a mapping."""
        payload = data or {}
        inputs_raw = payload.get("inputs")
        return cls(
            analysis_id=as_str(payload.get("analysis_id")),
            status=as_enum(
                EvaluationStatus,
                payload.get("status"),
                EvaluationStatus.NOT_EVALUATED,
            ),
            inputs=LifeOptimizationResult.from_dict(
                inputs_raw if isinstance(inputs_raw, Mapping) else None
            ),
            schema_version=as_str(payload.get("schema_version"), SCHEMA_LIFE_OPTIMIZATION),
        )


@dataclass(frozen=True, slots=True)
class NarrativeContext:
    """Narrative input container. No composer."""

    analysis_id: str = ""
    status: EvaluationStatus = EvaluationStatus.NOT_EVALUATED
    inputs: NarrativeSection = field(default_factory=NarrativeSection)
    schema_version: str = SCHEMA_COMPOSER

    @classmethod
    def from_dict(cls, data: Mapping[str, Any] | None) -> NarrativeContext:
        """Rebuild narrative context from a mapping."""
        payload = data or {}
        inputs_raw = payload.get("inputs")
        return cls(
            analysis_id=as_str(payload.get("analysis_id")),
            status=as_enum(
                EvaluationStatus,
                payload.get("status"),
                EvaluationStatus.NOT_EVALUATED,
            ),
            inputs=NarrativeSection.from_dict(
                inputs_raw if isinstance(inputs_raw, Mapping) else None
            ),
            schema_version=as_str(payload.get("schema_version"), SCHEMA_COMPOSER),
        )


@dataclass(frozen=True, slots=True)
class CanonicalAnalysisContext:
    """Full Pack 07 context chain. Context only; runtime stays not_evaluated."""

    analysis_id: str = ""
    status: EvaluationStatus = EvaluationStatus.NOT_EVALUATED
    interpretation: InterpretationContext = field(default_factory=InterpretationContext)
    evidence: EvidenceContext = field(default_factory=EvidenceContext)
    domain: DomainContext = field(default_factory=DomainContext)
    temporal: TemporalContext = field(default_factory=TemporalContext)
    optimization: OptimizationContext = field(default_factory=OptimizationContext)
    narrative: NarrativeContext = field(default_factory=NarrativeContext)
    runtime: CanonicalRuntimeResult = field(default_factory=CanonicalRuntimeResult)
    context_ref: str = ""
    schema_version: str = SCHEMA_CONTEXT

    @classmethod
    def from_dict(cls, data: Mapping[str, Any] | None) -> CanonicalAnalysisContext:
        """Rebuild the canonical analysis context chain."""
        payload = data or {}
        runtime_raw = payload.get("runtime")
        return cls(
            analysis_id=as_str(payload.get("analysis_id")),
            status=as_enum(
                EvaluationStatus,
                payload.get("status"),
                EvaluationStatus.NOT_EVALUATED,
            ),
            interpretation=InterpretationContext.from_dict(
                payload.get("interpretation")
                if isinstance(payload.get("interpretation"), Mapping)
                else None
            ),
            evidence=EvidenceContext.from_dict(
                payload.get("evidence") if isinstance(payload.get("evidence"), Mapping) else None
            ),
            domain=DomainContext.from_dict(
                payload.get("domain") if isinstance(payload.get("domain"), Mapping) else None
            ),
            temporal=TemporalContext.from_dict(
                payload.get("temporal") if isinstance(payload.get("temporal"), Mapping) else None
            ),
            optimization=OptimizationContext.from_dict(
                payload.get("optimization")
                if isinstance(payload.get("optimization"), Mapping)
                else None
            ),
            narrative=NarrativeContext.from_dict(
                payload.get("narrative") if isinstance(payload.get("narrative"), Mapping) else None
            ),
            runtime=CanonicalRuntimeResult.from_dict(
                runtime_raw if isinstance(runtime_raw, Mapping) else None
            ),
            context_ref=as_str(payload.get("context_ref")),
            schema_version=as_str(payload.get("schema_version"), SCHEMA_CONTEXT),
        )
