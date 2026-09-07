"""Compose customer Assessment Cards after Assessment and Recommendation exist.

Assessment owns semantic keys. Language Pack owns wording. Recommendation
owns action intent. This module only joins those siblings.
"""

from __future__ import annotations

from consulting.language.bindings.marriage import language_key_for
from consulting.language.catalog import load_validated_marriage_catalog
from consulting.language.models import LanguageCardWording, LanguageEntry, LanguageFactTemplate
from consulting.language.renderer import compact_text, fallback_card, fill_template, render_card
from consulting.language.selector import select_wording
from consulting.marriage.models.assessment import MarriageAssessmentCard
from consulting.marriage.models.comparison import MarriageComparisonFact
from consulting.marriage.models.enums import (
    ComparisonFactKind,
    MarriageDomain,
    RecommendationPriority,
    RecommendationType,
    RelationshipSubject,
)
from consulting.marriage.models.recommendation import MarriageRecommendation
from consulting.marriage.models.result import MarriageDecisionResult
from consulting.marriage.narrative.catalog import action_entry

_HOUR_LIMITATION = (
    "Giờ sinh chưa rõ nên một số nhận định liên quan trụ giờ được giữ ở mức tham khảo."
)
_MAX_FACTS = 4
_PRIORITY_RANK = {
    RecommendationPriority.CRITICAL: 0,
    RecommendationPriority.HIGH: 1,
    RecommendationPriority.MEDIUM: 2,
    RecommendationPriority.LOW: 3,
    RecommendationPriority.REFERENCE: 4,
}
_QUESTION_ACTIONS: dict[str, tuple[RecommendationType, ...]] = {
    "Q1": (
        RecommendationType.REDUCE_CONFLICT,
        RecommendationType.ROLE_BALANCE,
        RecommendationType.REINFORCE_STRENGTH,
        RecommendationType.FINANCIAL_STRUCTURE,
    ),
    "Q2": (
        RecommendationType.REINFORCE_STRENGTH,
        RecommendationType.ROLE_BALANCE,
        RecommendationType.REDUCE_CONFLICT,
    ),
    "Q3": (
        RecommendationType.ROLE_BALANCE,
        RecommendationType.REDUCE_CONFLICT,
    ),
    "Q4": (
        RecommendationType.REDUCE_CONFLICT,
        RecommendationType.FINANCIAL_STRUCTURE,
        RecommendationType.ROLE_BALANCE,
    ),
    "Q5": (RecommendationType.FAMILY_STRUCTURE,),
    "Q6": (
        RecommendationType.REDUCE_CONFLICT,
        RecommendationType.FINANCIAL_STRUCTURE,
        RecommendationType.ROLE_BALANCE,
        RecommendationType.REINFORCE_STRENGTH,
        RecommendationType.TIMING_AWARENESS,
    ),
}


def compose_customer_assessment_cards(
    result: MarriageDecisionResult,
    *,
    include_technical: bool = False,
) -> list[LanguageCardWording]:
    """Render six customer cards from Language Pack plus existing Recommendations."""
    catalog = load_validated_marriage_catalog()
    assessment = result.assessment
    if assessment is None:
        return []
    person_a = result.person_a.display_name or "Người A"
    person_b = result.person_b.display_name or "Người B"
    facts = list(result.comparison.facts) if result.comparison else []
    slots = {
        "person_a": person_a,
        "person_b": person_b,
        "person_offer": person_a,
        "person_need": person_b,
    }
    used_guidance: set[str] = set()
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
        bound = _bound_fact_rows(entry, card, result, facts, slots)
        wording = render_card(
            entry,
            selected,
            question_id=card.question_id,
            question=card.question,
            confidence=card.confidence,
            slots=slots,
            matched_fact_templates=[row[0] for row in bound],
            include_technical=include_technical,
        )
        wording.supporting_facts = [row[1] for row in bound]
        wording.fact_source_keys = [row[2] for row in bound]
        wording.limitations = _customer_limitations(entry, card, result, slots)
        _attach_guidance(wording, result.recommendations, used_guidance)
        cards.append(wording)
    return cards


