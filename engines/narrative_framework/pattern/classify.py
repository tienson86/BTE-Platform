"""Classify published Pattern evidence relative to the published Cách cục."""

from __future__ import annotations

from typing import Any

from engines.narrative_framework.contracts import INSUFFICIENT_COPY
from engines.narrative_framework.evidence_item import (
    CLASSIFICATION_NEGATIVE,
    CLASSIFICATION_NEUTRAL,
    CLASSIFICATION_POSITIVE,
    NarrativeEvidenceItem,
)
from engines.narrative_framework.pattern.constants import TOPIC_ID
from engines.narrative_framework.pattern.models import (
    PatternEvidence,
    PatternNarrativeEvidencePack,
)


def _item(
    component: str,
    value: Any,
    display: str,
    classification: str,
    reason: str,
    source_path: str,
    confidence: float | None,
    metadata: dict[str, Any] | None = None,
) -> NarrativeEvidenceItem:
    return NarrativeEvidenceItem(
        id=f"{TOPIC_ID}.{component}",
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


def _context_or_missing(
    component: str,
    value: Any,
    display: str,
    source_path: str,
    confidence: float | None,
    role: str,
) -> NarrativeEvidenceItem:
    if value in (None, "", (), []) and not display:
        return _item(
            component,
            None,
            "",
            CLASSIFICATION_NEUTRAL,
            INSUFFICIENT_COPY,
            source_path,
            confidence,
            {"role": role},
        )
    shown = display or str(value)
    return _item(
        component,
        value if value not in (None, "", ()) else shown,
        shown,
        CLASSIFICATION_NEUTRAL,
        shown,
        source_path,
        confidence,
        {"role": role},
    )


def _present_item(
    component: str,
    value: Any,
    display: str,
    classification: str,
    reason: str,
    source_path: str,
    confidence: float | None,
) -> NarrativeEvidenceItem:
    if value in (None, "", (), []) and not display:
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
    shown = display or (reason if reason != INSUFFICIENT_COPY else str(value))
    return _item(
        component,
        value if value not in (None, "") else shown,
        shown,
        classification,
        reason,
        source_path,
        confidence,
        {"role": "directional"},
    )


def classify_pattern_evidence(evidence: PatternEvidence) -> PatternNarrativeEvidencePack:
    """Project PatternEvidence into target-relative classified items."""
    conf = evidence.confidence
    matched_display = " · ".join(evidence.matched_rules)
    items = (
        _context_or_missing(
            "pattern",
            evidence.pattern_class or evidence.pattern_name,
            evidence.pattern_name,
            "pattern.cach_cuc",
            conf,
            "context",
        ),
        _context_or_missing(
            "pattern_type",
            evidence.pattern_type,
            evidence.pattern_type,
            "pattern.follow_type",
            conf,
            "context",
        ),
        _context_or_missing(
            "pattern_class",
            evidence.pattern_class,
            evidence.pattern_class,
            "pattern.pattern",
            conf,
            "context",
        ),
        _context_or_missing(
            "temperature",
            evidence.temperature_state,
            evidence.temperature_state,
            "temperature.climate_state",
            conf,
            "directional",
        ),
        _context_or_missing(
            "dieu_hau",
            evidence.dieu_hau,
            evidence.dieu_hau,
            "pattern.dieu_hau",
            conf,
            "directional",
        ),
        _context_or_missing(
            "special_pattern",
            evidence.special_pattern,
            evidence.special_pattern,
            "pattern.detected_special_pattern",
            conf,
            "context",
        ),
        _present_item(
            "winning_rule",
            evidence.winning_rule,
            evidence.winning_rule,
            CLASSIFICATION_POSITIVE,
            evidence.winning_rule or INSUFFICIENT_COPY,
            "pattern.winning_rule_id",
            conf,
        ),
        _present_item(
            "matched_rules",
            list(evidence.matched_rules) if evidence.matched_rules else None,
            matched_display,
            CLASSIFICATION_POSITIVE,
            matched_display or INSUFFICIENT_COPY,
            "pattern.matched_rules",
            conf,
        ),
        _present_item(
            "success_reason",
            evidence.success_reason,
            evidence.success_reason,
            CLASSIFICATION_POSITIVE,
            evidence.success_reason or INSUFFICIENT_COPY,
            "pattern.success_reason",
            conf,
        ),
        _present_item(
            "failure_reason",
            evidence.failure_reason,
            evidence.failure_reason,
            CLASSIFICATION_NEGATIVE,
            evidence.failure_reason or INSUFFICIENT_COPY,
            "pattern.failure_reason",
            conf,
        ),
        _present_item(
            "clash_status",
            evidence.clash_status,
            evidence.clash_status,
            CLASSIFICATION_NEGATIVE,
            evidence.clash_status or INSUFFICIENT_COPY,
            "pattern.clash_status",
            conf,
        ),
        _present_item(
            "combination_status",
            evidence.combination_status,
            evidence.combination_status,
            CLASSIFICATION_POSITIVE,
            evidence.combination_status or INSUFFICIENT_COPY,
            "pattern.combination_status",
            conf,
        ),
        _context_or_missing(
            "confidence",
            evidence.confidence,
            "" if evidence.confidence is None else str(evidence.confidence),
            "pattern.confidence",
            conf,
            "context",
        ),
        _context_or_missing(
            "reasoning",
            evidence.reasoning,
            evidence.reasoning,
            "pattern.reason",
            conf,
            "context",
        ),
    )
    return PatternNarrativeEvidencePack(raw_evidence=evidence, evidence_items=items)
