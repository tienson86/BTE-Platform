"""Classify published Strength evidence relative to Day Master strength."""

from __future__ import annotations

from typing import Any, Mapping

from engines.narrative_framework.contracts import INSUFFICIENT_COPY
from engines.narrative_framework.evidence_item import (
    CLASSIFICATION_NEGATIVE,
    CLASSIFICATION_NEUTRAL,
    CLASSIFICATION_POSITIVE,
    NarrativeEvidenceItem,
)
from engines.narrative_framework.strength.constants import TOPIC_ID
from engines.narrative_framework.strength.models import (
    StrengthEvidence,
    StrengthNarrativeEvidencePack,
)
from engines.strength_engine.labels import strength_level_label

_DIRECTIONAL: tuple[tuple[str, str, str, tuple[str, ...]], ...] = (
    ("season", "season_strength", "strength.season_score", ("Đắc lệnh", "Tướng", "Hưu", "Tù", "Tử")),
    ("root", "root_strength", "strength.root_score", ("Thông căn", "Vô căn", "Căn khí")),
    ("support", "support_strength", "strength.support_score", ("Ấn tinh", "Đồng hành", "trợ thân", "Chính Ấn")),
    ("control", "control_strength", "strength.control_score", ("Quan Sát", "khắc", "xung")),
    ("drain", "drain_strength", "strength.drain_score", ("tiết", "Tài tinh", "hao thân")),
)

_EFFECT_POSITIVE = frozenset({"positive", "support", "increase", "+"})
_EFFECT_NEGATIVE = frozenset({"negative", "weaken", "decrease", "restrain", "-"})


def _sign_class(value: float | None) -> str:
    if value is None or value == 0:
        return CLASSIFICATION_NEUTRAL
    return CLASSIFICATION_POSITIVE if value > 0 else CLASSIFICATION_NEGATIVE


def _published_reason(haystack: str, tokens: tuple[str, ...], fallback: str) -> str:
    for token in tokens:
        if token and token in haystack:
            return token
    return fallback


