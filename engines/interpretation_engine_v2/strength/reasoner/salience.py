"""Salience and relevance scoring."""

from __future__ import annotations

from engines.interpretation_engine_v2.strength.contracts.models import (
    KnowledgeUnit,
    PublishedStrengthFacts,
)
from engines.interpretation_engine_v2.strength.reasoner.budget import (
    PRIORITY_SCORE,
    SPECIFICITY_SCORE,
    VALUE_SCORE,
    WEIGHT_SCORE,
)


class SalienceRanker:
    """Rank eligible units by frozen salience policy."""

    _CAUSE_BONUS: dict[str, int] = {
        "control": 25,
        "root_thin": 20,
        "season": 15,
        "support": 10,
        "special": 5,
    }

    def score(self, unit: KnowledgeUnit, published: PublishedStrengthFacts) -> int:
        """Compute salience score for one unit."""
        total = PRIORITY_SCORE.get(unit.priority.upper(), 60)
        total += VALUE_SCORE.get(unit.customer_value.upper(), 20)
        total += WEIGHT_SCORE.get(unit.narrative_weight.upper(), 5)
        total += SPECIFICITY_SCORE.get(unit.specificity.upper(), 0)

        if unit.purpose == "WHY":
            for fact_key in unit.required_facts:
                if fact_key == "classification":
                    continue
                if published.facts.get(fact_key) is not None:
                    total += self._CAUSE_BONUS.get(fact_key, 0)

        if unit.purpose == "MEANING":
            if unit.strength_class == published.class_id:
                total += 35
            elif unit.strength_class == "all":
                total -= 25

        if unit.strength_class == published.class_id and unit.purpose in {
            "ADVANTAGE",
            "LEADERSHIP",
            "DECISION_MAKING",
            "LEARNING",
            "CHALLENGE",
            "CAREER",
            "MARRIAGE",
            "HEALTH",
            "RECOMMENDATION",
        }:
            total += 15

        if unit.purpose in {"CAREER", "MARRIAGE", "HEALTH"}:
            if "so what" in unit.title.lower():
                total -= 35
            if unit.purpose == "CAREER" and "employment" in unit.title.lower():
                total += 25
            if unit.purpose == "HEALTH" and "balance" in unit.title.lower():
                total += 20
            if unit.purpose == "MARRIAGE" and "bond" in unit.title.lower():
                total += 20

        if unit.purpose == "LEADERSHIP":
            total += 20

        if unit.purpose == "CHALLENGE":
            if unit.duplicate_cluster.upper() not in {"", "NONE"}:
                total += 30
            if any("Name two or three live costs" in item for item in unit.limitations):
                total -= 45

        if unit.purpose == "RECOMMENDATION":
            if unit.knowledge_id in {
                "IK-STR-REC-0036",
                "IK-STR-REC-0037",
                "IK-STR-REC-0038",
            }:
                total += 50
            if unit.knowledge_id == "IK-STR-REC-0008":
                total -= 45
            if "Chain from" in " ".join(unit.limitations):
                total += 10

        if "C1" in published.conflicts:
            if "receptivity" in unit.title.lower():
                total += 25
            if unit.knowledge_id.endswith(("0016", "0010")):
                total += 10

        return total

    def rank(
        self,
        units: list[KnowledgeUnit],
        published: PublishedStrengthFacts,
    ) -> list[KnowledgeUnit]:
        """Return units sorted by salience descending, id ascending."""
        return sorted(
            units,
            key=lambda unit: (-self.score(unit, published), unit.knowledge_id),
        )
