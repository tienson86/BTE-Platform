"""Copy upstream bundles into frozen composer input. No calculation."""

from __future__ import annotations

from typing import Any, Iterable, Mapping

from engines.interpretation_engine.foundation.assessment.strength import (
    StrengthAssessment,
)
from engines.interpretation_engine.foundation.explanation.models import (
    DecisionExplanationResult,
)
from engines.interpretation_engine.foundation.interpreters.pattern.interpretation import (
    PatternInterpretationBundle,
)
from engines.interpretation_engine.foundation.interpreters.shensha.interpretation import (
    ShenShaInterpretationBundle,
)
from engines.interpretation_engine.foundation.interpreters.ten_gods.interpretation import (
    TenGodInterpretationBundle,
)
from engines.interpretation_engine.foundation.interpreters.useful_god.result import (
    UsefulGodInterpretationResult,
)
from engines.interpretation_engine.foundation.knowledge.bundle import (
    UsefulGodKnowledgeBundle,
)
from engines.interpretation_engine.foundation.knowledge.entity import KnowledgeEntity
from engines.interpretation_engine.foundation.knowledge.pattern_bundle import (
    PatternKnowledgeBundle,
)
from engines.interpretation_engine.foundation.knowledge.shensha_bundle import (
    ShenShaKnowledgeBundle,
)
from engines.interpretation_engine.foundation.knowledge.strength_bundle import (
    StrengthKnowledgeBundle,
)
from engines.interpretation_engine.foundation.knowledge.ten_god_bundle import (
    TenGodKnowledgeBundle,
)
from engines.interpretation_engine.foundation.narrative.collect import (
    copy_knowledge_entity,
    copy_mapping_recommendations,
    copy_mapping_warnings,
    copy_statement,
    extend_copied,
)
from engines.interpretation_engine.foundation.narrative.constants import (
    BUNDLE_KIND_DECISION,
    BUNDLE_KIND_KNOWLEDGE,
    BUNDLE_KIND_RELATIONSHIP,
    BUNDLE_KIND_STATE,
    CUSTOMER_DOMAIN_HEALTH,
    KIND_APPLICATION,
    KIND_CONCLUSION,
    KIND_EVIDENCE,
    KIND_FACT,
    KIND_REASON,
    KIND_RECOMMENDATION,
    KIND_WARNING,
    KIND_IMPORTANCE,
    SLOT_CONCLUSION,
    SLOT_IMPACT,
    SLOT_OBSERVATION,
    SLOT_REASONING,
    SLOT_RECOMMENDATION,
    SLOT_SUMMARY,
    SLOT_WARNING,
)
from engines.interpretation_engine.foundation.narrative.input import (
    DecisionBundle,
    KnowledgeBundle,
    NarrativeComposerInput,
    RelationshipBundle,
    StateBundle,
    CopiedStatement,
)
from engines.interpretation_engine.foundation.narrative.adapters_decision import (
    copy_decision_explanation,
    copy_useful_god_interpretation,
)
from engines.interpretation_engine.foundation.relationship.models import (
    RelationshipAssessment,
)

_KnowledgeSource = (
    UsefulGodKnowledgeBundle
    | StrengthKnowledgeBundle
    | PatternKnowledgeBundle
    | TenGodKnowledgeBundle
    | ShenShaKnowledgeBundle
)


def build_decision_bundle(
    *,
    domain: str,
    explanation: DecisionExplanationResult | None,
    interpretation: UsefulGodInterpretationResult | None,
) -> DecisionBundle:
    """Copy Decision Explanation and Useful God interpretation into one bundle."""
    selected = ""
    reason = ""
    confidence = 0.0
    refs: list[str] = []
    statements: list[CopiedStatement] = []
    if explanation is not None:
        selected, reason, confidence = copy_decision_explanation(
            explanation, statements, refs
        )
    if interpretation is not None:
        copy_useful_god_interpretation(interpretation, statements, refs)
        if interpretation.confidence and not confidence:
            confidence = interpretation.confidence
    return DecisionBundle(
        bundle_id=f"{BUNDLE_KIND_DECISION}:{domain}",
        domain=domain,
        selected=selected,
        reason=reason,
        confidence=confidence,
        importance=KIND_IMPORTANCE[BUNDLE_KIND_DECISION],
        statements=tuple(statements),
        engine_truth_refs=tuple(dict.fromkeys(refs)),
    )


