"""Guard Temporal Activation contracts. Does not reason about new natal truth."""

from __future__ import annotations

from typing import Any
from uuid import uuid4

from engines.detailed_interpretation_engine.constants import SCHEMA_TEMPORAL, TEMPORAL_LAYER_PARENT
from engines.detailed_interpretation_engine.context_layers import CanonicalAnalysisContext
from engines.detailed_interpretation_engine.enums import EvaluationStatus, IssueSeverity
from engines.detailed_interpretation_engine.temporal import TemporalActivationResult
from engines.detailed_interpretation_engine.temporal_activation.constants import (
    ANNUAL_SOURCE_PATH,
    CONTRACT_SHELL_LAYERS,
    EXPRESSION_STATES,
    FORBIDDEN_DRIVER_IDS,
    KNOWN_LAYER_IDS,
    MAIN_TEMPORAL_IDS,
    MODIFIER_EFFECTS,
    TEMPORAL_BOTTLENECK_IDS,
    TEMPORAL_DRIVER_IDS,
)
from engines.detailed_interpretation_engine.validation import ValidationIssue, ValidationResult, result_from_issues


def validate_temporal_activation_result(
    result: TemporalActivationResult,
    context: CanonicalAnalysisContext | None = None,
) -> ValidationResult:
    """Guard hierarchy, year window, immutability, and annual-only drivers."""
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
                layer="temporal_activation",
                field=field,
                message=message,
                expected=expected,
                actual=actual,
                trace_id=f"p7v-{uuid4().hex[:12]}",
                validator="validate_temporal_activation_result",
                analysis_id=analysis_id,
            )
        )

    if result.schema_version and result.schema_version != SCHEMA_TEMPORAL:
        add(
            "P7V-VERSION-UNSUPPORTED",
            IssueSeverity.CRITICAL,
            "unsupported schema version",
            field="schema_version",
            expected=SCHEMA_TEMPORAL,
            actual=result.schema_version,
        )
    if result.analysis_id and analysis_id and result.analysis_id != analysis_id:
        add(
            "P7V-TA-ANALYSIS-ID",
            IssueSeverity.ERROR,
            "analysis_id mismatch",
            field="analysis_id",
            expected=analysis_id,
            actual=result.analysis_id,
        )
    if result.state in {EvaluationStatus.NOT_EVALUATED, EvaluationStatus.NOT_APPLICABLE}:
        return result_from_issues(issues, analysis_id=analysis_id)

    for layer in result.requested_layers + result.evaluated_layers + tuple(result.layer_results):
        if layer and layer not in KNOWN_LAYER_IDS:
            add(
                "P7V-TA-LAYER",
                IssueSeverity.ERROR,
                "unknown temporal layer",
                field="layer",
                actual=layer,
            )
    if result.active_layer in TEMPORAL_LAYER_PARENT:
        expected_parent = TEMPORAL_LAYER_PARENT[result.active_layer]
        if result.parent_layer and result.parent_layer != expected_parent:
            add(
                "P7V-TA-PARENT",
                IssueSeverity.CRITICAL,
                "child layer must refine its canonical parent",
                field="parent_layer",
                expected=expected_parent,
                actual=result.parent_layer,
            )
    for layer_id, layer_result in result.layer_results.items():
        parent = layer_result.parent_layer or TEMPORAL_LAYER_PARENT.get(layer_id, "")
        expected = TEMPORAL_LAYER_PARENT.get(layer_id, "")
        if expected and parent and parent != expected:
            add(
                "P7V-TA-LAYER-PARENT",
                IssueSeverity.CRITICAL,
                "layer parent-child hierarchy mismatch",
                field=f"{layer_id}.parent_layer",
                expected=expected,
                actual=parent,
            )
        if layer_id in CONTRACT_SHELL_LAYERS and layer_result.state not in {
            EvaluationStatus.NOT_EVALUATED,
            EvaluationStatus.NOT_APPLICABLE,
        }:
            add(
                "P7V-TA-SHELL",
                IssueSeverity.CRITICAL,
                "monthly/daily/hourly must stay not_evaluated in this ticket",
                field=layer_id,
                actual=layer_result.state.value,
            )

    if "annual" in result.evaluated_layers:
        if not result.time_window or not result.time_window.isdigit():
            add(
                "P7V-TA-YEAR",
                IssueSeverity.CRITICAL,
                "annual result requires an exact year window",
                field="time_window",
                actual=result.time_window,
            )
        if result.time_window.lower() in {"năm nay", "nam nay"}:
            add(
                "P7V-TA-YEAR-AMBIGUOUS",
                IssueSeverity.CRITICAL,
                "annual time window cannot be ambiguous",
                field="time_window",
                actual=result.time_window,
            )
        annual = result.layer_results.get("annual")
        if annual is None:
            add(
                "P7V-TA-ANNUAL-LAYER",
                IssueSeverity.CRITICAL,
                "evaluated annual layer is missing",
                field="layer_results.annual",
            )
        else:
            if annual.source_identity and annual.source_identity != ANNUAL_SOURCE_PATH:
                add(
                    "P7V-TA-ANNUAL-SOURCE",
                    IssueSeverity.CRITICAL,
                    "annual identity must come from canonical Liunian owner",
                    field="source_identity",
                    expected=ANNUAL_SOURCE_PATH,
                    actual=annual.source_identity,
                )
            if not annual.temporal_pillar:
                add(
                    "P7V-TA-ANNUAL-PILLAR",
                    IssueSeverity.ERROR,
                    "annual layer requires a canonical pillar",
                    field="temporal_pillar",
                )
            for actor in annual.temporal_actors:
                if actor.role == "natal":
                    add(
                        "P7V-TA-NATAL-ACTOR",
                        IssueSeverity.CRITICAL,
                        "annual actors cannot be natal Ten Gods",
                        field="temporal_actors",
                    )
        for domain_id in MAIN_TEMPORAL_IDS:
            item = result.domain_results.get(domain_id)
            if item is None:
                add(
                    "P7V-TA-MAIN-MISSING",
                    IssueSeverity.ERROR,
                    "main domain missing annual result",
                    field=domain_id,
                )
                continue
            if item.annual_expression_state not in EXPRESSION_STATES:
                add(
                    "P7V-TA-EXPRESSION",
                    IssueSeverity.ERROR,
                    "unknown annual expression state",
                    field=f"{domain_id}.annual_expression_state",
                    actual=item.annual_expression_state,
                )
            if item.annual_modifier not in MODIFIER_EFFECTS:
                add(
                    "P7V-TA-MODIFIER",
                    IssueSeverity.ERROR,
                    "unknown annual modifier",
                    field=f"{domain_id}.annual_modifier",
                    actual=item.annual_modifier,
                )
            driver = item.temporal_driver.strip()
            if driver not in TEMPORAL_DRIVER_IDS:
                add(
                    "P7V-TA-DRIVER",
                    IssueSeverity.ERROR,
                    "unknown temporal driver",
                    field=f"{domain_id}.temporal_driver",
                    actual=driver,
                )
            if driver in FORBIDDEN_DRIVER_IDS and driver not in {"not_applicable", "unresolved"}:
                add(
                    "P7V-TA-DRIVER-FOREIGN",
                    IssueSeverity.CRITICAL,
                    "temporal driver cannot copy natal, luck, or interaction drivers",
                    field=f"{domain_id}.temporal_driver",
                    actual=driver,
                )
            bottleneck = item.temporal_bottleneck.strip() or "none"
            if bottleneck not in TEMPORAL_BOTTLENECK_IDS:
                add(
                    "P7V-TA-BOTTLENECK",
                    IssueSeverity.ERROR,
                    "unknown temporal bottleneck",
                    field=f"{domain_id}.temporal_bottleneck",
                    actual=bottleneck,
                )
            if not item.evidence_ids and item.annual_expression_state not in {"dormant", "blocked", "unresolved"}:
                add(
                    "P7V-TA-EVIDENCE",
                    IssueSeverity.CRITICAL,
                    "annual expression requires evidence",
                    field=domain_id,
                )

    if context is not None:
        _check_immutability(add, result, context)

    return result_from_issues(issues, analysis_id=analysis_id)