def _item(
    component: str,
    value: Any,
    display: str,
    classification: str,
    reason: str,
    source_path: str,
    confidence: float | None,
    metadata: Mapping[str, Any] | None = None,
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


def _directional_items(evidence: StrengthEvidence) -> list[NarrativeEvidenceItem]:
    haystack = f"{evidence.reasoning} {evidence.evidence_compact}"
    items: list[NarrativeEvidenceItem] = []
    for component, field, path, tokens in _DIRECTIONAL:
        value = getattr(evidence, field)
        classification = _sign_class(value)
        if value is None:
            reason = INSUFFICIENT_COPY
            display = ""
        elif value == 0:
            reason = INSUFFICIENT_COPY
            display = "0"
        else:
            reason = _published_reason(haystack, tokens, f"{component} đã công bố")
            display = str(value)
        items.append(
            _item(
                component,
                value,
                display,
                classification,
                reason,
                path,
                evidence.confidence,
                {"role": "directional"},
            )
        )
    return items


def _published_effect(raw: Mapping[str, Any]) -> str:
    for key in ("classification", "effect", "polarity", "strength_effect", "day_master_effect"):
        token = str(raw.get(key) or "").strip().lower()
        if token in _EFFECT_POSITIVE:
            return CLASSIFICATION_POSITIVE
        if token in _EFFECT_NEGATIVE:
            return CLASSIFICATION_NEGATIVE
    if "score" in raw and raw.get("score") not in (None, ""):
        try:
            return _sign_class(float(raw["score"]))
        except (TypeError, ValueError):
            return CLASSIFICATION_NEUTRAL
    return CLASSIFICATION_NEUTRAL


def _special_items(evidence: StrengthEvidence) -> list[NarrativeEvidenceItem]:
    items: list[NarrativeEvidenceItem] = []
    details = {str(row.get("rule_id") or row.get("id") or ""): row for row in evidence.special_rule_details}
    seen: set[str] = set()
    for index, rule_id in enumerate(evidence.special_rules):
        row = details.get(rule_id, {})
        seen.add(rule_id)
        classification = _published_effect(row) if row else CLASSIFICATION_NEUTRAL
        reason = str(row.get("reason") or row.get("description") or "").strip() or INSUFFICIENT_COPY
        items.append(
            _item(
                "special_rules",
                rule_id,
                rule_id,
                classification,
                reason,
                "strength.metadata.trace.analysis.special_matches",
                evidence.confidence,
                {"role": "directional", "index": index, "rule_id": rule_id},
                item_id=f"{TOPIC_ID}.special_rules.{rule_id or index}",
            )
        )
    for row in evidence.special_rule_details:
        rule_id = str(row.get("rule_id") or row.get("id") or "").strip()
        if rule_id in seen:
            continue
        items.append(
            _item(
                "special_rules",
                rule_id or None,
                rule_id,
                _published_effect(row),
                str(row.get("reason") or "").strip() or INSUFFICIENT_COPY,
                "strength.metadata.trace.analysis.special_matches",
                evidence.confidence,
                {"role": "directional", "rule_id": rule_id},
            )
        )
    if not items:
        items.append(
            _item(
                "special_rules",
                None,
                "",
                CLASSIFICATION_NEUTRAL,
                INSUFFICIENT_COPY,
                "strength.metadata.trace.analysis.special_matches",
                evidence.confidence,
                {"role": "directional"},
            )
        )
    return items


def _temperature_item(evidence: StrengthEvidence) -> NarrativeEvidenceItem:
    state = evidence.temperature_state
    if not state:
        return _item(
            "temperature",
            None,
            "",
            CLASSIFICATION_NEUTRAL,
            INSUFFICIENT_COPY,
            "temperature.climate_state",
            evidence.confidence,
            {"role": "directional", "state_preserved": True},
        )
    return _item(
        "temperature",
        state,
        state,
        CLASSIFICATION_NEUTRAL,
        state,
        "temperature.climate_state",
        evidence.confidence,
        {"role": "directional", "state_preserved": True},
    )


def _context_items(evidence: StrengthEvidence) -> list[NarrativeEvidenceItem]:
    label = strength_level_label(evidence.strength_level)
    score_display = "" if evidence.score is None else str(evidence.score)
    conf_display = "" if evidence.confidence is None else str(evidence.confidence)
    return [
        _item(
            "strength_level",
            evidence.strength_level,
            label,
            CLASSIFICATION_NEUTRAL,
            label or INSUFFICIENT_COPY,
            "strength.strength_level",
            evidence.confidence,
            {"role": "context"},
        ),
        _item(
            "score",
            evidence.score,
            score_display,
            CLASSIFICATION_NEUTRAL,
            score_display or INSUFFICIENT_COPY,
            "strength.strength_score",
            evidence.confidence,
            {"role": "context"},
        ),
        _item(
            "confidence",
            evidence.confidence,
            conf_display,
            CLASSIFICATION_NEUTRAL,
            conf_display or INSUFFICIENT_COPY,
            "strength.confidence",
            evidence.confidence,
            {"role": "context"},
        ),
    ]


def classify_strength_evidence(evidence: StrengthEvidence) -> StrengthNarrativeEvidencePack:
    """Project StrengthEvidence into target-relative classified items."""
    items = (
        _directional_items(evidence)
        + [_temperature_item(evidence)]
        + _special_items(evidence)
        + _context_items(evidence)
    )
    return StrengthNarrativeEvidencePack(raw_evidence=evidence, evidence_items=tuple(items))


def apply_temperature_strength_effect(
    pack: StrengthNarrativeEvidencePack,
    temperature: Mapping[str, Any] | None,
) -> StrengthNarrativeEvidencePack:
    """Override temperature polarity only from explicit published Strength effect."""
    if not temperature:
        return pack
    effect = _published_effect(temperature)
    if effect == CLASSIFICATION_NEUTRAL:
        return pack
    updated: list[NarrativeEvidenceItem] = []
    for item in pack.evidence_items:
        if item.component != "temperature":
            updated.append(item)
            continue
        reason = str(
            temperature.get("strength_effect_reason")
            or temperature.get("reason")
            or item.reason
        )
        updated.append(
            NarrativeEvidenceItem(
                id=item.id,
                topic=item.topic,
                component=item.component,
                classification=effect,
                source_path=item.source_path,
                value=item.value,
                display_value=item.display_value,
                reason=reason,
                confidence=item.confidence,
                metadata={**dict(item.metadata), "explicit_strength_effect": True},
            )
        )
    return StrengthNarrativeEvidencePack(raw_evidence=pack.raw_evidence, evidence_items=tuple(updated))
