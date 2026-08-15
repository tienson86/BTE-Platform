"""Shen Sha interpretation and narrative mapping — structured, not customer prose."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

from engines.interpretation_engine.foundation.interpreters.shensha.facts import (
    ShenShaFacts,
)
from engines.interpretation_engine.foundation.interpreters.shensha.relationships import (
    explain_shensha_relationships,
)
from engines.interpretation_engine.foundation.knowledge.diagnostics import (
    BROKEN_RELATIONSHIP,
    INVALID_SHENSHA,
    MISSING_NARRATIVE_MAPPING,
    SHENSHA_CONCEPTS_MISSING,
    SHENSHA_KNOWLEDGE_MISSING,
)
from engines.interpretation_engine.foundation.knowledge.entity_types import (
    KNOWLEDGE_READINESS_PARTIAL,
    KNOWLEDGE_READINESS_READY,
)
from engines.interpretation_engine.foundation.knowledge.shensha_bundle import (
    ShenShaKnowledgeBundle,
)
from engines.interpretation_engine.foundation.knowledge.shensha_retrieval import (
    build_shensha_knowledge_bundle,
)
from engines.interpretation_engine.foundation.relationship import (
    RelationshipAssessment,
    validate_relationship_assessment,
)
from engines.interpretation_engine.foundation.status import DataAvailability


@dataclass(frozen=True, slots=True)
class ShenShaStarInterpretation:
    """Structured expert interpretation for one matched Shen Sha."""

    key: str
    why_exists: str
    mechanism: str
    base_influence: str
    conditional_influence: str
    activation: tuple[str, ...]
    typical_triggers: tuple[str, ...]
    suppression: str
    luck_relationship: str
    pattern_relationship: str
    ten_gods_relationship: str
    manifestation: str
    applications: Mapping[str, str]
    contraindications: tuple[Mapping[str, Any], ...]

    def to_dict(self) -> dict[str, Any]:
        """Serialize one star interpretation."""
        return {
            "key": self.key,
            "why_exists": self.why_exists,
            "mechanism": self.mechanism,
            "base_influence": self.base_influence,
            "conditional_influence": self.conditional_influence,
            "activation": list(self.activation),
            "typical_triggers": list(self.typical_triggers),
            "suppression": self.suppression,
            "luck_relationship": self.luck_relationship,
            "pattern_relationship": self.pattern_relationship,
            "ten_gods_relationship": self.ten_gods_relationship,
            "manifestation": self.manifestation,
            "applications": dict(self.applications),
            "contraindications": [dict(item) for item in self.contraindications],
        }


@dataclass(frozen=True, slots=True)
class ShenShaInterpretationResult:
    """Structured answers for matched Shen Sha. Not customer prose."""

    stars: tuple[ShenShaStarInterpretation, ...]
    creating_relationships: tuple[dict[str, str], ...]

    def to_dict(self) -> dict[str, Any]:
        """Serialize interpretation without long customer prose."""
        return {
            "stars": [item.to_dict() for item in self.stars],
            "creating_relationships": [dict(item) for item in self.creating_relationships],
        }


@dataclass(frozen=True, slots=True)
class ShenShaNarrativeFacts:
    """Structured narrative inputs for a later composer. Not generated prose."""

    summary: tuple[str, ...]
    reasoning: tuple[str, ...]
    impacts: tuple[str, ...]
    recommendations: tuple[Mapping[str, Any], ...]
    warnings: tuple[Mapping[str, Any], ...]

    def to_dict(self) -> dict[str, Any]:
        """Serialize narrative mapping."""
        return {
            "summary": list(self.summary),
            "reasoning": list(self.reasoning),
            "impacts": list(self.impacts),
            "recommendations": [dict(item) for item in self.recommendations],
            "warnings": [dict(item) for item in self.warnings],
        }


@dataclass(frozen=True, slots=True)
class ShenShaInterpretationBundle:
    """Complete Shen Sha domain output from facts through narrative mapping."""

    facts: ShenShaFacts
    relationship: RelationshipAssessment
    knowledge: ShenShaKnowledgeBundle
    interpretation: ShenShaInterpretationResult
    narrative: ShenShaNarrativeFacts
    status: DataAvailability
    readiness: str
    diagnostics: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        """Serialize the Shen Sha domain bundle."""
        return {
            "facts": self.facts.to_dict(),
            "relationship": self.relationship.to_dict(),
            "knowledge": self.knowledge.to_dict(),
            "interpretation": self.interpretation.to_dict(),
            "narrative": self.narrative.to_dict(),
            "status": self.status.value,
            "readiness": self.readiness,
            "diagnostics": list(self.diagnostics),
        }


def build_shensha_interpretation_bundle(
    facts: ShenShaFacts,
    *,
    relationship: RelationshipAssessment | None = None,
    knowledge: ShenShaKnowledgeBundle | None = None,
) -> ShenShaInterpretationBundle:
    """Assemble Shen Sha interpretation from facts, relationships, and knowledge."""
    graph = relationship or explain_shensha_relationships(facts)
    bundle = knowledge or build_shensha_knowledge_bundle(facts)
    interpretation = _interpret(facts, graph, bundle)
    narrative = build_shensha_narrative_facts(facts, graph, bundle, interpretation)
    diagnostics = list(dict.fromkeys([*facts.diagnostics, *graph.diagnostics, *bundle.diagnostics]))
    relation_result = validate_relationship_assessment(graph)
    if not relation_result.passed:
        diagnostics.append(BROKEN_RELATIONSHIP)
    if not narrative.summary or not narrative.reasoning:
        diagnostics.append(MISSING_NARRATIVE_MAPPING)
    diagnostics = list(dict.fromkeys(diagnostics))
    blocking = {
        SHENSHA_KNOWLEDGE_MISSING,
        SHENSHA_CONCEPTS_MISSING,
        INVALID_SHENSHA,
        BROKEN_RELATIONSHIP,
        MISSING_NARRATIVE_MAPPING,
    } & set(diagnostics)
    if INVALID_SHENSHA in diagnostics:
        status = DataAvailability.INVALID
        readiness = KNOWLEDGE_READINESS_PARTIAL
    elif blocking:
        status = DataAvailability.PARTIAL
        readiness = KNOWLEDGE_READINESS_PARTIAL
    else:
        status = DataAvailability.AVAILABLE
        readiness = KNOWLEDGE_READINESS_READY
    return ShenShaInterpretationBundle(
        facts=facts,
        relationship=graph,
        knowledge=bundle,
        interpretation=interpretation,
        narrative=narrative,
        status=status,
        readiness=readiness,
        diagnostics=tuple(diagnostics),
    )


def build_shensha_narrative_facts(
    facts: ShenShaFacts,
    relationship: RelationshipAssessment,
    knowledge: ShenShaKnowledgeBundle,
    interpretation: ShenShaInterpretationResult,
) -> ShenShaNarrativeFacts:
    """Map interpretation fields to narrative slots. Do not compose customer text."""
    summary = tuple(
        item
        for item in (*facts.matched_shensha, facts.day_master, facts.pattern_label)
        if item
    )
    reasoning = tuple(
        f"{edge.source}->{edge.relationship_type}->{edge.target}"
        for edge in relationship.graph.edges
    )
    impacts: list[str] = []
    recommendations: list[Mapping[str, Any]] = []
    warnings: list[Mapping[str, Any]] = []
    for star in interpretation.stars:
        for area, text in star.applications.items():
            if str(text).strip():
                impacts.append(f"{star.key}:{area}:{text}")
    for entity in knowledge.entities:
        recommendations.extend(dict(item) for item in entity.recommendations)
        warnings.extend(dict(item) for item in entity.warnings)
    return ShenShaNarrativeFacts(
        summary=summary,
        reasoning=reasoning,
        impacts=tuple(impacts),
        recommendations=tuple(recommendations),
        warnings=tuple(warnings),
    )


def _interpret(
    facts: ShenShaFacts,
    relationship: RelationshipAssessment,
    knowledge: ShenShaKnowledgeBundle,
) -> ShenShaInterpretationResult:
    """Fill structured interpretation slots from facts + knowledge."""
    creating = tuple(
        {
            "source": edge.source,
            "type": edge.relationship_type,
            "target": edge.target,
        }
        for edge in relationship.graph.edges
    )
    by_key = {entity.key: entity for entity in knowledge.entities}
    by_match = {item.name: item for item in facts.matches}
    stars: list[ShenShaStarInterpretation] = []
    for key in facts.matched_shensha:
        entity = by_key.get(key)
        match = by_match.get(key)
        why = ""
        if match is not None:
            why = f"matched:{key}:reason:{match.match_reason}"
        stars.append(
            ShenShaStarInterpretation(
                key=key,
                why_exists=why,
                mechanism=entity.mechanism if entity else "",
                base_influence=entity.base_influence if entity else "",
                conditional_influence=entity.conditional_influence if entity else "",
                activation=entity.activation_conditions if entity else (),
                typical_triggers=entity.typical_triggers if entity else (),
                suppression=entity.suppression if entity else "",
                luck_relationship=entity.luck_relationship if entity else "",
                pattern_relationship=_pattern_note(facts, entity),
                ten_gods_relationship=_ten_god_note(facts, entity),
                manifestation=entity.manifestation if entity else "",
                applications=dict(entity.applications) if entity else {},
                contraindications=tuple(entity.contraindications) if entity else (),
            )
        )
    return ShenShaInterpretationResult(stars=tuple(stars), creating_relationships=creating)


def _pattern_note(facts: ShenShaFacts, entity: Any) -> str:
    """Copy pattern frame beside entity relationship text."""
    base = entity.pattern_relationship if entity is not None else ""
    if facts.pattern_label:
        return f"{base}|pattern_frame:{facts.pattern_label}" if base else f"pattern_frame:{facts.pattern_label}"
    return base


def _ten_god_note(facts: ShenShaFacts, entity: Any) -> str:
    """Copy present ten-god roles beside entity relationship text."""
    base = entity.ten_gods_relationship if entity is not None else ""
    if facts.ten_god_roles:
        joined = ",".join(facts.ten_god_roles)
        return f"{base}|present_roles:{joined}" if base else f"present_roles:{joined}"
    return base
