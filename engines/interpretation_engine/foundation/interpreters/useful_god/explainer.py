"""Useful God decision explainer — builds DecisionExplanationResult from facts."""

from __future__ import annotations

from engines.interpretation_engine.foundation import diagnostics as diag
from engines.interpretation_engine.foundation.explanation.metrics import compute_explainability_metrics
from engines.interpretation_engine.foundation.explanation.models import (
    AdviceItem,
    AnalysisFact,
    Decision,
    DecisionAlternative,
    DecisionExplanationResult,
    DecisionPathStep,
    DomainApplication,
    DomainMeaningItem,
    EvidenceItem,
    WarningItem,
)
from engines.interpretation_engine.foundation.explanation.validation import validate_decision_explanation
from engines.interpretation_engine.foundation.facts.useful_god import (
    UsefulGodCandidateFact,
    UsefulGodInterpretationFacts,
    lookup_useful_god_entity_type,
)
from engines.interpretation_engine.foundation.interpreters.useful_god.templates import (
    ELEMENT_LABELS,
    GROUP_LABEL_VI,
    GROUP_PRIORITY,
    IMPACT_DOMAINS,
    KNOWLEDGE_ENTITY_TYPE_STEM,
    STEM_ELEMENT,
    STRENGTH_VI,
    TEMPERATURE_VI,
    customer_display_label,
)
from engines.interpretation_engine.foundation.status import DataAvailability


class UsefulGodExplainer:
    """Build framework-backed Useful God decision explanation from facts only."""

    def explain(self, facts: UsefulGodInterpretationFacts) -> DecisionExplanationResult:
        """Transform UsefulGodInterpretationFacts into DecisionExplanationResult."""
        diagnostics = list(facts.diagnostics)

        if not facts.selected or facts.presence != DataAvailability.AVAILABLE:
            diagnostics.append(diag.USEFUL_GOD_NOT_AVAILABLE)
            return self._partial_explanation(facts, diagnostics)

        if not facts.candidates:
            diagnostics.append(diag.USEFUL_GOD_CANDIDATES_MISSING)
            return self._partial_explanation(facts, diagnostics)

        winner = _resolve_winner(facts)
        if winner is None:
            diagnostics.append(diag.USEFUL_GOD_EVIDENCE_MISSING)
            return self._partial_explanation(facts, diagnostics)

        analysis = _build_analysis(facts)
        evidence = _build_evidence_items(facts, winner)
        evidence_ids = {item.evidence_id for item in evidence}
        decision_path = _build_decision_path(facts, winner, evidence_ids)
        alternatives = _build_alternatives(facts, winner, evidence_ids)
        decision = _build_decision(facts, winner, alternatives, evidence_ids)
        domain_meaning = _build_domain_meaning(facts, evidence_ids)
        applications = _build_applications(facts, evidence_ids)
        advice = _build_advice(facts, evidence_ids)
        warnings = _build_warnings(facts, evidence_ids)

        status = DataAvailability.AVAILABLE
        if diagnostics:
            status = DataAvailability.PARTIAL

        result = DecisionExplanationResult(
            domain="useful_god",
            status=status,
            analysis=tuple(analysis),
            decision_path=tuple(decision_path),
            evidence=tuple(evidence),
            decision=decision,
            alternatives=tuple(alternatives),
            domain_meaning=tuple(domain_meaning),
            applications=tuple(applications),
            advice=tuple(advice),
            warnings=tuple(warnings),
            confidence=facts.confidence,
            diagnostics=tuple(dict.fromkeys(diagnostics)),
        )

        metrics = compute_explainability_metrics(result)
        validation = validate_decision_explanation(
            result,
            analytical_selected=facts.selected,
        )
        merged_diagnostics = list(result.diagnostics)
        for issue in validation.issues:
            if issue.severity == "error":
                merged_diagnostics.append(issue.code)
        final_status = validation.status if not validation.passed else result.status

        return DecisionExplanationResult(
            domain=result.domain,
            status=final_status,
            analysis=result.analysis,
            decision_path=result.decision_path,
            evidence=result.evidence,
            decision=result.decision,
            alternatives=result.alternatives,
            domain_meaning=result.domain_meaning,
            applications=result.applications,
            advice=result.advice,
            warnings=result.warnings,
            confidence=result.confidence,
            diagnostics=tuple(dict.fromkeys(merged_diagnostics)),
            metrics=metrics,
        )

    def _partial_explanation(
        self,
        facts: UsefulGodInterpretationFacts,
        diagnostics: list[str],
    ) -> DecisionExplanationResult:
        """Return partial framework explanation when facts are insufficient."""
        analysis = _build_analysis(facts) if facts.day_master else []
        evidence = _build_evidence_items(facts, None)
        result = DecisionExplanationResult(
            domain="useful_god",
            status=DataAvailability.PARTIAL,
            analysis=tuple(analysis),
            decision_path=(),
            evidence=tuple(evidence),
            decision=None,
            alternatives=(),
            domain_meaning=(),
            applications=(),
            advice=(),
            warnings=(
                WarningItem(
                    condition="insufficient_facts",
                    risk="Thiếu cơ sở Dụng thần đầy đủ",
                    severity="medium",
                    evidence_ids=(),
                    mitigation="Không diễn giải thêm để tránh suy đoán",
                ),
            ),
            confidence=facts.confidence,
            diagnostics=tuple(dict.fromkeys(diagnostics)),
            metrics=compute_explainability_metrics(
                DecisionExplanationResult(
                    domain="useful_god",
                    status=DataAvailability.PARTIAL,
                    analysis=tuple(analysis),
                    decision_path=(),
                    evidence=tuple(evidence),
                    decision=None,
                    alternatives=(),
                    domain_meaning=(),
                    applications=(),
                    advice=(),
                    warnings=(),
                    confidence=facts.confidence,
                    diagnostics=tuple(dict.fromkeys(diagnostics)),
                )
            ),
        )
        return result


