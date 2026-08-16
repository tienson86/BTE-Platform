"""Copy Decision Explanation and Useful God interpretation. No calculation."""

from __future__ import annotations

from engines.interpretation_engine.foundation.explanation.models import (
    DecisionExplanationResult,
)
from engines.interpretation_engine.foundation.interpreters.useful_god.result import (
    UsefulGodInterpretationResult,
)
from engines.interpretation_engine.foundation.narrative.collect import (
    copy_statement,
    extend_copied,
)
from engines.interpretation_engine.foundation.narrative.constants import (
    CUSTOMER_DOMAIN_DECISION,
    KIND_APPLICATION,
    KIND_CONCLUSION,
    KIND_EVIDENCE,
    KIND_FACT,
    KIND_REASON,
    KIND_RECOMMENDATION,
    KIND_WARNING,
    SLOT_CONCLUSION,
    SLOT_IMPACT,
    SLOT_OBSERVATION,
    SLOT_REASONING,
    SLOT_RECOMMENDATION,
    SLOT_SUMMARY,
    SLOT_WARNING,
)
from engines.interpretation_engine.foundation.narrative.input import CopiedStatement


def copy_decision_explanation(
    explanation: DecisionExplanationResult,
    statements: list[CopiedStatement],
    refs: list[str],
) -> tuple[str, str, float]:
    """Copy Decision Explanation fields. Do not infer a selected value."""
    prefix = f"decision:{explanation.domain}"
    selected = ""
    reason = ""
    confidence = explanation.confidence
    if explanation.decision is not None:
        selected = explanation.decision.selected
        reason = explanation.decision.reason
        confidence = explanation.decision.confidence
        refs.extend(explanation.decision.supporting_evidence_ids)
        summary = (
            f"{selected}: {reason}" if selected and reason else (reason or selected)
        )
        extend_copied(
            statements,
            copy_statement(
                summary,
                kind=KIND_CONCLUSION,
                slot=SLOT_SUMMARY,
                engine_truth_ref=f"{prefix}:selected",
                customer_domain=CUSTOMER_DOMAIN_DECISION,
                confidence=confidence,
            ),
        )
        extend_copied(
            statements,
            copy_statement(
                reason,
                kind=KIND_REASON,
                slot=SLOT_REASONING,
                engine_truth_ref=f"{prefix}:reason",
                customer_domain=CUSTOMER_DOMAIN_DECISION,
                confidence=confidence,
            ),
        )
    for fact in explanation.analysis:
        extend_copied(
            statements,
            copy_statement(
                f"{fact.fact}={fact.value}",
                kind=KIND_FACT,
                slot=SLOT_OBSERVATION,
                engine_truth_ref=f"{prefix}:fact:{fact.source}:{fact.fact}",
                confidence=confidence,
            ),
        )
        refs.append(fact.source)
    for item in explanation.evidence:
        extend_copied(
            statements,
            copy_statement(
                f"{item.fact}={item.value}" if item.value else item.fact,
                kind=KIND_EVIDENCE,
                slot=SLOT_OBSERVATION,
                engine_truth_ref=item.evidence_id or f"{prefix}:evidence:{item.rule_id}",
                confidence=item.confidence or confidence,
            ),
        )
        if item.rule_id:
            refs.append(item.rule_id)
    for step in explanation.decision_path:
        extend_copied(
            statements,
            copy_statement(
                step.outcome or step.title,
                kind=KIND_REASON,
                slot=SLOT_REASONING,
                engine_truth_ref=f"{prefix}:path:{step.step_id}",
                confidence=confidence,
            ),
        )
        refs.extend(step.rule_refs)
    for alt in explanation.alternatives:
        if alt.status != "rejected":
            continue
        extend_copied(
            statements,
            copy_statement(
                alt.rejection_reason or f"{alt.candidate} rejected",
                kind=KIND_REASON,
                slot=SLOT_REASONING,
                engine_truth_ref=f"{prefix}:rejected:{alt.candidate}",
                customer_domain=CUSTOMER_DOMAIN_DECISION,
                confidence=confidence,
            ),
        )
    for item in explanation.domain_meaning:
        extend_copied(
            statements,
            copy_statement(
                item.statement,
                kind=KIND_CONCLUSION,
                slot=SLOT_CONCLUSION,
                engine_truth_ref=f"{prefix}:meaning",
                confidence=confidence,
            ),
        )
    for item in explanation.applications:
        extend_copied(
            statements,
            copy_statement(
                item.statement,
                kind=KIND_APPLICATION,
                slot=SLOT_IMPACT,
                engine_truth_ref=f"{prefix}:application:{item.domain}",
                customer_domain=item.domain,
                confidence=item.confidence or confidence,
            ),
        )
    for item in explanation.advice:
        extend_copied(
            statements,
            copy_statement(
                item.action,
                kind=KIND_RECOMMENDATION,
                slot=SLOT_RECOMMENDATION,
                engine_truth_ref=f"{prefix}:advice:{item.category}",
                category=item.category,
                rationale=item.rationale,
                confidence=confidence,
            ),
        )
    for item in explanation.warnings:
        extend_copied(
            statements,
            copy_statement(
                item.risk,
                kind=KIND_WARNING,
                slot=SLOT_WARNING,
                engine_truth_ref=f"{prefix}:warning:{item.condition}",
                condition=item.condition,
                mitigation=item.mitigation,
                confidence=confidence,
            ),
        )
    return selected, reason, confidence


