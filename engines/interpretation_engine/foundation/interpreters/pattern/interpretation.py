"""Pattern interpretation and narrative mapping — structured, not customer prose."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

from engines.interpretation_engine.foundation.interpreters.pattern.facts import (
    PatternFacts,
)
from engines.interpretation_engine.foundation.interpreters.pattern.relationships import (
    explain_pattern_relationships,
)
from engines.interpretation_engine.foundation.knowledge.diagnostics import (
    BROKEN_RELATIONSHIP,
    INVALID_PATTERN,
    MISSING_NARRATIVE_MAPPING,
    PATTERN_CONCEPTS_MISSING,
    PATTERN_KNOWLEDGE_MISSING,
)
from engines.interpretation_engine.foundation.knowledge.entity_types import (
    KNOWLEDGE_READINESS_PARTIAL,
    KNOWLEDGE_READINESS_READY,
)
from engines.interpretation_engine.foundation.knowledge.pattern_bundle import (
    PatternKnowledgeBundle,
)
from engines.interpretation_engine.foundation.knowledge.pattern_retrieval import (
    build_pattern_knowledge_bundle,
)
from engines.interpretation_engine.foundation.relationship import (
    RelationshipAssessment,
    validate_relationship_assessment,
)
from engines.interpretation_engine.foundation.status import DataAvailability


@dataclass(frozen=True, slots=True)
class PatternInterpretationResult:
    """Structured answers for why the pattern exists and what it implies."""

    why_exists: tuple[str, ...]
    creating_relationships: tuple[dict[str, str], ...]
    structural_meaning: str
    strengths: str
    risks: str
    applications: Mapping[str, str]
    activation_conditions: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        """Serialize interpretation without long customer prose."""
        return {
            "why_exists": list(self.why_exists),
            "creating_relationships": [dict(item) for item in self.creating_relationships],
            "structural_meaning": self.structural_meaning,
            "strengths": self.strengths,
            "risks": self.risks,
            "applications": dict(self.applications),
            "activation_conditions": list(self.activation_conditions),
        }


@dataclass(frozen=True, slots=True)
class PatternNarrativeFacts:
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
class PatternInterpretationBundle:
    """Complete Pattern domain output from facts through narrative mapping."""

    facts: PatternFacts
    relationship: RelationshipAssessment
    knowledge: PatternKnowledgeBundle
    interpretation: PatternInterpretationResult
    narrative: PatternNarrativeFacts
    status: DataAvailability
    readiness: str
    diagnostics: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        """Serialize the Pattern domain bundle."""
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


def build_pattern_interpretation_bundle(
    facts: PatternFacts,
    *,
    relationship: RelationshipAssessment | None = None,
    knowledge: PatternKnowledgeBundle | None = None,
) -> PatternInterpretationBundle:
    """Assemble Pattern interpretation from facts, relationships, and knowledge."""
    graph = relationship or explain_pattern_relationships(facts)
    bundle = knowledge or build_pattern_knowledge_bundle(facts)
    interpretation = _interpret(facts, graph, bundle)
    narrative = build_pattern_narrative_facts(facts, graph, bundle, interpretation)
    diagnostics = list(dict.fromkeys([*facts.diagnostics, *graph.diagnostics, *bundle.diagnostics]))
    relation_result = validate_relationship_assessment(graph)
    if not relation_result.passed:
        diagnostics.append(BROKEN_RELATIONSHIP)
    if not narrative.summary or not narrative.reasoning:
        diagnostics.append(MISSING_NARRATIVE_MAPPING)
    diagnostics = list(dict.fromkeys(diagnostics))
    blocking = {
        PATTERN_KNOWLEDGE_MISSING,
        PATTERN_CONCEPTS_MISSING,
        INVALID_PATTERN,
        BROKEN_RELATIONSHIP,
        MISSING_NARRATIVE_MAPPING,
    } & set(diagnostics)
    if INVALID_PATTERN in diagnostics:
        status = DataAvailability.INVALID
        readiness = KNOWLEDGE_READINESS_PARTIAL
    elif blocking:
        status = DataAvailability.PARTIAL
        readiness = KNOWLEDGE_READINESS_PARTIAL
    else:
        status = DataAvailability.AVAILABLE
        readiness = KNOWLEDGE_READINESS_READY
    return PatternInterpretationBundle(
        facts=facts,
        relationship=graph,
        knowledge=bundle,
        interpretation=interpretation,
        narrative=narrative,
        status=status,
        readiness=readiness,
        diagnostics=tuple(diagnostics),
    )


def build_pattern_narrative_facts(
    facts: PatternFacts,
    relationship: RelationshipAssessment,
    knowledge: PatternKnowledgeBundle,
    interpretation: PatternInterpretationResult,
) -> PatternNarrativeFacts:
    """Map interpretation fields to narrative slots. Do not compose customer text."""
    entity = knowledge.pattern_entity
    summary = tuple(
        item
        for item in (
            facts.label or facts.selected,
            facts.month_command,
            facts.reason,
        )
        if item
    )
    reasoning = tuple(
        f"{edge.source}->{edge.relationship_type}->{edge.target}"
        for edge in relationship.graph.edges
    )
    impacts = tuple(
        f"{area}:{text}"
        for area, text in interpretation.applications.items()
        if str(text).strip()
    )
    recommendations = tuple(dict(item) for item in (entity.recommendations if entity else ()))
    warnings = tuple(dict(item) for item in (entity.warnings if entity else ()))
    return PatternNarrativeFacts(
        summary=summary,
        reasoning=reasoning,
        impacts=impacts,
        recommendations=recommendations,
        warnings=warnings,
    )


def _interpret(
    facts: PatternFacts,
    relationship: RelationshipAssessment,
    knowledge: PatternKnowledgeBundle,
) -> PatternInterpretationResult:
    """Fill structured interpretation slots from facts + knowledge."""
    entity = knowledge.pattern_entity
    why = tuple(
        item
        for item in (
            f"selected:{facts.selected}",
            f"month_command:{facts.month_command}" if facts.month_command else "",
            f"reason:{facts.reason}" if facts.reason else "",
        )
        if item and not item.endswith(":")
    )
    creating = tuple(
        {
            "source": edge.source,
            "type": edge.relationship_type,
            "target": edge.target,
        }
        for edge in relationship.graph.edges
    )
    conditions = tuple(facts.supporting_relationships)
    if entity is not None:
        return PatternInterpretationResult(
            why_exists=why,
            creating_relationships=creating,
            structural_meaning=entity.meaning,
            strengths=entity.positive_meaning,
            risks=entity.negative_meaning,
            applications=dict(entity.applications),
            activation_conditions=conditions,
        )
    return PatternInterpretationResult(
        why_exists=why,
        creating_relationships=creating,
        structural_meaning="",
        strengths="",
        risks="",
        applications={},
        activation_conditions=conditions,
    )