def build_state_bundle(*, domain: str, assessment: StrengthAssessment) -> StateBundle:
    """Copy a Strength assessment. Score is not copied as a recommendation."""
    statements: list[CopiedStatement] = []
    refs: list[str] = list(assessment.rule_ids)
    prefix = f"state:{domain}"
    extend_copied(
        statements,
        copy_statement(
            assessment.state,
            kind=KIND_FACT,
            slot=SLOT_OBSERVATION,
            engine_truth_ref=f"{prefix}:state",
            confidence=assessment.confidence,
        ),
    )
    extend_copied(
        statements,
        copy_statement(
            assessment.label,
            kind=KIND_FACT,
            slot=SLOT_SUMMARY,
            engine_truth_ref=f"{prefix}:label",
            customer_domain=CUSTOMER_DOMAIN_HEALTH,
            confidence=assessment.confidence,
        ),
    )
    for step in assessment.assessment_path:
        extend_copied(
            statements,
            copy_statement(
                f"{step.title}={step.value}",
                kind=KIND_REASON,
                slot=SLOT_REASONING,
                engine_truth_ref=f"{prefix}:path:{step.step_id}",
                confidence=assessment.confidence,
            ),
        )
        refs.append(step.source)
    for index, item in enumerate(assessment.evidence):
        extend_copied(
            statements,
            copy_statement(
                item,
                kind=KIND_EVIDENCE,
                slot=SLOT_OBSERVATION,
                engine_truth_ref=f"{prefix}:evidence:{index}",
                confidence=assessment.confidence,
            ),
        )
    return StateBundle(
        bundle_id=f"{BUNDLE_KIND_STATE}:{domain}",
        domain=domain,
        state=assessment.state,
        label=assessment.label,
        confidence=assessment.confidence,
        importance=KIND_IMPORTANCE[BUNDLE_KIND_STATE],
        statements=tuple(statements),
        engine_truth_refs=tuple(dict.fromkeys(item for item in refs if item)),
    )


def build_relationship_bundle(
    *,
    domain: str,
    assessment: RelationshipAssessment,
    summary: Iterable[str] = (),
    reasoning: Iterable[str] = (),
    impacts: Iterable[str] = (),
    recommendations: Iterable[Mapping[str, Any]] = (),
    warnings: Iterable[Mapping[str, Any]] = (),
    conclusions: Iterable[str] = (),
) -> RelationshipBundle:
    """Copy a relationship assessment plus already-mapped narrative slots."""
    statements: list[CopiedStatement] = []
    refs: list[str] = list(assessment.rule_ids)
    prefix = f"relationship:{domain}"
    confidence = assessment.confidence
    for node in assessment.graph.nodes:
        extend_copied(
            statements,
            copy_statement(
                node.label or node.node_id,
                kind=KIND_FACT,
                slot=SLOT_OBSERVATION,
                engine_truth_ref=f"{prefix}:node:{node.node_id}",
                confidence=confidence,
            ),
        )
    for edge in assessment.graph.edges:
        extend_copied(
            statements,
            copy_statement(
                f"{edge.source}->{edge.relationship_type}->{edge.target}",
                kind=KIND_REASON,
                slot=SLOT_REASONING,
                engine_truth_ref=f"{prefix}:edge:{edge.edge_id}",
                confidence=edge.confidence or confidence,
            ),
        )
        refs.extend(edge.rule_ids)
    for item in assessment.evidence:
        extend_copied(
            statements,
            copy_statement(
                f"{item.fact}={item.value}" if item.value else item.fact,
                kind=KIND_EVIDENCE,
                slot=SLOT_OBSERVATION,
                engine_truth_ref=item.evidence_id or f"{prefix}:evidence:{item.rule_id}",
                confidence=item.confidence or confidence,
            ),
        )
        if item.rule_id:
            refs.append(item.rule_id)
    for item in assessment.meaning:
        extend_copied(
            statements,
            copy_statement(
                item.statement,
                kind=KIND_CONCLUSION,
                slot=SLOT_CONCLUSION,
                engine_truth_ref=f"{prefix}:meaning:{item.knowledge_key}",
                confidence=confidence,
            ),
        )
    for item in assessment.applications:
        extend_copied(
            statements,
            copy_statement(
                item.statement,
                kind=KIND_APPLICATION,
                slot=SLOT_IMPACT,
                engine_truth_ref=f"{prefix}:application:{item.area}",
                customer_domain=item.area,
                confidence=item.confidence or confidence,
            ),
        )
    for item in assessment.warnings:
        extend_copied(
            statements,
            copy_statement(
                item.risk,
                kind=KIND_WARNING,
                slot=SLOT_WARNING,
                engine_truth_ref=f"{prefix}:warning:{item.condition}",
                condition=item.condition,
                mitigation=item.mitigation,
                confidence=confidence,
            ),
        )
    for index, text in enumerate(summary):
        extend_copied(
            statements,
            copy_statement(
                text,
                kind=KIND_FACT,
                slot=SLOT_SUMMARY,
                engine_truth_ref=f"{prefix}:summary:{index}",
                confidence=confidence,
            ),
        )
    for index, text in enumerate(reasoning):
        extend_copied(
            statements,
            copy_statement(
                text,
                kind=KIND_REASON,
                slot=SLOT_REASONING,
                engine_truth_ref=f"{prefix}:reasoning:{index}",
                confidence=confidence,
            ),
        )
    for index, text in enumerate(impacts):
        area, statement = _split_impact(text)
        extend_copied(
            statements,
            copy_statement(
                statement,
                kind=KIND_APPLICATION,
                slot=SLOT_IMPACT,
                engine_truth_ref=f"{prefix}:impact:{index}",
                customer_domain=area,
                confidence=confidence,
            ),
        )
    statements.extend(
        copy_mapping_recommendations(
            recommendations, prefix=prefix, confidence=confidence
        )
    )
    statements.extend(
        copy_mapping_warnings(warnings, prefix=prefix, confidence=confidence)
    )
    for index, text in enumerate(conclusions):
        extend_copied(
            statements,
            copy_statement(
                text,
                kind=KIND_CONCLUSION,
                slot=SLOT_CONCLUSION,
                engine_truth_ref=f"{prefix}:interpretation:{index}",
                confidence=confidence,
            ),
        )
    return RelationshipBundle(
        bundle_id=f"{BUNDLE_KIND_RELATIONSHIP}:{domain}",
        domain=domain,
        confidence=confidence,
        importance=KIND_IMPORTANCE[BUNDLE_KIND_RELATIONSHIP],
        statements=tuple(statements),
        engine_truth_refs=tuple(dict.fromkeys(item for item in refs if item)),
    )