def copy_useful_god_interpretation(
    result: UsefulGodInterpretationResult,
    statements: list[CopiedStatement],
    refs: list[str],
) -> None:
    """Copy Useful God interpreter slots already validated upstream."""
    prefix = "decision:UsefulGod:interpretation"
    refs.extend(result.evidence.rule_ids)
    if result.evidence.selected_rule_id:
        refs.append(result.evidence.selected_rule_id)
    for index, text in enumerate(result.observations):
        extend_copied(
            statements,
            copy_statement(
                text,
                kind=KIND_FACT,
                slot=SLOT_OBSERVATION,
                engine_truth_ref=f"{prefix}:observation:{index}",
                confidence=result.confidence,
            ),
        )
    for index, text in enumerate(result.reasoning):
        extend_copied(
            statements,
            copy_statement(
                text,
                kind=KIND_REASON,
                slot=SLOT_REASONING,
                engine_truth_ref=f"{prefix}:reasoning:{index}",
                confidence=result.confidence,
            ),
        )
    for index, text in enumerate(result.conclusions):
        extend_copied(
            statements,
            copy_statement(
                text,
                kind=KIND_CONCLUSION,
                slot=SLOT_CONCLUSION,
                engine_truth_ref=f"{prefix}:conclusion:{index}",
                confidence=result.confidence,
            ),
        )
    for item in result.impacts:
        extend_copied(
            statements,
            copy_statement(
                item.text,
                kind=KIND_APPLICATION,
                slot=SLOT_IMPACT,
                engine_truth_ref=f"{prefix}:impact:{item.domain}",
                customer_domain=item.domain,
                confidence=result.confidence,
            ),
        )
    for group in result.recommendations:
        for index, text in enumerate(group.items):
            extend_copied(
                statements,
                copy_statement(
                    text,
                    kind=KIND_RECOMMENDATION,
                    slot=SLOT_RECOMMENDATION,
                    engine_truth_ref=f"{prefix}:recommendation:{group.category}:{index}",
                    category=group.category,
                    customer_domain=group.category,
                    confidence=result.confidence,
                ),
            )
    for index, text in enumerate(result.warnings):
        extend_copied(
            statements,
            copy_statement(
                text,
                kind=KIND_WARNING,
                slot=SLOT_WARNING,
                engine_truth_ref=f"{prefix}:warning:{index}",
                confidence=result.confidence,
            ),
        )