def _resolve_winner(facts: UsefulGodInterpretationFacts) -> UsefulGodCandidateFact | None:
    """Identify winning candidate using published scores and group priority."""
    if not facts.candidates:
        return None

    def sort_key(item: UsefulGodCandidateFact) -> tuple[int, float, str]:
        group = item.rule_group or item.candidate_type or ""
        priority = GROUP_PRIORITY.get(group, 0)
        return (priority, item.confidence, item.rule_id)

    ranked = sorted(facts.candidates, key=sort_key, reverse=True)
    for candidate in ranked:
        if candidate.useful_god == facts.selected:
            return candidate
    return ranked[0]


def _build_analysis(facts: UsefulGodInterpretationFacts) -> list[AnalysisFact]:
    """Build analysis stage from published facts."""
    items: list[AnalysisFact] = [
        AnalysisFact(
            fact="day_master",
            value=f"{facts.day_master} ({facts.day_master_element})",
            source=facts.owner,
            role="primary",
        ),
        AnalysisFact(
            fact="month_branch",
            value=facts.month_branch,
            source=facts.owner,
            role="context",
        ),
        AnalysisFact(
            fact="season",
            value=facts.season or "unknown",
            source=facts.owner,
            role="primary",
        ),
        AnalysisFact(
            fact="strength",
            value=f"{facts.strength_level} / {facts.strength_score:.2f}",
            source="StrengthEngine",
            role="supporting",
        ),
        AnalysisFact(
            fact="temperature",
            value=facts.temperature_level,
            source="TemperatureEngine",
            role="supporting",
        ),
        AnalysisFact(
            fact="useful_god_selected",
            value=facts.selected,
            source=facts.owner,
            role="primary",
        ),
        AnalysisFact(
            fact="favorable_gods",
            value=", ".join(facts.favorable_gods) if facts.favorable_gods else "none",
            source=facts.owner,
            role="supporting",
        ),
        AnalysisFact(
            fact="unfavorable_gods",
            value=", ".join(facts.unfavorable_gods) if facts.unfavorable_gods else "none",
            source=facts.owner,
            role="restricting",
        ),
    ]
    fe = facts.five_elements
    counts = ", ".join(
        f"{ELEMENT_LABELS[k]} {fe.get(k)}"
        for k in ("wood", "fire", "earth", "metal", "water")
        if fe.get(k) is not None
    )
    if counts:
        items.append(
            AnalysisFact(
                fact="five_elements",
                value=counts,
                source="RuleContext.wuxing",
                role="environment",
            )
        )
    return items