def build_knowledge_bundle(
    *,
    domain: str,
    entities: Iterable[KnowledgeEntity],
    confidence: float,
    extra_refs: Iterable[str] = (),
) -> KnowledgeBundle:
    """Copy knowledge entities. Composer does not look up or rewrite them."""
    entity_list = tuple(entities)
    statements: list[CopiedStatement] = []
    for entity in entity_list:
        extend_copied(
            statements,
            copy_statement(
                entity.title or entity.key,
                kind=KIND_FACT,
                slot=SLOT_OBSERVATION,
                engine_truth_ref=f"knowledge:{entity.domain}:{entity.key}:title",
                confidence=confidence,
            ),
        )
        statements.extend(copy_knowledge_entity(entity, confidence=confidence))
    keys = tuple(entity.key for entity in entity_list)
    refs = [entity.id for entity in entity_list]
    refs.extend(item for item in extra_refs if item)
    return KnowledgeBundle(
        bundle_id=f"{BUNDLE_KIND_KNOWLEDGE}:{domain}",
        domain=domain,
        entity_keys=keys,
        confidence=confidence,
        importance=KIND_IMPORTANCE[BUNDLE_KIND_KNOWLEDGE],
        statements=tuple(statements),
        engine_truth_refs=tuple(dict.fromkeys(refs)),
    )


def knowledge_bundle_from_source(
    source: _KnowledgeSource,
    *,
    domain: str,
    confidence: float,
) -> KnowledgeBundle:
    """Normalize any domain knowledge bundle into the frozen knowledge input."""
    entities = _entities_from_source(source)
    extra_refs: list[str] = []
    diagnostics = getattr(source, "diagnostics", ())
    extra_refs.extend(str(item) for item in diagnostics)
    return build_knowledge_bundle(
        domain=domain,
        entities=entities,
        confidence=confidence,
        extra_refs=extra_refs,
    )


