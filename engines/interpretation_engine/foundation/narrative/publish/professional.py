"""Professional Report Publisher — edition policy over the same Narrative."""

from __future__ import annotations

from typing import Any

from engines.interpretation_engine.foundation.narrative.constants import (
    CUSTOMER_DOMAIN_CAREER,
    CUSTOMER_DOMAIN_DECISION,
    CUSTOMER_DOMAIN_ENVIRONMENT,
    CUSTOMER_DOMAIN_FINANCE,
    CUSTOMER_DOMAIN_HEALTH,
    CUSTOMER_DOMAIN_LABELS,
    CUSTOMER_DOMAIN_LEARNING,
    CUSTOMER_DOMAIN_RELATIONSHIP,
    KIND_CONCLUSION,
    KIND_FACT,
    KIND_REASON,
    KIND_RECOMMENDATION,
    KIND_WARNING,
)
from engines.interpretation_engine.foundation.narrative.publish.builder import (
    _chart_names_from_payload,
    _paragraph_text,
    _same_meaning,
    _thesis_from_payload,
)
from engines.interpretation_engine.foundation.narrative.publish.criteria import (
    classify_node,
    word_count,
)
from engines.interpretation_engine.foundation.narrative.publish.constants import (
    CHART_FACT_PREFIXES,
    DECISION_APPENDIX,
    DECISION_DROP,
    DECISION_PUBLISH,
)
from engines.interpretation_engine.foundation.narrative.publish.current_dayun import (
    assemble_current_dayun_consultation,
)
from engines.interpretation_engine.foundation.narrative.publish.luck_analysis_copy import (
    career_overlay_from_analysis,
    conclusion_overlay_from_analysis,
    finance_overlay_from_analysis,
    health_overlay_from_analysis,
    luck_analysis_from_payload,
    recommendation_overlay_from_analysis,
    relationship_overlay_from_analysis,
)
from engines.interpretation_engine.foundation.narrative.publish.editions import (
    APPENDIX_LIMIT,
    APPENDIX_SECTION_ID,
    APPENDIX_TITLE,
    CAREER_MARKERS,
    CORE_DOMAINS,
    EDITION_APPENDIX,
    EDITION_EXECUTIVE,
    EDITION_PROFESSIONAL,
    LUCK_MARKERS,
    MIN_CONSULTING_WORDS,
    MIN_ROLE_WHY_WORDS,
    PROFESSIONAL_PAGE_ORDER,
    PROFESSIONAL_PAGE_TITLES,
    PROFESSIONAL_REPORT_PUBLISHER_ID,
    PROFESSIONAL_SECTION_LIMITS,
    ROLE_WHY_MARKERS,
    SHEN_SHA_DOMAIN,
    TEN_GOD_DOMAIN,
)
from engines.interpretation_engine.foundation.narrative.text import normalize_text

_LIFE_AREA_DOMAINS: tuple[str, ...] = (
    CUSTOMER_DOMAIN_FINANCE,
    CUSTOMER_DOMAIN_RELATIONSHIP,
    CUSTOMER_DOMAIN_HEALTH,
    CUSTOMER_DOMAIN_LEARNING,
)


class ProfessionalReportPublisher:
    """Publish one Narrative into Executive, Professional, or Appendix editions."""

    def apply(self, payload: dict[str, Any], edition: str) -> dict[str, Any]:
        """Return an edition payload. Never mutates composer internals in place."""
        if not isinstance(payload, dict):
            return payload
        target = _normalize_edition(edition)
        current = _payload_edition(payload)
        if current == target:
            return payload
        if target == EDITION_EXECUTIVE:
            return payload
        if target == EDITION_APPENDIX:
            return _apply_appendix(payload)
        return _apply_professional(payload)


def apply_report_edition(payload: dict[str, Any], edition: str) -> dict[str, Any]:
    """Public entry: select a publication edition of the same Narrative."""
    if not isinstance(payload, dict):
        return payload
    sections = payload.get("sections")
    if not isinstance(sections, list) or not sections:
        return payload
    return ProfessionalReportPublisher().apply(payload, edition)


