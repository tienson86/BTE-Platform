"""Compose commercial consulting sections from matched knowledge units.

Does not match. Does not calculate. Does not call consulting_knowledge matching.
"""

from __future__ import annotations

from typing import Any, Mapping, Sequence

from engines.commercial_composer.consulting_models import (
    CommercialComposerInput,
    CommercialComposerResult,
    CommercialConsultingSection,
    empty_commercial_composer_result,
)
from engines.commercial_composer.exceptions import CommercialComposerError
from engines.consulting_knowledge.contracts import CONSULTING_DOMAINS, DOMAIN_TITLES_VI
from engines.consulting_knowledge.models import ConsultingKnowledgeUnit


def compose_commercial_consulting(
    payload: CommercialComposerInput | Mapping[str, Any] | Sequence[Any] | None = None,
    *,
    matched_units: Sequence[Any] | None = None,
    analysis: Mapping[str, Any] | None = None,
) -> CommercialComposerResult:
    """Group matched catalog units into commercial consulting sections.

    Composer is a consumer. It does not rematch published signals.
    """
    _ = analysis
    units = _resolve_units(payload, matched_units)
    if not units:
        return empty_commercial_composer_result()
    sections = tuple(
        section
        for domain in CONSULTING_DOMAINS
        if (section := _compose_domain(domain, units)) is not None
    )
    if not sections:
        return empty_commercial_composer_result()
    return CommercialComposerResult(sections=sections, status="complete")


def stable_unique(items: Sequence[str]) -> tuple[str, ...]:
    """Drop exact duplicates while keeping first-occurrence order."""
    seen: set[str] = set()
    ordered: list[str] = []
    for item in items:
        text = item.strip() if isinstance(item, str) else str(item).strip()
        if not text or text in seen:
            continue
        seen.add(text)
        ordered.append(text)
    return tuple(ordered)


def _resolve_units(
    payload: CommercialComposerInput | Mapping[str, Any] | Sequence[Any] | None,
    matched_units: Sequence[Any] | None,
) -> tuple[ConsultingKnowledgeUnit, ...]:
    """Read matched units from the composer input. Do not match a catalog."""
    if isinstance(payload, CommercialComposerInput):
        return tuple(payload.matched_units)
    if isinstance(payload, Mapping) and "matched_units" in payload:
        return tuple(_as_unit(item) for item in payload["matched_units"] or ())
    if isinstance(payload, Sequence) and not isinstance(payload, (str, bytes)):
        return tuple(_as_unit(item) for item in payload)
    if matched_units is not None:
        return tuple(_as_unit(item) for item in matched_units)
    return ()


def _as_unit(item: Any) -> ConsultingKnowledgeUnit:
    """Accept a stored unit or an equivalent mapping. Do not invent fields."""
    if isinstance(item, ConsultingKnowledgeUnit):
        return item
    if not isinstance(item, Mapping):
        raise CommercialComposerError("matched_units entries must be knowledge units.")
    wording = item.get("customer_wording") or ()
    actions = item.get("recommended_actions") or ()
    refs = item.get("references") or ()
    return ConsultingKnowledgeUnit(
        unit_id=str(item.get("unit_id") or ""),
        domain=str(item.get("domain") or ""),
        condition=dict(item.get("condition") or {}),
        applicable_scope=dict(item.get("applicable_scope") or {}),
        consulting_meaning=str(item.get("consulting_meaning") or ""),
        customer_wording=tuple(wording),
        recommended_actions=tuple(actions),
        references=tuple(refs),
        status=str(item.get("status") or "complete"),
    )


def _compose_domain(
    domain: str,
    units: Sequence[ConsultingKnowledgeUnit],
) -> CommercialConsultingSection | None:
    """Build one section from units already in this domain. Omit if none match."""
    grouped = tuple(unit for unit in units if unit.domain == domain)
    if not grouped:
        return None
    wording = stable_unique(
        line for unit in grouped for line in unit.customer_wording
    )
    meaning = stable_unique(
        unit.consulting_meaning for unit in grouped if unit.consulting_meaning.strip()
    )
    recommendations = stable_unique(
        line for unit in grouped for line in unit.recommended_actions
    )
    references = stable_unique(line for unit in grouped for line in unit.references)
    source_ids = stable_unique(unit.unit_id for unit in grouped)
    if not wording or not source_ids:
        return None
    return CommercialConsultingSection(
        domain=domain,
        title=DOMAIN_TITLES_VI[domain],
        summary=" ".join(wording),
        meaning=meaning,
        recommendations=recommendations,
        references=references,
        source_unit_ids=source_ids,
    )
