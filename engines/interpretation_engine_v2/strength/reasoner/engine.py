"""Frozen PACK-01 reasoning policy orchestration."""

from __future__ import annotations

from collections import defaultdict

from engines.interpretation_engine_v2.strength.contracts.models import (
    AudienceMode,
    EvidenceState,
    GateResult,
    GateState,
    KnowledgeUnit,
    LanguageStrength,
    NarrativePlan,
    PublishedStrengthFacts,
    ReasoningInput,
    RejectedUnit,
    SectionPlan,
    SelectedUnit,
)
from engines.interpretation_engine_v2.strength.reasoner.budget import (
    BLOCKED_CLUSTER_SECTION,
    CLUSTER_REPRESENTATIVES,
    CLUSTER_REPRESENTATIVES_REC,
    CLUSTER_SECTION_OWNER,
    CUSTOMER_BUDGET,
    WHY_MANDATORY_CONTROL,
    WHY_SEASON_UNIT,
)
from engines.interpretation_engine_v2.strength.reasoner.duplicate import DuplicateResolver
from engines.interpretation_engine_v2.strength.reasoner.salience import SalienceRanker
from engines.interpretation_engine_v2.strength.selector.evidence_gate import EvidenceGate

_SECTION_MAP: dict[str, tuple[str, str]] = {
    "WHY": ("WHY", "EXPLAIN_CAUSES"),
    "MEANING": ("MEANING", "STATE_MEANING"),
    "ADVANTAGE": ("ADVANTAGE", "LIST_ADVANTAGES"),
    "CHALLENGE": ("CHALLENGE", "LIST_CHALLENGES"),
    "PERSONALITY": ("PERSONALITY", "DOMAIN_IMPLICATION"),
    "CAREER": ("CAREER", "DOMAIN_IMPLICATION"),
    "WEALTH": ("WEALTH", "DOMAIN_IMPLICATION"),
    "MARRIAGE": ("MARRIAGE", "DOMAIN_IMPLICATION"),
    "HEALTH": ("HEALTH", "DOMAIN_IMPLICATION"),
    "LUCK": ("LUCK", "LUCK_INTERACTION"),
    "RECOMMENDATION": ("RECOMMENDATION", "ADVISE"),
}

_PURPOSE_TO_SECTION: dict[str, str] = {
    "WHY": "WHY",
    "MEANING": "MEANING",
    "ADVANTAGE": "ADVANTAGE",
    "LEADERSHIP": "ADVANTAGE",
    "DECISION_MAKING": "ADVANTAGE",
    "LEARNING": "ADVANTAGE",
    "CHALLENGE": "CHALLENGE",
    "PERSONALITY": "PERSONALITY",
    "CAREER": "CAREER",
    "WEALTH": "WEALTH",
    "MARRIAGE": "MARRIAGE",
    "HEALTH": "HEALTH",
    "LUCK": "LUCK",
    "RECOMMENDATION": "RECOMMENDATION",
}

_EXEC_SUMMARY_CLAIMS = [
    "standing Strong qualified",
    "feed and control",
    "can carry load",
    "endurance as proof of method",
    "recovery is an operating condition",
    "rest + one reviser",
    "strong ≠ no brake",
]