def publication_edition_of(payload: dict[str, Any] | None) -> str:
    """Read the edition already stamped on a NarrativeResult payload."""
    return _payload_edition(payload or {})


def _apply_professional(payload: dict[str, Any]) -> dict[str, Any]:
    """Build the professional consultation from published spine + evidence."""
    thesis = _thesis_from_payload(payload)
    chart_names = _chart_names_from_payload(payload)
    published = _published_texts_by_section(payload)
    exec_texts = list(published.get("sec-executive_summary") or [])
    evidence = _evidence_candidates(payload, thesis, chart_names)
    used: list[str] = list(exec_texts)
    chart = _select_chart(published, evidence, [])
    core = _select_core(published, evidence, used)
    used = used + core
    ten_gods = _select_ten_gods(evidence, used)
    used = used + ten_gods
    shen_sha = _select_shen_sha(evidence, used)
    used = used + shen_sha
    luck = _select_luck(
        payload,
        published,
        evidence,
        [text for text in used if not _has_marker(text, LUCK_MARKERS)],
    )
    used = used + luck
    natal_used = _without_period_copy(used)
    career = _select_career(payload, published, evidence, natal_used)
    used = used + career
    life_areas = _select_life_areas(payload, published, evidence, natal_used)
    used = used + life_areas
    recommendations = _select_recommendations(
        payload,
        published,
        evidence,
        natal_used + _without_period_copy(career + life_areas),
    )
    pages = {
        "sec-executive_summary": _limit(exec_texts, "sec-executive_summary"),
        "sec-chart": chart,
        "sec-core_interpretation": core,
        "sec-ten_gods": ten_gods,
        "sec-shen_sha": shen_sha,
        "sec-luck": luck,
        "sec-career": career,
        "sec-life_areas": life_areas,
        "sec-professional_recommendation": recommendations,
        "sec-professional_conclusion": _select_conclusion(
            payload,
            published,
            natal_used,
        ),
    }
    sections = [
        _section_payload(section_id, pages.get(section_id) or [])
        for section_id in PROFESSIONAL_PAGE_ORDER
        if pages.get(section_id)
    ]
    out = dict(payload)
    out["sections"] = sections
    out["recommendations"] = _recommendation_records(
        pages.get("sec-professional_recommendation") or []
    )
    out["metadata"] = _edition_metadata(
        payload,
        edition=EDITION_PROFESSIONAL,
        sections=sections,
        appendix_count=_appendix_count(payload, thesis, chart_names),
    )
    return out


def _apply_appendix(payload: dict[str, Any]) -> dict[str, Any]:
    """Technical appendix only. Never mixed into the consultation spine."""
    thesis = _thesis_from_payload(payload)
    chart_names = _chart_names_from_payload(payload)
    texts = _unique(
        [
            item.text
            for item in _iter_evidence(payload)
            if _appendix_allowed(item, thesis, chart_names)
        ],
        [],
        APPENDIX_LIMIT,
    )
    sections = [_section_payload(APPENDIX_SECTION_ID, texts, title=APPENDIX_TITLE)]
    out = dict(payload)
    out["sections"] = sections
    out["recommendations"] = []
    out["metadata"] = _edition_metadata(
        payload,
        edition=EDITION_APPENDIX,
        sections=sections,
        appendix_count=len(texts),
    )
    return out


def _select_chart(
    published: dict[str, list[str]],
    evidence: list["_Evidence"],
    exclude: list[str],
) -> list[str]:
    """Page 2 — chart facts already composed. No encyclopedia."""
    facts = [
        text
        for text in published.get("sec-observation") or []
        if _is_chart_fact(text) or word_count(text) <= 12
    ]
    extra = [
        item.text
        for item in evidence
        if item.kind == KIND_FACT and _is_chart_fact(item.text)
    ]
    return _unique(facts + extra, exclude, PROFESSIONAL_SECTION_LIMITS["sec-chart"])


