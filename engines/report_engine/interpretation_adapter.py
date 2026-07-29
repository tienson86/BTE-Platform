"""Adapt InterpretationResult (object or dict) into template bind context."""

from __future__ import annotations

from dataclasses import asdict, is_dataclass
from typing import Any, Mapping


# WP6 builder section → Interpretation section keys (fallbacks allowed)
SECTION_CONTENT_KEYS: dict[str, tuple[str, ...]] = {
    "summary": ("summary",),
    "personality": ("personality",),
    "career": ("career",),
    "wealth": ("wealth",),
    "relationship": ("relationship",),
    "health": ("health",),
    "children": ("children", "relationship"),
    "useful_god": ("useful_god",),
    "luck_cycle": ("luck", "luck_cycle"),
    "yearly_fortune": ("year", "yearly_fortune", "luck"),
    "conclusion": ("conclusion",),
}


def interpretation_to_dict(interpretation: Any) -> dict[str, Any]:
    """Normalize InterpretationResult / dict / namespace into a plain dict."""
    if interpretation is None:
        return {}
    if isinstance(interpretation, Mapping):
        return dict(interpretation)
    if is_dataclass(interpretation):
        return asdict(interpretation)

    payload: dict[str, Any] = {}
    for key in (
        "summary",
        "sections",
        "sentences",
        "rules_used",
        "strengths",
        "weaknesses",
        "warnings",
        "confidence",
        "score",
        "priority_resolution",
        "matched_rule_count",
        "resolved_rule_count",
        "discarded_rules",
        "sentence_count",
        "section_count",
        "coverage",
        "unused_rules",
    ):
        if hasattr(interpretation, key):
            payload[key] = getattr(interpretation, key)

    # Normalize sections dataclass → dict of rule lists
    sections = payload.get("sections")
    if isinstance(sections, dict):
        normalized: dict[str, Any] = {}
        for name, section in sections.items():
            if isinstance(section, Mapping):
                normalized[str(name)] = dict(section)
            elif is_dataclass(section):
                normalized[str(name)] = asdict(section)
            else:
                rules = getattr(section, "rules", None)
                normalized[str(name)] = {
                    "name": getattr(section, "name", name),
                    "rules": list(rules or []),
                    "score": getattr(section, "score", 0),
                }
        payload["sections"] = normalized
    return payload


def extract_section_texts(
    interpretation: Mapping[str, Any],
    section_name: str,
) -> dict[str, Any]:
    """
    Build bindable fields for one report module from Interpretation content.

    Returns keys used by template content_ref tails: title, summary, body,
    recommendation, paragraphs (list).
    """
    keys = SECTION_CONTENT_KEYS.get(section_name, (section_name,))
    sections = interpretation.get("sections") or {}
    sentences = interpretation.get("sentences") or []

    rules: list[dict[str, Any]] = []
    for key in keys:
        section = sections.get(key)
        if isinstance(section, Mapping):
            for rule in section.get("rules") or []:
                if isinstance(rule, Mapping):
                    rules.append(dict(rule))
        for sentence in sentences:
            if not isinstance(sentence, Mapping):
                continue
            if str(sentence.get("section") or "") == key:
                rules.append(
                    {
                        "rule_id": sentence.get("rule_id"),
                        "description": sentence.get("sentence"),
                        "sentence": sentence.get("sentence"),
                        "priority": sentence.get("priority", 0),
                    }
                )

    # Deduplicate by text
    seen: set[str] = set()
    paragraphs: list[str] = []
    for rule in rules:
        text = str(
            rule.get("sentence")
            or rule.get("description")
            or rule.get("message")
            or ""
        ).strip()
        if not text:
            continue
        key = text.lower()
        if key in seen:
            continue
        seen.add(key)
        paragraphs.append(text)

    summary_text = ""
    if section_name == "summary":
        summary_text = str(interpretation.get("summary") or "").strip()
        if summary_text and summary_text.lower() not in seen:
            paragraphs.insert(0, summary_text)

    body = "\n\n".join(paragraphs)
    title = paragraphs[0] if paragraphs else summary_text
    recommendation = paragraphs[-1] if len(paragraphs) > 1 else ""

    return {
        "section_key": section_name,
        "title": title,
        "summary": summary_text or (paragraphs[0] if paragraphs else ""),
        "body": body,
        "recommendation": recommendation,
        "paragraphs": paragraphs,
        "rules": rules,
        "module_ready": bool(paragraphs or summary_text),
    }


def build_bind_context(interpretation: Any) -> dict[str, Any]:
    """Full placeholder / content_ref resolution context."""
    data = interpretation_to_dict(interpretation)
    modules: dict[str, Any] = {}
    for name in SECTION_CONTENT_KEYS:
        modules[name] = extract_section_texts(data, name)

    return {
        "interpretation": modules,
        "report_context": {
            "subject_name": (
                (data.get("metadata") or {}).get("subject_name")
                if isinstance(data.get("metadata"), Mapping)
                else ""
            )
            or "",
        },
        "raw": data,
    }
