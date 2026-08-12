"""Build structured NarrativePlan sections."""

from __future__ import annotations

from engines.interpretation_engine_v2.strength.contracts.models import (
    ClaimTrace,
    KnowledgeUnit,
    LanguageStrength,
    NarrativePlan,
    SectionPlan,
)


class NarrativePlanner:
    """Attach claim traces and normalize section ordering."""

    _ORDER = [
        "CONCLUSION",
        "WHY",
        "MEANING",
        "ADVANTAGE",
        "CHALLENGE",
        "PERSONALITY",
        "CAREER",
        "WEALTH",
        "MARRIAGE",
        "HEALTH",
        "LUCK",
        "RECOMMENDATION",
        "SUMMARY",
    ]

    def finalize(
        self,
        plan: NarrativePlan,
        units_by_id: dict[str, KnowledgeUnit],
    ) -> NarrativePlan:
        """Sort sections and build claim traces."""
        ordered = sorted(
            plan.sections,
            key=lambda section: self._ORDER.index(section.section_id)
            if section.section_id in self._ORDER
            else len(self._ORDER),
        )
        traces = self._build_traces(ordered, units_by_id, plan.primary_conclusion)
        plan.sections = ordered
        plan.diagnostics["claim_traces"] = traces
        return plan

    def _build_traces(
        self,
        sections: list[SectionPlan],
        units_by_id: dict[str, KnowledgeUnit],
        conclusion: dict[str, object],
    ) -> list[dict[str, object]]:
        traces: list[dict[str, object]] = []
        language = LanguageStrength(str(conclusion.get("language_strength", "firm")))
        traces.append(
            {
                "claim_id": "conclusion",
                "customer_section": "CONCLUSION",
                "knowledge_ids": [],
                "reason_codes": [str(conclusion.get("reason_code", ""))],
                "fact_ids": ["classification"],
                "gate_state": "eligible",
                "language_strength": language.value,
                "mode": "customer",
            }
        )
        for section in sections:
            for selected in section.selected_units:
                unit = units_by_id.get(selected.knowledge_id)
                if unit is None:
                    continue
                traces.append(
                    {
                        "claim_id": selected.knowledge_id,
                        "customer_section": section.section_id,
                        "knowledge_ids": [selected.knowledge_id, *selected.merged_with],
                        "reason_codes": [selected.reason_code, *selected.merged_with],
                        "fact_ids": list(unit.required_facts),
                        "gate_state": "eligible",
                        "language_strength": section.language_strength.value,
                        "mode": "customer",
                    }
                )
        return traces
