"""Customer-safe compact Luck Interaction. No IDs, traces, or hashes."""

from __future__ import annotations

from typing import Any

from engines.detailed_interpretation_engine.enums import EvaluationStatus
from engines.detailed_interpretation_engine.luck_interaction.constants import DRIVER_SENTINELS
from engines.detailed_interpretation_engine.luck_interaction.labels import (
    DOMAIN_TITLES,
    SITUATION_LABELS,
    TITLE,
    TYPE_LABELS,
)
from engines.detailed_interpretation_engine.temporal import LuckInteractionResult

_LEAK = ("TR-P7-", "E-DI-", "DI-10-", "mingju", "0x")
_EVENT = ("thăng chức", "kiếm nhiều tiền", "chia tay", "sẽ bệnh", "sẽ thành công", "phát tài")


def present_luck_interaction_customer(result: LuckInteractionResult) -> dict[str, Any]:
    """Compact current-Đại-Vận interaction for the existing Luck card."""
    if result.status in {EvaluationStatus.NOT_EVALUATED, EvaluationStatus.NOT_APPLICABLE}:
        return {}
    situation = SITUATION_LABELS.get(result.life_situation.situation_id, "")
    if result.life_situation.situation_id == "not_applicable":
        return {}
    edges = [_edge(item) for item in result.findings]
    edges = [item for item in edges if item]
    payload = {
        "title": TITLE,
        "situation": _safe(situation),
        "driver": _domain_title(result.interaction_driver),
        "bottleneck": _domain_title(result.interaction_bottleneck),
        "opportunity": _safe(result.opportunity),
        "risk": _safe(result.risk),
        "edges": edges,
    }
    if not payload["situation"] and not payload["driver"] and not edges:
        return {}
    return payload


def _edge(finding: Any) -> dict[str, str] | None:
    source = DOMAIN_TITLES.get(finding.source_domain, "")
    target = DOMAIN_TITLES.get(finding.target_domain, "")
    type_label = TYPE_LABELS.get(finding.interaction_type, "")
    if not source or not target or not type_label:
        return None
    explanation = ""
    if finding.opportunities:
        explanation = _safe(finding.opportunities[0])
    elif finding.risks:
        explanation = _safe(finding.risks[0])
    condition = _safe(finding.conditions[0]) if finding.conditions else ""
    if not explanation:
        explanation = f"{source} ↔ {target}"
    return {
        "source": source,
        "target": target,
        "type": type_label,
        "explanation": explanation,
        "condition": condition,
    }


def _domain_title(domain_id: str) -> str:
    if domain_id in DRIVER_SENTINELS:
        return ""
    return DOMAIN_TITLES.get(domain_id, "")


def _safe(value: str) -> str:
    text = (value or "").strip()
    if not text:
        return ""
    lowered = text.lower()
    if any(token.lower() in text for token in _LEAK):
        return ""
    if any(token in lowered for token in _EVENT):
        return ""
    return text