def _evidence_id(prefix: str, key: str) -> str:
    """Build stable evidence identifier."""
    return f"{prefix}_{key}"


def _entity_type_of(facts: UsefulGodInterpretationFacts, value: str) -> str:
    """Prefer stored facts type, else canonical knowledge type. Do not guess."""
    stored = facts.entity_type_of(value)
    if stored:
        return stored
    return lookup_useful_god_entity_type(value)


def _customer_label(facts: UsefulGodInterpretationFacts, value: str) -> str:
    """Customer-facing Useful God / Hỷ / Kỵ label from canonical type."""
    return customer_display_label(value, _entity_type_of(facts, value))


def _build_evidence_items(
    facts: UsefulGodInterpretationFacts,
    winner: UsefulGodCandidateFact | None,
) -> list[EvidenceItem]:
    """Build evidence registry from facts."""
    items: list[EvidenceItem] = []

    items.append(
        EvidenceItem(
            evidence_id=_evidence_id("fact", "day_master"),
            source_engine=facts.owner,
            source_field="day_master",
            rule_id="",
            fact="day_master",
            value=f"{facts.day_master} ({facts.day_master_element})",
            confidence=1.0,
            relevance="primary",
        )
    )
    items.append(
        EvidenceItem(
            evidence_id=_evidence_id("fact", "season"),
            source_engine=facts.owner,
            source_field="season",
            rule_id="",
            fact="season",
            value=f"{facts.season} / {facts.month_branch}",
            confidence=1.0,
            relevance="primary",
        )
    )
    items.append(
        EvidenceItem(
            evidence_id=_evidence_id("fact", "strength"),
            source_engine="StrengthEngine",
            source_field="strength_level",
            rule_id="",
            fact="strength",
            value=f"{facts.strength_level} / {facts.strength_score:.2f}",
            confidence=1.0,
            relevance="supporting",
        )
    )
    items.append(
        EvidenceItem(
            evidence_id=_evidence_id("fact", "temperature"),
            source_engine="TemperatureEngine",
            source_field="temperature_level",
            rule_id="",
            fact="temperature",
            value=facts.temperature_level,
            confidence=1.0,
            relevance="supporting",
        )
    )

    for candidate in facts.candidates:
        group = candidate.rule_group or candidate.candidate_type or "unknown"
        eid = _evidence_id("candidate", candidate.rule_id)
        items.append(
            EvidenceItem(
                evidence_id=eid,
                source_engine=facts.owner,
                source_field=f"candidate.{group}",
                rule_id=candidate.rule_id,
                fact=candidate.useful_god,
                value=candidate.reason or f"score={candidate.confidence:.2f}",
                confidence=candidate.confidence,
                relevance=group,
            )
        )

    if winner is not None:
        items.append(
            EvidenceItem(
                evidence_id=_evidence_id("decision", "reason"),
                source_engine=facts.owner,
                source_field="reasoning",
                rule_id=winner.rule_id,
                fact="selection_reason",
                value=facts.reason,
                confidence=facts.confidence,
                relevance="decision",
            )
        )

    for stem in facts.favorable_gods:
        items.append(
            EvidenceItem(
                evidence_id=_evidence_id("hy", stem),
                source_engine=facts.owner,
                source_field="favorable_gods",
                rule_id="",
                fact="favorable_god",
                value=stem,
                confidence=facts.confidence,
                relevance="supporting",
            )
        )
    for stem in facts.unfavorable_gods:
        items.append(
            EvidenceItem(
                evidence_id=_evidence_id("ky", stem),
                source_engine=facts.owner,
                source_field="unfavorable_gods",
                rule_id="",
                fact="unfavorable_god",
                value=stem,
                confidence=facts.confidence,
                relevance="restricting",
            )
        )

    return items


