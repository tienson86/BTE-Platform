"""Customer-safe compact Narrative Composer. No IDs, traces, or hashes."""

from __future__ import annotations

from typing import Any

from engines.detailed_interpretation_engine.enums import EvaluationStatus
from engines.detailed_interpretation_engine.narrative import NarrativeBlock, NarrativeResult
from engines.detailed_interpretation_engine.narrative_composer.constants import FORBIDDEN_CUSTOMER_TOKENS
from engines.detailed_interpretation_engine.narrative_composer.labels import DOMAIN_FIELD, SECTION_TITLES

_LEAK = ("TR-P7-", "E-DI-", "mingju", "0x", "nar.")


def present_narrative_customer(result: NarrativeResult) -> dict[str, Any]:
    """Compact Pack 07 narrative for the existing interpretation card."""
    if result.status in {EvaluationStatus.NOT_EVALUATED, EvaluationStatus.NOT_APPLICABLE}:
        return {}
    if not result.executive_summary and not result.blocks:
        return {}
    by_type: dict[str, list[NarrativeBlock]] = {}
    for item in result.blocks:
        by_type.setdefault(item.block_type, []).append(item)
    payload = {
        "title": "LUẬN GIẢI TỔNG THỂ",
        "executive": _clean(result.executive_summary),
        "strengths": [_item(item) for item in by_type.get("strength", [])],
        "risks": [_item(item) for item in by_type.get("risk", [])],
        "opportunities": [_item(item) for item in by_type.get("opportunity", [])],
        "domains": [_domain(item) for item in by_type.get("domain_section", [])],
        "luck": [_item(item) for item in by_type.get("temporal", [])],
        "actions": [_item(item) for item in by_type.get("action", [])],
        "closing": _clean(result.closing_summary),
        "labels": {
            "executive": SECTION_TITLES["executive_summary"],
            "strengths": SECTION_TITLES["strength"],
            "risks": SECTION_TITLES["risk"],
            "opportunities": SECTION_TITLES["opportunity"],
            "domains": SECTION_TITLES["domain_section"],
            "luck": SECTION_TITLES["temporal"],
            "actions": SECTION_TITLES["optimization_section"],
            "closing": SECTION_TITLES["closing_summary"],
            "fields": DOMAIN_FIELD,
        },
    }
    dump = str(payload).lower()
    if any(token in dump for token in FORBIDDEN_CUSTOMER_TOKENS) or any(token in dump for token in _LEAK):
        payload = _strip_leak(payload)
    return payload


def _item(block: NarrativeBlock) -> dict[str, str]:
    return {
        "title": _clean(block.title),
        "summary": _clean(block.summary),
        "domain": _clean(block.domain),
        "priority": block.priority,
    }


def _domain(block: NarrativeBlock) -> dict[str, str]:
        details = list(block.details)
        while len(details) < 6:
            details.append("")
        return {
            "id": block.domain,
            "title": _clean(block.title),
            "summary": _clean(block.summary),
            "state": _clean(details[0]),
            "driver": _clean(details[1]),
            "bottleneck": _clean(details[2]),
            "opportunity": _clean(details[3]),
            "caution": _clean(details[4]),
            "condition": _clean(details[5]),
        }


def _clean(value: str) -> str:
    text = value.strip()
    for token in _LEAK:
        if token in text:
            return ""
    return text


def _strip_leak(payload: Any) -> Any:
    if isinstance(payload, dict):
        return {key: _strip_leak(value) for key, value in payload.items()}
    if isinstance(payload, list):
        return [_strip_leak(item) for item in payload]
    if isinstance(payload, str) and any(token in payload for token in _LEAK):
        return ""
    return payload
