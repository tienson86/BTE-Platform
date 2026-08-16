"""Published Narrative Builder — publication stage after Narrative Composer."""

from __future__ import annotations

from typing import Any

from engines.interpretation_engine.foundation.narrative.constants import (
    CUSTOMER_DOMAIN_LABELS,
)
from engines.interpretation_engine.foundation.narrative.publish.constants import (
    DECISION_APPENDIX,
    DECISION_DROP,
    DECISION_PUBLISH,
    IMPACT_SPINE_LABELS,
    MEANING_JACCARD_THRESHOLD,
    PUBLISHED_NARRATIVE_BUILDER_ID,
    SECTION_LIMITS,
    SECTION_PRIORITY,
)
from engines.interpretation_engine.foundation.narrative.publish.criteria import (
    classify_node,
    engine_language_hits,
    meaning_tokens,
)
from engines.interpretation_engine.foundation.narrative.publish.metrics import (
    build_editorial_metrics,
)
from engines.interpretation_engine.foundation.narrative.publish.models import (
    PublicationNode,
    PublishedNarrative,
)
from engines.interpretation_engine.foundation.narrative.text import (
    fingerprint,
    normalize_text,
)

_CHART_NAME_LABELS = (
    "Nhật chủ:",
    "Dụng thần được chọn:",
    "Hỷ thần:",
    "Kỵ thần:",
    "Cục:",
)


class PublishedNarrativeBuilder:
    """Decide which composer paragraphs may appear in the customer report."""

    def publish(self, payload: dict[str, Any]) -> PublishedNarrative:
        """Classify every node, then emit published sections only."""
        thesis = _thesis_from_payload(payload)
        chart_names = _chart_names_from_payload(payload)
        nodes = _collect_nodes(payload, thesis, chart_names)
        nodes = _dedupe_by_meaning(nodes)
        nodes = _apply_section_limits(nodes)
        nodes = _promote_appendix_if_empty(nodes)
        published_sections = _rebuild_sections(payload, nodes)
        summary = _rebuild_summary(payload, published_sections)
        recommendations = _rebuild_recommendations(published_sections)
        metrics = build_editorial_metrics(nodes, thesis)
        return PublishedNarrative(
            sections=published_sections,
            summary=summary,
            recommendations=recommendations,
            nodes=tuple(nodes),
            metrics=metrics,
        )

    def apply(self, payload: dict[str, Any]) -> dict[str, Any]:
        """Replace customer-facing sections. Do not mutate composer internals."""
        metadata = payload.get("metadata")
        if isinstance(metadata, dict):
            publication = metadata.get("publication")
            if isinstance(publication, dict) and publication.get("applied"):
                return payload
        result = self.publish(payload)
        out = dict(payload)
        out["sections"] = result.sections
        out["summary"] = result.summary
        out["recommendations"] = result.recommendations
        out["metadata"] = _publication_metadata(payload, result)
        return _align_overlay(out, result)


def apply_published_narrative(payload: dict[str, Any]) -> dict[str, Any]:
    """Public entry: customer payload contains published narrative only."""
    if not isinstance(payload, dict):
        return payload
    sections = payload.get("sections")
    if not isinstance(sections, list) or not sections:
        return payload
    return PublishedNarrativeBuilder().apply(payload)