def _check_immutability(add: Any, result: TemporalActivationResult, context: CanonicalAnalysisContext) -> None:
    activation = context.runtime.temporal.luck_activation
    interaction = context.runtime.temporal.luck_interaction
    natal_map = _natal_states(context)
    for domain_id, item in result.domain_results.items():
        natal = natal_map.get(domain_id)
        luck_item = activation.items.get(domain_id)
        if natal is not None and item.natal_state and item.natal_state != natal[0]:
            add(
                "P7V-TA-MUTATE-DOMAIN",
                IssueSeverity.CRITICAL,
                "annual must not rewrite natal Domain state",
                field=f"{domain_id}.natal_state",
                expected=natal[0],
                actual=item.natal_state,
            )
        if luck_item is not None and item.luck_activation_state:
            expected = luck_item.activation_state.value
            if item.luck_activation_state != expected:
                add(
                    "P7V-TA-MUTATE-LUCK",
                    IssueSeverity.CRITICAL,
                    "annual must not rewrite Luck Activation state",
                    field=f"{domain_id}.luck_activation_state",
                    expected=expected,
                    actual=item.luck_activation_state,
                )
    if result.analysis_id and interaction.analysis_id and result.analysis_id != interaction.analysis_id:
        if interaction.analysis_id:
            add(
                "P7V-TA-MUTATE-INTERACTION",
                IssueSeverity.CRITICAL,
                "annual must not rewrite luck interaction identity",
                field="analysis_id",
                expected=interaction.analysis_id,
                actual=result.analysis_id,
            )


def _natal_states(context: CanonicalAnalysisContext) -> dict[str, tuple[str, str]]:
    section = context.runtime.domains
    items = {
        "authority": (section.authority.natal.state.value, section.authority.natal.driver_id),
        "career": (section.career.natal.state.value, section.career.natal.driver_id),
        "wealth": (section.wealth.natal.state.value, section.wealth.natal.driver_id),
        "relationship": (section.relationship.natal.state.value, section.relationship.natal.driver_id),
        "legacy": (section.legacy.natal.state.value, section.legacy.natal.driver_id),
        "vitality": (section.vitality.natal.state.value, section.vitality.natal.driver_id),
    }
    for domain_id, natal in section.supporting.items():
        items[domain_id] = (natal.state.value, natal.driver_id)
    return items
