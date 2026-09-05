"""Customer-safe compact Luck Activation. No IDs, traces, or hashes."""

from __future__ import annotations

from typing import Any

from engines.detailed_interpretation_engine.enums import ActivationState, EvaluationStatus
from engines.detailed_interpretation_engine.luck_activation.constants import MAIN_ACTIVATION_IDS
from engines.detailed_interpretation_engine.luck_activation.labels import (
    DOMAIN_TITLES_ACTIVATION,
    LEVEL_MARKERS,
    STATE_LABELS,
    TITLE,
)
from engines.detailed_interpretation_engine.temporal import LuckActivationResult

_SKIP_STATES = {ActivationState.BLOCKED, ActivationState.UNRESOLVED}


def present_luck_activation_customer(result: LuckActivationResult) -> dict[str, Any]:
    """Compact current-Đại-Vận activation for the existing Luck card."""
    if result.status in {EvaluationStatus.NOT_EVALUATED, EvaluationStatus.NOT_APPLICABLE}:
        return {}
    if not result.items:
        return {}
    order = [item for item in result.order if item in MAIN_ACTIVATION_IDS] or list(MAIN_ACTIVATION_IDS)
    items = [
        _item(result.items[domain_id])
        for domain_id in order
        if domain_id in result.items
    ]
    if not items:
        return {}
    return {
        "title": TITLE,
        "time_window": result.time_window,
        "gan_zhi": _gan_zhi(result),
        "items": items,
    }


def _gan_zhi(result: LuckActivationResult) -> str:
    stem = result.temporal_stem.strip()
    branch = result.temporal_branch.strip()
    if stem and branch:
        return f"{stem} {branch}".strip()
    return ""


def _item(result: Any) -> dict[str, Any]:
    unresolved = result.activation_state in _SKIP_STATES
    marker = _marker(result.support, result.stress)
    return {
        "id": result.domain_id,
        "title": DOMAIN_TITLES_ACTIVATION.get(result.domain_id, result.domain_id),
        "state": result.activation_state.value,
        "state_label": STATE_LABELS.get(result.activation_state.value, result.activation_state.value),
        "driver": "" if unresolved else result.activation_driver,
        "support": "" if unresolved else LEVEL_MARKERS.get(result.support, ""),
        "stress": "" if unresolved else LEVEL_MARKERS.get(result.stress, ""),
        "marker": marker,
        "bottleneck": "" if unresolved else result.activation_bottleneck,
        "conditions": () if unresolved else result.conditions,
        "natal_state": result.natal_state,
        "natal_driver": "" if unresolved else result.natal_driver,
    }


def _marker(support: str, stress: str) -> str:
    if stress in {"high", "excessive"}:
        return "Áp lực"
    if support in {"high", "excessive"}:
        return "Nâng đỡ"
    if support == "moderate":
        return "Nâng đỡ"
    if stress == "moderate":
        return "Áp lực"
    return ""