def _build_decision_path(
    facts: UsefulGodInterpretationFacts,
    winner: UsefulGodCandidateFact,
    evidence_ids: set[str],
) -> list[DecisionPathStep]:
    """Build ordered decision path with branching support."""
    win_group = winner.rule_group or winner.candidate_type or "unknown"
    win_priority = GROUP_PRIORITY.get(win_group, 0)
    strength_note = STRENGTH_VI.get(facts.strength_level, facts.strength_level)
    temp_note = TEMPERATURE_VI.get(facts.temperature_level, facts.temperature_level)

    steps: list[DecisionPathStep] = [
        DecisionPathStep(
            step_id="read_day_master_season",
            order=1,
            title="Read Day Master and season",
            input_facts=(
                _evidence_id("fact", "day_master"),
                _evidence_id("fact", "season"),
            ),
            rule_refs=(),
            condition=f"day_master={facts.day_master} AND season={facts.season}",
            outcome=f"Nhật chủ {facts.day_master} ({facts.day_master_element}); mùa {facts.season} (chi {facts.month_branch})",
            effect="Establish primary seasonal context for candidate groups",
            status="passed",
        ),
        DecisionPathStep(
            step_id="read_strength",
            order=2,
            title="Read Strength result",
            input_facts=(_evidence_id("fact", "strength"),),
            rule_refs=(),
            condition=f"strength={facts.strength_level}",
            outcome=f"Thân {strength_note} ({facts.strength_score:.2f})",
            effect="Enable strength-group candidates",
            status="passed" if facts.strength_level else "skipped",
        ),
        DecisionPathStep(
            step_id="read_temperature",
            order=3,
            title="Read Temperature result",
            input_facts=(_evidence_id("fact", "temperature"),),
            rule_refs=(),
            condition=f"temperature={facts.temperature_level}",
            outcome=f"Điều hậu khí {temp_note}",
            effect="Enable temperature-group warming/cooling candidates",
            status="passed" if facts.temperature_level else "skipped",
        ),
        DecisionPathStep(
            step_id="read_five_elements",
            order=4,
            title="Read Five Elements context",
            input_facts=tuple(
                eid for eid in evidence_ids if eid.startswith("fact_")
            )[:1],
            rule_refs=(),
            condition="five_elements available",
            outcome=(
                "Phân bố ngũ hành: "
                + ", ".join(
                    f"{ELEMENT_LABELS[k]} {facts.five_elements.get(k)}"
                    for k in ("wood", "fire", "earth", "metal", "water")
                    if facts.five_elements.get(k) is not None
                )
            ),
            effect="Enable flow-group balance candidates",
            status="passed" if any(facts.five_elements.values()) else "skipped",
        ),
        DecisionPathStep(
            step_id="load_candidates",
            order=5,
            title="Load Useful God candidates",
            input_facts=tuple(
                _evidence_id("candidate", c.rule_id) for c in facts.candidates
            ),
            rule_refs=tuple(c.rule_id for c in facts.candidates),
            condition=f"candidate_count={len(facts.candidates)}",
            outcome=f"Loaded {len(facts.candidates)} candidates from engine",
            effect="Prepare comparison set",
            status="passed",
        ),
        DecisionPathStep(
            step_id="compare_groups",
            order=6,
            title="Compare candidate groups",
            input_facts=(_evidence_id("candidate", winner.rule_id),),
            rule_refs=(winner.rule_id,),
            condition="group priority: season > strength > temperature > flow",
            outcome=(
                f"Group {GROUP_LABEL_VI.get(win_group, win_group)} "
                f"(priority {win_priority}) leads ranking"
            ),
            effect="Higher-priority group wins before lower group when scores compete",
            status="passed",
        ),
        DecisionPathStep(
            step_id="compare_scores",
            order=7,
            title="Compare candidate scores within groups",
            input_facts=tuple(
                _evidence_id("candidate", c.rule_id) for c in facts.candidates
            ),
            rule_refs=tuple(c.rule_id for c in facts.candidates),
            condition="score and rule_priority within same group",
            outcome=(
                f"Winner {winner.useful_god} score {winner.confidence:.2f} "
                f"via {winner.rule_id}"
            ),
            effect="Resolve tie-break within priority tier",
            status="passed",
        ),
        DecisionPathStep(
            step_id="select_winner",
            order=8,
            title="Select Useful God",
            input_facts=(
                _evidence_id("candidate", winner.rule_id),
                _evidence_id("decision", "reason"),
            ),
            rule_refs=(winner.rule_id,),
            condition=f"selected={facts.selected}",
            outcome=f"Dụng thần = {facts.selected}; reason: {facts.reason}",
            effect="Freeze analytical decision from engine truth",
            status="terminal",
        ),
        DecisionPathStep(
            step_id="preserve_hy_ky",
            order=9,
            title="Preserve Hỷ / Kỵ",
            input_facts=tuple(
                _evidence_id("hy", s) for s in facts.favorable_gods
            )
            + tuple(_evidence_id("ky", s) for s in facts.unfavorable_gods),
            rule_refs=(),
            condition="engine published favorable/unfavorable lists",
            outcome=(
                f"Hỷ = {', '.join(facts.favorable_gods)}; "
                f"Kỵ = {', '.join(facts.unfavorable_gods)}"
            ),
            effect="Attach supporting/restricting element sets",
            status="passed",
        ),
        DecisionPathStep(
            step_id="explain_rejected",
            order=10,
            title="Explain rejected alternatives",
            input_facts=tuple(
                _evidence_id("candidate", c.rule_id)
                for c in facts.candidates
                if c.rule_id != winner.rule_id
            ),
            rule_refs=tuple(
                c.rule_id for c in facts.candidates if c.rule_id != winner.rule_id
            ),
            condition="alternatives.status=rejected",
            outcome=_rejection_summary(facts, winner),
            effect="Document why competing candidates lost",
            status="passed",
        ),
    ]
    return steps