def _select_core(
    published: dict[str, list[str]],
    evidence: list["_Evidence"],
    exclude: list[str],
) -> list[str]:
    """Page 3 — deepen the thesis. Do not repeat Executive Summary."""
    blocked = list(exclude) + list(published.get("sec-executive_summary") or [])
    from_spine = [
        text
        for text in published.get("sec-reasoning") or []
        if word_count(text) >= MIN_CONSULTING_WORDS and not _is_chart_fact(text)
    ]
    from_evidence = [
        item.text
        for item in evidence
        if item.domain in CORE_DOMAINS
        and item.kind in {KIND_REASON, KIND_CONCLUSION}
        and word_count(item.text) >= MIN_CONSULTING_WORDS
        and not _is_chart_fact(item.text)
    ]
    return _unique(
        from_spine + from_evidence,
        blocked,
        PROFESSIONAL_SECTION_LIMITS["sec-core_interpretation"],
    )


def _select_ten_gods(evidence: list["_Evidence"], exclude: list[str]) -> list[str]:
    """Page 4 — chart-relevant roles. Why this role matters here."""
    chosen = [
        item.text
        for item in evidence
        if item.domain in {TEN_GOD_DOMAIN, "UsefulGod"}
        and item.kind in {KIND_REASON, KIND_CONCLUSION}
        and word_count(item.text) >= MIN_ROLE_WHY_WORDS
        and _has_marker(item.text, ROLE_WHY_MARKERS)
        and not _is_chart_fact(item.text)
        and item.customer_domain not in _LIFE_AREA_DOMAINS
        and item.customer_domain != CUSTOMER_DOMAIN_CAREER
    ]
    return _unique(chosen, exclude, PROFESSIONAL_SECTION_LIMITS["sec-ten_gods"])


def _select_shen_sha(evidence: list["_Evidence"], exclude: list[str]) -> list[str]:
    """Page 5 — matched stars only. No catalogue, no alias education."""
    chosen = [
        item.text
        for item in evidence
        if item.domain == SHEN_SHA_DOMAIN
        and word_count(item.text) >= 6
        and item.kind != KIND_WARNING
    ]
    return _unique(chosen, exclude, PROFESSIONAL_SECTION_LIMITS["sec-shen_sha"])


def _select_luck(
    payload: dict[str, Any],
    published: dict[str, list[str]],
    evidence: list["_Evidence"],
    exclude: list[str],
) -> list[str]:
    """Page 6 — current decade consultation. Not all ten cycles."""
    assembled = assemble_current_dayun_consultation(
        payload,
        published,
        exclude=exclude,
    )
    if assembled:
        return assembled
    return []


def _select_career(
    payload: dict[str, Any],
    published: dict[str, list[str]],
    evidence: list["_Evidence"],
    exclude: list[str],
) -> list[str]:
    """Page 7 — operating style plus period overlay. No profession catalogue."""
    overlay = career_overlay_from_analysis(luck_analysis_from_payload(payload))
    pool: list[str] = [overlay] if overlay else []
    for text in published.get("sec-impact") or []:
        if text.startswith(CUSTOMER_DOMAIN_LABELS[CUSTOMER_DOMAIN_CAREER]):
            pool.append(text)
    for item in evidence:
        if item.customer_domain in {
            CUSTOMER_DOMAIN_CAREER,
            CUSTOMER_DOMAIN_ENVIRONMENT,
            CUSTOMER_DOMAIN_DECISION,
        }:
            if word_count(item.text) >= MIN_CONSULTING_WORDS:
                pool.append(item.text)
                continue
        if _has_marker(item.text, CAREER_MARKERS) and word_count(item.text) >= MIN_CONSULTING_WORDS:
            pool.append(item.text)
    return _unique(pool, exclude, PROFESSIONAL_SECTION_LIMITS["sec-career"])


