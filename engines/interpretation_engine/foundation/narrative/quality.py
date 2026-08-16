"""Customer narrative quality gates and product metrics."""

from __future__ import annotations

import re

from engines.interpretation_engine.foundation.narrative.constants import (
    COMMERCIAL_RECOMMENDATION_LIMIT,
    CUSTOMER_DOMAIN_LABELS,
    NARRATIVE_SECTIONS,
    SECTION_CONCLUSION,
    SECTION_IMPACT,
    SECTION_REASONING,
    SECTION_RECOMMENDATION,
    SECTION_WARNING,
)
from engines.interpretation_engine.foundation.narrative.models import (
    ComposerMetrics,
    NarrativeComposerResult,
)
from engines.interpretation_engine.foundation.narrative.relevance import (
    is_hypothetical_role_leak,
)
from engines.interpretation_engine.foundation.narrative.input import ChartFocus
from engines.interpretation_engine.foundation.narrative.text import (
    fingerprint,
    implementation_language_hits,
    is_broken_fragment,
    normalize_text,
)
from engines.interpretation_engine.foundation.narrative.translation.models import (
    ExpertTranslationError,
)
from engines.interpretation_engine.foundation.narrative.translation.validator import (
    find_forbidden_terms,
)

_WORD = re.compile(r"\S+")


def assert_customer_narrative_quality(
    result: NarrativeComposerResult,
    *,
    focus: ChartFocus | None = None,
) -> None:
    """Fail customer composition that still looks like an internal export."""
    blob = _customer_blob(result)
    broken = broken_fragment_count(result)
    if broken:
        raise ExpertTranslationError(
            f"narrative contains {broken} broken fragment(s)"
        )
    impl = implementation_language_count(result)
    if impl:
        hits = find_forbidden_terms(blob) or implementation_language_hits(blob)
        preview = "; ".join(hits[:8]) if hits else "implementation term"
        raise ExpertTranslationError(
            f"narrative contains implementation language: {preview}"
        )
    leaks = hypothetical_knowledge_leak_count(result, focus)
    if leaks:
        raise ExpertTranslationError(
            f"narrative contains {leaks} hypothetical role leak(s)"
        )
    rec_section = result.section(SECTION_RECOMMENDATION)
    rec_count = len(rec_section.sentences) if rec_section else 0
    if rec_count > COMMERCIAL_RECOMMENDATION_LIMIT:
        raise ExpertTranslationError(
            f"recommendation count {rec_count} exceeds commercial limit"
        )
    if _duplicate_recommendation_block(result):
        raise ExpertTranslationError("duplicate recommendation block")


def customer_quality_metrics(
    *,
    result: NarrativeComposerResult,
    focus: ChartFocus | None,
    base: ComposerMetrics,
) -> ComposerMetrics:
    """Attach customer-facing quality metrics onto composer metrics."""
    blob = _customer_blob(result)
    words = len(_WORD.findall(blob))
    rec_section = result.section(SECTION_RECOMMENDATION)
    rec_count = len(rec_section.sentences) if rec_section else 0
    impact = result.section(SECTION_IMPACT)
    domain_count = len(impact.sentences) if impact else 0
    return ComposerMetrics(
        evidence_coverage=base.evidence_coverage,
        duplicate_ratio=base.duplicate_ratio,
        reason_coverage=base.reason_coverage,
        recommendation_coverage=base.recommendation_coverage,
        warning_coverage=base.warning_coverage,
        traceability_coverage=base.traceability_coverage,
        evidence_count=base.evidence_count,
        sentence_count=base.sentence_count,
        orphan_sentence_count=base.orphan_sentence_count,
        customer_relevance_ratio=_customer_relevance_ratio(result, focus),
        active_chart_fact_ratio=_active_chart_fact_ratio(result, focus),
        hypothetical_knowledge_leak_count=hypothetical_knowledge_leak_count(
            result, focus
        ),
        duplicate_section_ratio=duplicate_section_ratio(result),
        broken_fragment_count=broken_fragment_count(result),
        implementation_language_count=implementation_language_count(result),
        recommendation_count=rec_count,
        priority_recommendation_count=min(rec_count, COMMERCIAL_RECOMMENDATION_LIMIT),
        domain_paragraph_count=domain_count,
        customer_narrative_word_count=words,
    )