def _rejection_summary(
    facts: UsefulGodInterpretationFacts,
    winner: UsefulGodCandidateFact,
) -> str:
    """Summarize rejections for decision path terminal step."""
    parts: list[str] = []
    for candidate in facts.candidates:
        if candidate.rule_id == winner.rule_id:
            continue
        reason = _rejection_reason(candidate, winner, facts.selected)
        if reason:
            parts.append(reason)
    return " | ".join(parts[:4]) if parts else "No rejected alternatives"


def _rejection_reason(
    candidate: UsefulGodCandidateFact,
    winner: UsefulGodCandidateFact,
    selected: str,
) -> str:
    """Explain why one candidate lost."""
    group = candidate.rule_group or candidate.candidate_type or "unknown"
    win_group = winner.rule_group or winner.candidate_type or "unknown"
    group_priority = GROUP_PRIORITY.get(group, 0)
    win_priority = GROUP_PRIORITY.get(win_group, 0)
    group_label = GROUP_LABEL_VI.get(group, group)

    if candidate.useful_god == selected and candidate.rule_id != winner.rule_id:
        return (
            f"{candidate.useful_god} ({group_label}, {candidate.confidence:.2f}): "
            f"same stem, lower group priority ({group_priority} < {win_priority})"
        )
    if group_priority < win_priority:
        return (
            f"{candidate.useful_god} ({group_label}, {candidate.confidence:.2f}): "
            f"group priority {group_priority} < {win_priority}"
        )
    if candidate.confidence < winner.confidence:
        return (
            f"{candidate.useful_god} ({group_label}, {candidate.confidence:.2f}): "
            f"lower score than {winner.useful_god} ({winner.confidence:.2f})"
        )
    return (
        f"{candidate.useful_god} ({group_label}): "
        f"not selected after group and score ranking"
    )


