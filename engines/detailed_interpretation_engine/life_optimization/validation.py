"""Guard Life Optimization contracts. Does not invent natal or temporal truth."""

from __future__ import annotations

from uuid import uuid4

from engines.detailed_interpretation_engine.constants import SCHEMA_LIFE_OPTIMIZATION
from engines.detailed_interpretation_engine.context_layers import CanonicalAnalysisContext
from engines.detailed_interpretation_engine.enums import EvaluationStatus, IssueSeverity
from engines.detailed_interpretation_engine.evidence_priority.constants import SHEN_SHA_SOURCE_KINDS
from engines.detailed_interpretation_engine.life_optimization.constants import (
    ACTION_STATES,
    ACTION_TYPES,
    FORBIDDEN_ACTION_KEYS,
    KNOWN_OPTIMIZATION_IDS,
    MAIN_OPTIMIZATION_IDS,
    OVERLOAD_AVOID_KEYS,
    PRIORITY_VALUES,
    TIME_SCOPES,
)
from engines.detailed_interpretation_engine.optimization import LifeOptimizationResult
from engines.detailed_interpretation_engine.validation import ValidationIssue, ValidationResult, result_from_issues


def validate_life_optimization_result(
    result: LifeOptimizationResult,
    context: CanonicalAnalysisContext | None = None,
) -> ValidationResult:
    """Guard sources, priority floor, natal/temporal split, and safety boundaries."""
    analysis_id = context.analysis_id if context is not None else result.analysis_id
    issues: list[ValidationIssue] = []

    def add(
        code: str,
        severity: IssueSeverity,
        message: str,
        *,
        field: str = "",
        expected: str = "",
        actual: str = "",
    ) -> None:
        issues.append(
            ValidationIssue(
                code=code,
                severity=severity,
                layer="optimization",
                field=field,
                message=message,
                expected=expected,
                actual=actual,
                trace_id=f"p7v-{uuid4().hex[:12]}",
                validator="validate_life_optimization_result",
                analysis_id=analysis_id,
            )
        )

    if result.schema_version and result.schema_version != SCHEMA_LIFE_OPTIMIZATION:
        add(
            "P7V-VERSION-UNSUPPORTED",
            IssueSeverity.CRITICAL,
            "unsupported schema version",
            field="schema_version",
            expected=SCHEMA_LIFE_OPTIMIZATION,
            actual=result.schema_version,
        )
    if result.state in {EvaluationStatus.NOT_EVALUATED, EvaluationStatus.NOT_APPLICABLE}:
        return result_from_issues(issues, analysis_id=analysis_id)
    natal_ids = set(result.natal_plan.action_ids)
    temporal_ids = set(result.temporal_plan.action_ids)
    if natal_ids & temporal_ids:
        add(
            "P7V-OPT-NATAL-TEMPORAL-SPLIT",
            IssueSeverity.ERROR,
            "natal and temporal plans must stay distinct",
            field="natal_plan.action_ids",
        )
    known_evidence = set(result.evidence_ids)
    if context is not None:
        known_evidence.update(context.runtime.interpretation.evidence_priority.evidence_ids)
        for domain_id in MAIN_OPTIMIZATION_IDS:
            natal = getattr(context.runtime.domains, domain_id).natal
            known_evidence.update(natal.evidence_ids)
        known_evidence.update(context.runtime.temporal.luck_activation.evidence_ids)
        known_evidence.update(context.runtime.temporal.luck_interaction.evidence_ids)
        known_evidence.update(context.runtime.temporal.temporal_activation.evidence_ids)
        shen_findings = {
            item.finding_id
            for item in context.runtime.interpretation.evidence_priority.findings
            if item.source_kind in SHEN_SHA_SOURCE_KINDS
        }
    else:
        shen_findings = set()
    for action in result.actions:
        if action.action_type not in ACTION_TYPES:
            add(
                "P7V-OPT-ACTION-TYPE",
                IssueSeverity.ERROR,
                "unknown action type",
                field="actions.action_type",
                actual=action.action_type,
            )
        if action.state not in ACTION_STATES:
            add(
                "P7V-OPT-ACTION-STATE",
                IssueSeverity.ERROR,
                "unknown action state",
                field="actions.state",
                actual=action.state,
            )
        if action.priority not in PRIORITY_VALUES:
            add(
                "P7V-OPT-ACTION-PRIORITY",
                IssueSeverity.ERROR,
                "unknown action priority",
                field="actions.priority",
                actual=action.priority,
            )
        if action.time_scope not in TIME_SCOPES:
            add(
                "P7V-OPT-TIME-SCOPE",
                IssueSeverity.ERROR,
                "unknown time scope",
                field="actions.time_scope",
                actual=action.time_scope,
            )
        if action.target_domain and action.target_domain not in KNOWN_OPTIMIZATION_IDS:
            add(
                "P7V-OPT-TARGET-DOMAIN",
                IssueSeverity.ERROR,
                "action target domain unknown",
                field="actions.target_domain",
                actual=action.target_domain,
            )
        if not action.evidence_ids:
            add(
                "P7V-OPTIMIZATION-ACTION-NO-RESULT",
                IssueSeverity.ERROR,
                "optimization actions require a supporting result",
                field="actions.evidence_ids",
                actual=action.action_id,
            )
        if action.driver_kind == "shen_sha" and action.action_type != "monitor":
            add(
                "P7V-OPT-SHEN-SHA-DRIVER",
                IssueSeverity.CRITICAL,
                "Shen Sha must not drive actions",
                field="actions.driver_kind",
                actual=action.action_id,
            )
        if shen_findings and set(action.evidence_ids) <= shen_findings and action.action_type != "monitor":
            add(
                "P7V-OPT-SHEN-SHA-DRIVER",
                IssueSeverity.CRITICAL,
                "Shen Sha must not drive actions",
                field="actions.evidence_ids",
                actual=action.action_id,
            )
        key = action.recommended_action_key.lower()
        if any(token in key for token in FORBIDDEN_ACTION_KEYS):
            add(
                "P7V-OPT-SAFETY",
                IssueSeverity.CRITICAL,
                "forbidden action key",
                field="actions.recommended_action_key",
                actual=action.recommended_action_key,
            )
        if action.recommended_action_key in OVERLOAD_AVOID_KEYS:
            add(
                "P7V-OPT-SATURATION",
                IssueSeverity.ERROR,
                "overloaded domain must not recommend more load",
                field="actions.recommended_action_key",
                actual=action.recommended_action_key,
            )
        if context is not None and action.target_mechanism:
            natal = getattr(context.runtime.domains, action.target_domain, None)
            if natal is not None:
                source = natal.natal
                known_mechs = {source.bottleneck, source.leakage, source.driver_id, source.risk, *source.dimensions}
                if (
                    action.target_mechanism
                    and action.category in {"bottleneck", "leakage"}
                    and action.target_mechanism not in known_mechs
                    and action.target_mechanism
                    not in {
                        "capital_discipline",
                        "commercialization",
                        "communication",
                        "transmission",
                        "recovery",
                        "workload_control",
                        "pressure_control",
                        "authority_exposure",
                        "expansion",
                        "management",
                        "useful_god_function",
                    }
                ):
                    add(
                        "P7V-OPT-BOTTLENECK-REF",
                        IssueSeverity.ERROR,
                        "referenced bottleneck does not exist",
                        field="actions.target_mechanism",
                        actual=action.target_mechanism,
                    )
    for action_id in result.top_priorities:
        if action_id and action_id not in {item.action_id for item in result.actions}:
            add(
                "P7V-OPT-TOP-SOURCE",
                IssueSeverity.ERROR,
                "top priority must reference a real action",
                field="top_priorities",
                actual=action_id,
            )
    for domain_id, plan in result.domain_plans.items():
        if domain_id not in KNOWN_OPTIMIZATION_IDS:
            add(
                "P7V-CTX-REF-SHAPE",
                IssueSeverity.ERROR,
                "action references unknown domain",
                field="domain_plans",
                actual=domain_id,
            )
        if plan.bottleneck and context is not None:
            natal = getattr(context.runtime.domains, domain_id).natal
            if plan.bottleneck != natal.bottleneck and plan.bottleneck not in natal.dimensions:
                add(
                    "P7V-OPT-BOTTLENECK-REF",
                    IssueSeverity.ERROR,
                    "domain plan bottleneck does not exist",
                    field="domain_plans.bottleneck",
                    actual=plan.bottleneck,
                )
    useful = str(result.useful_god_plan.useful_god).lower()
    joined_actions = " ".join(item.recommended_action_key for item in result.actions).lower()
    if "wear_red" in useful or "wear_red" in joined_actions or "mặc đỏ" in joined_actions:
        add(
            "P7V-OPT-USEFUL-GOD-DECORATIVE",
            IssueSeverity.CRITICAL,
            "Useful God must stay function-first",
            field="useful_god_plan",
        )
    return result_from_issues(issues, analysis_id=analysis_id)