def _select_life_areas(
    payload: dict[str, Any],
    published: dict[str, list[str]],
    evidence: list["_Evidence"],
    exclude: list[str],
) -> list[str]:
    """Page 8 — one coherent consultation per remaining life area."""
    data = luck_analysis_from_payload(payload)
    overlays = {
        CUSTOMER_DOMAIN_FINANCE: finance_overlay_from_analysis(data),
        CUSTOMER_DOMAIN_RELATIONSHIP: relationship_overlay_from_analysis(data),
        CUSTOMER_DOMAIN_HEALTH: health_overlay_from_analysis(data),
    }
    chosen: list[str] = []
    blocked = list(exclude)
    for domain in _LIFE_AREA_DOMAINS:
        label = CUSTOMER_DOMAIN_LABELS[domain]
        overlay = overlays.get(domain) or ""
        natal_candidates: list[str] = []
        for text in published.get("sec-impact") or []:
            if text.startswith(label):
                natal_candidates.append(text)
        for item in evidence:
            if item.customer_domain == domain and word_count(item.text) >= MIN_CONSULTING_WORDS:
                natal_candidates.append(item.text)
        natal_limit = 1 if overlay else 2
        picked = _unique(natal_candidates, blocked, natal_limit)
        if overlay:
            chosen.append(overlay)
        chosen.extend(picked)
        blocked.extend(picked)
    return chosen[: PROFESSIONAL_SECTION_LIMITS["sec-life_areas"]]


def _select_recommendations(
    payload: dict[str, Any],
    published: dict[str, list[str]],
    evidence: list["_Evidence"],
    exclude: list[str],
) -> list[str]:
    """Page 9 — period overlay first, then ranked already-composed reasoning."""
    overlay = recommendation_overlay_from_analysis(luck_analysis_from_payload(payload))
    expanded: list[str] = [overlay] if overlay else []
    for item in evidence:
        if item.kind != KIND_RECOMMENDATION:
            continue
        if word_count(item.text) < 6:
            continue
        expanded.append(_join_clauses(item.text, item.rationale))
    if len(expanded) == (1 if overlay else 0):
        expanded.extend(published.get("sec-recommendation") or [])
    return _unique(
        expanded,
        exclude,
        PROFESSIONAL_SECTION_LIMITS["sec-professional_recommendation"],
    )


def _select_conclusion(
    payload: dict[str, Any],
    published: dict[str, list[str]],
    exclude: list[str],
) -> list[str]:
    """Page 10 — period-true close when Interaction Facts exist. No natal restart."""
    overlay = conclusion_overlay_from_analysis(luck_analysis_from_payload(payload))
    if overlay:
        return _unique(
            [overlay],
            exclude,
            PROFESSIONAL_SECTION_LIMITS["sec-professional_conclusion"],
        )
    texts = published.get("sec-conclusion") or []
    return _unique(texts, exclude, PROFESSIONAL_SECTION_LIMITS["sec-professional_conclusion"])


class _Evidence:
    """One already-composed evidence statement eligible for an edition."""

    __slots__ = (
        "text",
        "domain",
        "kind",
        "customer_domain",
        "rationale",
        "mitigation",
        "decision",
    )

    def __init__(
        self,
        *,
        text: str,
        domain: str,
        kind: str,
        customer_domain: str,
        rationale: str,
        mitigation: str,
        decision: str,
    ) -> None:
        self.text = text
        self.domain = domain
        self.kind = kind
        self.customer_domain = customer_domain
        self.rationale = rationale
        self.mitigation = mitigation
        self.decision = decision


def _evidence_candidates(
    payload: dict[str, Any],
    thesis: dict[str, Any] | None,
    chart_names: frozenset[str],
) -> list[_Evidence]:
    """PUBLISH-eligible evidence only. Drops stay unpublished."""
    chosen: list[_Evidence] = []
    for item in _iter_evidence(payload):
        if item.decision != DECISION_PUBLISH:
            continue
        chosen.append(item)
    return chosen