def _collect_nodes(
    payload: dict[str, Any],
    thesis: dict[str, Any] | None,
    chart_names: frozenset[str],
) -> list[PublicationNode]:
    """One node per paragraph. Never split a paragraph for partial publish."""
    nodes: list[PublicationNode] = []
    order = 0
    for section in payload.get("sections") or []:
        if not isinstance(section, dict):
            continue
        section_id = str(section.get("id") or "")
        paragraphs = list(section.get("paragraphs") or [])
        if not paragraphs and section.get("recommendations"):
            paragraphs = [
                {"id": str(item.get("id") or f"{section_id}-rec{index}"), "text": str(item.get("action") or "")}
                for index, item in enumerate(section.get("recommendations") or [])
                if isinstance(item, dict)
            ]
        for index, paragraph in enumerate(paragraphs):
            text = _paragraph_text(paragraph)
            decision, reason = classify_node(
                text,
                section_id=section_id,
                thesis=thesis,
                chart_names=chart_names,
            )
            node_id = ""
            if isinstance(paragraph, dict):
                node_id = str(paragraph.get("id") or "")
            nodes.append(
                PublicationNode(
                    node_id=node_id or f"{section_id}-p{index}",
                    section_id=section_id,
                    text=text,
                    decision=decision,
                    reason=reason,
                    order=order,
                )
            )
            order += 1
    return nodes


def _dedupe_by_meaning(nodes: list[PublicationNode]) -> list[PublicationNode]:
    """Keep one published paragraph per customer value. Meaning, not string."""
    kept: list[PublicationNode] = []
    out: list[PublicationNode] = []
    by_priority = {section_id: index for index, section_id in enumerate(SECTION_PRIORITY)}
    ranked = sorted(
        nodes,
        key=lambda node: (by_priority.get(node.section_id, 99), node.order),
    )
    for node in ranked:
        if node.decision != DECISION_PUBLISH:
            out.append(node)
            continue
        if node.section_id == "sec-conclusion":
            out.append(node)
            kept.append(node)
            continue
        if any(_same_meaning(node.text, other.text) for other in kept):
            out.append(
                PublicationNode(
                    node_id=node.node_id,
                    section_id=node.section_id,
                    text=node.text,
                    decision=DECISION_DROP,
                    reason="duplicate_meaning",
                    order=node.order,
                )
            )
            continue
        out.append(node)
        kept.append(node)
    return sorted(out, key=lambda node: node.order)


def _apply_section_limits(nodes: list[PublicationNode]) -> list[PublicationNode]:
    """Trim extras after classification. Extra impact domains become appendix."""
    seen_domain: set[str] = set()
    kept_by_section: dict[str, int] = {section_id: 0 for section_id in SECTION_LIMITS}
    out: list[PublicationNode] = []
    for node in nodes:
        if node.decision != DECISION_PUBLISH:
            out.append(node)
            continue
        limit = SECTION_LIMITS.get(node.section_id)
        if limit is None:
            out.append(node)
            continue
        if node.section_id == "sec-impact":
            domain = _impact_domain(node.text)
            if domain and domain in seen_domain:
                out.append(_retarget(node, DECISION_DROP, "duplicate_domain"))
                continue
            if domain and domain not in IMPACT_SPINE_LABELS:
                out.append(_retarget(node, DECISION_APPENDIX, "non_spine_domain"))
                continue
            if kept_by_section[node.section_id] >= limit:
                out.append(_retarget(node, DECISION_APPENDIX, "section_limit"))
                continue
            if domain:
                seen_domain.add(domain)
        elif kept_by_section[node.section_id] >= limit:
            out.append(_retarget(node, DECISION_DROP, "section_limit"))
            continue
        kept_by_section[node.section_id] += 1
        out.append(node)
    return out


def _promote_appendix_if_empty(nodes: list[PublicationNode]) -> list[PublicationNode]:
    """Keep a required section alive with appendix knowledge, never engine drops."""
    published = {section_id: 0 for section_id in SECTION_LIMITS}
    for node in nodes:
        if node.decision == DECISION_PUBLISH:
            published[node.section_id] = published.get(node.section_id, 0) + 1
    out: list[PublicationNode] = []
    promoted: set[str] = set()
    for node in nodes:
        empty = published.get(node.section_id, 0) == 0
        if (
            empty
            and node.decision == DECISION_APPENDIX
            and node.section_id not in promoted
            and node.section_id in SECTION_LIMITS
        ):
            out.append(_retarget(node, DECISION_PUBLISH, "promoted_appendix"))
            promoted.add(node.section_id)
            continue
        out.append(node)
    return out