def composer_input_from_domains(
    *,
    useful_god_explanation: DecisionExplanationResult | None,
    useful_god_interpretation: UsefulGodInterpretationResult | None,
    useful_god_knowledge: UsefulGodKnowledgeBundle | None,
    strength_assessment: StrengthAssessment | None,
    strength_knowledge: StrengthKnowledgeBundle | None,
    pattern_bundle: PatternInterpretationBundle | None,
    ten_god_bundle: TenGodInterpretationBundle | None,
    shensha_bundle: ShenShaInterpretationBundle | None,
) -> NarrativeComposerInput:
    """Assemble frozen composer input from already-built domain bundles."""
    decisions: list[DecisionBundle] = []
    states: list[StateBundle] = []
    relationships: list[RelationshipBundle] = []
    knowledge: list[KnowledgeBundle] = []
    if useful_god_explanation is not None or useful_god_interpretation is not None:
        decisions.append(
            build_decision_bundle(
                domain="UsefulGod",
                explanation=useful_god_explanation,
                interpretation=useful_god_interpretation,
            )
        )
    if useful_god_knowledge is not None:
        knowledge.append(
            knowledge_bundle_from_source(
                useful_god_knowledge,
                domain="UsefulGod",
                confidence=_bundle_confidence(useful_god_explanation),
            )
        )
    if strength_assessment is not None:
        states.append(build_state_bundle(domain="Strength", assessment=strength_assessment))
    if strength_knowledge is not None:
        knowledge.append(
            knowledge_bundle_from_source(
                strength_knowledge,
                domain="Strength",
                confidence=strength_assessment.confidence if strength_assessment else 0.0,
            )
        )
    _append_relationship_domain(relationships, knowledge, pattern_bundle, "Pattern")
    _append_relationship_domain(relationships, knowledge, ten_god_bundle, "TenGods")
    _append_relationship_domain(relationships, knowledge, shensha_bundle, "ShenSha")
    return NarrativeComposerInput(
        decision_bundles=tuple(decisions),
        state_bundles=tuple(states),
        relationship_bundles=tuple(relationships),
        knowledge_bundles=tuple(knowledge),
    )


def _append_relationship_domain(
    relationships: list[RelationshipBundle],
    knowledge: list[KnowledgeBundle],
    bundle: PatternInterpretationBundle
    | TenGodInterpretationBundle
    | ShenShaInterpretationBundle
    | None,
    domain: str,
) -> None:
    """Split one domain interpretation bundle into relationship + knowledge."""
    if bundle is None:
        return
    narrative = bundle.narrative
    relationships.append(
        build_relationship_bundle(
            domain=domain,
            assessment=bundle.relationship,
            summary=narrative.summary,
            reasoning=narrative.reasoning,
            impacts=narrative.impacts,
            recommendations=narrative.recommendations,
            warnings=narrative.warnings,
            conclusions=_interpretation_conclusions(bundle),
        )
    )
    knowledge.append(
        knowledge_bundle_from_source(
            bundle.knowledge,
            domain=domain,
            confidence=bundle.relationship.confidence,
        )
    )


def _entities_from_source(source: _KnowledgeSource) -> tuple[KnowledgeEntity, ...]:
    """Read entity fields already present on a knowledge bundle."""
    if isinstance(source, UsefulGodKnowledgeBundle):
        items = [
            source.selected_entity,
            *source.favorable_entities,
            *source.unfavorable_entities,
            *source.rejected_entities,
        ]
        return tuple(item for item in items if item is not None)
    if isinstance(source, StrengthKnowledgeBundle):
        return (source.state_entity,) if source.state_entity is not None else ()
    if isinstance(source, PatternKnowledgeBundle):
        return (source.pattern_entity,) if source.pattern_entity is not None else ()
    return tuple(source.entities)


def _bundle_confidence(explanation: DecisionExplanationResult | None) -> float:
    """Copy decision confidence when present."""
    if explanation is None:
        return 0.0
    if explanation.decision is not None:
        return explanation.decision.confidence
    return explanation.confidence


def _split_impact(text: str) -> tuple[str, str]:
    """Split `area:statement` narrative mapping without inventing a domain."""
    raw = str(text or "")
    if ":" not in raw:
        return "", raw
    area, statement = raw.split(":", 1)
    if ":" in statement and area not in {"career", "wealth", "relationships", "health", "learning", "decision_making", "environment"}:
        maybe_key, rest = statement.split(":", 1)
        if maybe_key in {"career", "wealth", "relationships", "health", "learning", "decision_making", "environment"}:
            return maybe_key, rest
    return area, statement


def _interpretation_conclusions(
    bundle: PatternInterpretationBundle
    | TenGodInterpretationBundle
    | ShenShaInterpretationBundle,
) -> tuple[str, ...]:
    """Copy already-validated interpretation meaning. Do not invent conclusions."""
    interpretation = bundle.interpretation
    items: list[str] = []
    structural = getattr(interpretation, "structural_meaning", "")
    if structural:
        items.append(str(structural))
    strengths = getattr(interpretation, "strengths", "")
    if strengths:
        items.append(str(strengths))
    for role in getattr(interpretation, "roles", ()):
        if getattr(role, "role_meaning", ""):
            items.append(str(role.role_meaning))
    for star in getattr(interpretation, "stars", ()):
        if getattr(star, "base_influence", ""):
            items.append(str(star.base_influence))
        elif getattr(star, "why_exists", ""):
            items.append(str(star.why_exists))
    return tuple(items)