def _iter_evidence(payload: dict[str, Any]) -> list[_Evidence]:
    """Read composer evidence already attached to the NarrativeResult."""
    thesis = _thesis_from_payload(payload)
    chart_names = _chart_names_from_payload(payload)
    raw = payload.get("evidence")
    nodes = raw.get("nodes") if isinstance(raw, dict) else None
    if not isinstance(nodes, list):
        return []
    items: list[_Evidence] = []
    for node in nodes:
        if not isinstance(node, dict):
            continue
        text = normalize_text(str(node.get("statement") or ""))
        if not text:
            continue
        decision, _reason = classify_node(
            text,
            section_id=_slot_section(str(node.get("slot") or "")),
            thesis=thesis,
            chart_names=chart_names,
        )
        items.append(
            _Evidence(
                text=text,
                domain=str(node.get("domain") or ""),
                kind=str(node.get("kind") or ""),
                customer_domain=str(node.get("customer_domain") or ""),
                rationale=normalize_text(str(node.get("rationale") or "")),
                mitigation=normalize_text(str(node.get("mitigation") or "")),
                decision=decision,
            )
        )
    return items


def _appendix_allowed(
    item: _Evidence,
    thesis: dict[str, Any] | None,
    chart_names: frozenset[str],
) -> bool:
    """Correct supporting material that must not occupy the consultation."""
    if item.decision == DECISION_APPENDIX:
        return word_count(item.text) >= MIN_CONSULTING_WORDS
    if item.decision != DECISION_DROP:
        return False
    decision, reason = classify_node(
        item.text,
        section_id="sec-reasoning",
        thesis=thesis,
        chart_names=chart_names,
    )
    if reason in {"engine_language", "empty", "not_customer_prose"}:
        return False
    return reason in {"knowledge_dump", "correct_but_unnecessary"} or decision == DECISION_APPENDIX


def _published_texts_by_section(payload: dict[str, Any]) -> dict[str, list[str]]:
    """Customer paragraphs already selected for the Executive spine."""
    by_section: dict[str, list[str]] = {}
    for section in payload.get("sections") or []:
        if not isinstance(section, dict):
            continue
        section_id = str(section.get("id") or "")
        texts = [
            _paragraph_text(paragraph)
            for paragraph in (section.get("paragraphs") or [])
            if _paragraph_text(paragraph)
        ]
        if texts:
            by_section[section_id] = texts
    return by_section


def _unique(texts: list[str], exclude: list[str], limit: int) -> list[str]:
    """Keep one paragraph per customer value. Expand, do not copy."""
    kept: list[str] = []
    blocked = list(exclude)
    for text in texts:
        blob = normalize_text(text)
        if not blob:
            continue
        if any(_same_meaning(blob, other) for other in blocked):
            continue
        kept.append(blob)
        blocked.append(blob)
        if len(kept) >= limit:
            break
    return kept


def _limit(texts: list[str], section_id: str) -> list[str]:
    """Apply the professional page cap without adding text."""
    return _unique(texts, [], PROFESSIONAL_SECTION_LIMITS[section_id])


def _section_payload(
    section_id: str,
    texts: list[str],
    *,
    title: str | None = None,
) -> dict[str, Any]:
    """Pack already-composed paragraphs into a report section shell."""
    heading = title or PROFESSIONAL_PAGE_TITLES.get(section_id, section_id)
    return {
        "id": section_id,
        "intent": section_id.replace("sec-", ""),
        "title": heading,
        "paragraphs": [
            {
                "id": f"{section_id}-p{index}",
                "role": "explanation",
                "text": text,
                "evidence_refs": [],
                "interpretation_refs": [],
                "rule_refs": [],
                "knowledge_refs": [],
                "confidence": 0.0,
                "insufficient_data": False,
            }
            for index, text in enumerate(texts)
        ],
        "recommendations": [],
        "evidence_refs": [],
        "interpretation_refs": [],
        "confidence": 0.0,
        "insufficient_data": not texts,
        "tone": "explanatory",
    }


def _recommendation_records(texts: list[str]) -> list[dict[str, Any]]:
    """Top-level recommendation list follows the professional page."""
    return [
        {
            "id": f"rec-{index}",
            "priority": "high" if index == 0 else "medium",
            "action": text,
            "reason": "",
            "benefit": "",
            "evidence_refs": [],
            "interpretation_refs": [],
            "rule_refs": [],
            "knowledge_refs": [],
            "insufficient_data": False,
        }
        for index, text in enumerate(texts)
    ]