def broken_fragment_count(result: NarrativeComposerResult) -> int:
    """Count empty or truncated fragments in rendered sentences."""
    return sum(
        1
        for sentence in _sentences(result)
        if is_broken_fragment(sentence.text)
    )


def implementation_language_count(result: NarrativeComposerResult) -> int:
    """Count rendered sentences that still leak implementation terms."""
    count = 0
    for sentence in _sentences(result):
        if find_forbidden_terms(sentence.text) or implementation_language_hits(
            sentence.text
        ):
            count += 1
    return count


def hypothetical_knowledge_leak_count(
    result: NarrativeComposerResult,
    focus: ChartFocus | None,
) -> int:
    """Count hypothetical Dụng/Hỷ/Kỵ sentences that do not match this chart."""
    if focus is None:
        return 0
    return sum(
        1
        for sentence in _sentences(result)
        if is_hypothetical_role_leak(sentence.text, focus)
    )


def duplicate_section_ratio(result: NarrativeComposerResult) -> float:
    """Share of later-section sentences that reprint earlier fingerprints."""
    seen: set[str] = set()
    reused = 0
    total = 0
    for name in NARRATIVE_SECTIONS:
        section = result.section(name)
        if section is None:
            continue
        for sentence in section.sentences:
            mark = fingerprint(sentence.text)
            if not mark:
                continue
            total += 1
            if name in {
                SECTION_IMPACT,
                SECTION_RECOMMENDATION,
                SECTION_WARNING,
                SECTION_CONCLUSION,
            } and mark in seen:
                reused += 1
            seen.add(mark)
    if total <= 0:
        return 0.0
    return reused / total


def _duplicate_recommendation_block(result: NarrativeComposerResult) -> bool:
    """True when the recommendation section reprints the same ranked block."""
    section = result.section(SECTION_RECOMMENDATION)
    if section is None or len(section.sentences) < 2:
        return False
    marks = [fingerprint(item.text) for item in section.sentences]
    return len(marks) != len(set(marks))


def _customer_relevance_ratio(
    result: NarrativeComposerResult,
    focus: ChartFocus | None,
) -> float:
    """Share of rendered sentences that mention an active chart fact."""
    sentences = list(_sentences(result))
    if not sentences:
        return 1.0
    if focus is None or not focus.active_names():
        return 1.0
    names = tuple(name for name in focus.active_names() if name)
    hits = 0
    for sentence in sentences:
        text = sentence.text
        if any(name in text for name in names):
            hits += 1
            continue
        if sentence.section in {SECTION_IMPACT, SECTION_RECOMMENDATION, SECTION_WARNING}:
            hits += 1
    return min(hits / len(sentences), 1.0)


def _active_chart_fact_ratio(
    result: NarrativeComposerResult,
    focus: ChartFocus | None,
) -> float:
    """Share of governing facts that appear in customer narrative."""
    if focus is None:
        return 1.0
    required = [
        item
        for item in (focus.selected, focus.pattern_label, focus.strength_label)
        if item
    ]
    if not required:
        return 1.0
    blob = _customer_blob(result)
    found = sum(1 for item in required if item in blob)
    return found / len(required)


def _customer_blob(result: NarrativeComposerResult) -> str:
    """Join rendered customer sentences."""
    return " ".join(sentence.text for sentence in _sentences(result))


def _sentences(result: NarrativeComposerResult):
    """Iterate rendered sentences in canonical section order."""
    for section in result.sections:
        yield from section.sentences


def ranked_recommendation_text(index: int, action: str) -> str:
    """Prefix a customer recommendation with a commercial rank."""
    return f"{index}. {normalize_text(action)}"


def domain_heading(domain: str) -> str:
    """Vietnamese customer heading for one life area. Not an English tag."""
    return CUSTOMER_DOMAIN_LABELS.get(domain, "")
