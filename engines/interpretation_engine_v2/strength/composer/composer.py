"""Compose customer and validation prose from NarrativePlan."""

from __future__ import annotations

from engines.interpretation_engine_v2.strength.contracts.models import (
    ComposedSection,
    KnowledgeUnit,
    LanguageStrength,
    NarrativePlan,
    SectionPlan,
)

_CLASS_LABELS = {
    "very_strong": "Very Strong",
    "strong": "Strong",
    "balanced": "Balanced",
    "weak": "Weak",
    "very_weak": "Very Weak",
}

_SECTION_TITLES = {
    "CONCLUSION": "Conclusion",
    "WHY": "Why",
    "MEANING": "Meaning",
    "ADVANTAGE": "Advantages",
    "CHALLENGE": "Challenges",
    "CAREER": "Career",
    "MARRIAGE": "Marriage",
    "HEALTH": "Health",
    "LUCK": "Luck Cycles",
    "RECOMMENDATION": "Recommendations",
    "SUMMARY": "Executive Summary",
}


class SentenceComposer:
    """Deterministic sentence composer — no LLM."""

    def compose_customer(
        self,
        plan: NarrativePlan,
        units_by_id: dict[str, KnowledgeUnit],
    ) -> list[ComposedSection]:
        """Compose Mode B — Customer sections."""
        sections: list[ComposedSection] = []
        sections.append(self._compose_conclusion(plan))
        for section in plan.sections:
            if section.section_id == "SUMMARY":
                continue
            composed = self._compose_section(section, units_by_id, customer=True)
            if composed.paragraphs:
                sections.append(composed)
        sections.append(self._compose_executive_summary(plan, units_by_id))
        return sections

    def compose_validation(
        self,
        plan: NarrativePlan,
        units_by_id: dict[str, KnowledgeUnit],
    ) -> list[ComposedSection]:
        """Compose Mode A — Validation sections."""
        sections = self.compose_customer(plan, units_by_id)
        sections.insert(
            1,
            ComposedSection(
                section_id="EVIDENCE",
                title="Evidence",
                paragraphs=self._evidence_paragraphs(plan),
            ),
        )
        sections.append(
            ComposedSection(
                section_id="CONFIDENCE",
                title="Confidence",
                paragraphs=[f"Interpretation confidence band: {plan.meta.get('confidence_band', 'high')}."],
            ),
        )
        if plan.alternative:
            sections.append(
                ComposedSection(
                    section_id="ALTERNATIVE",
                    title="Alternative Analysis",
                    paragraphs=[
                        f"Primary: {plan.alternative.get('primary', '')}.",
                        f"Runner-up: {plan.alternative.get('runner_up', '')} (Validation only).",
                    ],
                ),
            )
        sections.append(
            ComposedSection(
                section_id="DIAGNOSTICS",
                title="Diagnostics",
                paragraphs=[f"Rejected units: {len(plan.diagnostics.get('rejected', []))}."],
            ),
        )
        return sections

    def _compose_conclusion(self, plan: NarrativePlan) -> ComposedSection:
        class_id = str(plan.primary_conclusion.get("class_id", ""))
        label = _CLASS_LABELS.get(class_id, class_id.title())
        strength = LanguageStrength(str(plan.primary_conclusion.get("language_strength", "firm")))
        qualifier = ""
        if strength == LanguageStrength.QUALIFIED:
            qualifier = " This reading is qualified: support and control both shape the picture."
        paragraph = f"Your Day Master belongs to the {label} category.{qualifier}"
        return ComposedSection(section_id="CONCLUSION", title="Conclusion", paragraphs=[paragraph])

    def _compose_section(
        self,
        section: SectionPlan,
        units_by_id: dict[str, KnowledgeUnit],
        customer: bool,
    ) -> ComposedSection:
        title = _SECTION_TITLES.get(section.section_id, section.section_id.title())
        paragraphs: list[str] = []
        if section.insufficient_data:
            if section.insufficient_reason == "INSUFFICIENT_DATA_LUCK":
                paragraphs.append(
                    "Luck cycle interaction was not published for this chart, so timing guidance is omitted."
                )
            return ComposedSection(section_id=section.section_id, title=title, paragraphs=paragraphs)

        for selected in section.selected_units:
            unit = units_by_id.get(selected.knowledge_id)
            if unit is None:
                continue
            paragraphs.append(unit.claim.strip())
            if not customer:
                for point in unit.supporting_points:
                    paragraphs.append(point)

        return ComposedSection(section_id=section.section_id, title=title, paragraphs=paragraphs)

    def _compose_executive_summary(
        self,
        plan: NarrativePlan,
        units_by_id: dict[str, KnowledgeUnit],
    ) -> ComposedSection:
        paragraphs: list[str] = []
        for claim_role in plan.executive_summary_plan:
            paragraphs.append(claim_role)
        if not paragraphs:
            for section in plan.sections:
                for selected in section.selected_units[:1]:
                    unit = units_by_id.get(selected.knowledge_id)
                    if unit:
                        paragraphs.append(unit.claim.strip())
        return ComposedSection(section_id="SUMMARY", title="Executive Summary", paragraphs=paragraphs)

    @staticmethod
    def _evidence_paragraphs(plan: NarrativePlan) -> list[str]:
        gate_results = plan.diagnostics.get("gate_results", [])
        lines = [f"Gate evaluations: {len(gate_results)} units."]
        for item in gate_results[:10]:
            if item.get("state") != "eligible":
                lines.append(
                    f"{item.get('knowledge_id')}: {item.get('reason_code')}"
                )
        if plan.missing_data:
            lines.append(f"Missing data: {', '.join(plan.missing_data)}.")
        return lines
