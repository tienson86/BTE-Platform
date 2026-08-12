"""Candidate knowledge selection."""

from __future__ import annotations

from engines.interpretation_engine_v2.strength.contracts.models import (
    AudienceMode,
    KnowledgeUnit,
    PublishedStrengthFacts,
)


class KnowledgeSelector:
    """Select catalog candidates for a published Strength case."""

    _EXAMPLE_TOPIC = "examples"

    def select_candidates(
        self,
        units: list[KnowledgeUnit],
        published: PublishedStrengthFacts,
        audience: AudienceMode = AudienceMode.CUSTOMER,
    ) -> list[KnowledgeUnit]:
        """Return units that match class gate and mode visibility."""
        class_id = published.class_id
        selected: list[KnowledgeUnit] = []
        for unit in units:
            if unit.topic == self._EXAMPLE_TOPIC:
                continue
            if not self._class_matches(unit.strength_class, class_id):
                continue
            if audience == AudienceMode.CUSTOMER and unit.customer_mode != "ALLOWED":
                continue
            if audience == AudienceMode.VALIDATION and unit.validation_mode != "ALLOWED":
                continue
            selected.append(unit)
        return selected

    @staticmethod
    def _class_matches(unit_class: str, class_id: str) -> bool:
        if unit_class in {"all", "edge"}:
            return True
        return unit_class == class_id
