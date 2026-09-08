"""Compose Final Consulting Opinion from Language Pack + existing Recommendations."""

from __future__ import annotations

from consulting.language.models import LanguageCardWording
from consulting.language.renderer import compact_text
from consulting.marriage.narrative.catalog import action_entry
from consulting.marriage.narrative.input import NarrativeInput, RecommendationNarrativeInput
from consulting.marriage.report.customer_copy import customerize


def compose_final_opinion(payload: NarrativeInput) -> dict[str, str]:
    """Four customer sentences. No new Decision and no Recommendation ids."""
    cards = {item.question_id: item for item in payload.language_cards}
    q1 = cards.get("Q1")
    q2 = cards.get("Q2")
    q4 = cards.get("Q4")
    q6 = cards.get("Q6")
    return {
        "overall_opinion": _one_sentence((q6.headline if q6 else "") or _overall_fallback(payload)),
        "strongest_strength": _one_sentence(
            (q2.headline if q2 else "") or _first_fact(q2) or "Điểm mạnh nhất là khả năng bổ trợ đang có giữa hai người."
        ),
        "main_attention": _one_sentence(_attention(q4, q1)),
        "final_recommendation": _one_sentence(_recommendation(payload, q6)),
    }


def _attention(q4: LanguageCardWording | None, q1: LanguageCardWording | None) -> str:
    """One attention sentence from Q4 risk/facts or Q1 facts."""
    for card in (q4, q1):
        if card is None:
            continue
        for fact in card.supporting_facts:
            text = fact.replace("Rủi ro:", "").replace("Cứu giải:", "").strip()
            if text:
                return f"Điều cần lưu ý nhất là {text[0].lower() + text[1:]}" if text[0].isupper() else f"Điều cần lưu ý nhất là {text}"
    return "Điều cần lưu ý nhất là giữ quy ước rõ khi có khác biệt."


def _recommendation(payload: NarrativeInput, q6: LanguageCardWording | None) -> str:
    """Use existing Q6 guidance or B05 action wording. Never invent a new action."""
    if q6 and q6.quick_guidance:
        return q6.quick_guidance.replace("Gợi ý:", "").strip()
    rec = _first_action(payload.recommendations)
    if rec is not None:
        entry = action_entry(rec.action_type)
        if entry is not None:
            return compact_text(entry.action_bridge)
    if q6 and q6.meaning:
        return compact_text(q6.meaning).split(".")[0] + "."
    return "Nên dành thêm thời gian thống nhất cách sống trước khi đưa ra quyết định lâu dài."


def _first_action(items: list[RecommendationNarrativeInput]) -> RecommendationNarrativeInput | None:
    """First existing recommendation. Order is already Decision/Recommendation order."""
    return items[0] if items else None


def _first_fact(card: LanguageCardWording | None) -> str:
    """First bound Language Pack fact."""
    if card is None or not card.supporting_facts:
        return ""
    return card.supporting_facts[0]


def _overall_fallback(payload: NarrativeInput) -> str:
    """Q6 missing: use overall comparison long-term sentence if present."""
    if payload.overall_comparison and payload.overall_comparison.q6_text:
        return payload.overall_comparison.q6_text
    return "Đây là mối quan hệ cần đọc kèm phần đánh giá chi tiết."


def _one_sentence(text: str) -> str:
    """Keep a single customer sentence."""
    compact = compact_text(customerize(text))
    if not compact:
        return compact
    first = compact.split(". ")[0].strip()
    if first and not first.endswith("."):
        first += "."
    return first
