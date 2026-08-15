"""Ten Gods interpretation and narrative mapping — structured, not customer prose."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

from engines.interpretation_engine.foundation.interpreters.ten_gods.facts import (
    TenGodFacts,
)
from engines.interpretation_engine.foundation.interpreters.ten_gods.relationships import (
    explain_ten_god_relationships,
)
from engines.interpretation_engine.foundation.knowledge.diagnostics import (
    BROKEN_RELATIONSHIP,
    INVALID_POSITION,
    INVALID_TEN_GOD,
    MISSING_NARRATIVE_MAPPING,
    TEN_GOD_CONCEPTS_MISSING,
    TEN_GOD_KNOWLEDGE_MISSING,
)
from engines.interpretation_engine.foundation.knowledge.entity_types import (
    KNOWLEDGE_READINESS_PARTIAL,
    KNOWLEDGE_READINESS_READY,
)
from engines.interpretation_engine.foundation.knowledge.ten_god_bundle import (
    TenGodKnowledgeBundle,
)
from engines.interpretation_engine.foundation.knowledge.ten_god_retrieval import (
    build_ten_god_knowledge_bundle,
)
from engines.interpretation_engine.foundation.relationship import (
    RelationshipAssessment,
    validate_relationship_assessment,
)
from engines.interpretation_engine.foundation.status import DataAvailability


@dataclass(frozen=True, slots=True)
class TenGodRoleInterpretation:
    """Structured meaning for one Ten God role present in facts."""

    key: str
    positions: tuple[dict[str, str], ...]
    role_meaning: str
    strengths: str
    risks: str
    activation: tuple[str, ...]
    interaction_with_day_master: str
    interaction_with_pattern: str
    interaction_with_useful_god: str
    applications: Mapping[str, str]

    def to_dict(self) -> dict[str, Any]:
        """Serialize one role interpretation."""
        return {
            "key": self.key,
            "positions": [dict(item) for item in self.positions],
            "role_meaning": self.role_meaning,
            "strengths": self.strengths,
            "risks": self.risks,
            "activation": list(self.activation),
            "interaction_with_day_master": self.interaction_with_day_master,
            "interaction_with_pattern": self.interaction_with_pattern,
            "interaction_with_useful_god": self.interaction_with_useful_god,
            "applications": dict(self.applications),
        }


@dataclass(frozen=True, slots=True)
class TenGodInterpretationResult:
    """Structured answers for present Ten God roles. Not customer prose."""

    roles: tuple[TenGodRoleInterpretation, ...]
    creating_relationships: tuple[dict[str, str], ...]

    def to_dict(self) -> dict[str, Any]:
        """Serialize interpretation without long customer prose."""
        return {
            "roles": [item.to_dict() for item in self.roles],
            "creating_relationships": [dict(item) for item in self.creating_relationships],
        }


@dataclass(frozen=True, slots=True)
class TenGodNarrativeFacts:
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
class TenGodInterpretationBundle:
    """Complete Ten Gods domain output from facts through narrative mapping."""

    facts: TenGodFacts
    relationship: RelationshipAssessment
    knowledge: TenGodKnowledgeBundle
    interpretation: TenGodInterpretationResult
    narrative: TenGodNarrativeFacts
    status: DataAvailability
    readiness: str
    diagnostics: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        """Serialize the Ten Gods domain bundle."""
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


def build_ten_god_interpretation_bundle(
    facts: TenGodFacts,
    *,
    relationship: RelationshipAssessment | None = None,
    knowledge: TenGodKnowledgeBundle | None = None,
) -> TenGodInterpretationBundle:
    """Assemble Ten Gods interpretation from facts, relationships, and knowledge."""
    graph = relationship or explain_ten_god_relationships(facts)
    bundle = knowledge or build_ten_god_knowledge_bundle(facts)
    interpretation = _interpret(facts, graph, bundle)
    narrative = build_ten_god_narrative_facts(facts, graph, bundle, interpretation)
    diagnostics = list(dict.fromkeys([*facts.diagnostics, *graph.diagnostics, *bundle.diagnostics]))
    relation_result = validate_relationship_assessment(graph)
    if not relation_result.passed:
        diagnostics.append(BROKEN_RELATIONSHIP)
    if not narrative.summary or not narrative.reasoning:
        diagnostics.append(MISSING_NARRATIVE_MAPPING)
    diagnostics = list(dict.fromkeys(diagnostics))
    blocking = {
        TEN_GOD_KNOWLEDGE_MISSING,
        TEN_GOD_CONCEPTS_MISSING,
        INVALID_TEN_GOD,
        INVALID_POSITION,
        BROKEN_RELATIONSHIP,
        MISSING_NARRATIVE_MAPPING,
    } & set(diagnostics)
    if INVALID_TEN_GOD in diagnostics or INVALID_POSITION in diagnostics:
        status = DataAvailability.INVALID
        readiness = KNOWLEDGE_READINESS_PARTIAL
    elif blocking:
        status = DataAvailability.PARTIAL
        readiness = KNOWLEDGE_READINESS_PARTIAL
    else:
        status = DataAvailability.AVAILABLE
        readiness = KNOWLEDGE_READINESS_READY
    return TenGodInterpretationBundle(
        facts=facts,
        relationship=graph,
        knowledge=bundle,
        interpretation=interpretation,
        narrative=narrative,
        status=status,
        readiness=readiness,
        diagnostics=tuple(diagnostics),
    )


def build_ten_god_narrative_facts(
    facts: TenGodFacts,
    relationship: RelationshipAssessment,
    knowledge: TenGodKnowledgeBundle,
    interpretation: TenGodInterpretationResult,
) -> TenGodNarrativeFacts:
    """Map interpretation fields to narrative slots. Do not compose customer text."""
    summary = tuple(
        item
        for item in (
            *facts.selected_roles,
            facts.day_master,
            facts.strength_context,
        )
        if item
    )
    reasoning = tuple(
        f"{edge.source}->{edge.relationship_type}->{edge.target}"
        for edge in relationship.graph.edges
    )
    impacts: list[str] = []
    recommendations: list[Mapping[str, Any]] = []
    warnings: list[Mapping[str, Any]] = []
    for role in interpretation.roles:
        for area, text in role.applications.items():
            if str(text).strip():
                impacts.append(f"{role.key}:{area}:{text}")
    for entity in knowledge.entities:
        recommendations.extend(dict(item) for item in entity.recommendations)
        warnings.extend(dict(item) for item in entity.warnings)
    return TenGodNarrativeFacts(
        summary=summary,
        reasoning=reasoning,
        impacts=tuple(impacts),
        recommendations=tuple(recommendations),
        warnings=tuple(warnings),
    )


def _interpret(
    facts: TenGodFacts,
    relationship: RelationshipAssessment,
    knowledge: TenGodKnowledgeBundle,
) -> TenGodInterpretationResult:
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
    roles: list[TenGodRoleInterpretation] = []
    for key in _role_order(facts):
        entity = by_key.get(key)
        positions = tuple(
            {
                "pillar": item.pillar,
                "visibility": item.visibility,
                "stem": item.stem,
                "branch": item.branch,
            }
            for item in facts.positions
            if item.name == key
        )
        activation = tuple(
            f"{item.visibility}:{item.pillar}"
            for item in facts.positions
            if item.name == key and (item.visibility or item.pillar)
        )
        roles.append(
            TenGodRoleInterpretation(
                key=key,
                positions=positions,
                role_meaning=entity.meaning if entity else "",
                strengths=entity.positive_meaning if entity else "",
                risks=entity.negative_meaning if entity else "",
                activation=activation,
                interaction_with_day_master=_day_master_interaction(facts, key),
                interaction_with_pattern=_pattern_interaction(facts, key),
                interaction_with_useful_god=_useful_god_interaction(facts, key),
                applications=dict(entity.applications) if entity else {},
            )
        )
    return TenGodInterpretationResult(
        roles=tuple(roles),
        creating_relationships=creating,
    )


def _role_order(facts: TenGodFacts) -> tuple[str, ...]:
    """Preserve visible then hidden uniqueness; one interpretation per role."""
    return tuple(dict.fromkeys([*facts.visible_roles, *facts.hidden_roles]))


def _day_master_interaction(facts: TenGodFacts, key: str) -> str:
    """Copy day-master relation without predicting outcomes."""
    if not facts.day_master:
        return f"role:{key}"
    if key == "Nhật Chủ":
        return f"identity:{facts.day_master}"
    return f"relation:{key}:day_master:{facts.day_master}"


def _pattern_interaction(facts: TenGodFacts, key: str) -> str:
    """Copy selected pattern as frame; Ten Gods does not reselect pattern."""
    if not facts.pattern_label:
        return f"role:{key}:pattern:unset"
    return f"role:{key}:pattern_frame:{facts.pattern_label}"


def _useful_god_interaction(facts: TenGodFacts, key: str) -> str:
    """Copy Useful God selection; Decision owns assignment."""
    selected = facts.useful_god_selected
    if not selected:
        return f"role:{key}:useful_god:unset"
    if key == selected:
        return f"role:{key}:matches_useful_god:{selected}"
    return f"role:{key}:present_beside_useful_god:{selected}"
