"""Apply expert translation to composer input. Preserve ids and decisions."""

from __future__ import annotations

from engines.interpretation_engine.foundation.narrative.input import (
    CopiedStatement,
    DecisionBundle,
    KnowledgeBundle,
    NarrativeComposerInput,
    RelationshipBundle,
    StateBundle,
)
from engines.interpretation_engine.foundation.narrative.translation.translator import (
    translate_text,
)


def apply_expert_translation(
    source: NarrativeComposerInput,
    *,
    debug_mode: bool = False,
) -> NarrativeComposerInput:
    """Translate customer-facing text. Decisions and references stay intact."""
    if debug_mode:
        return source
    return NarrativeComposerInput(
        decision_bundles=tuple(
            _translate_decision(item, debug_mode=debug_mode)
            for item in source.decision_bundles
        ),
        state_bundles=tuple(
            _translate_state(item, debug_mode=debug_mode)
            for item in source.state_bundles
        ),
        relationship_bundles=tuple(
            _translate_relationship(item, debug_mode=debug_mode)
            for item in source.relationship_bundles
        ),
        knowledge_bundles=tuple(
            _translate_knowledge(item, debug_mode=debug_mode)
            for item in source.knowledge_bundles
        ),
        chart_focus=source.chart_focus,
    )


def _translate_decision(
    bundle: DecisionBundle,
    *,
    debug_mode: bool,
) -> DecisionBundle:
    """Translate decision statements. Keep selected value unchanged."""
    return DecisionBundle(
        bundle_id=bundle.bundle_id,
        domain=bundle.domain,
        selected=bundle.selected,
        reason=translate_text(bundle.reason, debug_mode=debug_mode),
        confidence=bundle.confidence,
        importance=bundle.importance,
        statements=_translate_statements(bundle.statements, debug_mode=debug_mode),
        engine_truth_refs=bundle.engine_truth_refs,
    )


def _translate_state(bundle: StateBundle, *, debug_mode: bool) -> StateBundle:
    """Translate state statements. Keep classified state unchanged."""
    return StateBundle(
        bundle_id=bundle.bundle_id,
        domain=bundle.domain,
        state=bundle.state,
        label=bundle.label,
        confidence=bundle.confidence,
        importance=bundle.importance,
        statements=_translate_statements(bundle.statements, debug_mode=debug_mode),
        engine_truth_refs=bundle.engine_truth_refs,
    )


def _translate_relationship(
    bundle: RelationshipBundle,
    *,
    debug_mode: bool,
) -> RelationshipBundle:
    """Translate relationship statements. Keep graph identity unchanged."""
    return RelationshipBundle(
        bundle_id=bundle.bundle_id,
        domain=bundle.domain,
        confidence=bundle.confidence,
        importance=bundle.importance,
        statements=_translate_statements(bundle.statements, debug_mode=debug_mode),
        engine_truth_refs=bundle.engine_truth_refs,
    )


def _translate_knowledge(
    bundle: KnowledgeBundle,
    *,
    debug_mode: bool,
) -> KnowledgeBundle:
    """Translate knowledge statements. Keep entity keys unchanged."""
    return KnowledgeBundle(
        bundle_id=bundle.bundle_id,
        domain=bundle.domain,
        entity_keys=bundle.entity_keys,
        confidence=bundle.confidence,
        importance=bundle.importance,
        statements=_translate_statements(bundle.statements, debug_mode=debug_mode),
        engine_truth_refs=bundle.engine_truth_refs,
    )


def _translate_statements(
    statements: tuple[CopiedStatement, ...],
    *,
    debug_mode: bool,
) -> tuple[CopiedStatement, ...]:
    """Translate copied prose fields only."""
    return tuple(
        CopiedStatement(
            text=translate_text(item.text, debug_mode=debug_mode),
            kind=item.kind,
            slot=item.slot,
            engine_truth_ref=item.engine_truth_ref,
            customer_domain=item.customer_domain,
            category=item.category,
            rationale=translate_text(item.rationale, debug_mode=debug_mode),
            condition=translate_text(item.condition, debug_mode=debug_mode),
            mitigation=translate_text(item.mitigation, debug_mode=debug_mode),
            confidence=item.confidence,
        )
        for item in statements
    )
