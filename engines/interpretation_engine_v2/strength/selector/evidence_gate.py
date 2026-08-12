"""Evidence gate for catalog units."""

from __future__ import annotations

from engines.interpretation_engine_v2.strength.contracts.models import (
    EvidenceState,
    GateResult,
    GateState,
    KnowledgeUnit,
    PublishedStrengthFacts,
)


class EvidenceGate:
    """Reject knowledge without required published evidence."""

    _CLASS_ONLY = "CLASS_ONLY"

    def evaluate(
        self,
        unit: KnowledgeUnit,
        published: PublishedStrengthFacts,
    ) -> GateResult:
        """Evaluate one unit against published facts."""
        if not self._class_matches(unit.strength_class, published.class_id):
            return GateResult(
                knowledge_id=unit.knowledge_id,
                state=GateState.INELIGIBLE,
                reason_code="REJECTED_CLASS_MISMATCH",
            )

        missing: list[str] = []
        partial = False
        for fact_key in unit.required_facts:
            if fact_key == "classification":
                continue
            state = published.facts.get(fact_key, EvidenceState.MISSING)
            if state == EvidenceState.MISSING:
                missing.append(fact_key)
            elif state == EvidenceState.INACTIVE:
                return GateResult(
                    knowledge_id=unit.knowledge_id,
                    state=GateState.INELIGIBLE,
                    reason_code="REJECTED_FACT_INACTIVE",
                    missing_required=[fact_key],
                )
            elif state in {EvidenceState.INSUFFICIENT, EvidenceState.NOT_APPLICABLE}:
                return GateResult(
                    knowledge_id=unit.knowledge_id,
                    state=GateState.INELIGIBLE,
                    reason_code="REJECTED_NOT_APPLICABLE"
                    if state == EvidenceState.NOT_APPLICABLE
                    else "REJECTED_INSUFFICIENT_EVIDENCE",
                    missing_required=[fact_key],
                )
            elif state == EvidenceState.PARTIAL:
                partial = True

        if missing:
            return GateResult(
                knowledge_id=unit.knowledge_id,
                state=GateState.INELIGIBLE,
                reason_code="REJECTED_MISSING_EVIDENCE",
                missing_required=missing,
            )

        for condition in unit.forbidden_conditions:
            if published.forbidden_flags.get(condition, False):
                reason_code = "REJECTED_FACT_INACTIVE"
                if condition != "drain_inactive":
                    reason_code = "REJECTED_FORBIDDEN_CONDITION"
                return GateResult(
                    knowledge_id=unit.knowledge_id,
                    state=GateState.INELIGIBLE,
                    reason_code=reason_code,
                    forbidden_hit=[condition],
                )

        if partial and unit.required_evidence.upper() != self._CLASS_ONLY:
            return GateResult(
                knowledge_id=unit.knowledge_id,
                state=GateState.PARTIALLY_SUPPORTED,
                reason_code="REJECTED_PARTIAL_AS_FIRM",
            )

        if unit.required_evidence.upper() == self._CLASS_ONLY:
            if "classification" not in published.facts:
                return GateResult(
                    knowledge_id=unit.knowledge_id,
                    state=GateState.INELIGIBLE,
                    reason_code="REJECTED_MISSING_EVIDENCE",
                    missing_required=["classification"],
                )

        return GateResult(
            knowledge_id=unit.knowledge_id,
            state=GateState.ELIGIBLE,
            reason_code="SELECTED_REQUIRED_SECTION",
        )

    def evaluate_all(
        self,
        units: list[KnowledgeUnit],
        published: PublishedStrengthFacts,
    ) -> dict[str, GateResult]:
        """Evaluate all units."""
        return {unit.knowledge_id: self.evaluate(unit, published) for unit in units}

    @staticmethod
    def _class_matches(unit_class: str, class_id: str) -> bool:
        if unit_class in {"all", "edge"}:
            return True
        return unit_class == class_id
