"""Customer-safe compact Temporal Activation. No IDs, traces, or hashes."""

from __future__ import annotations

from typing import Any

from engines.detailed_interpretation_engine.enums import EvaluationStatus
from engines.detailed_interpretation_engine.temporal import TemporalActivationResult
from engines.detailed_interpretation_engine.temporal_activation.constants import MAIN_TEMPORAL_IDS
from engines.detailed_interpretation_engine.temporal_activation.labels import (
    BOTTLENECK_LABELS,
    DOMAIN_TITLES,
    DRIVER_LABELS,
    EXPRESSION_LABELS,
    LEVEL_MARKERS,
    NATAL_LABELS,
    TITLE,
)
from engines.detailed_interpretation_engine.luck_activation.labels import STATE_LABELS as LUCK_LABELS

_LEAK = ("TR-P7-", "E-DI-", "DI-11-", "mingju", "0x", "damage_activation", "rescue_activation")
_EVENT = (
    "thăng chức",
    "kiếm nhiều tiền",
    "chia tay",
    "sẽ bệnh",
    "sẽ thành công",
    "phát tài",
    "cưới",
    "đổi việc",
    "năm nay chắc chắn",
)


def present_temporal_activation_customer(result: TemporalActivationResult) -> dict[str, Any]:
    """Compact current-year annual expression for the existing Luck card."""
    if result.state in {EvaluationStatus.NOT_EVALUATED, EvaluationStatus.NOT_APPLICABLE}:
        return {}
    if "annual" not in result.evaluated_layers:
        return {}
    items = [
        _item(result.domain_results[domain_id], result.time_window)
        for domain_id in MAIN_TEMPORAL_IDS
        if domain_id in result.domain_results
    ]
    if not items:
        return {}
    return {
        "title": TITLE,
        "year": result.time_window,
        "gan_zhi": _gan_zhi(result),
        "dominant_activation": _domain_title(result.dominant_activation),
        "dominant_suppression": _domain_title(result.dominant_suppression),
        "stress": _first_title(result.stress),
        "recovery": _first_title(result.recovery),
        "items": items,
    }


def _gan_zhi(result: TemporalActivationResult) -> str:
    layer = result.layer_results.get("annual")
    if layer is None:
        return ""
    return layer.temporal_pillar.strip()


def _item(result: Any, year: str) -> dict[str, Any]:
    return {
        "id": result.domain_id,
        "title": DOMAIN_TITLES.get(result.domain_id, result.domain_id),
        "year": year,
        "natal_state": result.natal_state,
        "natal_label": NATAL_LABELS.get(result.natal_state, result.natal_state),
        "luck_state": result.luck_activation_state,
        "luck_label": LUCK_LABELS.get(result.luck_activation_state, result.luck_activation_state),
        "annual_state": result.annual_expression_state,
        "annual_label": EXPRESSION_LABELS.get(
            result.annual_expression_state,
            result.annual_expression_state,
        ),
        "modifier": "",
        "driver": _safe(DRIVER_LABELS.get(result.temporal_driver, "")),
        "bottleneck": _safe(BOTTLENECK_LABELS.get(result.temporal_bottleneck, "")),
        "support": LEVEL_MARKERS.get(result.support, ""),
        "stress": LEVEL_MARKERS.get(result.stress, ""),
        "recovery": LEVEL_MARKERS.get(result.recovery, ""),
        "conditions": tuple(_safe(item) for item in result.conditions if _safe(item)),
    }


def _domain_title(domain_id: str) -> str:
    if not domain_id or domain_id in {"not_applicable", "unresolved"}:
        return ""
    return DOMAIN_TITLES.get(domain_id, "")


def _first_title(domain_ids: tuple[str, ...]) -> str:
    for domain_id in domain_ids:
        title = _domain_title(domain_id)
        if title:
            return title
    return ""


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
