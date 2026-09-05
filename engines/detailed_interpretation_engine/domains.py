"""Pack 07 domain result shells.

No domain scoring or inference.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping

from engines.detailed_interpretation_engine.codec import as_enum, as_str, as_str_dict, as_str_tuple
from engines.detailed_interpretation_engine.constants import SCHEMA_DOMAIN
from engines.detailed_interpretation_engine.enums import DomainState
from engines.detailed_interpretation_engine.value_objects import ConfidenceValue

GRAPH_RELATIONS: frozenset[str] = frozenset({"supports", "depends_on", "conflicts", "reinforces"})


def _domain_from_mapping(data: Mapping[str, Any] | None, default_id: str) -> DomainInterpretationResult:
    payload = data or {}
    domain_id = as_str(payload.get("domain_id"), default_id) or default_id
    evidence_ids = as_str_tuple(payload.get("evidence_ids") or payload.get("supporting_evidence_ids"))
    return DomainInterpretationResult(
        domain_id=domain_id,
        state=as_enum(DomainState, payload.get("state"), DomainState.NOT_EVALUATED),
        priority=as_str(payload.get("priority")),
        strengths=as_str_tuple(payload.get("strengths")),
        risks=as_str_tuple(payload.get("risks")),
        opportunities=as_str_tuple(payload.get("opportunities")),
        conditions=as_str_tuple(payload.get("conditions")),
        warnings=as_str_tuple(payload.get("warnings")),
        driver=as_str(payload.get("driver")),
        driver_id=as_str(payload.get("driver_id")),
        driver_evidence_ids=as_str_tuple(payload.get("driver_evidence_ids")),
        support=as_str(payload.get("support")),
        bottleneck=as_str(payload.get("bottleneck")),
        risk=as_str(payload.get("risk")),
        condition=as_str(payload.get("condition")),
        leakage=as_str(payload.get("leakage")),
        confidence=ConfidenceValue.from_dict(payload.get("confidence")),
        supporting_evidence_ids=evidence_ids,
        evidence_ids=evidence_ids,
        trace_ids=as_str_tuple(payload.get("trace_ids")),
        dimensions=as_str_dict(payload.get("dimensions")),
        driver_source=as_str(payload.get("driver_source")),
        support_source=as_str(payload.get("support_source")),
        bottleneck_source=as_str(payload.get("bottleneck_source")),
        customer_summary=as_str(payload.get("customer_summary")),
        schema_version=as_str(payload.get("schema_version"), SCHEMA_DOMAIN),
    )


@dataclass(frozen=True, slots=True)
class DomainInterpretationResult:
    """Single natal domain interpretation container (DI-08)."""

    domain_id: str = ""
    state: DomainState = DomainState.NOT_EVALUATED
    priority: str = ""
    strengths: tuple[str, ...] = ()
    risks: tuple[str, ...] = ()
    opportunities: tuple[str, ...] = ()
    conditions: tuple[str, ...] = ()
    warnings: tuple[str, ...] = ()
    driver: str = ""
    driver_id: str = ""
    driver_evidence_ids: tuple[str, ...] = ()
    support: str = ""
    bottleneck: str = ""
    risk: str = ""
    condition: str = ""
    leakage: str = ""
    confidence: ConfidenceValue = field(default_factory=ConfidenceValue)
    supporting_evidence_ids: tuple[str, ...] = ()
    evidence_ids: tuple[str, ...] = ()
    trace_ids: tuple[str, ...] = ()
    dimensions: dict[str, str] = field(default_factory=dict)
    driver_source: str = ""
    support_source: str = ""
    bottleneck_source: str = ""
    customer_summary: str = ""
    schema_version: str = SCHEMA_DOMAIN

    @classmethod
    def from_dict(cls, data: Mapping[str, Any] | None, default_id: str = "") -> DomainInterpretationResult:
        """Rebuild one domain result."""
        return _domain_from_mapping(data, default_id)


@dataclass(frozen=True, slots=True)
class AuthorityResult:
    """DI-12 Authority natal shell. Does not copy Grade."""

    natal: DomainInterpretationResult = field(
        default_factory=lambda: DomainInterpretationResult(domain_id="authority")
    )

    @classmethod
    def from_dict(cls, data: Mapping[str, Any] | None) -> AuthorityResult:
        """Rebuild Authority from a mapping."""
        payload = data or {}
        natal_raw = payload.get("natal") if isinstance(payload.get("natal"), Mapping) else payload
        return cls(natal=_domain_from_mapping(natal_raw if isinstance(natal_raw, Mapping) else None, "authority"))


@dataclass(frozen=True, slots=True)
class CareerResult:
    """DI-13 Career natal shell."""

    natal: DomainInterpretationResult = field(
        default_factory=lambda: DomainInterpretationResult(domain_id="career")
    )

    @classmethod
    def from_dict(cls, data: Mapping[str, Any] | None) -> CareerResult:
        """Rebuild Career from a mapping."""
        payload = data or {}
        natal_raw = payload.get("natal") if isinstance(payload.get("natal"), Mapping) else payload
        return cls(natal=_domain_from_mapping(natal_raw if isinstance(natal_raw, Mapping) else None, "career"))


@dataclass(frozen=True, slots=True)
class WealthResult:
    """DI-14 Wealth natal shell. Creation / retention live in later engines."""

    natal: DomainInterpretationResult = field(
        default_factory=lambda: DomainInterpretationResult(domain_id="wealth")
    )

    @classmethod
    def from_dict(cls, data: Mapping[str, Any] | None) -> WealthResult:
        """Rebuild Wealth from a mapping."""
        payload = data or {}
        natal_raw = payload.get("natal") if isinstance(payload.get("natal"), Mapping) else payload
        return cls(natal=_domain_from_mapping(natal_raw if isinstance(natal_raw, Mapping) else None, "wealth"))


@dataclass(frozen=True, slots=True)
class RelationshipResult:
    """DI-15 Relationship natal shell."""

    natal: DomainInterpretationResult = field(
        default_factory=lambda: DomainInterpretationResult(domain_id="relationship")
    )

    @classmethod
    def from_dict(cls, data: Mapping[str, Any] | None) -> RelationshipResult:
        """Rebuild Relationship from a mapping."""
        payload = data or {}
        natal_raw = payload.get("natal") if isinstance(payload.get("natal"), Mapping) else payload
        return cls(natal=_domain_from_mapping(natal_raw if isinstance(natal_raw, Mapping) else None, "relationship"))


@dataclass(frozen=True, slots=True)
class LegacyResult:
    """DI-16 Legacy natal shell."""

    natal: DomainInterpretationResult = field(
        default_factory=lambda: DomainInterpretationResult(domain_id="legacy")
    )

    @classmethod
    def from_dict(cls, data: Mapping[str, Any] | None) -> LegacyResult:
        """Rebuild Legacy from a mapping."""
        payload = data or {}
        natal_raw = payload.get("natal") if isinstance(payload.get("natal"), Mapping) else payload
        return cls(natal=_domain_from_mapping(natal_raw if isinstance(natal_raw, Mapping) else None, "legacy"))


@dataclass(frozen=True, slots=True)
class VitalityResult:
    """DI-17 Vitality natal shell."""

    natal: DomainInterpretationResult = field(
        default_factory=lambda: DomainInterpretationResult(domain_id="vitality")
    )

    @classmethod
    def from_dict(cls, data: Mapping[str, Any] | None) -> VitalityResult:
        """Rebuild Vitality from a mapping."""
        payload = data or {}
        natal_raw = payload.get("natal") if isinstance(payload.get("natal"), Mapping) else payload
        return cls(natal=_domain_from_mapping(natal_raw if isinstance(natal_raw, Mapping) else None, "vitality"))


@dataclass(frozen=True, slots=True)
class DomainGraphEdge:
    """One evidence-backed relation between domain nodes. Does not copy state."""

    source: str = ""
    target: str = ""
    relation: str = ""
    evidence_ids: tuple[str, ...] = ()

    @classmethod
    def from_dict(cls, data: Mapping[str, Any] | None) -> DomainGraphEdge:
        """Rebuild one graph edge."""
        payload = data or {}
        return cls(
            source=as_str(payload.get("source")),
            target=as_str(payload.get("target")),
            relation=as_str(payload.get("relation")),
            evidence_ids=as_str_tuple(payload.get("evidence_ids")),
        )


@dataclass(frozen=True, slots=True)
class DomainGraph:
    """Frozen DI-08 domain graph. Edges explain relationship; they do not copy state."""

    nodes: tuple[str, ...] = ()
    edges: tuple[DomainGraphEdge, ...] = ()

    @classmethod
    def from_dict(cls, data: Mapping[str, Any] | None) -> DomainGraph:
        """Rebuild the domain graph."""
        payload = data or {}
        raw_edges = payload.get("edges") or ()
        return cls(
            nodes=as_str_tuple(payload.get("nodes")),
            edges=tuple(
                DomainGraphEdge.from_dict(item if isinstance(item, Mapping) else None)
                for item in raw_edges
            ),
        )


@dataclass(frozen=True, slots=True)
class DomainSection:
    """Published domain layer. Each detailed domain exists once."""

    authority: AuthorityResult = field(default_factory=AuthorityResult)
    career: CareerResult = field(default_factory=CareerResult)
    wealth: WealthResult = field(default_factory=WealthResult)
    relationship: RelationshipResult = field(default_factory=RelationshipResult)
    legacy: LegacyResult = field(default_factory=LegacyResult)
    vitality: VitalityResult = field(default_factory=VitalityResult)
    supporting: dict[str, DomainInterpretationResult] = field(default_factory=dict)
    order: tuple[str, ...] = ()
    graph: DomainGraph = field(default_factory=DomainGraph)

    @classmethod
    def from_dict(cls, data: Mapping[str, Any] | None) -> DomainSection:
        """Rebuild the domain section."""
        payload = data or {}
        supporting_raw = payload.get("supporting")
        supporting: dict[str, DomainInterpretationResult] = {}
        if isinstance(supporting_raw, Mapping):
            for key, item in supporting_raw.items():
                if isinstance(item, Mapping):
                    supporting[str(key)] = _domain_from_mapping(item, str(key))
        graph_raw = payload.get("graph")
        return cls(
            authority=AuthorityResult.from_dict(
                payload.get("authority") if isinstance(payload.get("authority"), Mapping) else None
            ),
            career=CareerResult.from_dict(
                payload.get("career") if isinstance(payload.get("career"), Mapping) else None
            ),
            wealth=WealthResult.from_dict(
                payload.get("wealth") if isinstance(payload.get("wealth"), Mapping) else None
            ),
            relationship=RelationshipResult.from_dict(
                payload.get("relationship") if isinstance(payload.get("relationship"), Mapping) else None
            ),
            legacy=LegacyResult.from_dict(
                payload.get("legacy") if isinstance(payload.get("legacy"), Mapping) else None
            ),
            vitality=VitalityResult.from_dict(
                payload.get("vitality") if isinstance(payload.get("vitality"), Mapping) else None
            ),
            supporting=supporting,
            order=as_str_tuple(payload.get("order")),
            graph=DomainGraph.from_dict(graph_raw if isinstance(graph_raw, Mapping) else None),
        )
