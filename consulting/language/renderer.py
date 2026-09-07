"""Language Pack renderer. Slot fill + template bind. No LLM. No Assessment mutation."""

from __future__ import annotations

import logging
import re

from consulting.language.models import (
    LanguageCardWording,
    LanguageEntry,
    LanguageFactTemplate,
    SelectedWording,
)
from consulting.language.versions import (
    FALLBACK_HEADLINE,
    FALLBACK_MEANING,
    MAX_LIMITATIONS,
    MAX_SUPPORTING_FACTS,
)

_LOG = logging.getLogger("consulting.language")
_SLOT = re.compile(r"\{([a-z0-9_]+)\}")
_ID_LEAK = re.compile(r"\b(?:EV|F|RC|CF)-\d{4}\b")


def compact_text(text: str) -> str:
    """Collapse YAML folded whitespace into one customer paragraph."""
    return " ".join(text.split()).strip()


def fill_template(template: str, slots: dict[str, str]) -> str:
    """Substitute known slots. Unknown slots stay empty rather than crashing."""

    def _replace(match: re.Match[str]) -> str:
        return slots.get(match.group(1), "")

    return compact_text(_SLOT.sub(_replace, template))


def fallback_card(
    *,
    question_id: str,
    question: str,
    semantic_key: str,
    confidence: str,
) -> LanguageCardWording:
    """Controlled missing-key wording. Logs LANGUAGE_KEY_NOT_FOUND. Does not crash."""
    _LOG.warning("LANGUAGE_KEY_NOT_FOUND question_id=%s semantic_key=%s", question_id, semantic_key)
    return LanguageCardWording(
        question_id=question_id,
        question=question,
        language_key="",
        headline=FALLBACK_HEADLINE,
        meaning=FALLBACK_MEANING,
        supporting_facts=[],
        limitations=[],
        closing="",
        technical_explanation="",
        variant_id="fallback",
        confidence=confidence,
        fallback=True,
    )


def render_card(
    entry: LanguageEntry,
    selected: SelectedWording,
    *,
    question_id: str,
    question: str,
    confidence: str,
    slots: dict[str, str],
    matched_fact_templates: list[LanguageFactTemplate],
    include_technical: bool,
) -> LanguageCardWording:
    """Compose one Assessment Card from a catalog entry and bound templates."""
    facts = [
        text
        for text in (fill_template(item.template, slots) for item in matched_fact_templates)
        if text and not _ID_LEAK.search(text)
    ][:MAX_SUPPORTING_FACTS]
    limits = [
        text
        for text in (fill_template(item.template, slots) for item in entry.limitation_templates)
        if text and not _ID_LEAK.search(text)
    ][:MAX_LIMITATIONS]
    return LanguageCardWording(
        question_id=question_id,
        question=question,
        language_key=entry.language_key,
        headline=compact_text(selected.headline or entry.headline),
        meaning=compact_text(selected.meaning or entry.meaning or entry.plain_customer_text),
        supporting_facts=facts,
        limitations=limits,
        closing=compact_text(entry.closing),
        technical_explanation=compact_text(entry.technical_explanation) if include_technical else "",
        variant_id=selected.variant_id,
        confidence=confidence,
        fallback=False,
    )
