"""Duplicate cluster resolution."""

from __future__ import annotations

from engines.interpretation_engine_v2.strength.contracts.models import KnowledgeUnit
from engines.interpretation_engine_v2.strength.reasoner.budget import (
    CLUSTER_REPRESENTATIVES,
    CLUSTER_REPRESENTATIVES_REC,
)


class DuplicateResolver:
    """Keep one representative per duplicate cluster."""

    def resolve(
        self,
        units: list[KnowledgeUnit],
        section_id: str = "",
    ) -> tuple[list[KnowledgeUnit], list[tuple[str, str]]]:
        """Return kept units and rejected (id, reason) pairs."""
        kept: list[KnowledgeUnit] = []
        rejected: list[tuple[str, str]] = []
        seen_clusters: dict[str, KnowledgeUnit] = {}
        representative_map = CLUSTER_REPRESENTATIVES
        if section_id == "RECOMMENDATION":
            representative_map = {**CLUSTER_REPRESENTATIVES, **CLUSTER_REPRESENTATIVES_REC}

        for unit in units:
            cluster = unit.duplicate_cluster.upper()
            if cluster in {"", "NONE"}:
                kept.append(unit)
                continue

            representative = representative_map.get(cluster)
            if representative and unit.knowledge_id != representative:
                if any(item.knowledge_id == representative for item in units):
                    rejected.append((unit.knowledge_id, "REJECTED_DUPLICATE"))
                    continue

            if cluster not in seen_clusters:
                seen_clusters[cluster] = unit
                kept.append(unit)
                continue

            existing = seen_clusters[cluster]
            if self._prefer(unit, existing):
                rejected.append((existing.knowledge_id, "REJECTED_DUPLICATE"))
                kept.remove(existing)
                seen_clusters[cluster] = unit
                kept.append(unit)
            else:
                rejected.append((unit.knowledge_id, "REJECTED_DUPLICATE"))

        return kept, rejected

    @staticmethod
    def _prefer(candidate: KnowledgeUnit, incumbent: KnowledgeUnit) -> bool:
        weight_order = {"CORE": 3, "SUPPORTING": 2, "OPTIONAL": 1, "DETAIL": 0}
        candidate_weight = weight_order.get(candidate.narrative_weight.upper(), 0)
        incumbent_weight = weight_order.get(incumbent.narrative_weight.upper(), 0)
        if candidate_weight != incumbent_weight:
            return candidate_weight > incumbent_weight
        value_order = {"CRITICAL": 4, "HIGH": 3, "MEDIUM": 2, "LOW": 1}
        candidate_value = value_order.get(candidate.customer_value.upper(), 0)
        incumbent_value = value_order.get(incumbent.customer_value.upper(), 0)
        if candidate_value != incumbent_value:
            return candidate_value > incumbent_value
        return candidate.knowledge_id > incumbent.knowledge_id
