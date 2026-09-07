"""TV-01 Language Pack render seam. Wording only. Does not change Assessment."""

from __future__ import annotations

from consulting.language.bindings.marriage import language_key_for
from consulting.language.catalog import load_validated_marriage_catalog
from consulting.language.models import LanguageCardWording, LanguageEntry, LanguageFactTemplate
from consulting.language.renderer import fallback_card, render_card
from consulting.language.selector import select_wording
from consulting.marriage.models.assessment import MarriageAssessmentCard
from consulting.marriage.models.comparison import MarriageComparisonFact
from consulting.marriage.models.enums import ComparisonFactKind, RelationshipSubject
from consulting.marriage.models.result import MarriageDecisionResult


def render_marriage_language_cards(
    result: MarriageDecisionResult,
    *,
    include_technical: bool = False,
) -> list[LanguageCardWording]:
    """Render six Assessment Cards from the approved Marriage catalog."""
    catalog = load_validated_marriage_catalog()
    assessment = result.assessment
    if assessment is None:
        return []
    person_a = result.person_a.display_name or "Người A"
    person_b = result.person_b.display_name or "Người B"
    facts = list(result.comparison.facts) if result.comparison else []
    cards: list[LanguageCardWording] = []
    for card in assessment.cards:
        key = language_key_for(card.question_id, card.semantic_key)
        entry = catalog.entries_by_key.get(key or "")
        if entry is None:
            cards.append(
                fallback_card(
                    question_id=card.question_id,
                    question=card.question,
                    semantic_key=card.semantic_key,
                    confidence=card.confidence,
                )
            )
            continue
        selected = select_wording(
            entry,
            semantic_signature=_semantic_signature(result, card),
            catalog_version=catalog.catalog_version,
        )
        slots = {
            "person_a": person_a,
            "person_b": person_b,
            "person_offer": person_a,
            "person_need": person_b,
        }
        cards.append(
            render_card(
                entry,
                selected,
                question_id=card.question_id,
                question=card.question,
                confidence=card.confidence,
                slots=slots,
                matched_fact_templates=_bound_templates(entry, facts),
                include_technical=include_technical,
            )
        )
    return cards


def _semantic_signature(result: MarriageDecisionResult, card: MarriageAssessmentCard) -> str:
    """Deterministic selector input. Consultation id is not part of wording."""
    state = result.overall.state.value if result.overall.state else ""
    return f"{card.question_id}|{card.semantic_key}|{state}"


def _bound_templates(
    entry: LanguageEntry,
    facts: list[MarriageComparisonFact],
) -> list[LanguageFactTemplate]:
    """Keep templates whose source_fact binds a Decision comparison fact."""
    return [template for template in entry.supporting_fact_templates if _template_binds(template, facts)]


def _template_binds(template: LanguageFactTemplate, facts: list[MarriageComparisonFact]) -> bool:
    """True when a comparison fact justifies this catalog template."""
    source = template.source_fact or ""
    if not source:
        return False
    for fact in facts:
        if fact.template_key == source:
            return True
        if source == f"{fact.template_key}_a_to_b" and fact.subject is RelationshipSubject.A_TO_B:
            return True
        if source == f"{fact.template_key}_b_to_a" and fact.subject is RelationshipSubject.B_TO_A:
            return True
        if source == "directional_support" and fact.kind is ComparisonFactKind.SUPPORT:
            return True
        if source in {"mixed_support", "support_outweighs_conflict"} and fact.kind is ComparisonFactKind.SUPPORT:
            return True
        if source in {"rescue_present", "main_rescue"} and fact.kind is ComparisonFactKind.RESCUE:
            return True
        if source in {"main_conflict", "mixed_pressure"} and fact.kind is ComparisonFactKind.CONFLICT:
            return True
        if source == "mutual_favorable_support" and fact.template_key == "favorable_support":
            return True
        if source == "mutual_role_support" and fact.template_key in {"role_support", "role_pressure"}:
            return True
        if source in {"same_day_master", "similar_role_structure"} and fact.domain.value in {
            "ten_gods",
            "five_elements",
        }:
            return True
    return False