def _build_alternatives(
    facts: UsefulGodInterpretationFacts,
    winner: UsefulGodCandidateFact,
    evidence_ids: set[str],
) -> list[DecisionAlternative]:
    """Build accepted/rejected alternatives."""
    alts: list[DecisionAlternative] = []
    for candidate in facts.candidates:
        group = candidate.rule_group or candidate.candidate_type or "unknown"
        eid = _evidence_id("candidate", candidate.rule_id)
        is_winner = candidate.rule_id == winner.rule_id
        rejection = "" if is_winner else _rejection_reason(candidate, winner, facts.selected)
        alts.append(
            DecisionAlternative(
                alternative_id=eid,
                candidate=candidate.useful_god,
                candidate_type=group,
                score=candidate.confidence,
                priority=GROUP_PRIORITY.get(group, 0),
                supporting_evidence=(eid,) if eid in evidence_ids else (),
                opposing_evidence=(
                    (_evidence_id("candidate", winner.rule_id),)
                    if not is_winner
                    else ()
                ),
                rejection_reason=rejection,
                status="selected" if is_winner else "rejected",
            )
        )
    return alts


def _build_decision(
    facts: UsefulGodInterpretationFacts,
    winner: UsefulGodCandidateFact,
    alternatives: list[DecisionAlternative],
    evidence_ids: set[str],
) -> Decision:
    """Build decision object from analytical truth."""
    win_eid = _evidence_id("candidate", winner.rule_id)
    supporting = [
        eid
        for eid in (
            win_eid,
            _evidence_id("decision", "reason"),
            _evidence_id("fact", "season"),
            _evidence_id("fact", "strength"),
            _evidence_id("fact", "temperature"),
        )
        if eid in evidence_ids
    ]
    rejected = tuple(
        alt.alternative_id for alt in alternatives if alt.status == "rejected"
    )
    return Decision(
        selected=facts.selected,
        selected_type=winner.rule_group or winner.candidate_type or "unknown",
        reason=facts.reason,
        confidence=facts.confidence,
        supporting_evidence_ids=tuple(supporting),
        rejected_alternatives=rejected,
        selected_entity_type=_entity_type_of(facts, facts.selected),
    )


def _build_domain_meaning(
    facts: UsefulGodInterpretationFacts,
    evidence_ids: set[str],
) -> list[DomainMeaningItem]:
    """Expert domain meaning — not customer advice."""
    selected_label = _customer_label(facts, facts.selected)
    hy = ", ".join(_customer_label(facts, item) for item in facts.favorable_gods)
    ky = ", ".join(_customer_label(facts, item) for item in facts.unfavorable_gods)
    refs = [
        eid
        for eid in (
            _evidence_id("candidate", facts.rule_ids[0]) if facts.rule_ids else "",
            _evidence_id("decision", "reason"),
        )
        if eid in evidence_ids
    ]
    return [
        DomainMeaningItem(
            statement=(
                f"Dụng thần chính: {selected_label} — "
                f"trụ cột điều tiết hệ."
            ),
            evidence_ids=tuple(refs),
        ),
        DomainMeaningItem(
            statement=(
                f"Hỷ thần ({hy}) hỗ trợ duy trì cân bằng; "
                f"Kỵ thần ({ky}) cần hạn chế khuếch đại."
            ),
            evidence_ids=tuple(
                eid
                for eid in list(evidence_ids)
                if eid.startswith("hy_") or eid.startswith("ky_")
            ),
        ),
    ]


