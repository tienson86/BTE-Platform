"""Adapt DecisionExplanationResult to Sprint B1 UsefulGodInterpretationResult."""

from __future__ import annotations

from engines.interpretation_engine.foundation.explanation.models import (
    AnalysisFact,
    DecisionExplanationResult,
)
from engines.interpretation_engine.foundation.interpreters.useful_god.result import (
    UsefulGodCandidateScoreEvidence,
    UsefulGodDomainImpact,
    UsefulGodInterpretationEvidence,
    UsefulGodInterpretationResult,
    UsefulGodRecommendationGroup,
)
from engines.interpretation_engine.foundation.interpreters.useful_god.templates import (
    GROUP_LABEL_VI,
    GROUP_PRIORITY,
)

_OBSERVATION_LABELS: dict[str, str] = {
    "day_master": "Nhật chủ",
    "month_branch": "Lệnh tháng",
    "season": "Mùa",
    "strength": "Thân",
    "temperature": "Điều hậu",
    "five_elements": "Phân bố ngũ hành",
    "useful_god_selected": "Dụng thần được chọn",
    "favorable_gods": "Hỷ thần",
    "unfavorable_gods": "Kỵ thần",
}


_ADVICE_CATEGORY_MAP: dict[str, str] = {
    "priority_action": "priority_actions",
    "support": "elements_to_cultivate",
    "avoid": "elements_to_avoid",
    "environment": "supportive_environments",
    "decision_guidance": "decision_guidance",
}


def to_useful_god_interpretation_result(
    explanation: DecisionExplanationResult,
) -> UsefulGodInterpretationResult:
    """Map framework explanation to backward-compatible B1 contract."""
    observations = _observations_from_analysis(explanation.analysis)
    reasoning = _reasoning_from_path(explanation)

    conclusions = tuple(item.statement for item in explanation.domain_meaning)

    candidate_scores: list[UsefulGodCandidateScoreEvidence] = []
    rule_ids: list[str] = []
    selected_rule_id = ""
    engine_source = "UsefulGodEngine"

    for item in explanation.evidence:
        if item.rule_id:
            rule_ids.append(item.rule_id)
        if item.source_field.startswith("candidate."):
            candidate_scores.append(
                UsefulGodCandidateScoreEvidence(
                    useful_god=item.fact,
                    rule_id=item.rule_id,
                    confidence=item.confidence,
                    rule_group=item.relevance,
                    reason=item.value,
                )
            )
        if explanation.decision and item.evidence_id in explanation.decision.supporting_evidence_ids:
            if item.rule_id:
                selected_rule_id = item.rule_id
        if item.source_engine:
            engine_source = item.source_engine

    if explanation.decision and not selected_rule_id:
        for item in explanation.evidence:
            if item.fact == explanation.decision.selected and item.rule_id:
                selected_rule_id = item.rule_id
                break

    evidence = UsefulGodInterpretationEvidence(
        rule_ids=tuple(dict.fromkeys(rule_ids)),
        selected_rule_id=selected_rule_id,
        candidate_scores=tuple(candidate_scores),
        confidence=explanation.confidence,
        engine_source=engine_source,
        matched_rules=tuple(dict.fromkeys(rule_ids)),
    )

    impacts = tuple(
        UsefulGodDomainImpact(domain=item.domain, text=item.statement)
        for item in explanation.applications
    )

    rec_groups: dict[str, list[str]] = {}
    for item in explanation.advice:
        category = _ADVICE_CATEGORY_MAP.get(item.category, item.category)
        rec_groups.setdefault(category, []).append(item.action)
    recommendations = tuple(
        UsefulGodRecommendationGroup(category=cat, items=tuple(actions))
        for cat, actions in rec_groups.items()
    )

    warnings = tuple(
        f"{item.condition}: {item.risk}" + (f" — {item.mitigation}" if item.mitigation else "")
        for item in explanation.warnings
    )

    return UsefulGodInterpretationResult(
        observations=observations,
        reasoning=reasoning,
        evidence=evidence,
        conclusions=conclusions,
        impacts=impacts,
        recommendations=recommendations,
        warnings=warnings,
        confidence=explanation.confidence,
        diagnostics=explanation.diagnostics,
        status=explanation.status,
    )


def _observations_from_analysis(analysis: tuple[AnalysisFact, ...]) -> tuple[str, ...]:
    """Map analysis facts to B1 observation phrasing."""
    lines: list[str] = []
    month_branch = ""
    season = ""
    for item in analysis:
        if item.fact == "month_branch":
            month_branch = item.value
            continue
        if item.fact == "season":
            season = item.value
            continue

    for item in analysis:
        label = _OBSERVATION_LABELS.get(item.fact, item.fact)
        if item.fact == "month_branch":
            continue
        if item.fact == "season":
            lines.append(f"Lệnh tháng: {month_branch}; mùa: {season}.")
            continue
        lines.append(f"{label}: {item.value}.")
    return tuple(lines)


def _reasoning_from_path(explanation: DecisionExplanationResult) -> tuple[str, ...]:
    """Map decision path to B1 reasoning lines."""
    lines: list[str] = []
    if explanation.decision is not None:
        group = explanation.decision.selected_type
        priority = GROUP_PRIORITY.get(group, 0)
        label = GROUP_LABEL_VI.get(group, group)
        lines.append(
            f"Engine chọn {explanation.decision.selected} với độ tin cậy "
            f"{explanation.confidence:.2f} dựa trên nhóm {label} (ưu tiên {priority})."
        )
        if explanation.decision.reason:
            lines.append(f"Lý do engine: {explanation.decision.reason}.")

    for step in sorted(explanation.decision_path, key=lambda s: s.order):
        if step.step_id in {"select_winner", "read_day_master_season"}:
            continue
        if step.step_id == "read_strength" and step.outcome:
            strength_note = step.outcome.replace("Thân ", "")
            lines.append(
                f"Bối cảnh thân {strength_note.split('(')[0].strip()} "
                f"({step.outcome.split('(')[1].split(')')[0] if '(' in step.outcome else ''}) "
                f"làm nền cho các ứng viên nhóm thân vượng nhược."
            )
            continue
        if step.step_id == "read_temperature" and step.outcome:
            lines.append(
                f"Điều hậu {step.outcome.replace('Điều hậu ', '')} "
                f"kích hoạt các ứng viên nhóm điều hậu / khí hậu."
            )
            continue
        if step.step_id == "explain_rejected" and step.outcome:
            for part in step.outcome.split(" | "):
                if part:
                    lines.append(_format_rejection_line(part))
            continue
        if step.step_id == "compare_groups" and step.outcome:
            continue
        if step.outcome and step.step_id not in {"load_candidates", "read_five_elements"}:
            lines.append(step.outcome)

    return tuple(lines)


def _format_rejection_line(part: str) -> str:
    """Convert compact rejection summary to B1-style sentence."""
    if ": same stem" in part:
        stem = part.split("(")[0].strip()
        return (
            f"{stem} không được chọn vì cùng Dụng thần nhưng nhóm ưu tiên thấp hơn "
            f"so với ứng viên thắng."
        )
    if "group priority" in part:
        stem = part.split("(")[0].strip()
        return f"{stem} bị loại vì nhóm ưu tiên thấp hơn so với ứng viên thắng."
    if "lower score" in part:
        stem = part.split("(")[0].strip()
        return f"{stem} bị loại vì điểm thấp hơn ứng viên thắng trong cùng tầng ưu tiên."
    return part
