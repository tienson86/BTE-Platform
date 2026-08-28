"""Classify published Luck evidence relative to the published Luck reading."""

from __future__ import annotations

from typing import Any

from engines.narrative_framework.contracts import INSUFFICIENT_COPY
from engines.narrative_framework.evidence_item import (
    CLASSIFICATION_NEGATIVE,
    CLASSIFICATION_NEUTRAL,
    CLASSIFICATION_POSITIVE,
    NarrativeEvidenceItem,
)
from engines.narrative_framework.luck.constants import TOPIC_ID
from engines.narrative_framework.luck.models import LuckEvidence, LuckNarrativeEvidencePack


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


def _context(
    component: str,
    value: Any,
    display: str,
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
            {"role": "context"},
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
        {"role": "context"},
    )


def _group(
    component: str,
    values: tuple[str, ...],
    classification: str,
    fallback: str,
    source_path: str,
    confidence: float | None,
) -> NarrativeEvidenceItem:
    if not values:
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
    display = " · ".join(values)
    return _item(
        component,
        list(values),
        display,
        classification,
        display or fallback,
        source_path,
        confidence,
        {"role": "directional"},
    )


def classify_luck_evidence(evidence: LuckEvidence) -> LuckNarrativeEvidencePack:
    """Project LuckEvidence into target-relative classified items."""
    conf = evidence.confidence
    items = (
        _context(
            "current_cycle",
            evidence.current_cycle,
            evidence.current_cycle,
            "luck.current_dayun",
            conf,
        ),
        _context(
            "current_liunian",
            evidence.current_liunian,
            evidence.current_liunian,
            "luck.current_liunian",
            conf,
        ),
        _context(
            "cycle_index",
            evidence.cycle_index,
            "" if evidence.cycle_index is None else str(evidence.cycle_index),
            "luck.current_dayun.index",
            conf,
        ),
        _context(
            "age",
            evidence.age,
            "" if evidence.age is None else str(evidence.age),
            "luck.current_dayun.start_age",
            conf,
        ),
        _context(
            "reference_year",
            evidence.reference_year,
            "" if evidence.reference_year is None else str(evidence.reference_year),
            "luck.reference_year",
            conf,
        ),
        _context(
            "timeline",
            evidence.timeline,
            evidence.timeline,
            "luck.timeline",
            conf,
        ),
        _group(
            "support",
            evidence.support_elements,
            CLASSIFICATION_POSITIVE,
            "hỗ trợ",
            "luck.support_elements",
            conf,
        ),
        _group(
            "attack",
            evidence.attack_elements,
            CLASSIFICATION_NEGATIVE,
            "xung khắc",
            "luck.attack_elements",
            conf,
        ),
        _context(
            "luck_stage",
            evidence.luck_stage,
            evidence.luck_stage,
            "luck.luck_stage",
            conf,
        ),
        _context(
            "confidence",
            evidence.confidence,
            "" if evidence.confidence is None else str(evidence.confidence),
            "luck.confidence",
            conf,
        ),
        _context(
            "reasoning",
            evidence.reasoning,
            evidence.reasoning,
            "luck.luck_summary",
            conf,
        ),
    )
    return LuckNarrativeEvidencePack(raw_evidence=evidence, evidence_items=items)