def _rebuild_sections(
    payload: dict[str, Any],
    nodes: list[PublicationNode],
) -> list[dict[str, Any]]:
    """Copy section shells; keep only PUBLISH paragraphs."""
    published_by_section: dict[str, list[PublicationNode]] = {}
    for node in nodes:
        if node.decision != DECISION_PUBLISH:
            continue
        published_by_section.setdefault(node.section_id, []).append(node)
    original = {
        str(item.get("id") or ""): item
        for item in (payload.get("sections") or [])
        if isinstance(item, dict)
    }
    sections: list[dict[str, Any]] = []
    for section in payload.get("sections") or []:
        if not isinstance(section, dict):
            continue
        cloned = dict(section)
        section_id = str(section.get("id") or "")
        published_nodes = published_by_section.get(section_id, [])
        cloned["paragraphs"] = [
            _published_paragraph(original.get(section_id), node)
            for node in published_nodes
        ]
        if section_id == "sec-recommendation":
            allowed = {normalize_text(node.text) for node in published_nodes}
            cloned["recommendations"] = [
                rec
                for rec in (section.get("recommendations") or [])
                if isinstance(rec, dict)
                and normalize_text(str(rec.get("action") or rec.get("text") or ""))
                in allowed
            ]
        cloned["insufficient_data"] = not published_nodes
        sections.append(cloned)
    return sections


def _published_paragraph(
    section: dict[str, Any] | None,
    node: PublicationNode,
) -> dict[str, Any]:
    """Reuse the original paragraph payload when the id still matches."""
    for paragraph in (section or {}).get("paragraphs") or []:
        if isinstance(paragraph, dict) and str(paragraph.get("id") or "") == node.node_id:
            cloned = dict(paragraph)
            cloned["text"] = node.text
            return cloned
    return {"id": node.node_id, "role": "explanation", "text": node.text}


def _rebuild_summary(
    payload: dict[str, Any],
    sections: list[dict[str, Any]],
) -> dict[str, Any]:
    """Customer summary follows published exec / rec / warning text."""
    summary = dict(payload.get("summary") or {}) if isinstance(payload.get("summary"), dict) else {}
    by_id = {str(item.get("id") or ""): item for item in sections}
    exec_text = _section_blob(by_id.get("sec-executive_summary"))
    recs = _section_texts(by_id.get("sec-recommendation"))
    warns = _section_texts(by_id.get("sec-warning"))
    if exec_text:
        summary["identity"] = exec_text
    if recs:
        summary["priority_recommendation"] = recs[0]
        summary["next_action"] = recs[0]
    if warns:
        summary["weaknesses"] = warns[:3]
    return summary


