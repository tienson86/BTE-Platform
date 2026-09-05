"""Guard Luck Interaction contracts. Does not reason about new natal truth."""

from __future__ import annotations

from uuid import uuid4

from engines.detailed_interpretation_engine.constants import SCHEMA_LUCK_INTERACTION
from engines.detailed_interpretation_engine.context_layers import CanonicalAnalysisContext
from engines.detailed_interpretation_engine.domain_interpretation.constants import DOMAIN_DRIVER_IDS
from engines.detailed_interpretation_engine.enums import EvaluationStatus, IssueSeverity
from engines.detailed_interpretation_engine.luck_activation.constants import KNOWN_ACTIVATION_IDS
from engines.detailed_interpretation_engine.luck_interaction.constants import (
    DRIVER_SENTINELS,
    GRAPH_RELATIONS,
    INTERACTION_TYPES,
    KNOWN_INTERACTION_IDS,
    SITUATION_IDS,
    STRENGTH_RANK,
)
from engines.detailed_interpretation_engine.temporal import LuckInteractionResult
from engines.detailed_interpretation_engine.validation import ValidationIssue, ValidationResult, result_from_issues


def validate_luck_interaction_result(
    result: LuckInteractionResult,
    context: CanonicalAnalysisContext | None = None,
) -> ValidationResult:
    """Guard interaction IDs, evidence, and immutability of activation and natal domains."""
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
                layer="luck_interaction",
                field=field,
                message=message,
                expected=expected,
                actual=actual,
                trace_id=f"p7v-{uuid4().hex[:12]}",
                validator="validate_luck_interaction_result",
                analysis_id=analysis_id,
            )
        )

    if result.schema_version and result.schema_version != SCHEMA_LUCK_INTERACTION:
        add(
            "P7V-VERSION-UNSUPPORTED",
            IssueSeverity.CRITICAL,
            "unsupported schema version",
            field="schema_version",
            expected=SCHEMA_LUCK_INTERACTION,
            actual=result.schema_version,
        )
    if result.analysis_id and analysis_id and result.analysis_id != analysis_id:
        add(
            "P7V-LI-ANALYSIS-ID",
            IssueSeverity.ERROR,
            "analysis_id mismatch",
            field="analysis_id",
            expected=analysis_id,
            actual=result.analysis_id,
        )
    if result.status in {EvaluationStatus.NOT_EVALUATED, EvaluationStatus.NOT_APPLICABLE}:
        return result_from_issues(issues, analysis_id=analysis_id)

    activation = context.runtime.temporal.luck_activation if context is not None else None
    items = activation.items if activation is not None else {}
    natal = context.runtime.domains if context is not None else None
    natal_map = _natal_states(context)
    natal_driver_ids = {
        item for values in DOMAIN_DRIVER_IDS.values() for item in values
    } - {"not_applicable", "unresolved"}

    if activation is not None:
        if result.cycle_id and activation.cycle_id and result.cycle_id != activation.cycle_id:
            add(
                "P7V-LI-CYCLE",
                IssueSeverity.CRITICAL,
                "interaction must consume the current luck cycle, not recalculate it",
                field="cycle_id",
                expected=activation.cycle_id,
                actual=result.cycle_id,
            )
        if result.time_window and activation.time_window and result.time_window != activation.time_window:
            add(
                "P7V-LI-WINDOW",
                IssueSeverity.CRITICAL,
                "interaction must reuse the luck activation window",
                field="time_window",
                expected=activation.time_window,
                actual=result.time_window,
            )

    finding_ids = {item.finding_id for item in result.findings}
    for finding in result.findings:
        if finding.source_domain not in KNOWN_INTERACTION_IDS:
            add(
                "P7V-LI-SOURCE",
                IssueSeverity.ERROR,
                "interaction source must be a known domain",
                field="source_domain",
                actual=finding.source_domain,
            )
        if finding.target_domain not in KNOWN_INTERACTION_IDS:
            add(
                "P7V-LI-TARGET",
                IssueSeverity.ERROR,
                "interaction target must be a known domain",
                field="target_domain",
                actual=finding.target_domain,
            )
        if items:
            if finding.source_domain not in items:
                add(
                    "P7V-LI-SOURCE-ACTIVATION",
                    IssueSeverity.ERROR,
                    "interaction source activation is missing",
                    field=finding.source_domain,
                )
            if finding.target_domain not in items:
                add(
                    "P7V-LI-TARGET-ACTIVATION",
                    IssueSeverity.ERROR,
                    "interaction target activation is missing",
                    field=finding.target_domain,
                )
        if not finding.evidence_ids:
            add(
                "P7V-LI-EVIDENCE",
                IssueSeverity.CRITICAL,
                "interaction edge requires evidence",
                field=finding.finding_id or f"{finding.source_domain}->{finding.target_domain}",
            )
        if finding.interaction_type not in INTERACTION_TYPES:
            add(
                "P7V-LI-TYPE",
                IssueSeverity.ERROR,
                "unknown interaction type",
                field="interaction_type",
                actual=finding.interaction_type,
            )
        if finding.strength not in STRENGTH_RANK:
            add(
                "P7V-LI-STRENGTH",
                IssueSeverity.ERROR,
                "unknown interaction strength",
                field="strength",
                actual=finding.strength,
            )

    for edge in result.graph.edges:
        if edge.relation not in GRAPH_RELATIONS:
            add(
                "P7V-LI-GRAPH-RELATION",
                IssueSeverity.ERROR,
                "unknown interaction graph relation",
                field="graph.edges.relation",
                actual=edge.relation,
            )
        if not edge.evidence_ids:
            add(
                "P7V-LI-GRAPH-EVIDENCE",
                IssueSeverity.CRITICAL,
                "interaction graph edge requires evidence",
                field=f"{edge.source}->{edge.target}",
            )
        if edge.source not in KNOWN_ACTIVATION_IDS or edge.target not in KNOWN_ACTIVATION_IDS:
            add(
                "P7V-LI-GRAPH-DOMAIN",
                IssueSeverity.CRITICAL,
                "interaction graph must connect domain activation to domain activation",
                field=f"{edge.source}->{edge.target}",
            )

    driver = result.interaction_driver.strip()
    bottleneck = result.interaction_bottleneck.strip()
    if driver and driver not in DRIVER_SENTINELS:
        if driver not in KNOWN_INTERACTION_IDS:
            add(
                "P7V-LI-DRIVER",
                IssueSeverity.ERROR,
                "interaction_driver must be an activated domain",
                field="interaction_driver",
                actual=driver,
            )
        if driver in natal_driver_ids and driver not in KNOWN_INTERACTION_IDS:
            add(
                "P7V-LI-DRIVER-NATAL",
                IssueSeverity.CRITICAL,
                "interaction_driver cannot copy natal Domain Driver",
                field="interaction_driver",
                actual=driver,
            )
        if items and driver not in items:
            add(
                "P7V-LI-DRIVER-ACTIVATION",
                IssueSeverity.ERROR,
                "interaction_driver activation is missing",
                field="interaction_driver",
                actual=driver,
            )
    if bottleneck and bottleneck not in DRIVER_SENTINELS:
        if bottleneck not in KNOWN_INTERACTION_IDS:
            add(
                "P7V-LI-BOTTLENECK",
                IssueSeverity.ERROR,
                "interaction_bottleneck must be graph-based",
                field="interaction_bottleneck",
                actual=bottleneck,
            )
        if items and bottleneck not in items:
            add(
                "P7V-LI-BOTTLENECK-ACTIVATION",
                IssueSeverity.ERROR,
                "interaction_bottleneck activation is missing",
                field="interaction_bottleneck",
                actual=bottleneck,
            )

    situation = result.life_situation
    if situation.situation_id not in SITUATION_IDS:
        add(
            "P7V-LI-SITUATION",
            IssueSeverity.ERROR,
            "unknown life situation",
            field="life_situation.situation_id",
            actual=situation.situation_id,
        )
    if situation.temporality != "window_bound":
        add(
            "P7V-LI-SITUATION-TEMPORALITY",
            IssueSeverity.CRITICAL,
            "life situation must stay window-bound",
            field="life_situation.temporality",
            actual=situation.temporality,
        )
    if situation.situation_id not in DRIVER_SENTINELS and situation.situation_id != "unresolved":
        for finding_id in situation.supporting_finding_ids:
            if finding_id not in finding_ids:
                add(
                    "P7V-LI-SITUATION-TRACE",
                    IssueSeverity.ERROR,
                    "life situation must be traceable to interaction findings",
                    field="life_situation.supporting_finding_ids",
                    actual=finding_id,
                )

    if natal is not None and activation is not None:
        for domain_id, item in activation.items.items():
            natal_item = natal_map.get(domain_id)
            if natal_item is None:
                continue
            if item.natal_state and item.natal_state != natal_item[0]:
                add(
                    "P7V-LI-MUTATE-DOMAIN",
                    IssueSeverity.CRITICAL,
                    "interaction must not rewrite natal Domain state",
                    field=f"{domain_id}.natal_state",
                    expected=natal_item[0],
                    actual=item.natal_state,
                )
            if item.natal_driver_id and natal_item[1] and item.natal_driver_id != natal_item[1]:
                add(
                    "P7V-LI-MUTATE-DOMAIN-DRIVER",
                    IssueSeverity.CRITICAL,
                    "interaction must not rewrite natal Domain driver",
                    field=f"{domain_id}.natal_driver_id",
                    expected=natal_item[1],
                    actual=item.natal_driver_id,
                )

    return result_from_issues(issues, analysis_id=analysis_id)


def _natal_states(context: CanonicalAnalysisContext | None) -> dict[str, tuple[str, str]]:
    if context is None:
        return {}
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