def render_marriage_language_cards(
    result: MarriageDecisionResult,
    *,
    include_technical: bool = False,
) -> list[LanguageCardWording]:
    """Compatibility wrapper. Customer cards come from the Card Composer."""
    return compose_customer_assessment_cards(result, include_technical=include_technical)


def _semantic_signature(result: MarriageDecisionResult, card: MarriageAssessmentCard) -> str:
    """Deterministic selector input. Consultation id is not part of wording."""
    state = result.overall.state.value if result.overall.state else ""
    return f"{card.question_id}|{card.semantic_key}|{state}"


def _bound_fact_rows(
    entry: LanguageEntry,
    card: MarriageAssessmentCard,
    result: MarriageDecisionResult,
    facts: list[MarriageComparisonFact],
    slots: dict[str, str],
) -> list[tuple[LanguageFactTemplate, str, str]]:
    """Bind 2–4 strongest Language Pack facts that have a real Decision source."""
    ordered = _ordered_templates(entry, card.question_id)
    rows: list[tuple[LanguageFactTemplate, str, str]] = []
    seen: set[str] = set()
    for template in ordered:
        if not _template_applies(template, card, result, facts):
            continue
        text = fill_template(template.template, slots)
        if not text or text in seen:
            continue
        seen.add(text)
        source = template.source_fact or template.id
        rows.append((template, _label_fact(card.question_id, entry, template, text), source))
        if len(rows) >= _MAX_FACTS:
            break
    return rows


def _label_fact(
    question_id: str,
    entry: LanguageEntry,
    template: LanguageFactTemplate,
    text: str,
) -> str:
    """Q4 marks main risk and rescue. Labels only; wording stays from Language Pack."""
    if question_id != "Q4":
        return text
    risk_ids = {item.id for item in entry.main_risk_templates}
    rescue_ids = {item.id for item in entry.main_rescue_templates}
    if template.id in risk_ids and not text.startswith("Rủi ro"):
        return f"Rủi ro: {text}"
    if template.id in rescue_ids and not text.startswith("Cứu giải"):
        return f"Cứu giải: {text}"
    return text


def _ordered_templates(entry: LanguageEntry, question_id: str) -> list[LanguageFactTemplate]:
    """Question-specific fact order. Q2 directional. Q4 risk then rescue."""
    if question_id == "Q2":
        directional = [
            item
            for item in entry.supporting_fact_templates
            if (item.source_fact or "").endswith(("_a_to_b", "_b_to_a"))
            or item.id.startswith(("a_supports", "b_supports"))
        ]
        rest = [item for item in entry.supporting_fact_templates if item not in directional]
        return [*directional, *rest]
    if question_id == "Q4":
        return [
            *entry.main_risk_templates[:1],
            *entry.main_rescue_templates[:1],
            *entry.supporting_fact_templates,
        ]
    if question_id == "Q6":
        return list(entry.supporting_fact_templates)
    return list(entry.supporting_fact_templates)


def _template_applies(
    template: LanguageFactTemplate,
    card: MarriageAssessmentCard,
    result: MarriageDecisionResult,
    facts: list[MarriageComparisonFact],
) -> bool:
    """True when a Decision/Finding/condition justifies this catalog template."""
    source = template.source_fact or ""
    if not source:
        return False
    if source in {"children_domain_unavailable", "input_limitation"}:
        return "children_unsupported" in card.limitations or not _children_available(result)
    if source in {"decision_style_difference", "value_difference"} and card.semantic_key == "conflict":
        return True
    if source in {"insufficient_not_fertility_signal", "professional_review"}:
        return False
    if _comparison_binds(source, facts, result):
        return True
    return False