def _rebuild_recommendations(sections: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Top-level recommendation list matches the published recommendation section."""
    for section in sections:
        if section.get("id") == "sec-recommendation":
            recs = section.get("recommendations") or []
            if recs:
                return [dict(item) for item in recs if isinstance(item, dict)]
            return [
                {
                    "id": f"rec-{index}",
                    "priority": "high" if index == 0 else "medium",
                    "action": _paragraph_text(paragraph),
                    "reason": "",
                    "benefit": "",
                    "evidence_refs": list(paragraph.get("evidence_refs") or [])
                    if isinstance(paragraph, dict)
                    else [],
                    "interpretation_refs": [],
                    "rule_refs": [],
                    "knowledge_refs": [],
                    "insufficient_data": False,
                }
                for index, paragraph in enumerate(section.get("paragraphs") or [])
            ]
    return []


def _publication_metadata(
    payload: dict[str, Any],
    result: PublishedNarrative,
) -> dict[str, Any]:
    """Attach publication audit without copying dropped paragraph bodies."""
    metadata = dict(payload.get("metadata") or {}) if isinstance(payload.get("metadata"), dict) else {}
    metadata["publication"] = {
        "builder": PUBLISHED_NARRATIVE_BUILDER_ID,
        "applied": True,
        "metrics": result.metrics.to_dict(),
        "decisions": result.decisions(),
    }
    return metadata


def _align_overlay(payload: dict[str, Any], result: PublishedNarrative) -> dict[str, Any]:
    """Keep overlay keys, but stop them from bypassing published identity."""
    identity = str((result.summary or {}).get("identity") or "")
    executive = payload.get("commercial_executive_summary")
    if isinstance(executive, dict) and identity:
        composed = str(executive.get("composed_text") or "")
        if engine_language_hits(composed) or not composed.strip():
            item = dict(executive)
            item["composed_text"] = identity
            payload["commercial_executive_summary"] = item
    primary = payload.get("primary_recommendation")
    recs = result.recommendations
    if isinstance(primary, dict) and recs:
        composed = str(primary.get("composed_text") or primary.get("action") or "")
        if engine_language_hits(composed):
            item = dict(primary)
            action = str(recs[0].get("action") or "")
            item["composed_text"] = action
            payload["primary_recommendation"] = item
    return payload


def _same_meaning(left: str, right: str) -> bool:
    """True when two paragraphs communicate the same customer value."""
    if fingerprint(left) == fingerprint(right):
        return True
    tokens_left = meaning_tokens(left)
    tokens_right = meaning_tokens(right)
    if not tokens_left or not tokens_right:
        return False
    union = len(tokens_left | tokens_right)
    if union == 0:
        return False
    return (len(tokens_left & tokens_right) / union) >= MEANING_JACCARD_THRESHOLD


def _impact_domain(text: str) -> str:
    """Known domain heading, or empty when the paragraph has none."""
    blob = normalize_text(text)
    for label in CUSTOMER_DOMAIN_LABELS.values():
        if label and blob.startswith(label):
            return label
    return ""


def _retarget(node: PublicationNode, decision: str, reason: str) -> PublicationNode:
    """Copy a node with a new publication decision."""
    return PublicationNode(
        node_id=node.node_id,
        section_id=node.section_id,
        text=node.text,
        decision=decision,
        reason=reason,
        order=node.order,
    )


def _paragraph_text(paragraph: Any) -> str:
    """Extract customer text from a Pack 05 paragraph payload."""
    if isinstance(paragraph, dict):
        return normalize_text(str(paragraph.get("text") or ""))
    return normalize_text(str(paragraph or ""))


def _section_texts(section: dict[str, Any] | None) -> list[str]:
    """Published paragraph texts for one section."""
    if not section:
        return []
    return [
        _paragraph_text(item)
        for item in (section.get("paragraphs") or [])
        if _paragraph_text(item)
    ]


def _section_blob(section: dict[str, Any] | None) -> str:
    """Join published paragraphs into one customer string."""
    return " ".join(_section_texts(section))


def _thesis_from_payload(payload: dict[str, Any]) -> dict[str, Any] | None:
    """Read case thesis already attached by the composer. Do not recompute."""
    metadata = payload.get("metadata")
    if not isinstance(metadata, dict):
        return None
    thesis = metadata.get("case_thesis")
    return thesis if isinstance(thesis, dict) else None


def _chart_names_from_payload(payload: dict[str, Any]) -> frozenset[str]:
    """Names already present in observation text. Does not call engines."""
    names: set[str] = set()
    thesis = _thesis_from_payload(payload)
    if thesis:
        for key in ("title", "core_pattern", "useful_function", "ky_function"):
            value = str(thesis.get(key) or "").strip()
            if value:
                names.add(value)
    for section in payload.get("sections") or []:
        if not isinstance(section, dict) or section.get("id") != "sec-observation":
            continue
        for paragraph in section.get("paragraphs") or []:
            text = _paragraph_text(paragraph)
            for label in _CHART_NAME_LABELS:
                if text.startswith(label):
                    names.add(text.split(":", 1)[-1].strip())
    return frozenset(name for name in names if name)
