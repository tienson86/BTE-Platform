"""Customer-safe compact Domain Interpretation. No IDs, traces, or hashes."""

from __future__ import annotations

from typing import Any

from engines.detailed_interpretation_engine.domain_interpretation.constants import MAIN_DOMAIN_IDS
from engines.detailed_interpretation_engine.domain_interpretation.labels import (
    DIMENSION_LABELS,
    DOMAIN_TITLES,
    STATE_LABELS,
    UNRESOLVED_COPY,
    classification_label,
)
from engines.detailed_interpretation_engine.domains import DomainInterpretationResult, DomainSection
from engines.detailed_interpretation_engine.enums import DomainState

TITLE = "6 trụ cột luận giải"


def present_domains_customer(section: DomainSection) -> dict[str, Any]:
    """Compact six-domain summary plus accordion fields. Labels only."""
    lookup = {
        "authority": section.authority.natal,
        "career": section.career.natal,
        "wealth": section.wealth.natal,
        "relationship": section.relationship.natal,
        "legacy": section.legacy.natal,
        "vitality": section.vitality.natal,
    }
    order = [item for item in section.order if item in lookup] or list(MAIN_DOMAIN_IDS)
    items = [_item(lookup[domain_id]) for domain_id in order if domain_id in lookup]
    if not items:
        items = [_item(lookup[domain_id]) for domain_id in MAIN_DOMAIN_IDS]
    evaluated = [
        item
        for item in items
        if item["state"] not in {DomainState.NOT_EVALUATED.value}
    ]
    if not evaluated:
        return {}
    return {"title": TITLE, "items": evaluated}


def _item(result: DomainInterpretationResult) -> dict[str, Any]:
    unresolved = result.state in {DomainState.UNRESOLVED, DomainState.NOT_EVALUATED, DomainState.BLOCKED}
    summary = result.customer_summary.strip()
    if unresolved:
        summary = UNRESOLVED_COPY
    opportunity = result.opportunities[0] if result.opportunities else ""
    caution = result.risk or (result.warnings[0] if result.warnings else "") or result.bottleneck
    return {
        "id": result.domain_id,
        "title": DOMAIN_TITLES.get(result.domain_id, result.domain_id),
        "state": result.state.value,
        "state_label": STATE_LABELS.get(result.state.value, result.state.value),
        "driver": "" if unresolved else result.driver,
        "driver_id": "" if unresolved else result.driver_id,
        "support": "" if unresolved else result.support,
        "bottleneck": "" if unresolved else result.bottleneck,
        "opportunity": "" if unresolved else opportunity,
        "caution": "" if unresolved else caution,
        "condition": "" if unresolved else result.condition,
        "confidence": "" if unresolved else _confidence_label(result.confidence.summary),
        "summary": summary,
        "dimensions": _dimensions(result),
        "unresolved": unresolved,
    }


def _dimensions(result: DomainInterpretationResult) -> list[dict[str, str]]:
    if result.state in {DomainState.UNRESOLVED, DomainState.NOT_EVALUATED}:
        return []
    items: list[dict[str, str]] = []
    for key, value in result.dimensions.items():
        label = DIMENSION_LABELS.get(key, "")
        mapped = classification_label(value)
        if not label or not mapped:
            continue
        if key in {"biological_legacy", "family_legacy"}:
            continue
        items.append({"label": label, "value": mapped})
    return items[:8]


def _confidence_label(summary: str) -> str:
    if summary == "structural_qualified":
        return "Có căn cứ cấu trúc"
    if summary == "structural":
        return "Có căn cứ cấu trúc"
    if summary == "insufficient":
        return "Chưa đủ dữ liệu"
    return ""
