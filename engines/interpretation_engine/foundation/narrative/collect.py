"""Copy already-validated knowledge statements. Do not invent content."""

from __future__ import annotations

from typing import Any, Iterable, Mapping

from engines.interpretation_engine.foundation.knowledge.entity import KnowledgeEntity
from engines.interpretation_engine.foundation.narrative.constants import (
    KIND_APPLICATION,
    KIND_CONCLUSION,
    KIND_RECOMMENDATION,
    KIND_WARNING,
    SLOT_CONCLUSION,
    SLOT_IMPACT,
    SLOT_RECOMMENDATION,
    SLOT_WARNING,
)
from engines.interpretation_engine.foundation.narrative.input import CopiedStatement
from engines.interpretation_engine.foundation.narrative.mapping import map_customer_domain
from engines.interpretation_engine.foundation.narrative.text import normalize_text


def copy_statement(
    text: str,
    *,
    kind: str,
    slot: str,
    engine_truth_ref: str,
    customer_domain: str = "",
    category: str = "",
    rationale: str = "",
    condition: str = "",
    mitigation: str = "",
    confidence: float = 0.0,
) -> CopiedStatement | None:
    """Copy one non-empty statement. Empty text is dropped, not inferred."""
    cleaned = normalize_text(text)
    if not cleaned:
        return None
    mapped = map_customer_domain(customer_domain) if customer_domain else ""
    return CopiedStatement(
        text=cleaned,
        kind=kind,
        slot=slot,
        engine_truth_ref=engine_truth_ref,
        customer_domain=mapped,
        category=normalize_text(category),
        rationale=normalize_text(rationale),
        condition=normalize_text(condition),
        mitigation=normalize_text(mitigation),
        confidence=confidence,
    )


def extend_copied(target: list[CopiedStatement], item: CopiedStatement | None) -> None:
    """Append a copied statement when present."""
    if item is not None:
        target.append(item)


def copy_knowledge_entity(
    entity: KnowledgeEntity,
    *,
    confidence: float,
) -> tuple[CopiedStatement, ...]:
    """Copy expert meaning, applications, recommendations, and warnings."""
    prefix = f"knowledge:{entity.domain}:{entity.key}"
    items: list[CopiedStatement] = []
    extend_copied(
        items,
        copy_statement(
            entity.meaning,
            kind=KIND_CONCLUSION,
            slot=SLOT_CONCLUSION,
            engine_truth_ref=f"{prefix}:meaning",
            confidence=confidence,
        ),
    )
    extend_copied(
        items,
        copy_statement(
            entity.positive_meaning,
            kind=KIND_CONCLUSION,
            slot=SLOT_CONCLUSION,
            engine_truth_ref=f"{prefix}:positive_meaning",
            confidence=confidence,
        ),
    )
    for area, text in dict(entity.applications).items():
        extend_copied(
            items,
            copy_statement(
                str(text),
                kind=KIND_APPLICATION,
                slot=SLOT_IMPACT,
                engine_truth_ref=f"{prefix}:applications:{area}",
                customer_domain=str(area),
                confidence=confidence,
            ),
        )
    for rec in entity.recommendations:
        _copy_recommendation(items, rec, prefix=prefix, confidence=confidence)
    for warning in entity.warnings:
        _copy_warning(items, warning, prefix=prefix, confidence=confidence)
    return tuple(items)


def copy_mapping_recommendations(
    rows: Iterable[Mapping[str, Any]],
    *,
    prefix: str,
    confidence: float,
) -> tuple[CopiedStatement, ...]:
    """Copy structured recommendation mappings already produced upstream."""
    items: list[CopiedStatement] = []
    for rec in rows:
        _copy_recommendation(items, rec, prefix=prefix, confidence=confidence)
    return tuple(items)


def copy_mapping_warnings(
    rows: Iterable[Mapping[str, Any]],
    *,
    prefix: str,
    confidence: float,
) -> tuple[CopiedStatement, ...]:
    """Copy structured warning mappings already produced upstream."""
    items: list[CopiedStatement] = []
    for warning in rows:
        _copy_warning(items, warning, prefix=prefix, confidence=confidence)
    return tuple(items)


def _copy_recommendation(
    items: list[CopiedStatement],
    rec: Mapping[str, Any],
    *,
    prefix: str,
    confidence: float,
) -> None:
    """Copy one recommendation mapping if it has an action."""
    payload = dict(rec)
    action = str(payload.get("action") or payload.get("item") or "").strip()
    category = str(payload.get("category") or "")
    rationale = str(payload.get("rationale") or "")
    domain = str(payload.get("domain") or payload.get("area") or category)
    extend_copied(
        items,
        copy_statement(
            action,
            kind=KIND_RECOMMENDATION,
            slot=SLOT_RECOMMENDATION,
            engine_truth_ref=f"{prefix}:recommendation:{category or action[:40]}",
            customer_domain=domain,
            category=category,
            rationale=rationale,
            confidence=confidence,
        ),
    )


def _copy_warning(
    items: list[CopiedStatement],
    warning: Mapping[str, Any],
    *,
    prefix: str,
    confidence: float,
) -> None:
    """Copy one warning mapping if it has a risk statement."""
    payload = dict(warning)
    risk = str(payload.get("risk") or payload.get("text") or "").strip()
    condition = str(payload.get("condition") or "")
    mitigation = str(payload.get("mitigation") or "")
    extend_copied(
        items,
        copy_statement(
            risk,
            kind=KIND_WARNING,
            slot=SLOT_WARNING,
            engine_truth_ref=f"{prefix}:warning:{condition or risk[:40]}",
            condition=condition,
            mitigation=mitigation,
            confidence=confidence,
        ),
    )