def _build_applications(
    facts: UsefulGodInterpretationFacts,
    evidence_ids: set[str],
) -> list[DomainApplication]:
    """Map decision to life domains."""
    selected = facts.selected
    selected_label = _customer_label(facts, selected)
    selected_el = (
        STEM_ELEMENT.get(selected, "")
        if _entity_type_of(facts, selected) == KNOWLEDGE_ENTITY_TYPE_STEM
        else ""
    )
    hy = facts.favorable_gods
    ky = facts.unfavorable_gods
    strong = facts.strength_level == "strong"
    cool = facts.temperature_level in {"cool", "cold"}
    base_refs = tuple(
        eid
        for eid in (
            _evidence_id("decision", "reason"),
            _evidence_id("fact", "strength"),
        )
        if eid in evidence_ids
    )

    apps: list[DomainApplication] = []
    career = (
        f"Sự nghiệp ổn định hơn khi vận hành theo {selected_label}"
        + (" — thân vượng cần tiết xuất và trách nhiệm có cấu trúc." if strong else ".")
    )
    if ky:
        career += f" Hạn chế áp lực từ {', '.join(ky[:2])} khi nhận thêm cam kết."
    apps.append(
        DomainApplication(
            domain="career",
            statement=career,
            basis_evidence_ids=base_refs,
            confidence=facts.confidence,
        )
    )

    apps.append(
        DomainApplication(
            domain="wealth",
            statement=(
                f"Tài lộc liên quan khả năng điều tiết qua {selected_el or selected}; "
                f"ưu tiên dòng tiền gắn Hỷ thần ({', '.join(hy[:3])})."
            ),
            basis_evidence_ids=base_refs,
            confidence=facts.confidence,
        )
    )

    rel = (
        f"Quan hệ cân bằng hơn khi duy trì không khí thuận ({', '.join(hy[:2])}); "
        f"tránh kích hoạt Kỵ thần ({', '.join(ky[:2])}) trong tranh chấp."
        if ky
        else f"Quan hệ hưởng lợi từ không khí thuận ({', '.join(hy[:2])})."
    )
    apps.append(
        DomainApplication(
            domain="relationships",
            statement=rel,
            basis_evidence_ids=base_refs,
            confidence=facts.confidence,
        )
    )

    health = (
        f"Sức khỏe cần giữ ấm / cân khí"
        + (" vì điều hậu mát" if cool else "")
        + f"; {selected_label} là hướng điều tiết chính."
    )
    apps.append(
        DomainApplication(
            domain="health",
            statement=health,
            basis_evidence_ids=base_refs,
            confidence=facts.confidence,
        )
    )

    learn = (
        f"Học hỏi / phát triển: nuôi dưỡng {', '.join(hy[:2])} "
        f"thay vì thiên về {', '.join(ky[:2])}."
        if ky
        else f"Học hỏi / phát triển: theo hướng {', '.join(hy[:2])}."
    )
    apps.append(
        DomainApplication(
            domain="learning_growth",
            statement=learn,
            basis_evidence_ids=base_refs,
            confidence=facts.confidence,
        )
    )

    return apps