def _comparison_binds(
    source: str,
    facts: list[MarriageComparisonFact],
    result: MarriageDecisionResult,
) -> bool:
    """Match a catalog source_fact onto comparison facts or overall state."""
    kinds = {item.kind for item in facts}
    domains = {item.domain for item in facts}
    overall = result.overall.state.value if result.overall.state else ""
    for fact in facts:
        if fact.template_key == source:
            return True
        if source == f"{fact.template_key}_a_to_b" and fact.subject is RelationshipSubject.A_TO_B:
            return True
        if source == f"{fact.template_key}_b_to_a" and fact.subject is RelationshipSubject.B_TO_A:
            return True
        if source in {"directional_support", "directional_support_present"} and fact.kind is ComparisonFactKind.SUPPORT:
            return True
        if source in {
            "mixed_support",
            "support_outweighs_conflict",
            "mutual_support",
            "support_present",
            "support_stronger_than_conflict",
            "rescue_exists",
        } and fact.kind is ComparisonFactKind.SUPPORT:
            return True
        if source in {"mixed_conflict", "mixed_pressure", "main_conflict", "conflict_manageable"} and fact.kind is ComparisonFactKind.CONFLICT:
            return True
        if source in {"rescue_present", "main_rescue", "rescue_partial"} and fact.kind is ComparisonFactKind.RESCUE:
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
        if source in {"communication_difference", "finance_difference"} and fact.domain in {
            MarriageDomain.FINANCE,
            MarriageDomain.INTERACTION,
            MarriageDomain.STEM_BRANCH,
        }:
            return True
        if source in {"rescue_day_master", "rescue_useful_god"} and fact.kind is ComparisonFactKind.RESCUE:
            return True
        if source == "balanced_roles" and fact.domain is MarriageDomain.TEN_GODS:
            return True
    if source in {"compatibility_acceptable", "compatibility_good"} and overall in {
        "mixed",
        "balanced",
        "supportive",
    }:
        return True
    if source == "personality_balance" and MarriageDomain.TEN_GODS in domains:
        return True
    if source == "stability_good" and ComparisonFactKind.RESCUE in kinds:
        return True
    if source == "finance_support" and MarriageDomain.FINANCE in domains:
        return True
    return False


def _children_available(result: MarriageDecisionResult) -> bool:
    """True when the Children comparison domain is published."""
    comparison = result.comparison
    return bool(comparison and comparison.children.available)


def _customer_limitations(
    entry: LanguageEntry,
    card: MarriageAssessmentCard,
    result: MarriageDecisionResult,
    slots: dict[str, str],
) -> list[str]:
    """Show data limitations only. Never Assessment prose such as Insufficient."""
    items: list[str] = []
    hour_missing = not (
        result.person_a.birth_data_quality.birth_time_known
        and result.person_b.birth_data_quality.birth_time_known
    )
    if hour_missing:
        items.append(_HOUR_LIMITATION)
    if card.question_id == "Q5" and "children_unsupported" in card.limitations:
        for template in entry.limitation_templates:
            if template.source_fact == "insufficient_not_fertility_signal":
                text = fill_template(template.template, slots)
                if text:
                    items.append(text)
                break
    seen: set[str] = set()
    unique: list[str] = []
    for item in items:
        if item and item not in seen:
            seen.add(item)
            unique.append(item)
    return unique[:2]


def _attach_guidance(
    card: LanguageCardWording,
    recommendations: list[MarriageRecommendation],
    used: set[str],
) -> None:
    """Attach one existing Recommendation in approved B05 action wording."""
    preferred = _QUESTION_ACTIONS.get(card.question_id, ())
    selected = _select_recommendation(recommendations, preferred, used)
    if selected is None:
        return
    catalog = action_entry(selected.action_type)
    if catalog is None:
        return
    text = compact_text(catalog.action_bridge)
    if not text:
        return
    if not text.casefold().startswith("gợi ý"):
        text = f"Gợi ý: {text}"
    card.quick_guidance = text
    card.quick_guidance_recommendation_id = selected.recommendation_id
    card.quick_guidance_action_type = selected.action_type.value
    used.add(selected.recommendation_id)


def _select_recommendation(
    recommendations: list[MarriageRecommendation],
    preferred: tuple[RecommendationType, ...],
    used: set[str],
) -> MarriageRecommendation | None:
    """Pick the highest existing Recommendation for this question. No fabrication."""
    if not preferred:
        return None
    matching = [item for item in recommendations if item.action_type in preferred]
    if not matching:
        return None
    unused = [item for item in matching if item.recommendation_id not in used]
    pool = unused or matching

    def _rank(item: MarriageRecommendation) -> tuple[int, int, str]:
        pref = preferred.index(item.action_type) if item.action_type in preferred else 99
        priority = _PRIORITY_RANK.get(item.action_priority or RecommendationPriority.LOW, 9)
        return pref, priority, item.recommendation_id

    return sorted(pool, key=_rank)[0]