class StrengthReasoner:
    """Apply frozen reasoning policy to gated candidates."""

    def __init__(
        self,
        evidence_gate: EvidenceGate | None = None,
        salience: SalienceRanker | None = None,
        duplicates: DuplicateResolver | None = None,
    ) -> None:
        self._gate = evidence_gate or EvidenceGate()
        self._salience = salience or SalienceRanker()
        self._duplicates = duplicates or DuplicateResolver()

    def build_plan(self, reasoning_input: ReasoningInput) -> NarrativePlan:
        """Build NarrativePlan from ReasoningInput."""
        published = reasoning_input.published
        audience = reasoning_input.audience
        units_by_id = {unit.knowledge_id: unit for unit in reasoning_input.candidates}

        gate_results = self._gate.evaluate_all(reasoning_input.candidates, published)
        eligible = [
            unit
            for unit in reasoning_input.candidates
            if gate_results[unit.knowledge_id].state == GateState.ELIGIBLE
        ]

        grouped: dict[str, list[KnowledgeUnit]] = defaultdict(list)
        for unit in eligible:
            section_key = _PURPOSE_TO_SECTION.get(unit.purpose.upper(), unit.purpose.upper())
            grouped[section_key].append(unit)

        language_strength = self._language_strength(published)
        sections: list[SectionPlan] = []
        all_rejected: list[RejectedUnit] = []
        selected_clusters: set[str] = set()

        for section_id, (purpose, intent) in _SECTION_MAP.items():
            pool = self._salience.rank(grouped.get(section_id, []), published)
            pool, owner_rejected = self._filter_cluster_section_ownership(pool, section_id)
            pool, cluster_rejected = self._filter_cross_section_duplicates(pool, selected_clusters)
            kept, dup_rejected = self._duplicates.resolve(pool, section_id)
            for cluster in self._clusters_for_units(kept):
                selected_clusters.add(cluster)
            min_cap, max_cap = CUSTOMER_BUDGET.get(section_id, (0, 99))
            if audience == AudienceMode.CUSTOMER:
                selected = kept[:max_cap] if max_cap else []
            else:
                selected = kept

            if section_id == "WHY":
                selected, why_rejected = self._enforce_why_policy(selected, kept, units_by_id, published)
                all_rejected.extend(why_rejected)
            else:
                why_rejected = []

            if len(selected) < min_cap and section_id not in {"LUCK"}:
                pass

            rejected_ids = {item[0] for item in dup_rejected}
            rejected_ids.update(item.knowledge_id for item in why_rejected)
            rejected_ids.update(item[0] for item in owner_rejected)
            section_rejected = [
                RejectedUnit(
                    knowledge_id=unit.knowledge_id,
                    reason_code=gate_results[unit.knowledge_id].reason_code
                    if unit.knowledge_id in gate_results
                    else "REJECTED_LOW_SALIENCE",
                )
                for unit in pool
                if unit.knowledge_id not in {sel.knowledge_id for sel in selected}
                and unit.knowledge_id not in rejected_ids
            ]
            section_rejected.extend(
                RejectedUnit(knowledge_id=item[0], reason_code=item[1]) for item in dup_rejected
            )
            section_rejected.extend(
                RejectedUnit(knowledge_id=item[0], reason_code=item[1]) for item in owner_rejected
            )
            section_rejected.extend(
                RejectedUnit(knowledge_id=item[0], reason_code=item[1]) for item in cluster_rejected
            )
            section_rejected.extend(why_rejected)

            luck_state = published.facts.get("luck_interaction")
            if section_id == "LUCK" and luck_state in {None, EvidenceState.MISSING}:
                sections.append(
                    SectionPlan(
                        section_id=section_id,
                        purpose=purpose,
                        intent="LUCK_INSUFFICIENT",
                        selected_units=[],
                        rejected_units=section_rejected,
                        language_strength=language_strength,
                        insufficient_data=True,
                        insufficient_reason="INSUFFICIENT_DATA_LUCK",
                    )
                )
                all_rejected.extend(section_rejected)
                continue

            selected_units = [
                SelectedUnit(
                    knowledge_id=unit.knowledge_id,
                    reason_code=self._select_reason(unit, section_id),
                    merged_with=self._merged_with(unit, published),
                )
                for unit in selected
            ]

            sections.append(
                SectionPlan(
                    section_id=section_id,
                    purpose=purpose,
                    intent=intent,
                    selected_units=selected_units,
                    rejected_units=section_rejected,
                    language_strength=language_strength,
                )
            )
            all_rejected.extend(section_rejected)

        ineligible = [
            RejectedUnit(
                knowledge_id=unit.knowledge_id,
                reason_code=gate_results[unit.knowledge_id].reason_code,
            )
            for unit in reasoning_input.candidates
            if gate_results[unit.knowledge_id].state == GateState.INELIGIBLE
        ]

        plan = NarrativePlan(
            meta={
                "subject": "strength",
                "case_id": published.case_id,
                "knowledge_version": reasoning_input.knowledge_version,
                "reasoning_policy_version": reasoning_input.reasoning_policy_version,
            },
            primary_conclusion={
                "class_id": published.class_id,
                "language_strength": language_strength.value,
                "reason_code": "SELECTED_CORE_CONCLUSION",
                "qualifier": "QUALIFIED_FOR_CUSTOMER"
                if language_strength == LanguageStrength.QUALIFIED
                else "",
            },
            sections=sections,
            warnings=self._warnings(published),
            omitted_domains=self._omitted_domains(sections),
            missing_data=self._missing_data_labels(published),
            alternative={
                "primary": published.alternative_primary,
                "runner_up": published.alternative_runner_up,
                "shares": published.alternative_shares,
                "visibility": "DEFERRED_TO_VALIDATION",
            },
            executive_summary_plan=list(_EXEC_SUMMARY_CLAIMS),
            diagnostics={
                "gate_results": [self._gate_dict(item) for item in gate_results.values()],
                "rejected": [
                    {"knowledge_id": item.knowledge_id, "reason_code": item.reason_code}
                    for item in ineligible + all_rejected
                ],
                "conflicts": published.conflicts,
            },
        )
        return plan

    def _enforce_why_policy(
        self,
        selected: list[KnowledgeUnit],
        ranked: list[KnowledgeUnit],
        units_by_id: dict[str, KnowledgeUnit],
        published: PublishedStrengthFacts,
    ) -> tuple[list[KnowledgeUnit], list[RejectedUnit]]:
        """Ensure control is kept and season absorbs special merge."""
        rejected: list[RejectedUnit] = []
        selected_ids = {unit.knowledge_id for unit in selected}

        control = units_by_id.get(WHY_MANDATORY_CONTROL)
        if control and control.knowledge_id not in selected_ids:
            if len(selected) >= CUSTOMER_BUDGET["WHY"][1]:
                dropped = selected.pop()
                rejected.append(RejectedUnit(dropped.knowledge_id, "REJECTED_NARRATIVE_BUDGET"))
            selected.append(control)
            selected_ids.add(control.knowledge_id)

        season = units_by_id.get(WHY_SEASON_UNIT)
        if season and season.knowledge_id not in selected_ids and season in ranked:
            if len(selected) >= CUSTOMER_BUDGET["WHY"][1]:
                dropped = selected.pop()
                rejected.append(RejectedUnit(dropped.knowledge_id, "REJECTED_NARRATIVE_BUDGET"))
            selected.insert(0, season)
            selected_ids.add(season.knowledge_id)

        _, max_cap = CUSTOMER_BUDGET["WHY"]
        if len(selected) > max_cap:
            trimmed = sorted(selected, key=lambda unit: unit.knowledge_id)
            while len(trimmed) > max_cap:
                drop_candidate = next(
                    (unit for unit in reversed(trimmed) if unit.knowledge_id != WHY_MANDATORY_CONTROL),
                    trimmed[-1],
                )
                trimmed.remove(drop_candidate)
                rejected.append(RejectedUnit(drop_candidate.knowledge_id, "REJECTED_NARRATIVE_BUDGET"))
            selected = trimmed

        return selected, rejected

    @staticmethod
    def _clusters_for_units(units: list[KnowledgeUnit]) -> set[str]:
        clusters: set[str] = set()
        for unit in units:
            cluster = unit.duplicate_cluster.upper()
            if cluster not in {"", "NONE"}:
                clusters.add(cluster)
        return clusters

    def _filter_cluster_section_ownership(
        self,
        units: list[KnowledgeUnit],
        section_id: str,
    ) -> tuple[list[KnowledgeUnit], list[tuple[str, str]]]:
        """Reject duplicate-cluster members outside their owning section."""
        kept: list[KnowledgeUnit] = []
        rejected: list[tuple[str, str]] = []
        for unit in units:
            cluster = unit.duplicate_cluster.upper()
            if (cluster, section_id) in BLOCKED_CLUSTER_SECTION:
                rejected.append((unit.knowledge_id, "REJECTED_DUPLICATE"))
                continue
            owner = CLUSTER_SECTION_OWNER.get(cluster)
            if owner and owner != section_id:
                rejected.append((unit.knowledge_id, "REJECTED_DUPLICATE"))
                continue
            kept.append(unit)
        return kept, rejected

    def _filter_cross_section_duplicates(
        self,
        units: list[KnowledgeUnit],
        selected_clusters: set[str],
    ) -> tuple[list[KnowledgeUnit], list[tuple[str, str]]]:
        """Drop cluster members already represented in prior sections."""
        kept: list[KnowledgeUnit] = []
        rejected: list[tuple[str, str]] = []
        for unit in units:
            if unit.purpose == "RECOMMENDATION":
                kept.append(unit)
                continue
            cluster = unit.duplicate_cluster.upper()
            if cluster in {"", "NONE"} or cluster not in selected_clusters:
                kept.append(unit)
                continue
            representative = CLUSTER_REPRESENTATIVES.get(cluster)
            if representative and unit.knowledge_id == representative:
                kept.append(unit)
                continue
            rejected.append((unit.knowledge_id, "REJECTED_DUPLICATE"))
        return kept, rejected

    @staticmethod
    def _language_strength(published: PublishedStrengthFacts) -> LanguageStrength:
        if "C1" in published.conflicts or published.forbidden_flags.get("root_thin", False):
            return LanguageStrength.QUALIFIED
        if published.confidence_band in {"low", "experimental"}:
            return LanguageStrength.CAUTIOUS
        return LanguageStrength.FIRM

    @staticmethod
    def _select_reason(unit: KnowledgeUnit, section_id: str) -> str:
        if section_id == "WHY":
            return "SELECTED_CAUSE_PRESENT"
        if section_id == "RECOMMENDATION":
            return "SELECTED_CHAIN_ACTION"
        if section_id in {"ADVANTAGE", "CHALLENGE"}:
            return "SELECTED_HIGH_SALIENCE"
        return "SELECTED_REQUIRED_SECTION"

    @staticmethod
    def _merged_with(unit: KnowledgeUnit, published: PublishedStrengthFacts) -> list[str]:
        if unit.knowledge_id != WHY_SEASON_UNIT:
            return []
        if published.facts.get("special") is not None:
            return ["MERGED_CAUSE_SPECIAL_INTO_SEASON"]
        return []

    @staticmethod
    def _warnings(published: PublishedStrengthFacts) -> list[str]:
        warnings: list[str] = []
        if "C1" in published.conflicts:
            warnings.append("CONFLICT_QUALIFY")
        if published.forbidden_flags.get("root_thin", False):
            warnings.append("QUALIFIED_FOR_CUSTOMER")
        return warnings

    @staticmethod
    def _omitted_domains(sections: list[SectionPlan]) -> list[str]:
        omitted: list[str] = []
        for section in sections:
            if section.insufficient_data and section.section_id == "LUCK":
                omitted.append("luck content")
            if section.section_id in {"WEALTH", "PERSONALITY"} and not section.selected_units:
                omitted.append(section.section_id.lower())
        return omitted

    @staticmethod
    def _missing_data_labels(published: PublishedStrengthFacts) -> list[str]:
        labels: list[str] = []
        if published.facts.get("luck_interaction") is None:
            labels.append("luck_interaction")
        if published.facts.get("hidden_stems") is None:
            labels.append("hidden_stems")
        return labels

    @staticmethod
    def _gate_dict(result: GateResult) -> dict[str, object]:
        return {
            "knowledge_id": result.knowledge_id,
            "state": result.state.value,
            "reason_code": result.reason_code,
            "missing_required": list(result.missing_required),
            "forbidden_hit": list(result.forbidden_hit),
        }
