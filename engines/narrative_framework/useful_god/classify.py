"""Classify published Useful God evidence relative to the published Dụng thần."""

from __future__ import annotations

from typing import Any

from engines.narrative_framework.contracts import INSUFFICIENT_COPY
from engines.narrative_framework.evidence_item import (
    CLASSIFICATION_NEGATIVE,
    CLASSIFICATION_NEUTRAL,
    CLASSIFICATION_POSITIVE,
    NarrativeEvidenceItem,
)
from engines.narrative_framework.useful_god.constants import TOPIC_ID
from engines.narrative_framework.useful_god.models import (
    UsefulGodEvidence,
    UsefulGodNarrativeEvidencePack,
)

_LAYER_REASONS: tuple[tuple[str, str, str], ...] = (
    ("strength_reason", "strength_reason", "useful_god.strength_reason"),
    ("season_reason", "season_reason", "useful_god.season_reason"),
    ("temperature_reason", "temperature_reason", "useful_god.temperature_reason"),
    ("balance_reason", "balance_reason", "useful_god.balance_reason"),
)


def _is_unpublished_display(text: str) -> bool:
    stripped = text.strip()
    if not stripped:
        return True
    if stripped == INSUFFICIENT_COPY:
        return True
    return stripped.startswith("Chưa")


def _item(
    component: str,
    value: Any,
    display: str,
    classification: str,
    reason: str,
    source_path: str,
    confidence: float | None,
    metadata: dict[str, Any] | None = None,
    item_id: str | None = None,
) -> NarrativeEvidenceItem:
    return NarrativeEvidenceItem(
        id=item_id or f"{TOPIC_ID}.{component}",
        topic=TOPIC_ID,
        component=component,
        value=value,
        display_value=display,
        classification=classification,
        reason=reason,
        source_path=source_path,
        confidence=confidence,
        metadata=dict(metadata or {}),
    )


def _target_item(evidence: UsefulGodEvidence) -> NarrativeEvidenceItem:
    display = evidence.useful_display or evidence.useful_god
    if not display:
        return _item(
            "useful_god",
            None,
            "",
            CLASSIFICATION_NEUTRAL,
            INSUFFICIENT_COPY,
            "useful_god.useful_display",
            evidence.confidence,
            {"role": "context"},
        )
    return _item(
        "useful_god",
        evidence.useful_god or display,
        display,
        CLASSIFICATION_NEUTRAL,
        display,
        "useful_god.useful_display",
        evidence.confidence,
        {"role": "context"},
    )


def _list_item(
    component: str,
    values: tuple[str, ...],
    display: str,
    present_class: str,
    fallback_reason: str,
    source_path: str,
    confidence: float | None,
) -> NarrativeEvidenceItem:
    unpublished = _is_unpublished_display(display) and not values
    if unpublished:
        return _item(
            component,
            None,
            "",
            CLASSIFICATION_NEUTRAL,
            INSUFFICIENT_COPY,
            source_path,
            confidence,
            {"role": "directional"},
        )
    shown = display or " · ".join(values)
    reason = display if display and not _is_unpublished_display(display) else fallback_reason
    if values and not display:
        reason = fallback_reason
    return _item(
        component,
        list(values) or shown,
        shown,
        present_class,
        reason,
        source_path,
        confidence,
        {"role": "directional"},
    )


def _winning_item(evidence: UsefulGodEvidence) -> NarrativeEvidenceItem:
    if not evidence.winning_rule_id:
        return _item(
            "winning_rule",
            None,
            "",
            CLASSIFICATION_NEUTRAL,
            INSUFFICIENT_COPY,
            "useful_god.winning_rule_id",
            evidence.confidence,
            {"role": "directional"},
        )
    return _item(
        "winning_rule",
        evidence.winning_rule_id,
        evidence.winning_rule_id,
        CLASSIFICATION_POSITIVE,
        evidence.winning_rule_id,
        "useful_god.winning_rule_id",
        evidence.confidence,
        {"role": "directional", "rule_group": evidence.winning_rule_group},
    )


def _matched_item(evidence: UsefulGodEvidence) -> NarrativeEvidenceItem:
    if not evidence.matched_rules:
        return _item(
            "matched_rules",
            None,
            "",
            CLASSIFICATION_NEUTRAL,
            INSUFFICIENT_COPY,
            "useful_god.matched_rules",
            evidence.confidence,
            {"role": "directional"},
        )
    display = " · ".join(evidence.matched_rules)
    return _item(
        "matched_rules",
        list(evidence.matched_rules),
        display,
        CLASSIFICATION_POSITIVE,
        display,
        "useful_god.matched_rules",
        evidence.confidence,
        {"role": "directional"},
    )


def _climate_item(evidence: UsefulGodEvidence) -> NarrativeEvidenceItem:
    state = evidence.climate_display
    if not state:
        return _item(
            "climate",
            None,
            "",
            CLASSIFICATION_NEUTRAL,
            INSUFFICIENT_COPY,
            "useful_god.climate_display",
            evidence.confidence,
            {"role": "directional", "state_preserved": True},
        )
    return _item(
        "climate",
        state,
        state,
        CLASSIFICATION_NEUTRAL,
        evidence.climate_reason or state,
        "useful_god.climate_display",
        evidence.confidence,
        {"role": "directional", "state_preserved": True},
    )


def _layer_items(evidence: UsefulGodEvidence) -> list[NarrativeEvidenceItem]:
    items: list[NarrativeEvidenceItem] = []
    for component, field, path in _LAYER_REASONS:
        text = str(getattr(evidence, field) or "").strip()
        if not text:
            continue
        items.append(
            _item(
                component,
                text,
                text,
                CLASSIFICATION_POSITIVE,
                text,
                path,
                evidence.confidence,
                {"role": "directional"},
            )
        )
    return items


def _context_items(evidence: UsefulGodEvidence) -> list[NarrativeEvidenceItem]:
    conf_display = "" if evidence.confidence is None else str(evidence.confidence)
    reasoning_display = evidence.reasoning
    return [
        _item(
            "confidence",
            evidence.confidence,
            conf_display,
            CLASSIFICATION_NEUTRAL,
            conf_display or INSUFFICIENT_COPY,
            "useful_god.confidence",
            evidence.confidence,
            {"role": "context"},
        ),
        _item(
            "reasoning",
            reasoning_display or None,
            reasoning_display,
            CLASSIFICATION_NEUTRAL,
            reasoning_display or INSUFFICIENT_COPY,
            "useful_god.reasoning",
            evidence.confidence,
            {"role": "context"},
        ),
    ]


def classify_useful_god_evidence(evidence: UsefulGodEvidence) -> UsefulGodNarrativeEvidencePack:
    """Project UsefulGodEvidence into target-relative classified items."""
    items = (
        [
            _target_item(evidence),
            _list_item(
                "favorable",
                evidence.favorable_gods,
                evidence.favorable_display,
                CLASSIFICATION_POSITIVE,
                "Hỷ thần",
                "useful_god.favorable_display",
                evidence.confidence,
            ),
            _list_item(
                "unfavorable",
                evidence.unfavorable_gods,
                evidence.unfavorable_display,
                CLASSIFICATION_NEGATIVE,
                "Kỵ thần",
                "useful_god.unfavorable_display",
                evidence.confidence,
            ),
            _winning_item(evidence),
            _matched_item(evidence),
            _climate_item(evidence),
        ]
        + _layer_items(evidence)
        + _context_items(evidence)
    )
    return UsefulGodNarrativeEvidencePack(raw_evidence=evidence, evidence_items=tuple(items))