def _edition_metadata(
    payload: dict[str, Any],
    *,
    edition: str,
    sections: list[dict[str, Any]],
    appendix_count: int,
) -> dict[str, Any]:
    """Stamp edition policy without copying unpublished bodies."""
    metadata = dict(payload.get("metadata") or {}) if isinstance(payload.get("metadata"), dict) else {}
    publication = dict(metadata.get("publication") or {}) if isinstance(metadata.get("publication"), dict) else {}
    word_total = sum(
        word_count(_paragraph_text(paragraph))
        for section in sections
        for paragraph in (section.get("paragraphs") or [])
    )
    publication["edition"] = edition
    publication["publisher"] = PROFESSIONAL_REPORT_PUBLISHER_ID
    publication["applied"] = True
    publication["edition_metrics"] = {
        "edition": edition,
        "section_count": len(sections),
        "paragraph_count": sum(len(section.get("paragraphs") or []) for section in sections),
        "word_count": word_total,
        "appendix_count": appendix_count,
        "section_published": {
            str(section.get("id") or ""): len(section.get("paragraphs") or [])
            for section in sections
        },
    }
    metadata["publication"] = publication
    return metadata


def _appendix_count(
    payload: dict[str, Any],
    thesis: dict[str, Any] | None,
    chart_names: frozenset[str],
) -> int:
    """How many supporting nodes belong in the appendix edition."""
    return sum(
        1
        for item in _iter_evidence(payload)
        if _appendix_allowed(item, thesis, chart_names)
    )


def _join_clauses(left: str, right: str) -> str:
    """Concatenate already-composed clauses. Do not rewrite either side."""
    head = normalize_text(left)
    tail = normalize_text(right)
    if not tail or _same_meaning(head, tail):
        return head
    if tail.casefold() in head.casefold():
        return head
    return f"{head} {tail}"


def _is_chart_fact(text: str) -> bool:
    """True when the paragraph is an observation fact, not a consultation."""
    lowered = normalize_text(text).casefold()
    return any(lowered.startswith(prefix) for prefix in CHART_FACT_PREFIXES)


def _has_marker(text: str, markers: tuple[str, ...]) -> bool:
    """True when any publication marker appears in the paragraph."""
    lowered = normalize_text(text).casefold()
    return any(marker in lowered for marker in markers)


def _without_period_copy(texts: list[str]) -> list[str]:
    """Natal paragraphs only. Period overlays must not suppress each other."""
    kept: list[str] = []
    for text in texts:
        if _has_marker(text, LUCK_MARKERS):
            continue
        lowered = normalize_text(text).casefold()
        if "danh tính đại vận" in lowered:
            continue
        if "không lặp luận giải gốc" in lowered:
            continue
        if "chưa xác định thêm tương tác" in lowered:
            continue
        kept.append(text)
    return kept


def _slot_section(slot: str) -> str:
    """Map an evidence slot onto a classification section."""
    mapping = {
        "summary": "sec-executive_summary",
        "observation": "sec-observation",
        "reasoning": "sec-reasoning",
        "impact": "sec-impact",
        "recommendation": "sec-recommendation",
        "warning": "sec-warning",
        "conclusion": "sec-conclusion",
    }
    return mapping.get(slot, "sec-reasoning")


def _normalize_edition(edition: str) -> str:
    """Accept product aliases without creating a new edition."""
    blob = str(edition or "").strip().casefold()
    if blob in {"professional", "professional_report", "package_b"}:
        return EDITION_PROFESSIONAL
    if blob in {"technical_appendix", "appendix", "package_d"}:
        return EDITION_APPENDIX
    return EDITION_EXECUTIVE


def _payload_edition(payload: dict[str, Any]) -> str:
    """Edition already published on this payload, else executive."""
    metadata = payload.get("metadata")
    if not isinstance(metadata, dict):
        return EDITION_EXECUTIVE
    publication = metadata.get("publication")
    if not isinstance(publication, dict):
        return EDITION_EXECUTIVE
    return _normalize_edition(str(publication.get("edition") or EDITION_EXECUTIVE))
