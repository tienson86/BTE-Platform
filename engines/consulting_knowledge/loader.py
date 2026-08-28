"""CK-01B catalog loader. Loads stored units. Does not match signals."""

from __future__ import annotations

from engines.consulting_knowledge.catalog import CONSULTING_KNOWLEDGE_CATALOG
from engines.consulting_knowledge.contracts import CONSULTING_DOMAINS, KNOWLEDGE_UNIT_FIELDS
from engines.consulting_knowledge.exceptions import ConsultingKnowledgeError
from engines.consulting_knowledge.models import ConsultingKnowledgeUnit


def load_consulting_knowledge_catalog() -> tuple[ConsultingKnowledgeUnit, ...]:
    """Return the frozen catalog in stored order. Does not match published signals."""
    units = CONSULTING_KNOWLEDGE_CATALOG
    _validate_catalog(units)
    return units


def catalog_by_domain() -> dict[str, tuple[ConsultingKnowledgeUnit, ...]]:
    """Group catalog units by frozen domain. Does not match."""
    grouped: dict[str, list[ConsultingKnowledgeUnit]] = {
        domain: [] for domain in CONSULTING_DOMAINS
    }
    for unit in load_consulting_knowledge_catalog():
        grouped[unit.domain].append(unit)
    return {domain: tuple(items) for domain, items in grouped.items()}


def get_catalog_unit(unit_id: str) -> ConsultingKnowledgeUnit:
    """Return one stored unit by id. Raises if the id is not in the catalog."""
    for unit in load_consulting_knowledge_catalog():
        if unit.unit_id == unit_id:
            return unit
    raise ConsultingKnowledgeError(f"Unknown catalog unit: {unit_id}")


def _validate_catalog(units: tuple[ConsultingKnowledgeUnit, ...]) -> None:
    """Reject duplicate ids, missing domains, or incomplete stored fields."""
    if not units:
        raise ConsultingKnowledgeError("Catalog is empty.")
    seen: set[str] = set()
    domains_present: set[str] = set()
    for unit in units:
        if unit.unit_id in seen:
            raise ConsultingKnowledgeError(f"Duplicate catalog unit_id: {unit.unit_id}")
        seen.add(unit.unit_id)
        domains_present.add(unit.domain)
        payload = unit.to_dict()
        for field in KNOWLEDGE_UNIT_FIELDS:
            value = payload.get(field)
            if value in (None, "", [], {}):
                raise ConsultingKnowledgeError(
                    f"Catalog unit {unit.unit_id} is missing {field}."
                )
    missing = [domain for domain in CONSULTING_DOMAINS if domain not in domains_present]
    if missing:
        raise ConsultingKnowledgeError(f"Catalog missing domains: {missing}")