def _build_advice(
    facts: UsefulGodInterpretationFacts,
    evidence_ids: set[str],
) -> list[AdviceItem]:
    """Structured advice separate from analysis."""
    selected = facts.selected
    hy = facts.favorable_gods
    ky = facts.unfavorable_gods
    cool = facts.temperature_level in {"cool", "cold"}
    refs = tuple(
        eid for eid in (_evidence_id("decision", "reason"),) if eid in evidence_ids
    )

    items: list[AdviceItem] = [
        AdviceItem(
            category="priority_action",
            action=f"Đặt {selected} làm trọng tâm khi cần điều tiết hệ.",
            priority="high",
            rationale="Engine-selected Useful God",
            evidence_ids=refs,
        ),
        AdviceItem(
            category="support",
            action=f"Ưu tiên hành động gắn Hỷ thần: {', '.join(hy)}.",
            priority="high",
            rationale="Published favorable gods",
            evidence_ids=tuple(_evidence_id("hy", s) for s in hy if _evidence_id("hy", s) in evidence_ids),
        ),
        AdviceItem(
            category="environment",
            action=f"Môi trường thuận: không khí có yếu tố {', '.join(hy[:3])}.",
            priority="medium",
            rationale="Supportive element environment",
            evidence_ids=refs,
        ),
    ]
    if cool:
        items.append(
            AdviceItem(
                category="environment",
                action="Giữ ấm, tránh môi trường quá lạnh / khô kéo dài.",
                priority="medium",
                rationale="Cool temperature context",
                evidence_ids=tuple(
                    eid
                    for eid in (_evidence_id("fact", "temperature"),)
                    if eid in evidence_ids
                ),
            )
        )
    items.extend(
        [
            AdviceItem(
                category="support",
                action=f"Nuôi {_customer_label(facts, stem)}",
                priority="medium",
                rationale="Hỷ thần cultivation",
                evidence_ids=tuple(
                    eid
                    for eid in (_evidence_id("hy", stem),)
                    if eid in evidence_ids
                ),
            )
            for stem in hy
        ]
    )
    items.extend(
        [
            AdviceItem(
                category="avoid",
                action=f"Hạn chế khuếch đại {_customer_label(facts, stem)}",
                priority="medium",
                rationale="Kỵ thần restriction",
                evidence_ids=tuple(
                    eid
                    for eid in (_evidence_id("ky", stem),)
                    if eid in evidence_ids
                ),
            )
            for stem in ky
        ]
    )
    items.append(
        AdviceItem(
            category="decision_guidance",
            action=(
                f"Trước quyết định lớn: kiểm tra có đang thiên về Kỵ thần ({', '.join(ky)}) không."
                if ky
                else "Trước quyết định lớn: kiểm tra có đang thiên về yếu tố bất lợi không."
            ),
            priority="high",
            rationale="Avoid unfavorable element dominance",
            evidence_ids=refs,
        )
    )
    return items


def _build_warnings(
    facts: UsefulGodInterpretationFacts,
    evidence_ids: set[str],
) -> list[WarningItem]:
    """Evidence-backed warnings."""
    warnings: list[WarningItem] = []
    ky = facts.unfavorable_gods
    ky_refs = tuple(
        _evidence_id("ky", s) for s in ky if _evidence_id("ky", s) in evidence_ids
    )

    if ky:
        warnings.append(
            WarningItem(
                condition=f"Overusing Kỵ thần ({', '.join(ky)})",
                risk="Hệ vượng bị kìm / căng",
                severity="medium",
                evidence_ids=ky_refs,
                mitigation="Hạn chế khuếch đại yếu tố bất lợi",
            )
        )
    warnings.append(
        WarningItem(
            condition=f"Ignoring Useful God {facts.selected}",
            risk="Mất ổn định khi hệ mất cân",
            severity="medium",
            evidence_ids=tuple(
                eid
                for eid in (_evidence_id("decision", "reason"),)
                if eid in evidence_ids
            ),
            mitigation=f"Duy trì trọng tâm {facts.selected}",
        )
    )
    if len(set(facts.favorable_gods)) > 1 and ky:
        warnings.append(
            WarningItem(
                condition="Hỷ/Kỵ conflict environment",
                risk="Cam kết dài hạn trong môi trường xung khắc",
                severity="low",
                evidence_ids=ky_refs,
                mitigation="Nhận diện môi trường trước cam kết",
            )
        )
    if facts.temperature_level in {"cool", "cold"}:
        warnings.append(
            WarningItem(
                condition="Cool/cold temperature period",
                risk="Thêm hàn khí khi hệ cần dương / hỏa điều tiết",
                severity="medium",
                evidence_ids=tuple(
                    eid
                    for eid in (_evidence_id("fact", "temperature"),)
                    if eid in evidence_ids
                ),
                mitigation="Giữ ấm, tăng dương khí có kiểm soát",
            )
        )
    return warnings
